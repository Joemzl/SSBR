"""获取批次1样本的完整元数据"""
import pandas as pd
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('dataset/数据.xlsx')

# 获取指定样本的元数据
sample_ids = ['SSBR-042', 'SSBR-043', 'SSBR-044']
samples = df[df['样本ID'].isin(sample_ids)]

for _, row in samples.iterrows():
    print("=" * 80)
    print(f"样本 ID: {row['样本ID']}")
    print("=" * 80)
    for col in df.columns:
        val = row[col]
        if pd.notna(val):
            print(f"  {col}: {val}")
    print()
