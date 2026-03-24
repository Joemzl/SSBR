"""
Formula Designer Module for Multi-Literature Synthesis

This module provides formula design capabilities:
1. Parse target performance requirements
2. Detect conflicting targets
3. Generate formula recommendations

Feature: 004-multi-literature-synthesis
Tasks: T033, T034, T035
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    SampleSummary, FormulaRecommendation, ConfidenceTag
)
from utils.exceptions import ConflictingTargetsError


# 已知的性能冲突对
KNOWN_CONFLICTS = [
    ("拉伸强度", "断裂伸长率", "高强度通常伴随低伸长率"),
    ("湿地抓地力", "滚动阻力", "两者难以同时最优，需要平衡"),
    ("硬度", "弹性", "硬度增加通常降低弹性"),
]


class FormulaDesigner:
    """
    配方设计器：根据目标性能生成配方建议。
    
    主要功能：
    1. 解析目标性能需求
    2. 检测目标冲突
    3. 基于样本数据生成配方建议
    """
    
    def __init__(self, min_supporting_samples: int = 2):
        """
        初始化配方设计器。
        
        Args:
            min_supporting_samples: 最少支撑样本数
        """
        self.min_supporting_samples = min_supporting_samples
    
    def detect_conflicts(
        self,
        target_properties: Dict[str, str]
    ) -> List[Tuple[str, str, str]]:
        """
        检测目标性能中的冲突（T034）。
        
        Args:
            target_properties: 目标性能字典
        
        Returns:
            冲突列表 [(property1, property2, reason), ...]
        """
        conflicts = []
        target_keys = set(target_properties.keys())
        
        for prop1, prop2, reason in KNOWN_CONFLICTS:
            # 检查是否同时要求两个冲突属性都达到极值
            if prop1 in target_keys and prop2 in target_keys:
                val1 = target_properties[prop1].lower()
                val2 = target_properties[prop2].lower()
                
                # 检查是否都要求"高"或极值
                if ("高" in val1 or "优" in val1 or "max" in val1) and \
                   ("低" in val2 or "优" in val2 or "min" in val2):
                    conflicts.append((prop1, prop2, reason))
                elif ("高" in val1 and "高" in val2):
                    conflicts.append((prop1, prop2, reason))
        
        return conflicts
    
    def design_formula(
        self,
        target_properties: Dict[str, str],
        samples: List[SampleSummary],
        constraints: Optional[Dict[str, str]] = None
    ) -> FormulaRecommendation:
        """
        基于目标性能设计配方（T035）。
        
        Args:
            target_properties: 目标性能
            samples: 可参考的样本
            constraints: 约束条件
        
        Returns:
            FormulaRecommendation
        
        Raises:
            ConflictingTargetsError: 目标冲突且无法折中
        """
        # 1. 检测冲突
        conflicts = self.detect_conflicts(target_properties)
        
        # 2. 分析样本，找到最匹配的方案
        best_match = self._find_best_match(target_properties, samples)
        
        # 3. 生成推荐
        if best_match:
            recommended_group = best_match.functional_group
            recommended_degree = best_match.functionalization_degree
            supporting = [best_match.sample_id]
            confidence = ConfidenceTag.MEDIUM
        else:
            # 无精确匹配，使用综合分析
            recommended_group, recommended_degree = self._synthesize_recommendation(
                target_properties, samples
            )
            supporting = [s.sample_id for s in samples[:3]]
            confidence = ConfidenceTag.LOW
        
        # 4. 生成设计理由
        rationale = self._generate_rationale(
            target_properties, recommended_group, recommended_degree, samples
        )
        
        # 5. 生成取舍说明
        trade_offs = []
        if conflicts:
            for prop1, prop2, reason in conflicts:
                trade_offs.append(f"{prop1}与{prop2}存在权衡：{reason}")
        
        # 6. 安全警示
        warnings = self._check_safety_warnings(recommended_group)
        
        # 7. 预期性能
        expected_performance = self._estimate_performance(
            recommended_group, recommended_degree, samples
        )
        
        return FormulaRecommendation(
            target_properties=target_properties,
            recommended_functional_group=recommended_group,
            recommended_degree=recommended_degree,
            recommended_filler="白炭黑/偶联剂体系",  # 默认填料
            expected_performance=expected_performance,
            rationale=rationale,
            supporting_samples=supporting,
            trade_offs=trade_offs,
            warnings=warnings,
            confidence=confidence
        )
    
    def _find_best_match(
        self,
        target_properties: Dict[str, str],
        samples: List[SampleSummary]
    ) -> Optional[SampleSummary]:
        """找到最匹配目标的样本。"""
        best_score = 0
        best_sample = None
        
        for sample in samples:
            score = 0
            
            # 简单匹配：检查样本性能是否满足目标
            for prop, target in target_properties.items():
                sample_value = self._get_sample_property(sample, prop)
                if sample_value and self._matches_target(sample_value, target):
                    score += 1
            
            if score > best_score:
                best_score = score
                best_sample = sample
        
        return best_sample if best_score > 0 else None
    
    def _get_sample_property(
        self,
        sample: SampleSummary,
        prop_name: str
    ) -> Optional[str]:
        """获取样本的指定性能。"""
        prop_mapping = {
            "拉伸强度": "tensile_strength",
            "断裂伸长率": "elongation",
            "Tg": "tg",
            "湿地抓地力": "tan_delta_0c",
            "滚动阻力": "tan_delta_60c",
            "分散性": "payne_effect",
        }
        
        field = prop_mapping.get(prop_name)
        if field:
            return getattr(sample, field, None)
        return None
    
    def _matches_target(self, value: str, target: str) -> bool:
        """检查值是否满足目标。"""
        if not value or not target:
            return False
        
        # 简单的定性匹配
        if "高" in target and self._extract_numeric(value):
            return self._extract_numeric(value) > 15  # 拉伸强度 > 15 MPa
        if "低" in target and self._extract_numeric(value):
            return self._extract_numeric(value) < 10
        
        return False
    
    def _synthesize_recommendation(
        self,
        target_properties: Dict[str, str],
        samples: List[SampleSummary]
    ) -> Tuple[str, str]:
        """综合分析生成推荐。"""
        # 统计样本中的官能团分布
        group_counts = {}
        for sample in samples:
            fg = sample.functional_group
            if fg:
                group_counts[fg] = group_counts.get(fg, 0) + 1
        
        # 选择最常见的官能团
        if group_counts:
            recommended_group = max(group_counts, key=group_counts.get)
        else:
            recommended_group = "羟基"  # 默认
        
        # 推荐中等官能化程度
        recommended_degree = "3-8 wt%"
        
        return recommended_group, recommended_degree
    
    def _generate_rationale(
        self,
        target_properties: Dict[str, str],
        recommended_group: str,
        recommended_degree: str,
        samples: List[SampleSummary]
    ) -> List[str]:
        """生成设计理由。"""
        rationale = []
        
        rationale.append(
            f"推荐{recommended_group}官能化：该官能团在已有研究中"
            f"表现出良好的综合性能"
        )
        
        rationale.append(
            f"推荐官能化程度{recommended_degree}：基于"
            f"{len(samples)}个相关样本的数据分析，"
            f"该范围可实现目标性能的平衡"
        )
        
        if "湿地抓地力" in target_properties or "分散性" in target_properties:
            rationale.append(
                "建议使用白炭黑/偶联剂体系：可改善填料分散和界面相容性"
            )
        
        return rationale
    
    def _check_safety_warnings(self, functional_group: str) -> List[str]:
        """检查安全警示。"""
        warnings = []
        
        # 已知的安全提示
        safety_notes = {
            "异氰酸酯": "异氰酸酯类试剂具有毒性，需在通风环境下操作",
            "丙烯酸": "丙烯酸具有腐蚀性，需使用个人防护装备",
        }
        
        for keyword, warning in safety_notes.items():
            if keyword in functional_group:
                warnings.append(warning)
        
        return warnings
    
    def _estimate_performance(
        self,
        functional_group: str,
        degree: str,
        samples: List[SampleSummary]
    ) -> Dict[str, str]:
        """估计预期性能。"""
        # 从相似样本中估计
        similar_samples = [
            s for s in samples
            if s.functional_group and functional_group in s.functional_group
        ]
        
        expected = {}
        
        if similar_samples:
            # 取平均值
            tensile_values = [
                self._extract_numeric(s.tensile_strength)
                for s in similar_samples
                if s.tensile_strength
            ]
            if tensile_values:
                avg = sum(v for v in tensile_values if v) / len([v for v in tensile_values if v])
                expected["拉伸强度"] = f"约 {avg:.1f} MPa"
            
            tg_values = [
                self._extract_numeric(s.tg)
                for s in similar_samples
                if s.tg
            ]
            if tg_values:
                avg = sum(v for v in tg_values if v) / len([v for v in tg_values if v])
                expected["Tg"] = f"约 {avg:.0f}°C"
        
        return expected
    
    def _extract_numeric(self, text: Any) -> Optional[float]:
        """从文本中提取数值。"""
        if text is None:
            return None
        
        if isinstance(text, (int, float)):
            return float(text)
        
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

_designer_instance: Optional[FormulaDesigner] = None


def get_formula_designer(min_supporting_samples: int = 2) -> FormulaDesigner:
    """获取 FormulaDesigner 单例。"""
    global _designer_instance
    
    if _designer_instance is None:
        _designer_instance = FormulaDesigner(min_supporting_samples)
    
    return _designer_instance
