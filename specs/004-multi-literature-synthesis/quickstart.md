# Quickstart: 多文献综合推理问答系统

**Feature**: 004-multi-literature-synthesis  
**Date**: 2026-03-24

---

## 概述

本功能将 SSBR 问答系统从"单样本检索"升级为"多文献综合推理"，支持：

- 🔄 **多文献综合**：综合 3-8 个样本生成整合性回答
- 📈 **趋势分析**：从数据中提取规律和趋势
- 🔮 **保守外推**：基于数据趋势进行有限范围的预测
- ⚖️ **对比分析**：多方案结构化对比
- 🧪 **配方设计**：根据目标性能生成配方建议

---

## 快速开始

### 1. 基本使用（兼容 003）

```python
from scripts.qa_engine import get_qa_engine

engine = get_qa_engine()

# 原有方式继续工作
response = engine.answer("如何改善白炭黑分散性？")
print(response.answer.answer_text)
```

### 2. 启用综合模式

```python
from scripts.qa_engine import get_qa_engine
from scripts.models import SynthesisMode

engine = get_qa_engine()

# 自动检测模式（推荐）
response = engine.answer(
    "官能化程度如何影响力学性能？",
    synthesis_mode=None  # 自动检测
)

# 强制综合模式
response = engine.answer(
    "综合分析羟基和羧基官能化的效果",
    synthesis_mode=SynthesisMode.SYNTHESIS
)
```

### 3. 专用综合方法

```python
# 多文献综合
response = engine.synthesize(
    query="如何同时改善分散性和湿地抓地力？",
    top_k=8,
    enable_trend=True,
    enable_extrapolation=True
)

# 查看综合结果
print(f"引用文献数: {response.answer.get_citation_count()}")
print(f"趋势分析: {response.answer.trend_analysis}")
print(f"外推预测: {response.answer.extrapolation}")
```

### 4. 对比分析

```python
response = engine.compare(
    schemes=["羟基官能化", "氨基官能化", "环氧官能化"],
    dimensions=["拉伸强度", "Tg", "分散效果", "Payne效应"]
)

# 输出 Markdown 表格
print(response.answer.comparison.to_markdown())
```

输出示例：
```markdown
| 方案 | 拉伸强度 | Tg | 分散效果 | Payne效应 |
|---|---|---|---|---|
| 羟基官能化 | 18.5 MPa | -28°C | 优良 | 降低 35% |
| 氨基官能化 | 16.2 MPa | -25°C | 良好 | 降低 28% |
| 环氧官能化 | 17.8 MPa | -30°C | 优良 | 降低 32% |

综合来看，羟基官能化在分散效果和 Payne 效应改善上表现最优...
```

### 5. 配方设计

```python
response = engine.design_formula(
    target_properties={
        "湿地抓地力": "高",
        "滚动阻力": "低",
        "分散性": "优良"
    },
    constraints={
        "官能化程度": "<10%"
    }
)

formula = response.answer.formula
print(f"推荐官能团: {formula.recommended_functional_group}")
print(f"推荐程度: {formula.recommended_degree}")
print(f"预期性能: {formula.expected_performance}")
print(f"取舍说明: {formula.trade_offs}")
```

---

## 输出结构

### 分层回答格式

所有综合回答采用分层结构：

```markdown
## 结论摘要

羟基官能化是改善白炭黑分散性的有效方案，官能化程度在 3-8% 时效果最佳。

## 详细分析

### 1. 分散性改善机理

羟基官能团与白炭黑表面硅醇基形成氢键...

**数据支撑**：根据 Zhang 等人的研究，3.6% 羟基官能化使 Payne 效应降低 35%。

### 2. 最佳官能化程度

综合多项研究，3-8% 为最佳区间...

## 文献来源

1. Zhang et al., Polymer, 2023
2. Li et al., Rubber Chemistry, 2024

---

⚠️ 中等置信度（基于 5 个相近样本）
```

### 外推预测格式

```markdown
⚠️ **外推估计**：在 5% 官能化程度下，预计拉伸强度为 14-17 MPa
（中等置信度，基于 4 个相近样本）

⚠️ 注意：此预测超出数据覆盖范围（1%-15% 外推至 0.5%-22.5%），仅供参考
```

---

## 配置选项

### 环境变量

```bash
# 外推控制
EXTRAPOLATION_BOUNDARY=0.5  # 外推边界比例（默认 50%）
MIN_SAMPLES_TREND=3         # 趋势分析最小样本数
MIN_SAMPLES_COMPARE=2       # 对比分析最小样本数

# 性能调优
SYNTHESIS_TOP_K=8           # 综合检索默认样本数
SYNTHESIS_TIMEOUT=8000      # 综合问答超时时间（毫秒）
```

### 代码配置

```python
from scripts.qa_engine import QAEngineConfig

config = QAEngineConfig(
    # 现有配置保持不变
    similarity_threshold_high=0.7,
    similarity_threshold_low=0.5,
    rerank_candidates=10,
    rerank_top_k=3,
    
    # 新增综合配置
    synthesis_top_k=8,
    min_samples_trend=3,
    min_samples_compare=2,
    extrapolation_boundary=0.5,
    synthesis_timeout=8000,
)

engine = QAEngine(config=config)
```

---

## CLI 使用

```bash
# 综合问答
python scripts/qa_engine.py --query "官能化程度如何影响性能？" --synthesize

# 对比分析
python scripts/qa_engine.py --compare "羟基官能化" "氨基官能化"

# 配方设计
python scripts/qa_engine.py --design --target "湿地抓地力:高,滚动阻力:低"

# 禁用外推
python scripts/qa_engine.py --query "5%官能化的拉伸强度" --no-extrapolation
```

---

## Web Demo

```bash
# 启动 Demo（自动启用综合模式）
python demo/app.py

# 访问 http://localhost:7861
```

Demo 界面新增：
- 🔄 综合模式开关
- 📊 对比分析标签页
- 🧪 配方设计标签页
- 📈 趋势可视化（可选）

---

## 错误处理

```python
from scripts.utils.exceptions import (
    InsufficientDataError,
    ExtrapolationBoundaryError,
    ConflictingTargetsError
)

try:
    response = engine.synthesize("50% 官能化的效果？")
except ExtrapolationBoundaryError as e:
    print(f"查询超出范围: {e.query_value} {e.unit}")
    print(f"允许范围: {e.allowed_range}")
except InsufficientDataError as e:
    print(f"数据不足: 需要 {e.required} 个样本，仅找到 {e.actual} 个")
```

---

## 验证检查

```python
response = engine.synthesize("...")

# 检查是否满足规格要求
errors = response.answer.validate()
if errors:
    print(f"验证警告: {errors}")

# 检查性能目标
if not response.meets_performance_target():
    print(f"响应超时: {response.total_time_ms}ms > 8000ms")

# 检查引用数量
if response.answer.get_citation_count() < 2:
    print("警告: 引用文献数量不足 2 篇")
```

---

## 常见问题

### Q: 综合模式和单样本模式有什么区别？

| 特性 | 单样本模式 (003) | 综合模式 (004) |
|------|-----------------|----------------|
| 检索数量 | Top-3 | Top-8 |
| 回答来源 | 单一最佳样本 | 多文献综合 |
| 趋势分析 | ❌ | ✅ |
| 外推预测 | ❌ | ✅ |
| 对比表格 | ❌ | ✅ |
| 配方设计 | ❌ | ✅ |
| 响应时间 | ~5s | ~8s |

### Q: 外推预测可靠吗？

外推预测有严格的边界控制：
- 仅允许数据范围外 50% 的外推
- 所有外推必须标注"外推估计"和置信度
- 数据点 < 3 时拒绝外推

### Q: 如何保证引用准确性？

1. LLM 使用内部编号（方案 1、2、3...）
2. 后处理转换为文献引用
3. 验证所有引用指向有效来源
4. 无效引用自动丢弃

---

## 下一步

- 查看 [API 契约](./contracts/synthesis-api.md) 了解完整接口
- 查看 [数据模型](./data-model.md) 了解数据结构
- 查看 [研究文档](./research.md) 了解设计决策
