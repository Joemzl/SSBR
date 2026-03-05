"""
验证工具
用于验证样本 ID、YAML 字段等数据的有效性

Created: 2026-03-05
"""

import re
from typing import Dict, Any, List, Optional, Tuple


# 样本 ID 格式正则
SAMPLE_ID_PATTERN = re.compile(r'^SSBR-\d{3}$')

# 日期格式正则
DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')

# DOI 格式正则
DOI_PATTERN = re.compile(r'^10\.\d+/.*$')

# 有效的解读类型
VALID_INTERPRETATION_TYPES = {'nmr', 'tem', 'mechanical', 'dsc', 'summary'}

# 有效的 Skill 名称
VALID_SKILLS = {
    'ssbr-nmr-interpretation',
    'ssbr-tem-interpretation',
    'ssbr-stress-strain-interpretation',
    'ssbr-payne-interpretation',
    'ssbr-dma-interpretation',
    'ssbr-dsc-interpretation',
    'ssbr-mechanical-interpretation',
    'ssbr-summary-generator',
    'ssbr-recommender',
    'data-migration'  # 迁移脚本标识
}


def validate_sample_id(sample_id: str) -> Tuple[bool, Optional[str]]:
    """
    验证样本 ID 格式
    
    Args:
        sample_id: 样本 ID
        
    Returns:
        (是否有效, 错误消息或 None)
        
    Examples:
        >>> validate_sample_id('SSBR-001')
        (True, None)
        >>> validate_sample_id('SSBR-1')
        (False, '样本 ID 格式错误，应为 SSBR-XXX (XXX 为三位数字)')
    """
    if not sample_id:
        return False, "样本 ID 不能为空"
    
    if not isinstance(sample_id, str):
        return False, f"样本 ID 必须是字符串，实际类型: {type(sample_id).__name__}"
    
    if not SAMPLE_ID_PATTERN.match(sample_id):
        return False, "样本 ID 格式错误，应为 SSBR-XXX (XXX 为三位数字)"
    
    return True, None


def validate_yaml_required_fields(yaml_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    验证 YAML front matter 必填字段
    
    基于 yaml-schema.md 定义的 Base Schema:
    - sample_id: 必填
    - interpretation_type: 必填
    - skill_used: 必填
    - created_at: 必填
    
    Args:
        yaml_data: 解析后的 YAML 字典
        
    Returns:
        (是否有效, 缺失字段列表)
    """
    required_fields = ['sample_id', 'interpretation_type', 'skill_used', 'created_at']
    missing = []
    
    for field in required_fields:
        if field not in yaml_data or yaml_data[field] is None:
            missing.append(field)
    
    return len(missing) == 0, missing


def validate_interpretation_type(type_value: str) -> Tuple[bool, Optional[str]]:
    """
    验证解读类型是否有效
    
    Args:
        type_value: 解读类型值
        
    Returns:
        (是否有效, 错误消息或 None)
    """
    if not type_value:
        return False, "解读类型不能为空"
    
    if type_value not in VALID_INTERPRETATION_TYPES:
        return False, f"无效的解读类型: {type_value}，有效值: {VALID_INTERPRETATION_TYPES}"
    
    return True, None


def validate_skill_name(skill_name: str) -> Tuple[bool, Optional[str]]:
    """
    验证 Skill 名称是否有效
    
    Args:
        skill_name: Skill 名称
        
    Returns:
        (是否有效, 错误消息或 None)
    """
    if not skill_name:
        return False, "Skill 名称不能为空"
    
    if skill_name not in VALID_SKILLS:
        return False, f"未知的 Skill: {skill_name}，有效值: {VALID_SKILLS}"
    
    return True, None


def validate_date_format(date_str: str) -> Tuple[bool, Optional[str]]:
    """
    验证日期格式 (YYYY-MM-DD)
    
    Args:
        date_str: 日期字符串
        
    Returns:
        (是否有效, 错误消息或 None)
    """
    if not date_str:
        return False, "日期不能为空"
    
    if not DATE_PATTERN.match(str(date_str)):
        return False, f"日期格式错误: {date_str}，应为 YYYY-MM-DD"
    
    return True, None


def validate_numeric_range(
    value: float,
    min_val: float,
    max_val: float,
    field_name: str
) -> Tuple[bool, Optional[str]]:
    """
    验证数值范围
    
    Args:
        value: 数值
        min_val: 最小值
        max_val: 最大值
        field_name: 字段名（用于错误消息）
        
    Returns:
        (是否有效, 错误消息或 None)
    """
    if value is None:
        return True, None  # null 值是允许的
    
    try:
        num = float(value)
    except (TypeError, ValueError):
        return False, f"{field_name} 必须是数值，实际值: {value}"
    
    if num < min_val or num > max_val:
        return False, f"{field_name} 超出范围 [{min_val}, {max_val}]，实际值: {num}"
    
    return True, None


def validate_mechanical_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    验证 mechanical.md 的数据字段
    
    基于 yaml-schema.md 定义的数值范围:
    - stress_*: 0-50 MPa
    - tensile_strength: 0-100 MPa
    - elongation: 0-1000 %
    - tan_delta_*: 0-2
    - delta_g_prime: 0-5000 kPa
    
    Args:
        data: YAML 中的 data 字段
        
    Returns:
        (是否有效, 错误消息列表)
    """
    errors = []
    
    # 应力-应变数据
    for field in ['stress_100', 'stress_200', 'stress_300']:
        if field in data and data[field]:
            value = data[field].get('value') if isinstance(data[field], dict) else data[field]
            valid, msg = validate_numeric_range(value, 0, 50, field)
            if not valid:
                errors.append(msg)
    
    # 拉伸强度
    if 'tensile_strength' in data and data['tensile_strength']:
        value = data['tensile_strength'].get('value') if isinstance(data['tensile_strength'], dict) else data['tensile_strength']
        valid, msg = validate_numeric_range(value, 0, 100, 'tensile_strength')
        if not valid:
            errors.append(msg)
    
    # 断裂伸长率
    if 'elongation' in data and data['elongation']:
        value = data['elongation'].get('value') if isinstance(data['elongation'], dict) else data['elongation']
        valid, msg = validate_numeric_range(value, 0, 1000, 'elongation')
        if not valid:
            errors.append(msg)
    
    # DMA 数据
    for field in ['tan_delta_0c', 'tan_delta_60c']:
        if field in data and data[field]:
            value = data[field].get('value') if isinstance(data[field], dict) else data[field]
            valid, msg = validate_numeric_range(value, 0, 2, field)
            if not valid:
                errors.append(msg)
    
    # Payne 效应
    if 'delta_g_prime' in data and data['delta_g_prime']:
        value = data['delta_g_prime'].get('value') if isinstance(data['delta_g_prime'], dict) else data['delta_g_prime']
        valid, msg = validate_numeric_range(value, 0, 5000, 'delta_g_prime')
        if not valid:
            errors.append(msg)
    
    return len(errors) == 0, errors


def validate_dsc_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    验证 dsc.md 的数据字段
    
    Args:
        data: YAML 中的 data 字段
        
    Returns:
        (是否有效, 错误消息列表)
    """
    errors = []
    
    # Tg
    if 'tg' in data and data['tg']:
        value = data['tg'].get('value') if isinstance(data['tg'], dict) else data['tg']
        valid, msg = validate_numeric_range(value, -100, 50, 'tg')
        if not valid:
            errors.append(msg)
    
    return len(errors) == 0, errors


def validate_interpretation_file(yaml_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    综合验证解读文档
    
    Args:
        yaml_data: 解析后的完整 YAML 字典
        
    Returns:
        (是否有效, 所有错误消息列表)
    """
    errors = []
    
    # 1. 验证必填字段
    valid, missing = validate_yaml_required_fields(yaml_data)
    if not valid:
        errors.append(f"缺失必填字段: {missing}")
    
    # 2. 验证 sample_id 格式
    if 'sample_id' in yaml_data:
        valid, msg = validate_sample_id(yaml_data['sample_id'])
        if not valid:
            errors.append(msg)
    
    # 3. 验证 interpretation_type
    if 'interpretation_type' in yaml_data:
        valid, msg = validate_interpretation_type(yaml_data['interpretation_type'])
        if not valid:
            errors.append(msg)
    
    # 4. 验证 created_at 格式
    if 'created_at' in yaml_data:
        valid, msg = validate_date_format(str(yaml_data['created_at']))
        if not valid:
            errors.append(msg)
    
    # 5. 验证特定类型的数据
    interpretation_type = yaml_data.get('interpretation_type')
    data = yaml_data.get('data', {})
    
    if interpretation_type == 'mechanical' and data:
        valid, data_errors = validate_mechanical_data(data)
        errors.extend(data_errors)
    
    elif interpretation_type == 'dsc' and data:
        valid, data_errors = validate_dsc_data(data)
        errors.extend(data_errors)
    
    return len(errors) == 0, errors


if __name__ == '__main__':
    print("验证工具模块测试")
    print("="*50)
    
    # 测试 sample_id 验证
    test_ids = ['SSBR-001', 'SSBR-017', 'SSBR-1', 'ssbr-001', 'SSBR001', '']
    print("\n样本 ID 验证:")
    for sid in test_ids:
        valid, msg = validate_sample_id(sid)
        status = "✓" if valid else "✗"
        print(f"  {status} '{sid}': {msg or 'OK'}")
    
    # 测试解读类型验证
    test_types = ['mechanical', 'dsc', 'nmr', 'tem', 'summary', 'invalid']
    print("\n解读类型验证:")
    for t in test_types:
        valid, msg = validate_interpretation_type(t)
        status = "✓" if valid else "✗"
        print(f"  {status} '{t}': {msg or 'OK'}")
