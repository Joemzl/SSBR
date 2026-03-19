"""
Reranker Module for RAG QA System

This module implements cross-encoder reranking using BAAI/bge-reranker-base
to improve retrieval precision by reranking initial candidates.
"""

import os
import time
from typing import List, Optional, Tuple
from pathlib import Path

# Import from project modules
import sys
sys.path.insert(0, str(Path(__file__).parent))

from models import Candidate, RankedResult


class Reranker:
    """
    Cross-encoder reranker using bge-reranker-base.
    
    This class reranks candidate samples from vector search
    using a cross-encoder model for more accurate relevance scoring.
    """
    
    DEFAULT_MODEL = "BAAI/bge-reranker-base"
    MAX_LENGTH = 512
    
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: Optional[str] = None,
        lazy_load: bool = True
    ):
        """
        Initialize Reranker.
        
        Args:
            model_name: HuggingFace model name for cross-encoder
            device: Device to run model on ('cpu', 'cuda', or None for auto)
            lazy_load: If True, defer model loading until first use
        """
        self.model_name = model_name
        self.device = device
        self._model = None
        self._load_time_ms = 0
        
        if not lazy_load:
            self._load_model()
    
    def _load_model(self) -> None:
        """Load the cross-encoder model."""
        if self._model is not None:
            return
        
        start_time = time.time()
        
        try:
            from sentence_transformers import CrossEncoder
            
            # Determine device
            if self.device is None:
                import torch
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            print(f"Loading reranker model: {self.model_name} on {self.device}...")
            
            self._model = CrossEncoder(
                self.model_name,
                max_length=self.MAX_LENGTH,
                device=self.device
            )
            
            self._load_time_ms = int((time.time() - start_time) * 1000)
            print(f"Reranker loaded in {self._load_time_ms}ms")
            
        except ImportError:
            raise ImportError(
                "sentence-transformers is required for reranking. "
                "Install with: pip install sentence-transformers>=2.2.0"
            )
        except Exception as e:
            from utils.exceptions import RerankError
            raise RerankError(f"Failed to load reranker model: {e}", original_error=e)
    
    def warmup(self) -> int:
        """
        Warmup the model by running a dummy prediction.
        
        Returns:
            Load time in milliseconds
        """
        self._load_model()
        
        # Run dummy prediction for JIT compilation
        try:
            self._model.predict([("test query", "test document")])
        except Exception:
            pass
        
        return self._load_time_ms
    
    def rerank(
        self,
        query: str,
        candidates: List[Candidate],
        top_k: int = 3
    ) -> List[RankedResult]:
        """
        Rerank candidates using cross-encoder.
        
        Args:
            query: User query string
            candidates: List of Candidate objects from vector search
            top_k: Number of top results to return
        
        Returns:
            List of RankedResult objects, sorted by rerank_score descending
        """
        if not candidates:
            return []
        
        # Ensure model is loaded
        self._load_model()
        
        # Prepare query-document pairs
        pairs = [(query, c.content) for c in candidates]
        
        try:
            # Get rerank scores
            scores = self._model.predict(pairs)
            
            # Convert to list if numpy array
            if hasattr(scores, 'tolist'):
                scores = scores.tolist()
            
        except Exception as e:
            from utils.exceptions import RerankError
            raise RerankError(f"Reranking failed: {e}", original_error=e)
        
        # Create RankedResult objects with original ranks
        results = []
        for i, (candidate, score) in enumerate(zip(candidates, scores)):
            results.append(RankedResult(
                sample_id=candidate.sample_id,
                original_rank=i + 1,
                rerank_score=float(score),
                final_rank=0,  # Will be set after sorting
                similarity=candidate.similarity,
                quality_score=0.0,  # Will be set by QualityScorer
                content=candidate.content
            ))
        
        # Sort by rerank_score descending
        results.sort(key=lambda x: x.rerank_score, reverse=True)
        
        # Set final ranks and limit to top_k
        for i, result in enumerate(results[:top_k]):
            result.final_rank = i + 1
        
        return results[:top_k]
    
    def rerank_with_quality(
        self,
        query: str,
        candidates: List[Candidate],
        quality_scores: dict,
        top_k: int = 3,
        quality_weight: float = 0.1
    ) -> List[RankedResult]:
        """
        Rerank candidates considering both relevance and quality.
        
        The final score is computed as:
        final_score = rerank_score + quality_weight * quality_score
        
        Args:
            query: User query string
            candidates: List of Candidate objects
            quality_scores: Dict mapping sample_id to QualityScore
            top_k: Number of top results to return
            quality_weight: Weight for quality score in final ranking
        
        Returns:
            List of RankedResult objects
        """
        if not candidates:
            return []
        
        # First, get basic rerank results
        results = self.rerank(query, candidates, top_k=len(candidates))
        
        # Add quality scores and compute combined scores
        for result in results:
            quality = quality_scores.get(result.sample_id)
            if quality:
                result.quality_score = quality.overall_score
            else:
                result.quality_score = 0.5  # Default for unknown
        
        # Sort by combined score
        def combined_score(r: RankedResult) -> float:
            return r.rerank_score + quality_weight * r.quality_score
        
        results.sort(key=combined_score, reverse=True)
        
        # Update final ranks
        for i, result in enumerate(results[:top_k]):
            result.final_rank = i + 1
        
        return results[:top_k]
    
    def score_pairs(
        self,
        pairs: List[Tuple[str, str]]
    ) -> List[float]:
        """
        Score query-document pairs directly.
        
        Args:
            pairs: List of (query, document) tuples
        
        Returns:
            List of relevance scores
        """
        if not pairs:
            return []
        
        self._load_model()
        
        try:
            scores = self._model.predict(pairs)
            if hasattr(scores, 'tolist'):
                scores = scores.tolist()
            return [float(s) for s in scores]
        except Exception as e:
            from utils.exceptions import RerankError
            raise RerankError(f"Scoring failed: {e}", original_error=e)
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._model is not None
    
    @property
    def load_time_ms(self) -> int:
        """Get model load time in milliseconds."""
        return self._load_time_ms


# =============================================================================
# Singleton instance for reuse
# =============================================================================

_reranker_instance: Optional[Reranker] = None


def get_reranker(lazy_load: bool = True) -> Reranker:
    """
    Get singleton Reranker instance.
    
    Args:
        lazy_load: Whether to defer model loading
    
    Returns:
        Reranker instance
    """
    global _reranker_instance
    
    if _reranker_instance is None:
        _reranker_instance = Reranker(lazy_load=lazy_load)
    
    return _reranker_instance


# =============================================================================
# CLI for testing
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Reranker Utility")
    parser.add_argument("--warmup", action="store_true",
                        help="Load and warmup the model")
    parser.add_argument("--test", action="store_true",
                        help="Run a simple test")
    
    args = parser.parse_args()
    
    if args.warmup:
        print("Loading reranker model...")
        reranker = Reranker(lazy_load=False)
        load_time = reranker.warmup()
        print(f"✅ Reranker ready! Load time: {load_time}ms")
    
    elif args.test:
        print("Running reranker test...")
        reranker = Reranker()
        
        # Create test candidates
        test_candidates = [
            Candidate(
                sample_id="TEST-001",
                similarity=0.8,
                content="This document is about rubber modification and silica dispersion.",
                summary_path="test/path1.md"
            ),
            Candidate(
                sample_id="TEST-002",
                similarity=0.7,
                content="This document discusses polymer chemistry fundamentals.",
                summary_path="test/path2.md"
            ),
            Candidate(
                sample_id="TEST-003",
                similarity=0.6,
                content="This document covers white carbon black dispersion in SSBR compounds.",
                summary_path="test/path3.md"
            ),
        ]
        
        query = "How to improve silica dispersion in rubber?"
        
        print(f"\nQuery: {query}")
        print("\nOriginal order (by vector similarity):")
        for c in test_candidates:
            print(f"  {c.sample_id}: {c.similarity:.2f}")
        
        results = reranker.rerank(query, test_candidates, top_k=3)
        
        print("\nReranked order:")
        for r in results:
            print(f"  {r.sample_id}: rerank={r.rerank_score:.4f}, "
                  f"orig_rank={r.original_rank} → final_rank={r.final_rank}")
        
        print("\n✅ Test passed!")
    
    else:
        parser.print_help()
