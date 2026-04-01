"""
Prompt Templates Module for RAG QA System

This module provides prompt templates for generating answers based on
retrieved samples. Templates are designed to ensure:
1. All citations are traceable to sample IDs
2. Clear distinction between literature data and general advice
3. Professional and accurate responses
4. Controlled length (300-500 characters)
"""

from typing import List, Dict, Any, Optional
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

SYSTEM_PROMPT_DIRECT = """你是一位 SSBR（溶聚丁苯橡胶）官能化改性领域的专家。

你的任务是**基于检索到的样本信息**，简洁、直接地回答用户问题。

## 回答规范

### 1. 忠实于上下文
- **回答中的具体数值必须来自样本信息**
- 严禁编造数据
- 当数据充足时，直接引用样本中的具体数值
- 当数据不足时，**可以基于样本数据进行合理推断**，但需标注"根据数据推断"

### 2. 直接回答优先
- **第一句话必须直接回答用户问题的核心**
- 先给出结论或推荐，再补充数据支撑
- 示例：
  - ✅ "硅烷官能化 SSBR 的拉伸强度为 18.2-26.0 MPa，其中羧基官能化（8.7 wt%）的 26.0 MPa 最高。"
  - ❌ "SSBR 是一种重要的合成橡胶，官能化改性可以..."

### 3. 简洁性要求
- 回答长度控制在 **200-350 字**
- 去除冗余的背景介绍
- 优先陈述样本数据中的核心信息

### 4. 当数据不完全匹配时
- **仍然尝试基于已有数据回答**
- 可以说"根据相近官能化程度的样本..."或"根据数据趋势推断..."
- 只有完全无相关数据时才说"知识库中暂无此数据"

### 5. 引用规范
- 使用官能团类型描述方案（如"硅烷官能化"、"羧基官能化"）
- 禁止直接展示样本 ID（如 SSBR-002）"""

SYSTEM_PROMPT_REFERENCE = """你是一位 SSBR（溶聚丁苯橡胶）官能化改性领域的专家。

你的任务是**基于检索到的样本信息**提供参考性回答。注意：检索结果相关性中等，请谨慎使用数据。

## 回答规范

### 1. 忠实于上下文
- **回答中的具体数值必须来自样本信息**
- 严禁编造数据
- 当数据不完全匹配时，**可以基于相似样本进行合理推断**

### 2. 直接回答优先
- 必须在回答**第一句话**直接回答用户的核心问题
- 如果能找到具体数值，直接给出数值
- 然后再补充不确定性声明

### 3. 示例格式
- ✅ "根据检索到的数据，羟基官能化 SSBR 的断裂伸长率为 200%（官能化程度 3.6 wt%）。⚠️ 此数据来自单一样本，实际值可能有差异。"
- ❌ "羟基官能化通常可以改善延展性..."（空泛描述）

### 4. 当数据不完全匹配时
- 仍然尝试基于相近样本回答
- 可以说"根据相近条件的样本推断..."
- 在答案后标注不确定性

### 5. 内容规范
- 回答长度控制在 200-350 字
- 使用官能团类型描述方案（禁止直接展示样本 ID）"""

SYSTEM_PROMPT_GUIDANCE = """你是一位 SSBR（溶聚丁苯橡胶）官能化改性领域的专家。

当前检索结果相关性较低（未找到高度匹配的样本），请尽可能提供有价值的回答。

## 回答规范

1. **尝试直接回答**：
   - 如果检索结果中有任何相关信息，优先尝试回答用户问题
   - 第一句话直接给出你能推断的答案（即使不完全确定）
   - 然后说明数据来源和不确定性

2. **示例格式**：
   - ✅ "根据现有数据，tan δ(0°C) 较高的样本包括羧基官能化类型，典型值在 0.7-0.9 范围。⚠️ 注意：知识库中没有完全匹配的样本..."
   - ❌ "当前知识库中未找到高度相关的样本。用户询问..."

3. **内容结构**：
   - **直接回答**：先尝试回答问题（基于已有数据推断）
   - **不确定性说明**：说明数据覆盖范围的局限
   - **查询优化提示**：简要建议（1句话）

4. **格式规范**：
   - 回答长度控制在 150-250 字
   - 简洁直接，避免过多解释性内容
   - 禁止编造具体数值，但可以给出已知数据的范围"""


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
    """Format sample list for prompt inclusion with structured metadata."""
    formatted = []
    
    for i, sample in enumerate(samples, 1):
        similarity = sample.get('similarity', 0)
        quality = sample.get('quality_score', 0)
        content = sample.get('content', '')
        
        # 优先使用结构化元数据字段（由 SampleAggregator 提取）
        functional_group = sample.get('functional_group')
        reagent = sample.get('reagent')
        degree = sample.get('functionalization_degree')
        doi = sample.get('doi')
        first_author = sample.get('first_author')
        
        # 如果没有结构化数据，则从内容中提取
        if not functional_group or functional_group == '未知官能团':
            functional_group = _extract_functional_group(content)
        else:
            functional_group = f"{functional_group}官能化"
        
        # 格式化试剂和官能化程度
        reagent_str = reagent if reagent and reagent != '-' else '未知'
        degree_str = degree if degree and degree != '-' else 'N/A'
        
        # 格式化来源信息
        source_info = ""
        if doi:
            author_part = f"{first_author} 等人 - " if first_author else ""
            source_info = f"\n\n**数据来源**: {author_part}DOI: {doi}"
        
        # Truncate content if too long
        max_content_length = 1500  # 减少内容长度，因为增加了结构化信息
        if len(content) > max_content_length:
            content = content[:max_content_length] + "\n...[内容已截断]"
        
        # 使用官能团名称作为标题，添加结构化元数据表格
        formatted.append(f"""### 方案 {i}: {functional_group}

**相关度**: {similarity:.2f} | **数据完整度**: {quality:.0%}

| 项目 | 内容 |
|------|------|
| 官能化试剂 | {reagent_str} |
| 官能化程度 | {degree_str} |

{content}{source_info}
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


# =============================================================================
# Synthesis Prompt Templates (004-multi-literature-synthesis)
# =============================================================================

SYNTHESIS_SYSTEM_PROMPT = """你是一位 SSBR（溶聚丁苯橡胶）官能化改性领域的专家。

你的任务是**基于检索到的多个样本数据**，进行综合分析并给出简洁明确的回答。

## 核心原则

### 1. 忠实于上下文
- **回答中的具体数值必须来自样本数据**
- 禁止编造数据
- 当数据充足时，直接引用样本中的具体数值
- 当数据不完全匹配时，**可以基于相似样本进行合理推断**，标注"根据数据推断"

### 2. 直接回答优先
- **第一句话直接回答用户问题的核心**
- 先给出结论或推荐，再补充数据支撑
- 示例：
  - ✅ "羧基官能化（8.7 wt%）的拉伸强度为 26.0 MPa（最高），硅烷官能化（1.7 wt%）为 18.2 MPa。推荐选择羧基官能化以获得最佳力学性能。"
  - ❌ "SSBR 官能化可以通过多种方式改善性能..."

### 3. 零幻觉原则
- 所有具体数值必须来自提供的样本数据
- 禁止编造数据
- 推荐值必须基于样本数据的实际范围

### 4. 当数据不完全匹配时
- **仍然尝试基于已有数据给出有价值的回答**
- 可以说"根据相近条件的样本..."或"根据数据趋势..."
- 只有完全无相关数据时才说"知识库中暂无此数据"

### 5. 引用规范
- 使用"方案 1"、"方案 2"引用样本
- 禁止暴露内部 ID（如 SSBR-002）

### 6. 输出格式（精简版）

```markdown
## 直接回答

[1-2 句话直接回答问题核心，引用具体数值并给出推荐]

## 🎯 推荐方案

| 参数 | 推荐值 | 置信度 |
|------|--------|--------|
| **推荐官能团** | [名称] | 高/中/低 |
| **推荐试剂** | [名称] | 高/中/低 |
| **推荐官能化程度** | [X-Y wt%] | 高/中/低 |
| **预期改善效果** | [基于样本数据] | 高/中/低 |

## 关键数据支撑

- 方案 X：[引用样本数据中的数值]
- 方案 Y：[引用样本数据中的数值]

⚠️ 置信度说明：[简短说明]
```

### 7. 长度控制
- 回答长度：**400-600 字**
- 优先陈述核心数据和推荐
- 去除冗余的背景介绍"""

SYNTHESIS_USER_TEMPLATE = """## 用户问题

{query}

## 检索到的相关样本（共 {sample_count} 个）

{samples_text}

## 数据范围参考

{data_ranges_text}

## 回答要求

请基于以上样本信息，生成**简洁明确的综合性回答**：

1. **第一句话直接回答问题核心**（例如："羧基官能化程度 4-5 wt% 可有效降低 Payne 效应。"）
2. 给出推荐方案表格
3. 列出 2-3 个关键数据点支撑
4. 回答长度 **400-600 字**（不要超过）

**重要：不要从背景介绍开始，直接给出答案！**"""


def build_synthesis_prompt(
    query: str,
    samples: List[Dict[str, Any]],
    data_ranges: Optional[Dict[str, Any]] = None
) -> str:
    """
    构建综合问答的用户 Prompt。
    
    Args:
        query: 用户查询
        samples: 样本列表（包含 SampleSummary 数据）
        data_ranges: 数据范围信息
    
    Returns:
        格式化的用户 Prompt
    """
    # 格式化样本信息
    samples_text = _format_synthesis_samples(samples)
    
    # 格式化数据范围
    data_ranges_text = _format_data_ranges(data_ranges) if data_ranges else "（无定量数据范围）"
    
    return SYNTHESIS_USER_TEMPLATE.format(
        query=query,
        sample_count=len(samples),
        samples_text=samples_text,
        data_ranges_text=data_ranges_text
    )


def _format_synthesis_samples(samples: List[Dict[str, Any]]) -> str:
    """格式化综合分析的样本列表。"""
    formatted = []
    
    for i, sample in enumerate(samples, 1):
        # 提取关键字段
        fg = sample.get('functional_group', '未知官能团')
        degree = sample.get('functionalization_degree', '-')
        reagent = sample.get('reagent', '-')
        
        # 性能指标
        tensile = sample.get('tensile_strength', '-')
        elongation = sample.get('elongation', '-')
        tg = sample.get('tg', '-')
        payne = sample.get('payne_effect', '-')
        
        # 来源信息
        author = sample.get('first_author', '未知')
        year = sample.get('year', '未知')
        similarity = sample.get('similarity', 0)
        quality = sample.get('quality_score', 0)
        
        formatted.append(f"""### 方案 {i}: {fg}官能化

**基本信息**：
- 官能化试剂: {reagent}
- 官能化程度: {degree}
- 相关度: {similarity:.2f} | 数据完整度: {quality:.0%}

**性能指标**：
- 拉伸强度: {tensile}
- 断裂伸长率: {elongation}
- Tg: {tg}
- Payne 效应: {payne}

**文献来源**：{author} 等人 ({year})
""")
    
    return "\n---\n".join(formatted)


def _format_data_ranges(data_ranges: Dict[str, Any]) -> str:
    """格式化数据范围信息。"""
    if not data_ranges:
        return "（无定量数据范围）"
    
    lines = []
    for field_name, range_info in data_ranges.items():
        if isinstance(range_info, dict):
            min_val = range_info.get('min_value', 'N/A')
            max_val = range_info.get('max_value', 'N/A')
            unit = range_info.get('unit', '')
            points = range_info.get('data_points', 0)
            lines.append(f"- {field_name}: {min_val} - {max_val} {unit}（{points} 个数据点）")
    
    return "\n".join(lines) if lines else "（无定量数据范围）"


# =============================================================================
# Trend Analysis Prompts (for Phase 4)
# =============================================================================

TREND_ANALYSIS_SYSTEM_PROMPT = """你是一位数据分析专家，擅长从实验数据中识别趋势和规律。

你的任务是分析 SSBR 官能化样本数据，识别变量之间的关系。

## 分析要求

1. **定性描述趋势**：使用"随 X 增加，Y 呈现...趋势"的表述
2. **不进行数学拟合**：不输出回归方程或 R² 值
3. **标注数据支撑**：说明基于多少个数据点得出结论
4. **识别异常值**：如有偏离趋势的点，说明可能原因"""


# =============================================================================
# Formula Design Prompts (for Phase 5)
# =============================================================================

FORMULA_DESIGN_SYSTEM_PROMPT = """你是一位 SSBR 配方设计专家，擅长根据性能目标设计官能化配方。

你的任务是基于知识库中的样本数据，为用户设计配方建议。

## 设计原则

1. **三要素必备**：官能团类型、官能化程度、填料体系（至少给出两项）
2. **每个选择有理由**：说明为什么推荐该参数
3. **承认不确定性**：如果数据不足，明确说明
4. **指出取舍**：不同性能目标可能存在矛盾，需要说明折中方案

## 输出结构（FR-006, FR-007）

```markdown
## 配方建议

### 推荐方案

- **官能团类型**: [推荐官能团]
- **官能化程度**: [推荐范围，如 3-8 wt%]
- **填料体系**: [推荐填料/偶联剂]

### 设计理由

1. [为什么选择该官能团]
2. [为什么选择该程度范围]
3. [为什么推荐该填料体系]

### 预期性能

| 性能指标 | 预期范围 | 来源支撑 |
|---------|---------|---------|
| 拉伸强度 | X-Y MPa | 基于方案 1/2... |
| ... | ... | ... |

### 性能取舍

⚠️ [冲突性能的权衡说明]

### 注意事项

- [安全/环保/工艺提示]
```

## 规则

1. **数据支撑**：每个推荐必须有样本数据支撑
2. **禁止编造**：无数据时明确标注"数据不足"
3. **冲突提示**：多目标冲突时给出权衡建议（FR-008）
4. **三要素完整率 ≥80%**：至少给出 2 个要素的具体值"""


FORMULA_USER_TEMPLATE = """## 用户需求

{target_description}

## 目标性能

{target_properties_text}

## 参考样本（共 {sample_count} 个）

{samples_text}

## 回答要求

请基于以上样本信息，设计一个满足目标性能的配方建议：

1. 给出官能团类型、官能化程度、填料体系的推荐值
2. 每个推荐附带理由和数据支撑
3. 如有性能冲突，说明取舍建议
4. 回答长度 400-600 字"""


def build_formula_prompt(
    target_description: str,
    target_properties: Dict[str, str],
    samples: List[Dict[str, Any]]
) -> str:
    """
    构建配方设计的用户 Prompt。
    
    Args:
        target_description: 用户的目标描述
        target_properties: 目标性能字典
        samples: 参考样本列表
    
    Returns:
        格式化的用户 Prompt
    """
    # 格式化目标性能
    target_props_lines = [f"- {prop}: {val}" for prop, val in target_properties.items()]
    target_properties_text = "\n".join(target_props_lines) if target_props_lines else "（未明确指定）"
    
    # 格式化样本信息
    samples_text = _format_formula_samples(samples)
    
    return FORMULA_USER_TEMPLATE.format(
        target_description=target_description,
        target_properties_text=target_properties_text,
        sample_count=len(samples),
        samples_text=samples_text
    )


def _format_formula_samples(samples: List[Dict[str, Any]]) -> str:
    """格式化配方设计的参考样本。"""
    formatted = []
    
    for i, sample in enumerate(samples, 1):
        fg = sample.get('functional_group', '未知')
        degree = sample.get('functionalization_degree', '-')
        
        # 性能指标
        tensile = sample.get('tensile_strength', '-')
        elongation = sample.get('elongation', '-')
        tg = sample.get('tg', '-')
        tan_0 = sample.get('tan_delta_0c', '-')
        tan_60 = sample.get('tan_delta_60c', '-')
        payne = sample.get('payne_effect', '-')
        
        formatted.append(f"""### 方案 {i}: {fg}官能化

**配方参数**：
- 官能化程度: {degree}

**性能指标**：
- 拉伸强度: {tensile}
- 断裂伸长率: {elongation}
- Tg: {tg}
- tan δ (0°C): {tan_0}
- tan δ (60°C): {tan_60}
- Payne 效应: {payne}
""")
    
    return "\n---\n".join(formatted)


# =============================================================================
# Comparison Table Prompts (for Phase 6)
# =============================================================================

COMPARISON_SYSTEM_PROMPT = """你是一位材料对比分析专家。

你的任务是生成结构化的官能化方案对比表格。

## 输出格式（FR-009, FR-010）

```markdown
## {方案A} vs {方案B} 对比分析

### 核心指标对比

| 维度 | 方案 A | 方案 B | 优势方 |
|------|--------|--------|-------|
| 拉伸强度 | X MPa | Y MPa | A/B |
| 断裂伸长率 | X% | Y% | A/B |
| ... | ... | ... | ... |

### 综合评价

[2-3 句话总结两种方案的适用场景]
```

## 规则

1. **数据不足标注**：无数据的单元格填写"数据不足"
2. **禁止编造**：所有数值必须来自样本
3. **5-7 个维度**：自动选择最相关的核心维度
4. **优势判定**：根据维度特性判定优势方（higher_is_better）
5. **结尾总结**：用 2-3 句话概括对比结论和适用场景

## 维度选择优先级

1. 力学性能：拉伸强度、断裂伸长率、撕裂强度
2. 热学性能：Tg、DSC 特征峰
3. 动态性能：tan δ (0°C/60°C)、Payne 效应
4. 填料分散：TEM 分散评级
5. 官能化参数：官能化程度"""


COMPARISON_USER_TEMPLATE = """## 对比分析请求

{comparison_description}

## 待对比方案

{schemes_text}

## 方案数据

{samples_text}

## 回答要求

请生成一个结构化的对比表格：

1. 选择 5-7 个最相关的对比维度
2. 填入各方案的具体数值（无数据填"数据不足"）
3. 判定每个维度的优势方
4. 结尾总结两种方案的优缺点和适用场景"""


def build_comparison_prompt(
    comparison_description: str,
    scheme_names: List[str],
    samples_by_scheme: Dict[str, List[Dict[str, Any]]]
) -> str:
    """
    构建对比分析的用户 Prompt。
    
    Args:
        comparison_description: 用户的对比描述
        scheme_names: 方案名称列表
        samples_by_scheme: 每个方案对应的样本列表
    
    Returns:
        格式化的用户 Prompt
    """
    # 格式化方案名称
    schemes_text = "\n".join([f"- {name}" for name in scheme_names])
    
    # 格式化样本数据
    samples_text_parts = []
    for scheme_name, samples in samples_by_scheme.items():
        samples_text_parts.append(f"### {scheme_name}\n")
        samples_text_parts.append(_format_comparison_samples(samples))
    
    samples_text = "\n".join(samples_text_parts)
    
    return COMPARISON_USER_TEMPLATE.format(
        comparison_description=comparison_description,
        schemes_text=schemes_text,
        samples_text=samples_text
    )


def _format_comparison_samples(samples: List[Dict[str, Any]]) -> str:
    """格式化对比分析的样本。"""
    if not samples:
        return "（无相关样本）"
    
    formatted = []
    for sample in samples:
        fg = sample.get('functional_group', '未知')
        degree = sample.get('functionalization_degree', '-')
        tensile = sample.get('tensile_strength', '-')
        elongation = sample.get('elongation', '-')
        tg = sample.get('tg', '-')
        payne = sample.get('payne_effect', '-')
        
        formatted.append(
            f"- {fg}: 程度 {degree}, 拉伸 {tensile}, 伸长率 {elongation}, Tg {tg}, Payne {payne}"
        )
    
    return "\n".join(formatted)
