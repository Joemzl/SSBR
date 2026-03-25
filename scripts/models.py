"""
Data Models for RAG QA System

This module defines all data classes used in the QA system,
following the specifications in data-model.md.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any


# =============================================================================
# Enumerations
# =============================================================================

class AnswerType(Enum):
    """
    Answer type based on similarity threshold.
    
    - DIRECT: similarity >= 0.7 (high confidence)
    - REFERENCE: 0.5 <= similarity < 0.7 (medium confidence)
    - GUIDANCE: similarity < 0.5 (low/no match)
    """
    DIRECT = "direct"
    REFERENCE = "reference"
    GUIDANCE = "guidance"


class ConfidenceLevel(Enum):
    """
    Confidence level for generated answers.
    """
    HIGH = "high"       # Based on high-quality, high-similarity samples
    MEDIUM = "medium"   # Medium quality or similarity
    LOW = "low"         # Guidance answer or low-quality samples


# =============================================================================
# Synthesis Enumerations (004-multi-literature-synthesis)
# =============================================================================

class SynthesisMode(Enum):
    """
    综合问答模式（004-multi-literature-synthesis）。
    
    - SINGLE: 单样本模式（兼容 003）
    - SYNTHESIS: 多文献综合
    - COMPARISON: 对比分析
    - FORMULA: 配方设计
    """
    SINGLE = "single"
    SYNTHESIS = "synthesis"
    COMPARISON = "comparison"
    FORMULA = "formula"


class ConfidenceTag(Enum):
    """
    外推置信度标签（三级）。
    
    - HIGH: 数据点 ≥5，在数据范围内
    - MEDIUM: 数据点 3-4，或在外推区域
    - LOW: 数据点 <3，或接近边界
    """
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ContentType(Enum):
    """
    内容类型枚举（FR-012 要求区分三类内容）。
    
    - LITERATURE_DATA: 文献原始数据
    - ANALYSIS: 基于数据的分析结论
    - EXTRAPOLATION: 外推预测
    """
    LITERATURE_DATA = "literature_data"
    ANALYSIS = "analysis"
    EXTRAPOLATION = "extrapolation"


# =============================================================================
# Core Data Classes
# =============================================================================

@dataclass
class Query:
    """
    User's natural language query.
    
    Attributes:
        raw_text: Original user input
        processed_text: Preprocessed query text
        embedding: 1536-dimensional vector (text-embedding-3-small)
        timestamp: Query timestamp
    """
    raw_text: str
    processed_text: str = ""
    embedding: Optional[List[float]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.processed_text:
            self.processed_text = self.raw_text.strip()
    
    def validate(self) -> bool:
        """Validate query constraints."""
        if not self.raw_text or len(self.raw_text.strip()) < 2:
            return False
        if len(self.raw_text) > 1000:
            return False
        return True


@dataclass
class Candidate:
    """
    Candidate sample from initial vector search.
    
    Attributes:
        sample_id: Sample ID (e.g., SSBR-002)
        similarity: Cosine similarity (0.0 - 1.0)
        content: summary.md body content
        summary_path: File path
    """
    sample_id: str
    similarity: float
    content: str
    summary_path: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "sample_id": self.sample_id,
            "similarity": self.similarity,
            "content": self.content,
            "summary_path": self.summary_path
        }


@dataclass
class QualityScore:
    """
    Sample data quality assessment based on field completeness.
    
    Attributes:
        sample_id: Sample ID
        overall_score: Combined quality score (0.0 - 1.0)
        functionalization_score: Functionalization info completeness
        mechanical_score: Mechanical properties completeness
        thermal_score: Thermal properties completeness
        dynamic_score: Dynamic properties completeness
        source_score: Literature source completeness
        missing_fields: List of missing key fields
    """
    sample_id: str
    overall_score: float = 0.0
    functionalization_score: float = 0.0
    mechanical_score: float = 0.0
    thermal_score: float = 0.0
    dynamic_score: float = 0.0
    source_score: float = 0.0
    missing_fields: List[str] = field(default_factory=list)
    content_hash: str = ""
    
    def calculate_overall(self) -> float:
        """
        Calculate overall score using weighted formula.
        
        Weights:
        - Functionalization: 30%
        - Mechanical: 25%
        - Thermal: 15%
        - Dynamic: 15%
        - Source: 15%
        """
        self.overall_score = (
            self.functionalization_score * 0.30 +
            self.mechanical_score * 0.25 +
            self.thermal_score * 0.15 +
            self.dynamic_score * 0.15 +
            self.source_score * 0.15
        )
        return self.overall_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization/caching."""
        return {
            "sample_id": self.sample_id,
            "overall_score": self.overall_score,
            "functionalization_score": self.functionalization_score,
            "mechanical_score": self.mechanical_score,
            "thermal_score": self.thermal_score,
            "dynamic_score": self.dynamic_score,
            "source_score": self.source_score,
            "missing_fields": self.missing_fields,
            "content_hash": self.content_hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QualityScore":
        """Create instance from dictionary."""
        return cls(
            sample_id=data.get("sample_id", ""),
            overall_score=data.get("overall_score", 0.0),
            functionalization_score=data.get("functionalization_score", 0.0),
            mechanical_score=data.get("mechanical_score", 0.0),
            thermal_score=data.get("thermal_score", 0.0),
            dynamic_score=data.get("dynamic_score", 0.0),
            source_score=data.get("source_score", 0.0),
            missing_fields=data.get("missing_fields", []),
            content_hash=data.get("content_hash", "")
        )


@dataclass
class RankedResult:
    """
    Re-ranked sample result from cross-encoder.
    
    Attributes:
        sample_id: Sample ID
        original_rank: Rank before reranking (1-based)
        rerank_score: Cross-encoder score
        final_rank: Rank after reranking (1-based)
        similarity: Original cosine similarity
        quality_score: Sample quality score (0.0 - 1.0)
        content: summary.md body content
    """
    sample_id: str
    original_rank: int
    rerank_score: float
    final_rank: int
    similarity: float
    quality_score: float
    content: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "sample_id": self.sample_id,
            "original_rank": self.original_rank,
            "rerank_score": self.rerank_score,
            "final_rank": self.final_rank,
            "similarity": self.similarity,
            "quality_score": self.quality_score,
            "content": self.content
        }


@dataclass
class Citation:
    """
    Data source citation in generated answer.
    
    Attributes:
        sample_id: Sample ID (required)
        doi: Literature DOI (optional)
        citation_text: Citation format (journal, year, page)
        data_type: Type of cited data (e.g., "力学性能")
    """
    sample_id: str
    data_type: str
    doi: Optional[str] = None
    citation_text: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "sample_id": self.sample_id,
            "data_type": self.data_type,
            "doi": self.doi,
            "citation_text": self.citation_text
        }


@dataclass
class GeneratedAnswer:
    """
    System-generated natural language answer.
    
    Attributes:
        answer_text: Answer body (Markdown format)
        answer_type: Answer type enum
        citations: List of citations
        confidence: Confidence level
        query: Original query
        source_samples: Referenced sample IDs
        generation_time_ms: Generation time (milliseconds)
        model_used: Model used (e.g., gpt-4o-mini)
    """
    answer_text: str
    answer_type: AnswerType
    citations: List[Citation]
    confidence: ConfidenceLevel
    query: str
    source_samples: List[str]
    generation_time_ms: int
    model_used: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "answer_text": self.answer_text,
            "answer_type": self.answer_type.value,
            "citations": [c.to_dict() for c in self.citations],
            "confidence": self.confidence.value,
            "query": self.query,
            "source_samples": self.source_samples,
            "generation_time_ms": self.generation_time_ms,
            "model_used": self.model_used
        }


@dataclass
class QAResponse:
    """
    Complete QA response including answer and samples.
    
    Attributes:
        answer: Generated answer
        samples: Ranked sample list
        search_time_ms: Search time (milliseconds)
        rerank_time_ms: Rerank time (milliseconds)
        generation_time_ms: Generation time (milliseconds)
        total_time_ms: Total time (milliseconds)
    """
    answer: GeneratedAnswer
    samples: List[RankedResult]
    search_time_ms: int
    rerank_time_ms: int
    generation_time_ms: int
    total_time_ms: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "answer": self.answer.to_dict(),
            "samples": [s.to_dict() for s in self.samples],
            "search_time_ms": self.search_time_ms,
            "rerank_time_ms": self.rerank_time_ms,
            "generation_time_ms": self.generation_time_ms,
            "total_time_ms": self.total_time_ms
        }


# =============================================================================
# Synthesis Data Classes (004-multi-literature-synthesis)
# =============================================================================

@dataclass
class RecommendationCard:
    """
    推荐卡片数据结构（FR-014a）。
    
    综合分析的核心输出，在 UI 最顶部醒目展示。
    """
    # 核心推荐参数（必填）
    functional_group: str           # 推荐官能团（如"羟基 (-OH)"）
    reagent: str                    # 推荐官能化试剂
    degree_range: str               # 推荐官能化程度范围（如"2.5-4.0 wt%"）
    expected_improvement: str       # 预期改善效果
    confidence: ConfidenceTag       # 推荐置信度
    
    # 可选字段
    best_sample_ref: Optional[str] = None   # 最佳参考样本 ID
    supporting_samples: List[str] = field(default_factory=list)  # 支撑样本列表
    rationale: str = ""             # 推荐理由摘要
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "functional_group": self.functional_group,
            "reagent": self.reagent,
            "degree_range": self.degree_range,
            "expected_improvement": self.expected_improvement,
            "confidence": self.confidence.value,
            "best_sample_ref": self.best_sample_ref,
            "supporting_samples": self.supporting_samples,
            "rationale": self.rationale
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecommendationCard":
        """Create instance from dictionary (for GPT response parsing)."""
        return cls(
            functional_group=data.get("functional_group", "未知"),
            reagent=data.get("reagent", "未知"),
            degree_range=data.get("degree_range", "未知"),
            expected_improvement=data.get("expected_improvement", "未知"),
            confidence=ConfidenceTag(data.get("confidence", "medium")),
            best_sample_ref=data.get("best_sample_ref"),
            supporting_samples=data.get("supporting_samples", []),
            rationale=data.get("rationale", "")
        )


@dataclass
class SampleSummary:
    """
    样本结构化摘要，用于综合分析（T007）。
    
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "sample_id": self.sample_id,
            "functional_group": self.functional_group,
            "functionalization_degree": self.functionalization_degree,
            "reagent": self.reagent,
            "method": self.method,
            "tensile_strength": self.tensile_strength,
            "elongation": self.elongation,
            "tg": self.tg,
            "payne_effect": self.payne_effect,
            "tan_delta_0c": self.tan_delta_0c,
            "tan_delta_60c": self.tan_delta_60c,
            "doi": self.doi,
            "first_author": self.first_author,
            "year": self.year,
            "quality_score": self.quality_score,
            "similarity": self.similarity
        }


@dataclass
class DataRange:
    """
    数据范围定义，用于外推边界计算（T008）。
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
        return max(0, self.min_value - range_size * 0.5)  # 不低于 0
    
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "field_name": self.field_name,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "unit": self.unit,
            "data_points": self.data_points,
            "extrapolation_min": self.extrapolation_min,
            "extrapolation_max": self.extrapolation_max
        }


@dataclass
class SynthesizedAnswer:
    """
    综合多文献的回答（T009）。
    
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
    literature_citations: List['Citation']   # 文献引用
    
    # 推荐卡片（FR-014a）- 综合分析核心输出
    recommendation_card: Optional[RecommendationCard] = None
    
    # 可选综合结果（后续 Phase 添加）
    trend_analysis: Optional[Any] = None          # TrendAnalysis
    extrapolation: Optional[Any] = None           # ExtrapolationResult
    formula: Optional[Any] = None                 # FormulaRecommendation
    comparison: Optional[Any] = None              # ComparisonTable
    
    # 内容分类（FR-012）
    content_breakdown: Dict[ContentType, List[str]] = field(default_factory=dict)
    
    def get_citation_count(self) -> int:
        """获取引用文献数量（SC-001: ≥2）"""
        return len(set(c.doi for c in self.literature_citations if c.doi))
    
    def get_unique_literature_count(self) -> int:
        """获取独立文献数量"""
        dois = set()
        for sample in self.source_samples:
            if sample.doi:
                dois.add(sample.doi)
        return len(dois)
    
    def validate(self) -> List[str]:
        """验证回答符合规格要求"""
        errors = []
        
        # SC-001: 综合回答引用 ≥2 篇文献
        if self.synthesis_mode == SynthesisMode.SYNTHESIS:
            if self.get_citation_count() < 2:
                errors.append("综合回答引用文献数量不足（要求 ≥2）")
        
        # SC-002: 外推标注率 100%（如有外推内容）
        if self.extrapolation is not None:
            # 外推结果必须有标注
            if hasattr(self.extrapolation, 'is_extrapolation'):
                if not self.extrapolation.is_extrapolation:
                    errors.append("外推结果缺少标注")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "answer_text": self.answer_text,
            "answer_type": self.answer_type.value,
            "confidence": self.confidence.value,
            "query": self.query,
            "generation_time_ms": self.generation_time_ms,
            "model_used": self.model_used,
            "synthesis_mode": self.synthesis_mode.value,
            "source_samples": [s.to_dict() for s in self.source_samples],
            "literature_citations": [c.to_dict() for c in self.literature_citations],
            "recommendation_card": self.recommendation_card.to_dict() if self.recommendation_card else None,
            "citation_count": self.get_citation_count(),
            "unique_literature_count": self.get_unique_literature_count()
        }
        return result


@dataclass
class SynthesisResponse:
    """
    完整的综合问答响应（T010）。
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "answer": self.answer.to_dict(),
            "samples": [s.to_dict() for s in self.samples],
            "data_ranges": {k: v.to_dict() for k, v in self.data_ranges.items()},
            "search_time_ms": self.search_time_ms,
            "rerank_time_ms": self.rerank_time_ms,
            "synthesis_time_ms": self.synthesis_time_ms,
            "generation_time_ms": self.generation_time_ms,
            "total_time_ms": self.total_time_ms,
            "sample_count": self.sample_count,
            "unique_literature_count": self.unique_literature_count,
            "meets_performance_target": self.meets_performance_target()
        }


# =============================================================================
# Trend Analysis & Extrapolation (Phase 4 - T022-T023)
# =============================================================================

@dataclass
class TrendAnalysis:
    """
    从多样本数据中提取的趋势分析（T022）。
    """
    variable_x: str                     # 自变量名称（如 "官能化程度"）
    variable_y: str                     # 因变量名称（如 "拉伸强度"）
    trend_description: str              # 趋势定性描述
    supporting_data: List[Dict[str, Any]]  # [{sample_id, x_value, y_value}, ...]
    data_range: DataRange               # 数据覆盖范围
    confidence: ConfidenceTag           # 置信度标签
    
    def to_display_text(self) -> str:
        """生成用户可见的趋势描述"""
        return (
            f"{self.trend_description}\n"
            f"（{self.confidence.value}置信度，基于 {len(self.supporting_data)} 个数据点）"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "variable_x": self.variable_x,
            "variable_y": self.variable_y,
            "trend_description": self.trend_description,
            "supporting_data": self.supporting_data,
            "data_range": self.data_range.to_dict(),
            "confidence": self.confidence.value,
            "data_points": len(self.supporting_data)
        }


@dataclass
class ExtrapolationResult:
    """
    基于趋势的外推预测结果（T023）。
    
    所有外推必须明确标注，并附带置信度说明。
    """
    query_value: float              # 查询的自变量值
    query_unit: str                 # 单位
    predicted_range: tuple          # 预测值区间 (min, max)
    predicted_unit: str             # 预测值单位
    confidence: ConfidenceTag       # 置信度标签
    data_points_used: int           # 使用的数据点数
    is_extrapolation: bool          # 是否为外推（True）或插值（False）
    boundary_warning: Optional[str] = None  # 边界警告信息
    
    def to_display_text(self) -> str:
        """生成用户可见的预测描述（T031）"""
        range_str = f"{self.predicted_range[0]:.1f}-{self.predicted_range[1]:.1f} {self.predicted_unit}"
        prefix = "⚠️ **外推估计**：" if self.is_extrapolation else "**估计值**："
        confidence_str = f"（{self.confidence.value}置信度，基于 {self.data_points_used} 个相近样本）"
        
        result = f"{prefix}{range_str} {confidence_str}"
        if self.boundary_warning:
            result += f"\n⚠️ {self.boundary_warning}"
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "query_value": self.query_value,
            "query_unit": self.query_unit,
            "predicted_range": list(self.predicted_range),
            "predicted_unit": self.predicted_unit,
            "confidence": self.confidence.value,
            "data_points_used": self.data_points_used,
            "is_extrapolation": self.is_extrapolation,
            "boundary_warning": self.boundary_warning
        }


# =============================================================================
# Formula Design (Phase 5 - T032)
# =============================================================================

@dataclass
class FormulaRecommendation:
    """
    基于目标性能的配方设计建议（T032）。
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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "target_properties": self.target_properties,
            "recommended_functional_group": self.recommended_functional_group,
            "recommended_degree": self.recommended_degree,
            "recommended_filler": self.recommended_filler,
            "expected_performance": self.expected_performance,
            "rationale": self.rationale,
            "supporting_samples": self.supporting_samples,
            "trade_offs": self.trade_offs,
            "warnings": self.warnings,
            "confidence": self.confidence.value,
            "is_complete": self.is_complete()
        }


# =============================================================================
# Comparison Table (Phase 6 - T039-T041)
# =============================================================================

@dataclass
class ComparisonDimension:
    """对比维度（T039）"""
    name: str                           # 维度名称（如 "拉伸强度"）
    unit: str                           # 单位
    higher_is_better: bool = True       # 是否越高越好
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "unit": self.unit,
            "higher_is_better": self.higher_is_better
        }


@dataclass
class ComparisonEntry:
    """对比条目（T040）"""
    scheme_name: str                    # 方案名称（如 "羟基官能化"）
    sample_ids: List[str]               # 来源样本
    values: Dict[str, Optional[str]]    # {dimension_name: value}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "scheme_name": self.scheme_name,
            "sample_ids": self.sample_ids,
            "values": self.values
        }


@dataclass
class ComparisonTable:
    """
    结构化对比表格（T041）。
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
        """生成 Markdown 格式表格（T048）"""
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
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "dimensions": [d.to_dict() for d in self.dimensions],
            "entries": [e.to_dict() for e in self.entries],
            "summary": self.summary,
            "has_missing_data": self.has_missing_data()
        }


# =============================================================================
# Utility Functions
# =============================================================================

def determine_answer_type(max_similarity: float) -> AnswerType:
    """
    Determine answer type based on maximum similarity score.
    
    Args:
        max_similarity: Maximum similarity score from candidates
    
    Returns:
        Appropriate AnswerType
    """
    if max_similarity >= 0.7:
        return AnswerType.DIRECT
    elif max_similarity >= 0.5:
        return AnswerType.REFERENCE
    else:
        return AnswerType.GUIDANCE


def determine_confidence(
    answer_type: AnswerType,
    avg_quality_score: float
) -> ConfidenceLevel:
    """
    Determine confidence level based on answer type and quality.
    
    Args:
        answer_type: The determined answer type
        avg_quality_score: Average quality score of source samples
    
    Returns:
        Appropriate ConfidenceLevel
    """
    if answer_type == AnswerType.GUIDANCE:
        return ConfidenceLevel.LOW
    
    if answer_type == AnswerType.DIRECT and avg_quality_score >= 0.7:
        return ConfidenceLevel.HIGH
    elif answer_type == AnswerType.DIRECT or avg_quality_score >= 0.5:
        return ConfidenceLevel.MEDIUM
    else:
        return ConfidenceLevel.LOW
