"""
查看指定样本的详细信息
"""
import pandas as pd
from pathlib import Path
import sys

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')

# 读取数据
excel_path = Path(__file__).parent.parent / "dataset" / "数据.xlsx"
df = pd.read_excel(excel_path)

# 查找 SSBR-012
sample = df[df['样本ID'] == 'SSBR-012']

if len(sample) > 0:
    row = sample.iloc[0]
    print("SSBR-012 详细信息:")
    print("=" * 50)
    for col in df.columns:
        value = row[col]
        if pd.isna(value):
            print(f"  {col}: [缺失]")
        else:
            print(f"  {col}: {value}")
else:
    print("未找到 SSBR-012")
