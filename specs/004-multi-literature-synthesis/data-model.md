# Data Model: 多文献综合推理问答系统

**Feature**: 004-multi-literature-synthesis  
**Date**: 2026-03-24

## Overview

本文档定义综合推理问答系统的数据模型。基于现有 003 系统的 `models.py`，新增综合推理相关实体。

---

## Existing Entities (from 003)

以下实体保持不变，仅列出供参考：

| Entity | Description | Location |
|--------|-------------|----------|
| `Query` | 用户查询 | `scripts/models.py` |
| `Candidate` | 向量检索候选样本 | `scripts/models.py` |
| `QualityScore` | 样本质量评分 | `scripts/models.py` |
| `RankedResult` | 重排序结果 | `scripts/models.py` |
| `Citation` | 数据来源引用 | `scripts/models.py` |
| `GeneratedAnswer` | 生成的回答 | `scripts/models.py` |
| `QAResponse` | 完整问答响应 | `scripts/models.py` |
| `AnswerType` | 回答类型枚举 | `scripts/models.py` |
| `ConfidenceLevel` | 置信度枚举 | `scripts/models.py` |

---

## New Entities

### SynthesisMode (Enum)

综合问答模式枚举。

```python
class SynthesisMode(Enum):
    """综合问答模式"""
    SINGLE = "single"           # 单样本模式（兼容 003）
    SYNTHESIS = "synthesis"     # 多文献综合
    COMPARISON = "comparison"   # 对比分析
    FORMULA = "formula"         # 配方设计
```

---

### ConfidenceTag (Enum)

外推预测置信度标签（三级）。

```python
class ConfidenceTag(Enum):
    """外推置信度标签"""
    HIGH = "high"       # 数据点 ≥5，在数据范围内
    MEDIUM = "medium"   # 数据点 3-4，或在外推区域
    LOW = "low"         # 数据点 <3，或接近边界
```

**Determination Rules**:
```
if data_points >= 5 and within_range:
    return HIGH
elif data_points >= 3:
    return MEDIUM
else:
    return LOW
```

---

### ContentType (Enum)

内容类型枚举（三类区分）。

```python
class ContentType(Enum):
    """内容类型（FR-012 要求）"""
    LITERATURE_DATA = "literature_data"   # 文献原始数据
    ANALYSIS = "analysis"                  # 基于数据的分析结论
    EXTRAPOLATION = "extrapolation"        # 外推预测
```

---

### SampleSummary

样本摘要，用于 Prompt 构建（减少 token）。

```python
@dataclass
class SampleSummary:
    """
    样本结构化摘要，用于综合分析。
    
    从 summary.md 提取关键字段，避免传递全量内容。
    """
    sample_id: str
    
    # 官能化信息
    functional_group: str           # 核心官能团名称
    functionalization_degree: str   # 官能化程度（如 "3.6 wt%"）
    reagent: str                    # 官能化试剂
    method: str                     # 官能化方法
    
    # 关键性能指标
    tensile_strength: Optional[str] = None      # 拉伸强度
    elongation: Optional[str] = None            # 断裂伸长率
    tg: Optional[str] = None                    # 玻璃化转变温度
    payne_effect: Optional[str] = None          # Payne 效应
    tan_delta_0c: Optional[str] = None          # 湿地抓地力指标
    tan_delta_60c: Optional[str] = None         # 滚动阻力指标
    
    # 文献来源
    doi: Optional[str] = None
    first_author: Optional[str] = None
    year: Optional[int] = None
    
    # 元数据
    quality_score: float = 0.0
    similarity: float = 0.0
```

**Extraction Source**: `summary.md` YAML front matter

**Validation Rules**:
- `sample_id`: 必须匹配 `SSBR-\d{3}` 格式
- `functional_group`: 非空
- `quality_score`: 0.0 - 1.0

---

### DataRange

数据范围，用于外推边界计算。

```python
@dataclass
class DataRange:
    """
    数据范围定义，用于外推边界计算。
    """
    field_name: str             # 字段名（如 "functionalization_degree"）
    min_value: float            # 最小值
    max_value: float            # 最大值
    unit: str                   # 单位
    data_points: int            # 数据点数量
    
    @property
    def extrapolation_min(self) -> float:
        """允许的外推下界（范围外 50%）"""
        range_size = self.max_value - self.min_value
        return self.min_value - range_size * 0.5
    
    @property
    def extrapolation_max(self) -> float:
        """允许的外推上界（范围外 50%）"""
        range_size = self.max_value - self.min_value
        return self.max_value + range_size * 0.5
    
    def is_within_data(self, value: float) -> bool:
        """检查值是否在数据范围内"""
        return self.min_value <= value <= self.max_value
    
    def is_within_extrapolation(self, value: float) -> bool:
        """检查值是否在允许的外推范围内"""
        return self.extrapolation_min <= value <= self.extrapolation_max
```

**Example**:
```python
range = DataRange(
    field_name="functionalization_degree",
    min_value=1.0,
    max_value=15.0,
    unit="wt%",
    data_points=12
)
# extrapolation_min = 1.0 - 7.0 = -6.0 → 实际取 0（物理约束）
# extrapolation_max = 15.0 + 7.0 = 22.0
```

---

### TrendAnalysis

趋势分析结果。

```python
@dataclass
class TrendAnalysis:
    """
    从多样本数据中提取的趋势分析。
    
    Attributes:
        variable_x: 自变量名称（如 "官能化程度"）
        variable_y: 因变量名称（如 "拉伸强度"）
        trend_description: 趋势定性描述
        supporting_data: 支撑数据点列表
        data_range: 数据覆盖范围
        confidence: 置信度标签
    """
    variable_x: str
    variable_y: str
    trend_description: str
    supporting_data: List[Dict[str, Any]]  # [{sample_id, x_value, y_value}, ...]
    data_range: DataRange
    confidence: ConfidenceTag
    
    def to_display_text(self) -> str:
        """生成用户可见的趋势描述"""
        return (
            f"{self.trend_description}\n"
            f"（{self.confidence.value}置信度，基于 {len(self.supporting_data)} 个数据点）"
        )
```

**Validation Rules**:
- `supporting_data`: 长度 ≥ 2（对比分析）或 ≥ 3（趋势分析）
- `trend_description`: 非空，使用定性语言

---

### ExtrapolationResult

外推预测结果。

```python
@dataclass
class ExtrapolationResult:
    """
    基于趋势的外推预测结果。
    
    所有外推必须明确标注，并附带置信度说明。
    """
    query_value: float              # 查询的自变量值
    query_unit: str                 # 单位
    predicted_range: Tuple[float, float]  # 预测值区间 (min, max)
    predicted_unit: str             # 预测值单位
    confidence: ConfidenceTag       # 置信度标签
    data_points_used: int           # 使用的数据点数
    is_extrapolation: bool          # 是否为外推（True）或插值（False）
    boundary_warning: Optional[str] = None  # 边界警告信息
    
    def to_display_text(self) -> str:
        """生成用户可见的预测描述"""
        range_str = f"{self.predicted_range[0]:.1f}-{self.predicted_range[1]:.1f} {self.predicted_unit}"
        prefix = "⚠️ **外推估计**：" if self.is_extrapolation else "**估计值**："
        confidence_str = f"（{self.confidence.value}置信度，基于 {self.data_points_used} 个相近样本）"
        
        result = f"{prefix}{range_str} {confidence_str}"
        if self.boundary_warning:
            result += f"\n⚠️ {self.boundary_warning}"
        return result
```

**Validation Rules**:
- `is_extrapolation = True` 时，必须有 `confidence` 和 `data_points_used`
- `predicted_range[0] <= predicted_range[1]`
- 如果 `query_value` 超出 `DataRange.extrapolation_max`，必须设置 `boundary_warning`

---

### FormulaRecommendation

配方设计建议。

```python
@dataclass
class FormulaRecommendation:
    """
    基于目标性能的配方设计建议。
    """
    target_properties: Dict[str, str]   # 目标性能 {property: target_value}
    
    # 推荐配方
    recommended_functional_group: str   # 推荐官能团
    recommended_degree: str             # 推荐官能化程度
    recommended_filler: Optional[str]   # 推荐填料体系
    
    # 预期性能
    expected_performance: Dict[str, str]  # {property: expected_value}
    
    # 设计理由
    rationale: List[str]                # 每个参数的选择理由
    supporting_samples: List[str]       # 支撑样本 ID 列表
    
    # 风险提示
    trade_offs: List[str]               # 性能取舍说明
    warnings: List[str]                 # 安全/环保警示
    
    confidence: ConfidenceTag
    
    def is_complete(self) -> bool:
        """检查配方完整性（FR-007: ≥80% = 3 要素中至少 2 项）"""
        has_group = bool(self.recommended_functional_group)
        has_degree = bool(self.recommended_degree)
        has_filler = bool(self.recommended_filler)
        return sum([has_group, has_degree, has_filler]) >= 2
```

**Validation Rules**:
- `supporting_samples`: 长度 ≥ 2
- `rationale`: 每个推荐参数至少一条理由
- `is_complete()` 必须返回 `True`

---

### ComparisonTable

对比分析表格。

```python
@dataclass
class ComparisonDimension:
    """对比维度"""
    name: str                           # 维度名称（如 "拉伸强度"）
    unit: str                           # 单位
    higher_is_better: bool = True       # 是否越高越好

@dataclass
class ComparisonEntry:
    """对比条目"""
    scheme_name: str                    # 方案名称（如 "羟基官能化"）
    sample_ids: List[str]               # 来源样本
    values: Dict[str, Optional[str]]    # {dimension_name: value}
    
@dataclass
class ComparisonTable:
    """
    结构化对比表格。
    """
    title: str                          # 表格标题
    dimensions: List[ComparisonDimension]  # 对比维度
    entries: List[ComparisonEntry]      # 对比条目
    summary: str                        # 综合结论
    
    def has_missing_data(self) -> bool:
        """检查是否有数据缺失"""
        for entry in self.entries:
            for dim in self.dimensions:
                if entry.values.get(dim.name) is None:
                    return True
        return False
    
    def to_markdown(self) -> str:
        """生成 Markdown 格式表格"""
        # Header
        header = "| 方案 | " + " | ".join(d.name for d in self.dimensions) + " |"
        separator = "|---" + "|---" * len(self.dimensions) + "|"
        
        # Rows
        rows = []
        for entry in self.entries:
            values = []
            for dim in self.dimensions:
                v = entry.values.get(dim.name)
                values.append(v if v else "数据不足")
            rows.append(f"| {entry.scheme_name} | " + " | ".join(values) + " |")
        
        return "\n".join([header, separator] + rows + ["", self.summary])
```

**Validation Rules**:
- `entries`: 长度 ≥ 2（至少两个方案对比）
- `dimensions`: 长度 5-7（FR-009: 自动选择核心维度）
- 缺失值必须标注 "数据不足"，禁止编造

---

### SynthesizedAnswer

综合回答（扩展自 GeneratedAnswer）。

```python
@dataclass
class SynthesizedAnswer:
    """
    综合多文献的回答。
    
    扩展自 GeneratedAnswer，增加综合特有字段。
    """
    # 基础字段（继承自 GeneratedAnswer 概念）
    answer_text: str
    answer_type: AnswerType
    confidence: ConfidenceLevel
    query: str
    generation_time_ms: int
    model_used: str
    
    # 综合特有字段
    synthesis_mode: SynthesisMode
    source_samples: List[SampleSummary]     # 来源样本摘要
    literature_citations: List[Citation]     # 文献引用
    
    # 可选综合结果
    trend_analysis: Optional[TrendAnalysis] = None
    extrapolation: Optional[ExtrapolationResult] = None
    formula: Optional[FormulaRecommendation] = None
    comparison: Optional[ComparisonTable] = None
    
    # 内容分类（FR-012）
    content_breakdown: Dict[ContentType, List[str]] = field(default_factory=dict)
    
    def get_citation_count(self) -> int:
        """获取引用文献数量（SC-001: ≥2）"""
        return len(set(c.doi for c in self.literature_citations if c.doi))
    
    def validate(self) -> List[str]:
        """验证回答符合规格要求"""
        errors = []
        
        # SC-001: 综合回答引用 ≥2 篇文献
        if self.synthesis_mode == SynthesisMode.SYNTHESIS:
            if self.get_citation_count() < 2:
                errors.append("综合回答引用文献数量不足（要求 ≥2）")
        
        # SC-002: 外推标注率 100%
        if self.extrapolation and not self.extrapolation.is_extrapolation:
            errors.append("外推结果缺少标注")
        
        return errors
```

---

### SynthesisResponse

完整综合问答响应。

```python
@dataclass
class SynthesisResponse:
    """
    完整的综合问答响应。
    """
    answer: SynthesizedAnswer
    samples: List[RankedResult]         # 检索结果
    data_ranges: Dict[str, DataRange]   # 相关数据范围
    
    # 时间统计
    search_time_ms: int
    rerank_time_ms: int
    synthesis_time_ms: int              # 综合分析时间
    generation_time_ms: int
    total_time_ms: int
    
    # 元信息
    sample_count: int                   # 使用的样本数
    unique_literature_count: int        # 独立文献数
    
    def meets_performance_target(self) -> bool:
        """检查是否满足性能目标（SC-006: ≤8s）"""
        return self.total_time_ms <= 8000
```

---

## Entity Relationships

```
┌─────────────────┐
│  SynthesisMode  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ SynthesisQuery  │────▶│  SampleSummary  │ (1:N)
└────────┬────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│SynthesizedAnswer│────▶│   DataRange     │ (1:N)
└────────┬────────┘     └─────────────────┘
         │
         ├──────────────▶ TrendAnalysis (0:1)
         │
         ├──────────────▶ ExtrapolationResult (0:1)
         │
         ├──────────────▶ FormulaRecommendation (0:1)
         │
         └──────────────▶ ComparisonTable (0:1)
```

---

## State Transitions

### SynthesisMode Selection

```
User Query
    │
    ▼
┌─────────────────────────────────┐
│ Query Intent Classification     │
├─────────────────────────────────┤
│ "对比/比较 X 和 Y" → COMPARISON │
│ "设计配方/推荐" → FORMULA       │
│ "趋势/规律/外推" → SYNTHESIS    │
│ 其他 → SYNTHESIS (default)      │
└─────────────────────────────────┘
```

### Confidence Determination

```
Input: data_points, is_within_range
    │
    ▼
┌─────────────────────────────────┐
│ data_points >= 5 AND in_range   │──▶ HIGH
├─────────────────────────────────┤
│ data_points >= 3                │──▶ MEDIUM
├─────────────────────────────────┤
│ else                            │──▶ LOW
└─────────────────────────────────┘
```

---

## Serialization Format

所有新实体支持 `to_dict()` 方法，输出 JSON 兼容格式：

```python
def to_dict(self) -> Dict[str, Any]:
    """Convert to dictionary for serialization."""
    return {
        "field_name": self.field_name,
        "nested": self.nested.to_dict() if self.nested else None,
        "list_field": [item.to_dict() for item in self.list_field],
        "enum_field": self.enum_field.value,
    }
```
