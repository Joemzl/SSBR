"""检查有官能化试剂但缺少接枝反应基团的样本"""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 读取 Excel - 第一行是标题行，第二行是表头
df = pd.read_excel('dataset/数据.xlsx', header=0)

print("=== 检查缺失接枝反应基团的样本 ===\n")

# 列名
reagent_col = '官能化试剂名称'
graft_col = '接枝反应基团'
sample_col = '样本ID'
doi_col = 'DOI'

# 筛选：有官能化试剂但没有接枝反应基团的样本
mask = df[reagent_col].notna() & df[reagent_col].astype(str).str.strip().ne('') & \
       (df[graft_col].isna() | df[graft_col].astype(str).str.strip().eq(''))

missing_samples = df[mask][[sample_col, reagent_col, graft_col, doi_col]]

print(f"找到 {len(missing_samples)} 个样本有官能化试剂但缺少接枝反应基团：\n")
if len(missing_samples) > 0:
    for _, row in missing_samples.iterrows():
        print(f"  {row[sample_col]}: 试剂={row[reagent_col]}, DOI={row[doi_col]}")
else:
    print("  所有样本的接枝反应基团都已填写！")
    
# 也检查一下有多少样本有接枝反应基团
has_graft = df[graft_col].notna() & df[graft_col].astype(str).str.strip().ne('')
print(f"\n统计: {has_graft.sum()}/{len(df)} 个样本有接枝反应基团")
