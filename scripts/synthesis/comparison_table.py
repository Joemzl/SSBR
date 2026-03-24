"""
Comparison Table Generator Module for Multi-Literature Synthesis

This module generates structured comparison tables for different functionalization schemes:
1. Scheme-based sample retrieval (T043)
2. Automatic dimension selection (T044)
3. Missing data handling (T045)
4. Markdown table formatting (T048)

Feature: 004-multi-literature-synthesis
Tasks: T042, T043, T044, T045, T046, T047, T048
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    SampleSummary, ComparisonTable, ComparisonDimension, ComparisonEntry
)


# 标准对比维度定义（按优先级排序）
STANDARD_DIMENSIONS = [
    # 力学性能
    ComparisonDimension("拉伸强度", "MPa", True),
    ComparisonDimension("断裂伸长率", "%", True),
    ComparisonDimension("撕裂强度", "kN/m", True),
    # 热学性能
    ComparisonDimension("Tg", "°C", False),  # Tg 视情况而定
    # 动态性能
    ComparisonDimension("tan δ (0°C)", "-", True),  # 湿地抓地力，越高越好
    ComparisonDimension("tan δ (60°C)", "-", False),  # 滚动阻力，越低越好
    ComparisonDimension("Payne 效应", "-", False),  # 越低分散越好
    # 官能化参数
    ComparisonDimension("官能化程度", "wt%", None),  # 无明确好坏
]


# 字段名到样本属性的映射
FIELD_MAPPING = {
    "拉伸强度": "tensile_strength",
    "断裂伸长率": "elongation",
    "撕裂强度": None,  # 暂无字段
    "Tg": "tg",
    "tan δ (0°C)": "tan_delta_0c",
    "tan δ (60°C)": "tan_delta_60c",
    "Payne 效应": "payne_effect",
    "官能化程度": "functionalization_degree",
}


class ComparisonTableGenerator:
    """
    对比表格生成器。
    
    主要功能：
    1. 按方案聚合样本数据
    2. 自动选择对比维度（5-7 个）
    3. 处理缺失数据
    4. 生成 Markdown 表格
    """
    
    def __init__(self, min_dimensions: int = 5, max_dimensions: int = 7):
        """
        初始化对比表格生成器。
        
        Args:
            min_dimensions: 最少对比维度数
            max_dimensions: 最多对比维度数
        """
        self.min_dimensions = min_dimensions
        self.max_dimensions = max_dimensions
    
    def generate(
        self,
        scheme_names: List[str],
        samples_by_scheme: Dict[str, List[SampleSummary]]
    ) -> ComparisonTable:
        """
        生成对比表格（T042）。
        
        Args:
            scheme_names: 方案名称列表
            samples_by_scheme: 每个方案对应的样本列表
        
        Returns:
            ComparisonTable
        """
        # 1. 选择对比维度（T044）
        dimensions = self._select_dimensions(samples_by_scheme)
        
        # 2. 生成对比条目（T043, T045）
        entries = []
        for scheme_name in scheme_names:
            samples = samples_by_scheme.get(scheme_name, [])
            entry = self._create_entry(scheme_name, samples, dimensions)
            entries.append(entry)
        
        # 3. 生成综合结论
        summary = self._generate_summary(entries, dimensions)
        
        # 4. 生成标题
        title = f"{' vs '.join(scheme_names)} 对比分析"
        
        return ComparisonTable(
            title=title,
            dimensions=dimensions,
            entries=entries,
            summary=summary
        )
    
    def _select_dimensions(
        self,
        samples_by_scheme: Dict[str, List[SampleSummary]]
    ) -> List[ComparisonDimension]:
        """
        自动选择最相关的对比维度（T044）。
        
        选择策略：
        1. 统计每个维度在所有样本中的数据可用率
        2. 按可用率排序，选择可用率最高的维度
        3. 确保至少有 min_dimensions 个，最多 max_dimensions 个
        """
        # 统计各维度的数据可用率
        dimension_coverage = {}
        all_samples = []
        for samples in samples_by_scheme.values():
            all_samples.extend(samples)
        
        total_samples = len(all_samples) if all_samples else 1
        
        for dim in STANDARD_DIMENSIONS:
            field_name = FIELD_MAPPING.get(dim.name)
            if field_name is None:
                continue
            
            # 统计有值的样本数
            count = sum(
                1 for s in all_samples
                if getattr(s, field_name, None) is not None
                and str(getattr(s, field_name, "")).strip() not in ["", "-", "N/A"]
            )
            
            coverage = count / total_samples if total_samples > 0 else 0
            dimension_coverage[dim.name] = (dim, coverage)
        
        # 按覆盖率排序
        sorted_dims = sorted(
            dimension_coverage.items(),
            key=lambda x: x[1][1],
            reverse=True
        )
        
        # 选择覆盖率 > 0 的维度，限制在 min-max 范围内
        selected = []
        for dim_name, (dim, coverage) in sorted_dims:
            if coverage > 0 or len(selected) < self.min_dimensions:
                selected.append(dim)
            if len(selected) >= self.max_dimensions:
                break
        
        # 确保至少有 min_dimensions 个
        if len(selected) < self.min_dimensions:
            for dim in STANDARD_DIMENSIONS:
                if dim not in selected:
                    selected.append(dim)
                if len(selected) >= self.min_dimensions:
                    break
        
        return selected
    
    def _create_entry(
        self,
        scheme_name: str,
        samples: List[SampleSummary],
        dimensions: List[ComparisonDimension]
    ) -> ComparisonEntry:
        """
        创建对比条目（T043, T045）。
        
        对于每个维度：
        - 如有多个样本，取平均值或典型值
        - 如无数据，填 None（显示为"数据不足"）
        """
        sample_ids = [s.sample_id for s in samples]
        values = {}
        
        for dim in dimensions:
            field_name = FIELD_MAPPING.get(dim.name)
            if field_name is None:
                values[dim.name] = None
                continue
            
            # 收集该维度的所有有效值
            dim_values = []
            for sample in samples:
                val = getattr(sample, field_name, None)
                if val is not None and str(val).strip() not in ["", "-", "N/A"]:
                    dim_values.append(val)
            
            if dim_values:
                # 取第一个值（或可以实现取平均）
                values[dim.name] = self._format_value(dim_values[0], dim.unit)
            else:
                values[dim.name] = None
        
        return ComparisonEntry(
            scheme_name=scheme_name,
            sample_ids=sample_ids,
            values=values
        )
    
    def _format_value(self, value: Any, unit: str) -> str:
        """格式化数值。"""
        if value is None:
            return None
        
        # 如果已经是字符串且包含单位，直接返回
        str_val = str(value).strip()
        if unit and unit not in ["-"] and unit not in str_val:
            return f"{str_val} {unit}"
        return str_val
    
    def _generate_summary(
        self,
        entries: List[ComparisonEntry],
        dimensions: List[ComparisonDimension]
    ) -> str:
        """
        生成综合结论。
        
        基于各方案在不同维度的表现，给出简要总结。
        """
        if not entries or not dimensions:
            return "数据不足，无法生成综合评价。"
        
        # 统计各方案的优势维度
        scheme_advantages = {entry.scheme_name: [] for entry in entries}
        
        for dim in dimensions:
            if dim.higher_is_better is None:
                continue
            
            # 提取各方案在该维度的数值
            values_with_scheme = []
            for entry in entries:
                val = entry.values.get(dim.name)
                if val is not None:
                    numeric = self._extract_numeric(val)
                    if numeric is not None:
                        values_with_scheme.append((entry.scheme_name, numeric))
            
            if len(values_with_scheme) < 2:
                continue
            
            # 找出最优方案
            if dim.higher_is_better:
                best = max(values_with_scheme, key=lambda x: x[1])
            else:
                best = min(values_with_scheme, key=lambda x: x[1])
            
            scheme_advantages[best[0]].append(dim.name)
        
        # 生成总结文本
        summary_parts = []
        for scheme_name, advantages in scheme_advantages.items():
            if advantages:
                summary_parts.append(
                    f"{scheme_name}在{'/'.join(advantages[:3])}方面表现更优"
                )
        
        if summary_parts:
            return "；".join(summary_parts) + "。"
        else:
            return "各方案在关键性能上各有优劣，需根据具体应用场景选择。"
    
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

_generator_instance: Optional[ComparisonTableGenerator] = None


def get_comparison_generator(
    min_dimensions: int = 5,
    max_dimensions: int = 7
) -> ComparisonTableGenerator:
    """获取 ComparisonTableGenerator 单例。"""
    global _generator_instance
    
    if _generator_instance is None:
        _generator_instance = ComparisonTableGenerator(min_dimensions, max_dimensions)
    
    return _generator_instance
