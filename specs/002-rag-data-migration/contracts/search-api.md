# Search API Contract: RAG 语义检索接口

**Date**: 2026-03-05 | **Branch**: `002-rag-data-migration`

## Overview

本文档定义 RAG 语义检索的接口契约，供 `ssbr-recommender` Skill 调用。

---

## Core Interface

### search(query, k=3) → SearchResult[]

语义检索主接口，基于用户查询返回相似样本。

#### Parameters

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| query | string | ✅ | - | 用户自然语言查询 |
| k | integer | ❌ | 3 | 返回结果数量 |
| threshold | float | ❌ | 0.0 | 最低相似度阈值 |

#### Returns

```typescript
interface SearchResult {
    sample_id: string;       // 样本 ID，如 "SSBR-001"
    similarity: float;       // 余弦相似度，范围 [0, 1]
    summary_path: string;    // summary.md 文件路径
    relevance: string;       // 相关性标签："高度相关" | "相关" | "参考"
}
```

#### Example

**Request:**
```
query: "我需要改善白炭黑分散性并降低滚动阻力"
k: 3
```

**Response:**
```json
[
    {
        "sample_id": "SSBR-001",
        "similarity": 0.89,
        "summary_path": "/dataset/interpretations/SSBR-001/summary.md",
        "relevance": "高度相关"
    },
    {
        "sample_id": "SSBR-005",
        "similarity": 0.72,
        "summary_path": "/dataset/interpretations/SSBR-005/summary.md",
        "relevance": "相关"
    },
    {
        "sample_id": "SSBR-012",
        "similarity": 0.58,
        "summary_path": "/dataset/interpretations/SSBR-012/summary.md",
        "relevance": "相关"
    }
]
```

---

## Relevance Classification

### 相似度 → 相关性映射

| 相似度范围 | 相关性标签 | 用户提示 |
|------------|------------|----------|
| ≥ 0.7 | 高度相关 | 直接推荐，无需额外说明 |
| 0.5 - 0.7 | 相关 | 正常推荐，可标注「相关度中等」 |
| < 0.5 | 参考 | 提示「知识库中无高度相关案例，以下为参考」 |

### 空结果处理

当知识库为空或所有样本缺少 summary.md 时：

```json
{
    "error": "NO_SEARCHABLE_SAMPLES",
    "message": "知识库中无可检索的样本，请先为样本生成 summary.md"
}
```

---

## Embedding Interface

### embed(text) → float[1536]

文本向量化接口，调用外部 Embedding API。

#### Parameters

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | ✅ | 待向量化的文本内容 |

#### Returns

```typescript
float[1536]  // OpenAI text-embedding-3-small 输出维度
```

#### Error Handling

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| API_TIMEOUT | 请求超时 | 记录日志，通知用户稍后重试 |
| RATE_LIMIT | 配额用尽 | 记录日志，通知用户 API 限制 |
| NETWORK_ERROR | 网络不可用 | 降级提示，建议检查网络 |

---

## MVP Implementation (Pseudo-code)

```python
import os
from pathlib import Path

def search(query: str, k: int = 3, threshold: float = 0.0) -> list[dict]:
    """
    语义检索主接口
    
    MVP 实现：遍历所有 summary.md，实时计算向量相似度
    """
    # 1. 获取查询向量
    query_embedding = embed(query)
    
    # 2. 遍历所有样本
    results = []
    interpretations_dir = Path("/dataset/interpretations")
    
    for sample_dir in interpretations_dir.iterdir():
        if not sample_dir.is_dir():
            continue
        if sample_dir.name == "TEMPLATE.md":
            continue
            
        summary_path = sample_dir / "summary.md"
        if not summary_path.exists():
            continue
        
        # 3. 读取 summary 内容
        summary_content = summary_path.read_text(encoding="utf-8")
        
        # 4. 计算相似度
        summary_embedding = embed(summary_content)
        similarity = cosine_similarity(query_embedding, summary_embedding)
        
        # 5. 应用阈值过滤
        if similarity >= threshold:
            results.append({
                "sample_id": sample_dir.name,
                "similarity": round(similarity, 2),
                "summary_path": str(summary_path),
                "relevance": classify_relevance(similarity)
            })
    
    # 6. 排序并返回 Top-K
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:k]


def classify_relevance(similarity: float) -> str:
    """相似度 → 相关性分类"""
    if similarity >= 0.7:
        return "高度相关"
    elif similarity >= 0.5:
        return "相关"
    else:
        return "参考"


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """计算余弦相似度"""
    import numpy as np
    v1, v2 = np.array(vec1), np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
```

---

## Chroma Migration Interface (Future)

当迁移到 Chroma 向量数据库后，接口保持不变，实现替换为：

```python
import chromadb

client = chromadb.PersistentClient(path="./vector_db")
collection = client.get_or_create_collection("summaries")

def search(query: str, k: int = 3, threshold: float = 0.0) -> list[dict]:
    """
    Chroma 实现：直接查询向量数据库
    """
    results = collection.query(
        query_texts=[query],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    
    # 转换为统一格式
    return [
        {
            "sample_id": results["ids"][0][i],
            "similarity": 1 - results["distances"][0][i],  # Chroma 返回距离，需转换
            "summary_path": results["metadatas"][0][i]["path"],
            "relevance": classify_relevance(1 - results["distances"][0][i])
        }
        for i in range(len(results["ids"][0]))
        if (1 - results["distances"][0][i]) >= threshold
    ]
```

---

## Integration with ssbr-recommender

### 调用流程

```
用户输入查询
      │
      ▼
┌─────────────────────────────────────────┐
│  ssbr-recommender Skill                  │
│                                          │
│  1. 调用 search(query, k=3)              │
│  2. 获取 Top-K SearchResult              │
│  3. 读取各样本 summary.md 全文           │
│  4. 读取 Excel 元数据                    │
│  5. 构建推荐上下文                        │
│  6. LLM 生成推荐结果                      │
└─────────────────────────────────────────┘
      │
      ▼
推荐输出（含推荐方案 + 参考案例 + 理由）
```

### 上下文构建模板

```markdown
## 检索到的相关案例

### 案例 1: SSBR-001 (相似度: 0.89, 高度相关)
[summary.md 全文内容]

### 案例 2: SSBR-005 (相似度: 0.72, 相关)
[summary.md 全文内容]

### 案例 3: SSBR-012 (相似度: 0.58, 相关)
[summary.md 全文内容]

---

基于以上案例，请为用户生成官能化方案推荐...
```

---

## Performance Contract

| 指标 | MVP 目标 | Chroma 目标 |
|------|----------|-------------|
| 单次检索延迟 | < 30 秒 | < 3 秒 |
| 全量向量化 (17 样本) | < 5 分钟 | < 30 秒 |
| 内存占用 | 无额外占用 | < 50 MB |

---

## Versioning

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-05 | 初始版本，MVP 实时计算方案 |
