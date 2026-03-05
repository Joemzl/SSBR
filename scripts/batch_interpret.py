"""
批量解读脚本
调度 Skills 为样本生成解读文档

Created: 2026-03-05
Tasks: T016.1, T016.2, T016.3
"""

import sys
from pathlib import Path
from datetime import date
from typing import Dict, Any, List, Optional

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.yaml_parser import write_interpretation_file
from utils.excel_handler import ExcelHandler

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
INTERPRETATIONS_DIR = DATASET_DIR / "interpretations"
EXCEL_PATH = DATASET_DIR / "数据.xlsx"


def create_placeholder_nmr(
    sample_id: str,
    source_figure: Optional[str] = None,
    source_doi: Optional[str] = None
) -> None:
    """
    为样本创建 nmr.md 占位文件
    
    由于 NMR 数据需要解读文献图谱，此处创建占位文档，
    标注"暂无此项数据"，待后续手动调用 Skill 补充。
    
    Args:
        sample_id: 样本 ID
        source_figure: 核磁谱图图注（如有）
        source_doi: 文献 DOI
    """
    today = date.today().isoformat()
    
    yaml_data = {
        'sample_id': sample_id,
        'interpretation_type': 'nmr',
        'source_figure': source_figure,
        'source_doi': source_doi,
        'skill_used': 'data-migration',
        'created_at': today,
        'data': {
            'functionalization_degree': {
                'value': None,
                'unit': 'wt%',
                'source': '暂无此项数据'
            },
            'characteristic_peaks': [],
            'vinyl_content': {
                'value': None,
                'unit': '%',
                'source': '暂无此项数据'
            }
        }
    }
    
    body = f"""# ¹H NMR 核磁共振解读：{sample_id}

> 此文档为占位文件，由数据迁移脚本自动生成。
> 如需完整解读，请使用 `@ssbr-nmr-interpretation` Skill 解读文献核磁谱图。

## 一、官能化确认

**暂无此项数据**

*请使用 Skill 解读文献中的 NMR 谱图：`{source_figure or '未指定'}`*

## 二、SSBR 主链结构

**暂无此项数据**

## 三、溶剂峰和杂质峰

**暂无此项数据**

---

## 文献来源

- **DOI**: {source_doi or '*待补充*'}
- **图注引用**: {source_figure or '*待补充*'}
"""
    
    output_path = INTERPRETATIONS_DIR / sample_id / "nmr.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_interpretation_file(output_path, yaml_data, body)


def create_placeholder_tem(
    sample_id: str,
    source_figure: Optional[str] = None,
    source_doi: Optional[str] = None
) -> None:
    """
    为样本创建 tem.md 占位文件
    
    由于 TEM 数据需要解读文献图像，此处创建占位文档，
    标注"暂无此项数据"，待后续手动调用 Skill 补充。
    
    Args:
        sample_id: 样本 ID
        source_figure: TEM 图注（如有）
        source_doi: 文献 DOI
    """
    today = date.today().isoformat()
    
    yaml_data = {
        'sample_id': sample_id,
        'interpretation_type': 'tem',
        'source_figure': source_figure,
        'source_doi': source_doi,
        'skill_used': 'data-migration',
        'created_at': today,
        'data': {
            'domain_size': {
                'value': None,
                'range': None,
                'unit': 'nm',
                'source': '暂无此项数据'
            },
            'dispersion_quality': None,
            'morphology': None,
            'scale_bar': None
        }
    }
    
    body = f"""# TEM 透射电镜形貌解读：{sample_id}

> 此文档为占位文件，由数据迁移脚本自动生成。
> 如需完整解读，请使用 `@ssbr-tem-interpretation` Skill 解读文献 TEM 图像。

## 一、微相分离形貌

**暂无此项数据**

*请使用 Skill 解读文献中的 TEM 图像：`{source_figure or '未指定'}`*

## 二、填料分散状态

**暂无此项数据**

## 三、与对照组对比

**暂无此项数据**

## 四、结构-性能关联

**暂无此项数据**

---

## 文献来源

- **DOI**: {source_doi or '*待补充*'}
- **图注引用**: {source_figure or '*待补充*'}
"""
    
    output_path = INTERPRETATIONS_DIR / sample_id / "tem.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_interpretation_file(output_path, yaml_data, body)


def batch_create_nmr(dry_run: bool = False) -> Dict[str, Any]:
    """
    为所有样本批量创建 nmr.md
    
    Args:
        dry_run: 如果为 True，只打印不实际创建
        
    Returns:
        执行统计
    """
    stats = {
        'total': 0,
        'created': 0,
        'skipped': 0,
        'errors': []
    }
    
    with ExcelHandler(EXCEL_PATH) as excel:
        samples = excel.get_all_samples()
        stats['total'] = len(samples)
        
        for sample in samples:
            sample_id = sample.get('sample_id')
            if not sample_id:
                continue
            
            nmr_path = INTERPRETATIONS_DIR / sample_id / "nmr.md"
            
            # 如果已存在则跳过
            if nmr_path.exists():
                stats['skipped'] += 1
                print(f"  跳过 {sample_id}/nmr.md (已存在)")
                continue
            
            source_figure = sample.get('nmr_figure')
            source_doi = sample.get('doi')
            
            if dry_run:
                print(f"  [DRY RUN] 将创建 {sample_id}/nmr.md")
            else:
                try:
                    create_placeholder_nmr(sample_id, source_figure, source_doi)
                    stats['created'] += 1
                    print(f"  ✓ 创建 {sample_id}/nmr.md")
                except Exception as e:
                    stats['errors'].append(f"{sample_id}: {e}")
                    print(f"  ✗ 错误 {sample_id}: {e}")
    
    return stats


def batch_create_tem(dry_run: bool = False) -> Dict[str, Any]:
    """
    为所有样本批量创建 tem.md
    
    Args:
        dry_run: 如果为 True，只打印不实际创建
        
    Returns:
        执行统计
    """
    stats = {
        'total': 0,
        'created': 0,
        'skipped': 0,
        'errors': []
    }
    
    with ExcelHandler(EXCEL_PATH) as excel:
        samples = excel.get_all_samples()
        stats['total'] = len(samples)
        
        for sample in samples:
            sample_id = sample.get('sample_id')
            if not sample_id:
                continue
            
            tem_path = INTERPRETATIONS_DIR / sample_id / "tem.md"
            
            # 如果已存在则跳过
            if tem_path.exists():
                stats['skipped'] += 1
                print(f"  跳过 {sample_id}/tem.md (已存在)")
                continue
            
            source_figure = sample.get('tem_figure')
            source_doi = sample.get('doi')
            
            if dry_run:
                print(f"  [DRY RUN] 将创建 {sample_id}/tem.md")
            else:
                try:
                    create_placeholder_tem(sample_id, source_figure, source_doi)
                    stats['created'] += 1
                    print(f"  ✓ 创建 {sample_id}/tem.md")
                except Exception as e:
                    stats['errors'].append(f"{sample_id}: {e}")
                    print(f"  ✗ 错误 {sample_id}: {e}")
    
    return stats


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SSBR 批量解读文档生成工具')
    parser.add_argument('--dry-run', action='store_true', help='只打印操作，不实际执行')
    parser.add_argument('--type', choices=['nmr', 'tem', 'all'], default='all',
                        help='生成的文档类型')
    args = parser.parse_args()
    
    print("=" * 60)
    print("SSBR 批量解读文档生成工具")
    print("=" * 60)
    
    if args.dry_run:
        print("\n[DRY RUN 模式] 只显示将要执行的操作")
    
    total_stats = {
        'nmr': None,
        'tem': None
    }
    
    if args.type in ['nmr', 'all']:
        print("\n" + "-" * 40)
        print("生成 NMR 解读文档...")
        total_stats['nmr'] = batch_create_nmr(dry_run=args.dry_run)
    
    if args.type in ['tem', 'all']:
        print("\n" + "-" * 40)
        print("生成 TEM 解读文档...")
        total_stats['tem'] = batch_create_tem(dry_run=args.dry_run)
    
    # 打印统计
    print("\n" + "=" * 60)
    print("执行统计")
    print("=" * 60)
    
    for doc_type, stats in total_stats.items():
        if stats:
            print(f"\n{doc_type.upper()}:")
            print(f"  总样本数: {stats['total']}")
            print(f"  创建: {stats['created']}")
            print(f"  跳过: {stats['skipped']}")
            print(f"  错误: {len(stats['errors'])}")
    
    # 检查是否有错误
    all_errors = []
    for stats in total_stats.values():
        if stats and stats['errors']:
            all_errors.extend(stats['errors'])
    
    return 0 if not all_errors else 1


if __name__ == '__main__':
    sys.exit(main())
