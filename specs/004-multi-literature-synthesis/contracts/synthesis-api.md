# API Contract: 综合问答系统

**Feature**: 004-multi-literature-synthesis  
**Date**: 2026-03-24  
**Base**: 003-rag-qa-enhancement `contracts/qa-api.md`

---

## Overview

本契约定义综合问答系统的 Python API 接口。基于现有 `QAEngine` 扩展，保持向后兼容。

---

## 1. QAEngine Extensions

### 1.1 answer() - 扩展参数

```python
def answer(
    self,
    query: str,
    top_k: int = 3,
    include_samples: bool = True,
    # 新增参数
    synthesis_mode: Optional[SynthesisMode] = None,  # 综合模式
    enable_extrapolation: bool = True,               # 启用外推
) -> Union[QAResponse, SynthesisResponse]:
    """
    生成问答响应。
    
    扩展说明:
    - synthesis_mode=None: 自动检测模式（默认）
    - synthesis_mode=SynthesisMode.SINGLE: 强制单样本模式（兼容 003）
    - synthesis_mode=SynthesisMode.SYNTHESIS: 强制综合模式
    - enable_extrapolation=False: 禁用外推，仅使用数据范围内的结论
    
    Returns:
        synthesis_mode=SINGLE: QAResponse (兼容 003)
        其他模式: SynthesisResponse
    """
```

**Backward Compatibility**:
- 不传 `synthesis_mode` 时，根据查询自动选择模式
- 现有调用方式完全兼容

---

### 1.2 synthesize() - 专用综合方法

```python
def synthesize(
    self,
    query: str,
    top_k: int = 8,                    # 默认 8 个样本
    min_samples: int = 3,              # 最少样本数（FR-005）
    enable_trend: bool = True,         # 启用趋势分析
    enable_extrapolation: bool = True, # 启用外推
) -> SynthesisResponse:
    """
    执行多文献综合问答。
    
    Pipeline:
    1. 向量检索 Top-K 样本
    2. 质量评分 + 重排序
    3. 提取样本摘要
    4. 计算数据范围
    5. LLM 综合生成
    6. 后处理验证
    
    Args:
        query: 用户查询
        top_k: 检索样本数（推荐 5-10）
        min_samples: 最少样本数，不足则拒绝综合
        enable_trend: 是否生成趋势分析
        enable_extrapolation: 是否允许外推预测
    
    Returns:
        SynthesisResponse
    
    Raises:
        InsufficientDataError: 样本数 < min_samples
        ExtrapolationBoundaryError: 查询超出允许外推范围
    """
```

**Example**:
```python
engine = QAEngine()
response = engine.synthesize(
    query="官能化程度如何影响拉伸强度？",
    top_k=8,
    enable_trend=True
)
print(response.answer.trend_analysis.to_display_text())
```

---

### 1.3 compare() - 对比分析方法

```python
def compare(
    self,
    schemes: List[str],                # 对比方案名称
    dimensions: Optional[List[str]] = None,  # 对比维度
    top_k_per_scheme: int = 3,         # 每方案检索数
) -> SynthesisResponse:
    """
    执行多方案对比分析。
    
    Args:
        schemes: 对比方案列表（如 ["羟基官能化", "羧基官能化"]）
        dimensions: 对比维度，None 时自动选择 5-7 个核心维度
        top_k_per_scheme: 每个方案检索的样本数
    
    Returns:
        SynthesisResponse，其中 answer.comparison 包含对比表格
    
    Raises:
        InsufficientDataError: 任一方案样本数 < 2（FR-005）
    """
```

**Auto-selected Dimensions** (when `dimensions=None`):
1. 拉伸强度
2. 断裂伸长率
3. Tg
4. Payne 效应
5. tan δ (0°C) - 湿地抓地力
6. tan δ (60°C) - 滚动阻力
7. 分散性评价

**Example**:
```python
response = engine.compare(
    schemes=["羟基官能化", "氨基官能化", "环氧官能化"],
    dimensions=["拉伸强度", "Tg", "分散效果"]
)
print(response.answer.comparison.to_markdown())
```

---

### 1.4 design_formula() - 配方设计方法

```python
def design_formula(
    self,
    target_properties: Dict[str, str], # 目标性能
    constraints: Optional[Dict[str, str]] = None,  # 约束条件
) -> SynthesisResponse:
    """
    基于目标性能设计配方建议。
    
    Args:
        target_properties: 目标性能字典
            例: {"湿地抓地力": "高", "滚动阻力": "低", "拉伸强度": ">15 MPa"}
        constraints: 约束条件
            例: {"官能化程度": "<10%", "成本": "低"}
    
    Returns:
        SynthesisResponse，其中 answer.formula 包含配方建议
    
    Raises:
        ConflictingTargetsError: 目标性能存在内在矛盾（FR-008）
    """
```

**Example**:
```python
response = engine.design_formula(
    target_properties={
        "湿地抓地力": "高",
        "滚动阻力": "低",
        "分散性": "优良"
    }
)
formula = response.answer.formula
print(f"推荐官能团: {formula.recommended_functional_group}")
print(f"推荐程度: {formula.recommended_degree}")
print(f"取舍说明: {formula.trade_offs}")
```

---

## 2. New Error Types

```python
class InsufficientDataError(QAError):
    """
    数据不足错误（FR-005）。
    
    当相关样本数量不满足最小要求时抛出。
    """
    def __init__(self, required: int, actual: int, operation: str):
        self.required = required
        self.actual = actual
        self.operation = operation
        super().__init__(
            f"{operation}需要至少 {required} 个相关样本，当前仅找到 {actual} 个"
        )


class ExtrapolationBoundaryError(QAError):
    """
    外推边界错误（FR-005）。
    
    当查询值超出允许的外推范围时抛出。
    """
    def __init__(self, query_value: float, allowed_range: Tuple[float, float], unit: str):
        self.query_value = query_value
        self.allowed_range = allowed_range
        self.unit = unit
        super().__init__(
            f"查询值 {query_value} {unit} 超出允许的外推范围 "
            f"[{allowed_range[0]:.1f}, {allowed_range[1]:.1f}] {unit}"
        )


class ConflictingTargetsError(QAError):
    """
    目标冲突错误（FR-008）。
    
    当用户指定的目标性能存在内在矛盾时抛出。
    """
    def __init__(self, conflicts: List[Tuple[str, str]], suggestion: str):
        self.conflicts = conflicts
        self.suggestion = suggestion
        conflict_str = ", ".join(f"{a} vs {b}" for a, b in conflicts)
        super().__init__(
            f"目标性能存在冲突: {conflict_str}。建议: {suggestion}"
        )
```

---

## 3. Response Structure

### SynthesisResponse JSON Schema

```json
{
  "answer": {
    "answer_text": "string (Markdown)",
    "answer_type": "direct|reference|guidance",
    "confidence": "high|medium|low",
    "synthesis_mode": "single|synthesis|comparison|formula",
    "source_samples": [
      {
        "sample_id": "SSBR-XXX",
        "functional_group": "string",
        "doi": "string|null"
      }
    ],
    "literature_citations": [
      {
        "sample_id": "SSBR-XXX",
        "doi": "string|null",
        "citation_text": "string|null"
      }
    ],
    "trend_analysis": {
      "variable_x": "string",
      "variable_y": "string",
      "trend_description": "string",
      "confidence": "high|medium|low",
      "data_points": 5
    },
    "extrapolation": {
      "query_value": 5.0,
      "predicted_range": [12.0, 16.0],
      "confidence": "medium",
      "is_extrapolation": true,
      "boundary_warning": "string|null"
    },
    "formula": {
      "recommended_functional_group": "string",
      "recommended_degree": "string",
      "confidence": "medium",
      "trade_offs": ["string"]
    },
    "comparison": {
      "dimensions": ["string"],
      "entries": [{"scheme": "string", "values": {}}],
      "summary": "string"
    }
  },
  "samples": [...],
  "search_time_ms": 200,
  "rerank_time_ms": 800,
  "synthesis_time_ms": 500,
  "generation_time_ms": 4000,
  "total_time_ms": 5500
}
```

---

## 4. Output Format Contract (FR-014)

### 分层结构要求

所有综合回答必须采用以下结构：

```markdown
## 结论摘要

[2-3 句话总结核心结论]

## 详细分析

### [要点 1]

[分析内容]

**数据支撑**：根据 [文献引用]，[具体数据]

### [要点 2]

...

## 文献来源

1. [引用 1]
2. [引用 2]
...

---

⚠️ [置信度说明/外推警告（如有）]
```

### 内容类型标注

| 类型 | 标注方式 | 示例 |
|------|----------|------|
| 文献原始数据 | 直接引用 | "拉伸强度为 18.5 MPa [1]" |
| 分析结论 | 无特殊标注 | "羟基官能化在分散性上表现更优" |
| 外推预测 | ⚠️ **外推估计** | "⚠️ **外推估计**：预计 12-16 MPa（中等置信度）" |

---

## 5. Performance Contract (SC-006)

| Metric | Target | Measurement |
|--------|--------|-------------|
| 综合问答总时间 | ≤ 8000 ms | `total_time_ms` |
| 向量检索 | ≤ 500 ms | `search_time_ms` |
| 重排序 | ≤ 1500 ms | `rerank_time_ms` |
| LLM 生成 | ≤ 6000 ms | `generation_time_ms` |

**超时处理**：
- 检索超时：返回空结果 + 错误提示
- 生成超时：返回已检索样本 + 降级提示

---

## 6. Validation Contract

### 输入验证

| Field | Rule | Error |
|-------|------|-------|
| query | 2-1000 字符 | `EmptyQueryError` / `QueryTooLongError` |
| top_k | 1-20 | ValueError |
| min_samples | 2-10 | ValueError |
| schemes (compare) | 长度 2-5 | ValueError |

### 输出验证

| Rule | FR | Action |
|------|-----|--------|
| 引用文献数 ≥ 2 | SC-001 | 警告日志 |
| 外推标注率 100% | SC-002 | 自动添加标注 |
| 配方完整性 ≥ 80% | SC-004 | 警告 + 补充说明 |
| 数据准确率 100% | SC-005 | 引用验证 |

---

## 7. Migration Guide

### From 003 to 004

**无破坏性变更**：

```python
# 003 代码（继续工作）
engine = QAEngine()
response = engine.answer("如何改善分散性？")

# 004 新功能（可选使用）
response = engine.synthesize("如何改善分散性？", top_k=8)
```

**推荐升级路径**：

1. 默认开启综合模式（自动检测）
2. 显式调用 `synthesize()` 获取完整功能
3. 使用 `compare()` 进行对比分析
4. 使用 `design_formula()` 进行配方设计
