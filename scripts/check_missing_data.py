"""
检查 Excel 数据中的缺失字段，识别需要从 Zotero 补充的样本
"""
import pandas as pd
from pathlib import Path

# 读取数据
excel_path = Path(__file__).parent.parent / "dataset" / "数据.xlsx"
df = pd.read_excel(excel_path)

print(f"总样本数: {len(df)}")
print(f"\n列名 ({len(df.columns)} 列):")
for i, col in enumerate(df.columns):
    print(f"  {chr(65+i)}: {col}")

# 关键字段（需要补充的）- 使用实际的列名
key_fields = [
    '苯乙烯含量_wt%',
    '乙烯基含量_mol%',
    '数均分子量 (Mn)',
    '官能化程度_原始数值',
    '官能化程度_原始单位',
    '试剂整体 SMILES',
    '核心官能团 SMILES'
]

print("\n" + "="*60)
print("关键字段缺失统计:")
print("="*60)

for field in key_fields:
    if field in df.columns:
        missing = df[field].isna().sum()
        total = len(df)
        pct = missing / total * 100
        print(f"  {field}: {missing}/{total} 缺失 ({pct:.1f}%)")
    else:
        print(f"  {field}: 列不存在")

# 找出有 DOI_SI 但关键字段缺失的样本
print("\n" + "="*60)
print("有 SI 且关键字段缺失的样本（优先补充）:")
print("="*60)

# 检查 DOI_SI 列
if 'DOI_SI' in df.columns:
    has_si = df['DOI_SI'].notna() & (df['DOI_SI'] != '') & (df['DOI_SI'] != '-')
    
    for idx, row in df[has_si].iterrows():
        sample_id = row.get('样本ID', f'Row-{idx}')
        doi = row.get('DOI', '')
        
        missing_fields = []
        for field in key_fields:
            if field in df.columns and pd.isna(row[field]):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"\n{sample_id} (DOI: {doi})")
            print(f"  缺失: {', '.join(missing_fields)}")
else:
    print("  DOI_SI 列不存在")

# 统计所有样本的缺失情况
print("\n" + "="*60)
print("所有样本缺失详情（按缺失数量排序）:")
print("="*60)

sample_missing = []
for idx, row in df.iterrows():
    sample_id = row.get('样本ID', f'Row-{idx}')
    doi = row.get('DOI', '')
    
    missing_fields = []
    for field in key_fields:
        if field in df.columns and pd.isna(row[field]):
            missing_fields.append(field)
    
    if missing_fields:
        sample_missing.append((sample_id, doi, missing_fields))

# 按缺失数量排序
sample_missing.sort(key=lambda x: len(x[2]), reverse=True)

for sample_id, doi, missing_fields in sample_missing[:20]:  # 只显示前20个
    print(f"\n{sample_id} (DOI: {doi})")
    print(f"  缺失 {len(missing_fields)} 项: {', '.join(missing_fields)}")

if len(sample_missing) > 20:
    print(f"\n... 还有 {len(sample_missing) - 20} 个样本有缺失")
