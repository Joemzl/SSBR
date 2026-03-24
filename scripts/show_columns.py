"""查看 Excel 列名"""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('dataset/数据.xlsx', header=0)
print("=== Excel 列名 ===")
for i, col in enumerate(df.columns):
    print(f"  {i}: [{col}] -> repr: {repr(col)}")
