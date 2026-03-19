# Data Model: RAG 问答系统增强

**Feature**: 003-rag-qa-enhancement  
**Date**: 2026-03-19  
**Status**: Complete

---

## 1. 实体定义

### 1.1 Query（查询）

用户输入的自然语言问题。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| raw_text | string | ✓ | 用户原始输入 |
| processed_text | string | ✓ | 预处理后的查询文本 |
| embedding | List[float] | ✓ | 1536 维向量（text-embedding-3-small） |
| timestamp | datetime | ✓ | 查询时间 |

**验证规则**:
- raw_text 长度 > 0 且 < 1000 字符
- 非空白字符数 > 2

---

### 1.2 Candidate（候选样本）

初步向量检索返回的样本。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sample_id | string | ✓ | 样本 ID（如 SSBR-002） |
| similarity | float | ✓ | 余弦相似度 (0.0 - 1.0) |
| content | string | ✓ | summary.md 正文内容 |
| summary_path | string | ✓ | 文件路径 |

**来源**: `RAGSearchEngine.search()` 返回的 Top-10 结果

---

### 1.3 RankedResult（重排结果）

经过交叉编码器重排后的样本。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sample_id | string | ✓ | 样本 ID |
| original_rank | int | ✓ | 重排前排名 (1-based) |
| rerank_score | float | ✓ | 重排分数（交叉编码器输出） |
| final_rank | int | ✓ | 重排后排名 (1-based) |
| similarity | float | ✓ | 原始余弦相似度 |
| quality_score | float | ✓ | 样本质量分数 (0.0 - 1.0) |
| content | string | ✓ | summary.md 正文内容 |

**状态转换**:
```
Candidate → (Reranker) → RankedResult
```

---

### 1.4 QualityScore（质量分数）

基于字段完整性的样本数据评估。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sample_id | string | ✓ | 样本 ID |
| overall_score | float | ✓ | 综合质量分数 (0.0 - 1.0) |
| functionalization_score | float | ✓ | 官能化信息完整度 |
| mechanical_score | float | ✓ | 力学性能完整度 |
| thermal_score | float | ✓ | 热学性能完整度 |
| dynamic_score | float | ✓ | 动态性能完整度 |
| source_score | float | ✓ | 文献来源完整度 |
| missing_fields | List[string] | ✓ | 缺失的关键字段列表 |

**计算公式**:
```python
overall_score = (
    functionalization_score * 0.30 +
    mechanical_score * 0.25 +
    thermal_score * 0.15 +
    dynamic_score * 0.15 +
    source_score * 0.15
)
```

---

### 1.5 GeneratedAnswer（生成回答）

系统生成的自然语言回答。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| answer_text | string | ✓ | 回答正文（Markdown 格式） |
| answer_type | AnswerType | ✓ | 回答类型枚举 |
| citations | List[Citation] | ✓ | 引用列表 |
| confidence | ConfidenceLevel | ✓ | 置信度级别 |
| query | string | ✓ | 原始查询 |
| source_samples | List[string] | ✓ | 参考的样本 ID 列表 |
| generation_time_ms | int | ✓ | 生成耗时（毫秒） |
| model_used | string | ✓ | 使用的模型（如 gpt-4o-mini） |

**AnswerType 枚举**:
| 值 | 说明 |
|-----|------|
| DIRECT | 直接回答（相似度 ≥ 0.7） |
| REFERENCE | 参考回答（相似度 0.5-0.7） |
| GUIDANCE | 引导性回答（相似度 < 0.5） |

**ConfidenceLevel 枚举**:
| 值 | 说明 |
|-----|------|
| HIGH | 高置信度（基于高质量、高相似度样本） |
| MEDIUM | 中等置信度 |
| LOW | 低置信度（引导性回答或低质量样本） |

---

### 1.6 Citation（引用）

回答中的数据来源引用。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sample_id | string | ✓ | 样本 ID |
| doi | string | ○ | 文献 DOI |
| citation_text | string | ○ | 引文格式（期刊, 年份, 页码） |
| data_type | string | ✓ | 引用数据类型（如"力学性能"） |

---

## 2. 关系图

```
┌─────────────┐
│    Query    │
└──────┬──────┘
       │ 1:N
       ▼
┌─────────────┐      ┌─────────────────┐
│  Candidate  │─────▶│  QualityScore   │
└──────┬──────┘ 1:1  └─────────────────┘
       │ 1:1
       ▼
┌─────────────┐
│ RankedResult│
└──────┬──────┘
       │ N:1
       ▼
┌─────────────────┐      ┌─────────────┐
│ GeneratedAnswer │─────▶│   Citation  │
└─────────────────┘ 1:N  └─────────────┘
```

---

## 3. 数据流

```
用户输入
    │
    ▼
┌────────────────┐
│ Query 预处理   │ → Query 对象
└────────────────┘
    │
    ▼
┌────────────────┐
│ 向量检索 Top-10│ → List[Candidate]
└────────────────┘
    │
    ▼
┌────────────────┐
│ 质量评估       │ → 附加 QualityScore
└────────────────┘
    │
    ▼
┌────────────────┐
│ 重排 → Top-3   │ → List[RankedResult]
└────────────────┘
    │
    ▼
┌────────────────┐
│ 判断回答类型   │ → AnswerType
└────────────────┘
    │
    ├─── DIRECT/REFERENCE ───┐
    │                        ▼
    │              ┌──────────────────┐
    │              │ GPT 生成回答     │
    │              └──────────────────┘
    │                        │
    └─── GUIDANCE ───────────┤
                             ▼
                   ┌──────────────────┐
                   │ GeneratedAnswer  │
                   └──────────────────┘
```

---

## 4. 存储设计

### 4.1 现有存储（不变）

| 存储 | 路径 | 说明 |
|------|------|------|
| 向量缓存 | `.cache/vector_cache.json` | 文档向量预计算 |
| 样本文档 | `dataset/interpretations/*/summary.md` | 82 个样本 |
| 元数据 | `dataset/数据.xlsx` | Excel 元数据 |

### 4.2 新增存储（可选）

| 存储 | 路径 | 说明 |
|------|------|------|
| 质量分数缓存 | `.cache/quality_scores.json` | 预计算的质量分数 |
| 重排模型 | `~/.cache/huggingface/` | bge-reranker 模型（自动管理） |

### 4.3 质量分数缓存结构

```json
{
  "version": "1.0",
  "updated_at": "2026-03-19T...",
  "scores": {
    "SSBR-002": {
      "overall_score": 0.95,
      "functionalization_score": 1.0,
      "mechanical_score": 1.0,
      "thermal_score": 0.8,
      "dynamic_score": 1.0,
      "source_score": 1.0,
      "missing_fields": ["tan_delta_60"],
      "content_hash": "abc123..."
    }
  }
}
```

---

## 5. 验证规则汇总

| 实体 | 规则 | 错误处理 |
|------|------|----------|
| Query | 非空，< 1000 字符 | 返回错误提示 |
| Candidate | similarity ∈ [0, 1] | 跳过异常样本 |
| RankedResult | rerank_score 有效 | 保留原始排名 |
| QualityScore | overall_score ∈ [0, 1] | 默认 0.5 |
| GeneratedAnswer | answer_text 非空 | 回退到推荐列表 |
| Citation | sample_id 存在 | 移除无效引用 |

---

## 6. 与现有代码的映射

| 数据模型 | 现有代码位置 | 修改类型 |
|----------|--------------|----------|
| Query | `rag_search.py:QueryPreprocessor` | 扩展 |
| Candidate | `rag_search.py:SearchResult` | 兼容 |
| RankedResult | 新增 `reranker.py:RankedResult` | 新增 |
| QualityScore | 新增 `quality_scorer.py:QualityScore` | 新增 |
| GeneratedAnswer | 新增 `answer_generator.py:GeneratedAnswer` | 新增 |
| Citation | 新增 `answer_generator.py:Citation` | 新增 |
