"""
Answer Generator Module for RAG QA System

This module generates natural language answers using LLM APIs
based on retrieved and reranked samples.

支持的模型提供商（按优先级）：
1. Claude 3.5 Sonnet (优先，需要 ANTHROPIC_API_KEY)
2. GPT-4o-mini (降级，需要 OPENAI_API_KEY)

配置方式：
- 设置 ANTHROPIC_API_KEY 启用 Claude
- 设置 OPENAI_API_KEY 作为降级或默认选项
- Claude 不可用时自动降级到 OpenAI
"""

import os
import re
import time
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

# Import from project modules
import sys
sys.path.insert(0, str(Path(__file__).parent))

from models import (
    RankedResult, GeneratedAnswer, Citation, 
    AnswerType, ConfidenceLevel, determine_confidence
)
from utils.prompt_templates import (
    get_system_prompt, build_user_prompt, AnswerType as PromptAnswerType
)
from utils.exceptions import GenerationError, handle_generation_error
from utils.llm_client import UnifiedLLMClient, LLMConfig, LLMProvider

logger = logging.getLogger(__name__)


class AnswerGenerator:
    """
    Generate natural language answers using LLM APIs.
    
    This class handles:
    - Building prompts from ranked results
    - Calling LLM API (Claude 优先, OpenAI 降级)
    - Extracting and validating citations
    - Post-processing answers
    
    Usage:
        generator = AnswerGenerator()
        answer = generator.generate(query, ranked_results, answer_type)
        print(f"使用模型: {answer.model_used}")
    """
    
    DEFAULT_MAX_TOKENS = 800
    DEFAULT_TEMPERATURE = 0.3
    DEFAULT_TIMEOUT = 30
    
    def __init__(
        self,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        timeout: float = DEFAULT_TIMEOUT,
        llm_config: Optional[LLMConfig] = None
    ):
        """
        Initialize AnswerGenerator.
        
        Args:
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            timeout: API timeout in seconds
            llm_config: LLM 配置，默认从环境变量加载
        """
        self.max_tokens = int(os.environ.get("QA_MAX_TOKENS", max_tokens))
        self.temperature = temperature
        self.timeout = timeout
        
        # 初始化统一 LLM 客户端
        if llm_config is None:
            llm_config = LLMConfig.from_env()
            llm_config.max_tokens = self.max_tokens
            llm_config.temperature = self.temperature
            llm_config.timeout = self.timeout
        
        self._llm_client = UnifiedLLMClient(llm_config)
        self._last_provider: Optional[LLMProvider] = None
    
    def generate(
        self,
        query: str,
        ranked_results: List[RankedResult],
        answer_type: AnswerType
    ) -> GeneratedAnswer:
        """
        Generate answer based on ranked results.
        
        Args:
            query: User's original query
            ranked_results: Reranked sample results
            answer_type: Type of answer to generate
        
        Returns:
            GeneratedAnswer object
        """
        start_time = time.time()
        
        # Convert answer type for prompt templates
        prompt_answer_type = PromptAnswerType(answer_type.value)
        
        # Build prompts
        system_prompt = get_system_prompt(prompt_answer_type)
        
        # 使用 SampleAggregator 提取结构化元数据
        from synthesis.aggregator import SampleAggregator
        aggregator = SampleAggregator()
        
        # Prepare samples for prompt with structured metadata
        samples_for_prompt = []
        for r in ranked_results:
            # 从 content 中提取结构化元数据
            summary = aggregator.extract_summary(
                sample_id=r.sample_id,
                content=r.content,
                similarity=r.similarity,
                quality_score=r.quality_score
            )
            
            # 合并结构化元数据和原始内容
            sample_dict = {
                'sample_id': r.sample_id,
                'content': r.content,
                'similarity': r.similarity,
                'quality_score': r.quality_score,
                # 添加结构化元数据字段
                'functional_group': summary.functional_group,
                'functionalization_degree': summary.functionalization_degree,
                'reagent': summary.reagent,
                'method': summary.method,
                'doi': summary.doi,
                'first_author': summary.first_author,
                'year': summary.year,
                'tensile_strength': summary.tensile_strength,
                'elongation': summary.elongation,
                'tg': summary.tg,
            }
            samples_for_prompt.append(sample_dict)
        
        user_prompt = build_user_prompt(query, samples_for_prompt, prompt_answer_type)
        
        try:
            # 使用统一 LLM 客户端调用 (Claude 优先, OpenAI 降级)
            answer_text, provider = self._llm_client.chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            self._last_provider = provider
            
            # 记录降级日志（仅后台可见）
            if self._llm_client.fallback_used:
                logger.warning(
                    f"LLM 降级触发: Claude → OpenAI, 原因: {self._llm_client.fallback_reason}"
                )
            
        except Exception as e:
            raise GenerationError(
                f"LLM API call failed: {str(e)[:200]}",
                original_error=e
            )
        
        generation_time_ms = int((time.time() - start_time) * 1000)
        
        # Extract citations from answer
        citations = self._extract_citations(answer_text, ranked_results)
        
        # Validate citations
        valid_citations = self._validate_citations(citations, ranked_results)
        
        # Post-process answer
        answer_text = self._post_process_answer(answer_text, answer_type)
        
        # Determine confidence level
        avg_quality = sum(r.quality_score for r in ranked_results) / len(ranked_results) if ranked_results else 0
        confidence = determine_confidence(answer_type, avg_quality)
        
        return GeneratedAnswer(
            answer_text=answer_text,
            answer_type=answer_type,
            citations=valid_citations,
            confidence=confidence,
            query=query,
            source_samples=[r.sample_id for r in ranked_results],
            generation_time_ms=generation_time_ms,
            model_used=self._llm_client.get_model_name()
        )
    
    def generate_guidance(self, query: str) -> GeneratedAnswer:
        """
        Generate guidance answer when no relevant samples found.
        
        Args:
            query: User's original query
        
        Returns:
            GeneratedAnswer with GUIDANCE type
        """
        return self.generate(query, [], AnswerType.GUIDANCE)
    
    def _extract_citations(
        self,
        answer_text: str,
        ranked_results: List[RankedResult]
    ) -> List[Citation]:
        """
        Extract citations from generated answer text.
        
        Looks for patterns like [SSBR-002], [SSBR-015] in the text.
        
        Args:
            answer_text: Generated answer text
            ranked_results: Source samples for citation metadata
        
        Returns:
            List of Citation objects
        """
        citations = []
        seen_ids = set()
        
        # 防御 None 输入
        if not answer_text:
            return citations
        
        # Pattern to match sample ID citations: [SSBR-XXX]
        pattern = r'\[SSBR-(\d+)\]'
        matches = re.findall(pattern, answer_text)
        
        # Create lookup for sample metadata
        sample_lookup = {r.sample_id: r for r in ranked_results}
        
        for match in matches:
            sample_id = f"SSBR-{match}"
            
            if sample_id in seen_ids:
                continue
            seen_ids.add(sample_id)
            
            # Get sample metadata if available
            sample = sample_lookup.get(sample_id)
            
            # Extract DOI and citation from content if available
            doi = None
            citation_text = None
            
            if sample:
                doi = self._extract_doi(sample.content)
                citation_text = self._extract_citation_text(sample.content)
            
            citations.append(Citation(
                sample_id=sample_id,
                data_type="综合数据",  # Default type
                doi=doi,
                citation_text=citation_text
            ))
        
        return citations
    
    def _extract_doi(self, content: str) -> Optional[str]:
        """Extract DOI from sample content."""
        if not content:
            return None
        
        # Pattern for DOI
        doi_pattern = r'(?:DOI|doi)[：:]\s*(10\.\d{4,}/[^\s\n]+)'
        match = re.search(doi_pattern, content)
        if match:
            return match.group(1).rstrip('.,;')
        
        # Alternative pattern
        doi_pattern2 = r'(10\.\d{4,}/[^\s\n]+)'
        match = re.search(doi_pattern2, content)
        if match:
            return match.group(1).rstrip('.,;')
        
        return None
    
    def _extract_citation_text(self, content: str) -> Optional[str]:
        """Extract citation text from sample content."""
        if not content:
            return None
        
        # Look for citation in YAML front matter or text
        citation_pattern = r'(?:引文|citation|cite)[：:]\s*([^\n]+)'
        match = re.search(citation_pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None
    
    def _validate_citations(
        self,
        citations: List[Citation],
        ranked_results: List[RankedResult]
    ) -> List[Citation]:
        """
        Validate citations against source samples.
        
        Only keep citations that reference actual source samples.
        
        Args:
            citations: Extracted citations
            ranked_results: Source samples
        
        Returns:
            List of valid citations
        """
        valid_sample_ids = {r.sample_id for r in ranked_results}
        
        valid_citations = []
        for citation in citations:
            if citation.sample_id in valid_sample_ids:
                valid_citations.append(citation)
            # Invalid citations are silently dropped (per data-model.md spec)
        
        return valid_citations
    
    def _post_process_answer(
        self,
        answer_text: str,
        answer_type: AnswerType
    ) -> str:
        """
        Post-process generated answer.
        
        - Remove any sample IDs that may have leaked through
        - Ensure proper formatting
        - Add reference disclaimer for REFERENCE type
        - Check length constraints
        
        Args:
            answer_text: Raw generated answer
            answer_type: Type of answer
        
        Returns:
            Processed answer text
        """
        # 防御 None 输入
        if not answer_text:
            return "无法生成回答，请稍后重试。"
        
        # Clean up whitespace
        answer_text = answer_text.strip()
        
        # 移除所有样本 ID 引用（用户界面不应显示内部 ID）
        # 匹配格式：[SSBR-XXX]、（样本 SSBR-XXX）、SSBR-XXX 等
        answer_text = re.sub(r'\[SSBR-\d+\]', '', answer_text)
        answer_text = re.sub(r'[（(]样本\s*SSBR-\d+[）)]', '', answer_text)
        answer_text = re.sub(r'样本\s*SSBR-\d+', '该方案', answer_text)
        answer_text = re.sub(r'SSBR-\d+\s*样本', '该方案', answer_text)
        # 单独出现的 SSBR-XXX（带编号格式）
        answer_text = re.sub(r'(?<!\w)SSBR-\d{3}(?!\w)', '该方案', answer_text)
        
        # 清理行内多余空格（保留换行符，只处理同一行内的多个连续空格）
        answer_text = re.sub(r'[^\S\n]+', ' ', answer_text)  # 只替换非换行的空白字符
        answer_text = re.sub(r' ([，。、；：])', r'\1', answer_text)
        
        # 清理多余的空行（超过2个连续空行变成2个）
        answer_text = re.sub(r'\n{3,}', '\n\n', answer_text)
        
        # For REFERENCE type, ensure disclaimer is present
        if answer_type == AnswerType.REFERENCE:
            if "仅供参考" not in answer_text and "⚠️" not in answer_text:
                answer_text = "⚠️ **以下内容仅供参考，检索相关性中等**\n\n" + answer_text
        
        return answer_text
    
    def generate_fallback(self, query: str, error: Exception) -> GeneratedAnswer:
        """
        Generate fallback response when generation fails.
        
        Args:
            query: User's original query
            error: The exception that caused failure
        
        Returns:
            Fallback GeneratedAnswer
        """
        fallback_text = handle_generation_error(error)
        
        return GeneratedAnswer(
            answer_text=fallback_text,
            answer_type=AnswerType.GUIDANCE,
            citations=[],
            confidence=ConfidenceLevel.LOW,
            query=query,
            source_samples=[],
            generation_time_ms=0,
            model_used="fallback"
        )


# =============================================================================
# Singleton instance for reuse
# =============================================================================

_generator_instance: Optional[AnswerGenerator] = None


def get_answer_generator(**kwargs) -> AnswerGenerator:
    """
    Get singleton AnswerGenerator instance.
    
    Args:
        **kwargs: Arguments to pass to AnswerGenerator constructor
    
    Returns:
        AnswerGenerator instance
    """
    global _generator_instance
    
    if _generator_instance is None:
        _generator_instance = AnswerGenerator(**kwargs)
    
    return _generator_instance


# =============================================================================
# CLI for testing
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    parser = argparse.ArgumentParser(description="Answer Generator Utility")
    parser.add_argument("--test", action="store_true",
                        help="Run a simple test")
    parser.add_argument("--query", type=str,
                        help="Test with a specific query")
    
    args = parser.parse_args()
    
    if args.test or args.query:
        print("Testing Answer Generator...")
        print("=" * 60)
        
        # 显示 LLM 配置
        config = LLMConfig.from_env()
        print(f"📋 LLM 配置:")
        print(f"   Claude API Key: {'已配置' if config.claude_api_key else '未配置'}")
        print(f"   OpenAI API Key: {'已配置' if config.openai_api_key else '未配置'}")
        print(f"   降级策略: {'启用' if config.enable_fallback else '禁用'}")
        print("=" * 60)
        
        # Create test ranked results
        test_results = [
            RankedResult(
                sample_id="SSBR-002",
                original_rank=1,
                rerank_score=0.85,
                final_rank=1,
                similarity=0.75,
                quality_score=0.9,
                content="""# SSBR-002 综合档案

## 官能化信息
- 官能化试剂: 3-氨基丙基三乙氧基硅烷
- 官能化程度: 高
- 核心官能团: -NH2

## 性能数据
- 拉伸强度: 18.5 MPa
- 断裂伸长率: 450%
- Tg: -25°C

## 文献来源
DOI: 10.1016/j.polymer.2023.001
"""
            )
        ]
        
        query = args.query or "如何改善白炭黑分散性？"
        
        generator = AnswerGenerator()
        
        try:
            answer = generator.generate(
                query=query,
                ranked_results=test_results,
                answer_type=AnswerType.DIRECT
            )
            
            print(f"\n📝 Query: {query}")
            print(f"\n📄 Answer ({answer.answer_type.value}):")
            print("-" * 50)
            print(answer.answer_text)
            print("-" * 50)
            print(f"\n⏱️ Generation time: {answer.generation_time_ms}ms")
            print(f"🤖 Model used: {answer.model_used}")
            print(f"🔗 Citations: {[c.sample_id for c in answer.citations]}")
            print(f"📊 Confidence: {answer.confidence.value}")
            
            # 显示降级信息（如果有）
            if generator._llm_client.fallback_used:
                print(f"\n⚠️ 降级触发: {generator._llm_client.fallback_reason}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        parser.print_help()
