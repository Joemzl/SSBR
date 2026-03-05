# Research: RAG 推荐系统数据架构重构

**Date**: 2026-03-05 | **Branch**: `002-rag-data-migration`

## Research Tasks

基于技术上下文和需求分析，识别以下需要研究的问题：

---

## 1. Embedding API 选型

### Question
选择哪个 Embedding API 进行向量化？

### Decision
**OpenAI text-embedding-3-small (1536 维)**

### Rationale
- 17 条数据量小，API 调用成本可忽略（约 $0.01/次全量向量化）
- 1536 维向量在语义理解上表现优秀
- 广泛使用，文档完善，易于集成
- 支持中英文混合文本（summary.md 含专业术语）

### Alternatives Considered
| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| OpenAI text-embedding-3-small | 性价比高，效果好 | 需网络连接 | ✅ 选用 |
| OpenAI text-embedding-3-large | 效果更好 | 成本更高，17条无必要 | ❌ 过度 |
| 智谱 embedding-3 | 国内访问稳定 | 需另开账号 | 🔄 备选 |
| 本地模型 (sentence-transformers) | 离线可用 | 部署复杂，效果不稳定 | ❌ 不符合轻量化原则 |

---

## 2. 向量存储方案

### Question
向量数据如何存储和检索？

### Decision
**MVP: 纯文件 + 实时 Embedding 计算**

### Rationale
- 17 条数据极少，实时计算延迟约 5-10 秒（可接受）
- 零部署成本，无需安装向量数据库
- 数据层与向量层解耦，未来迁移成本低
- 符合宪法「轻量化与可维护性」原则

### Implementation Details
```
检索流程：
1. 用户输入查询 → 调用 Embedding API 获得查询向量 (1536维)
2. 遍历 /interpretations/*/summary.md → 逐个调用 Embedding API
3. 计算余弦相似度 → 返回 Top-K (默认 K=3)
```

### Future Migration Path
参见 spec.md 中的 "Vector Storage Evolution Guide" 章节。

---

## 3. YAML Front Matter 解析

### Question
如何解析解读文档中的 YAML front matter？

### Decision
**使用 Python yaml 库 + 正则提取**

### Rationale
- Python yaml 是标准库，无额外依赖
- YAML front matter 格式简单（`---` 包裹）
- Skills 环境（CodeBuddy）可直接执行 Python 代码块

### Implementation Pattern
```python
import yaml
import re

def parse_yaml_frontmatter(content: str) -> dict:
    """提取 Markdown 文件的 YAML front matter"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return {}
```

---

## 4. Excel 数据迁移策略

### Question
如何安全地将 Excel P-W 列数据迁移到解读文档？

### Decision
**三阶段迁移：备份 → 写入文档 → 删除列**

### Rationale
- 备份确保数据安全，可回滚
- 先写入后删除，确保迁移完整性
- 校验脚本验证数据一致性

### Migration Steps
1. **备份阶段**
   - 复制 `数据.xlsx` → `数据_backup_20260305.xlsx`
   - 记录原始数据 MD5 校验和

2. **写入阶段**
   - 读取 Excel P-W 列数据
   - 为每个样本创建/更新 mechanical.md 和 dsc.md
   - 将数值写入 YAML front matter 的 `data:` 部分

3. **验证阶段**
   - 对比解读文档中的数值与 Excel 原始数据
   - 生成验证报告，确保 100% 一致

4. **清理阶段**
   - 删除 Excel P-W 列
   - 保存瘦身后的 Excel（仅 A-O 列）

### Column Mapping
| Excel 列 | 目标文件 | YAML 字段 |
|----------|----------|-----------|
| P (100%定伸应力) | mechanical.md | `data.stress_100.value` |
| Q (200%定伸应力) | mechanical.md | `data.stress_200.value` |
| R (300%定伸应力) | mechanical.md | `data.stress_300.value` |
| S (拉伸强度) | mechanical.md | `data.tensile_strength.value` |
| T (断裂伸长率) | mechanical.md | `data.elongation.value` |
| U (力学数据来源) | mechanical.md | `data.mechanical_source` |
| V (Tg) | dsc.md | `data.tg.value` |
| W (热学数据来源) | dsc.md | `data.thermal_source` |

---

## 5. Summary 生成策略

### Question
如何自动生成高质量的 summary.md？

### Decision
**基于模板的 LLM 生成 + 结构化数据填充**

### Rationale
- summary.md 需要自然语言描述，适合 LLM 生成
- 结构化部分（官能化信息、关键指标）直接从数据提取
- 模板约束确保内容完整性和一致性

### Generation Flow
```
输入：
├── Excel A-O 列元数据
├── /interpretations/{sample_id}/mechanical.md
├── /interpretations/{sample_id}/dsc.md
├── /interpretations/{sample_id}/nmr.md (如有)
└── /interpretations/{sample_id}/tem.md (如有)

处理：
├── 提取各文档 YAML 数值
├── 提取各文档「核心发现」章节
├── LLM 综合生成自然语言描述
└── 填充模板结构

输出：
└── /interpretations/{sample_id}/summary.md
```

### Template Structure
参见 `/dataset/interpretations/TEMPLATE.md` 中的 summary.md 模板。

---

## 6. Skills 输出格式调整

### Question
现有 7 个解读 Skills 如何调整输出格式？

### Decision
**统一采用 YAML front matter + Markdown 正文格式**

### Rationale
- 结构化数据（YAML）支持程序化提取
- 自然语言描述（Markdown）保持人类可读性
- 统一格式简化 summary 生成逻辑

### Skills Update Scope

| Skill | 当前输出 | 目标输出 | 变更量 |
|-------|----------|----------|--------|
| ssbr-stress-strain-interpretation | Markdown | YAML + MD → mechanical.md | 中 |
| ssbr-payne-interpretation | Markdown | YAML + MD → mechanical.md (追加) | 中 |
| ssbr-dma-interpretation | Markdown | YAML + MD → mechanical.md (追加) | 中 |
| ssbr-dsc-interpretation | Markdown | YAML + MD → dsc.md | 中 |
| ssbr-nmr-interpretation | Markdown | YAML + MD → nmr.md | 中 |
| ssbr-tem-interpretation | Markdown | YAML + MD → tem.md | 中 |
| ssbr-mechanical-interpretation | 调度层 | 更新调度逻辑 | 小 |
| **ssbr-summary-generator** | 新增 | 读取数据生成 summary.md | **新建** |
| ssbr-recommender | Excel 读取 | RAG 向量检索 | 大 |

---

## 7. 检索相似度阈值

### Question
语义检索的相似度阈值如何设定？

### Decision
**相似度 < 0.5 时提示「无高度相关案例」**

### Rationale
- 0.5 为余弦相似度的中值
- 低于此值表示语义相关性弱
- 用户可获得最接近的参考（即使相似度低）

### Threshold Behavior
| 最高相似度 | 系统行为 |
|------------|----------|
| ≥ 0.7 | 正常推荐，标注「高度相关」 |
| 0.5 - 0.7 | 正常推荐，标注「相关」 |
| < 0.5 | 提示「知识库中无高度相关案例」，展示最接近的 Top-3 作为参考 |

---

## 8. 并发与文件冲突

### Question
多人同时操作时如何避免文件冲突？

### Decision
**基于 Git 的版本控制 + 文件级锁定**

### Rationale
- 项目已使用 Git 管理
- 解读文档按样本隔离，冲突概率低
- 实际使用场景为单人学术研究，并发需求低

### Conflict Prevention
1. **样本级隔离**：每个样本独立目录，不同样本互不影响
2. **Git 版本控制**：所有变更可追溯、可回滚
3. **Excel 单一写入**：元数据修改走 Git PR 流程

---

## Research Summary

| 问题 | 决策 | 风险等级 |
|------|------|----------|
| Embedding API | OpenAI text-embedding-3-small | 🟢 低 |
| 向量存储 | 纯文件 + 实时计算 | 🟢 低 |
| YAML 解析 | Python yaml + 正则 | 🟢 低 |
| 数据迁移 | 三阶段：备份→写入→删除 | 🟡 中（需谨慎执行） |
| Summary 生成 | 模板 + LLM | 🟢 低 |
| Skills 格式 | YAML + Markdown 统一 | 🟢 低 |
| 相似度阈值 | 0.5 | 🟢 低（可调整） |
| 并发控制 | Git + 样本隔离 | 🟢 低 |

**所有 NEEDS CLARIFICATION 已解决，可进入 Phase 1 设计阶段。**
