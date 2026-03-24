"""
Synthesis Module for Multi-Literature Reasoning QA System

This module provides components for synthesizing knowledge from multiple literature sources:
- SampleAggregator: Extract and aggregate sample summaries
- TrendAnalyzer: Identify trends and patterns from data
- Extrapolator: Perform conservative extrapolation with boundary checks
- FormulaDesigner: Generate formula recommendations
- ComparisonTableGenerator: Create structured comparison tables
- CitationValidator: Verify and format citations
- ZeroHallucinationValidator: Verify all data points are traceable

Feature: 004-multi-literature-synthesis
"""

from .aggregator import SampleAggregator
from .citation_validator import CitationValidator
from .trend_analyzer import TrendAnalyzer
from .extrapolator import Extrapolator
from .formula_designer import FormulaDesigner, get_formula_designer
from .comparison_table import ComparisonTableGenerator, get_comparison_generator
from .hallucination_validator import (
    ZeroHallucinationValidator, 
    get_validator as get_hallucination_validator,
    validate_zero_hallucination
)

__all__ = [
    "SampleAggregator",
    "CitationValidator",
    "TrendAnalyzer",
    "Extrapolator",
    # Phase 5
    "FormulaDesigner",
    "get_formula_designer",
    # Phase 6
    "ComparisonTableGenerator",
    "get_comparison_generator",
    # Phase 8 - Zero Hallucination (T061)
    "ZeroHallucinationValidator",
    "get_hallucination_validator",
    "validate_zero_hallucination",
]
