"""
Extrapolator Module for Multi-Literature Synthesis

This module provides conservative extrapolation capabilities:
1. Boundary validation (50% rule)
2. Confidence tag determination
3. Extrapolation result generation

Feature: 004-multi-literature-synthesis
Tasks: T026, T027, T028
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    SampleSummary, DataRange, ExtrapolationResult, ConfidenceTag
)
from utils.exceptions import ExtrapolationBoundaryError


class Extrapolator:
    """
    外推预测器：基于数据趋势进行保守外推。
    
    主要功能：
    1. 验证外推边界（50% 规则）
    2. 生成外推预测
    3. 确定置信度标签
    
    Constitution I-A 合规：
    - 仅允许数据范围外 50% 的外推
    - 必须明确标注"外推估计"
    - 附带置信度和数据支撑点数
    """
    
    def __init__(self, boundary_ratio: float = 0.5):
        """
        初始化外推器。
        
        Args:
            boundary_ratio: 外推边界比例（默认 50%）
        """
        self.boundary_ratio = boundary_ratio
    
    def validate_boundary(
        self,
        query_value: float,
        data_range: DataRange
    ) -> Tuple[bool, Optional[str]]:
        """
        验证查询值是否在允许的外推范围内（T027）。
        
        Args:
            query_value: 查询的自变量值
            data_range: 数据范围
        
        Returns:
            (is_valid, warning_message)
        
        Raises:
            ExtrapolationBoundaryError: 超出允许范围
        """
        if data_range.is_within_data(query_value):
            return True, None
        
        if data_range.is_within_extrapolation(query_value):
            # 在外推范围内，返回警告
            warning = (
                f"此预测超出数据覆盖范围"
                f"（{data_range.min_value:.1f}-{data_range.max_value:.1f} {data_range.unit} "
                f"外推至 {data_range.extrapolation_min:.1f}-{data_range.extrapolation_max:.1f} {data_range.unit}），"
                f"仅供参考"
            )
            return True, warning
        
        # 超出外推边界
        raise ExtrapolationBoundaryError(
            query_value=query_value,
            allowed_range=(data_range.extrapolation_min, data_range.extrapolation_max),
            unit=data_range.unit
        )
    
    def extrapolate(
        self,
        query_value: float,
        query_unit: str,
        samples: List[SampleSummary],
        target_field: str,
        target_unit: str,
        data_range: DataRange
    ) -> ExtrapolationResult:
        """
        执行外推预测。
        
        Args:
            query_value: 查询的自变量值
            query_unit: 查询值单位
            samples: 样本数据
            target_field: 目标字段名
            target_unit: 目标字段单位
            data_range: 数据范围
        
        Returns:
            ExtrapolationResult
        """
        # 1. 验证边界
        is_valid, warning = self.validate_boundary(query_value, data_range)
        
        # 2. 判断是否为外推
        is_extrapolation = not data_range.is_within_data(query_value)
        
        # 3. 提取目标字段数据
        target_values = []
        for sample in samples:
            value = self._extract_numeric(getattr(sample, target_field, None))
            if value is not None:
                target_values.append(value)
        
        if len(target_values) < 2:
            # 数据不足，使用大范围估计
            predicted_min = 0
            predicted_max = 100  # 默认上限
            confidence = ConfidenceTag.LOW
        else:
            # 基于现有数据范围估计
            data_min = min(target_values)
            data_max = max(target_values)
            data_mean = sum(target_values) / len(target_values)
            data_std = (sum((v - data_mean) ** 2 for v in target_values) / len(target_values)) ** 0.5
            
            # 预测范围：均值 ± 标准差
            predicted_min = max(0, data_mean - data_std * 1.5)
            predicted_max = data_mean + data_std * 1.5
            
            # 确定置信度（T028）
            confidence = self._determine_confidence(
                data_points=len(target_values),
                is_extrapolation=is_extrapolation,
                within_range=data_range.is_within_data(query_value)
            )
        
        return ExtrapolationResult(
            query_value=query_value,
            query_unit=query_unit,
            predicted_range=(predicted_min, predicted_max),
            predicted_unit=target_unit,
            confidence=confidence,
            data_points_used=len(target_values),
            is_extrapolation=is_extrapolation,
            boundary_warning=warning
        )
    
    def _determine_confidence(
        self,
        data_points: int,
        is_extrapolation: bool,
        within_range: bool
    ) -> ConfidenceTag:
        """
        确定置信度标签（T028）。
        
        规则：
        - HIGH: 数据点 ≥5，在数据范围内
        - MEDIUM: 数据点 3-4，或在外推区域
        - LOW: 数据点 <3，或接近边界
        """
        if data_points >= 5 and within_range:
            return ConfidenceTag.HIGH
        elif data_points >= 3:
            return ConfidenceTag.MEDIUM
        else:
            return ConfidenceTag.LOW
    
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
    
    def detect_extrapolation_query(
        self,
        query: str
    ) -> Optional[Tuple[float, str, str]]:
        """
        检测查询是否为外推查询，提取查询值。
        
        Args:
            query: 用户查询
        
        Returns:
            (query_value, unit, target_field) 或 None
        """
        # 匹配"X% 官能化程度"模式
        patterns = [
            (r'(\d+\.?\d*)\s*%?\s*官能化程度.*拉伸强度', "tensile_strength"),
            (r'官能化程度.*(\d+\.?\d*)\s*%.*拉伸强度', "tensile_strength"),
            (r'(\d+\.?\d*)\s*wt%.*时.*强度', "tensile_strength"),
            (r'(\d+\.?\d*)\s*%.*官能化.*Tg', "tg"),
        ]
        
        for pattern, target_field in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                try:
                    value = float(match.group(1))
                    return (value, "wt%", target_field)
                except (ValueError, IndexError):
                    continue
        
        return None


# =============================================================================
# Factory Function
# =============================================================================

_extrapolator_instance: Optional[Extrapolator] = None


def get_extrapolator(boundary_ratio: float = 0.5) -> Extrapolator:
    """获取 Extrapolator 单例。"""
    global _extrapolator_instance
    
    if _extrapolator_instance is None:
        _extrapolator_instance = Extrapolator(boundary_ratio)
    
    return _extrapolator_instance
