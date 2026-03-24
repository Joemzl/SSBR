#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查官能化程度_原始数值 和 官能化程度_原始单位 两列的内容
"""

import pandas as pd
from pathlib import Path

DATASET_PATH = Path("d:/SSBR/dataset/数据.xlsx")

df = pd.read_excel(DATASET_PATH)

print("=" * 80)
print("官能化程度_原始数值 列内容")
print("=" * 80)

val_col = '官能化程度_原始数值'
unit_col = '官能化程度_原始单位'

# 找出非纯数字的数值
print("\n非纯数字的「官能化程度_原始数值」:")
print("-" * 60)
for idx, row in df.iterrows():
    val = str(row.get(val_col, ''))
    # 检查是否包含中文或非数字字符（除了小数点和连字符）
    import re
    if val and val != 'nan' and val != '-':
        # 纯数字模式: 只含数字、小数点、连字符
        if not re.match(r'^[\d\.\-]+$', val):
            print(f"{row['样本ID']}: {val}")

print("\n" + "=" * 80)
print("官能化程度_原始单位 列内容")
print("=" * 80)

# 找出含有括号的单位
print("\n含有括号的「官能化程度_原始单位」:")
print("-" * 60)
for idx, row in df.iterrows():
    unit = str(row.get(unit_col, ''))
    if '(' in unit or '（' in unit:
        print(f"{row['样本ID']}: {unit}")

print("\n" + "=" * 80)
print("所有样本的官能化程度数据")
print("=" * 80)
print(f"\n{'样本ID':<12} {'原始数值':<25} {'原始单位':<30}")
print("-" * 70)
for idx, row in df.iterrows():
    sample_id = row['样本ID']
    val = str(row.get(val_col, '-'))
    unit = str(row.get(unit_col, '-'))
    print(f"{sample_id:<12} {val:<25} {unit:<30}")
