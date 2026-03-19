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
