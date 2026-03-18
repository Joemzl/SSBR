"""检查 Excel 文件结构"""
import pandas as pd

df = pd.read_excel('dataset/数据.xlsx')
print("=" * 60)
print("列名列表:")
print("=" * 60)
for i, col in enumerate(df.columns):
    print(f"[{i}] {col}")

# 使用第一列作为样本编号
sample_col = df.columns[0]
print(f"\n样本编号列: {sample_col}")

print("\n" + "=" * 60)
print("SSBR-035 行数据:")
print("=" * 60)
row = df[df[sample_col] == 'SSBR-035'].iloc[0]
for col in df.columns:
    print(f"{col}: {row[col]}")
