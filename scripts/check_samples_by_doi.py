"""
从 Zotero 文献中提取的数据，用于补充 Excel 中的缺失字段
"""
import pandas as pd
from pathlib import Path

# 读取数据
excel_path = Path(__file__).parent.parent / "dataset" / "数据.xlsx"
df = pd.read_excel(excel_path)

# 查找 DOI 为 10.1039/c9ra02783a 的样本
doi_target = "10.1039/c9ra02783a"
samples = df[df['DOI'] == doi_target]

print(f"DOI: {doi_target}")
print(f"找到 {len(samples)} 个样本:\n")

for idx, row in samples.iterrows():
    print(f"样本ID: {row['样本ID']}")
    print(f"  官能化试剂名称: {row['官能化试剂名称']}")
    print(f"  苯乙烯含量_wt%: {row['苯乙烯含量_wt%']}")
    print(f"  乙烯基含量_mol%: {row['乙烯基含量_mol%']}")
    print(f"  数均分子量 (Mn): {row['数均分子量 (Mn)']}")
    print()
