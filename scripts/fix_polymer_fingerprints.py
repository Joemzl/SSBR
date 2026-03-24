#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
按照标准格式重建高分子指纹描述符

标准格式（来自 other/解析数据的提示词.txt）：
[试剂整体SMILES]-[数均分子量 (Mn)]-[苯乙烯含量_wt%]-[乙烯基含量_mol%]-[接枝反应基团SMILES]-[核心官能团SMILES]-[官能化程度_原始数值][官能化程度_原始单位]

关键修正点：
1. 官能化程度部分只包含 数值+单位，不包含括号中的解释性文字
2. 缺失项保留 "-"
"""

import pandas as pd
from pathlib import Path
import re

DATASET_PATH = Path("d:/SSBR/dataset/数据.xlsx")

def clean_value(val):
    """清理数值，转为字符串，空值返回 '-'"""
    if pd.isna(val) or str(val).strip() in ['', 'nan', 'None', '待补充']:
        return '-'
    return str(val).strip()

def clean_degree_value(val_str, unit_str):
    """
    清理官能化程度部分，移除括号中的解释性文字
    只保留纯数值和单位
    """
    val = clean_value(val_str)
    unit = clean_value(unit_str)
    
    if val == '-' and unit == '-':
        return '-'
    
    # 如果数值中包含括号解释，移除
    # 例如 "5wt% (vs SiO2)" -> "5wt%"
    # 例如 "86% (封端效率)" -> "86%"
    if val != '-':
        # 移除中文括号及其内容
        val = re.sub(r'\s*（[^）]*）', '', val)
        val = re.sub(r'\s*\([^)]*\)', '', val)
        val = val.strip()
    
    if unit != '-':
        # 移除单位中的括号及其内容
        unit = re.sub(r'\s*（[^）]*）', '', unit)
        unit = re.sub(r'\s*\([^)]*\)', '', unit)
        unit = unit.strip()
    
    # 拼接
    if val != '-' and unit != '-':
        return f"{val}{unit}"
    elif val != '-':
        return val
    else:
        return '-'

def build_fingerprint(row):
    """
    按标准格式构建高分子指纹描述符
    """
    # 获取各字段
    reagent_smiles = clean_value(row.get('试剂整体SMILES', '-'))
    mn = clean_value(row.get('数均分子量 (Mn)', '-'))
    styrene = clean_value(row.get('苯乙烯含量_wt%', '-'))
    vinyl = clean_value(row.get('乙烯基含量_mol%', '-'))
    graft_smiles = clean_value(row.get('接枝反应基团SMILES', '-'))
    core_smiles = clean_value(row.get('核心官能团SMILES', '-'))
    
    # 官能化程度部分
    degree_val = clean_value(row.get('官能化程度_原始数值', '-'))
    degree_unit = clean_value(row.get('官能化程度_原始单位', '-'))
    
    # 清理官能化程度，移除括号解释
    degree_part = clean_degree_value(degree_val, degree_unit)
    
    # 拼接指纹：试剂整体SMILES-Mn-苯乙烯-乙烯基-接枝反应基团SMILES-核心官能团SMILES-官能化程度
    fingerprint = f"{reagent_smiles}-{mn}-{styrene}-{vinyl}-{graft_smiles}-{core_smiles}-{degree_part}"
    
    return fingerprint

def main():
    print("=" * 80)
    print("重建高分子指纹描述符（按标准格式）")
    print("=" * 80)
    
    # 读取 Excel
    df = pd.read_excel(DATASET_PATH)
    print(f"\n读取 {len(df)} 条记录")
    
    # 显示原始字段情况
    print("\n检查原始数据字段...")
    sample_cols = ['样本ID', '试剂整体SMILES', '数均分子量 (Mn)', '苯乙烯含量_wt%', 
                   '乙烯基含量_mol%', '接枝反应基团SMILES', '核心官能团SMILES',
                   '官能化程度_原始数值', '官能化程度_原始单位']
    
    # 显示前几条数据的原始字段
    print("\n前5条样本的原始数据：")
    for idx in range(min(5, len(df))):
        row = df.iloc[idx]
        print(f"\n{row['样本ID']}:")
        print(f"  试剂整体SMILES: {row.get('试剂整体SMILES', 'N/A')}")
        print(f"  数均分子量: {row.get('数均分子量 (Mn)', 'N/A')}")
        print(f"  官能化程度_原始数值: {row.get('官能化程度_原始数值', 'N/A')}")
        print(f"  官能化程度_原始单位: {row.get('官能化程度_原始单位', 'N/A')}")
    
    changes = []
    
    for idx, row in df.iterrows():
        sample_id = row['样本ID']
        old_fp = str(row.get('高分子指纹描述符', ''))
        new_fp = build_fingerprint(row)
        
        if old_fp != new_fp:
            changes.append({
                'sample_id': sample_id,
                'old': old_fp,
                'new': new_fp
            })
            df.at[idx, '高分子指纹描述符'] = new_fp
    
    print(f"\n\n需要修改的记录数：{len(changes)}")
    
    if changes:
        print("\n变更详情（显示前30条）：")
        print("-" * 80)
        for i, c in enumerate(changes[:30]):
            print(f"\n{c['sample_id']}:")
            print(f"  OLD: {c['old']}")
            print(f"  NEW: {c['new']}")
        
        if len(changes) > 30:
            print(f"\n... 还有 {len(changes) - 30} 条变更未显示")
        
        # 保存
        df.to_excel(DATASET_PATH, index=False)
        print(f"\n[OK] 已保存到 {DATASET_PATH}")
    else:
        print("\n[OK] 无需修改")

if __name__ == "__main__":
    main()
