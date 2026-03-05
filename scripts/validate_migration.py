"""
数据迁移验证脚本
对比 Excel 原数据与解读文档中的数据，验证迁移完整性

Created: 2026-03-05
Task: T015
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.excel_handler import ExcelHandler
from utils.yaml_parser import read_interpretation_file

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
INTERPRETATIONS_DIR = DATASET_DIR / "interpretations"
EXCEL_PATH = DATASET_DIR / "数据.xlsx"


def compare_values(excel_val: Any, yaml_val: Any, tolerance: float = 0.001) -> bool:
    """
    比较两个值是否相等
    
    Args:
        excel_val: Excel 中的值
        yaml_val: YAML 中的值
        tolerance: 数值比较容差
        
    Returns:
        是否相等
    """
    # 都是 None 或空
    if (excel_val is None or excel_val == '') and (yaml_val is None or yaml_val == ''):
        return True
    
    # 一个是 None，另一个不是
    if excel_val is None or yaml_val is None:
        return False
    
    # 尝试数值比较
    try:
        excel_num = float(excel_val)
        yaml_num = float(yaml_val)
        return abs(excel_num - yaml_num) < tolerance
    except (TypeError, ValueError):
        pass
    
    # 字符串比较
    return str(excel_val).strip() == str(yaml_val).strip()


def validate_mechanical(
    sample_id: str,
    excel_data: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    """
    验证 mechanical.md 数据
    
    Args:
        sample_id: 样本 ID
        excel_data: Excel 中的迁移数据
        
    Returns:
        (是否通过, 错误列表)
    """
    errors = []
    
    mech_path = INTERPRETATIONS_DIR / sample_id / "mechanical.md"
    
    if not mech_path.exists():
        # 检查 Excel 中是否有数据
        mech_data = excel_data.get('mechanical', {})
        has_data = any(v is not None for v in mech_data.values())
        
        if has_data:
            errors.append(f"mechanical.md 不存在，但 Excel 中有数据")
        
        return len(errors) == 0, errors
    
    # 读取解读文档
    try:
        doc = read_interpretation_file(mech_path)
        yaml_data = doc['yaml'].get('data', {})
    except Exception as e:
        errors.append(f"读取 mechanical.md 失败: {e}")
        return False, errors
    
    # 对比字段
    field_mapping = [
        ('stress_100', 'stress_100'),
        ('stress_200', 'stress_200'),
        ('stress_300', 'stress_300'),
        ('tensile_strength', 'tensile_strength'),
        ('elongation', 'elongation'),
        ('mechanical_source', 'mechanical_source'),
    ]
    
    mech_excel = excel_data.get('mechanical', {})
    
    for excel_field, yaml_field in field_mapping:
        excel_val = mech_excel.get(excel_field)
        
        if yaml_field in yaml_data:
            yaml_entry = yaml_data[yaml_field]
            if isinstance(yaml_entry, dict):
                yaml_val = yaml_entry.get('value')
            else:
                yaml_val = yaml_entry
        else:
            yaml_val = None
        
        if not compare_values(excel_val, yaml_val):
            errors.append(
                f"mechanical.{excel_field}: Excel={excel_val}, YAML={yaml_val}"
            )
    
    return len(errors) == 0, errors


def validate_dsc(
    sample_id: str,
    excel_data: Dict[str, Any]
) -> Tuple[bool, List[str]]:
    """
    验证 dsc.md 数据
    
    Args:
        sample_id: 样本 ID
        excel_data: Excel 中的迁移数据
        
    Returns:
        (是否通过, 错误列表)
    """
    errors = []
    
    dsc_path = INTERPRETATIONS_DIR / sample_id / "dsc.md"
    
    if not dsc_path.exists():
        # 检查 Excel 中是否有数据
        dsc_data = excel_data.get('dsc', {})
        has_data = any(v is not None for v in dsc_data.values())
        
        if has_data:
            errors.append(f"dsc.md 不存在，但 Excel 中有数据")
        
        return len(errors) == 0, errors
    
    # 读取解读文档
    try:
        doc = read_interpretation_file(dsc_path)
        yaml_data = doc['yaml'].get('data', {})
    except Exception as e:
        errors.append(f"读取 dsc.md 失败: {e}")
        return False, errors
    
    # 对比字段
    field_mapping = [
        ('tg', 'tg'),
        ('thermal_source', 'thermal_source'),
    ]
    
    dsc_excel = excel_data.get('dsc', {})
    
    for excel_field, yaml_field in field_mapping:
        excel_val = dsc_excel.get(excel_field)
        
        if yaml_field in yaml_data:
            yaml_entry = yaml_data[yaml_field]
            if isinstance(yaml_entry, dict):
                yaml_val = yaml_entry.get('value')
            else:
                yaml_val = yaml_entry
        else:
            yaml_val = None
        
        if not compare_values(excel_val, yaml_val):
            errors.append(
                f"dsc.{excel_field}: Excel={excel_val}, YAML={yaml_val}"
            )
    
    return len(errors) == 0, errors


def validate_sample(
    sample_id: str,
    excel_handler: ExcelHandler
) -> Dict[str, Any]:
    """
    验证单个样本的迁移数据
    
    Args:
        sample_id: 样本 ID
        excel_handler: Excel 处理器
        
    Returns:
        验证结果
    """
    result = {
        'sample_id': sample_id,
        'mechanical_valid': False,
        'dsc_valid': False,
        'errors': []
    }
    
    # 获取 Excel 数据
    excel_data = excel_handler.get_migration_data(sample_id)
    if not excel_data:
        result['errors'].append(f"未在 Excel 中找到样本 {sample_id}")
        return result
    
    # 验证 mechanical
    valid, errors = validate_mechanical(sample_id, excel_data)
    result['mechanical_valid'] = valid
    result['errors'].extend(errors)
    
    # 验证 dsc
    valid, errors = validate_dsc(sample_id, excel_data)
    result['dsc_valid'] = valid
    result['errors'].extend(errors)
    
    return result


def validate_all() -> Dict[str, Any]:
    """
    验证所有样本的迁移数据
    
    Returns:
        验证统计信息
    """
    stats = {
        'total_samples': 0,
        'passed': 0,
        'failed': 0,
        'details': []
    }
    
    with ExcelHandler(EXCEL_PATH) as excel:
        samples = excel.get_all_samples()
        stats['total_samples'] = len(samples)
        
        for sample in samples:
            sample_id = sample.get('sample_id')
            if not sample_id:
                continue
            
            result = validate_sample(sample_id, excel)
            stats['details'].append(result)
            
            if result['mechanical_valid'] and result['dsc_valid'] and not result['errors']:
                stats['passed'] += 1
            else:
                stats['failed'] += 1
    
    return stats


def main():
    """主函数"""
    print("=" * 60)
    print("SSBR 数据迁移验证工具")
    print("=" * 60)
    
    if not EXCEL_PATH.exists():
        print(f"\n错误: Excel 文件不存在: {EXCEL_PATH}")
        return 1
    
    stats = validate_all()
    
    print(f"\n验证结果:")
    print(f"  总样本数: {stats['total_samples']}")
    print(f"  通过: {stats['passed']}")
    print(f"  失败: {stats['failed']}")
    
    # 打印详细错误
    failed_samples = [d for d in stats['details'] if d['errors']]
    
    if failed_samples:
        print("\n" + "-" * 60)
        print("失败详情:")
        for detail in failed_samples:
            print(f"\n  {detail['sample_id']}:")
            for err in detail['errors']:
                print(f"    - {err}")
    else:
        print("\n✓ 所有样本数据验证通过！")
    
    # 打印成功样本
    passed_samples = [d for d in stats['details'] if not d['errors']]
    if passed_samples:
        print("\n" + "-" * 60)
        print(f"通过验证的样本 ({len(passed_samples)} 个):")
        for detail in passed_samples:
            status_mech = "✓" if detail['mechanical_valid'] else "-"
            status_dsc = "✓" if detail['dsc_valid'] else "-"
            print(f"  {detail['sample_id']}: mechanical={status_mech}, dsc={status_dsc}")
    
    return 0 if stats['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
