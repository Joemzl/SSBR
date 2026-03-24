"""
Citation Validator Module for Multi-Literature Synthesis

This module provides citation verification and format conversion:
1. Validate citations against source samples
2. Convert internal references to natural language citations
3. Ensure FR-013 compliance (no internal IDs exposed)

Feature: 004-multi-literature-synthesis
Task: T012
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Citation, SampleSummary


@dataclass
class ValidatedCitation:
    """验证后的引用信息。"""
    citation_id: int                    # 引用编号 [1], [2], ...
    sample_id: str                      # 内部样本 ID（不暴露给用户）
    inline_ref: str                     # 行内引用格式 "Zhang 等人 [1]"
    full_ref: str                       # 完整引用格式
    doi: Optional[str] = None
    is_valid: bool = True
    error_message: Optional[str] = None


class CitationValidator:
    """
    引用验证器：确保所有引用可追溯且格式正确。
    
    主要功能：
    1. 验证 LLM 输出中的引用是否指向有效样本
    2. 将内部编号转换为自然语言引用格式
    3. 生成参考文献列表
    """
    
    def __init__(self):
        """初始化验证器。"""
        self._sample_registry: Dict[str, SampleSummary] = {}
        self._citation_counter = 0
    
    def register_samples(self, samples: List[SampleSummary]) -> Dict[int, str]:
        """
        注册样本并分配引用编号。
        
        Args:
            samples: 样本摘要列表
        
        Returns:
            编号到样本ID的映射 {1: "SSBR-002", 2: "SSBR-005", ...}
        """
        self._sample_registry.clear()
        self._citation_counter = 0
        
        number_to_id = {}
        
        for sample in samples:
            self._citation_counter += 1
            self._sample_registry[sample.sample_id] = sample
            number_to_id[self._citation_counter] = sample.sample_id
        
        return number_to_id
    
    def create_sample_reference_map(
        self,
        samples: List[SampleSummary]
    ) -> Dict[str, str]:
        """
        创建样本 ID 到自然语言引用的映射。
        
        用于 Prompt 中告诉 LLM 如何引用样本。
        
        Args:
            samples: 样本摘要列表
        
        Returns:
            {"方案 1": "羟基官能化（Zhang 等人, 2023）", ...}
        """
        ref_map = {}
        
        for i, sample in enumerate(samples, 1):
            author = sample.first_author or "未知作者"
            year = sample.year or "未知年份"
            fg = sample.functional_group or "官能化"
            
            # 构建自然语言引用
            ref_map[f"方案 {i}"] = f"{fg}（{author} 等人, {year}）"
        
        return ref_map
    
    def validate_and_convert(
        self,
        answer_text: str,
        samples: List[SampleSummary]
    ) -> Tuple[str, List[ValidatedCitation]]:
        """
        验证并转换回答中的引用。
        
        将 LLM 使用的"方案 1"、"方案 2"等转换为自然语言引用。
        
        Args:
            answer_text: LLM 生成的回答文本
            samples: 源样本列表
        
        Returns:
            (转换后的文本, 验证后的引用列表)
        """
        self.register_samples(samples)
        
        validated_citations = []
        converted_text = answer_text
        
        # 匹配"方案 X"模式
        pattern = r'方案\s*(\d+)'
        matches = list(re.finditer(pattern, answer_text))
        
        # 从后向前替换，避免位置偏移
        for match in reversed(matches):
            scheme_num = int(match.group(1))
            
            if scheme_num <= len(samples):
                sample = samples[scheme_num - 1]
                
                # 生成自然语言引用
                inline_ref = self._generate_inline_ref(sample, scheme_num)
                full_ref = self._generate_full_ref(sample, scheme_num)
                
                validated_citations.insert(0, ValidatedCitation(
                    citation_id=scheme_num,
                    sample_id=sample.sample_id,
                    inline_ref=inline_ref,
                    full_ref=full_ref,
                    doi=sample.doi,
                    is_valid=True
                ))
                
                # 替换文本
                converted_text = (
                    converted_text[:match.start()] +
                    inline_ref +
                    converted_text[match.end():]
                )
            else:
                # 无效引用
                validated_citations.insert(0, ValidatedCitation(
                    citation_id=scheme_num,
                    sample_id="",
                    inline_ref=f"[无效引用 {scheme_num}]",
                    full_ref="",
                    is_valid=False,
                    error_message=f"方案 {scheme_num} 超出范围（共 {len(samples)} 个样本）"
                ))
        
        return converted_text, validated_citations
    
    def generate_reference_list(
        self,
        citations: List[ValidatedCitation]
    ) -> str:
        """
        生成参考文献列表。
        
        Args:
            citations: 验证后的引用列表
        
        Returns:
            Markdown 格式的参考文献列表
        """
        if not citations:
            return ""
        
        lines = ["## 文献来源", ""]
        
        for citation in citations:
            if citation.is_valid:
                lines.append(f"{citation.citation_id}. {citation.full_ref}")
        
        return "\n".join(lines)
    
    def extract_citations_to_models(
        self,
        citations: List[ValidatedCitation]
    ) -> List[Citation]:
        """
        将验证后的引用转换为 Citation 模型。
        
        Args:
            citations: 验证后的引用列表
        
        Returns:
            Citation 模型列表
        """
        result = []
        
        for vc in citations:
            if vc.is_valid:
                result.append(Citation(
                    sample_id=vc.sample_id,
                    data_type="综合分析",
                    doi=vc.doi,
                    citation_text=vc.full_ref
                ))
        
        return result
    
    def _generate_inline_ref(
        self,
        sample: SampleSummary,
        citation_num: int
    ) -> str:
        """生成行内引用格式。"""
        author = sample.first_author or "研究者"
        fg = sample.functional_group or "该方案"
        
        # 格式："{官能团}（{作者} 等人 [{编号}]）"
        return f"{fg}（{author} 等人 [{citation_num}]）"
    
    def _generate_full_ref(
        self,
        sample: SampleSummary,
        citation_num: int
    ) -> str:
        """生成完整引用格式。"""
        parts = []
        
        # 作者
        author = sample.first_author or "未知作者"
        parts.append(f"{author} 等人")
        
        # 年份
        if sample.year:
            parts.append(f"({sample.year})")
        
        # 官能团
        if sample.functional_group:
            parts.append(f"- {sample.functional_group}")
        
        # 官能化程度
        if sample.functionalization_degree and sample.functionalization_degree != '-':
            parts.append(f"({sample.functionalization_degree})")
        
        # DOI
        if sample.doi:
            parts.append(f"DOI: {sample.doi}")
        
        return " ".join(parts)
    
    def check_zero_hallucination(
        self,
        answer_text: str,
        samples: List[SampleSummary]
    ) -> List[str]:
        """
        检查回答是否存在幻觉（FR-011 零幻觉原则）。
        
        检测规则：
        1. 数值必须能在样本中找到来源
        2. 引用编号必须有效
        
        Args:
            answer_text: 回答文本
            samples: 源样本列表
        
        Returns:
            潜在幻觉警告列表
        """
        warnings = []
        
        # 提取回答中的数值
        numeric_pattern = r'(\d+\.?\d*)\s*(MPa|%|°C|wt%)'
        matches = re.findall(numeric_pattern, answer_text)
        
        # 构建样本中的已知数值集合
        known_values = set()
        for sample in samples:
            if sample.tensile_strength:
                known_values.add(self._normalize_value(sample.tensile_strength))
            if sample.functionalization_degree:
                known_values.add(self._normalize_value(sample.functionalization_degree))
            if sample.tg:
                known_values.add(self._normalize_value(sample.tg))
        
        # 检查每个数值是否有来源
        for value, unit in matches:
            normalized = self._normalize_value(value)
            if normalized and normalized not in known_values:
                # 允许一定的近似匹配
                if not any(abs(normalized - kv) < 0.5 for kv in known_values if kv):
                    warnings.append(f"数值 {value} {unit} 可能缺少文献来源")
        
        return warnings
    
    def _normalize_value(self, text: str) -> Optional[float]:
        """标准化数值。"""
        if not text:
            return None
        
        match = re.search(r'(-?\d+\.?\d*)', str(text))
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        
        return None


# =============================================================================
# Factory Function
# =============================================================================

_validator_instance: Optional[CitationValidator] = None


def get_citation_validator() -> CitationValidator:
    """获取 CitationValidator 单例。"""
    global _validator_instance
    
    if _validator_instance is None:
        _validator_instance = CitationValidator()
    
    return _validator_instance


# =============================================================================
# CLI for testing
# =============================================================================

if __name__ == "__main__":
    # 测试示例
    from models import SampleSummary
    
    # 创建测试样本
    samples = [
        SampleSummary(
            sample_id="SSBR-002",
            functional_group="羟基",
            functionalization_degree="3.6 wt%",
            reagent="硅烷偶联剂",
            method="溶液法",
            tensile_strength="18.5 MPa",
            tg="-28°C",
            doi="10.1016/j.polymer.2023.001",
            first_author="Zhang",
            year=2023
        ),
        SampleSummary(
            sample_id="SSBR-005",
            functional_group="氨基",
            functionalization_degree="5.2 wt%",
            reagent="氨基硅烷",
            method="乳液法",
            tensile_strength="16.2 MPa",
            tg="-25°C",
            doi="10.1039/c9py00234k",
            first_author="Li",
            year=2024
        ),
    ]
    
    validator = CitationValidator()
    
    # 测试引用转换
    test_text = """
    根据方案 1，羟基官能化的拉伸强度可达 18.5 MPa。
    而方案 2 采用氨基官能化，强度为 16.2 MPa。
    综合来看，方案 1 在力学性能上更优。
    """
    
    converted, citations = validator.validate_and_convert(test_text, samples)
    
    print("原文:")
    print(test_text)
    print("\n转换后:")
    print(converted)
    print("\n参考文献:")
    print(validator.generate_reference_list(citations))
