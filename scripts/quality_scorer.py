"""
Quality Scorer Module for RAG QA System

This module assesses sample data quality based on field completeness
in the summary.md YAML front matter.

Quality scoring dimensions:
- Functionalization info (30%)
- Mechanical properties (25%)
- Thermal properties (15%)
- Dynamic properties (15%)
- Literature source (15%)
"""

import os
import re
import json
import hashlib
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import from project modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import QualityScore


class QualityScorer:
    """
    Sample quality assessment based on field completeness.
    
    Quality scores are used to weight samples during answer generation.
    Low-quality samples are not excluded, but their information is
    marked as "for reference only".
    """
    
    # Key fields and their weights for each dimension
    FIELD_CONFIG = {
        'functionalization': {
            'weight': 0.30,
            'fields': {
                '官能化试剂': 0.33,
                '官能化程度': 0.33,
                '核心官能团': 0.34,
            }
        },
        'mechanical': {
            'weight': 0.25,
            'fields': {
                '拉伸强度': 0.35,
                '断裂伸长率': 0.35,
                '定伸应力': 0.30,
            }
        },
        'thermal': {
            'weight': 0.15,
            'fields': {
                'Tg': 1.0,
            }
        },
        'dynamic': {
            'weight': 0.15,
            'fields': {
                'tan δ': 0.5,
                'tanδ': 0.5,  # Alternative spelling
            }
        },
        'source': {
            'weight': 0.15,
            'fields': {
                'DOI': 0.6,
                '引文': 0.4,
            }
        }
    }
    
    # Alternative field names for matching
    FIELD_ALIASES = {
        'Tg': ['tg', 'glass_transition', '玻璃化转变温度', '玻璃化温度'],
        'DOI': ['doi', 'DOI_link'],
        '官能化试剂': ['functionalization_agent', '改性剂'],
        '官能化程度': ['functionalization_degree', '改性程度'],
        '拉伸强度': ['tensile_strength', 'TS'],
        '断裂伸长率': ['elongation_at_break', 'EB'],
        '定伸应力': ['modulus', 'M300', 'M100'],
        'tan δ': ['tan_delta', 'loss_tangent'],
    }
    
    def __init__(self, cache_path: Optional[str] = None):
        """
        Initialize QualityScorer.
        
        Args:
            cache_path: Path to quality scores cache file
        """
        if cache_path is None:
            # Default cache path
            project_root = Path(__file__).parent.parent.parent
            cache_path = project_root / ".cache" / "quality_scores.json"
        
        self.cache_path = Path(cache_path)
        self._cache: Dict[str, QualityScore] = {}
        self._load_cache()
    
    def _load_cache(self) -> None:
        """Load quality scores from cache file."""
        if self.cache_path.exists():
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    scores = data.get('scores', {})
                    for sample_id, score_data in scores.items():
                        self._cache[sample_id] = QualityScore.from_dict(score_data)
            except Exception as e:
                print(f"Warning: Failed to load quality cache: {e}")
                self._cache = {}
    
    def _save_cache(self) -> None:
        """Save quality scores to cache file."""
        # Ensure directory exists
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "version": "1.0",
            "updated_at": str(__import__('datetime').datetime.now().isoformat()),
            "scores": {
                sample_id: score.to_dict()
                for sample_id, score in self._cache.items()
            }
        }
        
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _compute_content_hash(self, content: str) -> str:
        """Compute hash of content for cache invalidation."""
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
    
    def _has_valid_field(self, content: str, field_name: str) -> bool:
        """
        Check if content has a valid (non-empty) field value.
        
        Args:
            content: The summary.md content
            field_name: The field name to check
        
        Returns:
            True if field exists with valid value
        """
        # Build pattern to match field name and aliases
        names_to_check = [field_name] + self.FIELD_ALIASES.get(field_name, [])
        
        for name in names_to_check:
            # Pattern 1: YAML front matter style (key: value)
            yaml_pattern = rf'{re.escape(name)}\s*[:：]\s*(.+?)(?:\n|$)'
            match = re.search(yaml_pattern, content, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                # Check if value is not empty or placeholder
                if value and value not in ['-', 'N/A', 'NA', '无', '未知', '—', '–']:
                    return True
            
            # Pattern 2: Markdown header style (## Field Name)
            header_pattern = rf'##\s*{re.escape(name)}'
            if re.search(header_pattern, content, re.IGNORECASE):
                return True
            
            # Pattern 3: Field mentioned with value in text
            text_pattern = rf'{re.escape(name)}[：:]\s*\d'
            if re.search(text_pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _calculate_dimension_score(
        self,
        content: str,
        fields: Dict[str, float]
    ) -> tuple[float, List[str]]:
        """
        Calculate score for a single dimension.
        
        Args:
            content: The summary.md content
            fields: Dict of field names and their weights
        
        Returns:
            Tuple of (score, missing_fields)
        """
        score = 0.0
        missing = []
        
        for field_name, weight in fields.items():
            if self._has_valid_field(content, field_name):
                score += weight
            else:
                # Don't add duplicate aliases to missing list
                if field_name not in ['tanδ']:  # Skip alternatives
                    missing.append(field_name)
        
        return min(score, 1.0), missing  # Cap at 1.0
    
    def score(self, sample_id: str, content: str) -> QualityScore:
        """
        Calculate quality score for a single sample.
        
        Args:
            sample_id: Sample ID (e.g., SSBR-002)
            content: summary.md content
        
        Returns:
            QualityScore object
        """
        content_hash = self._compute_content_hash(content)
        
        # Check cache
        if sample_id in self._cache:
            cached = self._cache[sample_id]
            if cached.content_hash == content_hash:
                return cached
        
        # Calculate scores for each dimension
        all_missing = []
        
        func_score, func_missing = self._calculate_dimension_score(
            content, self.FIELD_CONFIG['functionalization']['fields']
        )
        all_missing.extend(func_missing)
        
        mech_score, mech_missing = self._calculate_dimension_score(
            content, self.FIELD_CONFIG['mechanical']['fields']
        )
        all_missing.extend(mech_missing)
        
        therm_score, therm_missing = self._calculate_dimension_score(
            content, self.FIELD_CONFIG['thermal']['fields']
        )
        all_missing.extend(therm_missing)
        
        dyn_score, dyn_missing = self._calculate_dimension_score(
            content, self.FIELD_CONFIG['dynamic']['fields']
        )
        all_missing.extend(dyn_missing)
        
        src_score, src_missing = self._calculate_dimension_score(
            content, self.FIELD_CONFIG['source']['fields']
        )
        all_missing.extend(src_missing)
        
        # Create QualityScore object
        quality = QualityScore(
            sample_id=sample_id,
            functionalization_score=func_score,
            mechanical_score=mech_score,
            thermal_score=therm_score,
            dynamic_score=dyn_score,
            source_score=src_score,
            missing_fields=all_missing,
            content_hash=content_hash
        )
        quality.calculate_overall()
        
        # Update cache
        self._cache[sample_id] = quality
        
        return quality
    
    def batch_score(
        self,
        samples: List[Dict[str, str]],
        use_cache: bool = True
    ) -> Dict[str, QualityScore]:
        """
        Batch calculate quality scores for multiple samples.
        
        Args:
            samples: List of dicts with 'sample_id' and 'content' keys
            use_cache: Whether to use cached scores
        
        Returns:
            Dict mapping sample_id to QualityScore
        """
        results = {}
        
        for sample in samples:
            sample_id = sample.get('sample_id', '')
            content = sample.get('content', '')
            
            if not sample_id or not content:
                continue
            
            if use_cache and sample_id in self._cache:
                content_hash = self._compute_content_hash(content)
                cached = self._cache[sample_id]
                if cached.content_hash == content_hash:
                    results[sample_id] = cached
                    continue
            
            results[sample_id] = self.score(sample_id, content)
        
        return results
    
    def save_scores(self) -> None:
        """Save current scores to cache file."""
        self._save_cache()
    
    def get_cached_score(self, sample_id: str) -> Optional[QualityScore]:
        """
        Get cached score for a sample (without recalculating).
        
        Args:
            sample_id: Sample ID
        
        Returns:
            Cached QualityScore or None
        """
        return self._cache.get(sample_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about cached scores."""
        if not self._cache:
            return {"total": 0}
        
        scores = list(self._cache.values())
        overall_scores = [s.overall_score for s in scores]
        
        return {
            "total": len(scores),
            "avg_score": sum(overall_scores) / len(overall_scores),
            "min_score": min(overall_scores),
            "max_score": max(overall_scores),
            "high_quality_count": sum(1 for s in overall_scores if s >= 0.7),
            "medium_quality_count": sum(1 for s in overall_scores if 0.5 <= s < 0.7),
            "low_quality_count": sum(1 for s in overall_scores if s < 0.5),
        }


# =============================================================================
# CLI for testing and cache building
# =============================================================================

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description="Quality Scorer Utility")
    parser.add_argument("--build-cache", action="store_true",
                        help="Build quality scores cache for all samples")
    parser.add_argument("--stats", action="store_true",
                        help="Show cache statistics")
    parser.add_argument("--sample", type=str,
                        help="Score a specific sample by ID")
    
    args = parser.parse_args()
    
    scorer = QualityScorer()
    
    if args.stats:
        stats = scorer.get_stats()
        print("\n📊 Quality Scores Statistics:")
        print(f"  Total samples: {stats.get('total', 0)}")
        if stats.get('total', 0) > 0:
            print(f"  Average score: {stats.get('avg_score', 0):.2%}")
            print(f"  Score range: {stats.get('min_score', 0):.2%} - {stats.get('max_score', 0):.2%}")
            print(f"  High quality (≥70%): {stats.get('high_quality_count', 0)}")
            print(f"  Medium quality (50-70%): {stats.get('medium_quality_count', 0)}")
            print(f"  Low quality (<50%): {stats.get('low_quality_count', 0)}")
    
    elif args.sample:
        # Score a specific sample
        project_root = Path(__file__).parent.parent
        summary_path = project_root / "dataset" / "interpretations" / args.sample / "summary.md"
        
        if summary_path.exists():
            with open(summary_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            score = scorer.score(args.sample, content)
            print(f"\n📋 Quality Score for {args.sample}:")
            print(f"  Overall: {score.overall_score:.2%}")
            print(f"  Functionalization: {score.functionalization_score:.2%}")
            print(f"  Mechanical: {score.mechanical_score:.2%}")
            print(f"  Thermal: {score.thermal_score:.2%}")
            print(f"  Dynamic: {score.dynamic_score:.2%}")
            print(f"  Source: {score.source_score:.2%}")
            if score.missing_fields:
                print(f"  Missing fields: {', '.join(score.missing_fields)}")
        else:
            print(f"❌ Sample {args.sample} not found at {summary_path}")
    
    elif args.build_cache:
        print("Building quality scores cache...")
        # Will be implemented in T008
        print("Use 'python scripts/build_quality_cache.py' for full cache building")
    
    else:
        parser.print_help()
