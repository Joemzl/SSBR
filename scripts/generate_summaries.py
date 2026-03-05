"""
Summary 综合档案生成脚本
为每个样本生成 summary.md，供 RAG 检索使用

Created: 2026-03-05
Tasks: T019-T026
"""

import sys
from pathlib import Path
from datetime import date
from typing import Dict, Any, List, Optional

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.excel_handler import ExcelHandler
from utils.yaml_parser import read_interpretation_file, write_interpretation_file, parse_yaml_frontmatter

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
INTERPRETATIONS_DIR = DATASET_DIR / "interpretations"
EXCEL_PATH = DATASET_DIR / "数据.xlsx"


def get_interpretation_status(sample_id: str) -> Dict[str, bool]:
    """
    检查样本的解读文档完整性
    
    Args:
        sample_id: 样本 ID
        
    Returns:
        各文档类型的存在状态
    """
    sample_dir = INTERPRETATIONS_DIR / sample_id
    
    status = {
        'mechanical': (sample_dir / 'mechanical.md').exists(),
        'dsc': (sample_dir / 'dsc.md').exists(),
        'nmr': (sample_dir / 'nmr.md').exists(),
        'tem': (sample_dir / 'tem.md').exists(),
    }
    
    return status


def extract_mechanical_data(sample_id: str) -> Dict[str, Any]:
    """
    从 mechanical.md 提取关键数据
    
    Args:
        sample_id: 样本 ID
        
    Returns:
        提取的数据字典
    """
    mech_path = INTERPRETATIONS_DIR / sample_id / "mechanical.md"
    
    if not mech_path.exists():
        return {}
    
    try:
        doc = read_interpretation_file(mech_path)
        yaml_data = doc['yaml'].get('data', {})
        
        result = {}
        
        # 提取数值
        for field in ['stress_100', 'stress_200', 'stress_300', 'tensile_strength', 'elongation']:
            if field in yaml_data:
                entry = yaml_data[field]
                if isinstance(entry, dict):
                    result[field] = entry.get('value')
                else:
                    result[field] = entry
        
        # 提取来源
        result['mechanical_source'] = yaml_data.get('mechanical_source')
        
        # 提取正文摘要（核心发现部分）
        body = doc['body']
        result['body_excerpt'] = body[:500] if body else None
        
        return result
        
    except Exception as e:
        print(f"  警告: 读取 {sample_id}/mechanical.md 失败: {e}")
        return {}


def extract_dsc_data(sample_id: str) -> Dict[str, Any]:
    """
    从 dsc.md 提取关键数据
    
    Args:
        sample_id: 样本 ID
        
    Returns:
        提取的数据字典
    """
    dsc_path = INTERPRETATIONS_DIR / sample_id / "dsc.md"
    
    if not dsc_path.exists():
        return {}
    
    try:
        doc = read_interpretation_file(dsc_path)
        yaml_data = doc['yaml'].get('data', {})
        
        result = {}
        
        # 提取 Tg
        if 'tg' in yaml_data:
            entry = yaml_data['tg']
            if isinstance(entry, dict):
                result['tg'] = entry.get('value')
                result['tg_range'] = entry.get('range')
            else:
                result['tg'] = entry
        
        # 提取来源
        result['thermal_source'] = yaml_data.get('thermal_source')
        
        return result
        
    except Exception as e:
        print(f"  警告: 读取 {sample_id}/dsc.md 失败: {e}")
        return {}


def generate_one_sentence_summary(
    metadata: Dict[str, Any],
    mech_data: Dict[str, Any],
    dsc_data: Dict[str, Any]
) -> str:
    """
    生成一句话总结
    
    Args:
        metadata: Excel 元数据
        mech_data: 力学数据
        dsc_data: 热学数据
        
    Returns:
        一句话总结
    """
    parts = []
    
    # 官能团信息
    fg_name = metadata.get('functional_group_name')
    if fg_name:
        parts.append(f"采用{fg_name}官能化")
    
    # 应用场景
    application = metadata.get('application')
    if application:
        parts.append(f"适用于{application}")
    
    # 如果没有提取到足够信息，给出通用描述
    if len(parts) < 2:
        return f"官能化 SSBR 样本，具有改性橡胶的典型性能特点"
    
    return "，".join(parts) + "。"


def generate_performance_features(
    mech_data: Dict[str, Any],
    dsc_data: Dict[str, Any]
) -> List[Dict[str, str]]:
    """
    生成核心性能特点列表
    
    Args:
        mech_data: 力学数据
        dsc_data: 热学数据
        
    Returns:
        特点列表
    """
    features = []
    
    # 力学性能特点
    if mech_data.get('tensile_strength'):
        ts = mech_data['tensile_strength']
        rating = "良好" if ts > 10 else "一般"
        features.append({
            'title': '拉伸强度',
            'rating': rating,
            'description': f"拉伸强度达到 {ts} MPa，{rating}的力学强度。"
        })
    
    if mech_data.get('elongation'):
        el = mech_data['elongation']
        rating = "优秀" if el > 400 else ("良好" if el > 300 else "一般")
        features.append({
            'title': '断裂伸长率',
            'rating': rating,
            'description': f"断裂伸长率为 {el}%，展现出{rating}的延展性。"
        })
    
    # 热学性能特点
    if dsc_data.get('tg'):
        tg = dsc_data['tg']
        if tg < -40:
            rating = "优秀"
            desc = "低温性能优异"
        elif tg < -20:
            rating = "良好"
            desc = "低温性能良好"
        else:
            rating = "一般"
            desc = "低温性能一般"
        
        features.append({
            'title': '玻璃化转变温度',
            'rating': rating,
            'description': f"Tg 为 {tg}℃，{desc}。"
        })
    
    return features


def generate_suitable_scenarios(
    metadata: Dict[str, Any],
    mech_data: Dict[str, Any],
    dsc_data: Dict[str, Any]
) -> List[str]:
    """
    生成适用场景列表
    
    Args:
        metadata: 元数据
        mech_data: 力学数据
        dsc_data: 热学数据
        
    Returns:
        适用场景列表
    """
    scenarios = []
    
    # 根据应用场景
    application = metadata.get('application')
    if application:
        scenarios.append(f"✅ {application}")
    
    # 根据性能数据推断
    if mech_data.get('elongation') and mech_data['elongation'] > 400:
        scenarios.append("✅ 需要高延展性的应用场景")
    
    if dsc_data.get('tg') and dsc_data['tg'] < -30:
        scenarios.append("✅ 低温环境应用")
    
    if not scenarios:
        scenarios.append("✅ 通用橡胶制品")
    
    # 添加注意事项
    if dsc_data.get('tg') and dsc_data['tg'] > -20:
        scenarios.append("⚠️ 注意：Tg 较高，低温性能可能受限")
    
    return scenarios


def build_summary_yaml(
    sample_id: str,
    interpretation_status: Dict[str, bool]
) -> Dict[str, Any]:
    """
    构建 summary.md 的 YAML front matter
    
    Args:
        sample_id: 样本 ID
        interpretation_status: 解读文档状态
        
    Returns:
        YAML 数据字典
    """
    today = date.today().isoformat()
    
    included = [k for k, v in interpretation_status.items() if v]
    missing = [k for k, v in interpretation_status.items() if not v]
    
    return {
        'sample_id': sample_id,
        'interpretation_type': 'summary',
        'skill_used': 'ssbr-summary-generator',
        'created_at': today,
        'updated_at': today,
        'interpretations_included': included,
        'interpretations_missing': missing,
    }


def build_summary_body(
    sample_id: str,
    metadata: Dict[str, Any],
    mech_data: Dict[str, Any],
    dsc_data: Dict[str, Any],
    interpretation_status: Dict[str, bool]
) -> str:
    """
    构建 summary.md 的 Markdown 正文
    
    Args:
        sample_id: 样本 ID
        metadata: Excel 元数据
        mech_data: 力学数据
        dsc_data: 热学数据
        interpretation_status: 解读文档状态
        
    Returns:
        Markdown 正文内容
    """
    lines = [f"# {sample_id} 综合档案", ""]
    
    # 一句话总结
    summary_sentence = generate_one_sentence_summary(metadata, mech_data, dsc_data)
    lines.extend([
        "## 一句话总结",
        "",
        summary_sentence,
        "",
        "---",
        "",
    ])
    
    # 官能化信息
    lines.extend([
        "## 官能化信息",
        "",
        f"- **官能化试剂**: {metadata.get('reagent_name') or '*未知*'}",
        f"- **核心官能团**: {metadata.get('functional_group_name') or '*未知*'} ({metadata.get('functional_group_formula') or '*未知*'})",
        f"- **官能化程度**: {metadata.get('functionalization_degree') or '*未知*'} wt%",
        "",
        "---",
        "",
    ])
    
    # 核心性能特点
    lines.extend(["## 核心性能特点", ""])
    
    features = generate_performance_features(mech_data, dsc_data)
    if features:
        for f in features:
            lines.extend([
                f"### {f['title']} 【{f['rating']}】",
                "",
                f"{f['description']}",
                "",
            ])
    else:
        lines.extend(["*暂无足够数据生成性能特点分析*", ""])
    
    lines.extend(["---", ""])
    
    # 适用场景
    lines.extend(["## 适用场景", ""])
    scenarios = generate_suitable_scenarios(metadata, mech_data, dsc_data)
    for s in scenarios:
        lines.append(f"- {s}")
    lines.extend(["", "---", ""])
    
    # 关键性能指标表
    lines.extend([
        "## 关键性能指标",
        "",
        "| 类别 | 指标 | 数值 | 单位 | 评价 |",
        "|------|------|------|------|------|",
    ])
    
    # 力学数据
    for field, label in [
        ('stress_100', '100%定伸应力'),
        ('stress_200', '200%定伸应力'),
        ('stress_300', '300%定伸应力'),
        ('tensile_strength', '拉伸强度'),
        ('elongation', '断裂伸长率'),
    ]:
        val = mech_data.get(field)
        unit = '%' if field == 'elongation' else 'MPa'
        lines.append(f"| 力学性能 | {label} | {val or '-'} | {unit} | - |")
    
    # 热学数据
    tg_val = dsc_data.get('tg') or dsc_data.get('tg_range') or '-'
    lines.append(f"| 热学性能 | Tg | {tg_val} | ℃ | - |")
    
    lines.extend(["", "---", ""])
    
    # 解读文档完整性
    lines.extend([
        "## 解读文档完整性",
        "",
        "| 文档类型 | 状态 | 备注 |",
        "|----------|------|------|",
    ])
    
    for doc_type, exists in interpretation_status.items():
        status = "✓" if exists else "✗"
        note = "已生成" if exists else "暂无数据"
        lines.append(f"| {doc_type}.md | {status} | {note} |")
    
    lines.extend(["", "---", ""])
    
    # 文献来源
    lines.extend([
        "## 文献来源",
        "",
        f"- **DOI**: {metadata.get('doi') or '*未知*'}",
        f"- **引文**: {metadata.get('citation') or '*未知*'}",
    ])
    
    if metadata.get('doi_si'):
        lines.append(f"- **SI**: {metadata.get('doi_si')}")
    
    lines.extend([
        "",
        "---",
        "",
        "*本综合档案由 `ssbr-summary-generator` 脚本自动生成，用于 RAG 语义检索。*",
    ])
    
    return "\n".join(lines)


def generate_summary(sample_id: str, excel_handler: ExcelHandler, dry_run: bool = False) -> Dict[str, Any]:
    """
    为单个样本生成 summary.md
    
    Args:
        sample_id: 样本 ID
        excel_handler: Excel 处理器
        dry_run: 如果为 True，只打印不实际写入
        
    Returns:
        生成结果
    """
    result = {
        'sample_id': sample_id,
        'created': False,
        'errors': []
    }
    
    # 获取元数据
    metadata = excel_handler.get_metadata_fields(sample_id)
    if not metadata:
        result['errors'].append(f"未找到样本 {sample_id} 的元数据")
        return result
    
    # 获取解读文档状态
    interpretation_status = get_interpretation_status(sample_id)
    
    # 提取解读数据
    mech_data = extract_mechanical_data(sample_id)
    dsc_data = extract_dsc_data(sample_id)
    
    # 构建 YAML 和正文
    yaml_data = build_summary_yaml(sample_id, interpretation_status)
    body = build_summary_body(sample_id, metadata, mech_data, dsc_data, interpretation_status)
    
    # 写入文件
    output_path = INTERPRETATIONS_DIR / sample_id / "summary.md"
    
    if dry_run:
        print(f"  [DRY RUN] 将创建 {output_path}")
    else:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            write_interpretation_file(output_path, yaml_data, body)
            result['created'] = True
        except Exception as e:
            result['errors'].append(f"写入失败: {e}")
    
    return result


def generate_all_summaries(dry_run: bool = False) -> Dict[str, Any]:
    """
    为所有样本生成 summary.md
    
    Args:
        dry_run: 如果为 True，只打印不实际写入
        
    Returns:
        生成统计
    """
    stats = {
        'total_samples': 0,
        'created': 0,
        'errors': []
    }
    
    with ExcelHandler(EXCEL_PATH) as excel:
        samples = excel.get_all_samples()
        stats['total_samples'] = len(samples)
        
        print(f"\n开始生成 {len(samples)} 个样本的综合档案...")
        
        for sample in samples:
            sample_id = sample.get('sample_id')
            if not sample_id:
                continue
            
            print(f"\n处理 {sample_id}...")
            result = generate_summary(sample_id, excel, dry_run)
            
            if result['created']:
                stats['created'] += 1
                print(f"  [OK] summary.md 已生成")
            
            if result['errors']:
                stats['errors'].extend([f"{sample_id}: {e}" for e in result['errors']])
                for err in result['errors']:
                    print(f"  [ERROR] 错误: {err}")
    
    return stats


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SSBR Summary 综合档案生成工具')
    parser.add_argument('--dry-run', action='store_true', help='只打印操作，不实际执行')
    parser.add_argument('--sample', type=str, help='只处理指定样本（如 SSBR-001）')
    args = parser.parse_args()
    
    print("=" * 60)
    print("SSBR Summary 综合档案生成工具")
    print("=" * 60)
    
    if args.dry_run:
        print("\n[DRY RUN 模式] 只显示将要执行的操作")
    
    if args.sample:
        # 单个样本处理
        with ExcelHandler(EXCEL_PATH) as excel:
            result = generate_summary(args.sample, excel, dry_run=args.dry_run)
            if result['created']:
                print(f"\n[OK] {args.sample}/summary.md 生成成功")
            else:
                print(f"\n[ERROR] 生成失败: {result['errors']}")
    else:
        # 批量处理
        stats = generate_all_summaries(dry_run=args.dry_run)
        
        print("\n" + "=" * 60)
        print("生成统计")
        print("=" * 60)
        print(f"  总样本数: {stats['total_samples']}")
        print(f"  成功生成: {stats['created']}")
        print(f"  错误数: {len(stats['errors'])}")
        
        if stats['errors']:
            print("\n错误列表:")
            for err in stats['errors']:
                print(f"  - {err}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
