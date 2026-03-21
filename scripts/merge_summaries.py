"""
Summary 综合档案合并脚本

将旧版 summary.md（丰富的叙事性内容）与新版结构化数据合并，
生成既有丰富解读内容，又便于 RAG 检索的综合档案。

功能：
1. 从 Git 恢复旧版 summary.md
2. 提取旧版的「研究亮点」「核心发现」「改性机理」「应用前景」等章节
3. 与新版的结构化数据（性能指标表、官能化信息等）合并
4. 生成统一格式的新 summary.md

Created: 2026-03-21
"""

import sys
import subprocess
import re
from pathlib import Path
from datetime import date
from typing import Dict, Any, List, Optional, Tuple

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.excel_handler import ExcelHandler
from utils.yaml_parser import read_interpretation_file, write_interpretation_file, parse_yaml_frontmatter

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
INTERPRETATIONS_DIR = DATASET_DIR / "interpretations"
EXCEL_PATH = DATASET_DIR / "数据.xlsx"

# 需要从旧版保留的章节（叙事性内容）
# 使用 \n## 作为章节分隔符，确保匹配到完整内容
PRESERVED_SECTION_PATTERNS = [
    # (正则模式, 章节名, 是否必须)
    (r'##\s*研究亮点\s*\n(.*?)(?=\n## |\Z)', '研究亮点', False),
    (r'##\s*核心发现\s*\n(.*?)(?=\n## |\Z)', '核心发现', False),
    (r'##\s*改性机理\s*\n(.*?)(?=\n## |\Z)', '改性机理', False),
    (r'##\s*应用前景\s*\n(.*?)(?=\n## |\Z)', '应用前景', False),
    (r'##\s*技术要点摘要\s*\n(.*?)(?=\n## |\Z)', '技术要点摘要', False),
    (r'##\s*核心技术创新\s*\n(.*?)(?=\n## |\Z)', '核心技术创新', False),
    (r'##\s*性能优势总结\s*\n(.*?)(?=\n## |\Z)', '性能优势总结', False),
    (r'##\s*样本概述\s*\n(.*?)(?=\n## |\Z)', '样本概述', False),
    (r'##\s*材料信息\s*\n(.*?)(?=\n## |\Z)', '材料信息', False),
    (r'##\s*界面作用机制\s*\n(.*?)(?=\n## |\Z)', '界面作用机制', False),
    (r'##\s*轮胎应用价值\s*\n(.*?)(?=\n## |\Z)', '轮胎应用价值', False),
    # 也提取旧版的核心性能特点（如果有详细内容）
    (r'##\s*核心性能特点\s*\n(.*?)(?=\n## |\Z)', '核心性能特点_old', False),
    # 一、二、三... 格式的章节（如 SSBR-015）
    (r'##\s*一、样本概述\s*\n(.*?)(?=\n## |\Z)', '样本概述', False),
    (r'##\s*二、聚合物结构\s*\n(.*?)(?=\n## |\Z)', '聚合物结构', False),
    (r'##\s*三、关键性能数据\s*\n(.*?)(?=\n## |\Z)', '关键性能数据', False),
    (r'##\s*四、核心技术创新\s*\n(.*?)(?=\n## |\Z)', '核心技术创新', False),
    (r'##\s*五、性能优势总结\s*\n(.*?)(?=\n## |\Z)', '性能优势总结', False),
    (r'##\s*六、应用前景\s*\n(.*?)(?=\n## |\Z)', '应用前景', False),
]


def get_old_summary_from_git(sample_id: str) -> Optional[str]:
    """
    从 Git 历史获取旧版 summary.md 内容
    
    Args:
        sample_id: 样本 ID
        
    Returns:
        旧版 summary.md 内容，如果不存在则返回 None
    """
    file_path = f"dataset/interpretations/{sample_id}/summary.md"
    
    try:
        result = subprocess.run(
            ['git', 'show', f'HEAD:{file_path}'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=PROJECT_ROOT
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except Exception as e:
        print(f"  警告: 无法从 Git 获取 {sample_id} 的旧版内容: {e}")
        return None


def extract_preserved_sections(content: str) -> Dict[str, str]:
    """
    从旧版 summary.md 中提取需要保留的章节
    
    Args:
        content: 旧版 summary.md 完整内容
        
    Returns:
        提取的章节字典 {章节名: 章节内容}
    """
    sections = {}
    
    for pattern, section_name, _ in PRESERVED_SECTION_PATTERNS:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            section_content = match.group(1).strip()
            # 过滤掉太短的内容（可能是空章节）
            if len(section_content) > 50:
                sections[section_name] = section_content
    
    return sections


def extract_old_yaml(content: str) -> Dict[str, Any]:
    """
    从旧版 summary.md 中提取 YAML front matter
    
    Args:
        content: 旧版 summary.md 完整内容
        
    Returns:
        YAML 数据字典
    """
    try:
        yaml_data, _ = parse_yaml_frontmatter(content)
        return yaml_data or {}
    except Exception:
        return {}


def extract_one_sentence_summary(content: str) -> Optional[str]:
    """
    从旧版 summary.md 中提取一句话总结
    
    Args:
        content: 旧版 summary.md 完整内容
        
    Returns:
        一句话总结
    """
    # 尝试多种格式
    patterns = [
        r'##\s*一句话总结\s*\n+(.+?)(?=\n---|\n##|\Z)',
        r'>\s*\*\*一句话总结\*\*:\s*(.+?)(?=\n)',
        r'>\s*一句话总结:\s*(.+?)(?=\n)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            summary = match.group(1).strip()
            # 清理 Markdown 格式
            summary = re.sub(r'\*\*(.+?)\*\*', r'\1', summary)
            if len(summary) > 10 and len(summary) < 200:
                return summary
    
    return None


def extract_old_performance_features(content: str) -> List[Dict[str, str]]:
    """
    从旧版 summary.md 中提取核心性能特点（详细版）
    
    Args:
        content: 旧版 summary.md 完整内容
        
    Returns:
        性能特点列表
    """
    features = []
    
    # 匹配 ### 【特点标题】评价：xxx 格式
    pattern = r'###\s*【(.+?)】\s*评价[：:]\s*(\S+)\s*\n+(.*?)(?=\n###|\n##|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for title, rating, description in matches:
        desc = description.strip()
        if len(desc) > 20:  # 有实质内容
            features.append({
                'title': title,
                'rating': rating,
                'description': desc
            })
    
    return features


def get_interpretation_status(sample_id: str) -> Dict[str, bool]:
    """检查样本的解读文档完整性"""
    sample_dir = INTERPRETATIONS_DIR / sample_id
    return {
        'mechanical': (sample_dir / 'mechanical.md').exists(),
        'dsc': (sample_dir / 'dsc.md').exists(),
        'nmr': (sample_dir / 'nmr.md').exists(),
        'tem': (sample_dir / 'tem.md').exists(),
    }


def extract_mechanical_data(sample_id: str) -> Dict[str, Any]:
    """从 mechanical.md 提取关键数据（复用原有函数逻辑）"""
    mech_path = INTERPRETATIONS_DIR / sample_id / "mechanical.md"
    
    if not mech_path.exists():
        return {}
    
    try:
        doc = read_interpretation_file(mech_path)
        yaml_data = doc['yaml'].get('data', {})
        body = doc['body'] or ""
        
        result = {}
        
        # 从 YAML 提取
        for field in ['stress_100', 'stress_200', 'stress_300', 'tensile_strength', 'elongation']:
            if field in yaml_data:
                entry = yaml_data[field]
                if isinstance(entry, dict):
                    if entry.get('value') is not None:
                        result[field] = entry.get('value')
                    elif entry.get('description'):
                        result[f'{field}_desc'] = entry.get('description')
                else:
                    result[field] = entry
        
        # 结合橡胶含量
        if 'bound_rubber' in yaml_data:
            br_entry = yaml_data['bound_rubber']
            if isinstance(br_entry, dict) and br_entry.get('value') is not None:
                result['bound_rubber'] = br_entry.get('value')
        
        # 从正文表格提取
        table_patterns = [
            (r'拉伸强度[^|]*\|\s*([\d.]+)', 'tensile_strength'),
            (r'断裂伸长率[^|]*\|\s*([\d.]+)', 'elongation'),
            (r'100%?\s*(?:定伸应力|模量)[^|]*\|\s*([\d.]+)', 'stress_100'),
            (r'300%?\s*(?:定伸应力|模量)[^|]*\|\s*([\d.]+)', 'stress_300'),
            (r'tanδ@0°?C[^|]*\|\s*([\d.]+)', 'tan_delta_0'),
            (r'tanδ@60°?C[^|]*\|\s*([\d.]+)', 'tan_delta_60'),
            (r'Tg[^|]*\|\s*(-?[\d.]+)', 'tg_from_mech'),
        ]
        
        for pattern, field in table_patterns:
            if field not in result:
                match = re.search(pattern, body, re.IGNORECASE)
                if match:
                    try:
                        result[field] = float(match.group(1))
                    except ValueError:
                        pass
        
        return result
        
    except Exception as e:
        return {}


def extract_dsc_data(sample_id: str) -> Dict[str, Any]:
    """从 dsc.md 提取关键数据"""
    dsc_path = INTERPRETATIONS_DIR / sample_id / "dsc.md"
    
    if not dsc_path.exists():
        return {}
    
    try:
        doc = read_interpretation_file(dsc_path)
        yaml_data = doc['yaml'].get('data', {})
        
        result = {}
        if 'tg' in yaml_data:
            entry = yaml_data['tg']
            if isinstance(entry, dict):
                result['tg'] = entry.get('value')
            else:
                result['tg'] = entry
        
        return result
    except Exception:
        return {}


def build_merged_yaml(
    sample_id: str,
    old_yaml: Dict[str, Any],
    interpretation_status: Dict[str, bool],
    metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """
    构建合并后的 YAML front matter
    
    保留旧版的重要字段，同时更新时间戳
    """
    today = date.today().isoformat()
    
    # 基础字段
    yaml_data = {
        'sample_id': sample_id,
        'doi': old_yaml.get('doi') or metadata.get('doi'),
        'polymer_type': old_yaml.get('polymer_type') or metadata.get('polymer_type'),
    }
    
    # 保留旧版的 functionalization 结构（如果有）
    if 'functionalization' in old_yaml:
        yaml_data['functionalization'] = old_yaml['functionalization']
    
    # 保留旧版的 filler_system 和 application
    if old_yaml.get('filler_system'):
        yaml_data['filler_system'] = old_yaml['filler_system']
    if old_yaml.get('application'):
        yaml_data['application'] = old_yaml['application']
    
    # 数据完整性
    yaml_data['data_completeness'] = interpretation_status
    
    # 关键词（保留旧版）
    if old_yaml.get('keywords'):
        yaml_data['keywords'] = old_yaml['keywords']
    
    # 时间戳
    yaml_data['created_at'] = old_yaml.get('created_at') or today
    yaml_data['updated_at'] = today
    
    return yaml_data


def build_merged_body(
    sample_id: str,
    metadata: Dict[str, Any],
    mech_data: Dict[str, Any],
    dsc_data: Dict[str, Any],
    interpretation_status: Dict[str, bool],
    preserved_sections: Dict[str, str],
    old_one_sentence: Optional[str],
    old_performance_features: List[Dict[str, str]]
) -> str:
    """
    构建合并后的 Markdown 正文
    
    结构：
    1. 一句话总结（优先用旧版）
    2. 研究亮点（旧版保留）
    3. 核心发现（旧版保留）
    4. 改性机理（旧版保留）
    5. 核心性能特点（新版结构化 + 旧版详细描述）
    6. 关键性能指标表（新版）
    7. 适用场景（新版）
    8. 应用前景（旧版保留）
    9. 文献来源
    """
    lines = [f"# {sample_id} 综合档案", ""]
    
    # ========== 一句话总结 ==========
    one_sentence = old_one_sentence
    if not one_sentence:
        # 生成新的一句话总结
        fg_name = metadata.get('functional_group_name')
        application = metadata.get('application')
        if fg_name and application:
            one_sentence = f"采用{fg_name}官能化，适用于{application}。"
        elif fg_name:
            one_sentence = f"采用{fg_name}官能化的 SSBR 样本。"
        else:
            one_sentence = "官能化 SSBR 样本，具有改性橡胶的典型性能特点。"
    
    lines.extend([
        "## 一句话总结",
        "",
        one_sentence,
        "",
        "---",
        "",
    ])
    
    # ========== 研究亮点（旧版保留） ==========
    if '研究亮点' in preserved_sections:
        lines.extend([
            "## 研究亮点",
            "",
            preserved_sections['研究亮点'],
            "",
            "---",
            "",
        ])
    
    # ========== 样本概述（旧版保留） ==========
    if '样本概述' in preserved_sections:
        lines.extend([
            "## 样本概述",
            "",
            preserved_sections['样本概述'],
            "",
            "---",
            "",
        ])
    
    # ========== 核心发现（旧版保留） ==========
    if '核心发现' in preserved_sections:
        lines.extend([
            "## 核心发现",
            "",
            preserved_sections['核心发现'],
            "",
            "---",
            "",
        ])
    
    # ========== 聚合物结构（旧版保留） ==========
    if '聚合物结构' in preserved_sections:
        lines.extend([
            "## 聚合物结构",
            "",
            preserved_sections['聚合物结构'],
            "",
            "---",
            "",
        ])
    
    # ========== 关键性能数据（旧版保留） ==========
    if '关键性能数据' in preserved_sections:
        lines.extend([
            "## 关键性能数据",
            "",
            preserved_sections['关键性能数据'],
            "",
            "---",
            "",
        ])
    
    # ========== 改性机理（旧版保留） ==========
    if '改性机理' in preserved_sections:
        lines.extend([
            "## 改性机理",
            "",
            preserved_sections['改性机理'],
            "",
            "---",
            "",
        ])
    
    # ========== 界面作用机制（旧版保留） ==========
    if '界面作用机制' in preserved_sections:
        lines.extend([
            "## 界面作用机制",
            "",
            preserved_sections['界面作用机制'],
            "",
            "---",
            "",
        ])
    
    # ========== 核心技术创新（旧版保留） ==========
    if '核心技术创新' in preserved_sections:
        lines.extend([
            "## 核心技术创新",
            "",
            preserved_sections['核心技术创新'],
            "",
            "---",
            "",
        ])
    
    # ========== 性能优势总结（旧版保留） ==========
    if '性能优势总结' in preserved_sections:
        lines.extend([
            "## 性能优势总结",
            "",
            preserved_sections['性能优势总结'],
            "",
            "---",
            "",
        ])
    
    # ========== 核心性能特点 ==========
    lines.extend(["## 核心性能特点", ""])
    
    # 优先使用旧版详细的性能特点
    if old_performance_features:
        for f in old_performance_features:
            lines.extend([
                f"### 【{f['title']}】评价：{f['rating']}",
                "",
                f"{f['description']}",
                "",
            ])
    elif '核心性能特点_old' in preserved_sections:
        # 直接使用旧版的核心性能特点章节
        lines.append(preserved_sections['核心性能特点_old'])
        lines.extend(["", ""])
    else:
        # 生成新的性能特点（简化版）
        features = generate_simple_performance_features(mech_data, dsc_data)
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
    
    # ========== 适用场景 ==========
    lines.extend(["## 适用场景", ""])
    
    application = metadata.get('application')
    if application:
        lines.append(f"- ✅ {application}")
    
    # 根据性能推断
    el = mech_data.get('elongation')
    try:
        if el is not None and float(el) > 400:
            lines.append("- ✅ 需要高延展性的应用场景")
    except (ValueError, TypeError):
        pass
    
    tg = dsc_data.get('tg') or mech_data.get('tg_from_mech')
    try:
        if tg is not None and float(tg) < -30:
            lines.append("- ✅ 低温环境应用")
    except (ValueError, TypeError):
        pass
    
    if not lines[-1].startswith("- "):
        lines.append("- ✅ 通用橡胶制品")
    
    lines.extend(["", "---", ""])
    
    # ========== 应用前景（旧版保留） ==========
    if '应用前景' in preserved_sections:
        lines.extend([
            "## 应用前景",
            "",
            preserved_sections['应用前景'],
            "",
            "---",
            "",
        ])
    
    # ========== 轮胎应用价值（旧版保留） ==========
    if '轮胎应用价值' in preserved_sections:
        lines.extend([
            "## 轮胎应用价值",
            "",
            preserved_sections['轮胎应用价值'],
            "",
            "---",
            "",
        ])
    
    # ========== 技术要点摘要（旧版保留） ==========
    if '技术要点摘要' in preserved_sections:
        lines.extend([
            "## 技术要点摘要",
            "",
            preserved_sections['技术要点摘要'],
            "",
            "---",
            "",
        ])
    
    # ========== 关键性能指标表（新版） ==========
    lines.extend([
        "## 关键性能指标",
        "",
        "| 类别 | 指标 | 数值 | 单位 | 评价 |",
        "|------|------|------|------|------|",
    ])
    
    # 力学数据
    for field, label in [
        ('stress_100', '100%定伸应力'),
        ('stress_300', '300%定伸应力'),
        ('tensile_strength', '拉伸强度'),
        ('elongation', '断裂伸长率'),
    ]:
        val = mech_data.get(field)
        desc = mech_data.get(f'{field}_desc')
        unit = '%' if field == 'elongation' else 'MPa'
        
        if val is not None:
            lines.append(f"| 力学性能 | {label} | {val} | {unit} | - |")
        elif desc:
            lines.append(f"| 力学性能 | {label} | {desc} | 相对 | - |")
        else:
            lines.append(f"| 力学性能 | {label} | - | {unit} | - |")
    
    # 热学数据
    tg_val = dsc_data.get('tg') or mech_data.get('tg_from_mech') or '-'
    lines.append(f"| 热学性能 | Tg | {tg_val} | ℃ | - |")
    
    # 动态力学指标
    if mech_data.get('tan_delta_0') is not None:
        lines.append(f"| 动态性能 | tanδ@0°C | {mech_data.get('tan_delta_0')} | - | 湿抓 |")
    if mech_data.get('tan_delta_60') is not None:
        lines.append(f"| 动态性能 | tanδ@60°C | {mech_data.get('tan_delta_60')} | - | 滚阻 |")
    
    # 结合橡胶含量
    if mech_data.get('bound_rubber') is not None:
        lines.append(f"| 界面性能 | 结合橡胶含量 | {mech_data.get('bound_rubber')} | % | - |")
    
    lines.extend(["", "---", ""])
    
    # ========== 解读文档完整性 ==========
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
    
    # ========== 文献来源 ==========
    lines.extend([
        "## 文献来源",
        "",
        f"- **DOI**: {metadata.get('doi') or '*未知*'}",
        f"- **引文**: {metadata.get('citation') or '*未知*'}",
    ])
    
    lines.extend([
        "",
        "---",
        "",
        "*本综合档案由 `ssbr-summary-generator` 脚本合并生成，保留了人工撰写的解读内容，用于 RAG 语义检索。*",
    ])
    
    return "\n".join(lines)


def generate_simple_performance_features(mech_data: Dict[str, Any], dsc_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """生成简化的性能特点列表"""
    features = []
    
    def safe_float(val):
        if val is None:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None
    
    ts = safe_float(mech_data.get('tensile_strength'))
    if ts is not None:
        rating = "良好" if ts > 10 else "一般"
        features.append({
            'title': '拉伸强度',
            'rating': rating,
            'description': f"拉伸强度达到 {ts} MPa，{rating}的力学强度。"
        })
    
    el = safe_float(mech_data.get('elongation'))
    if el is not None:
        rating = "优秀" if el > 400 else ("良好" if el > 300 else "一般")
        features.append({
            'title': '断裂伸长率',
            'rating': rating,
            'description': f"断裂伸长率为 {el}%，展现出{rating}的延展性。"
        })
    
    tg = safe_float(dsc_data.get('tg')) or safe_float(mech_data.get('tg_from_mech'))
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
    
    return features


def merge_summary(sample_id: str, excel_handler: ExcelHandler, dry_run: bool = False) -> Dict[str, Any]:
    """
    为单个样本合并生成 summary.md
    
    Args:
        sample_id: 样本 ID
        excel_handler: Excel 处理器
        dry_run: 如果为 True，只打印不实际写入
        
    Returns:
        合并结果
    """
    result = {
        'sample_id': sample_id,
        'merged': False,
        'has_old_content': False,
        'preserved_sections': [],
        'errors': []
    }
    
    # 获取元数据
    metadata = excel_handler.get_metadata_fields(sample_id)
    if not metadata:
        result['errors'].append(f"未找到样本 {sample_id} 的元数据")
        return result
    
    # 获取旧版 summary.md
    old_content = get_old_summary_from_git(sample_id)
    
    if old_content:
        result['has_old_content'] = True
        
        # 提取旧版信息
        old_yaml = extract_old_yaml(old_content)
        preserved_sections = extract_preserved_sections(old_content)
        old_one_sentence = extract_one_sentence_summary(old_content)
        old_performance_features = extract_old_performance_features(old_content)
        
        result['preserved_sections'] = list(preserved_sections.keys())
    else:
        old_yaml = {}
        preserved_sections = {}
        old_one_sentence = None
        old_performance_features = []
    
    # 获取解读文档状态
    interpretation_status = get_interpretation_status(sample_id)
    
    # 提取解读数据
    mech_data = extract_mechanical_data(sample_id)
    dsc_data = extract_dsc_data(sample_id)
    
    # 构建合并后的 YAML 和正文
    yaml_data = build_merged_yaml(sample_id, old_yaml, interpretation_status, metadata)
    body = build_merged_body(
        sample_id, metadata, mech_data, dsc_data, interpretation_status,
        preserved_sections, old_one_sentence, old_performance_features
    )
    
    # 写入文件
    output_path = INTERPRETATIONS_DIR / sample_id / "summary.md"
    
    if dry_run:
        print(f"  [DRY RUN] 将创建 {output_path}")
        if preserved_sections:
            print(f"    保留章节: {', '.join(preserved_sections.keys())}")
    else:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            write_interpretation_file(output_path, yaml_data, body)
            result['merged'] = True
        except Exception as e:
            result['errors'].append(f"写入失败: {e}")
    
    return result


def merge_all_summaries(dry_run: bool = False) -> Dict[str, Any]:
    """
    为所有样本合并生成 summary.md
    """
    stats = {
        'total_samples': 0,
        'merged': 0,
        'with_old_content': 0,
        'errors': []
    }
    
    with ExcelHandler(EXCEL_PATH) as excel:
        samples = excel.get_all_samples()
        stats['total_samples'] = len(samples)
        
        print(f"\n开始合并 {len(samples)} 个样本的综合档案...")
        
        for sample in samples:
            sample_id = sample.get('sample_id')
            if not sample_id:
                continue
            
            print(f"\n处理 {sample_id}...")
            result = merge_summary(sample_id, excel, dry_run)
            
            if result['merged']:
                stats['merged'] += 1
                if result['has_old_content']:
                    stats['with_old_content'] += 1
                    print(f"  [OK] 已合并，保留章节: {', '.join(result['preserved_sections']) or '无'}")
                else:
                    print(f"  [OK] 新生成（无旧版内容）")
            
            if result['errors']:
                stats['errors'].extend([f"{sample_id}: {e}" for e in result['errors']])
                for err in result['errors']:
                    print(f"  [ERROR] {err}")
    
    return stats


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SSBR Summary 综合档案合并工具')
    parser.add_argument('--dry-run', action='store_true', help='只打印操作，不实际执行')
    parser.add_argument('--sample', type=str, help='只处理指定样本（如 SSBR-001）')
    args = parser.parse_args()
    
    print("=" * 60)
    print("SSBR Summary 综合档案合并工具")
    print("=" * 60)
    print("\n功能：将旧版丰富内容与新版结构化数据合并")
    
    if args.dry_run:
        print("\n[DRY RUN 模式] 只显示将要执行的操作")
    
    if args.sample:
        # 单个样本处理
        with ExcelHandler(EXCEL_PATH) as excel:
            result = merge_summary(args.sample, excel, dry_run=args.dry_run)
            if result['merged'] or args.dry_run:
                print(f"\n[OK] {args.sample}/summary.md {'将' if args.dry_run else ''}合并成功")
                if result['preserved_sections']:
                    print(f"  保留章节: {', '.join(result['preserved_sections'])}")
            if result['errors']:
                print(f"\n[ERROR] 合并失败: {result['errors']}")
    else:
        # 批量处理
        stats = merge_all_summaries(dry_run=args.dry_run)
        
        print("\n" + "=" * 60)
        print("合并统计")
        print("=" * 60)
        print(f"  总样本数: {stats['total_samples']}")
        print(f"  成功合并: {stats['merged']}")
        print(f"  有旧版内容: {stats['with_old_content']}")
        print(f"  错误数: {len(stats['errors'])}")
        
        if stats['errors']:
            print("\n错误列表:")
            for err in stats['errors']:
                print(f"  - {err}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
