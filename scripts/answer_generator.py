"""
Answer Generator Module for RAG QA System

This module generates natural language answers using OpenAI GPT API
based on retrieved and reranked samples.
"""

import os
import re
import time
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


class AnswerGenerator:
    """
    Generate natural language answers using GPT API.
    
    This class handles:
    - Building prompts from ranked results
    - Calling OpenAI API
    - Extracting and validating citations
    - Post-processing answers
    """
    
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_MAX_TOKENS = 800
    DEFAULT_TEMPERATURE = 0.3
    DEFAULT_TIMEOUT = 30
    
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        timeout: float = DEFAULT_TIMEOUT,
        api_key: Optional[str] = None
    ):
        """
        Initialize AnswerGenerator.
        
        Args:
            model: OpenAI model name
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            timeout: API timeout in seconds
            api_key: OpenAI API key (or use OPENAI_API_KEY env var)
        """
        self.model = os.environ.get("QA_MODEL", model)
        self.max_tokens = int(os.environ.get("QA_MAX_TOKENS", max_tokens))
        self.temperature = temperature
        self.timeout = timeout
        
        # Initialize OpenAI client
        self._client = None
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")
    
    def _get_client(self):
        """Get or create OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self._api_key,
                    timeout=self.timeout
                )
            except ImportError:
                raise ImportError(
                    "openai package is required. Install with: pip install openai>=1.0.0"
                )
        return self._client
    
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
        
        # Prepare samples for prompt
        samples_for_prompt = [
            {
                'sample_id': r.sample_id,
                'content': r.content,
                'similarity': r.similarity,
                'quality_score': r.quality_score
            }
            for r in ranked_results
        ]
        
        user_prompt = build_user_prompt(query, samples_for_prompt, prompt_answer_type)
        
        try:
            # Call OpenAI API
            client = self._get_client()
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            answer_text = response.choices[0].message.content.strip()
            
        except Exception as e:
            raise GenerationError(
                f"GPT API call failed: {str(e)[:200]}",
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
            model_used=self.model
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
        
        - Ensure proper formatting
        - Add reference disclaimer for REFERENCE type
        - Check length constraints
        
        Args:
            answer_text: Raw generated answer
            answer_type: Type of answer
        
        Returns:
            Processed answer text
        """
        # Clean up whitespace
        answer_text = answer_text.strip()
        
        # For REFERENCE type, ensure disclaimer is present
        if answer_type == AnswerType.REFERENCE:
            if "仅供参考" not in answer_text and "⚠️" not in answer_text:
                answer_text = "⚠️ **以下内容仅供参考，检索相关性中等**\n\n" + answer_text
        
        # For GUIDANCE type, ensure no false sample references
        if answer_type == AnswerType.GUIDANCE:
            # Remove any accidental sample references
            answer_text = re.sub(r'\[SSBR-\d+\]', '', answer_text)
        
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
    
    parser = argparse.ArgumentParser(description="Answer Generator Utility")
    parser.add_argument("--test", action="store_true",
                        help="Run a simple test")
    parser.add_argument("--query", type=str,
                        help="Test with a specific query")
    
    args = parser.parse_args()
    
    if args.test or args.query:
        print("Testing Answer Generator...")
        
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
            print(f"🔗 Citations: {[c.sample_id for c in answer.citations]}")
            print(f"📊 Confidence: {answer.confidence.value}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        parser.print_help()
