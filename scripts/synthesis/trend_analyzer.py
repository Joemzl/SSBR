"""
Trend Analyzer Module for Multi-Literature Synthesis

This module provides trend detection and analysis capabilities:
1. Identify variable relationships from multiple samples
2. Generate qualitative trend descriptions
3. Support trend-based queries

Feature: 004-multi-literature-synthesis
Tasks: T024, T025
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    SampleSummary, DataRange, TrendAnalysis, ConfidenceTag
)


class TrendAnalyzer:
    """
    趋势分析器：从多样本数据中识别规律。
    
    主要功能：
    1. 从样本中提取数值对
    2. 识别定性趋势（递增/递减/无明显趋势）
    3. 生成趋势描述
    """
    
    # 支持的变量对
    SUPPORTED_RELATIONSHIPS = [
        ("functionalization_degree", "tensile_strength", "官能化程度", "拉伸强度"),
        ("functionalization_degree", "elongation", "官能化程度", "断裂伸长率"),
        ("functionalization_degree", "tg", "官能化程度", "Tg"),
        ("functionalization_degree", "payne_effect", "官能化程度", "Payne效应"),
    ]
    
    def __init__(self, min_data_points: int = 3):
        """
        初始化趋势分析器。
        
        Args:
            min_data_points: 趋势分析最小数据点数（FR-005）
        """
        self.min_data_points = min_data_points
    
    def analyze_trends(
        self,
        samples: List[SampleSummary],
        target_variable: Optional[str] = None
    ) -> List[TrendAnalysis]:
        """
        分析样本数据中的趋势。
        
        Args:
            samples: 样本摘要列表
            target_variable: 目标因变量（可选，不指定则分析所有）
        
        Returns:
            TrendAnalysis 列表
        """
        trends = []
        
        for x_field, y_field, x_name, y_name in self.SUPPORTED_RELATIONSHIPS:
            if target_variable and y_field != target_variable:
                continue
            
            # 提取数据点
            data_points = self._extract_data_points(samples, x_field, y_field)
            
            if len(data_points) < self.min_data_points:
                continue
            
            # 分析趋势
            trend = self._analyze_relationship(
                data_points, x_name, y_name, x_field, y_field
            )
            
            if trend:
                trends.append(trend)
        
        return trends
    
    def detect_trend_query(self, query: str) -> Optional[Tuple[str, str]]:
        """
        检测查询是否为趋势查询，返回变量对。
        
        Args:
            query: 用户查询
        
        Returns:
            (x_variable, y_variable) 或 None
        """
        # 检测"X 如何影响 Y"模式
        patterns = [
            (r'官能化程度.*影响.*拉伸强度', ("functionalization_degree", "tensile_strength")),
            (r'官能化程度.*影响.*伸长率', ("functionalization_degree", "elongation")),
            (r'官能化程度.*影响.*Tg', ("functionalization_degree", "tg")),
            (r'官能化程度.*和.*关系', ("functionalization_degree", "tensile_strength")),
            (r'官能化程度.*趋势', ("functionalization_degree", "tensile_strength")),
        ]
        
        for pattern, variables in patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return variables
        
        return None
    
    def _extract_data_points(
        self,
        samples: List[SampleSummary],
        x_field: str,
        y_field: str
    ) -> List[Dict[str, Any]]:
        """提取数据点。"""
        data_points = []
        
        for sample in samples:
            x_value = self._extract_numeric(getattr(sample, x_field, None))
            y_value = self._extract_numeric(getattr(sample, y_field, None))
            
            if x_value is not None and y_value is not None:
                data_points.append({
                    "sample_id": sample.sample_id,
                    "x_value": x_value,
                    "y_value": y_value
                })
        
        return data_points
    
    def _analyze_relationship(
        self,
        data_points: List[Dict[str, Any]],
        x_name: str,
        y_name: str,
        x_field: str,
        y_field: str
    ) -> Optional[TrendAnalysis]:
        """分析变量关系。"""
        if len(data_points) < self.min_data_points:
            return None
        
        # 按 X 值排序
        sorted_points = sorted(data_points, key=lambda p: p["x_value"])
        
        # 计算趋势方向
        x_values = [p["x_value"] for p in sorted_points]
        y_values = [p["y_value"] for p in sorted_points]
        
        # 简单线性趋势判断
        trend_direction = self._detect_direction(x_values, y_values)
        
        # 生成描述
        if trend_direction == "increasing":
            description = f"随着{x_name}的增加，{y_name}呈现上升趋势"
        elif trend_direction == "decreasing":
            description = f"随着{x_name}的增加，{y_name}呈现下降趋势"
        else:
            description = f"{x_name}与{y_name}之间未观察到明显的线性趋势"
        
        # 确定置信度
        confidence = self._determine_confidence(len(data_points), trend_direction)
        
        # 构建数据范围
        data_range = DataRange(
            field_name=x_field,
            min_value=min(x_values),
            max_value=max(x_values),
            unit="wt%" if x_field == "functionalization_degree" else "",
            data_points=len(data_points)
        )
        
        return TrendAnalysis(
            variable_x=x_name,
            variable_y=y_name,
            trend_description=description,
            supporting_data=sorted_points,
            data_range=data_range,
            confidence=confidence
        )
    
    def _detect_direction(
        self,
        x_values: List[float],
        y_values: List[float]
    ) -> str:
        """检测趋势方向。"""
        if len(x_values) < 2:
            return "none"
        
        # 计算相邻点的变化
        increases = 0
        decreases = 0
        
        for i in range(1, len(y_values)):
            if y_values[i] > y_values[i-1]:
                increases += 1
            elif y_values[i] < y_values[i-1]:
                decreases += 1
        
        total = increases + decreases
        if total == 0:
            return "none"
        
        # 如果 70% 以上一致方向，认为有趋势
        if increases / total >= 0.7:
            return "increasing"
        elif decreases / total >= 0.7:
            return "decreasing"
        else:
            return "none"
    
    def _determine_confidence(
        self,
        data_points: int,
        trend_direction: str
    ) -> ConfidenceTag:
        """确定置信度标签。"""
        if trend_direction == "none":
            return ConfidenceTag.LOW
        
        if data_points >= 5:
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


# =============================================================================
# Factory Function
# =============================================================================

_analyzer_instance: Optional[TrendAnalyzer] = None


def get_trend_analyzer(min_data_points: int = 3) -> TrendAnalyzer:
    """获取 TrendAnalyzer 单例。"""
    global _analyzer_instance
    
    if _analyzer_instance is None:
        _analyzer_instance = TrendAnalyzer(min_data_points)
    
    return _analyzer_instance
