"""
Prompt Templates Module for RAG QA System

This module provides prompt templates for generating answers based on
retrieved samples. Templates are designed to ensure:
1. All citations are traceable to sample IDs
2. Clear distinction between literature data and general advice
3. Professional and accurate responses
4. Controlled length (300-500 characters)
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class AnswerType(Enum):
    """Answer type based on similarity threshold."""
    DIRECT = "direct"        # similarity >= 0.7
    REFERENCE = "reference"  # 0.5 <= similarity < 0.7
    GUIDANCE = "guidance"    # similarity < 0.5


@dataclass
class PromptConfig:
    """Configuration for prompt generation."""
    max_answer_length: int = 500
    min_answer_length: int = 300
    model: str = "gpt-4o-mini"
    temperature: float = 0.3


# =============================================================================
# System Prompts
# =============================================================================

SYSTEM_PROMPT_DIRECT = """你是一位 SSBR（溶聚丁苯橡胶）官能化改性领域的专家，拥有丰富的高分子材料研究经验。

你的任务是基于用户提供的检索样本信息，生成专业、准确的技术回答。

## 回答规范

1. **引用规范**：
   - 使用官能团类型或试剂名称描述方案（如"硅烷官能化方案"、"采用丙烯酸的羧基化改性"）
   - 禁止直接展示样本 ID（如 SSBR-002），必须转换为用户友好的描述
   - 可引用文献来源（期刊名、年份）增加可信度

2. **内容规范**：
   - 基于文献数据回答，禁止编造不存在的数据
   - 明确区分"基于文献数据"和"一般性建议"
   - 保持专业性和准确性

3. **格式规范**：
   - 使用 Markdown 格式
   - 回答长度控制在 400-500 字
   - 结构清晰，分点阐述

4. **输出结构**：
   - 开篇直接回答问题核心
   - 中间展开具体数据和分析
   - 结尾总结关键要点"""

SYSTEM_PROMPT_REFERENCE = """你是一位 SSBR（溶聚丁苯橡胶）官能化改性领域的专家。

你的任务是基于检索到的样本信息提供参考性回答。注意：检索结果相关性中等，请谨慎使用数据。

## 回答规范

1. **重要声明**：
   - 必须在回答开头标注"⚠️ 以下内容仅供参考，检索相关性中等"
   - 建议用户进一步验证关键数据

2. **引用规范**：
   - 使用官能团类型或试剂名称描述方案（如"硅烷官能化方案"、"羧基化改性"）
   - 禁止直接展示样本 ID（如 SSBR-002），必须转换为用户友好的描述
   - 明确标注数据的不确定性

3. **内容规范**：
   - 基于文献数据回答，禁止编造
   - 更多强调一般性知识和建议
   - 回答长度控制在 300-400 字

4. **格式规范**：
   - 使用 Markdown 格式
   - 结构清晰"""

SYSTEM_PROMPT_GUIDANCE = """你是一位 SSBR（溶聚丁苯橡胶）官能化改性领域的专家。

当前检索结果相关性较低（未找到高度匹配的样本），请提供引导性回答。

## 回答规范

1. **重要声明**：
   - 必须在开头说明"当前知识库中未找到高度相关的样本"
   - 不引用任何具体样本数据

2. **内容结构**：
   - **问题分析**：分析用户查询意图，说明知识库覆盖范围
   - **通用建议**：提供 SSBR 官能化的一般性知识（明确标注"基于领域通用知识"）
   - **查询优化提示**：建议用户调整查询关键词

3. **格式规范**：
   - 使用 Markdown 格式
   - 回答长度控制在 200-300 字
   - 禁止编造具体数值或样本信息"""


# =============================================================================
# User Prompt Templates
# =============================================================================

def build_user_prompt_direct(query: str, samples: List[Dict[str, Any]]) -> str:
    """
    Build user prompt for DIRECT answer type.
    
    Args:
        query: User's query
        samples: List of ranked sample dictionaries with keys:
            - sample_id: str
            - content: str (summary.md content)
            - similarity: float
            - quality_score: float
    
    Returns:
        Formatted user prompt string
    """
    samples_text = _format_samples(samples)
    
    return f"""## 用户问题

{query}

## 检索到的相关样本

{samples_text}

## 回答要求

请基于以上样本信息，生成一个专业、准确的回答：
1. 使用官能团名称或试剂名称描述方案（禁止直接展示样本ID）
2. 综合多个样本的信息
3. 回答长度 400-500 字"""


def build_user_prompt_reference(query: str, samples: List[Dict[str, Any]]) -> str:
    """
    Build user prompt for REFERENCE answer type.
    
    Args:
        query: User's query
        samples: List of ranked sample dictionaries
    
    Returns:
        Formatted user prompt string
    """
    samples_text = _format_samples(samples)
    
    return f"""## 用户问题

{query}

## 检索到的参考样本（相关性中等）

{samples_text}

## 回答要求

请基于以上样本信息，生成一个参考性回答：
1. 开头声明"仅供参考"
2. 使用官能团名称描述方案（禁止直接展示样本ID）
3. 谨慎使用具体数据，强调不确定性
4. 回答长度 300-400 字"""


def build_user_prompt_guidance(query: str) -> str:
    """
    Build user prompt for GUIDANCE answer type (no relevant samples).
    
    Args:
        query: User's query
    
    Returns:
        Formatted user prompt string
    """
    return f"""## 用户问题

{query}

## 检索状态

当前知识库中未找到高度相关的样本（最高相似度 < 0.5）。

## 回答要求

请生成一个引导性回答：
1. 分析用户查询意图
2. 提供 SSBR 官能化领域的通用知识（标注为"基于领域通用知识"）
3. 建议用户如何优化查询（如使用关键词：白炭黑分散、滚动阻力、湿地抓地力、Tg 等）
4. 回答长度 200-300 字
5. 禁止编造任何具体样本或数据"""


# =============================================================================
# Helper Functions
# =============================================================================

def _format_samples(samples: List[Dict[str, Any]]) -> str:
    """Format sample list for prompt inclusion."""
    formatted = []
    
    for i, sample in enumerate(samples, 1):
        similarity = sample.get('similarity', 0)
        quality = sample.get('quality_score', 0)
        content = sample.get('content', '')
        
        # 从内容中提取官能团名称
        functional_group = _extract_functional_group(content)
        
        # Truncate content if too long
        max_content_length = 2000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "\n...[内容已截断]"
        
        # 使用官能团名称作为标题，不再显示样本 ID
        formatted.append(f"""### 方案 {i}: {functional_group}

**相关度**: {similarity:.2f} | **数据完整度**: {quality:.0%}

{content}
""")
    
    return "\n---\n".join(formatted)


def _extract_functional_group(content: str) -> str:
    """从样本内容中提取官能团名称。"""
    import re
    
    # 防御 None 输入
    if not content:
        return "官能化方案"
    
    # 尝试从 YAML 或 Markdown 格式中提取
    patterns = [
        r'[-\s]*\*\*核心官能团\*\*:\s*(.+?)(?:\s*[（(]|$|\n)',
        r'官能团[：:]\s*(.+?)(?:\n|$)',
        r'functional[_\s]?group[：:]\s*(.+?)(?:\n|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            fg = match.group(1).strip()
            if fg and fg not in ['-', '无', 'N/A']:
                return f"{fg}官能化"
    
    # 尝试从官能化试剂中推断
    reagent_match = re.search(r'[-\s]*\*\*官能化试剂\*\*:\s*(.+?)(?:\n|$)', content)
    if reagent_match:
        reagent = reagent_match.group(1).strip()
        if reagent and "无" not in reagent:
            # 简化试剂名称
            if "硅烷" in reagent or "silane" in reagent.lower():
                return "硅烷官能化"
            elif "丙烯酸" in reagent or "acrylic" in reagent.lower():
                return "羧基官能化"
            elif "马来酸" in reagent or "maleic" in reagent.lower():
                return "马来酸酐官能化"
            elif "巯基" in reagent or "mercapto" in reagent.lower():
                return "巯基官能化"
            elif "氨基" in reagent or "amino" in reagent.lower():
                return "氨基官能化"
            else:
                return f"{reagent[:10]}官能化"
    
    return "官能化方案"


def get_system_prompt(answer_type: AnswerType) -> str:
    """
    Get system prompt based on answer type.
    
    Args:
        answer_type: The type of answer to generate
    
    Returns:
        Appropriate system prompt string
    """
    prompts = {
        AnswerType.DIRECT: SYSTEM_PROMPT_DIRECT,
        AnswerType.REFERENCE: SYSTEM_PROMPT_REFERENCE,
        AnswerType.GUIDANCE: SYSTEM_PROMPT_GUIDANCE,
    }
    return prompts.get(answer_type, SYSTEM_PROMPT_DIRECT)


def build_user_prompt(
    query: str,
    samples: List[Dict[str, Any]],
    answer_type: AnswerType
) -> str:
    """
    Build user prompt based on answer type.
    
    Args:
        query: User's query
        samples: List of ranked sample dictionaries
        answer_type: The type of answer to generate
    
    Returns:
        Formatted user prompt string
    """
    if answer_type == AnswerType.DIRECT:
        return build_user_prompt_direct(query, samples)
    elif answer_type == AnswerType.REFERENCE:
        return build_user_prompt_reference(query, samples)
    else:  # GUIDANCE
        return build_user_prompt_guidance(query)


# =============================================================================
# Validation
# =============================================================================

def validate_answer_length(answer: str, answer_type: AnswerType) -> bool:
    """
    Validate if answer length is within acceptable range.
    
    Args:
        answer: Generated answer text
        answer_type: The type of answer
    
    Returns:
        True if length is acceptable
    """
    length = len(answer)
    
    ranges = {
        AnswerType.DIRECT: (400, 600),      # Allow some flexibility
        AnswerType.REFERENCE: (300, 500),
        AnswerType.GUIDANCE: (200, 400),
    }
    
    min_len, max_len = ranges.get(answer_type, (200, 600))
    return min_len <= length <= max_len
