#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量更新 summary.md 的 YAML front matter
只补充官能化相关的结构化数据，不修改正文内容
"""

import pandas as pd
from pathlib import Path
import yaml
import re
from datetime import date

def parse_yaml_and_content(content):
    """解析 YAML front matter 和正文"""
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if match:
        yaml_str = match.group(1)
        body = match.group(2)
        try:
            yaml_data = yaml.safe_load(yaml_str)
            return yaml_data, body
        except Exception as e:
            print(f"YAML 解析错误: {e}")
            return None, content
    return None, content

def build_functionalization_block(row):
    """根据 Excel 数据构建 functionalization 结构"""
    func_data = {}
    
    # 是否官能化
    is_func = str(row.get('是否是链中官能化', ''))
    if is_func == '是':
        func_data['type'] = 'in_chain'
    elif is_func == '否':
        func_data['type'] = 'chain_end_or_additive'
    
    # 官能化试剂
    reagent = row.get('官能化试剂名称', '')
    if pd.notna(reagent) and str(reagent).strip():
        func_data['reagent'] = str(reagent).strip()
    
    # 接枝反应基团
    grafting_group = row.get('接枝反应基团', '')
    if pd.notna(grafting_group) and str(grafting_group).strip():
        func_data['grafting_group'] = str(grafting_group).strip()
    
    # 接枝反应基团 SMILES
    grafting_smiles = row.get('接枝反应基团SMILES', '')
    if pd.notna(grafting_smiles) and str(grafting_smiles).strip() and str(grafting_smiles).strip() != '-':
        func_data['grafting_group_smiles'] = str(grafting_smiles).strip()
    
    # 核心官能团 SMILES
    core_smiles = row.get('核心官能团 SMILES', '')
    if pd.notna(core_smiles) and str(core_smiles).strip():
        func_data['core_functional_group_smiles'] = str(core_smiles).strip()
    
    # 核心官能团名称
    core_name = row.get('核心官能团名称', '')
    if pd.notna(core_name) and str(core_name).strip():
        func_data['core_functional_group_name'] = str(core_name).strip()
    
    # 官能化程度
    degree_val = row.get('官能化程度_原始数值', '')
    degree_unit = row.get('官能化程度_原始单位', '')
    if pd.notna(degree_val) and str(degree_val).strip() and str(degree_val).strip() != '未公开':
        degree_str = str(degree_val).strip()
        if pd.notna(degree_unit) and str(degree_unit).strip():
            degree_str = f"{degree_str} {str(degree_unit).strip()}"
        func_data['degree'] = degree_str
    
    return func_data if func_data else None

def update_summary_yaml(sample_id, row, summary_path):
    """更新单个 summary.md 的 YAML"""
    content = summary_path.read_text(encoding='utf-8')
    yaml_data, body = parse_yaml_and_content(content)
    
    if yaml_data is None:
        print(f"  [SKIP] 无法解析 YAML")
        return False
    
    # 构建新的 functionalization 数据
    func_data = build_functionalization_block(row)
    if func_data:
        yaml_data['functionalization'] = func_data
    
    # 高分子指纹描述符
    fingerprint = row.get('高分子指纹描述符', '')
    if pd.notna(fingerprint) and str(fingerprint).strip():
        yaml_data['polymer_fingerprint'] = str(fingerprint).strip()
    
    # 更新时间
    yaml_data['updated_at'] = str(date.today())
    
    # 重新组装文件
    # 使用自定义 YAML 格式化，避免中文被转义
    def yaml_str_presenter(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    
    yaml.add_representer(str, yaml_str_presenter)
    
    yaml_str = yaml.dump(yaml_data, allow_unicode=True, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{yaml_str}---\n{body}"
    
    summary_path.write_text(new_content, encoding='utf-8')
    return True

def main():
    # 读取 Excel
    df = pd.read_excel('dataset/数据.xlsx')
    print(f"Excel 样本数: {len(df)}")
    
    # 解读文档目录
    interp_dir = Path('dataset/interpretations')
    
    updated = 0
    skipped = 0
    errors = 0
    
    for idx, row in df.iterrows():
        sample_id = row['样本ID']
        summary_path = interp_dir / sample_id / 'summary.md'
        
        if not summary_path.exists():
            print(f"[MISSING] {sample_id}: summary.md 不存在")
            skipped += 1
            continue
        
        print(f"[UPDATE] {sample_id}...")
        try:
            if update_summary_yaml(sample_id, row, summary_path):
                updated += 1
            else:
                errors += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"更新完成:")
    print(f"  - 成功更新: {updated}")
    print(f"  - 跳过: {skipped}")
    print(f"  - 错误: {errors}")

if __name__ == '__main__':
    main()
