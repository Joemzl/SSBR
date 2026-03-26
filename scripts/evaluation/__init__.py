"""
SSBR QA System Evaluation Module

Contains evaluation tools including:
- RAGAS integration for RAG system evaluation
- Custom metrics for citation accuracy and recommendation quality
"""

from .ragas_evaluator import (
    RAGASEvaluator,
    EvalSample,
    EvalResult,
    EvalReport,
    SYNTHESIS_TEST_SAMPLES,
    SINGLE_TEST_SAMPLES,
)

__all__ = [
    "RAGASEvaluator",
    "EvalSample",
    "EvalResult", 
    "EvalReport",
    "SYNTHESIS_TEST_SAMPLES",
    "SINGLE_TEST_SAMPLES",
]
