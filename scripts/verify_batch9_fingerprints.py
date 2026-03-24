"""验证刚更新的6个样本的高分子指纹描述符"""
import pandas as pd
from pathlib import Path

excel_path = Path("dataset/数据.xlsx")
df = pd.read_excel(excel_path)

# 要验证的样本
target_samples = ['SSBR-090', 'SSBR-093', 'SSBR-097', 'SSBR-104', 'SSBR-107', 'SSBR-108']

print("=== 验证第九批更新的样本指纹 ===\n")

for sample_id in target_samples:
    row = df[df['样本ID'] == sample_id].iloc[0]
    
    print(f"【{sample_id}】")
    print(f"  官能化试剂: {row['官能化试剂名称']}")
    print(f"  官能化程度: {row['官能化程度_原始数值']} {row['官能化程度_原始单位']}")
    print(f"  指纹描述符: {row['高分子指纹描述符']}")
    print()
