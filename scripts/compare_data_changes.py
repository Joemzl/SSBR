#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""对比 Excel 数据变化，找出需要更新解读文档的样本"""

import pandas as pd
from pathlib import Path
import json

# 读取当前数据
df = pd.read_excel('dataset/数据.xlsx')
print(f"当前样本数: {len(df)}")
print(f"列数: {len(df.columns)}")
print(f"列名: {list(df.columns)}")

# 列出所有样本及其关键字段
print("\n" + "="*80)
print("所有样本的关键数据字段：")
print("="*80)

key_columns = [
    '样本ID', '官能化方式', '接枝反应基团', '官能化程度_原始数值', '官能化程度_原始单位',
    '白�ite黑用量_phr', '偶联剂类型', '偶联剂用量_phr'
]

# 检查实际存在的列名
actual_columns = ['样本ID']
for col in df.columns:
    if '官能化' in col or '白炭黑' in col or '偶联剂' in col or '接枝' in col:
        actual_columns.append(col)

print(f"\n关键列: {actual_columns}")

# 输出每个样本的关键数据
for idx, row in df.iterrows():
    sample_id = row['样本ID']
    print(f"\n{sample_id}:")
    for col in actual_columns[1:]:  # 跳过样本ID
        val = row.get(col, 'N/A')
        if pd.notna(val) and val != '':
            print(f"  {col}: {val}")
