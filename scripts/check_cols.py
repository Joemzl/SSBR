"""检查 Excel 列结构"""
import pandas as pd

df = pd.read_excel('dataset/数据.xlsx')
print("Excel 列索引:")
for i, c in enumerate(df.columns):
    print(f"[{i}] {c}")
