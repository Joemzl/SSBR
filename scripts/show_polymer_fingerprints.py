"""显示所有样本的高分子指纹描述符"""
import pandas as pd
from pathlib import Path

excel_path = Path("dataset/数据.xlsx")
df = pd.read_excel(excel_path)

col = "高分子指纹描述符"
sample_col = "样本ID"

print("=== 所有样本的高分子指纹描述符 ===\n")
for _, row in df.iterrows():
    sample_id = row[sample_col]
    fingerprint = row[col]
    print(f"{sample_id}: {fingerprint}")
