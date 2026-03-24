# -*- coding: utf-8 -*-
"""获取样本详细信息"""
import pandas as pd

df = pd.read_excel('dataset/数据.xlsx')
row = df[df['样本ID'] == 'SSBR-104'].iloc[0]
print('=== SSBR-104 详细信息 ===')
print('引文:', row['引文'])
print('DOI:', row['DOI'])
print('官能化试剂名称:', row['官能化试剂名称'])
