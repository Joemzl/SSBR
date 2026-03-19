#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
标准化所有 summary.md 文件的 YAML front matter 格式。

该脚本将现有的各种格式统一为标准格式，同时保留原有的 Markdown 正文内容。

标准 YAML 格式:
---
sample_id: SSBR-XXX
doi: "10.xxxx/xxxxx"
polymer_type: "官能化类型描述"
functionalization:
  is_functionalized: true/false
  type: "chain_end/in_chain/none/filler_modification"
  reagent: "官能化试剂名称"
  functional_group: "核心官能团"
  degree: "X.X wt%"
  method: "改性方法"
filler_system: "填料体系描述"
application: "应用场景"
data_completeness:
  mechanical: true/false
  dsc: true/false
  nmr: true/false
  tem: true/false
keywords: []
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

Usage:
    python scripts/standardize_summaries.py --dry-run    # 预览变更
    python scripts/standardize_summaries.py              # 执行标准化
    python scripts/standardize_summaries.py --stats      # 查看统计
    python scripts/standardize_summaries.py --sample SSBR-001  # 处理单个样本
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Optional

import yaml


# ============================================================
# 配置
# ============================================================

BASE_DIR = Path(__file__).parent.parent / "dataset" / "interpretations"
TODAY = date.today().isoformat()


# ============================================================
# YAML 解析与提取
# ============================================================

def parse_yaml_front_matter(content: str) -> tuple[dict, str]:
    """解析 YAML front matter 和 Markdown 正文"""
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if yaml_match:
        yaml_str = yaml_match.group(1)
        markdown_body = content[yaml_match.end():]
        try:
            yaml_data = yaml.safe_load(yaml_str) or {}
        except yaml.YAMLError as e:
            print(f"  [!] YAML 解析错误: {e}")
            yaml_data = {}
        return yaml_data, markdown_body
    return {}, content


def extract_from_markdown(content: str) -> dict:
    """从 Markdown 正文提取关键信息（作为 YAML 的补充）"""
    extracted = {}
    
    # 提取官能化试剂
    reagent_match = re.search(r'\*\*官能化试剂\*\*[：:]\s*(.+?)(?:\n|$)', content)
    if reagent_match:
        extracted['reagent_from_md'] = reagent_match.group(1).strip()
    
    # 提取核心官能团
    fg_match = re.search(r'\*\*核心官能团\*\*[：:]\s*(.+?)(?:\n|$)', content)
    if fg_match:
        extracted['functional_group_from_md'] = fg_match.group(1).strip()
    
    # 提取官能化程度
    degree_match = re.search(r'\*\*官能化程度\*\*[：:]\s*(.+?)(?:\n|$)', content)
    if degree_match:
        extracted['degree_from_md'] = degree_match.group(1).strip()
    
    # 提取改性方法
    method_match = re.search(r'\*\*改性方法\*\*[：:]\s*(.+?)(?:\n|$)', content)
    if method_match:
        extracted['method_from_md'] = method_match.group(1).strip()
    
    # 提取 DOI
    doi_match = re.search(r'\*\*DOI\*\*[：:]\s*(.+?)(?:\n|$)', content)
    if doi_match:
        extracted['doi_from_md'] = doi_match.group(1).strip()
    
    return extracted


# ============================================================
# 标准化逻辑
# ============================================================

def normalize_doi(yaml_data: dict) -> Optional[str]:
    """从各种字段提取 DOI"""
    doi_fields = ['doi', 'source_doi', 'literature_doi', 'data_source']
    for field in doi_fields:
        if field in yaml_data and yaml_data[field]:
            doi = str(yaml_data[field])
            # 清理 DOI 格式
            doi = doi.replace('https://doi.org/', '').replace('http://doi.org/', '')
            return doi
    return None


def normalize_functionalization(yaml_data: dict, md_extracted: dict) -> dict:
    """标准化官能化信息"""
    func_info = {
        'is_functionalized': True,
        'type': 'unknown',
        'reagent': None,
        'functional_group': None,
        'degree': None,
        'method': None,
    }
    
    # ===== 检测是否为未官能化 =====
    polymer_type = yaml_data.get('polymer_type', '')
    functionalization = yaml_data.get('functionalization', '')
    
    # 从 polymer 嵌套字段检查
    polymer_info = yaml_data.get('polymer', {})
    if isinstance(polymer_info, dict):
        is_func = polymer_info.get('is_functionalized')
        if is_func is False:
            func_info['is_functionalized'] = False
            func_info['type'] = 'none'
            return func_info
        if polymer_info.get('functionalization_type'):
            func_info['type'] = polymer_info['functionalization_type']
        if polymer_info.get('functional_reagent'):
            func_info['reagent'] = polymer_info['functional_reagent']
        if polymer_info.get('functional_group'):
            func_info['functional_group'] = polymer_info['functional_group']
    
    # 检测未官能化样本
    if '未官能化' in polymer_type or functionalization == '无' or functionalization == 'none':
        func_info['is_functionalized'] = False
        func_info['type'] = 'none'
        return func_info
    
    # ===== 检测填料改性 =====
    modification_strategy = yaml_data.get('modification_strategy', '')
    if '填料' in modification_strategy or '表面改性' in modification_strategy:
        func_info['type'] = 'filler_modification'
        func_info['reagent'] = yaml_data.get('filler_system', modification_strategy)
        return func_info
    if '硅烷' in modification_strategy or '偶联剂' in modification_strategy:
        func_info['type'] = 'filler_modification'
        func_info['reagent'] = modification_strategy
        return func_info
    
    # ===== 从 functionalizing_agent 提取（格式 B）=====
    func_agent = yaml_data.get('functionalizing_agent', {})
    if isinstance(func_agent, dict) and func_agent:
        func_info['reagent'] = func_agent.get('full_name') or func_agent.get('name')
        func_info['functional_group'] = func_agent.get('core_functional_group')
        func_info['type'] = 'in_chain'  # 默认为链中官能化
    
    # ===== 从顶层字段提取 =====
    if not func_info['reagent']:
        func_info['reagent'] = (
            yaml_data.get('functionalization_reagent') or
            yaml_data.get('functionalization_agent') or
            md_extracted.get('reagent_from_md')
        )
    
    if not func_info['functional_group']:
        top_fg = yaml_data.get('functional_group', '')
        if top_fg:
            # 提取官能团名称（去掉括号中的化学式）
            func_info['functional_group'] = re.sub(r'\s*[（(].+?[）)]', '', top_fg).strip()
        else:
            func_info['functional_group'] = md_extracted.get('functional_group_from_md')
    
    # ===== 从 sample_info 嵌套字段提取 =====
    sample_info = yaml_data.get('sample_info', {})
    if isinstance(sample_info, dict):
        nested_type = sample_info.get('type', '')
        if '未官能化' in nested_type:
            func_info['is_functionalized'] = False
            func_info['type'] = 'none'
            return func_info
        nested_agent = sample_info.get('functionalization_agent', '')
        if nested_agent and '未明确' not in nested_agent and not func_info['reagent']:
            func_info['reagent'] = nested_agent
        nested_fg = sample_info.get('core_functional_group')
        if nested_fg and not func_info['functional_group']:
            func_info['functional_group'] = nested_fg
    
    # ===== 从 sample_type 提取 =====
    sample_type = yaml_data.get('sample_type', '')
    if sample_type and not func_info['functional_group']:
        fg_match = re.search(r'(\w+)\s*官能化', sample_type)
        if fg_match:
            func_info['functional_group'] = fg_match.group(1)
    
    # ===== 官能化程度 =====
    func_info['degree'] = (
        yaml_data.get('key_metrics', {}).get('functionalization_degree') or
        md_extracted.get('degree_from_md')
    )
    func_degree_obj = yaml_data.get('functionalization_degree', {})
    if isinstance(func_degree_obj, dict):
        val = func_degree_obj.get('value', '')
        unit = func_degree_obj.get('unit', '')
        if val:
            func_info['degree'] = f"{val} {unit}".strip()
    
    # ===== 改性方法 =====
    func_info['method'] = (
        yaml_data.get('functionalization_type') or
        md_extracted.get('method_from_md')
    )
    
    # ===== 判断官能化类型 =====
    func_type = yaml_data.get('functionalization_type', '')
    if 'chain_end' in func_type or '链端' in func_type or '双端' in func_type:
        func_info['type'] = 'chain_end'
    elif 'in_chain' in func_type or '链中' in func_type or '巯基-烯' in str(func_info.get('method', '')):
        func_info['type'] = 'in_chain'
    elif func_info['reagent'] and func_info['is_functionalized']:
        func_info['type'] = 'in_chain'  # 默认
    
    return func_info


def normalize_data_completeness(yaml_data: dict, sample_dir: Path) -> dict:
    """标准化数据完整性信息"""
    completeness = {
        'mechanical': False,
        'dsc': False,
        'nmr': False,
        'tem': False,
    }
    
    # 从 YAML 读取
    existing = yaml_data.get('data_completeness', {})
    if isinstance(existing, dict):
        for key in completeness:
            val = existing.get(key) or existing.get('thermal' if key == 'dsc' else key)
            if val is True or val == 'true' or val == 'partial':
                completeness[key] = True
    
    # 从 interpretations_included 读取
    included = yaml_data.get('interpretations_included', [])
    if isinstance(included, list):
        for item in included:
            if item in completeness:
                completeness[item] = True
    
    # 检查实际文件是否存在
    for doc_type in completeness:
        doc_file = sample_dir / f"{doc_type}.md"
        if doc_file.exists():
            content = doc_file.read_text(encoding='utf-8')
            # 检查文件是否有实际内容（不只是模板）
            if len(content) > 200 and '## ' in content:
                completeness[doc_type] = True
    
    return completeness


def build_standard_yaml(
    sample_id: str,
    yaml_data: dict,
    md_extracted: dict,
    sample_dir: Path
) -> dict:
    """构建标准化的 YAML 数据"""
    
    func_info = normalize_functionalization(yaml_data, md_extracted)
    
    standard = {
        'sample_id': sample_id,
        'doi': normalize_doi(yaml_data) or md_extracted.get('doi_from_md'),
        'polymer_type': get_polymer_type_description(yaml_data, func_info),
        'functionalization': {
            'is_functionalized': func_info['is_functionalized'],
            'type': func_info['type'],
            'reagent': func_info['reagent'],
            'functional_group': func_info['functional_group'],
            'degree': func_info['degree'],
            'method': func_info['method'],
        },
        'filler_system': get_filler_system(yaml_data),
        'application': yaml_data.get('application') or yaml_data.get('target_scenario'),
        'data_completeness': normalize_data_completeness(yaml_data, sample_dir),
        'keywords': yaml_data.get('keywords', []),
        'created_at': yaml_data.get('created_at') or yaml_data.get('created') or TODAY,
        'updated_at': TODAY,
    }
    
    # 清理 None 值（保留结构但用 null 表示）
    return standard


def get_polymer_type_description(yaml_data: dict, func_info: dict) -> str:
    """生成聚合物类型描述"""
    polymer_type = yaml_data.get('polymer_type', '')
    if polymer_type:
        return polymer_type
    
    if not func_info['is_functionalized']:
        return '未官能化工业 SSBR'
    
    fg = func_info.get('functional_group', '')
    func_type = func_info.get('type', '')
    
    if func_type == 'filler_modification':
        return '填料改性 SSBR'
    elif fg:
        return f'{fg}官能化 SSBR'
    else:
        return 'SSBR'


def get_filler_system(yaml_data: dict) -> Optional[str]:
    """提取填料体系信息"""
    filler = yaml_data.get('filler_system') or yaml_data.get('filler')
    if isinstance(filler, dict):
        filler_type = filler.get('type', '')
        loading = filler.get('loading', '')
        return f"{filler_type} ({loading})" if loading else filler_type
    return filler


# ============================================================
# 文件处理
# ============================================================

def standardize_summary(sample_dir: Path, dry_run: bool = False) -> dict:
    """标准化单个样本的 summary.md"""
    sample_id = sample_dir.name
    summary_path = sample_dir / "summary.md"
    
    if not summary_path.exists():
        return {'status': 'skip', 'reason': 'no summary.md'}
    
    content = summary_path.read_text(encoding='utf-8')
    yaml_data, markdown_body = parse_yaml_front_matter(content)
    md_extracted = extract_from_markdown(content)
    
    # 检查是否已经是标准格式
    if 'functionalization' in yaml_data and isinstance(yaml_data['functionalization'], dict):
        if 'is_functionalized' in yaml_data['functionalization']:
            return {'status': 'skip', 'reason': 'already standardized'}
    
    # 构建标准化 YAML
    standard_yaml = build_standard_yaml(sample_id, yaml_data, md_extracted, sample_dir)
    
    # 生成新的 YAML 字符串
    yaml_str = yaml.dump(
        standard_yaml,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    )
    
    # 组合新内容
    new_content = f"---\n{yaml_str}---\n{markdown_body}"
    
    if dry_run:
        return {
            'status': 'would_update',
            'old_yaml': yaml_data,
            'new_yaml': standard_yaml,
        }
    
    # 写入文件
    summary_path.write_text(new_content, encoding='utf-8')
    return {'status': 'updated', 'new_yaml': standard_yaml}


def process_all_samples(dry_run: bool = False, target_sample: Optional[str] = None):
    """处理所有样本"""
    if target_sample:
        sample_dirs = [BASE_DIR / target_sample]
    else:
        sample_dirs = sorted([
            d for d in BASE_DIR.iterdir()
            if d.is_dir() and d.name.startswith('SSBR-')
        ])
    
    stats = {
        'updated': 0,
        'would_update': 0,
        'skip_standardized': 0,
        'skip_no_file': 0,
        'errors': 0,
    }
    
    print(f"{'[DRY RUN] ' if dry_run else ''}处理 {len(sample_dirs)} 个样本...")
    print("=" * 60)
    
    for sample_dir in sample_dirs:
        sample_id = sample_dir.name
        try:
            result = standardize_summary(sample_dir, dry_run)
            
            if result['status'] == 'updated':
                stats['updated'] += 1
                print(f"  [✓] {sample_id}: 已标准化")
            elif result['status'] == 'would_update':
                stats['would_update'] += 1
                print(f"  [~] {sample_id}: 需要标准化")
                # 显示关键变更
                new_yaml = result['new_yaml']
                func = new_yaml.get('functionalization', {})
                fg = func.get('functional_group') or '无'
                reagent = func.get('reagent') or '无'
                is_func = '是' if func.get('is_functionalized') else '否'
                print(f"      官能化: {is_func}, 官能团: {fg}, 试剂: {reagent}")
            elif result['status'] == 'skip':
                if 'standardized' in result.get('reason', ''):
                    stats['skip_standardized'] += 1
                else:
                    stats['skip_no_file'] += 1
                    print(f"  [-] {sample_id}: {result['reason']}")
        except Exception as e:
            stats['errors'] += 1
            print(f"  [!] {sample_id}: 错误 - {e}")
    
    print("=" * 60)
    print(f"\n统计:")
    if dry_run:
        print(f"  需要更新: {stats['would_update']}")
    else:
        print(f"  已更新: {stats['updated']}")
    print(f"  已是标准格式: {stats['skip_standardized']}")
    print(f"  无 summary.md: {stats['skip_no_file']}")
    print(f"  错误: {stats['errors']}")
    
    return stats


def show_stats():
    """显示当前格式统计"""
    sample_dirs = sorted([
        d for d in BASE_DIR.iterdir()
        if d.is_dir() and d.name.startswith('SSBR-')
    ])
    
    format_counts = {
        'standard': 0,       # 标准格式
        'skill_used': 0,     # 旧标准格式（有 skill_used）
        'functionalizing_agent': 0,
        'polymer_nested': 0,
        'sample_info': 0,
        'simple': 0,         # 简单格式
        'no_file': 0,
    }
    
    for sample_dir in sample_dirs:
        summary_path = sample_dir / "summary.md"
        if not summary_path.exists():
            format_counts['no_file'] += 1
            continue
        
        content = summary_path.read_text(encoding='utf-8')[:1500]
        
        if 'functionalization:' in content and 'is_functionalized:' in content:
            format_counts['standard'] += 1
        elif 'skill_used:' in content:
            format_counts['skill_used'] += 1
        elif 'functionalizing_agent:' in content:
            format_counts['functionalizing_agent'] += 1
        elif 'polymer:' in content and 'is_functionalized:' in content:
            format_counts['polymer_nested'] += 1
        elif 'sample_info:' in content:
            format_counts['sample_info'] += 1
        else:
            format_counts['simple'] += 1
    
    total = len(sample_dirs)
    print("=" * 60)
    print("Summary.md 格式分布统计")
    print("=" * 60)
    
    for fmt, count in format_counts.items():
        pct = count / total * 100 if total > 0 else 0
        bar = "█" * int(pct / 3)
        label = {
            'standard': '[OK] 标准格式 (新)',
            'skill_used': '旧标准格式',
            'functionalizing_agent': 'functionalizing_agent 嵌套',
            'polymer_nested': 'polymer 嵌套',
            'sample_info': 'sample_info 嵌套',
            'simple': '简单/其他格式',
            'no_file': '无 summary.md',
        }.get(fmt, fmt)
        print(f"  {label:30s}: {count:3d} ({pct:5.1f}%) {bar}")
    
    print(f"\n总计: {total} 个样本目录")


# ============================================================
# 主入口
# ============================================================

def main():
    # 设置输出编码为 UTF-8
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(
        description='标准化 summary.md 的 YAML 格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--dry-run', action='store_true', help='预览变更，不实际写入')
    parser.add_argument('--stats', action='store_true', help='显示当前格式统计')
    parser.add_argument('--sample', type=str, help='只处理指定样本 (如 SSBR-001)')
    
    args = parser.parse_args()
    
    if args.stats:
        show_stats()
    else:
        process_all_samples(dry_run=args.dry_run, target_sample=args.sample)


if __name__ == '__main__':
    main()
