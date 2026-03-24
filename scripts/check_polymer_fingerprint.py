"""检查高分子指纹描述符列的缺失状态"""
import pandas as pd
from pathlib import Path

excel_path = Path("dataset/数据.xlsx")
df = pd.read_excel(excel_path)

col = "高分子指纹描述符"
sample_col = "样本ID"

print(f"=== 高分子指纹描述符检查 ===")
print(f"总样本数: {len(df)}")

# 检查缺失情况
def is_missing(val):
    if pd.isna(val):
        return True
    if str(val).strip() in ['', '待补充', 'N/A', 'nan']:
        return True
    return False

missing_mask = df[col].apply(is_missing)
missing_df = df[missing_mask]

print(f"缺失/待补充数量: {len(missing_df)}")

if len(missing_df) > 0:
    print("\n缺失样本列表:")
    for _, row in missing_df.iterrows():
        sample_id = row[sample_col]
        reagent = row.get("官能化试剂名称", "")
        smiles = row.get("试剂整体 SMILES", "")
        print(f"  {sample_id}: 试剂={reagent}, SMILES={str(smiles)[:50]}...")
else:
    print("\n全部样本已有高分子指纹描述符！")

# 统计现有数据
filled = df[~missing_mask]
print(f"\n已填充数量: {len(filled)}")
print("\n已填充样本示例 (前5个):")
for _, row in filled.head(5).iterrows():
    sample_id = row[sample_col]
    fingerprint = str(row[col])[:60]
    print(f"  {sample_id}: {fingerprint}...")
