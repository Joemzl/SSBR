# Quick Start: RAG 问答系统增强

**Feature**: 003-rag-qa-enhancement  
**Date**: 2026-03-19

---

## 前置条件

- Python 3.10+
- OpenAI API Key（已有）
- 现有 SSBR 项目环境

---

## 1. 安装新依赖

```bash
cd d:\SSBR

# 安装 sentence-transformers（用于重排）
pip install sentence-transformers>=2.2.0
```

> ⚠️ 首次安装会自动安装 PyTorch（约 2GB），请耐心等待。

---

## 2. 预下载重排模型（可选）

```python
# 预下载 bge-reranker-base 模型（约 500MB）
from sentence_transformers import CrossEncoder
reranker = CrossEncoder('BAAI/bge-reranker-base')
```

或在首次查询时自动下载。

---

## 3. 启动问答系统

```bash
cd d:\SSBR
python demo/app.py
```

访问 http://localhost:7861

---

## 4. 使用问答功能

### Web 界面

1. 输入问题，如："如何改善白炭黑分散性？"
2. 点击 **[检索并生成回答]**
3. 查看 AI 生成的专业回答
4. 可选：查看相关样本列表获取详细信息

### Python API

```python
from scripts.qa_engine import QAEngine

engine = QAEngine()
response = engine.answer("如何改善白炭黑分散性？")

# 查看生成的回答
print(response.answer.answer_text)

# 查看引用的样本
for citation in response.answer.citations:
    print(f"- {citation.sample_id}: {citation.doi}")
```

---

## 5. 配置选项

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| OPENAI_API_KEY | - | OpenAI API 密钥（必填） |
| QA_MODEL | gpt-4o-mini | 生成模型 |
| QA_MAX_TOKENS | 800 | 最大回答长度 |
| RERANK_TOP_K | 3 | 重排后保留数量 |

### 代码配置

```python
# scripts/qa_engine.py
DEFAULT_CONFIG = {
    "similarity_threshold": 0.5,     # 低质量匹配阈值
    "rerank_candidates": 10,         # 重排候选数
    "answer_max_length": 500,        # 回答最大字数
    "model": "gpt-4o-mini"           # 默认模型
}
```

---

## 6. 验证安装

```bash
# 测试重排模块
python -c "from scripts.reranker import Reranker; print('Reranker OK')"

# 测试问答引擎
python -c "from scripts.qa_engine import QAEngine; print('QAEngine OK')"

# 测试完整问答流程（需要 OPENAI_API_KEY）
python scripts/qa_engine.py --query "如何改善白炭黑分散性？" --no-rerank
```

---

## 7. 常见问题

### Q: 首次运行很慢？

A: 正在下载 bge-reranker 模型（约 500MB）。后续运行会使用本地缓存。

### Q: 内存不足？

A: 重排模型约占用 1GB 内存。如果内存紧张，可以：
1. 减小 `rerank_candidates` 参数
2. 使用 `bge-reranker-base` 而非 large 版本（默认已是 base）

### Q: GPT API 超时？

A: 生成回答默认超时 30 秒。可通过以下方式调整：
```python
engine = QAEngine(generation_timeout=60)
```

### Q: 如何回退到纯推荐模式？

A: Web 界面点击 **[仅检索推荐]** 按钮，或 API 调用：
```python
results = engine.search_only("查询")  # 不生成回答
```

---

## 8. 下一步

- 查看 [API 契约](./contracts/qa-api.md) 了解详细接口
- 查看 [数据模型](./data-model.md) 了解数据结构
- 查看 [研究文档](./research.md) 了解技术选型
