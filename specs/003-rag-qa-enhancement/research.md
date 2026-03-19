# Research: RAG 问答系统增强

**Feature**: 003-rag-qa-enhancement  
**Date**: 2026-03-19  
**Status**: Complete

---

## 1. 交叉编码器重排方案

### Decision: 使用 BAAI/bge-reranker-base

### Rationale

1. **精度优势**：bge-reranker 系列在 MTEB 榜单上表现优异，适合中英文混合场景
2. **开源可用**：通过 sentence-transformers 直接加载，无额外 API 成本
3. **性能平衡**：base 版本（278M 参数）在精度和速度间取得良好平衡
4. **首次加载**：约 500MB 模型下载，后续使用本地缓存

### Alternatives Considered

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| bge-reranker-large | 精度更高 | 1.3GB，推理慢 | 规模过大 |
| bge-reranker-v2-m3 | 多语言支持最好 | 需要更新依赖 | 备选 |
| Cohere Rerank API | 无需本地模型 | 增加外部依赖和成本 | 违反本地优先原则 |
| LLM 重排（GPT） | 精度极高 | 延迟高、成本高 | 不适合实时场景 |

### Implementation Notes

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('BAAI/bge-reranker-base', max_length=512)

# 重排 Top-10 → Top-K
pairs = [(query, doc['content']) for doc in candidates]
scores = reranker.predict(pairs)
```

---

## 2. GPT 回答生成方案

### Decision: 使用 OpenAI GPT-4o-mini（默认），可选升级 GPT-4o

### Rationale

1. **已有集成**：项目已使用 OpenAI API 进行 Embedding，复用同一 SDK
2. **成本效益**：GPT-4o-mini 价格低（$0.15/1M input），质量足够专业问答
3. **速度满足**：300-500 字回答生成通常 < 3 秒
4. **灵活升级**：可配置切换到 GPT-4o 以获得更高质量

### Alternatives Considered

| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| 本地 LLM (Ollama) | 无 API 成本 | 质量不稳定，部署复杂 | 不推荐 |
| Claude API | 长上下文支持好 | 增加新依赖 | 备选 |
| 模板拼接 | 确定性输出 | 无法生成自然语言 | 不满足需求 |

### Prompt 设计原则

1. **System Prompt**：定义角色（SSBR 官能化专家）、输出格式、引用规范
2. **User Prompt**：包含查询 + 检索到的样本摘要（重排后 Top-3）
3. **约束**：
   - 必须引用样本 ID
   - 禁止编造数据
   - 区分文献数据与一般建议
   - 控制长度 300-500 字

### Token 估算

| 组成部分 | 估算 Token |
|----------|------------|
| System Prompt | ~200 |
| 查询 | ~50 |
| 3 个样本摘要（每个 ~800 字） | ~3000 |
| 回答输出 | ~600 |
| **总计** | ~3850 |

成本：约 $0.0006/次查询（GPT-4o-mini）

---

## 3. 低质量匹配处理策略

### Decision: 阈值 0.5 + 分层响应策略

### 响应层级

| 最高相似度 | 响应策略 | 回答类型 |
|------------|----------|----------|
| ≥ 0.7 | 正常问答 | 直接回答 + 引用 |
| 0.5 ~ 0.7 | 谨慎问答 | 回答 + "仅供参考"声明 |
| < 0.5 | 引导模式 | 引导性回答（无具体推荐） |

### 引导性回答内容

1. **问题分析**：解析用户查询意图，说明知识库覆盖范围
2. **通用建议**：提供 SSBR 官能化的一般性知识（不引用具体样本）
3. **查询优化提示**：建议用户调整查询关键词

### 示例引导性回答

```
## 分析结果

您的查询"XXX"在当前知识库中未找到高度相关的样本。

### 可能原因
- 知识库主要覆盖 SSBR 官能化改性研究
- 您的查询可能涉及知识库未收录的特定领域

### 一般性建议
[提供领域通用知识，明确标注"基于领域通用知识"]

### 建议调整查询
- 尝试关键词：白炭黑分散、滚动阻力、湿地抓地力、Tg 等
- 或描述具体的性能指标需求
```

---

## 4. 样本质量评估方案

### Decision: 基于 summary.md YAML front matter 字段完整性评估

### 评分维度

| 字段类别 | 关键字段 | 权重 |
|----------|----------|------|
| 官能化信息 | 官能化试剂、官能化程度、核心官能团 | 30% |
| 力学性能 | 拉伸强度、断裂伸长率、定伸应力 | 25% |
| 热学性能 | Tg | 15% |
| 动态性能 | tan δ (0℃)、tan δ (60℃) | 15% |
| 文献来源 | DOI、引文 | 15% |

### 评分公式

```python
def calculate_quality_score(summary_content: str) -> float:
    """
    计算样本质量分数 (0.0 - 1.0)
    
    基于字段完整性评估，缺失字段降权但不排除样本
    """
    score = 0.0
    
    # 检查各类关键字段是否存在且有有效值
    if has_valid_field(summary_content, '官能化试剂'): score += 0.10
    if has_valid_field(summary_content, '官能化程度'): score += 0.10
    if has_valid_field(summary_content, '核心官能团'): score += 0.10
    if has_valid_field(summary_content, '拉伸强度'): score += 0.10
    if has_valid_field(summary_content, '断裂伸长率'): score += 0.08
    if has_valid_field(summary_content, '定伸应力'): score += 0.07
    if has_valid_field(summary_content, 'Tg'): score += 0.15
    if has_valid_field(summary_content, 'tan δ'): score += 0.15
    if has_valid_field(summary_content, 'DOI'): score += 0.15
    
    return score
```

### 质量分数使用方式

1. **生成回答时**：质量分数作为信息权重，低质量样本信息以"仅供参考"形式呈现
2. **搜索结果展示**：标注样本完整性（如"数据完整度: 85%"）
3. **不排除**：即使质量分数低，只要相似度达标仍纳入结果

---

## 5. 依赖更新

### 新增依赖

```text
# requirements.txt 新增
sentence-transformers>=2.2.0    # bge-reranker 交叉编码器
```

### 依赖兼容性

| 依赖 | 现有版本 | 兼容性 |
|------|----------|--------|
| openai | >=1.0.0 | ✅ 无冲突 |
| numpy | >=1.24.0 | ✅ sentence-transformers 兼容 |
| torch | 自动安装 | ⚠️ 首次安装约 2GB |

### 首次运行注意

1. 安装 sentence-transformers 会自动安装 PyTorch
2. bge-reranker-base 模型首次加载需下载 ~500MB
3. 建议提供进度提示

---

## 6. 性能预估

### 端到端延迟拆解

| 步骤 | 预估延迟 | 说明 |
|------|----------|------|
| 查询向量化 | 0.2s | OpenAI Embedding API |
| 向量检索 Top-10 | 0.1s | 本地缓存 + 余弦相似度 |
| 重排 Top-10 → Top-3 | 0.5-0.8s | 本地 bge-reranker |
| 质量评估 | <0.1s | 本地字段检查 |
| GPT 生成回答 | 2-3s | OpenAI API（300-500 字） |
| **总计** | **3-4s** | ✅ 满足 <5s 目标 |

### 资源占用

| 资源 | 预估 |
|------|------|
| 内存（新增） | ~1GB（reranker 模型） |
| 磁盘（新增） | ~500MB（模型缓存） |
| API 成本/查询 | ~$0.001 |

---

## 7. 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| PyTorch 安装失败 | 中 | 高 | 提供详细安装指南，考虑 CPU-only 版本 |
| GPT API 延迟波动 | 中 | 中 | 设置超时，支持降级到纯推荐模式 |
| 重排模型首次加载慢 | 低 | 低 | 启动时预加载，显示进度 |
| 引用准确性问题 | 低 | 高 | 严格 Prompt 约束，后处理验证 |

---

## 8. 总结

所有技术选型已明确，无 NEEDS CLARIFICATION 项。

| 模块 | 选型 | 状态 |
|------|------|------|
| 重排 | bge-reranker-base | ✅ 确定 |
| 生成 | GPT-4o-mini | ✅ 确定 |
| 阈值 | 0.5 | ✅ 确定 |
| 质量评估 | 字段完整性 | ✅ 确定 |

可进入 Phase 1: 设计阶段。
