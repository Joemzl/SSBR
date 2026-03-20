"""
数据质量检查脚本
检查 数据.xlsx 中的数据质量问题
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path

# 读取数据
excel_path = Path(__file__).parent.parent / "dataset" / "数据.xlsx"
df = pd.read_excel(excel_path)

print("=" * 80)
print("SSBR 数据质量检查报告")
print("=" * 80)

print(f"\n📊 数据概览:")
print(f"   总样本数: {len(df)}")
print(f"   总列数: {len(df.columns)}")
print(f"   列名: {list(df.columns)}")

# 获取关键列名（假设列名）
# 需要先确认实际列名
print("\n" + "=" * 80)
print("列名检查")
print("=" * 80)
for i, col in enumerate(df.columns):
    print(f"   {chr(65+i) if i < 26 else '??'}: {col}")

# 检查样本ID列
sample_id_col = df.columns[0]  # 假设第一列是样本ID
print(f"\n📋 样本ID列: {sample_id_col}")
print(f"   样本列表: {df[sample_id_col].tolist()}")

# 查找官能化试剂相关列
print("\n" + "=" * 80)
print("官能化试剂相关列")
print("=" * 80)

reagent_col = None
smiles_col = None
fingerprint_col = None

for col in df.columns:
    col_lower = str(col).lower()
    if '官能化试剂' in str(col) and 'smiles' not in col_lower:
        reagent_col = col
        print(f"   官能化试剂列: {col}")
    if 'smiles' in col_lower:
        smiles_col = col
        print(f"   SMILES列: {col}")
    if '指纹' in str(col) or '描述符' in str(col):
        fingerprint_col = col
        print(f"   指纹描述符列: {col}")

print("\n" + "=" * 80)
print("问题1: 缺少官能化试剂名称的样本")
print("=" * 80)

if reagent_col:
    missing_reagent = df[df[reagent_col].isna() | (df[reagent_col] == '')]
    if len(missing_reagent) > 0:
        print(f"   ❌ 发现 {len(missing_reagent)} 个样本缺少官能化试剂名称:")
        for idx, row in missing_reagent.iterrows():
            print(f"      - {row[sample_id_col]}")
    else:
        print("   ✅ 所有样本都有官能化试剂名称")
else:
    print("   ⚠️ 未找到官能化试剂列")

print("\n" + "=" * 80)
print("问题2: SMILES缺失或错误的样本")
print("=" * 80)

if smiles_col and reagent_col:
    # 检查有试剂但无SMILES
    has_reagent_no_smiles = df[
        (df[reagent_col].notna()) & 
        (df[reagent_col] != '') & 
        (df[smiles_col].isna() | (df[smiles_col] == ''))
    ]
    
    if len(has_reagent_no_smiles) > 0:
        print(f"   ❌ 发现 {len(has_reagent_no_smiles)} 个样本有试剂但缺少SMILES:")
        for idx, row in has_reagent_no_smiles.iterrows():
            print(f"      - {row[sample_id_col]}: 试剂={row[reagent_col]}, SMILES=空")
    else:
        print("   ✅ 所有有试剂的样本都有SMILES")
    
    # 检查SMILES格式错误（如包含"-SMILES"后缀、或明显不是SMILES格式）
    print("\n   检查SMILES格式错误:")
    smiles_errors = []
    for idx, row in df.iterrows():
        smiles = str(row[smiles_col]) if pd.notna(row[smiles_col]) else ''
        if smiles and smiles != 'nan':
            # 检查明显的格式错误
            is_error = False
            error_reason = ""
            
            # 1. 包含 -SMILES 后缀
            if '-SMILES' in smiles.upper():
                is_error = True
                error_reason = "包含'-SMILES'后缀"
            # 2. 不包含任何化学符号（至少应有C, N, O, S等）
            elif not any(c in smiles for c in 'CNOSPFClBrI'):
                is_error = True
                error_reason = "不包含有效化学元素符号"
            # 3. 太短（有效SMILES通常至少有几个字符）
            elif len(smiles) < 3 and smiles not in ['C', 'N', 'O', 'S']:
                is_error = True
                error_reason = "SMILES太短"
            
            if is_error:
                smiles_errors.append({
                    'sample_id': row[sample_id_col],
                    'reagent': row[reagent_col] if reagent_col else '',
                    'smiles': smiles,
                    'reason': error_reason
                })
    
    if smiles_errors:
        print(f"   ❌ 发现 {len(smiles_errors)} 个样本SMILES格式错误:")
        for err in smiles_errors:
            print(f"      - {err['sample_id']}: 试剂={err['reagent']}, SMILES={err['smiles']}")
            print(f"        原因: {err['reason']}")
    else:
        print("   ✅ 未发现明显的SMILES格式错误")

else:
    print("   ⚠️ 未找到SMILES列或官能化试剂列")

print("\n" + "=" * 80)
print("问题3: 高分子指纹描述符缺失的样本")
print("=" * 80)

if fingerprint_col:
    # 检查有数据但指纹为空的样本
    # 定义"有数据"：至少有3个非空的数据列
    data_cols = [c for c in df.columns if c not in [sample_id_col, fingerprint_col]]
    
    missing_fingerprint = []
    for idx, row in df.iterrows():
        # 计算非空数据列数
        non_empty_count = sum(1 for c in data_cols if pd.notna(row[c]) and str(row[c]).strip() != '')
        
        # 检查指纹是否为空
        fingerprint_empty = pd.isna(row[fingerprint_col]) or str(row[fingerprint_col]).strip() == ''
        
        if fingerprint_empty and non_empty_count >= 3:
            missing_fingerprint.append({
                'sample_id': row[sample_id_col],
                'non_empty_cols': non_empty_count,
                'reagent': row[reagent_col] if reagent_col and pd.notna(row[reagent_col]) else '无'
            })
    
    if missing_fingerprint:
        print(f"   ❌ 发现 {len(missing_fingerprint)} 个样本有数据但缺少指纹描述符:")
        for item in missing_fingerprint:
            print(f"      - {item['sample_id']}: 有 {item['non_empty_cols']} 个非空数据列, 试剂={item['reagent']}")
    else:
        print("   ✅ 所有有数据的样本都有指纹描述符")
else:
    print("   ⚠️ 未找到指纹描述符列")

print("\n" + "=" * 80)
print("数据质量汇总")
print("=" * 80)

# 输出详细的样本数据用于审查
print("\n" + "=" * 80)
print("关键列数据详情 (用于人工审查)")
print("=" * 80)

key_cols = [sample_id_col]
if reagent_col:
    key_cols.append(reagent_col)
if smiles_col:
    key_cols.append(smiles_col)
if fingerprint_col:
    key_cols.append(fingerprint_col)

print(f"\n选中的关键列: {key_cols}")
print("\n" + "-" * 100)

for idx, row in df.iterrows():
    sample_id = row[sample_id_col]
    reagent = row[reagent_col] if reagent_col and pd.notna(row[reagent_col]) else '空'
    smiles = row[smiles_col] if smiles_col and pd.notna(row[smiles_col]) else '空'
    fingerprint = row[fingerprint_col] if fingerprint_col and pd.notna(row[fingerprint_col]) else '空'
    
    # 截断过长的内容
    smiles_display = str(smiles)[:50] + '...' if len(str(smiles)) > 50 else str(smiles)
    fingerprint_display = str(fingerprint)[:30] + '...' if len(str(fingerprint)) > 30 else str(fingerprint)
    
    print(f"{sample_id}: 试剂={reagent}, SMILES={smiles_display}, 指纹={fingerprint_display}")

print("\n" + "=" * 80)
print("检查完成")
print("=" * 80)
