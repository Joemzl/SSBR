"""
论文图表生成脚本
生成毕业论文所需的数据可视化图表
- 图 3-4: 外推置信度衰减曲线
- 图 4-2: 重排序前后精度对比柱状图

风格: 学术论文风格
英文字体: Times New Roman
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pathlib import Path

# ============ 全局样式设置 ============
# 设置字体
plt.rcParams['font.family'] = ['Times New Roman', 'SimHei']  # 英文用 Times New Roman，中文用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['mathtext.fontset'] = 'stix'  # 数学公式字体

# 学术论文风格
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.figsize'] = (8, 6)

# 颜色方案 (学术风格)
COLORS = {
    'primary': '#2E5090',      # 深蓝
    'secondary': '#C44E52',    # 红色
    'tertiary': '#4C72B0',     # 蓝色
    'quaternary': '#55A868',   # 绿色
    'gray': '#8C8C8C',         # 灰色
    'light_blue': '#CCE5FF',   # 浅蓝
    'light_red': '#FFCCCC',    # 浅红
}

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / 'docs' / 'paper-2.0' / 'figures'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_figure_3_4():
    """
    图 3-4: 外推置信度衰减曲线 (CEBC 机制)
    
    展示置信度随外推距离的衰减规律:
    - 数据范围内: 置信度 = 基础置信度
    - 外推 0-50%: 置信度线性衰减
    - 超出 50%: 拒绝外推
    """
    fig, ax = plt.subplots(figsize=(9, 6))
    
    # 数据定义
    # x 轴: 相对于数据边界的位置 (-100% 到 +100%)
    # 数据范围: -100% 到 0%
    # 外推区域: 0% 到 50%
    # 拒绝区域: 50% 以上
    
    x_data = np.linspace(-100, 0, 100)      # 数据范围内
    x_extrapolate = np.linspace(0, 50, 50)  # 允许外推区域
    x_reject = np.linspace(50, 100, 50)     # 拒绝外推区域
    
    # 置信度计算
    base_confidence = 0.85  # 基础置信度 (L2 级别)
    
    # 数据范围内: 恒定置信度
    y_data = np.full_like(x_data, base_confidence)
    
    # 外推区域: 线性衰减 (从 0.85 衰减到 0.5)
    y_extrapolate = base_confidence - (x_extrapolate / 50) * (base_confidence - 0.50)
    
    # 拒绝区域: 置信度为 0 (不提供外推)
    y_reject = np.full_like(x_reject, 0.0)
    
    # 绘制曲线
    ax.plot(x_data, y_data, color=COLORS['primary'], linewidth=2.5, 
            label='Data range (interpolation)')
    ax.plot(x_extrapolate, y_extrapolate, color=COLORS['secondary'], linewidth=2.5,
            label='Extrapolation zone (0-50%)', linestyle='--')
    ax.plot(x_reject, y_reject, color=COLORS['gray'], linewidth=2.5,
            label='Rejection zone (>50%)', linestyle=':')
    
    # 填充区域
    ax.fill_between(x_data, 0, y_data, alpha=0.15, color=COLORS['primary'])
    ax.fill_between(x_extrapolate, 0, y_extrapolate, alpha=0.15, color=COLORS['secondary'])
    ax.axvspan(50, 100, alpha=0.1, color=COLORS['gray'], hatch='///')
    
    # 关键点标注
    ax.scatter([0], [base_confidence], color=COLORS['primary'], s=100, zorder=5, 
               edgecolors='white', linewidths=2)
    ax.scatter([50], [0.50], color=COLORS['secondary'], s=100, zorder=5,
               edgecolors='white', linewidths=2)
    
    # 添加标注文字
    ax.annotate('Data boundary\n(confidence = 0.85)', 
                xy=(0, base_confidence), xytext=(15, 0.92),
                fontsize=10, ha='left',
                arrowprops=dict(arrowstyle='->', color='black', lw=1))
    
    ax.annotate('50% extrapolation limit\n(confidence = 0.50)', 
                xy=(50, 0.50), xytext=(55, 0.62),
                fontsize=10, ha='left',
                arrowprops=dict(arrowstyle='->', color='black', lw=1))
    
    ax.annotate('Extrapolation rejected\n(insufficient data)', 
                xy=(75, 0.05), xytext=(75, 0.25),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=1))
    
    # 公式标注
    formula_box = r'$C_{extrap} = C_{base} \times \left(1 - \frac{d}{d_{max}}\right)$'
    ax.text(0.02, 0.02, formula_box, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='white', 
            edgecolor='gray', alpha=0.9))
    
    # 垂直分界线
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1.5, alpha=0.7)
    ax.axvline(x=50, color='black', linestyle='--', linewidth=1.2, alpha=0.5)
    
    # 设置坐标轴
    ax.set_xlim(-100, 100)
    ax.set_ylim(0, 1.0)
    ax.set_xlabel('Distance from data boundary (%)', fontsize=12, fontweight='normal')
    ax.set_ylabel('Confidence level', fontsize=12, fontweight='normal')
    ax.set_title('Figure 3-4: Confidence decay curve for extrapolation (CEBC mechanism)', 
                 fontsize=13, fontweight='bold', pad=15)
    
    # 添加区域标签
    ax.text(-50, 0.05, 'DATA RANGE', fontsize=11, ha='center', color=COLORS['primary'],
            fontweight='bold', alpha=0.7)
    ax.text(25, 0.05, 'EXTRAPOLATION\nZONE', fontsize=10, ha='center', color=COLORS['secondary'],
            fontweight='bold', alpha=0.7)
    ax.text(75, 0.40, 'REJECTION\nZONE', fontsize=10, ha='center', color=COLORS['gray'],
            fontweight='bold', alpha=0.7)
    
    # 图例
    ax.legend(loc='upper right', frameon=True, framealpha=0.95, edgecolor='gray')
    
    # 网格
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # 保存
    plt.tight_layout()
    output_path = OUTPUT_DIR / 'figure_3_4_confidence_decay.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    output_path_pdf = OUTPUT_DIR / 'figure_3_4_confidence_decay.pdf'
    plt.savefig(output_path_pdf, bbox_inches='tight', facecolor='white')
    
    print(f"[OK] Figure 3-4 saved: {output_path}")
    print(f"[OK] Figure 3-4 saved: {output_path_pdf}")
    
    plt.close()


def generate_figure_4_2():
    """
    图 4-2: 重排序前后精度对比柱状图
    
    展示交叉编码器重排序对检索精度的提升效果
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 数据定义 (基于实际系统性能)
    metrics = ['P@3', 'P@5', 'P@10', 'MRR', 'Hit Rate@5']
    
    # 重排序前 (仅向量检索)
    before_rerank = [0.72, 0.68, 0.61, 0.75, 0.83]
    
    # 重排序后 (向量检索 + 交叉编码器)
    after_rerank = [0.89, 0.85, 0.78, 0.91, 0.917]
    
    # 提升幅度
    improvement = [(a - b) / b * 100 for a, b in zip(after_rerank, before_rerank)]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    # 绘制柱状图
    bars1 = ax.bar(x - width/2, before_rerank, width, label='Before re-ranking (vector retrieval only)',
                   color=COLORS['light_blue'], edgecolor=COLORS['primary'], linewidth=1.5)
    bars2 = ax.bar(x + width/2, after_rerank, width, label='After re-ranking (+ cross-encoder)',
                   color=COLORS['primary'], edgecolor='white', linewidth=1)
    
    # 添加数值标签
    def add_labels(bars, values, offset=0.02):
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.annotate(f'{val:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    add_labels(bars1, before_rerank)
    add_labels(bars2, after_rerank)
    
    # 添加提升幅度标注
    for i, (imp, x_pos) in enumerate(zip(improvement, x)):
        ax.annotate(f'+{imp:.1f}%',
                    xy=(x_pos + width/2, after_rerank[i] + 0.06),
                    ha='center', va='bottom',
                    fontsize=9, color=COLORS['quaternary'], fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#E8F5E9', 
                             edgecolor=COLORS['quaternary'], alpha=0.8))
    
    # 设置坐标轴
    ax.set_ylim(0, 1.15)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_xlabel('Evaluation metrics', fontsize=12)
    ax.set_title('Figure 4-2: Impact of cross-encoder re-ranking on retrieval precision', 
                 fontsize=13, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11)
    
    # 添加基准线
    ax.axhline(y=0.8, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(len(metrics) - 0.5, 0.81, 'Target: 0.80', fontsize=9, color='gray', ha='right')
    
    # 图例
    ax.legend(loc='upper left', frameon=True, framealpha=0.95, edgecolor='gray')
    
    # 网格
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # 添加统计信息框
    avg_improvement = np.mean(improvement)
    stats_text = f'Average improvement: +{avg_improvement:.1f}%\nRe-ranker: bge-reranker-base'
    ax.text(0.98, 0.02, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='gray', alpha=0.9))
    
    # 保存
    plt.tight_layout()
    output_path = OUTPUT_DIR / 'figure_4_2_rerank_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    output_path_pdf = OUTPUT_DIR / 'figure_4_2_rerank_comparison.pdf'
    plt.savefig(output_path_pdf, bbox_inches='tight', facecolor='white')
    
    print(f"[OK] Figure 4-2 saved: {output_path}")
    print(f"[OK] Figure 4-2 saved: {output_path_pdf}")
    
    plt.close()


def main():
    """生成所有论文图表"""
    print("=" * 50)
    print("论文图表生成脚本")
    print("=" * 50)
    print(f"输出目录: {OUTPUT_DIR}")
    print()
    
    # 检查字体
    print("Checking fonts...")
    available_fonts = [f.name for f in mpl.font_manager.fontManager.ttflist]
    if 'Times New Roman' in available_fonts:
        print("  [OK] Times New Roman installed")
    else:
        print("  [WARN] Times New Roman not found, using default font")
    
    print()
    print("生成图表...")
    print("-" * 50)
    
    # 生成图 3-4
    print("\n[1/2] 生成图 3-4: 外推置信度衰减曲线")
    generate_figure_3_4()
    
    # 生成图 4-2
    print("\n[2/2] 生成图 4-2: 重排序前后精度对比柱状图")
    generate_figure_4_2()
    
    print()
    print("=" * 50)
    print("[OK] All figures generated successfully!")
    print(f"[OK] Output directory: {OUTPUT_DIR}")
    print("=" * 50)


if __name__ == '__main__':
    main()
