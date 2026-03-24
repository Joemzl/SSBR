#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对比 Excel 数据和 summary.md 文件，找出需要更新的样本
"""

import pandas as pd
from pathlib import Path
import yaml
import re

def extract_yaml_from_md(content):
    """从 Markdown 文件中提取 YAML front matter"""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except:
            return {}
    return {}

def main():
    # 读取 Excel
    df = pd.read_excel('dataset/数据.xlsx')
    
    # 解读文档目录
    interp_dir = Path('dataset/interpretations')
    
    # 检查每个样本
    updates_needed = []
    
    for idx, row in df.iterrows():
        sample_id = row['样本ID']
        summary_path = interp_dir / sample_id / 'summary.md'
        
        if not summary_path.exists():
            print(f"[MISSING] {sample_id}: summary.md 不存在")
            continue
            
        # 读取现有 summary.md
        content = summary_path.read_text(encoding='utf-8')
        yaml_data = extract_yaml_from_md(content)
        
        if not yaml_data:
            print(f"[NO_YAML] {sample_id}: 无法解析 YAML")
            continue
        
        # 对比关键字段
        changes = []
        
        # 官能化程度
        excel_degree = str(row.get('官能化程度_原始数值', ''))
        excel_unit = str(row.get('官能化程度_原始单位', ''))
        yaml_degree = yaml_data.get('functionalization', {}).get('degree', '')
        
        if excel_degree and excel_degree != 'nan' and excel_degree != '未公开':
            expected_degree = f"{excel_degree} {excel_unit}".strip() if excel_unit and excel_unit != 'nan' else excel_degree
            if str(yaml_degree) != expected_degree and str(yaml_degree) != excel_degree:
                changes.append(f"官能化程度: YAML='{yaml_degree}' vs Excel='{expected_degree}'")
        
        # 官能化试剂
        excel_reagent = str(row.get('官能化试剂名称', ''))
        yaml_reagent = yaml_data.get('functionalization', {}).get('reagent', '')
        if excel_reagent and excel_reagent != 'nan' and excel_reagent != str(yaml_reagent):
            changes.append(f"官能化试剂: YAML='{yaml_reagent}' vs Excel='{excel_reagent}'")
        
        # 接枝反应基团
        excel_group = str(row.get('接枝反应基团', ''))
        yaml_group = yaml_data.get('functionalization', {}).get('grafting_group', '')
        if excel_group and excel_group != 'nan' and excel_group != str(yaml_group):
            changes.append(f"接枝反应基团: YAML='{yaml_group}' vs Excel='{excel_group}'")
        
        # 接枝反应基团 SMILES
        excel_smiles = str(row.get('接枝反应基团SMILES', ''))
        yaml_smiles = yaml_data.get('functionalization', {}).get('grafting_group_smiles', '')
        if excel_smiles and excel_smiles != 'nan' and excel_smiles != '-' and excel_smiles != str(yaml_smiles):
            changes.append(f"接枝SMILES: YAML='{yaml_smiles}' vs Excel='{excel_smiles}'")
        
        # 核心官能团 SMILES
        excel_core_smiles = str(row.get('核心官能团 SMILES', ''))
        yaml_core_smiles = yaml_data.get('functionalization', {}).get('core_functional_group_smiles', '')
        if excel_core_smiles and excel_core_smiles != 'nan' and excel_core_smiles != str(yaml_core_smiles):
            changes.append(f"核心官能团SMILES: YAML='{yaml_core_smiles}' vs Excel='{excel_core_smiles}'")
        
        # 核心官能团名称
        excel_core_name = str(row.get('核心官能团名称', ''))
        yaml_core_name = yaml_data.get('functionalization', {}).get('core_functional_group_name', '')
        if excel_core_name and excel_core_name != 'nan' and excel_core_name != str(yaml_core_name):
            changes.append(f"核心官能团名称: YAML='{yaml_core_name}' vs Excel='{excel_core_name}'")
        
        # 高分子指纹描述符
        excel_fingerprint = str(row.get('高分子指纹描述符', ''))
        yaml_fingerprint = yaml_data.get('polymer_fingerprint', '')
        if excel_fingerprint and excel_fingerprint != 'nan' and excel_fingerprint != str(yaml_fingerprint):
            changes.append(f"高分子指纹: YAML='{yaml_fingerprint[:50]}...' vs Excel='{excel_fingerprint[:50]}...'")
        
        if changes:
            updates_needed.append({
                'sample_id': sample_id,
                'changes': changes
            })
            print(f"\n[UPDATE] {sample_id}:")
            for c in changes:
                print(f"  - {c}")
    
    print(f"\n{'='*80}")
    print(f"需要更新的样本数: {len(updates_needed)}")
    print(f"样本列表: {[u['sample_id'] for u in updates_needed]}")

if __name__ == '__main__':
    main()
