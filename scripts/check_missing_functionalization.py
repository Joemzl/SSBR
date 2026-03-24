"""检查缺失官能化程度的样本"""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('dataset/数据.xlsx', header=0)

value_col = '官能化程度_原始数值'
unit_col = '官能化程度_原始单位'

# 检查数值列为空的样本
missing = df[df[value_col].isna() | (df[value_col].astype(str).str.strip() == '') | (df[value_col].astype(str).str.strip() == 'nan')]

print(f'缺失官能化程度的样本数: {len(missing)} / {len(df)}')
print('\n缺失样本列表:')
print(missing[['样本ID', '官能化试剂名称', 'DOI', value_col, unit_col]].to_string(index=False))
