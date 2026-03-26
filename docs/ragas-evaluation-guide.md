# RAGAS 评测 SSBR 问答系统指南

本文档介绍如何使用 RAGAS 框架评测 SSBR 问答系统的性能。

## 1. 什么是 RAGAS？

[RAGAS](https://docs.ragas.io/) (Retrieval Augmented Generation Assessment) 是一个专门用于评估 RAG 系统的开源框架，提供以下核心指标：

| 指标 | 说明 | 评估维度 |
|------|------|----------|
| **Faithfulness** | 回答是否忠实于检索到的上下文 | 检测幻觉 |
| **Answer Relevancy** | 回答与问题的相关性 | 回答质量 |
| **Context Precision** | 检索结果中相关文档的排序质量 | 检索排序 |
| **Context Recall** | 检索到的上下文覆盖了多少真实答案 | 检索召回 |

## 2. 安装依赖

```bash
# 安装 RAGAS 和相关依赖
pip install ragas datasets

# 或使用 requirements.txt
pip install -r requirements.txt
```

## 3. 运行评测

### 3.1 评测综合分析模块

```bash
python scripts/evaluation/ragas_evaluator.py --mode synthesis
```

### 3.2 评测单样本问答

```bash
python scripts/evaluation/ragas_evaluator.py --mode single
```

### 3.3 全面评测

```bash
python scripts/evaluation/ragas_evaluator.py --mode all --export both
```

## 4. 评测输出

评测完成后，报告会保存在 `evaluation/ragas_reports/` 目录下：

- `synthesis_report.md` - 综合分析评测报告（Markdown）
- `synthesis_report.csv` - 综合分析评测数据（CSV）
- `single_report.md` - 单样本问答评测报告

## 5. 评测指标解读

### 5.1 RAGAS 核心指标

| 指标 | 优秀 | 良好 | 需改进 |
|------|------|------|--------|
| Faithfulness | ≥0.9 | 0.7-0.9 | <0.7 |
| Answer Relevancy | ≥0.8 | 0.6-0.8 | <0.6 |
| Context Precision | ≥0.8 | 0.6-0.8 | <0.6 |
| Context Recall | ≥0.7 | 0.5-0.7 | <0.5 |

### 5.2 自定义指标（综合分析专用）

| 指标 | 说明 | 目标值 |
|------|------|--------|
| **Citation Accuracy** | 引用是否可追溯到源样本 | ≥0.9 |
| **Recommendation Completeness** | 推荐卡片是否包含所有必填字段 | ≥0.8 |

## 6. 自定义测试用例

编辑 `scripts/evaluation/ragas_evaluator.py` 中的测试集：

```python
SYNTHESIS_TEST_SAMPLES = [
    EvalSample(
        question="你的测试问题",
        ground_truth="标准答案（可选）",
        expected_samples=["SSBR-002", "SSBR-003"],  # 期望检索到的样本
        category="分类",
        difficulty="easy/medium/hard"
    ),
    # 添加更多测试用例...
]
```

## 7. 与现有评测的区别

| 维度 | 现有评测 (`evaluate_rag.py`) | RAGAS 评测 |
|------|------------------------------|------------|
| **评估对象** | 检索系统 | 完整问答链路 |
| **核心指标** | Hit Rate, Precision, MRR | Faithfulness, Relevancy |
| **是否需要 LLM** | ❌ | ✅ (评估用) |
| **幻觉检测** | ❌ | ✅ |
| **适用场景** | 检索调优 | 端到端质量评估 |

## 8. 高级用法

### 8.1 使用本地 LLM 评估

```python
from scripts.evaluation import RAGASEvaluator

evaluator = RAGASEvaluator(use_local_llm=True)
```

### 8.2 自定义指标

```python
from ragas.metrics import NumericalMetric

# 定义自定义指标
custom_metric = NumericalMetric(
    name="domain_accuracy",
    prompt="Rate the domain accuracy of the response (1-5)...",
    allowed_values=(1, 5),
)
```

### 8.3 批量评测与 CI 集成

```bash
# 运行评测并检查阈值
python scripts/evaluation/ragas_evaluator.py --mode synthesis --threshold 0.7
```

## 9. 常见问题

### Q: RAGAS 评测很慢？

RAGAS 需要调用 LLM 来评估每个样本，这会增加评测时间。建议：
- 减少测试用例数量（精选代表性样本）
- 使用更快的 LLM 模型
- 并行处理多个样本

### Q: Faithfulness 分数很低？

可能原因：
1. 回答包含未在上下文中出现的信息（幻觉）
2. 上下文质量不高
3. Prompt 没有强调基于上下文回答

### Q: 如何提高 Context Precision？

1. 优化检索算法（embedding 模型、重排器）
2. 改善文档分块策略
3. 调整 top-k 参数

---

*更多信息请参考 [RAGAS 官方文档](https://docs.ragas.io/)*
