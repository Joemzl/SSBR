# QA API Contract: RAG 问答系统

**Feature**: 003-rag-qa-enhancement  
**Version**: 1.0.0  
**Date**: 2026-03-19

---

## 概述

本契约定义 RAG 问答系统的核心接口，包括问答 API、重排 API 和质量评估 API。

---

## 1. 问答主接口

### `QAEngine.answer()`

基于用户查询生成专业回答。

**签名**:
```python
def answer(
    query: str,
    top_k: int = 3,
    include_samples: bool = True,
    model: str = "gpt-4o-mini"
) -> QAResponse
```

**参数**:
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | str | - | 用户查询（必填） |
| top_k | int | 3 | 用于生成回答的样本数 |
| include_samples | bool | True | 是否返回样本列表 |
| model | str | "gpt-4o-mini" | 生成模型 |

**返回**:
```python
@dataclass
class QAResponse:
    answer: GeneratedAnswer       # 生成的回答
    samples: List[RankedResult]   # 重排后的样本列表
    search_time_ms: int           # 检索耗时
    rerank_time_ms: int           # 重排耗时
    generation_time_ms: int       # 生成耗时
    total_time_ms: int            # 总耗时
```

**示例**:
```python
from scripts.qa_engine import QAEngine

engine = QAEngine()
response = engine.answer("如何改善白炭黑分散性？")

print(response.answer.answer_text)
print(f"总耗时: {response.total_time_ms}ms")
```

**错误处理**:
| 错误类型 | 触发条件 | 处理方式 |
|----------|----------|----------|
| ValueError | 查询为空或过长 | 抛出异常 |
| EmbeddingError | Embedding API 失败 | 抛出异常 |
| GenerationError | GPT API 失败 | 回退到纯推荐模式 |

---

## 2. 重排接口

### `Reranker.rerank()`

对候选样本进行重排序。

**签名**:
```python
def rerank(
    query: str,
    candidates: List[Candidate],
    top_k: int = 3
) -> List[RankedResult]
```

**参数**:
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | str | - | 用户查询 |
| candidates | List[Candidate] | - | 候选样本列表 |
| top_k | int | 3 | 返回结果数 |

**返回**: 重排后的 Top-K 样本，按 `rerank_score` 降序。

**契约保证**:
1. 输出数量 ≤ min(top_k, len(candidates))
2. 保留原始 similarity 字段
3. 新增 rerank_score 和 final_rank 字段

---

## 3. 质量评估接口

### `QualityScorer.score()`

计算样本质量分数。

**签名**:
```python
def score(sample_id: str, content: str) -> QualityScore
```

**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| sample_id | str | 样本 ID |
| content | str | summary.md 内容 |

**返回**: `QualityScore` 对象（详见 data-model.md）

### `QualityScorer.batch_score()`

批量计算质量分数（带缓存）。

**签名**:
```python
def batch_score(
    samples: List[Dict[str, str]],
    use_cache: bool = True
) -> Dict[str, QualityScore]
```

---

## 4. 回答生成接口

### `AnswerGenerator.generate()`

基于重排结果生成回答。

**签名**:
```python
def generate(
    query: str,
    ranked_results: List[RankedResult],
    answer_type: AnswerType
) -> GeneratedAnswer
```

**参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| query | str | 用户查询 |
| ranked_results | List[RankedResult] | 重排后的样本 |
| answer_type | AnswerType | 回答类型（DIRECT/REFERENCE/GUIDANCE） |

**回答类型判定规则**:
```python
def determine_answer_type(max_similarity: float) -> AnswerType:
    if max_similarity >= 0.7:
        return AnswerType.DIRECT
    elif max_similarity >= 0.5:
        return AnswerType.REFERENCE
    else:
        return AnswerType.GUIDANCE
```

**回答长度约束**:
- DIRECT: 400-500 字
- REFERENCE: 300-400 字 + "仅供参考"声明
- GUIDANCE: 200-300 字（无具体样本引用）

---

## 5. Gradio Web 接口

### 搜索并生成回答

**函数**: `search_and_answer(query: str, top_k: int) -> Tuple`

**返回**:
```python
(
    answer_html: str,      # 生成回答（HTML/Markdown）
    samples_html: str,     # 样本列表（HTML/Markdown）
    dropdown_choices: List[str],  # 样本下拉选项
    stats_text: str        # 性能统计
)
```

### 向后兼容

保留原有接口 `search_samples()`，新增 `search_and_answer()` 接口。

UI 布局更新:
```
┌─────────────────────────────────────┐
│ 查询输入框                          │
├─────────────────────────────────────┤
│ [检索并生成回答] [仅检索推荐]        │
├─────────────────────────────────────┤
│ 📝 AI 回答                          │
│ ┌─────────────────────────────────┐ │
│ │ 生成的专业回答...               │ │
│ └─────────────────────────────────┘ │
├─────────────────────────────────────┤
│ 📋 相关样本列表                     │
│ ┌─────────────────────────────────┐ │
│ │ 1. SSBR-002 (匹配度: 高)       │ │
│ │ 2. SSBR-015 (匹配度: 中)       │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## 6. 错误码定义

| 错误码 | 名称 | 说明 |
|--------|------|------|
| QA001 | EMPTY_QUERY | 查询为空 |
| QA002 | QUERY_TOO_LONG | 查询超过 1000 字符 |
| QA003 | EMBEDDING_FAILED | Embedding API 调用失败 |
| QA004 | RERANK_FAILED | 重排模型加载或推理失败 |
| QA005 | GENERATION_FAILED | GPT API 调用失败 |
| QA006 | NO_SAMPLES | 没有可检索的样本 |

---

## 7. 性能契约

| 指标 | 目标值 | 测量方式 |
|------|--------|----------|
| 端到端延迟 | < 5000ms | total_time_ms |
| 重排延迟 | < 1000ms | rerank_time_ms |
| 生成延迟 | < 3000ms | generation_time_ms |
| 引用准确率 | 100% | 人工抽检 |

---

## 8. 版本兼容性

| 版本 | 变更 | 兼容性 |
|------|------|--------|
| 1.0.0 | 初始版本 | - |

**向后兼容承诺**:
- `RAGSearchEngine.search()` 接口保持不变
- 新增 `QAEngine` 类，不修改现有类
- UI 保留"仅检索推荐"模式
