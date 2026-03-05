"""
Excel 数据迁移脚本
将 Excel P-W 列数据迁移到解读文档的 YAML front matter

Created: 2026-03-05
Tasks: T010, T013, T014, T017
"""

import sys
from pathlib import Path
from datetime import date
from typing import Dict, Any, List, Optional

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.excel_handler import ExcelHandler
from utils.yaml_parser import write_interpretation_file, read_interpretation_file, parse_yaml_frontmatter

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
INTERPRETATIONS_DIR = DATASET_DIR / "interpretations"
EXCEL_PATH = DATASET_DIR / "数据.xlsx"


def build_mechanical_yaml(
    sample_id: str,
    data: Dict[str, Any],
    source_figure: Optional[str] = None,
    source_doi: Optional[str] = None
) -> Dict[str, Any]:
    """
    构建 mechanical.md 的 YAML front matter
    
    Args:
        sample_id: 样本 ID
        data: 从 Excel 提取的力学数据
        source_figure: 来源图注
        source_doi: 来源 DOI
    """
    today = date.today().isoformat()
    
    yaml_data = {
        'sample_id': sample_id,
        'interpretation_type': 'mechanical',
        'source_figure': source_figure,
        'source_doi': source_doi,
        'skill_used': 'data-migration',
        'created_at': today,
        'updated_at': today,
        'mechanical_subtypes': ['stress-strain'],
        'data': {}
    }
    
    # 应力-应变数据
    if data.get('stress_100') is not None:
        yaml_data['data']['stress_100'] = {
            'value': data['stress_100'],
            'unit': 'MPa',
            'source': data.get('mechanical_source', '文献数据')
        }
    
    if data.get('stress_200') is not None:
        yaml_data['data']['stress_200'] = {
            'value': data['stress_200'],
            'unit': 'MPa',
            'source': data.get('mechanical_source', '文献数据')
        }
    
    if data.get('stress_300') is not None:
        yaml_data['data']['stress_300'] = {
            'value': data['stress_300'],
            'unit': 'MPa',
            'source': data.get('mechanical_source', '文献数据')
        }
    
    if data.get('tensile_strength') is not None:
        yaml_data['data']['tensile_strength'] = {
            'value': data['tensile_strength'],
            'unit': 'MPa',
            'source': data.get('mechanical_source', '文献数据')
        }
    
    if data.get('elongation') is not None:
        yaml_data['data']['elongation'] = {
            'value': data['elongation'],
            'unit': '%',
            'source': data.get('mechanical_source', '文献数据')
        }
    
    if data.get('mechanical_source'):
        yaml_data['data']['mechanical_source'] = data['mechanical_source']
    
    return yaml_data


def build_dsc_yaml(
    sample_id: str,
    data: Dict[str, Any],
    source_figure: Optional[str] = None,
    source_doi: Optional[str] = None
) -> Dict[str, Any]:
    """
    构建 dsc.md 的 YAML front matter
    
    Args:
        sample_id: 样本 ID
        data: 从 Excel 提取的热学数据
        source_figure: 来源图注
        source_doi: 来源 DOI
    """
    today = date.today().isoformat()
    
    yaml_data = {
        'sample_id': sample_id,
        'interpretation_type': 'dsc',
        'source_figure': source_figure,
        'source_doi': source_doi,
        'skill_used': 'data-migration',
        'created_at': today,
        'updated_at': today,
        'data': {}
    }
    
    if data.get('tg') is not None:
        yaml_data['data']['tg'] = {
            'value': data['tg'],
            'unit': '℃',
            'source': data.get('thermal_source', '文献数据')
        }
    
    if data.get('thermal_source'):
        yaml_data['data']['thermal_source'] = data['thermal_source']
    
    return yaml_data


def build_mechanical_body(sample_id: str, data: Dict[str, Any]) -> str:
    """构建 mechanical.md 的 Markdown 正文"""
    lines = [
        f"# 力学性能解读：{sample_id}",
        "",
        "> 此文档由数据迁移脚本自动生成，数据来源于原 Excel 文件。",
        "> 如需完整解读，请使用 `@ssbr-mechanical-interpretation` Skill 重新解读文献图谱。",
        "",
        "## 一、静态力学性能（应力-应变曲线）",
        "",
        "### 数值数据",
        "",
        "| 指标 | 数值 | 单位 |",
        "|------|------|------|",
    ]
    
    if data.get('stress_100') is not None:
        lines.append(f"| 100%定伸应力 | {data['stress_100']} | MPa |")
    if data.get('stress_200') is not None:
        lines.append(f"| 200%定伸应力 | {data['stress_200']} | MPa |")
    if data.get('stress_300') is not None:
        lines.append(f"| 300%定伸应力 | {data['stress_300']} | MPa |")
    if data.get('tensile_strength') is not None:
        lines.append(f"| 拉伸强度 | {data['tensile_strength']} | MPa |")
    if data.get('elongation') is not None:
        lines.append(f"| 断裂伸长率 | {data['elongation']} | % |")
    
    lines.extend([
        "",
        f"**数据来源**: {data.get('mechanical_source', '文献数据')}",
        "",
        "### 核心发现",
        "",
        "*待补充：请使用 Skill 解读文献图谱获取详细分析。*",
        "",
        "## 二、动态力学性能（Payne效应）",
        "",
        "*暂无此项数据*",
        "",
        "## 三、动态力学性能（DMA温度扫描）",
        "",
        "*暂无此项数据*",
    ])
    
    return "\n".join(lines)


def build_dsc_body(sample_id: str, data: Dict[str, Any]) -> str:
    """构建 dsc.md 的 Markdown 正文"""
    lines = [
        f"# DSC 热分析解读：{sample_id}",
        "",
        "> 此文档由数据迁移脚本自动生成，数据来源于原 Excel 文件。",
        "> 如需完整解读，请使用 `@ssbr-dsc-interpretation` Skill 重新解读文献图谱。",
        "",
        "## 一、玻璃化转变",
        "",
        "### 数值数据",
        "",
        "| 指标 | 数值 | 单位 |",
        "|------|------|------|",
    ]
    
    if data.get('tg') is not None:
        lines.append(f"| 玻璃化转变温度 (Tg) | {data['tg']} | ℃ |")
    
    lines.extend([
        "",
        f"**数据来源**: {data.get('thermal_source', '文献数据')}",
        "",
        "### 核心发现",
        "",
        "*待补充：请使用 Skill 解读文献图谱获取详细分析。*",
    ])
    
    return "\n".join(lines)


def migrate_sample(
    sample_id: str,
    excel_handler: ExcelHandler,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    迁移单个样本的数据
    
    Args:
        sample_id: 样本 ID
        excel_handler: Excel 处理器
        dry_run: 如果为 True，只打印不实际写入
        
    Returns:
        迁移结果信息
    """
    result = {
        'sample_id': sample_id,
        'mechanical_created': False,
        'dsc_created': False,
        'errors': []
    }
    
    # 获取迁移数据
    migration_data = excel_handler.get_migration_data(sample_id)
    if not migration_data:
        result['errors'].append(f"未找到样本 {sample_id} 的数据")
        return result
    
    # 获取元数据（用于 source_figure 和 source_doi）
    metadata = excel_handler.get_metadata_fields(sample_id)
    source_figure = metadata.get('mechanical_figure')
    source_doi = metadata.get('doi')
    dsc_figure = metadata.get('dsc_figure')
    
    sample_dir = INTERPRETATIONS_DIR / sample_id
    
    # 确保目录存在
    if not dry_run:
        sample_dir.mkdir(parents=True, exist_ok=True)
    
    # 迁移 mechanical 数据
    mech_data = migration_data.get('mechanical', {})
    if any(v is not None for v in mech_data.values()):
        mechanical_yaml = build_mechanical_yaml(sample_id, mech_data, source_figure, source_doi)
        mechanical_body = build_mechanical_body(sample_id, mech_data)
        
        if dry_run:
            print(f"  [DRY RUN] 将创建 {sample_dir / 'mechanical.md'}")
        else:
            write_interpretation_file(sample_dir / 'mechanical.md', mechanical_yaml, mechanical_body)
            result['mechanical_created'] = True
    
    # 迁移 dsc 数据
    dsc_data = migration_data.get('dsc', {})
    if any(v is not None for v in dsc_data.values()):
        dsc_yaml = build_dsc_yaml(sample_id, dsc_data, dsc_figure, source_doi)
        dsc_body = build_dsc_body(sample_id, dsc_data)
        
        if dry_run:
            print(f"  [DRY RUN] 将创建 {sample_dir / 'dsc.md'}")
        else:
            write_interpretation_file(sample_dir / 'dsc.md', dsc_yaml, dsc_body)
            result['dsc_created'] = True
    
    return result


def delete_migration_columns(excel_handler: ExcelHandler, dry_run: bool = False) -> None:
    """
    删除 Excel 中的 P-W 列
    
    Args:
        excel_handler: Excel 处理器
        dry_run: 如果为 True，只打印不实际删除
    """
    columns_to_delete = ['P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']
    
    if dry_run:
        print(f"\n[DRY RUN] 将删除列: {columns_to_delete}")
    else:
        excel_handler.delete_columns(columns_to_delete)
        print(f"\n已删除列: {columns_to_delete}")


def migrate_all(dry_run: bool = False, delete_columns: bool = False) -> Dict[str, Any]:
    """
    迁移所有样本数据
    
    Args:
        dry_run: 如果为 True，只打印不实际操作
        delete_columns: 是否在迁移后删除 Excel 列
        
    Returns:
        迁移统计信息
    """
    stats = {
        'total_samples': 0,
        'mechanical_created': 0,
        'dsc_created': 0,
        'errors': []
    }
    
    with ExcelHandler(EXCEL_PATH) as excel:
        samples = excel.get_all_samples()
        stats['total_samples'] = len(samples)
        
        print(f"\n开始迁移 {len(samples)} 个样本...")
        
        for sample in samples:
            sample_id = sample.get('sample_id')
            if not sample_id:
                continue
            
            print(f"\n处理 {sample_id}...")
            result = migrate_sample(sample_id, excel, dry_run)
            
            if result['mechanical_created']:
                stats['mechanical_created'] += 1
                print(f"  ✓ mechanical.md 已创建")
            
            if result['dsc_created']:
                stats['dsc_created'] += 1
                print(f"  ✓ dsc.md 已创建")
            
            if result['errors']:
                stats['errors'].extend(result['errors'])
                for err in result['errors']:
                    print(f"  ✗ 错误: {err}")
        
        # 删除 Excel 列
        if delete_columns and not dry_run:
            delete_migration_columns(excel, dry_run)
            excel.save()
            print("\n✓ Excel 文件已保存（P-W 列已删除）")
    
    return stats


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SSBR Excel 数据迁移工具')
    parser.add_argument('--dry-run', action='store_true', help='只打印操作，不实际执行')
    parser.add_argument('--delete-columns', action='store_true', help='迁移后删除 Excel P-W 列')
    args = parser.parse_args()
    
    print("=" * 60)
    print("SSBR Excel 数据迁移工具")
    print("=" * 60)
    
    if args.dry_run:
        print("\n[DRY RUN 模式] 只显示将要执行的操作")
    
    stats = migrate_all(dry_run=args.dry_run, delete_columns=args.delete_columns)
    
    print("\n" + "=" * 60)
    print("迁移统计")
    print("=" * 60)
    print(f"  总样本数: {stats['total_samples']}")
    print(f"  mechanical.md 创建: {stats['mechanical_created']}")
    print(f"  dsc.md 创建: {stats['dsc_created']}")
    print(f"  错误数: {len(stats['errors'])}")
    
    if stats['errors']:
        print("\n错误列表:")
        for err in stats['errors']:
            print(f"  - {err}")
    
    return 0 if not stats['errors'] else 1


if __name__ == '__main__':
    sys.exit(main())
