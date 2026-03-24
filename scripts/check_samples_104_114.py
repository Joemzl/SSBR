#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_excel('d:/SSBR/dataset/数据.xlsx')
samples = df[df['样本ID'].isin(['SSBR-104', 'SSBR-114'])]

for idx, row in samples.iterrows():
    print(f"\n{'='*60}")
    print(f"样本ID: {row['样本ID']}")
    print(f"DOI: {row.get('DOI', '-')}")
    print(f"引文: {row.get('引文', '-')}")
    print(f"官能化试剂名称: {row.get('官能化试剂名称', '-')}")
    print(f"官能化程度_原始数值: {row.get('官能化程度_原始数值', '-')}")
    print(f"官能化程度_原始单位: {row.get('官能化程度_原始单位', '-')}")
