#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RAGAS 评测结果可视化脚本

用于生成科研论文级别的可视化图表，全面展示 RAG 系统的评测性能。

生成图表包括：
1. 雷达图 (Radar Chart) - 多维度性能总览
2. 柱状图 (Bar Chart) - 各指标得分对比
3. 分组柱状图 - 按查询类型的性能分布
4. 响应时间分析图 - 系统延迟分布
5. 热力图 (Heatmap) - 各样本各指标得分矩阵
6. 综合仪表盘 (Dashboard) - 组合多图的完整报告

输出格式：高分辨率 PNG (300 DPI) + PDF (矢量图)

使用方法：
    python evaluation/visualize_ragas.py
    python evaluation/visualize_ragas.py --input evaluation/ragas_reports/synthesis_report.csv
    python evaluation/visualize_ragas.py --output-dir figures/
    python evaluation/visualize_ragas.py --format pdf  # 仅输出 PDF
    python evaluation/visualize_ragas.py --format png  # 仅输出 PNG
    python evaluation/visualize_ragas.py --dpi 600     # 高分辨率输出

作者: SSBR Research Team
日期: 2026-03-26
"""

import argparse
import csv
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

# 设置 matplotlib 后端和中文字体
import matplotlib
matplotlib.use('Agg')  # 非交互式后端，避免 GUI 问题

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path as MplPath
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

# ============================================================================
# 全局配置：科研论文风格设置
# ============================================================================

def setup_matplotlib_style():
    """配置 matplotlib 为科研论文风格"""
    
    # 尝试使用系统中文字体
    chinese_fonts = [
        'SimHei',           # 黑体 (Windows)
        'Microsoft YaHei',  # 微软雅黑 (Windows)
        'SimSun',           # 宋体 (Windows)
        'STSong',           # 华文宋体 (macOS)
        'PingFang SC',      # 苹方 (macOS)
        'WenQuanYi Micro Hei',  # 文泉驿 (Linux)
        'Noto Sans CJK SC',     # Google Noto (跨平台)
        'DejaVu Sans',      # Fallback
    ]
    
    # 检测可用字体
    available_font = None
    for font in chinese_fonts:
        try:
            from matplotlib.font_manager import FontProperties
            fp = FontProperties(family=font)
            if fp.get_name() != font:
                continue
            available_font = font
            break
        except:
            continue
    
    if available_font is None:
        available_font = 'DejaVu Sans'
        print(f"警告: 未找到中文字体，使用 {available_font}（中文可能显示异常）")
    
    # 科研论文配置
    rcParams.update({
        # 字体设置 - 英文使用 Times New Roman，中文使用可用字体
        'font.family': ['Times New Roman', available_font, 'DejaVu Sans'],
        'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'font.sans-serif': [available_font, 'DejaVu Sans', 'Arial'],
        'font.size': 10,
        'mathtext.fontset': 'stix',  # 数学字体使用 STIX (类似 Times)
        
        # 坐标轴
        'axes.titlesize': 12,
        'axes.titleweight': 'bold',
        'axes.labelsize': 10,
        'axes.linewidth': 1.2,
        'axes.spines.top': True,
        'axes.spines.right': True,
        'axes.unicode_minus': False,  # 解决负号显示问题
        
        # 刻度
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'xtick.major.width': 1.0,
        'ytick.major.width': 1.0,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        
        # 图例
        'legend.fontsize': 9,
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.edgecolor': '0.8',
        
        # 线条
        'lines.linewidth': 1.5,
        'lines.markersize': 6,
        
        # 图像
        'figure.figsize': (8, 6),
        'figure.dpi': 100,
        'figure.facecolor': 'white',
        'figure.edgecolor': 'white',
        'figure.autolayout': False,
        
        # 保存
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
        'savefig.facecolor': 'white',
        'savefig.edgecolor': 'white',
    })
    
    return available_font


# ============================================================================
# 数据模型
# ============================================================================

@dataclass
class EvaluationResult:
    """单个评测结果"""
    question: str
    mode: str
    sample_count: int
    response_time_ms: int
    faithfulness: Optional[float]
    answer_relevancy: Optional[float]
    context_precision: Optional[float]
    context_recall: Optional[float]
    citation_accuracy: Optional[float]
    recommendation_completeness: Optional[float]


@dataclass
class EvaluationReport:
    """完整评测报告"""
    results: List[EvaluationResult]
    timestamp: str
    mode: str
    
    @property
    def avg_faithfulness(self) -> float:
        values = [r.faithfulness for r in self.results if r.faithfulness is not None]
        return np.mean(values) if values else 0.0
    
    @property
    def avg_answer_relevancy(self) -> float:
        values = [r.answer_relevancy for r in self.results if r.answer_relevancy is not None]
        return np.mean(values) if values else 0.0
    
    @property
    def avg_context_precision(self) -> float:
        values = [r.context_precision for r in self.results if r.context_precision is not None]
        return np.mean(values) if values else 0.0
    
    @property
    def avg_context_recall(self) -> float:
        values = [r.context_recall for r in self.results if r.context_recall is not None]
        return np.mean(values) if values else 0.0
    
    @property
    def avg_citation_accuracy(self) -> float:
        values = [r.citation_accuracy for r in self.results if r.citation_accuracy is not None]
        return np.mean(values) if values else 0.0
    
    @property
    def avg_recommendation_completeness(self) -> float:
        values = [r.recommendation_completeness for r in self.results if r.recommendation_completeness is not None]
        return np.mean(values) if values else 0.0
    
    @property
    def avg_response_time(self) -> float:
        return np.mean([r.response_time_ms for r in self.results])
    
    @property
    def std_response_time(self) -> float:
        return np.std([r.response_time_ms for r in self.results])


# ============================================================================
# 数据加载
# ============================================================================

def load_csv_report(csv_path: str) -> EvaluationReport:
    """从 CSV 文件加载评测报告"""
    results = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = EvaluationResult(
                question=row.get('question', ''),
                mode=row.get('mode', 'synthesis'),
                sample_count=int(row.get('sample_count', 0)),
                response_time_ms=int(row.get('response_time_ms', 0)),
                faithfulness=_parse_float(row.get('faithfulness')),
                answer_relevancy=_parse_float(row.get('answer_relevancy')),
                context_precision=_parse_float(row.get('context_precision')),
                context_recall=_parse_float(row.get('context_recall')),
                citation_accuracy=_parse_float(row.get('citation_accuracy')),
                recommendation_completeness=_parse_float(row.get('recommendation_completeness')),
            )
            results.append(result)
    
    return EvaluationReport(
        results=results,
        timestamp=datetime.now().isoformat(),
        mode='synthesis'
    )


def _parse_float(value: Optional[str]) -> Optional[float]:
    """安全解析浮点数"""
    if value is None or value == '' or value == 'N/A':
        return None
    try:
        return float(value)
    except ValueError:
        return None


# ============================================================================
# 颜色方案
# ============================================================================

class ColorScheme:
    """科研论文配色方案"""
    
    # 主色调 (Nature/Science 风格)
    PRIMARY = '#2E86AB'      # 蓝色
    SECONDARY = '#A23B72'    # 紫红色
    ACCENT = '#F18F01'       # 橙色
    SUCCESS = '#4CAF50'      # 绿色
    WARNING = '#FF9800'      # 警告色
    DANGER = '#F44336'       # 红色
    
    # 渐变色板 (用于多数据系列)
    PALETTE = [
        '#2E86AB',  # 蓝
        '#A23B72',  # 紫红
        '#F18F01',  # 橙
        '#4CAF50',  # 绿
        '#9C27B0',  # 紫
        '#00BCD4',  # 青
    ]
    
    # 灰度
    GRAY_DARK = '#333333'
    GRAY_MEDIUM = '#666666'
    GRAY_LIGHT = '#999999'
    GRAY_LIGHTER = '#CCCCCC'
    GRAY_LIGHTEST = '#F5F5F5'
    
    # 热力图配色
    HEATMAP_CMAP = 'RdYlGn'  # 红-黄-绿 (性能从低到高)
    
    @classmethod
    def get_performance_color(cls, score: float) -> str:
        """根据得分返回颜色"""
        if score >= 0.8:
            return cls.SUCCESS
        elif score >= 0.6:
            return cls.WARNING
        else:
            return cls.DANGER


# ============================================================================
# 雷达图 (Radar Chart)
# ============================================================================

def radar_factory(num_vars, frame='polygon'):
    """创建雷达图投影"""
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
    
    class RadarTransform(PolarAxes.PolarTransform):
        def transform_non_affine(self, tr):
            if tr.shape == (2,):
                return np.column_stack([tr])
            return np.column_stack([tr[:, 0], tr[:, 1]])
    
    class RadarAxes(PolarAxes):
        name = 'radar'
        PolarTransform = RadarTransform
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')
            self.set_theta_direction(-1)
        
        def fill(self, *args, closed=True, **kwargs):
            return super().fill(*args, closed=closed, **kwargs)
        
        def plot(self, *args, **kwargs):
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)
            return lines
        
        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)
        
        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)
        
        def _gen_axes_patch(self):
            if frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars, radius=0.5, 
                                      edgecolor='k', facecolor='none')
            else:
                return Circle((0.5, 0.5), 0.5)
        
        def _gen_axes_spines(self):
            if frame == 'polygon':
                spine = Spine(self, 'circle', MplPath.unit_regular_polygon(num_vars))
                spine.set_transform(Affine2D().scale(0.5).translate(0.5, 0.5) + self.transAxes)
                return {'polar': spine}
            else:
                return super()._gen_axes_spines()
    
    register_projection(RadarAxes)
    return theta


def plot_radar_chart(report: EvaluationReport, output_path: str, dpi: int = 300):
    """
    绘制雷达图 - 多维度性能总览
    
    展示所有评测指标的综合得分，直观呈现系统优势和不足。
    """
    # 准备数据
    labels = [
        'Faithfulness\n(忠实度)',
        'Answer Relevancy\n(回答相关性)',
        'Context Precision\n(上下文精度)',
        'Citation Accuracy\n(引用准确性)',
        'Recommendation\nCompleteness\n(推荐完整性)',
    ]
    
    values = [
        report.avg_faithfulness,
        report.avg_answer_relevancy,
        report.avg_context_precision,
        report.avg_citation_accuracy,
        report.avg_recommendation_completeness,
    ]
    
    num_vars = len(labels)
    
    # 角度
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values_plot = values + values[:1]  # 闭合
    angles += angles[:1]
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # 设置角度起始位置和方向
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # 绘制网格
    ax.set_rlabel_position(0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], color=ColorScheme.GRAY_MEDIUM, size=8)
    ax.set_ylim(0, 1.0)
    
    # 设置标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=10, fontweight='bold')
    
    # 绘制数据区域
    ax.plot(angles, values_plot, 'o-', linewidth=2.5, color=ColorScheme.PRIMARY, 
            label='RAGAS Score', markersize=8)
    ax.fill(angles, values_plot, alpha=0.25, color=ColorScheme.PRIMARY)
    
    # 添加数值标注
    for angle, value, label in zip(angles[:-1], values, labels):
        # 计算标注位置
        x = angle
        y = value + 0.08
        if y > 1.0:
            y = value - 0.12
        
        ax.annotate(f'{value:.2f}', xy=(x, y), ha='center', va='center',
                   fontsize=10, fontweight='bold', color=ColorScheme.GRAY_DARK)
    
    # 添加标题
    plt.title('RAGAS 评测指标雷达图\n(Multi-dimensional Performance Overview)', 
              size=14, fontweight='bold', pad=20, y=1.08)
    
    # 保存
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ 雷达图已保存: {output_path}")


# ============================================================================
# 柱状图 (Bar Chart)
# ============================================================================

def plot_metrics_bar_chart(report: EvaluationReport, output_path: str, dpi: int = 300):
    """
    绘制柱状图 - 各指标得分对比
    
    清晰展示各个评测指标的具体数值，便于量化比较。
    """
    # 准备数据
    metrics = {
        'Faithfulness': report.avg_faithfulness,
        'Answer\nRelevancy': report.avg_answer_relevancy,
        'Context\nPrecision': report.avg_context_precision,
        'Citation\nAccuracy': report.avg_citation_accuracy,
        'Recommendation\nCompleteness': report.avg_recommendation_completeness,
    }
    
    labels = list(metrics.keys())
    values = list(metrics.values())
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 设置条形颜色 (根据得分)
    colors = [ColorScheme.get_performance_color(v) for v in values]
    
    # 绘制柱状图
    bars = ax.bar(labels, values, color=colors, edgecolor='white', linewidth=1.5, width=0.6)
    
    # 添加数值标注
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.annotate(f'{value:.3f}',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 5),
                   textcoords='offset points',
                   ha='center', va='bottom',
                   fontsize=11, fontweight='bold',
                   color=ColorScheme.GRAY_DARK)
    
    # 添加基准线
    ax.axhline(y=0.8, color=ColorScheme.SUCCESS, linestyle='--', linewidth=1.5, 
               alpha=0.7, label='优秀阈值 (0.8)')
    ax.axhline(y=0.6, color=ColorScheme.WARNING, linestyle='--', linewidth=1.5, 
               alpha=0.7, label='合格阈值 (0.6)')
    
    # 设置坐标轴
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    
    # 添加网格
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # 设置标题
    ax.set_title('RAGAS 评测指标得分\n(RAGAS Metrics Scores)', 
                fontsize=14, fontweight='bold', pad=15)
    
    # 添加图例
    ax.legend(loc='upper right', framealpha=0.9)
    
    # 移除顶部和右侧边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 保存
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ 柱状图已保存: {output_path}")


# ============================================================================
# 分组柱状图 - 按查询展示
# ============================================================================

def plot_query_comparison(report: EvaluationReport, output_path: str, dpi: int = 300):
    """
    绘制分组柱状图 - 各查询的性能对比
    
    展示不同查询问题在各指标上的表现差异。
    """
    # 准备数据
    n_queries = len(report.results)
    
    # 简化查询标签
    query_labels = []
    for i, r in enumerate(report.results, 1):
        # 截取问题前15个字符
        short_q = r.question[:15] + '...' if len(r.question) > 15 else r.question
        query_labels.append(f'Q{i}')
    
    # 指标数据
    metrics_data = {
        'Faithfulness': [r.faithfulness or 0 for r in report.results],
        'Context Precision': [r.context_precision or 0 for r in report.results],
        'Citation Accuracy': [r.citation_accuracy or 0 for r in report.results],
        'Recommendation': [r.recommendation_completeness or 0 for r in report.results],
    }
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(n_queries)
    width = 0.2
    multiplier = 0
    
    # 绘制每个指标的柱状图
    for i, (metric, values) in enumerate(metrics_data.items()):
        offset = width * multiplier
        bars = ax.bar(x + offset, values, width, label=metric, 
                     color=ColorScheme.PALETTE[i], edgecolor='white', linewidth=0.5)
        multiplier += 1
    
    # 设置坐标轴
    ax.set_xlabel('Query', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(query_labels)
    ax.set_ylim(0, 1.15)
    
    # 添加基准线
    ax.axhline(y=1.0, color=ColorScheme.GRAY_LIGHTER, linestyle='-', linewidth=1)
    
    # 添加网格
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # 设置标题
    ax.set_title('各查询问题的评测指标对比\n(Performance Comparison Across Queries)', 
                fontsize=14, fontweight='bold', pad=15)
    
    # 添加图例
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=4, framealpha=0.9)
    
    # 移除顶部和右侧边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 添加查询问题注释
    # 在图下方添加问题列表
    questions_text = '\n'.join([f'Q{i+1}: {r.question[:40]}...' 
                                for i, r in enumerate(report.results)])
    fig.text(0.02, -0.08, questions_text, fontsize=8, 
             color=ColorScheme.GRAY_MEDIUM, va='top', ha='left',
             transform=ax.transAxes)
    
    # 保存
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ 分组柱状图已保存: {output_path}")


# ============================================================================
# 响应时间分析图
# ============================================================================

def plot_response_time_analysis(report: EvaluationReport, output_path: str, dpi: int = 300):
    """
    绘制响应时间分析图
    
    包含：柱状图 + 平均线 + 目标线
    """
    # 准备数据
    n_queries = len(report.results)
    query_labels = [f'Q{i+1}' for i in range(n_queries)]
    response_times = [r.response_time_ms / 1000.0 for r in report.results]  # 转换为秒
    avg_time = np.mean(response_times)
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制柱状图
    colors = [ColorScheme.SUCCESS if t <= 10 else 
              (ColorScheme.WARNING if t <= 15 else ColorScheme.DANGER) 
              for t in response_times]
    
    bars = ax.bar(query_labels, response_times, color=colors, 
                 edgecolor='white', linewidth=1.5, width=0.6)
    
    # 添加数值标注
    for bar, time in zip(bars, response_times):
        height = bar.get_height()
        ax.annotate(f'{time:.1f}s',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 5),
                   textcoords='offset points',
                   ha='center', va='bottom',
                   fontsize=10, fontweight='bold',
                   color=ColorScheme.GRAY_DARK)
    
    # 添加平均线
    ax.axhline(y=avg_time, color=ColorScheme.PRIMARY, linestyle='-', linewidth=2,
               label=f'平均响应时间: {avg_time:.1f}s')
    
    # 添加目标线 (8秒)
    ax.axhline(y=8, color=ColorScheme.SUCCESS, linestyle='--', linewidth=1.5,
               alpha=0.7, label='目标阈值: 8s')
    
    # 设置坐标轴
    ax.set_xlabel('Query', fontsize=12, fontweight='bold')
    ax.set_ylabel('Response Time (seconds)', fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(response_times) * 1.2)
    
    # 添加网格
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # 设置标题
    ax.set_title('系统响应时间分析\n(System Response Time Analysis)', 
                fontsize=14, fontweight='bold', pad=15)
    
    # 添加图例
    ax.legend(loc='upper right', framealpha=0.9)
    
    # 移除顶部和右侧边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # 添加统计信息文本框
    stats_text = (f'样本数: {n_queries}\n'
                  f'平均时间: {avg_time:.1f}s\n'
                  f'标准差: {np.std(response_times):.1f}s\n'
                  f'最小值: {min(response_times):.1f}s\n'
                  f'最大值: {max(response_times):.1f}s')
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor=ColorScheme.GRAY_LIGHTER)
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=props)
    
    # 保存
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ 响应时间图已保存: {output_path}")


# ============================================================================
# 热力图 (Heatmap)
# ============================================================================

def plot_heatmap(report: EvaluationReport, output_path: str, dpi: int = 300):
    """
    绘制热力图 - 各样本各指标得分矩阵
    
    直观展示每个查询在各指标上的得分分布。
    """
    # 准备数据
    metrics = ['Faithfulness', 'Answer\nRelevancy', 'Context\nPrecision', 
               'Citation\nAccuracy', 'Recommendation\nCompleteness']
    
    n_queries = len(report.results)
    query_labels = [f'Q{i+1}' for i in range(n_queries)]
    
    # 构建数据矩阵
    data = np.zeros((n_queries, len(metrics)))
    for i, r in enumerate(report.results):
        data[i, 0] = r.faithfulness or 0
        data[i, 1] = r.answer_relevancy or 0
        data[i, 2] = r.context_precision or 0
        data[i, 3] = r.citation_accuracy or 0
        data[i, 4] = r.recommendation_completeness or 0
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 绘制热力图
    im = ax.imshow(data, cmap=ColorScheme.HEATMAP_CMAP, aspect='auto', 
                   vmin=0, vmax=1)
    
    # 设置坐标轴
    ax.set_xticks(np.arange(len(metrics)))
    ax.set_yticks(np.arange(n_queries))
    ax.set_xticklabels(metrics, fontsize=10)
    ax.set_yticklabels(query_labels, fontsize=10)
    
    # 旋转 x 轴标签
    plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
    
    # 添加数值标注
    for i in range(n_queries):
        for j in range(len(metrics)):
            value = data[i, j]
            # 根据背景色选择文字颜色
            text_color = 'white' if value < 0.5 else 'black'
            text = ax.text(j, i, f'{value:.2f}',
                          ha='center', va='center', color=text_color,
                          fontsize=10, fontweight='bold')
    
    # 添加颜色条
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.set_ylabel('Score', rotation=-90, va='bottom', fontsize=11, fontweight='bold')
    
    # 设置标题
    ax.set_title('RAGAS 评测指标热力图\n(Evaluation Metrics Heatmap)', 
                fontsize=14, fontweight='bold', pad=15)
    
    # 添加边框
    for edge, spine in ax.spines.items():
        spine.set_visible(True)
        spine.set_linewidth(1.5)
    
    # 保存
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ 热力图已保存: {output_path}")


# ============================================================================
# 综合仪表盘 (Dashboard)
# ============================================================================

def plot_dashboard(report: EvaluationReport, output_path: str, dpi: int = 300):
    """
    绘制综合仪表盘 - 组合多图的完整报告
    
    包含：雷达图 + 柱状图 + 响应时间 + 热力图
    """
    # 创建图形
    fig = plt.figure(figsize=(16, 12))
    
    # 定义网格布局
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.25,
                          left=0.05, right=0.95, top=0.92, bottom=0.08)
    
    # ========== 子图1: 雷达图 (左上) ==========
    ax1 = fig.add_subplot(gs[0, 0], polar=True)
    
    labels = ['Faithfulness', 'Answer\nRelevancy', 'Context\nPrecision', 
              'Citation\nAccuracy', 'Recommendation']
    values = [
        report.avg_faithfulness,
        report.avg_answer_relevancy,
        report.avg_context_precision,
        report.avg_citation_accuracy,
        report.avg_recommendation_completeness,
    ]
    
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values_plot = values + values[:1]
    angles += angles[:1]
    
    ax1.set_theta_offset(np.pi / 2)
    ax1.set_theta_direction(-1)
    ax1.set_rlabel_position(0)
    ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax1.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], color=ColorScheme.GRAY_MEDIUM, size=7)
    ax1.set_ylim(0, 1.0)
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(labels, size=8, fontweight='bold')
    
    ax1.plot(angles, values_plot, 'o-', linewidth=2, color=ColorScheme.PRIMARY, markersize=6)
    ax1.fill(angles, values_plot, alpha=0.25, color=ColorScheme.PRIMARY)
    ax1.set_title('(a) 性能雷达图', size=11, fontweight='bold', pad=10)
    
    # ========== 子图2: 柱状图 (右上) ==========
    ax2 = fig.add_subplot(gs[0, 1])
    
    metrics = {
        'Faith.': report.avg_faithfulness,
        'Relev.': report.avg_answer_relevancy,
        'Prec.': report.avg_context_precision,
        'Citat.': report.avg_citation_accuracy,
        'Recom.': report.avg_recommendation_completeness,
    }
    
    labels2 = list(metrics.keys())
    values2 = list(metrics.values())
    colors2 = [ColorScheme.get_performance_color(v) for v in values2]
    
    bars2 = ax2.bar(labels2, values2, color=colors2, edgecolor='white', linewidth=1, width=0.6)
    
    for bar, value in zip(bars2, values2):
        height = bar.get_height()
        ax2.annotate(f'{value:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',
                    fontsize=9, fontweight='bold')
    
    ax2.axhline(y=0.8, color=ColorScheme.SUCCESS, linestyle='--', linewidth=1, alpha=0.7)
    ax2.set_ylim(0, 1.15)
    ax2.set_ylabel('Score', fontsize=10, fontweight='bold')
    ax2.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax2.set_axisbelow(True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_title('(b) 指标得分柱状图', size=11, fontweight='bold', pad=10)
    
    # ========== 子图3: 响应时间 (左下) ==========
    ax3 = fig.add_subplot(gs[1, 0])
    
    n_queries = len(report.results)
    query_labels = [f'Q{i+1}' for i in range(n_queries)]
    response_times = [r.response_time_ms / 1000.0 for r in report.results]
    avg_time = np.mean(response_times)
    
    colors3 = [ColorScheme.SUCCESS if t <= 10 else 
               (ColorScheme.WARNING if t <= 15 else ColorScheme.DANGER) 
               for t in response_times]
    
    bars3 = ax3.bar(query_labels, response_times, color=colors3, 
                   edgecolor='white', linewidth=1, width=0.6)
    
    for bar, time in zip(bars3, response_times):
        height = bar.get_height()
        ax3.annotate(f'{time:.1f}s', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',
                    fontsize=9, fontweight='bold')
    
    ax3.axhline(y=avg_time, color=ColorScheme.PRIMARY, linestyle='-', linewidth=1.5,
               label=f'平均: {avg_time:.1f}s')
    ax3.axhline(y=8, color=ColorScheme.SUCCESS, linestyle='--', linewidth=1, alpha=0.7,
               label='目标: 8s')
    
    ax3.set_xlabel('Query', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Time (s)', fontsize=10, fontweight='bold')
    ax3.set_ylim(0, max(response_times) * 1.2)
    ax3.legend(loc='upper right', fontsize=8)
    ax3.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax3.set_axisbelow(True)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.set_title('(c) 响应时间分析', size=11, fontweight='bold', pad=10)
    
    # ========== 子图4: 热力图 (右下) ==========
    ax4 = fig.add_subplot(gs[1, 1])
    
    metrics_heatmap = ['Faith.', 'Relev.', 'Prec.', 'Citat.', 'Recom.']
    
    data = np.zeros((n_queries, len(metrics_heatmap)))
    for i, r in enumerate(report.results):
        data[i, 0] = r.faithfulness or 0
        data[i, 1] = r.answer_relevancy or 0
        data[i, 2] = r.context_precision or 0
        data[i, 3] = r.citation_accuracy or 0
        data[i, 4] = r.recommendation_completeness or 0
    
    im = ax4.imshow(data, cmap=ColorScheme.HEATMAP_CMAP, aspect='auto', vmin=0, vmax=1)
    
    ax4.set_xticks(np.arange(len(metrics_heatmap)))
    ax4.set_yticks(np.arange(n_queries))
    ax4.set_xticklabels(metrics_heatmap, fontsize=9)
    ax4.set_yticklabels(query_labels, fontsize=9)
    
    for i in range(n_queries):
        for j in range(len(metrics_heatmap)):
            value = data[i, j]
            text_color = 'white' if value < 0.5 else 'black'
            ax4.text(j, i, f'{value:.2f}', ha='center', va='center', 
                    color=text_color, fontsize=9, fontweight='bold')
    
    cbar = ax4.figure.colorbar(im, ax=ax4, shrink=0.8)
    cbar.ax.set_ylabel('Score', rotation=-90, va='bottom', fontsize=9)
    ax4.set_title('(d) 指标热力图', size=11, fontweight='bold', pad=10)
    
    # ========== 添加总标题 ==========
    fig.suptitle('RAGAS 评测综合仪表盘\n(RAGAS Evaluation Dashboard)', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # ========== 添加底部说明 ==========
    summary_text = (
        f"评测模式: {report.mode.upper()} | "
        f"测试样本: {n_queries} 个 | "
        f"平均响应时间: {avg_time:.1f}s | "
        f"综合得分: {np.mean([v for v in values if v > 0]):.2f}"
    )
    fig.text(0.5, 0.02, summary_text, ha='center', va='bottom', 
             fontsize=10, color=ColorScheme.GRAY_MEDIUM)
    
    # 保存
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ 综合仪表盘已保存: {output_path}")


# ============================================================================
# 论文级指标汇总表
# ============================================================================

def plot_summary_table(report: EvaluationReport, output_path: str, dpi: int = 300):
    """
    绘制论文级指标汇总表
    
    清晰展示各项指标的统计数据，便于直接用于论文表格。
    """
    # 准备数据
    metrics_data = [
        ('Faithfulness', '忠实度', 
         [r.faithfulness for r in report.results if r.faithfulness is not None]),
        ('Answer Relevancy', '回答相关性', 
         [r.answer_relevancy for r in report.results if r.answer_relevancy is not None]),
        ('Context Precision', '上下文精度', 
         [r.context_precision for r in report.results if r.context_precision is not None]),
        ('Citation Accuracy', '引用准确性', 
         [r.citation_accuracy for r in report.results if r.citation_accuracy is not None]),
        ('Recommendation Completeness', '推荐完整性', 
         [r.recommendation_completeness for r in report.results if r.recommendation_completeness is not None]),
    ]
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis('off')
    
    # 表格数据
    table_data = [
        ['指标 (Metric)', '中文名', '均值 (Mean)', '标准差 (Std)', '最小值 (Min)', '最大值 (Max)', '评级']
    ]
    
    for eng_name, cn_name, values in metrics_data:
        if values:
            mean_val = np.mean(values)
            std_val = np.std(values)
            min_val = np.min(values)
            max_val = np.max(values)
            
            # 评级
            if mean_val >= 0.8:
                rating = '★★★ 优秀'
            elif mean_val >= 0.6:
                rating = '★★☆ 良好'
            elif mean_val >= 0.4:
                rating = '★☆☆ 一般'
            else:
                rating = '☆☆☆ 待改进'
            
            table_data.append([
                eng_name, cn_name, 
                f'{mean_val:.3f}', f'{std_val:.3f}', 
                f'{min_val:.3f}', f'{max_val:.3f}',
                rating
            ])
        else:
            table_data.append([eng_name, cn_name, 'N/A', 'N/A', 'N/A', 'N/A', '-'])
    
    # 添加响应时间行
    response_times = [r.response_time_ms for r in report.results]
    table_data.append([
        'Response Time', '响应时间',
        f'{np.mean(response_times):.0f} ms',
        f'{np.std(response_times):.0f} ms',
        f'{np.min(response_times):.0f} ms',
        f'{np.max(response_times):.0f} ms',
        '★★☆ 良好' if np.mean(response_times) <= 10000 else '★☆☆ 一般'
    ])
    
    # 绘制表格
    table = ax.table(
        cellText=table_data[1:],
        colLabels=table_data[0],
        cellLoc='center',
        loc='center',
        colWidths=[0.22, 0.12, 0.11, 0.11, 0.11, 0.11, 0.12]
    )
    
    # 设置表格样式
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)
    
    # 设置表头样式
    for j in range(len(table_data[0])):
        cell = table[(0, j)]
        cell.set_facecolor(ColorScheme.PRIMARY)
        cell.set_text_props(color='white', fontweight='bold')
    
    # 设置数据行样式 (交替背景色)
    for i in range(1, len(table_data)):
        for j in range(len(table_data[0])):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor(ColorScheme.GRAY_LIGHTEST)
            else:
                cell.set_facecolor('white')
    
    # 设置标题
    ax.set_title('RAGAS 评测指标汇总表\n(RAGAS Evaluation Metrics Summary)', 
                fontsize=14, fontweight='bold', pad=20, y=0.95)
    
    # 保存
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"  ✓ 汇总表已保存: {output_path}")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    # Windows 终端编码兼容
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(
        description='RAGAS 评测结果可视化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python visualize_ragas.py
  python visualize_ragas.py --input ragas_reports/synthesis_report.csv
  python visualize_ragas.py --output-dir figures/ --dpi 600
  python visualize_ragas.py --format pdf
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        default='evaluation/ragas_reports/synthesis_report.csv',
        help='输入 CSV 文件路径 (默认: evaluation/ragas_reports/synthesis_report.csv)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default='evaluation/figures',
        help='输出目录 (默认: evaluation/figures)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['png', 'pdf', 'both'],
        default='both',
        help='输出格式 (默认: both)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='输出分辨率 (默认: 300)'
    )
    
    args = parser.parse_args()
    
    # 确定项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 处理输入路径
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = project_root / args.input
    
    # 处理输出目录
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = project_root / args.output_dir
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("RAGAS 评测结果可视化工具")
    print("=" * 60)
    print(f"输入文件: {input_path}")
    print(f"输出目录: {output_dir}")
    print(f"输出格式: {args.format}")
    print(f"分辨率: {args.dpi} DPI")
    print("=" * 60)
    
    # 检查输入文件
    if not input_path.exists():
        print(f"\n❌ 错误: 找不到输入文件 '{input_path}'")
        print("请先运行 RAGAS 评测生成 CSV 报告:")
        print("  python scripts/evaluation/ragas_evaluator.py --mode synthesis --export both")
        sys.exit(1)
    
    # 配置 matplotlib 样式
    print("\n[1/2] 配置绘图样式...")
    font_used = setup_matplotlib_style()
    print(f"  ✓ 使用字体: {font_used}")
    
    # 加载数据
    print("\n[2/2] 加载评测数据...")
    report = load_csv_report(str(input_path))
    print(f"  ✓ 加载 {len(report.results)} 条评测记录")
    
    # 生成图表
    print("\n[3/7] 生成雷达图...")
    formats = ['png', 'pdf'] if args.format == 'both' else [args.format]
    
    for fmt in formats:
        plot_radar_chart(report, str(output_dir / f'ragas_radar.{fmt}'), args.dpi)
    
    print("\n[4/7] 生成柱状图...")
    for fmt in formats:
        plot_metrics_bar_chart(report, str(output_dir / f'ragas_bar.{fmt}'), args.dpi)
    
    print("\n[5/7] 生成分组对比图...")
    for fmt in formats:
        plot_query_comparison(report, str(output_dir / f'ragas_comparison.{fmt}'), args.dpi)
    
    print("\n[6/7] 生成响应时间图...")
    for fmt in formats:
        plot_response_time_analysis(report, str(output_dir / f'ragas_response_time.{fmt}'), args.dpi)
    
    print("\n[7/7] 生成热力图...")
    for fmt in formats:
        plot_heatmap(report, str(output_dir / f'ragas_heatmap.{fmt}'), args.dpi)
    
    print("\n[Bonus] 生成综合仪表盘...")
    for fmt in formats:
        plot_dashboard(report, str(output_dir / f'ragas_dashboard.{fmt}'), args.dpi)
    
    print("\n[Bonus] 生成汇总表...")
    for fmt in formats:
        plot_summary_table(report, str(output_dir / f'ragas_summary_table.{fmt}'), args.dpi)
    
    # 输出总结
    print("\n" + "=" * 60)
    print("✅ 可视化完成！")
    print("=" * 60)
    print(f"\n生成的图表文件:")
    for f in sorted(output_dir.glob('ragas_*.*')):
        print(f"  - {f.name}")
    
    print(f"\n📁 输出目录: {output_dir}")
    print("\n💡 建议:")
    print("  - ragas_dashboard 适合组会汇报和论文正文")
    print("  - ragas_summary_table 适合作为论文表格")
    print("  - 其他单图适合作为补充材料或附录")
    print("  - PDF 格式为矢量图，适合论文投稿")
    print("  - PNG 格式适合 PPT 和网页展示")


if __name__ == '__main__':
    main()
