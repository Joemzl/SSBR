"""
数据质量检查脚本 v2 - 详细报告
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path

# 读取数据
excel_path = Path(__file__).parent.parent / "dataset" / "数据.xlsx"
df = pd.read_excel(excel_path)

# 列名映射
SAMPLE_ID = '样本ID'
REAGENT = '官能化试剂名称'
REAGENT_SMILES = '试剂整体 SMILES'
CORE_FG_SMILES = '核心官能团 SMILES'
FINGERPRINT = '高分子指纹描述符'

print("=" * 80)
print("SSBR 数据质量检查报告 (详细版)")
print("=" * 80)
print(f"总样本数: {len(df)}")

# ============================================================================
# 问题类别1: 缺少官能化试剂名称
# ============================================================================
print("\n" + "=" * 80)
print("【问题类别1】缺少官能化试剂名称的样本")
print("=" * 80)

missing_reagent = []
for idx, row in df.iterrows():
    reagent = row[REAGENT]
    if pd.isna(reagent) or str(reagent).strip() == '':
        missing_reagent.append(row[SAMPLE_ID])

print(f"共 {len(missing_reagent)} 个样本:")
for sid in missing_reagent:
    print(f"  - {sid}")

# ============================================================================
# 问题类别2: 有试剂但SMILES缺失或错误
# ============================================================================
print("\n" + "=" * 80)
print("【问题类别2】有官能化试剂但SMILES缺失或错误的样本")
print("=" * 80)

smiles_issues = []
for idx, row in df.iterrows():
    reagent = row[REAGENT]
    reagent_smiles = row[REAGENT_SMILES]
    core_smiles = row[CORE_FG_SMILES]
    
    # 跳过没有试剂的样本
    if pd.isna(reagent) or str(reagent).strip() == '':
        continue
    
    reagent_str = str(reagent).strip()
    smiles_str = str(reagent_smiles).strip() if pd.notna(reagent_smiles) else ''
    
    issue = None
    
    # 检查1: SMILES完全缺失
    if smiles_str == '' or smiles_str == 'nan':
        issue = "SMILES缺失"
    # 检查2: SMILES包含明显的占位符
    elif '-SMILES' in smiles_str.upper():
        issue = "SMILES为占位符格式"
    # 检查3: SMILES与试剂名称相同（明显是复制粘贴错误）
    elif smiles_str == reagent_str:
        issue = "SMILES与试剂名称相同"
    # 检查4: SMILES不包含任何有效化学元素
    elif not any(c in smiles_str for c in 'CNOSPFBrClI'):
        issue = "SMILES不包含有效化学元素"
    
    if issue:
        smiles_issues.append({
            'sample_id': row[SAMPLE_ID],
            'reagent': reagent_str,
            'smiles': smiles_str if smiles_str else '空',
            'issue': issue
        })

print(f"共 {len(smiles_issues)} 个样本:")
for item in smiles_issues:
    print(f"  - {item['sample_id']}")
    print(f"    试剂: {item['reagent']}")
    print(f"    SMILES: {item['smiles']}")
    print(f"    问题: {item['issue']}")
    print()

# ============================================================================
# 问题类别3: 高分子指纹描述符缺失但有其他数据
# ============================================================================
print("\n" + "=" * 80)
print("【问题类别3】有数据但高分子指纹描述符缺失的样本")
print("=" * 80)

# 定义关键数据列（不包括样本ID和指纹本身）
data_cols = ['苯乙烯含量_wt%', '乙烯基含量_mol%', '数均分子量 (Mn)', 
             '官能化程度_原始数值', '核心官能团名称', '核心官能团化学式']

fingerprint_missing = []
for idx, row in df.iterrows():
    fingerprint = row[FINGERPRINT]
    reagent = row[REAGENT]
    
    # 检查指纹是否为空
    fp_empty = pd.isna(fingerprint) or str(fingerprint).strip() == '' or str(fingerprint).strip() == 'nan'
    
    if not fp_empty:
        continue
    
    # 计算有多少关键数据列非空
    non_empty_data = []
    for col in data_cols:
        if col in df.columns:
            val = row[col]
            if pd.notna(val) and str(val).strip() != '' and str(val).strip() != 'nan':
                non_empty_data.append(col)
    
    # 如果有试剂或者有至少2个其他数据列，则认为应该有指纹
    has_reagent = pd.notna(reagent) and str(reagent).strip() != ''
    
    if has_reagent or len(non_empty_data) >= 2:
        fingerprint_missing.append({
            'sample_id': row[SAMPLE_ID],
            'reagent': str(reagent) if has_reagent else '空',
            'available_data': non_empty_data
        })

print(f"共 {len(fingerprint_missing)} 个样本:")
for item in fingerprint_missing:
    print(f"  - {item['sample_id']}")
    print(f"    试剂: {item['reagent']}")
    print(f"    已有数据列: {', '.join(item['available_data']) if item['available_data'] else '无'}")
    print()

# ============================================================================
# 汇总
# ============================================================================
print("\n" + "=" * 80)
print("【汇总】")
print("=" * 80)

# 计算低质量样本（去重）
low_quality_samples = set(missing_reagent)
for item in smiles_issues:
    low_quality_samples.add(item['sample_id'])

# 可修补的样本（有试剂但缺指纹）
repairable_samples = set()
for item in fingerprint_missing:
    if item['reagent'] != '空':
        repairable_samples.add(item['sample_id'])

print(f"1. 缺少官能化试剂的样本: {len(missing_reagent)} 个")
print(f"2. SMILES有问题的样本: {len(smiles_issues)} 个")
print(f"3. 指纹缺失但有数据的样本: {len(fingerprint_missing)} 个")
print()
print(f"低质量样本总数 (去重): {len(low_quality_samples)} 个")
print(f"  → 建议删除的样本: {sorted(low_quality_samples)}")
print()
print(f"可修补的样本 (有试剂但缺指纹): {len(repairable_samples)} 个")
print(f"  → 建议补充指纹的样本: {sorted(repairable_samples)}")
print()

# 完全低质量（无试剂）需要删除
truly_low_quality = set(missing_reagent)
print(f"完全低质量（无试剂，建议删除）: {len(truly_low_quality)} 个")
print(f"  {sorted(truly_low_quality)}")

# SMILES需要修复的
smiles_to_fix = set(item['sample_id'] for item in smiles_issues)
print(f"\nSMILES需要修复: {len(smiles_to_fix)} 个")
print(f"  {sorted(smiles_to_fix)}")

# 指纹需要补充的
print(f"\n指纹需要补充: {len(repairable_samples)} 个")
print(f"  {sorted(repairable_samples)}")
