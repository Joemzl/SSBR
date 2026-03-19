"""
QA Engine Module for RAG QA System

This is the main orchestrator that coordinates:
- Vector search (RAGSearchEngine)
- Quality scoring (QualityScorer)
- Reranking (Reranker)
- Answer generation (AnswerGenerator)

Implements the QAEngine.answer() API as specified in contracts/qa-api.md.
"""

import os
import time
from typing import List, Optional, Dict, Any
from pathlib import Path

# Import from project modules
import sys
sys.path.insert(0, str(Path(__file__).parent))

from models import (
    Query, Candidate, RankedResult, QAResponse, GeneratedAnswer,
    AnswerType, ConfidenceLevel, determine_answer_type, determine_confidence
)
from quality_scorer import QualityScorer
from reranker import Reranker, get_reranker
from answer_generator import AnswerGenerator, get_answer_generator
from rag_search import RAGSearchEngine, SearchResult
from utils.exceptions import (
    QAError, EmptyQueryError, QueryTooLongError, 
    GenerationError, NoSamplesError
)


class QAEngineConfig:
    """Configuration for QAEngine."""
    
    def __init__(
        self,
        similarity_threshold_high: float = 0.7,
        similarity_threshold_low: float = 0.5,
        rerank_candidates: int = 10,
        rerank_top_k: int = 3,
        answer_max_length: int = 500,
        generation_timeout: float = 30.0,
        enable_rerank: bool = True,
        enable_quality_scoring: bool = True
    ):
        self.similarity_threshold_high = similarity_threshold_high
        self.similarity_threshold_low = similarity_threshold_low
        self.rerank_candidates = rerank_candidates
        self.rerank_top_k = int(os.environ.get("RERANK_TOP_K", rerank_top_k))
        self.answer_max_length = answer_max_length
        self.generation_timeout = generation_timeout
        self.enable_rerank = enable_rerank
        self.enable_quality_scoring = enable_quality_scoring


class QAEngine:
    """
    Main QA Engine that orchestrates the question-answering pipeline.
    
    Pipeline:
    1. Query preprocessing
    2. Vector search (Top-10)
    3. Quality scoring
    4. Reranking (Top-10 → Top-3)
    5. Answer type determination
    6. Answer generation
    """
    
    def __init__(
        self,
        config: Optional[QAEngineConfig] = None,
        search_engine: Optional[RAGSearchEngine] = None,
        quality_scorer: Optional[QualityScorer] = None,
        reranker: Optional[Reranker] = None,
        answer_generator: Optional[AnswerGenerator] = None
    ):
        """
        Initialize QAEngine.
        
        Args:
            config: Engine configuration
            search_engine: RAG search engine instance
            quality_scorer: Quality scorer instance
            reranker: Reranker instance
            answer_generator: Answer generator instance
        """
        self.config = config or QAEngineConfig()
        
        # Initialize components (lazy load where possible)
        self._search_engine = search_engine
        self._quality_scorer = quality_scorer
        self._reranker = reranker
        self._answer_generator = answer_generator
    
    @property
    def search_engine(self) -> RAGSearchEngine:
        """Get or create search engine."""
        if self._search_engine is None:
            self._search_engine = RAGSearchEngine(use_cache=True)
        return self._search_engine
    
    @property
    def quality_scorer(self) -> QualityScorer:
        """Get or create quality scorer."""
        if self._quality_scorer is None:
            self._quality_scorer = QualityScorer()
        return self._quality_scorer
    
    @property
    def reranker(self) -> Reranker:
        """Get or create reranker."""
        if self._reranker is None:
            self._reranker = get_reranker(lazy_load=True)
        return self._reranker
    
    @property
    def answer_generator(self) -> AnswerGenerator:
        """Get or create answer generator."""
        if self._answer_generator is None:
            self._answer_generator = get_answer_generator(
                timeout=self.config.generation_timeout
            )
        return self._answer_generator
    
    def _validate_query(self, query: str) -> str:
        """
        Validate and preprocess query.
        
        Args:
            query: Raw user query
        
        Returns:
            Processed query string
        
        Raises:
            EmptyQueryError: If query is empty
            QueryTooLongError: If query exceeds limit
        """
        if not query or not query.strip():
            raise EmptyQueryError()
        
        query = query.strip()
        
        if len(query) > 1000:
            raise QueryTooLongError(len(query))
        
        return query
    
    def _search_candidates(self, query: str, top_k: int) -> List[Candidate]:
        """
        Search for candidate samples using vector similarity.
        
        Args:
            query: Processed query string
            top_k: Number of candidates to retrieve
        
        Returns:
            List of Candidate objects
        """
        # Use existing RAG search engine
        results: List[SearchResult] = self.search_engine.search(
            query=query,
            k=top_k
        )
        
        # Convert SearchResult to Candidate
        candidates = []
        for result in results:
            # Load content from summary.md
            content = self._load_sample_content(result.summary_path)
            
            candidates.append(Candidate(
                sample_id=result.sample_id,
                similarity=result.similarity,
                content=content,
                summary_path=result.summary_path
            ))
        
        return candidates
    
    def _load_sample_content(self, summary_path: str) -> str:
        """Load content from summary.md file."""
        try:
            path = Path(summary_path)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception:
            pass
        return ""
    
    def _score_candidates(
        self,
        candidates: List[Candidate]
    ) -> Dict[str, Any]:
        """
        Score candidate quality.
        
        Args:
            candidates: List of candidates to score
        
        Returns:
            Dict mapping sample_id to QualityScore
        """
        if not self.config.enable_quality_scoring:
            return {}
        
        samples = [
            {'sample_id': c.sample_id, 'content': c.content}
            for c in candidates
        ]
        
        return self.quality_scorer.batch_score(samples, use_cache=True)
    
    def _rerank_candidates(
        self,
        query: str,
        candidates: List[Candidate],
        quality_scores: Dict[str, Any],
        top_k: int
    ) -> List[RankedResult]:
        """
        Rerank candidates using cross-encoder.
        
        Args:
            query: User query
            candidates: Candidates to rerank
            quality_scores: Quality scores for candidates
            top_k: Number of results to return
        
        Returns:
            List of RankedResult objects
        """
        if not self.config.enable_rerank or not candidates:
            # Skip reranking, convert directly
            results = []
            for i, c in enumerate(candidates[:top_k]):
                quality = quality_scores.get(c.sample_id)
                results.append(RankedResult(
                    sample_id=c.sample_id,
                    original_rank=i + 1,
                    rerank_score=c.similarity,  # Use similarity as score
                    final_rank=i + 1,
                    similarity=c.similarity,
                    quality_score=quality.overall_score if quality else 0.5,
                    content=c.content
                ))
            return results
        
        # Use reranker
        results = self.reranker.rerank_with_quality(
            query=query,
            candidates=candidates,
            quality_scores=quality_scores,
            top_k=top_k
        )
        
        return results
    
    def _determine_answer_type(
        self,
        ranked_results: List[RankedResult]
    ) -> AnswerType:
        """
        Determine answer type based on similarity scores.
        
        Thresholds:
        - >= 0.7: DIRECT
        - >= 0.5: REFERENCE
        - < 0.5: GUIDANCE
        
        Args:
            ranked_results: Reranked results
        
        Returns:
            AnswerType enum
        """
        if not ranked_results:
            return AnswerType.GUIDANCE
        
        # Use the best similarity score
        max_similarity = max(r.similarity for r in ranked_results)
        
        return determine_answer_type(max_similarity)
    
    def answer(
        self,
        query: str,
        top_k: int = 3,
        include_samples: bool = True
    ) -> QAResponse:
        """
        Generate answer for user query.
        
        This is the main API entry point as defined in contracts/qa-api.md.
        
        Args:
            query: User query string
            top_k: Number of samples to use for answer generation
            include_samples: Whether to include sample list in response
        
        Returns:
            QAResponse containing answer and samples
        
        Raises:
            EmptyQueryError: If query is empty
            QueryTooLongError: If query exceeds limit
            GenerationError: If answer generation fails (can fall back)
        """
        total_start = time.time()
        
        # 1. Validate query
        query = self._validate_query(query)
        
        # 2. Search for candidates
        search_start = time.time()
        candidates = self._search_candidates(
            query, 
            top_k=self.config.rerank_candidates
        )
        search_time_ms = int((time.time() - search_start) * 1000)
        
        if not candidates:
            # No samples found, generate guidance answer
            return self._generate_empty_response(
                query, search_time_ms, total_start
            )
        
        # 3. Score quality
        quality_scores = self._score_candidates(candidates)
        
        # 4. Rerank
        rerank_start = time.time()
        ranked_results = self._rerank_candidates(
            query, candidates, quality_scores,
            top_k=min(top_k, self.config.rerank_top_k)
        )
        rerank_time_ms = int((time.time() - rerank_start) * 1000)
        
        # 5. Determine answer type
        answer_type = self._determine_answer_type(ranked_results)
        
        # 6. Generate answer
        generation_start = time.time()
        
        try:
            # 使用默认的 AnswerGenerator（model 参数已废弃，由环境变量配置）
            # 注意：新架构通过 LLMConfig 配置模型，不再支持运行时切换
            generator = self.answer_generator
            
            generated_answer = generator.generate(
                query=query,
                ranked_results=ranked_results,
                answer_type=answer_type
            )
        except GenerationError as e:
            # Fall back to recommendation-only mode
            generated_answer = self.answer_generator.generate_fallback(query, e)
        
        generation_time_ms = int((time.time() - generation_start) * 1000)
        total_time_ms = int((time.time() - total_start) * 1000)
        
        return QAResponse(
            answer=generated_answer,
            samples=ranked_results if include_samples else [],
            search_time_ms=search_time_ms,
            rerank_time_ms=rerank_time_ms,
            generation_time_ms=generation_time_ms,
            total_time_ms=total_time_ms
        )
    
    def _generate_empty_response(
        self,
        query: str,
        search_time_ms: int,
        total_start: float
    ) -> QAResponse:
        """Generate response when no samples found."""
        generation_start = time.time()
        
        generated_answer = self.answer_generator.generate_guidance(query)
        
        generation_time_ms = int((time.time() - generation_start) * 1000)
        total_time_ms = int((time.time() - total_start) * 1000)
        
        return QAResponse(
            answer=generated_answer,
            samples=[],
            search_time_ms=search_time_ms,
            rerank_time_ms=0,
            generation_time_ms=generation_time_ms,
            total_time_ms=total_time_ms
        )
    
    def search_only(
        self,
        query: str,
        top_k: int = 5
    ) -> List[RankedResult]:
        """
        Search without generating answer (recommendation mode).
        
        Args:
            query: User query
            top_k: Number of results
        
        Returns:
            List of RankedResult objects
        """
        query = self._validate_query(query)
        candidates = self._search_candidates(query, top_k=self.config.rerank_candidates)
        
        if not candidates:
            return []
        
        quality_scores = self._score_candidates(candidates)
        
        return self._rerank_candidates(
            query, candidates, quality_scores, top_k=top_k
        )
    
    def warmup(self) -> Dict[str, int]:
        """
        Warmup all components for faster first query.
        
        Returns:
            Dict with warmup times in milliseconds
        """
        times = {}
        
        # Warmup search engine (load vector cache)
        start = time.time()
        _ = self.search_engine
        times['search_engine'] = int((time.time() - start) * 1000)
        
        # Warmup quality scorer (load cache)
        start = time.time()
        _ = self.quality_scorer
        times['quality_scorer'] = int((time.time() - start) * 1000)
        
        # Warmup reranker (load model)
        if self.config.enable_rerank:
            start = time.time()
            self.reranker.warmup()
            times['reranker'] = int((time.time() - start) * 1000)
        
        return times


# =============================================================================
# Singleton instance
# =============================================================================

_qa_engine_instance: Optional[QAEngine] = None


def get_qa_engine(config: Optional[QAEngineConfig] = None) -> QAEngine:
    """
    Get singleton QAEngine instance.
    
    Args:
        config: Optional configuration
    
    Returns:
        QAEngine instance
    """
    global _qa_engine_instance
    
    if _qa_engine_instance is None:
        _qa_engine_instance = QAEngine(config=config)
    
    return _qa_engine_instance


# =============================================================================
# CLI for testing
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="QA Engine CLI")
    parser.add_argument("--query", "-q", type=str,
                        help="Query to answer")
    parser.add_argument("--search-only", "-s", action="store_true",
                        help="Search only, no answer generation")
    parser.add_argument("--warmup", action="store_true",
                        help="Warmup components")
    parser.add_argument("--top-k", "-k", type=int, default=3,
                        help="Number of results")
    parser.add_argument("--no-rerank", action="store_true",
                        help="Disable reranking")
    
    args = parser.parse_args()
    
    # Create engine with options
    config = QAEngineConfig(
        enable_rerank=not args.no_rerank
    )
    engine = QAEngine(config=config)
    
    if args.warmup:
        print("🔄 Warming up components...")
        times = engine.warmup()
        for component, ms in times.items():
            print(f"  {component}: {ms}ms")
        print("✅ Warmup complete!")
    
    elif args.query:
        if args.search_only:
            print(f"🔍 Searching: {args.query}\n")
            results = engine.search_only(args.query, top_k=args.top_k)
            
            for r in results:
                print(f"  {r.final_rank}. {r.sample_id}")
                print(f"     Similarity: {r.similarity:.2f}")
                print(f"     Rerank Score: {r.rerank_score:.4f}")
                print(f"     Quality: {r.quality_score:.0%}")
                print()
        else:
            print(f"❓ Query: {args.query}\n")
            response = engine.answer(args.query, top_k=args.top_k)
            
            print("📝 Answer:")
            print("-" * 50)
            print(response.answer.answer_text)
            print("-" * 50)
            print(f"\n📊 Type: {response.answer.answer_type.value}")
            print(f"🔗 Citations: {[c.sample_id for c in response.answer.citations]}")
            print(f"⏱️ Total time: {response.total_time_ms}ms")
            print(f"   (search: {response.search_time_ms}ms, "
                  f"rerank: {response.rerank_time_ms}ms, "
                  f"generation: {response.generation_time_ms}ms)")
    
    else:
        parser.print_help()
