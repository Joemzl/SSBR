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
    AnswerType, ConfidenceLevel, determine_answer_type, determine_confidence,
    # Synthesis models (004-multi-literature-synthesis)
    SynthesisMode, SynthesizedAnswer, SynthesisResponse, SampleSummary, DataRange,
    RecommendationCard, ConfidenceTag
)
from quality_scorer import QualityScorer
from reranker import Reranker, get_reranker
from answer_generator import AnswerGenerator, get_answer_generator
from rag_search import RAGSearchEngine, SearchResult
from utils.exceptions import (
    QAError, EmptyQueryError, QueryTooLongError, 
    GenerationError, NoSamplesError,
    InsufficientDataError, ExtrapolationBoundaryError, ConflictingTargetsError
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
        enable_quality_scoring: bool = True,
        # Synthesis config (004-multi-literature-synthesis)
        synthesis_top_k: int = 8,
        min_samples_trend: int = 3,
        min_samples_compare: int = 2,
        extrapolation_boundary: float = 0.5,
        synthesis_timeout: int = 8000,  # milliseconds (SC-006)
    ):
        self.similarity_threshold_high = similarity_threshold_high
        self.similarity_threshold_low = similarity_threshold_low
        self.rerank_candidates = rerank_candidates
        self.rerank_top_k = int(os.environ.get("RERANK_TOP_K", rerank_top_k))
        self.answer_max_length = answer_max_length
        self.generation_timeout = generation_timeout
        self.enable_rerank = enable_rerank
        self.enable_quality_scoring = enable_quality_scoring
        # Synthesis config
        self.synthesis_top_k = int(os.environ.get("SYNTHESIS_TOP_K", synthesis_top_k))
        self.min_samples_trend = int(os.environ.get("MIN_SAMPLES_TREND", min_samples_trend))
        self.min_samples_compare = int(os.environ.get("MIN_SAMPLES_COMPARE", min_samples_compare))
        self.extrapolation_boundary = float(os.environ.get("EXTRAPOLATION_BOUNDARY", extrapolation_boundary))
        self.synthesis_timeout = int(os.environ.get("SYNTHESIS_TIMEOUT", synthesis_timeout))


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
    
    # =========================================================================
    # Recommendation Card Parsing (FR-014a)
    # =========================================================================
    
    def _parse_recommendation_card(
        self,
        answer_text: str,
        sample_summaries: List['SampleSummary']
    ) -> Optional['RecommendationCard']:
        """
        从 GPT 回答中解析推荐卡片（FR-014a）。
        
        尝试从 Markdown 表格中提取推荐参数。
        
        Args:
            answer_text: GPT 生成的回答文本
            sample_summaries: 来源样本摘要列表
        
        Returns:
            RecommendationCard 或 None（如解析失败）
        """
        import re
        import logging
        from models import RecommendationCard, ConfidenceTag
        
        logger = logging.getLogger(__name__)
        
        try:
            # 尝试从表格中提取推荐参数
            # 匹配形如 | **推荐官能团** | 羟基 (-OH) | 高 |
            patterns = {
                'functional_group': [
                    r'\|\s*\*{0,2}推荐官能团\*{0,2}\s*\|\s*([^|]+?)\s*\|',
                    r'推荐官能团[：:]\s*([^\n]+)',
                ],
                'reagent': [
                    r'\|\s*\*{0,2}推荐试剂\*{0,2}\s*\|\s*([^|]+?)\s*\|',
                    r'推荐试剂[：:]\s*([^\n]+)',
                    r'\|\s*\*{0,2}官能化试剂\*{0,2}\s*\|\s*([^|]+?)\s*\|',
                ],
                'degree_range': [
                    r'\|\s*\*{0,2}推荐官能化程度\*{0,2}\s*\|\s*([^|]+?)\s*\|',
                    r'推荐官能化程度[：:]\s*([^\n]+)',
                    r'\|\s*\*{0,2}官能化程度\*{0,2}\s*\|\s*([^|]+?)\s*\|',
                ],
                'expected_improvement': [
                    r'\|\s*\*{0,2}预期改善效果\*{0,2}\s*\|\s*([^|]+?)\s*\|',
                    r'预期改善效果[：:]\s*([^\n]+)',
                    r'\|\s*\*{0,2}预期效果\*{0,2}\s*\|\s*([^|]+?)\s*\|',
                ],
            }
            
            extracted = {}
            for field, field_patterns in patterns.items():
                for pattern in field_patterns:
                    match = re.search(pattern, answer_text, re.IGNORECASE)
                    if match:
                        value = match.group(1).strip()
                        # 清理 Markdown 格式
                        value = re.sub(r'\*{1,2}', '', value)
                        value = value.strip()
                        if value and value not in ['-', 'N/A', '未知']:
                            extracted[field] = value
                            break
            
            # 检查必填字段
            required_fields = ['functional_group', 'reagent', 'degree_range', 'expected_improvement']
            if not all(f in extracted for f in required_fields):
                logger.debug(f"推荐卡片解析: 缺少必填字段, 已提取: {list(extracted.keys())}")
                # 尝试从样本摘要中补充信息
                if sample_summaries:
                    best_sample = sample_summaries[0]  # 使用相关度最高的样本
                    if 'functional_group' not in extracted and best_sample.functional_group:
                        extracted['functional_group'] = best_sample.functional_group
                    if 'reagent' not in extracted and best_sample.reagent:
                        extracted['reagent'] = best_sample.reagent
                    if 'degree_range' not in extracted and best_sample.functionalization_degree:
                        extracted['degree_range'] = best_sample.functionalization_degree
                    if 'expected_improvement' not in extracted:
                        extracted['expected_improvement'] = "改善目标性能"
            
            # 再次检查必填字段
            if not all(f in extracted for f in required_fields):
                logger.warning(f"推荐卡片解析失败: 仍缺少必填字段")
                return None
            
            # 解析置信度
            confidence = ConfidenceTag.MEDIUM  # 默认中等
            confidence_patterns = [
                (r'高置信度|🟢\s*高|置信度.*高', ConfidenceTag.HIGH),
                (r'低置信度|🔴\s*低|置信度.*低', ConfidenceTag.LOW),
            ]
            for pattern, tag in confidence_patterns:
                if re.search(pattern, answer_text, re.IGNORECASE):
                    confidence = tag
                    break
            
            # 解析最佳参考样本
            best_sample_ref = None
            best_ref_match = re.search(r'最佳参考样本[：:]\s*方案\s*(\d+)', answer_text)
            if best_ref_match:
                idx = int(best_ref_match.group(1)) - 1
                if 0 <= idx < len(sample_summaries):
                    best_sample_ref = sample_summaries[idx].sample_id
            
            # 提取推荐理由
            rationale = ""
            rationale_match = re.search(
                r'(?:推荐理由|##\s*推荐理由)\s*[：:]?\s*\n?\s*(.+?)(?=\n##|\n---|\Z)',
                answer_text,
                re.DOTALL | re.IGNORECASE
            )
            if rationale_match:
                rationale = rationale_match.group(1).strip()[:200]  # 限制长度
            
            # 构建推荐卡片
            card = RecommendationCard(
                functional_group=extracted['functional_group'],
                reagent=extracted['reagent'],
                degree_range=extracted['degree_range'],
                expected_improvement=extracted['expected_improvement'],
                confidence=confidence,
                best_sample_ref=best_sample_ref,
                supporting_samples=[s.sample_id for s in sample_summaries[:5]],
                rationale=rationale
            )
            
            logger.info(f"推荐卡片解析成功: {card.functional_group}, {card.degree_range}")
            return card
            
        except Exception as e:
            logger.error(f"推荐卡片解析异常: {e}")
            return None
    
    # =========================================================================
    # Input Validation (T054 - Phase 8)
    # =========================================================================
    
    def _validate_synthesis_params(
        self,
        top_k: int,
        min_samples: int,
        operation: str
    ) -> None:
        """
        验证综合分析参数（T054）。
        
        Args:
            top_k: 检索样本数
            min_samples: 最少样本数
            operation: 操作名称
        
        Raises:
            ValueError: 参数无效
        """
        if top_k < 1:
            raise ValueError(f"{operation}: top_k 必须 >= 1，当前 {top_k}")
        if top_k > 20:
            raise ValueError(f"{operation}: top_k 不能超过 20，当前 {top_k}")
        if min_samples < 1:
            raise ValueError(f"{operation}: min_samples 必须 >= 1，当前 {min_samples}")
        if min_samples > top_k:
            raise ValueError(f"{operation}: min_samples ({min_samples}) 不能大于 top_k ({top_k})")
    
    def _validate_target_properties(
        self,
        target_properties: Dict[str, str]
    ) -> Dict[str, str]:
        """
        验证并清洗目标性能参数（T054）。
        
        Args:
            target_properties: 原始目标性能
        
        Returns:
            清洗后的目标性能
        """
        if not target_properties:
            return {}
        
        cleaned = {}
        for key, value in target_properties.items():
            # 清洗键名
            key = str(key).strip()
            if not key:
                continue
            
            # 清洗值
            value = str(value).strip()
            if not value:
                continue
            
            # 长度限制
            if len(key) > 50:
                key = key[:50]
            if len(value) > 100:
                value = value[:100]
            
            cleaned[key] = value
        
        return cleaned
    
    def _validate_scheme_names(
        self,
        scheme_names: List[str]
    ) -> List[str]:
        """
        验证并清洗方案名称（T054）。
        
        Args:
            scheme_names: 原始方案名称列表
        
        Returns:
            清洗后的方案名称列表
        
        Raises:
            ValueError: 方案数量不足
        """
        if not scheme_names or len(scheme_names) < 2:
            raise ValueError("对比分析需要至少 2 个方案")
        
        cleaned = []
        for name in scheme_names:
            name = str(name).strip()
            if name and len(name) >= 2:
                if len(name) > 50:
                    name = name[:50]
                cleaned.append(name)
        
        if len(cleaned) < 2:
            raise ValueError("有效方案名称数量不足（需要至少 2 个）")
        
        return cleaned
    
    def _check_timeout(
        self,
        start_time: float,
        operation: str
    ) -> None:
        """
        检查是否超时（T056 - SC-006）。
        
        Args:
            start_time: 操作开始时间
            operation: 操作名称
        
        Raises:
            TimeoutError: 超时
        """
        from utils.exceptions import TimeoutError as QATimeoutError
        
        elapsed_ms = int((time.time() - start_time) * 1000)
        if elapsed_ms > self.config.synthesis_timeout:
            raise QATimeoutError(
                operation=operation,
                timeout_seconds=self.config.synthesis_timeout / 1000
            )
    
    # =========================================================================
    # Synthesis Mode Methods (004-multi-literature-synthesis)
    # =========================================================================
    
    def _detect_synthesis_mode(self, query: str) -> SynthesisMode:
        """
        自动检测查询意图，返回适合的综合模式（T015）。
        
        检测规则：
        - 包含"对比/比较 X 和 Y" → COMPARISON
        - 包含"设计配方/推荐配方" → FORMULA
        - 包含"趋势/规律/外推" 或 复杂综合问题 → SYNTHESIS
        - 其他简单问题 → SINGLE
        
        Args:
            query: 用户查询
        
        Returns:
            SynthesisMode 枚举值
        """
        import re
        
        query_lower = query.lower()
        
        # 检测对比分析模式
        comparison_patterns = [
            r'对比|比较|区别|差异|不同',
            r'和|与|vs\.?|versus',
            r'哪个.*更|更.*哪个',
        ]
        for pattern in comparison_patterns:
            if re.search(pattern, query_lower):
                # 确认是对比两个方案
                if re.search(r'(羟基|氨基|羧基|环氧|硅烷).*(羟基|氨基|羧基|环氧|硅烷)', query):
                    return SynthesisMode.COMPARISON
        
        # 检测配方设计模式
        formula_patterns = [
            r'设计.*(配方|方案)',
            r'推荐.*(配方|方案|参数)',
            r'如何.*配方',
            r'给出.*配方',
        ]
        for pattern in formula_patterns:
            if re.search(pattern, query_lower):
                return SynthesisMode.FORMULA
        
        # 检测综合分析模式
        synthesis_patterns = [
            r'趋势|规律|关系|影响',
            r'综合|整体|全面',
            r'外推|预测|估计',
            r'如何.*改善|如何.*提高|如何.*降低',
            r'同时|兼顾|平衡',
        ]
        for pattern in synthesis_patterns:
            if re.search(pattern, query_lower):
                return SynthesisMode.SYNTHESIS
        
        # 默认单样本模式（简单问题）
        return SynthesisMode.SINGLE
    
    def synthesize(
        self,
        query: str,
        top_k: int = 8,
        min_samples: int = 3,
        enable_trend: bool = True,
        enable_extrapolation: bool = True
    ) -> SynthesisResponse:
        """
        执行多文献综合问答（T016）。
        
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
        """
        import logging
        logger = logging.getLogger(__name__)
        
        from synthesis.aggregator import SampleAggregator
        from synthesis.citation_validator import CitationValidator
        from utils.prompt_templates import SYNTHESIS_SYSTEM_PROMPT, build_synthesis_prompt
        
        total_start = time.time()
        
        # T054: 输入验证
        self._validate_synthesis_params(top_k, min_samples, "综合分析")
        
        # 1. Validate query
        query = self._validate_query(query)
        logger.info(f"[synthesize] 开始综合分析: {query[:50]}...")
        
        # 2. Search for candidates (more than normal mode)
        search_start = time.time()
        candidates = self._search_candidates(
            query, 
            top_k=max(top_k, self.config.synthesis_top_k)
        )
        search_time_ms = int((time.time() - search_start) * 1000)
        logger.debug(f"[synthesize] 检索耗时: {search_time_ms}ms, 找到 {len(candidates)} 个候选")
        
        # Check minimum samples requirement (FR-005)
        if len(candidates) < min_samples:
            raise InsufficientDataError(
                required=min_samples,
                actual=len(candidates),
                operation="综合分析"
            )
        
        # 3. Score quality
        quality_scores = self._score_candidates(candidates)
        
        # 4. Rerank (get more samples for synthesis)
        rerank_start = time.time()
        ranked_results = self._rerank_candidates(
            query, candidates, quality_scores,
            top_k=min(top_k, len(candidates))
        )
        rerank_time_ms = int((time.time() - rerank_start) * 1000)
        
        # 5. Aggregate sample summaries (T011)
        synthesis_start = time.time()
        aggregator = SampleAggregator()
        sample_summaries = aggregator.aggregate_from_ranked_results(
            ranked_results, 
            top_k=min(5, len(ranked_results))  # FR-001: 综合 3-5 个样本
        )
        
        # 6. Calculate data ranges
        data_ranges = aggregator.get_data_ranges(sample_summaries)
        
        # 7. Generate synthesized answer (T017)
        answer_type = self._determine_answer_type(ranked_results)
        
        # Prepare samples for prompt
        samples_for_prompt = [s.to_dict() for s in sample_summaries]
        data_ranges_for_prompt = {k: v.to_dict() for k, v in data_ranges.items()}
        
        user_prompt = build_synthesis_prompt(
            query=query,
            samples=samples_for_prompt,
            data_ranges=data_ranges_for_prompt
        )
        
        generation_start = time.time()
        
        try:
            # Use answer generator's LLM client
            from utils.llm_client import UnifiedLLMClient, LLMConfig
            
            llm_config = LLMConfig.from_env()
            llm_config.max_tokens = 1200  # Synthesis needs more tokens
            llm_client = UnifiedLLMClient(llm_config)
            
            answer_text, provider = llm_client.chat(
                system_prompt=SYNTHESIS_SYSTEM_PROMPT,
                user_prompt=user_prompt
            )
            model_used = llm_client.get_model_name()
            
        except Exception as e:
            raise GenerationError(
                f"综合回答生成失败: {str(e)[:200]}",
                original_error=e
            )
        
        generation_time_ms = int((time.time() - generation_start) * 1000)
        synthesis_time_ms = int((time.time() - synthesis_start) * 1000)
        
        # 8. Validate and convert citations (T018)
        citation_validator = CitationValidator()
        converted_text, validated_citations = citation_validator.validate_and_convert(
            answer_text, sample_summaries
        )
        
        # Generate reference list and append to answer
        ref_list = citation_validator.generate_reference_list(validated_citations)
        if ref_list:
            converted_text = converted_text + "\n\n" + ref_list
        
        # Convert to Citation models
        literature_citations = citation_validator.extract_citations_to_models(validated_citations)
        
        # 8.5 Parse recommendation card from answer (FR-014a)
        recommendation_card = self._parse_recommendation_card(answer_text, sample_summaries)
        
        # 9. Build SynthesizedAnswer (T019, T021)
        from models import ConfidenceLevel
        avg_quality = sum(r.quality_score for r in ranked_results) / len(ranked_results) if ranked_results else 0
        confidence = ConfidenceLevel.HIGH if avg_quality >= 0.7 else (
            ConfidenceLevel.MEDIUM if avg_quality >= 0.5 else ConfidenceLevel.LOW
        )
        
        synthesized_answer = SynthesizedAnswer(
            answer_text=converted_text,
            answer_type=answer_type,
            confidence=confidence,
            query=query,
            generation_time_ms=generation_time_ms,
            model_used=model_used,
            synthesis_mode=SynthesisMode.SYNTHESIS,
            source_samples=sample_summaries,
            literature_citations=literature_citations,
            recommendation_card=recommendation_card  # FR-014a
        )
        
        # 10. Validate answer (T021)
        validation_errors = synthesized_answer.validate()
        if validation_errors:
            # Log warnings but don't fail
            import logging
            logger = logging.getLogger(__name__)
            for error in validation_errors:
                logger.warning(f"Synthesis validation: {error}")
        
        total_time_ms = int((time.time() - total_start) * 1000)
        
        return SynthesisResponse(
            answer=synthesized_answer,
            samples=ranked_results,
            data_ranges=data_ranges,
            search_time_ms=search_time_ms,
            rerank_time_ms=rerank_time_ms,
            synthesis_time_ms=synthesis_time_ms,
            generation_time_ms=generation_time_ms,
            total_time_ms=total_time_ms,
            sample_count=len(sample_summaries),
            unique_literature_count=synthesized_answer.get_unique_literature_count()
        )
    
    def design_formula(
        self,
        target_description: str,
        target_properties: Dict[str, str],
        top_k: int = 8,
        min_samples: int = 2
    ) -> SynthesisResponse:
        """
        根据目标性能设计配方（T037, FR-006, FR-007, FR-008）。
        
        Pipeline:
        1. 解析目标性能
        2. 检索相关样本
        3. 检测目标冲突
        4. 生成配方建议
        5. 生成取舍分析
        
        Args:
            target_description: 用户的目标描述（自然语言）
            target_properties: 目标性能字典 {property: target}
            top_k: 检索样本数
            min_samples: 最少样本数
        
        Returns:
            SynthesisResponse（含 FormulaRecommendation）
        
        Raises:
            InsufficientDataError: 样本数 < min_samples
            ConflictingTargetsError: 目标冲突且无法折中
        """
        import logging
        logger = logging.getLogger(__name__)
        
        from synthesis.aggregator import SampleAggregator
        from synthesis.formula_designer import FormulaDesigner, get_formula_designer
        from utils.prompt_templates import FORMULA_DESIGN_SYSTEM_PROMPT, build_formula_prompt
        
        total_start = time.time()
        
        # T054: 输入验证
        self._validate_synthesis_params(top_k, min_samples, "配方设计")
        target_properties = self._validate_target_properties(target_properties)
        
        logger.info(f"[design_formula] 开始配方设计: {target_description[:50]}...")
        
        # 1. 构建检索查询（综合目标描述）
        query = f"{target_description} " + " ".join(target_properties.keys())
        query = self._validate_query(query)
        
        # 2. 检索相关样本
        search_start = time.time()
        candidates = self._search_candidates(
            query,
            top_k=max(top_k, self.config.synthesis_top_k)
        )
        search_time_ms = int((time.time() - search_start) * 1000)
        
        if len(candidates) < min_samples:
            raise InsufficientDataError(
                required=min_samples,
                actual=len(candidates),
                operation="配方设计"
            )
        
        # 3. 质量评分 + 重排序
        quality_scores = self._score_candidates(candidates)
        rerank_start = time.time()
        ranked_results = self._rerank_candidates(
            query, candidates, quality_scores,
            top_k=min(top_k, len(candidates))
        )
        rerank_time_ms = int((time.time() - rerank_start) * 1000)
        
        # 4. 提取样本摘要
        synthesis_start = time.time()
        aggregator = SampleAggregator()
        sample_summaries = aggregator.aggregate_from_ranked_results(
            ranked_results,
            top_k=min(5, len(ranked_results))
        )
        
        # 5. 使用 FormulaDesigner 生成配方
        designer = get_formula_designer()
        formula_rec = designer.design_formula(
            target_properties=target_properties,
            samples=sample_summaries,
            constraints=None
        )
        
        # 6. 生成 LLM 配方建议文本
        generation_start = time.time()
        
        samples_for_prompt = [s.to_dict() for s in sample_summaries]
        user_prompt = build_formula_prompt(
            target_description=target_description,
            target_properties=target_properties,
            samples=samples_for_prompt
        )
        
        try:
            from utils.llm_client import UnifiedLLMClient, LLMConfig
            
            llm_config = LLMConfig.from_env()
            llm_config.max_tokens = 1000
            llm_client = UnifiedLLMClient(llm_config)
            
            answer_text, provider = llm_client.chat(
                system_prompt=FORMULA_DESIGN_SYSTEM_PROMPT,
                user_prompt=user_prompt
            )
            model_used = llm_client.get_model_name()
            
        except Exception as e:
            raise GenerationError(
                f"配方建议生成失败: {str(e)[:200]}",
                original_error=e
            )
        
        generation_time_ms = int((time.time() - generation_start) * 1000)
        synthesis_time_ms = int((time.time() - synthesis_start) * 1000)
        
        # 7. 构建响应
        from models import ConfidenceLevel
        answer_type = self._determine_answer_type(ranked_results)
        
        synthesized_answer = SynthesizedAnswer(
            answer_text=answer_text,
            answer_type=answer_type,
            confidence=ConfidenceLevel.MEDIUM if formula_rec.is_complete() else ConfidenceLevel.LOW,
            query=target_description,
            generation_time_ms=generation_time_ms,
            model_used=model_used,
            synthesis_mode=SynthesisMode.FORMULA,
            source_samples=sample_summaries,
            literature_citations=[],
            formula=formula_rec
        )
        
        total_time_ms = int((time.time() - total_start) * 1000)
        data_ranges = aggregator.get_data_ranges(sample_summaries)
        
        return SynthesisResponse(
            answer=synthesized_answer,
            samples=ranked_results,
            data_ranges=data_ranges,
            search_time_ms=search_time_ms,
            rerank_time_ms=rerank_time_ms,
            synthesis_time_ms=synthesis_time_ms,
            generation_time_ms=generation_time_ms,
            total_time_ms=total_time_ms,
            sample_count=len(sample_summaries),
            unique_literature_count=len(set(s.doi for s in sample_summaries if s.doi))
        )
    
    def compare(
        self,
        scheme_names: List[str],
        comparison_description: str = "",
        top_k_per_scheme: int = 5
    ) -> SynthesisResponse:
        """
        对比分析不同官能化方案（T047, FR-009, FR-010）。
        
        Pipeline:
        1. 按方案名称分别检索样本
        2. 提取样本摘要
        3. 生成对比表格
        4. LLM 生成综合评价
        
        Args:
            scheme_names: 待对比方案名称（如 ["羟基官能化", "环氧官能化"]）
            comparison_description: 对比说明（可选）
            top_k_per_scheme: 每个方案检索的样本数
        
        Returns:
            SynthesisResponse（含 ComparisonTable）
        """
        import logging
        logger = logging.getLogger(__name__)
        
        from synthesis.aggregator import SampleAggregator
        from synthesis.comparison_table import ComparisonTableGenerator, get_comparison_generator
        from utils.prompt_templates import COMPARISON_SYSTEM_PROMPT, build_comparison_prompt
        from models import ComparisonTable
        
        total_start = time.time()
        
        # T054: 输入验证
        scheme_names = self._validate_scheme_names(scheme_names)
        if top_k_per_scheme < 1 or top_k_per_scheme > 10:
            raise ValueError(f"top_k_per_scheme 必须在 1-10 之间，当前 {top_k_per_scheme}")
        
        logger.info(f"[compare] 开始对比分析: {' vs '.join(scheme_names)}")
        
        # 1. 按方案分别检索
        search_start = time.time()
        all_candidates = []
        samples_by_scheme: Dict[str, List[SampleSummary]] = {}
        aggregator = SampleAggregator()
        
        for scheme_name in scheme_names:
            # 检索该方案的相关样本
            query = f"{scheme_name}"
            candidates = self._search_candidates(query, top_k=top_k_per_scheme)
            
            if candidates:
                quality_scores = self._score_candidates(candidates)
                ranked = self._rerank_candidates(
                    query, candidates, quality_scores,
                    top_k=min(3, len(candidates))
                )
                all_candidates.extend(ranked)
                
                # 提取样本摘要
                summaries = aggregator.aggregate_from_ranked_results(
                    ranked,
                    top_k=min(3, len(ranked))
                )
                samples_by_scheme[scheme_name] = summaries
            else:
                samples_by_scheme[scheme_name] = []
        
        search_time_ms = int((time.time() - search_start) * 1000)
        
        # 2. 生成对比表格
        synthesis_start = time.time()
        comparison_gen = get_comparison_generator()
        comparison_table = comparison_gen.generate(
            scheme_names=scheme_names,
            samples_by_scheme=samples_by_scheme
        )
        
        # 3. LLM 生成综合评价
        generation_start = time.time()
        
        # 准备 prompt 数据
        samples_dict_by_scheme = {
            name: [s.to_dict() for s in samples]
            for name, samples in samples_by_scheme.items()
        }
        
        if not comparison_description:
            comparison_description = f"对比 {' 和 '.join(scheme_names)} 的区别"
        
        user_prompt = build_comparison_prompt(
            comparison_description=comparison_description,
            scheme_names=scheme_names,
            samples_by_scheme=samples_dict_by_scheme
        )
        
        try:
            from utils.llm_client import UnifiedLLMClient, LLMConfig
            
            llm_config = LLMConfig.from_env()
            llm_config.max_tokens = 1000
            llm_client = UnifiedLLMClient(llm_config)
            
            answer_text, provider = llm_client.chat(
                system_prompt=COMPARISON_SYSTEM_PROMPT,
                user_prompt=user_prompt
            )
            model_used = llm_client.get_model_name()
            
        except Exception as e:
            # Fallback: 使用表格的 Markdown 输出
            answer_text = comparison_table.to_markdown()
            model_used = "fallback"
        
        generation_time_ms = int((time.time() - generation_start) * 1000)
        synthesis_time_ms = int((time.time() - synthesis_start) * 1000)
        
        # 4. 构建响应
        from models import ConfidenceLevel
        all_samples_flat = []
        for samples in samples_by_scheme.values():
            all_samples_flat.extend(samples)
        
        synthesized_answer = SynthesizedAnswer(
            answer_text=answer_text,
            answer_type=AnswerType.DIRECT if all_samples_flat else AnswerType.GUIDANCE,
            confidence=ConfidenceLevel.MEDIUM if not comparison_table.has_missing_data() else ConfidenceLevel.LOW,
            query=comparison_description,
            generation_time_ms=generation_time_ms,
            model_used=model_used,
            synthesis_mode=SynthesisMode.COMPARISON,
            source_samples=all_samples_flat,
            literature_citations=[],
            comparison=comparison_table
        )
        
        total_time_ms = int((time.time() - total_start) * 1000)
        
        return SynthesisResponse(
            answer=synthesized_answer,
            samples=all_candidates,
            data_ranges={},  # 对比模式不需要数据范围
            search_time_ms=search_time_ms,
            rerank_time_ms=0,  # 已包含在 search 中
            synthesis_time_ms=synthesis_time_ms,
            generation_time_ms=generation_time_ms,
            total_time_ms=total_time_ms,
            sample_count=len(all_samples_flat),
            unique_literature_count=len(set(s.doi for s in all_samples_flat if s.doi))
        )


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
    
    # 004-multi-literature-synthesis: 综合模式参数
    parser.add_argument("--synthesize", action="store_true",
                        help="Enable multi-literature synthesis mode")
    parser.add_argument("--compare", type=str, nargs="+",
                        help="Compare schemes (e.g., --compare 羟基官能化 环氧官能化)")
    parser.add_argument("--design", type=str,
                        help="Design formula for target (e.g., --design '高湿地抓地力低滚阻')")
    parser.add_argument("--target", type=str, nargs="*",
                        help="Target properties for design (e.g., --target 湿地抓地力=高 滚动阻力=低)")
    parser.add_argument("--no-extrapolation", action="store_true",
                        help="Disable extrapolation in synthesis mode")
    parser.add_argument("--benchmark", action="store_true",
                        help="Run performance benchmark (SC-006: 8s SLA)")
    parser.add_argument("--benchmark-runs", type=int, default=3,
                        help="Number of benchmark runs (default: 3)")
    
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
    
    # 性能基准测试 (--benchmark) - T060
    elif args.benchmark:
        print("=" * 60)
        print("Performance Benchmark (SC-006: 8s SLA)")
        print("=" * 60)
        
        # 预热
        print("\n📦 Warming up components...")
        warmup_times = engine.warmup()
        print(f"   Warmup complete in {sum(warmup_times.values())}ms")
        
        # 测试用例
        benchmark_cases = [
            {
                "name": "Single QA (answer)",
                "type": "single",
                "query": "如何改善白炭黑分散性？",
            },
            {
                "name": "Synthesis (synthesize)",
                "type": "synthesis",
                "query": "官能化程度如何影响力学性能？",
            },
            {
                "name": "Comparison (compare)",
                "type": "compare",
                "schemes": ["羟基官能化", "环氧官能化"],
            },
            {
                "name": "Formula Design (design_formula)",
                "type": "design",
                "desc": "高湿地抓地力低滚阻配方",
                "props": {"湿地抓地力": "高", "滚动阻力": "低"},
            },
        ]
        
        results = []
        runs = args.benchmark_runs
        
        for case in benchmark_cases:
            print(f"\n🧪 Testing: {case['name']} ({runs} runs)")
            times = []
            errors = []
            
            for i in range(runs):
                try:
                    start = time.time()
                    
                    if case["type"] == "single":
                        response = engine.answer(case["query"])
                        elapsed = response.total_time_ms
                    elif case["type"] == "synthesis":
                        response = engine.synthesize(case["query"], top_k=5, min_samples=2)
                        elapsed = response.total_time_ms
                    elif case["type"] == "compare":
                        response = engine.compare(case["schemes"])
                        elapsed = response.total_time_ms
                    elif case["type"] == "design":
                        response = engine.design_formula(case["desc"], case["props"], min_samples=1)
                        elapsed = response.total_time_ms
                    else:
                        continue
                    
                    times.append(elapsed)
                    print(f"   Run {i+1}: {elapsed}ms {'[PASS]' if elapsed <= 8000 else '[FAIL]'}")
                    
                except Exception as e:
                    errors.append(str(e))
                    print(f"   Run {i+1}: ERROR - {str(e)[:50]}")
            
            if times:
                avg = sum(times) / len(times)
                min_t = min(times)
                max_t = max(times)
                passed = all(t <= 8000 for t in times)
                results.append({
                    "name": case["name"],
                    "avg_ms": avg,
                    "min_ms": min_t,
                    "max_ms": max_t,
                    "passed": passed,
                    "errors": len(errors)
                })
            else:
                results.append({
                    "name": case["name"],
                    "avg_ms": 0,
                    "min_ms": 0,
                    "max_ms": 0,
                    "passed": False,
                    "errors": len(errors)
                })
        
        # 汇总结果
        print("\n" + "=" * 60)
        print("Benchmark Results")
        print("=" * 60)
        print(f"{'Test Case':<35} {'Avg (ms)':<10} {'Min':<8} {'Max':<8} {'Status':<8}")
        print("-" * 60)
        
        all_passed = True
        for r in results:
            status = "[PASS]" if r["passed"] else "[FAIL]"
            if not r["passed"]:
                all_passed = False
            print(f"{r['name']:<35} {r['avg_ms']:<10.0f} {r['min_ms']:<8.0f} {r['max_ms']:<8.0f} {status}")
            if r["errors"] > 0:
                print(f"   (Errors: {r['errors']})")
        
        print("-" * 60)
        print(f"Overall: {'[PASS] All tests within 8s SLA' if all_passed else '[FAIL] Some tests exceeded 8s SLA'}")
        print("=" * 60)
    
    # 对比分析模式 (--compare)
    elif args.compare:
        scheme_names = args.compare
        description = args.query or f"对比 {' 和 '.join(scheme_names)} 的区别"
        
        print(f"📊 Comparing: {', '.join(scheme_names)}\n")
        
        try:
            response = engine.compare(
                scheme_names=scheme_names,
                comparison_description=description
            )
            
            print("📝 Comparison Result:")
            print("-" * 50)
            print(response.answer.answer_text)
            print("-" * 50)
            
            # 显示表格（如有）
            if response.answer.comparison:
                print("\n📋 Comparison Table:")
                print(response.answer.comparison.to_markdown())
            
            print(f"\n⏱️ Total time: {response.total_time_ms}ms")
            print(f"📚 Samples used: {response.sample_count}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # 配方设计模式 (--design)
    elif args.design:
        target_desc = args.design
        
        # 解析目标属性
        target_props = {}
        if args.target:
            for item in args.target:
                if "=" in item:
                    k, v = item.split("=", 1)
                    target_props[k.strip()] = v.strip()
        
        print(f"🧪 Designing formula for: {target_desc}\n")
        if target_props:
            print(f"   Target properties: {target_props}")
        
        try:
            response = engine.design_formula(
                target_description=target_desc,
                target_properties=target_props,
                top_k=args.top_k
            )
            
            print("\n📝 Formula Recommendation:")
            print("-" * 50)
            print(response.answer.answer_text)
            print("-" * 50)
            
            # 显示配方详情（如有）
            if response.answer.formula:
                f = response.answer.formula
                print(f"\n🎯 Recommended:")
                print(f"   - Functional Group: {f.recommended_functional_group}")
                print(f"   - Degree: {f.recommended_degree}")
                print(f"   - Filler: {f.recommended_filler}")
                print(f"   - Confidence: {f.confidence.value}")
                
                if f.trade_offs:
                    print(f"\n⚠️ Trade-offs:")
                    for t in f.trade_offs:
                        print(f"   - {t}")
            
            print(f"\n⏱️ Total time: {response.total_time_ms}ms")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # 综合问答模式 (--synthesize)
    elif args.synthesize and args.query:
        print(f"🔬 Synthesizing: {args.query}\n")
        
        try:
            response = engine.synthesize(
                query=args.query,
                top_k=args.top_k,
                enable_extrapolation=not args.no_extrapolation
            )
            
            print("📝 Synthesized Answer:")
            print("-" * 50)
            print(response.answer.answer_text)
            print("-" * 50)
            print(f"\n📊 Mode: {response.answer.synthesis_mode.value}")
            print(f"📚 Sources: {response.sample_count} samples, {response.unique_literature_count} unique literature")
            print(f"⏱️ Total time: {response.total_time_ms}ms")
            
            if not response.meets_performance_target():
                print(f"⚠️ Warning: Exceeded 8s performance target")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
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
