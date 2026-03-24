#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查高分子指纹描述符中是否含有不规范的内容（如括号中的解释性文字）
"""

import pandas as pd
from pathlib import Path
import re

DATASET_PATH = Path("d:/SSBR/dataset/数据.xlsx")

df = pd.read_excel(DATASET_PATH)

print("检查高分子指纹描述符中含有括号的记录：")
print("=" * 80)

count = 0
for idx, row in df.iterrows():
    sample_id = row['样本ID']
    fp = str(row.get('高分子指纹描述符', ''))
    
    # 检查是否含有括号（中文或英文）
    if '(' in fp or ')' in fp or '（' in fp or '）' in fp:
        count += 1
        print(f"\n{sample_id}:")
        print(f"  {fp}")

print(f"\n\n共发现 {count} 条含有括号的记录")
print("\n" + "=" * 80)
print("\n所有高分子指纹描述符：")
for idx, row in df.iterrows():
    sample_id = row['样本ID']
    fp = str(row.get('高分子指纹描述符', ''))
    print(f"{sample_id}: {fp}")
