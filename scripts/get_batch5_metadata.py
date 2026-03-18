#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""获取批次5样本的元数据"""

import pandas as pd
import sys
import io

# 设置stdout编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

df = pd.read_excel('dataset/数据.xlsx')
samples = ['SSBR-071', 'SSBR-074', 'SSBR-078', 'SSBR-081']
result = df[df.iloc[:,0].isin(samples)]

print("=" * 80)
print("批次5样本元数据")
print("=" * 80)

for idx, row in result.iterrows():
    print(f"\n### {row.iloc[0]} ###")
    for i, (col, val) in enumerate(zip(df.columns, row)):
        if pd.notna(val):
            try:
                print(f"  [{i}] {col}: {val}")
            except:
                print(f"  [{i}] {col}: [encoding error]")
