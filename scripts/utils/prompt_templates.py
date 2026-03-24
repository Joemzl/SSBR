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


# =============================================================================
# Synthesis Prompt Templates (004-multi-literature-synthesis)
# =============================================================================

SYNTHESIS_SYSTEM_PROMPT = """你是一位 SSBR（溶聚丁苯橡胶）官能化改性领域的资深专家，拥有丰富的多文献综合分析经验。

你的任务是基于用户提供的**多个样本信息**，进行**综合分析**，生成整合性的专业回答。

## 核心原则

### 1. 零幻觉原则（Constitution I-A）
- **文献原始数据**：直接引用样本中的数值，标注来源
- **分析结论**：基于多样本数据推导，无需特殊标注
- **外推预测**：必须明确标注"⚠️ **外推估计**"，附带置信度

### 2. 综合分析要求
- 综合 3-5 个样本的数据和结论
- 识别共性规律和差异点
- 提供比单一样本更全面的见解

### 3. 引用规范
- 使用"方案 1"、"方案 2"等编号引用样本
- 禁止暴露内部 ID（如 SSBR-002）
- 引用将在后处理中转换为自然语言格式

### 4. 输出结构（FR-014 分层结构）
```markdown
## 结论摘要

[2-3 句话核心结论]

## 详细分析

### [要点 1]

[分析内容]

**数据支撑**：根据方案 X...

### [要点 2]

...

---

⚠️ [置信度说明/外推警告（如有）]
```

## 回答规范

1. **长度控制**：600-800 字
2. **使用 Markdown 格式**
3. **每个数据点必须标注来源**
4. **禁止编造任何数据**
5. **有分歧时展示多方观点**"""

SYNTHESIS_USER_TEMPLATE = """## 用户问题

{query}

## 检索到的相关样本（共 {sample_count} 个）

{samples_text}

## 数据范围参考

{data_ranges_text}

## 回答要求

请基于以上样本信息，生成一个**综合性**回答：

1. 综合多个样本的数据和结论（不是简单罗列）
2. 识别共性规律和差异点
3. 每个数据点标注来源（使用"方案 X"格式）
4. 采用分层结构：结论摘要 → 详细分析 → 置信度说明
5. 回答长度 600-800 字"""


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
