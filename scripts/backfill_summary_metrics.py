#!/usr/bin/env python3
"""
从 mechanical.md 和 dsc.md 中提取关键性能指标，回填到 summary.md

支持的指标类型:
1. 传统力学指标: 100%/200%/300%定伸应力、拉伸强度、断裂伸长率
2. Payne效应指标: 活化能 Ea、ΔG' 
3. DMA指标: tan δmax、tan δ(0℃)、tan δ(60℃)
4. 热学指标: Tg

用法:
    python scripts/backfill_summary_metrics.py              # 处理所有样本
    python scripts/backfill_summary_metrics.py --sample SSBR-004  # 处理单个样本
    python scripts/backfill_summary_metrics.py --dry-run    # 仅显示将要更新的内容
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import argparse


def extract_yaml_from_md(content: str) -> Optional[Dict[str, Any]]:
    """从 Markdown 中提取 YAML 数据（支持两种格式）"""
    
    # 格式1: YAML 代码块 ```yaml ... ```
    yaml_block_match = re.search(r'```yaml\s*\n(.+?)\n```', content, re.DOTALL)
    if yaml_block_match:
        try:
            return yaml.safe_load(yaml_block_match.group(1))
        except yaml.YAMLError:
            pass
    
    # 格式2: YAML front matter --- ... ---
    front_matter_match = re.match(r'^---\s*\n(.+?)\n---', content, re.DOTALL)
    if front_matter_match:
        try:
            return yaml.safe_load(front_matter_match.group(1))
        except yaml.YAMLError:
            pass
    
    return None


def get_value(data: Dict, *keys) -> Optional[Any]:
    """安全地从嵌套字典中获取值"""
    current = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current if current is not None else None


def extract_from_markdown_table(content: str, patterns: List[Tuple[str, int]]) -> Optional[float]:
    """从 Markdown 表格中提取数值
    
    Args:
        content: Markdown 内容
        patterns: [(正则模式, 捕获组索引), ...] 列表
    
    Returns:
        提取的数值或 None
    """
    for pattern, group_idx in patterns:
        match = re.search(pattern, content)
        if match:
            try:
                return float(match.group(group_idx))
            except (ValueError, IndexError):
                continue
    return None


def extract_mechanical_metrics(md_path: Path) -> Dict[str, Any]:
    """从 mechanical.md 提取力学性能指标（包含传统力学和 Payne 效应）"""
    metrics = {
        'stress_100': None,
        'stress_200': None,
        'stress_300': None,
        'tensile_strength': None,
        'elongation': None,
        # Payne 效应指标
        'activation_energy': None,  # 活化能 Ea (kJ/mol)
        'delta_g_prime': None,      # ΔG' (MPa)
    }
    
    if not md_path.exists():
        return metrics
    
    content = md_path.read_text(encoding='utf-8')
    data = extract_yaml_from_md(content)
    
    if data:
        # 从 YAML 提取传统力学指标
        mech = data.get('mechanical_properties', data.get('data', {}))
        metrics['stress_100'] = get_value(mech, 'stress_100', 'value')
        metrics['stress_200'] = get_value(mech, 'stress_200', 'value')
        metrics['stress_300'] = get_value(mech, 'stress_300', 'value')
        metrics['tensile_strength'] = get_value(mech, 'tensile_strength', 'value')
        metrics['elongation'] = get_value(mech, 'elongation_at_break', 'value') or get_value(mech, 'elongation', 'value')
        
        # 从 YAML 提取 Payne 效应指标
        payne = data.get('payne_effect', {})
        metrics['activation_energy'] = get_value(payne, 'activation_energy', 'value')
        metrics['delta_g_prime'] = get_value(payne, 'delta_G_prime', 'value')
    
    # 从 Markdown 表格中提取 Payne 效应指标 (如果 YAML 中没有)
    if metrics['activation_energy'] is None:
        metrics['activation_energy'] = extract_from_markdown_table(content, [
            # | 活化能 Ea | 11.3 | kJ/mol |
            (r'\|\s*活化能\s*Ea?\s*\|\s*([\d.]+)\s*\|', 1),
            # | Ea (kJ/mol) | 11.3 |
            (r'Ea\s*\(?kJ/mol\)?\s*\|\s*([\d.]+)', 1),
            # Ea = 11.3 kJ/mol
            (r'Ea\s*[=:]\s*([\d.]+)\s*kJ', 1),
        ])
    
    return metrics


def extract_dma_metrics(md_path: Path) -> Dict[str, Any]:
    """从 mechanical.md 或 dsc.md 提取 DMA 指标"""
    metrics = {
        'tan_delta_max': None,
        'tan_delta_0c': None,
        'tan_delta_60c': None,
    }
    
    if not md_path.exists():
        return metrics
    
    content = md_path.read_text(encoding='utf-8')
    data = extract_yaml_from_md(content)
    
    if data:
        # 从 YAML 提取 DMA 指标
        dma = data.get('dma_properties', {})
        metrics['tan_delta_max'] = get_value(dma, 'tan_delta_max', 'value') or get_value(dma, 'tan_delta_max')
        metrics['tan_delta_0c'] = get_value(dma, 'tan_delta_0C', 'value')
        metrics['tan_delta_60c'] = get_value(dma, 'tan_delta_60C', 'value')
    
    # 从 Markdown 表格中提取 DMA 指标
    if metrics['tan_delta_max'] is None:
        metrics['tan_delta_max'] = extract_from_markdown_table(content, [
            # | tan δmax | 1.07 | 高 |
            (r'\|\s*tan\s*δmax\s*\|\s*([\d.]+)\s*\|', 1),
            # | tan δmax | 1.0460 |
            (r'tan\s*δmax\s*\|\s*([\d.]+)', 1),
            # tan δmax = 1.1940
            (r'tan\s*δmax\s*[=:]\s*([\d.]+)', 1),
            # **tan δmax = 1.1940**
            (r'\*\*tan\s*δmax\s*[=:]\s*([\d.]+)', 1),
        ])
    
    if metrics['tan_delta_0c'] is None:
        metrics['tan_delta_0c'] = extract_from_markdown_table(content, [
            # | tan δ (0℃) | 0.7596 |
            (r'\|\s*tan\s*δ\s*\(?0℃?\)?\s*\|\s*([\d.]+)\s*\|', 1),
            # tan δ (0℃) = 0.8737
            (r'tan\s*δ\s*\(?0℃?\)?\s*[=:]\s*([\d.]+)', 1),
        ])
    
    if metrics['tan_delta_60c'] is None:
        metrics['tan_delta_60c'] = extract_from_markdown_table(content, [
            # | tan δ (60℃) | 0.0913 |
            (r'\|\s*tan\s*δ\s*\(?60℃?\)?\s*\|\s*([\d.]+)\s*\|', 1),
            # tan δ (60℃) = 0.0797
            (r'tan\s*δ\s*\(?60℃?\)?\s*[=:]\s*([\d.]+)', 1),
        ])
    
    return metrics


def extract_thermal_metrics(md_path: Path) -> Dict[str, Any]:
    """从 dsc.md 提取热学性能指标"""
    metrics = {
        'tg': None,
    }
    
    if not md_path.exists():
        return metrics
    
    content = md_path.read_text(encoding='utf-8')
    data = extract_yaml_from_md(content)
    
    if data:
        # 尝试从 thermal_properties 或 data 中提取
        thermal = data.get('thermal_properties', data.get('data', {}))
        metrics['tg'] = get_value(thermal, 'tg', 'value')
    
    # 如果 YAML 中没有，尝试从 Markdown 表格中提取
    if metrics['tg'] is None:
        metrics['tg'] = extract_tg_from_markdown(content)
    
    return metrics


def extract_tg_from_markdown(content: str) -> Optional[float]:
    """从 Markdown 表格中提取 Tg 值"""
    patterns = [
        # | SSBR（未改性） | -26.1 | 0 |
        (r'\|\s*SSBR[^|]*\|\s*([-\d.]+)\s*\|', 1),
        # | Tg | -9.0 | ℃ |
        (r'\|\s*Tg\s*\|\s*([-\d.]+)\s*\|', 1),
        # | 玻璃化转变温度 | -26.1 | ℃ |
        (r'\|\s*玻璃化转变温度[^|]*\|\s*([-\d.]+)\s*\|', 1),
        # Tg = -26.1℃ 
        (r'Tg\s*[=:]\s*([-\d.]+)\s*℃', 1),
        # **Tg = -26.1℃**
        (r'\*\*Tg\s*[=:]\s*([-\d.]+)\s*℃', 1),
        # | Tg | -7.8℃ | +0.2℃ |  (带℃符号的表格)
        (r'\|\s*Tg\s*\|\s*([-\d.]+)℃\s*\|', 1),
        # | Tg (tan δ 峰温) | -8.0℃ |
        (r'Tg[^|]*\|\s*([-\d.]+)℃?\s*\|', 1),
    ]
    
    return extract_from_markdown_table(content, patterns)


def format_value(value: Any, decimals: int = 1) -> str:
    """格式化数值为显示字符串"""
    if value is None:
        return "-"
    if isinstance(value, float):
        if decimals == 0 or abs(value) >= 100:
            return f"{value:.0f}"
        elif decimals == 4:
            return f"{value:.4f}"
        elif decimals == 2:
            return f"{value:.2f}"
        else:
            return f"{value:.1f}"
    return str(value)


def evaluate_metric(metric_type: str, value: Any, sample_id: str) -> str:
    """根据指标类型和数值给出评价"""
    if value is None:
        return "-"
    
    # 针对空白对照样本的特殊处理
    blank_samples = ["SSBR-001", "SSBR-005", "SSBR-009", "SSBR-013"]
    if sample_id in blank_samples:
        return "基准"
    
    # 针对不同指标类型的评价标准
    evaluations = {
        # 传统力学指标
        'stress_100': lambda v: "优" if v >= 2.5 else ("良" if v >= 2.0 else "中"),
        'stress_300': lambda v: "优" if v >= 12.0 else ("良" if v >= 10.0 else "中"),
        'tensile_strength': lambda v: "优" if v >= 20.0 else ("良" if v >= 17.0 else "中"),
        'elongation': lambda v: "优" if v >= 450 else ("良" if v >= 400 else "中"),
        # 热学指标
        'tg': lambda v: "适中" if -10 <= v <= -5 else ("偏低" if v < -10 else "偏高"),
        # Payne 效应指标 (活化能越高越好)
        'activation_energy': lambda v: "优" if v >= 16 else ("良" if v >= 13 else "中"),
        # DMA 指标
        'tan_delta_max': lambda v: "优" if v >= 1.2 else ("良" if v >= 1.1 else "中"),
        'tan_delta_0c': lambda v: "优" if v >= 0.85 else ("良" if v >= 0.75 else "中"),  # 高=好(湿抓地)
        'tan_delta_60c': lambda v: "优" if v <= 0.08 else ("良" if v <= 0.09 else "中"),  # 低=好(滚阻)
    }
    
    if metric_type in evaluations:
        return evaluations[metric_type](value)
    return "-"


def generate_metrics_table(metrics: Dict[str, Any], sample_id: str) -> str:
    """生成关键性能指标表格"""
    rows = []
    rows.append("| 类别 | 指标 | 数值 | 单位 | 评价 |")
    rows.append("|------|------|------|------|------|")
    
    # 传统力学性能 (仅当有数据时才显示)
    has_traditional_mech = any(metrics.get(k) is not None for k in ['stress_100', 'stress_300', 'tensile_strength', 'elongation'])
    if has_traditional_mech:
        rows.append(f"| 力学性能 | 100%定伸应力 | {format_value(metrics.get('stress_100'))} | MPa | {evaluate_metric('stress_100', metrics.get('stress_100'), sample_id)} |")
        rows.append(f"| 力学性能 | 200%定伸应力 | {format_value(metrics.get('stress_200'))} | MPa | - |")
        rows.append(f"| 力学性能 | 300%定伸应力 | {format_value(metrics.get('stress_300'))} | MPa | {evaluate_metric('stress_300', metrics.get('stress_300'), sample_id)} |")
        rows.append(f"| 力学性能 | 拉伸强度 | {format_value(metrics.get('tensile_strength'))} | MPa | {evaluate_metric('tensile_strength', metrics.get('tensile_strength'), sample_id)} |")
        rows.append(f"| 力学性能 | 断裂伸长率 | {format_value(metrics.get('elongation'), 0)} | % | {evaluate_metric('elongation', metrics.get('elongation'), sample_id)} |")
    
    # Payne 效应指标 (仅当有数据时才显示)
    if metrics.get('activation_energy') is not None:
        rows.append(f"| Payne效应 | 活化能 Ea | {format_value(metrics.get('activation_energy'))} | kJ/mol | {evaluate_metric('activation_energy', metrics.get('activation_energy'), sample_id)} |")
    
    # DMA 动态力学指标 (仅当有数据时才显示)
    has_dma = any(metrics.get(k) is not None for k in ['tan_delta_max', 'tan_delta_0c', 'tan_delta_60c'])
    if has_dma:
        if metrics.get('tan_delta_max') is not None:
            rows.append(f"| 动态性能 | tan δmax | {format_value(metrics.get('tan_delta_max'), 2)} | - | {evaluate_metric('tan_delta_max', metrics.get('tan_delta_max'), sample_id)} |")
        if metrics.get('tan_delta_0c') is not None:
            rows.append(f"| 动态性能 | tan δ (0℃) | {format_value(metrics.get('tan_delta_0c'), 4)} | - | {evaluate_metric('tan_delta_0c', metrics.get('tan_delta_0c'), sample_id)} |")
        if metrics.get('tan_delta_60c') is not None:
            rows.append(f"| 动态性能 | tan δ (60℃) | {format_value(metrics.get('tan_delta_60c'), 4)} | - | {evaluate_metric('tan_delta_60c', metrics.get('tan_delta_60c'), sample_id)} |")
    
    # 热学性能
    rows.append(f"| 热学性能 | Tg | {format_value(metrics.get('tg'))} | ℃ | {evaluate_metric('tg', metrics.get('tg'), sample_id)} |")
    
    return "\n".join(rows)


def generate_performance_summary(metrics: Dict[str, Any], sample_id: str) -> str:
    """生成核心性能特点总结"""
    points = []
    
    # 分析传统力学性能
    ts = metrics.get('tensile_strength')
    s100 = metrics.get('stress_100')
    s300 = metrics.get('stress_300')
    elong = metrics.get('elongation')
    tg = metrics.get('tg')
    
    # Payne 效应和 DMA 指标
    ea = metrics.get('activation_energy')
    tan_max = metrics.get('tan_delta_max')
    tan_0c = metrics.get('tan_delta_0c')
    tan_60c = metrics.get('tan_delta_60c')
    
    # 传统力学性能分析
    if ts is not None:
        if ts >= 20:
            points.append(f"拉伸强度优异（{ts:.1f} MPa），力学性能突出")
        elif ts >= 17:
            points.append(f"拉伸强度良好（{ts:.1f} MPa）")
        else:
            points.append(f"拉伸强度中等（{ts:.1f} MPa）")
    
    if s100 is not None and s300 is not None:
        modulus_ratio = s300 / s100 if s100 > 0 else 0
        if modulus_ratio >= 5:
            points.append(f"模量增长显著（300%/100% = {modulus_ratio:.1f}），界面结合强")
    
    if elong is not None:
        if elong >= 450:
            points.append(f"断裂伸长率高（{elong:.0f}%），延展性好")
        elif elong < 400:
            points.append(f"断裂伸长率适中（{elong:.0f}%），刚性增强")
    
    # Payne 效应分析
    if ea is not None:
        if ea >= 16:
            points.append(f"Payne效应活化能高（{ea:.1f} kJ/mol），填料网络稳定")
        elif ea >= 13:
            points.append(f"Payne效应活化能良好（{ea:.1f} kJ/mol）")
        else:
            points.append(f"Payne效应活化能较低（{ea:.1f} kJ/mol），填料网络不稳定")
    
    # DMA 动态性能分析
    if tan_max is not None:
        if tan_max >= 1.2:
            points.append(f"tan δmax 高（{tan_max:.2f}），能量耗散能力强")
        elif tan_max >= 1.0:
            points.append(f"tan δmax 适中（{tan_max:.2f}）")
    
    if tan_0c is not None and tan_60c is not None:
        # 评估轮胎性能平衡（魔术三角）
        if tan_0c >= 0.85 and tan_60c <= 0.08:
            points.append(f"动态性能优异：抗湿滑（tan δ 0℃={tan_0c:.4f}）与低滚阻（tan δ 60℃={tan_60c:.4f}）兼得")
        elif tan_0c >= 0.80:
            points.append(f"抗湿滑性良好（tan δ 0℃={tan_0c:.4f}）")
        if tan_60c <= 0.08:
            points.append(f"滚动阻力低（tan δ 60℃={tan_60c:.4f}）")
        elif tan_60c >= 0.09:
            points.append(f"滚动阻力较高（tan δ 60℃={tan_60c:.4f}），有改进空间")
    
    # Tg 分析
    if tg is not None:
        if tg >= -6:
            points.append(f"Tg 偏高（{tg:.1f}℃），湿抓地力有利")
        elif tg <= -9:
            points.append(f"Tg 偏低（{tg:.1f}℃），低温性能良好")
        else:
            points.append(f"Tg 适中（{tg:.1f}℃），性能均衡")
    
    if not points:
        return "*暂无足够数据生成性能特点分析*"
    
    return "\n".join(f"- {p}" for p in points)


def update_summary_md(sample_dir: Path, dry_run: bool = False) -> bool:
    """更新单个样本的 summary.md"""
    sample_id = sample_dir.name
    summary_path = sample_dir / "summary.md"
    mechanical_path = sample_dir / "mechanical.md"
    dsc_path = sample_dir / "dsc.md"
    
    if not summary_path.exists():
        print(f"  [WARN] {sample_id}: summary.md does not exist, skip")
        return False
    
    # 提取所有指标
    mech_metrics = extract_mechanical_metrics(mechanical_path)
    thermal_metrics = extract_thermal_metrics(dsc_path)
    
    # 从 mechanical.md 和 dsc.md 都尝试提取 DMA 指标
    dma_from_mech = extract_dma_metrics(mechanical_path)
    dma_from_dsc = extract_dma_metrics(dsc_path)
    
    # 合并 DMA 指标（优先 dsc.md）
    dma_metrics = {
        'tan_delta_max': dma_from_dsc.get('tan_delta_max') or dma_from_mech.get('tan_delta_max'),
        'tan_delta_0c': dma_from_dsc.get('tan_delta_0c') or dma_from_mech.get('tan_delta_0c'),
        'tan_delta_60c': dma_from_dsc.get('tan_delta_60c') or dma_from_mech.get('tan_delta_60c'),
    }
    
    # 合并所有指标
    all_metrics = {
        **mech_metrics,
        **thermal_metrics,
        **dma_metrics,
    }
    
    # 检查是否有有效数据
    has_data = any(v is not None for v in all_metrics.values())
    
    if not has_data:
        print(f"  [WARN] {sample_id}: no valid data found")
        return False
    
    # 生成新内容
    new_table = generate_metrics_table(all_metrics, sample_id)
    new_summary = generate_performance_summary(all_metrics, sample_id)
    
    # 读取当前 summary.md
    content = summary_path.read_text(encoding='utf-8')
    
    # 替换关键性能指标表格
    table_pattern = r'(## 关键性能指标\s*\n\n)([\s\S]*?)(\n---|\n## )'
    if re.search(table_pattern, content):
        content = re.sub(table_pattern, f'\\1{new_table}\n\n\\3', content)
    
    # 替换核心性能特点
    perf_pattern = r'(## 核心性能特点\s*\n\n)([\s\S]*?)(\n---|\n## )'
    if re.search(perf_pattern, content):
        content = re.sub(perf_pattern, f'\\1{new_summary}\n\n\\3', content)
    
    if dry_run:
        print(f"\n  [PREVIEW] {sample_id}:")
        print(f"     Mech: stress_100={mech_metrics.get('stress_100')}, stress_300={mech_metrics.get('stress_300')}, tensile={mech_metrics.get('tensile_strength')}, elong={mech_metrics.get('elongation')}")
        print(f"     Payne: Ea={mech_metrics.get('activation_energy')}")
        print(f"     DMA: tan_max={dma_metrics.get('tan_delta_max')}, tan_0c={dma_metrics.get('tan_delta_0c')}, tan_60c={dma_metrics.get('tan_delta_60c')}")
        print(f"     Thermal: Tg={thermal_metrics.get('tg')}")
    else:
        summary_path.write_text(content, encoding='utf-8')
        print(f"  [OK] {sample_id}: updated")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Backfill summary.md with performance metrics")
    parser.add_argument('--sample', type=str, help='Specify sample ID (e.g. SSBR-004)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without writing')
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent / "dataset" / "interpretations"
    
    if args.sample:
        sample_dirs = [base_dir / args.sample]
        if not sample_dirs[0].exists():
            print(f"[ERROR] Sample directory not found: {args.sample}")
            return
    else:
        sample_dirs = sorted([d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith("SSBR-")])
    
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Backfilling summary.md metrics...")
    print(f"Total: {len(sample_dirs)} samples\n")
    
    success_count = 0
    for sample_dir in sample_dirs:
        if update_summary_md(sample_dir, args.dry_run):
            success_count += 1
    
    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Done! Updated {success_count}/{len(sample_dirs)} samples")


if __name__ == "__main__":
    main()
