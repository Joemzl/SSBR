#!/usr/bin/env python3
"""
Build Quality Scores Cache

This script pre-computes quality scores for all sample summary.md files
and stores them in .cache/quality_scores.json for fast retrieval.

Usage:
    python scripts/build_quality_cache.py           # Incremental update
    python scripts/build_quality_cache.py --force   # Force rebuild all
    python scripts/build_quality_cache.py --stats   # Show statistics only
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "scripts"))

from quality_scorer import QualityScorer


def find_all_summaries(dataset_path: Path) -> list:
    """
    Find all summary.md files in the dataset.
    
    Args:
        dataset_path: Path to dataset/interpretations directory
    
    Returns:
        List of (sample_id, summary_path) tuples
    """
    summaries = []
    interpretations_dir = dataset_path / "interpretations"
    
    if not interpretations_dir.exists():
        print(f"❌ Directory not found: {interpretations_dir}")
        return summaries
    
    for sample_dir in interpretations_dir.iterdir():
        if sample_dir.is_dir() and sample_dir.name.startswith("SSBR-"):
            summary_path = sample_dir / "summary.md"
            if summary_path.exists():
                summaries.append((sample_dir.name, summary_path))
    
    # Sort by sample ID
    summaries.sort(key=lambda x: x[0])
    
    return summaries


def build_cache(force: bool = False, verbose: bool = True) -> dict:
    """
    Build quality scores cache for all samples.
    
    Args:
        force: If True, rebuild all scores even if cached
        verbose: If True, print progress
    
    Returns:
        Statistics dictionary
    """
    dataset_path = project_root / "dataset"
    cache_path = project_root / ".cache" / "quality_scores.json"
    
    # Initialize scorer
    scorer = QualityScorer(cache_path=cache_path)
    
    if force:
        scorer._cache = {}
        if verbose:
            print("🔄 Force rebuild mode - clearing existing cache")
    
    # Find all summaries
    summaries = find_all_summaries(dataset_path)
    
    if not summaries:
        print("❌ No summary files found!")
        return {"total": 0, "updated": 0, "cached": 0}
    
    if verbose:
        print(f"📁 Found {len(summaries)} summary files")
    
    # Process each summary
    updated = 0
    cached = 0
    
    for sample_id, summary_path in summaries:
        with open(summary_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already cached with same content hash
        existing = scorer.get_cached_score(sample_id)
        content_hash = scorer._compute_content_hash(content)
        
        if existing and existing.content_hash == content_hash and not force:
            cached += 1
            if verbose:
                print(f"  ⏭️  {sample_id}: cached (score={existing.overall_score:.0%})")
        else:
            score = scorer.score(sample_id, content)
            updated += 1
            if verbose:
                print(f"  ✅ {sample_id}: scored (score={score.overall_score:.0%})")
    
    # Save cache
    scorer.save_scores()
    
    stats = {
        "total": len(summaries),
        "updated": updated,
        "cached": cached,
        "cache_path": str(cache_path),
        "timestamp": datetime.now().isoformat()
    }
    
    if verbose:
        print(f"\n📊 Summary:")
        print(f"  Total samples: {stats['total']}")
        print(f"  Updated: {stats['updated']}")
        print(f"  Cached: {stats['cached']}")
        print(f"  Cache saved to: {stats['cache_path']}")
    
    return stats


def show_stats():
    """Show statistics about the quality scores cache."""
    cache_path = project_root / ".cache" / "quality_scores.json"
    
    if not cache_path.exists():
        print("❌ Cache file not found. Run without --stats to build cache.")
        return
    
    scorer = QualityScorer(cache_path=cache_path)
    stats = scorer.get_stats()
    
    print("\n📊 Quality Scores Cache Statistics")
    print("=" * 40)
    print(f"  Total samples: {stats.get('total', 0)}")
    
    if stats.get('total', 0) > 0:
        print(f"  Average score: {stats.get('avg_score', 0):.1%}")
        print(f"  Score range: {stats.get('min_score', 0):.1%} - {stats.get('max_score', 0):.1%}")
        print(f"\n  Quality Distribution:")
        print(f"    High (≥70%): {stats.get('high_quality_count', 0)} samples")
        print(f"    Medium (50-70%): {stats.get('medium_quality_count', 0)} samples")
        print(f"    Low (<50%): {stats.get('low_quality_count', 0)} samples")
    
    # Show cache file info
    if cache_path.exists():
        size_kb = cache_path.stat().st_size / 1024
        print(f"\n  Cache file: {cache_path}")
        print(f"  File size: {size_kb:.1f} KB")


def main():
    parser = argparse.ArgumentParser(
        description="Build Quality Scores Cache for SSBR samples"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force rebuild all scores (ignore existing cache)"
    )
    parser.add_argument(
        "--stats", "-s",
        action="store_true",
        help="Show cache statistics only"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet mode (less output)"
    )
    
    args = parser.parse_args()
    
    if args.stats:
        show_stats()
    else:
        print("🔧 Building Quality Scores Cache...")
        print("-" * 40)
        build_cache(force=args.force, verbose=not args.quiet)
        print("-" * 40)
        print("✅ Done!")


if __name__ == "__main__":
    main()
