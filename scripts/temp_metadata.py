"""获取指定样本的元数据"""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('dataset/数据.xlsx')
sample_id = 'SSBR-035'
row = df[df.iloc[:,0] == sample_id]
if not row.empty:
    print(f"\n===== {sample_id} 元数据 =====")
    for i, col in enumerate(df.columns):
        val = row.iloc[0, i]
        if pd.notna(val):
            print(f"[{i}] {col}: {val}")
else:
    print(f"未找到 {sample_id}")
