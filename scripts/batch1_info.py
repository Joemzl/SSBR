"""批次1样本信息"""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('dataset/数据.xlsx')

batch1 = ['SSBR-042', 'SSBR-043', 'SSBR-044', 'SSBR-015', 'SSBR-016', 
          'SSBR-019', 'SSBR-013', 'SSBR-014', 'SSBR-046', 'SSBR-007']

print("=" * 80)
print("批次 1 样本详情 (10 个样本)")
print("=" * 80)

# 按 DOI 分组
b1_df = df[df['样本ID'].isin(batch1)]

for doi, group in b1_df.groupby('DOI'):
    samples = group['样本ID'].tolist()
    reagent = group['官能化试剂名称'].iloc[0]
    chain = group['是否是链中官能化'].iloc[0]
    print(f"\n【DOI: {doi}】")
    print(f"  样本: {samples}")
    print(f"  官能化试剂: {reagent}")
    print(f"  链中官能化: {chain}")

print("\n" + "=" * 80)
print("DOI 列表 (按样本数排序):")
print("=" * 80)
doi_counts = b1_df.groupby('DOI').size().sort_values(ascending=False)
for doi, count in doi_counts.items():
    print(f"{count} 个样本: {doi}")
