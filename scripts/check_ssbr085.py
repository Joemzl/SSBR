#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查 SSBR-085 删除情况"""

import pandas as pd

df = pd.read_excel('dataset/数据.xlsx')
print(f"当前样本数: {len(df)}")
print(f"SSBR-085 是否存在: {'SSBR-085' in df['样本ID'].values}")

# 检查 SSBR-104 和 SSBR-114 的当前官能化程度数据
for sample_id in ['SSBR-104', 'SSBR-114']:
    if sample_id in df['样本ID'].values:
        row = df[df['样本ID'] == sample_id].iloc[0]
        print(f"\n{sample_id}:")
        print(f"  官能化程度_原始数值: {row['官能化程度_原始数值']}")
        print(f"  官能化程度_原始单位: {row['官能化程度_原始单位']}")
