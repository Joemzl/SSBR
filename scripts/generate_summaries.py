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


import re


def extract_from_markdown_table(body: str) -> Dict[str, Any]:
    """
    从 Markdown 正文表格中提取数值数据
    
    支持的表格格式：
    | 参数 | 数值 | ... |
    | 拉伸强度 | 24.7 MPa | ... |
    
    Args:
        body: Markdown 正文内容
        
    Returns:
        提取的数据字典
    """
    result = {}
    
    # 匹配模式：提取表格行中的数值
    patterns = [
        # 拉伸强度
        (r'拉伸强度[^|]*\|\s*([\d.]+)\s*(?:MPa)?', 'tensile_strength'),
        (r'tensile\s*strength[^|]*\|\s*([\d.]+)', 'tensile_strength'),
        # 断裂伸长率
        (r'断裂伸长率[^|]*\|\s*([\d.]+)\s*%?', 'elongation'),
        (r'elongation[^|]*\|\s*([\d.]+)', 'elongation'),
        # 100% 定伸应力
        (r'100%?\s*(?:定伸应力|模量)[^|]*\|\s*([\d.]+)', 'stress_100'),
        (r'M100[^|]*\|\s*([\d.]+)', 'stress_100'),
        # 200% 定伸应力
        (r'200%?\s*(?:定伸应力|模量)[^|]*\|\s*([\d.]+)', 'stress_200'),
        (r'M200[^|]*\|\s*([\d.]+)', 'stress_200'),
        # 300% 定伸应力
        (r'300%?\s*(?:定伸应力|模量)[^|]*\|\s*([\d.]+)', 'stress_300'),
        (r'M300[^|]*\|\s*([\d.]+)', 'stress_300'),
        # 结合橡胶含量
        (r'结合橡胶[^|]*\|\s*([\d.]+)', 'bound_rubber'),
        (r'bound\s*rubber[^|]*\|\s*([\d.]+)', 'bound_rubber'),
        # tanδ 相关
        (r'tanδ@0°?C[^|]*\|\s*([\d.]+)', 'tan_delta_0'),
        (r'tanδ@60°?C[^|]*\|\s*([\d.]+)', 'tan_delta_60'),
        # Tg
        (r'Tg[^|]*\|\s*(-?[\d.]+)\s*°?C?', 'tg_from_mech'),
    ]
    
    for pattern, field in patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match and field not in result:
            try:
                result[field] = float(match.group(1))
            except ValueError:
                pass
    
    return result


def extract_qualitative_features(body: str) -> Dict[str, str]:
    """
    从 Markdown 正文描述中提取定性特征
    
    匹配关键词：提高、降低、改善、增强等
    
    Args:
        body: Markdown 正文内容
        
    Returns:
        提取的定性描述字典
    """
    result = {}
    
    # 定性描述模式
    qualitative_patterns = [
        # 拉伸强度
        (r'拉伸强度[^。，\n]*?(提高|提升|增加|增强|改善)[^。，\n]*?(\d+(?:\.\d+)?%)?', 
         'tensile_strength_qual', '拉伸强度提升'),
        (r'拉伸强度[^。，\n]*?(降低|下降|减少)', 
         'tensile_strength_qual', '拉伸强度下降'),
        # 断裂伸长率
        (r'(?:断裂)?伸长率[^。，\n]*?(提高|提升|增加|改善)[^。，\n]*?(\d+(?:\.\d+)?%)?', 
         'elongation_qual', '断裂伸长率提升'),
        (r'(?:断裂)?伸长率[^。，\n]*?(保持|维持)', 
         'elongation_qual', '断裂伸长率保持'),
        # 模量/定伸应力
        (r'(?:模量|定伸应力)[^。，\n]*?(提高|提升|增加)[^。，\n]*?(\d+(?:\.\d+)?%)?', 
         'modulus_qual', '模量提升'),
        # 分散性
        (r'分散[^。，\n]*?(改善|提高|提升|良好|优异)', 
         'dispersion_qual', '填料分散性改善'),
        (r'(?:白炭黑|炭黑|填料)[^。，\n]*?分散[^。，\n]*?(改善|提高|良好)', 
         'dispersion_qual', '填料分散性改善'),
        # Payne 效应
        (r'Payne\s*效应[^。，\n]*?(降低|减小|下降)', 
         'payne_qual', 'Payne 效应降低（分散性改善）'),
        (r'Payne\s*效应[^。，\n]*?(明显|显著)', 
         'payne_qual', 'Payne 效应明显'),
        # 界面
        (r'界面[^。，\n]*?(增强|改善|提高|强)', 
         'interface_qual', '填料-橡胶界面作用增强'),
        (r'交联密度[^。，\n]*?(提高|增加|增强)', 
         'interface_qual', '交联密度提高'),
        # 耐磨性
        (r'耐磨[^。，\n]*?(改善|提高|提升|优异|良好)', 
         'wear_qual', '耐磨性改善'),
        # 湿抓
        (r'湿[^。，\n]*?抓[^。，\n]*?(提高|改善|良好|优异)', 
         'wet_grip_qual', '湿地抓地力改善'),
        (r'湿滑[^。，\n]*?(制动|抓地)[^。，\n]*?(提高|改善)', 
         'wet_grip_qual', '湿地抓地力改善'),
        # 滚阻
        (r'滚动阻力[^。，\n]*?(降低|减小|改善)', 
         'rolling_resistance_qual', '滚动阻力降低'),
        (r'滚阻[^。，\n]*?(降低|减小)', 
         'rolling_resistance_qual', '滚动阻力降低'),
        # 强度与韧性同时提升
        (r'强度[^。，\n]*韧性[^。，\n]*?(同时|兼顾|平衡)', 
         'strength_toughness_qual', '强度与韧性同时提升'),
    ]
    
    for pattern, field, default_desc in qualitative_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match and field not in result:
            # 尝试提取百分比
            groups = match.groups()
            if len(groups) >= 2 and groups[1]:
                result[field] = f"{default_desc} {groups[1]}"
            else:
                result[field] = default_desc
    
    return result


def extract_mechanical_data(sample_id: str) -> Dict[str, Any]:
    """
    从 mechanical.md 提取关键数据（增强版）
    
    数据来源优先级：
    1. YAML data: 字段中的绝对值
    2. YAML data: 字段中的相对描述
    3. 正文 Markdown 表格中的数值
    4. 正文描述中的定性特征
    
    Args:
        sample_id: 样本 ID
        
    Returns:
        提取的数据字典，包含绝对值、相对数据和定性描述
    """
    mech_path = INTERPRETATIONS_DIR / sample_id / "mechanical.md"
    
    if not mech_path.exists():
        return {}
    
    try:
        doc = read_interpretation_file(mech_path)
        yaml_data = doc['yaml'].get('data', {})
        body = doc['body'] or ""
        
        result = {}
        
        # ========== 第一优先级：从 YAML 提取 ==========
        for field in ['stress_100', 'stress_200', 'stress_300', 'tensile_strength', 'elongation']:
            if field in yaml_data:
                entry = yaml_data[field]
                if isinstance(entry, dict):
                    # 优先使用绝对值
                    if entry.get('value') is not None:
                        result[field] = entry.get('value')
                    # 其次使用相对描述
                    elif entry.get('description'):
                        result[f'{field}_desc'] = entry.get('description')
                else:
                    result[field] = entry
        
        # 结合橡胶含量
        if 'bound_rubber' in yaml_data:
            br_entry = yaml_data['bound_rubber']
            if isinstance(br_entry, dict) and br_entry.get('value') is not None:
                result['bound_rubber'] = br_entry.get('value')
                result['bound_rubber_unit'] = br_entry.get('unit', '%')
        
        # Payne 效应
        if 'payne_effect' in yaml_data:
            payne_entry = yaml_data['payne_effect']
            if isinstance(payne_entry, dict) and payne_entry.get('description'):
                result['payne_effect_desc'] = payne_entry.get('description')
        
        # 提取来源
        result['mechanical_source'] = yaml_data.get('mechanical_source')
        
        # ========== 第二优先级：从正文表格提取 ==========
        table_data = extract_from_markdown_table(body)
        for field, value in table_data.items():
            # 只填补缺失的字段
            if field not in result and f'{field}_desc' not in result:
                result[field] = value
        
        # ========== 第三优先级：从正文描述提取定性特征 ==========
        qualitative_data = extract_qualitative_features(body)
        
        # 如果没有定量数据，使用定性描述
        if 'tensile_strength' not in result and 'tensile_strength_desc' not in result:
            if 'tensile_strength_qual' in qualitative_data:
                result['tensile_strength_qual'] = qualitative_data['tensile_strength_qual']
        
        if 'elongation' not in result and 'elongation_desc' not in result:
            if 'elongation_qual' in qualitative_data:
                result['elongation_qual'] = qualitative_data['elongation_qual']
        
        # 添加其他定性特征（用于核心性能特点）
        for qual_field in ['dispersion_qual', 'payne_qual', 'interface_qual', 
                           'wear_qual', 'wet_grip_qual', 'rolling_resistance_qual',
                           'modulus_qual', 'strength_toughness_qual']:
            if qual_field in qualitative_data:
                result[qual_field] = qualitative_data[qual_field]
        
        # 提取正文摘要（核心发现部分）
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
    生成核心性能特点列表（增强版）
    
    数据来源优先级：
    1. 绝对数值 → 生成定量评价
    2. 相对描述 → 生成相对评价
    3. 定性特征 → 生成定性评价
    
    Args:
        mech_data: 力学数据
        dsc_data: 热学数据
        
    Returns:
        特点列表
    """
    features = []
    
    def safe_float(val, default=None):
        """安全转换为浮点数"""
        if val is None:
            return default
        try:
            return float(val)
        except (ValueError, TypeError):
            return default
    
    # ========== 拉伸强度 ==========
    ts = safe_float(mech_data.get('tensile_strength'))
    ts_desc = mech_data.get('tensile_strength_desc')
    ts_qual = mech_data.get('tensile_strength_qual')
    
    if ts is not None:
        rating = "良好" if ts > 10 else "一般"
        features.append({
            'title': '拉伸强度',
            'rating': rating,
            'description': f"拉伸强度达到 {ts} MPa，{rating}的力学强度。"
        })
    elif ts_desc:
        features.append({
            'title': '拉伸强度',
            'rating': '改善',
            'description': f"拉伸强度{ts_desc}。"
        })
    elif ts_qual:
        features.append({
            'title': '拉伸强度',
            'rating': '改善',
            'description': f"{ts_qual}。"
        })
    
    # ========== 断裂伸长率 ==========
    el = safe_float(mech_data.get('elongation'))
    el_desc = mech_data.get('elongation_desc')
    el_qual = mech_data.get('elongation_qual')
    
    if el is not None:
        rating = "优秀" if el > 400 else ("良好" if el > 300 else "一般")
        features.append({
            'title': '断裂伸长率',
            'rating': rating,
            'description': f"断裂伸长率为 {el}%，展现出{rating}的延展性。"
        })
    elif el_desc:
        features.append({
            'title': '断裂伸长率',
            'rating': '改善',
            'description': f"断裂伸长率{el_desc}。"
        })
    elif el_qual:
        features.append({
            'title': '断裂伸长率',
            'rating': '改善',
            'description': f"{el_qual}。"
        })
    
    # ========== 玻璃化转变温度 ==========
    tg = safe_float(dsc_data.get('tg'))
    # 也检查从 mechanical 提取的 Tg
    if tg is None:
        tg = safe_float(mech_data.get('tg_from_mech'))
    
    if tg is not None:
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
    
    # ========== 结合橡胶含量 ==========
    br = safe_float(mech_data.get('bound_rubber'))
    if br is not None:
        if br > 50:
            rating = "优秀"
            desc = "界面结合能力强"
        elif br > 30:
            rating = "良好"
            desc = "界面结合良好"
        else:
            rating = "一般"
            desc = "界面结合一般"
        
        features.append({
            'title': '结合橡胶含量',
            'rating': rating,
            'description': f"结合橡胶含量为 {br}%，{desc}。"
        })
    
    # ========== 定性特征（从正文描述提取） ==========
    
    # 填料分散性
    disp_qual = mech_data.get('dispersion_qual')
    payne_qual = mech_data.get('payne_qual')
    if disp_qual:
        features.append({
            'title': '填料分散性',
            'rating': '改善',
            'description': f"{disp_qual}。"
        })
    elif payne_qual and 'Payne 效应降低' in payne_qual:
        features.append({
            'title': '填料分散性',
            'rating': '改善',
            'description': f"{payne_qual}。"
        })
    
    # 界面作用
    interface_qual = mech_data.get('interface_qual')
    if interface_qual:
        features.append({
            'title': '界面性能',
            'rating': '增强',
            'description': f"{interface_qual}。"
        })
    
    # 耐磨性
    wear_qual = mech_data.get('wear_qual')
    if wear_qual:
        features.append({
            'title': '耐磨性',
            'rating': '改善',
            'description': f"{wear_qual}。"
        })
    
    # 湿地抓地力
    wet_qual = mech_data.get('wet_grip_qual')
    tan_0 = safe_float(mech_data.get('tan_delta_0'))
    if wet_qual:
        features.append({
            'title': '湿地抓地力',
            'rating': '改善',
            'description': f"{wet_qual}。"
        })
    elif tan_0 is not None and tan_0 > 0.3:
        features.append({
            'title': '湿地抓地力',
            'rating': '良好',
            'description': f"tanδ@0°C = {tan_0}，有利于湿滑路面制动。"
        })
    
    # 滚动阻力
    rr_qual = mech_data.get('rolling_resistance_qual')
    tan_60 = safe_float(mech_data.get('tan_delta_60'))
    if rr_qual:
        features.append({
            'title': '滚动阻力',
            'rating': '降低',
            'description': f"{rr_qual}。"
        })
    elif tan_60 is not None and tan_60 < 0.15:
        features.append({
            'title': '滚动阻力',
            'rating': '良好',
            'description': f"tanδ@60°C = {tan_60}，滚动阻力较低，有利于节能。"
        })
    
    # 模量
    mod_qual = mech_data.get('modulus_qual')
    if mod_qual and not any(f['title'] == '拉伸强度' for f in features):
        features.append({
            'title': '模量',
            'rating': '提升',
            'description': f"{mod_qual}。"
        })
    
    # 强度-韧性平衡
    st_qual = mech_data.get('strength_toughness_qual')
    if st_qual:
        features.append({
            'title': '综合性能',
            'rating': '优秀',
            'description': f"{st_qual}，在提升力学强度的同时保持良好韧性。"
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
    def safe_float(val, default=None):
        """安全转换为浮点数"""
        if val is None:
            return default
        try:
            return float(val)
        except (ValueError, TypeError):
            return default
    
    scenarios = []
    
    # 根据应用场景
    application = metadata.get('application')
    if application:
        scenarios.append(f"✅ {application}")
    
    # 根据性能数据推断
    el = safe_float(mech_data.get('elongation'))
    if el is not None and el > 400:
        scenarios.append("✅ 需要高延展性的应用场景")
    
    tg = safe_float(dsc_data.get('tg'))
    if tg is not None and tg < -30:
        scenarios.append("✅ 低温环境应用")
    
    if not scenarios:
        scenarios.append("✅ 通用橡胶制品")
    
    # 添加注意事项
    if tg is not None and tg > -20:
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
    
    # 力学数据 - 支持绝对值、相对描述和定性描述
    for field, label in [
        ('stress_100', '100%定伸应力'),
        ('stress_200', '200%定伸应力'),
        ('stress_300', '300%定伸应力'),
        ('tensile_strength', '拉伸强度'),
        ('elongation', '断裂伸长率'),
    ]:
        val = mech_data.get(field)
        desc = mech_data.get(f'{field}_desc')  # 相对描述（如"相比基准提高 43.8%"）
        qual = mech_data.get(f'{field}_qual')  # 定性描述（如"拉伸强度提升"）
        unit = '%' if field == 'elongation' else 'MPa'
        
        if val is not None:
            # 有绝对值
            lines.append(f"| 力学性能 | {label} | {val} | {unit} | - |")
        elif desc:
            # 有相对描述
            lines.append(f"| 力学性能 | {label} | {desc} | 相对 | - |")
        elif qual:
            # 有定性描述
            lines.append(f"| 力学性能 | {label} | {qual} | 定性 | - |")
        else:
            lines.append(f"| 力学性能 | {label} | - | {unit} | - |")
    
    # 热学数据
    tg_val = dsc_data.get('tg') or dsc_data.get('tg_range') or mech_data.get('tg_from_mech') or '-'
    lines.append(f"| 热学性能 | Tg | {tg_val} | ℃ | - |")
    
    # 额外指标：结合橡胶含量
    if mech_data.get('bound_rubber') is not None:
        br_val = mech_data.get('bound_rubber')
        br_unit = mech_data.get('bound_rubber_unit', '%')
        lines.append(f"| 界面性能 | 结合橡胶含量 | {br_val} | {br_unit} | - |")
    
    # 动态力学指标（从正文表格提取）
    if mech_data.get('tan_delta_0') is not None:
        lines.append(f"| 动态性能 | tanδ@0°C | {mech_data.get('tan_delta_0')} | - | 湿抓 |")
    if mech_data.get('tan_delta_60') is not None:
        lines.append(f"| 动态性能 | tanδ@60°C | {mech_data.get('tan_delta_60')} | - | 滚阻 |")
    
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
