import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('d:/SSBR/dataset/数据.xlsx')

# 查看 SSBR-017 和 SSBR-020 的详细信息
samples = df[df['样本ID'].isin(['SSBR-017', 'SSBR-020'])]
print("SSBR-017 和 SSBR-020 详细信息:")
for idx, row in samples.iterrows():
    print(f"\n{'='*50}")
    print(f"样本ID: {row['样本ID']}")
    print(f"官能化试剂名称: {row['官能化试剂名称']}")
    print(f"是否是链中官能化: {row['是否是链中官能化']}")
