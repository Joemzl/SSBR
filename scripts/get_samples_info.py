# -*- coding: utf-8 -*-
"""获取多个样本的详细信息"""
import pandas as pd

df = pd.read_excel('dataset/数据.xlsx')
samples = ['SSBR-025', 'SSBR-033', 'SSBR-045', 'SSBR-050', 'SSBR-114']

for sample_id in samples:
    row = df[df['样本ID'] == sample_id]
    if len(row) > 0:
        row = row.iloc[0]
        print(f"=== {sample_id} ===")
        print(f"引文: {row['引文']}")
        print(f"DOI: {row['DOI']}")
        print(f"官能化试剂: {row['官能化试剂名称']}")
        print(f"官能化程度_原始数值: {row['官能化程度_原始数值']}")
        print(f"官能化程度_原始单位: {row['官能化程度_原始单位']}")
        print()
