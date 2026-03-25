"""
Sample Aggregator Module for Multi-Literature Synthesis

This module provides the SampleAggregator class for extracting structured
sample summaries from summary.md files, enabling efficient multi-sample
synthesis without passing full content to LLM.

Feature: 004-multi-literature-synthesis
Task: T011
"""

import re
import yaml
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import SampleSummary, RankedResult


class SampleAggregator:
    """
    样本聚合器：从 summary.md 提取结构化摘要。
    
    主要功能：
    1. 解析 YAML front matter 提取结构化数据
    2. 提取关键性能指标
    3. 生成 SampleSummary 用于综合分析
    """
    
    # 关键字段映射（YAML key → SampleSummary field）
    FIELD_MAPPINGS = {
        # 官能化信息
        '核心官能团': 'functional_group',
        '官能化程度': 'functionalization_degree',
        '官能化试剂': 'reagent',
        '官能化方法': 'method',
        'functional_group': 'functional_group',
        'functionalization_degree': 'functionalization_degree',
        
        # 力学性能
        '拉伸强度': 'tensile_strength',
        '断裂伸长率': 'elongation',
        'tensile_strength': 'tensile_strength',
        'elongation': 'elongation',
        
        # 热学性能
        'Tg': 'tg',
        '玻璃化转变温度': 'tg',
        'glass_transition': 'tg',
        
        # 动态性能
        'Payne效应': 'payne_effect',
        'payne_effect': 'payne_effect',
        'tan_delta_0': 'tan_delta_0c',
        'tan_delta_60': 'tan_delta_60c',
        
        # 文献来源
        'DOI': 'doi',
        'doi': 'doi',
        '第一作者': 'first_author',
        'first_author': 'first_author',
        '年份': 'year',
        'year': 'year',
    }
    
    def __init__(self, interpretations_dir: Optional[str] = None):
        """
        初始化聚合器。
        
        Args:
            interpretations_dir: 解读文档目录路径
        """
        if interpretations_dir:
            self.interpretations_dir = Path(interpretations_dir)
        else:
            # 默认路径
            self.interpretations_dir = Path(__file__).parent.parent.parent / "dataset" / "interpretations"
    
    def extract_summary(
        self,
        sample_id: str,
        content: str,
        similarity: float = 0.0,
        quality_score: float = 0.0
    ) -> SampleSummary:
        """
        从 summary.md 内容提取结构化摘要。
        
        Args:
            sample_id: 样本 ID
            content: summary.md 内容
            similarity: 相似度分数
            quality_score: 质量分数
        
        Returns:
            SampleSummary 实例
        """
        # 解析 YAML front matter
        yaml_data = self._parse_yaml_front_matter(content)
        
        # 从 Markdown 正文提取补充信息
        markdown_data = self._parse_markdown_content(content)
        
        # 合并数据（YAML 优先）
        merged = {**markdown_data, **yaml_data}
        
        # 构建 SampleSummary
        return SampleSummary(
            sample_id=sample_id,
            functional_group=merged.get('functional_group', '未知官能团'),
            functionalization_degree=merged.get('functionalization_degree', '-'),
            reagent=merged.get('reagent', '-'),
            method=merged.get('method', '-'),
            tensile_strength=merged.get('tensile_strength'),
            elongation=merged.get('elongation'),
            tg=merged.get('tg'),
            payne_effect=merged.get('payne_effect'),
            tan_delta_0c=merged.get('tan_delta_0c'),
            tan_delta_60c=merged.get('tan_delta_60c'),
            doi=merged.get('doi'),
            first_author=merged.get('first_author'),
            year=self._parse_year(merged.get('year')),
            quality_score=quality_score,
            similarity=similarity
        )
    
    def aggregate_from_ranked_results(
        self,
        ranked_results: List[RankedResult],
        top_k: int = 5
    ) -> List[SampleSummary]:
        """
        从重排序结果批量提取样本摘要。
        
        Args:
            ranked_results: 重排序结果列表
            top_k: 最多提取的样本数
        
        Returns:
            SampleSummary 列表
        """
        summaries = []
        
        for result in ranked_results[:top_k]:
            summary = self.extract_summary(
                sample_id=result.sample_id,
                content=result.content,
                similarity=result.similarity,
                quality_score=result.quality_score
            )
            summaries.append(summary)
        
        return summaries
    
    def load_sample_content(self, sample_id: str) -> str:
        """
        加载样本的 summary.md 内容。
        
        Args:
            sample_id: 样本 ID
        
        Returns:
            summary.md 内容
        """
        summary_path = self.interpretations_dir / sample_id / "summary.md"
        
        if summary_path.exists():
            with open(summary_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        return ""
    
    def _parse_yaml_front_matter(self, content: str) -> Dict[str, Any]:
        """解析 YAML front matter，包括嵌套的 functionalization 字段。"""
        if not content:
            return {}
        
        # 匹配 YAML front matter (---...---)
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}
        
        try:
            yaml_content = match.group(1)
            data = yaml.safe_load(yaml_content) or {}
            
            # 映射字段名
            result = {}
            for key, value in data.items():
                mapped_key = self.FIELD_MAPPINGS.get(key, key)
                result[mapped_key] = value
            
            # 特殊处理 functionalization 嵌套对象
            if 'functionalization' in data and isinstance(data['functionalization'], dict):
                func_data = data['functionalization']
                
                # 映射 functionalization 子字段
                func_mappings = {
                    'core_functional_group_name': 'functional_group',
                    'degree': 'functionalization_degree',
                    'reagent': 'reagent',
                    'type': 'method',
                    'grafting_group': 'grafting_group',
                    'core_functional_group_smiles': 'functional_group_smiles',
                    'grafting_group_smiles': 'grafting_group_smiles',
                }
                
                for yaml_key, summary_key in func_mappings.items():
                    if yaml_key in func_data and func_data[yaml_key]:
                        # 不覆盖已有的非空值
                        if summary_key not in result or not result.get(summary_key):
                            result[summary_key] = func_data[yaml_key]
            
            return result
        except yaml.YAMLError:
            return {}
    
    def _parse_markdown_content(self, content: str) -> Dict[str, Any]:
        """从 Markdown 正文提取关键信息。"""
        result = {}
        
        if not content:
            return result
        
        # 提取官能团信息
        patterns = {
            'functional_group': [
                r'\*\*核心官能团\*\*[:：]\s*(.+?)(?:\s*[（(]|$|\n)',
                r'官能团[:：]\s*(.+?)(?:\n|$)',
            ],
            'functionalization_degree': [
                r'\*\*官能化程度\*\*[:：]\s*(.+?)(?:\n|$)',
                r'官能化程度[:：]\s*(.+?)(?:\n|$)',
            ],
            'reagent': [
                r'\*\*官能化试剂\*\*[:：]\s*(.+?)(?:\n|$)',
            ],
            'tensile_strength': [
                r'拉伸强度[:：]\s*(.+?)\s*MPa',
                r'tensile\s*strength[:：]?\s*(\d+\.?\d*)\s*MPa',
            ],
            'tg': [
                r'Tg[:：]\s*(-?\d+\.?\d*)\s*°?C',
                r'玻璃化转变温度[:：]\s*(-?\d+\.?\d*)',
            ],
            'doi': [
                r'DOI[:：]\s*(10\.\d{4,}/[^\s]+)',
                r'\[DOI\]\((10\.\d{4,}/[^\)]+)\)',
            ],
            'first_author': [
                r'第一作者[:：]\s*(.+?)(?:\n|$)',
                r'作者[:：]\s*(.+?)(?:等|et al|,|\n)',
                # 从引文格式提取：- **引文**: Author A, Author B, et al.
                r'\*\*引文\*\*[:：]\s*([A-Z][a-z]+ [A-Z])',
            ],
            'year': [
                # 从引文提取年份：...[J]. Journal, 2022, ...
                r'\*\*引文\*\*.*?,\s*(\d{4}),',
            ],
        }
        
        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    result[field] = match.group(1).strip()
                    break
        
        return result
    
    def _parse_year(self, year_value: Any) -> Optional[int]:
        """解析年份值。"""
        if year_value is None:
            return None
        
        if isinstance(year_value, int):
            return year_value
        
        if isinstance(year_value, str):
            match = re.search(r'(\d{4})', year_value)
            if match:
                return int(match.group(1))
        
        return None
    
    def get_data_ranges(
        self,
        summaries: List[SampleSummary]
    ) -> Dict[str, 'DataRange']:
        """
        从样本摘要中计算数据范围。
        
        Args:
            summaries: 样本摘要列表
        
        Returns:
            字段名到 DataRange 的映射
        """
        from models import DataRange
        
        # 收集数值字段
        numeric_fields = {
            'functionalization_degree': ('wt%', []),
            'tensile_strength': ('MPa', []),
            'tg': ('°C', []),
        }
        
        for summary in summaries:
            # 解析官能化程度
            if summary.functionalization_degree and summary.functionalization_degree != '-':
                value = self._extract_numeric(summary.functionalization_degree)
                if value is not None:
                    numeric_fields['functionalization_degree'][1].append(value)
            
            # 解析拉伸强度
            if summary.tensile_strength:
                value = self._extract_numeric(summary.tensile_strength)
                if value is not None:
                    numeric_fields['tensile_strength'][1].append(value)
            
            # 解析 Tg
            if summary.tg:
                value = self._extract_numeric(summary.tg)
                if value is not None:
                    numeric_fields['tg'][1].append(value)
        
        # 构建 DataRange
        data_ranges = {}
        for field_name, (unit, values) in numeric_fields.items():
            if len(values) >= 2:
                data_ranges[field_name] = DataRange(
                    field_name=field_name,
                    min_value=min(values),
                    max_value=max(values),
                    unit=unit,
                    data_points=len(values)
                )
        
        return data_ranges
    
    def _extract_numeric(self, text: str) -> Optional[float]:
        """从文本中提取数值。"""
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

_aggregator_instance: Optional[SampleAggregator] = None


def get_aggregator(interpretations_dir: Optional[str] = None) -> SampleAggregator:
    """获取 SampleAggregator 单例。"""
    global _aggregator_instance
    
    if _aggregator_instance is None:
        _aggregator_instance = SampleAggregator(interpretations_dir)
    
    return _aggregator_instance


# =============================================================================
# CLI for testing
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sample Aggregator CLI")
    parser.add_argument("--sample", "-s", type=str, help="Sample ID to extract")
    parser.add_argument("--dir", "-d", type=str, help="Interpretations directory")
    
    args = parser.parse_args()
    
    aggregator = SampleAggregator(args.dir) if args.dir else SampleAggregator()
    
    if args.sample:
        content = aggregator.load_sample_content(args.sample)
        if content:
            summary = aggregator.extract_summary(args.sample, content)
            print(f"Sample: {summary.sample_id}")
            print(f"  官能团: {summary.functional_group}")
            print(f"  官能化程度: {summary.functionalization_degree}")
            print(f"  试剂: {summary.reagent}")
            print(f"  拉伸强度: {summary.tensile_strength}")
            print(f"  Tg: {summary.tg}")
            print(f"  DOI: {summary.doi}")
        else:
            print(f"Sample {args.sample} not found")
    else:
        parser.print_help()
