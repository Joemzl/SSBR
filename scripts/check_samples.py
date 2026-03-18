"""检查 Excel 中的样本与 interpretations 目录的差异，并分析待生成样本"""
import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 读取 Excel 中的样本 ID
df = pd.read_excel('dataset/数据.xlsx')
excel_samples = df.iloc[:, 0].tolist()

# 获取 interpretations 目录中的样本
interp_dir = 'dataset/interpretations'
interp_samples = [f for f in os.listdir(interp_dir) 
                  if os.path.isdir(os.path.join(interp_dir, f)) and f.startswith('SSBR-')]

# 统计完成状态
done_samples = []
for s in interp_samples:
    sample_dir = os.path.join(interp_dir, s)
    files = [f for f in os.listdir(sample_dir) if f.endswith('.md')]
    if len(files) >= 5:
        done_samples.append(s)

done_set = set(done_samples)

# 筛选未完成的样本
pending_df = df[~df['样本ID'].isin(done_set)]

print("=" * 80)
print("待生成解读的 65 个样本分布分析")
print("=" * 80)

# 按 DOI 分组分析
print(f"\n📊 按 DOI 分组统计 (共 {pending_df['DOI'].nunique()} 篇文献):\n")

doi_groups = []
for doi, group in pending_df.groupby('DOI'):
    samples = group['样本ID'].tolist()
    reagents = group['官能化试剂名称'].unique().tolist()
    is_chain = group['是否是链中官能化'].unique().tolist()
    doi_groups.append({
        'DOI': doi,
        '样本数': len(samples),
        '样本列表': samples,
        '官能化试剂': reagents,
        '是否链中官能化': is_chain
    })

# 按样本数排序
doi_groups.sort(key=lambda x: x['样本数'], reverse=True)

for i, g in enumerate(doi_groups, 1):
    print(f"【文献 {i}】DOI: {g['DOI']}")
    print(f"    样本数: {g['样本数']} 个")
    print(f"    样本: {g['样本列表']}")
    print(f"    官能化试剂: {g['官能化试剂']}")
    print(f"    链中官能化: {g['是否链中官能化']}")
    print()

# 汇总统计
print("=" * 80)
print("📈 汇总统计")
print("=" * 80)
print(f"待生成样本总数: {len(pending_df)} 个")
print(f"涉及文献数: {len(doi_groups)} 篇")
print(f"平均每篇文献样本数: {len(pending_df) / len(doi_groups):.1f} 个")

# 按官能化试剂统计
print(f"\n📌 按官能化试剂统计:")
reagent_counts = pending_df['官能化试剂名称'].value_counts()
for reagent, count in reagent_counts.items():
    print(f"    {reagent}: {count} 个样本")

# 输出 DOI 列表供 Zotero 查询
print("\n" + "=" * 80)
print("📚 DOI 列表 (供 Zotero 查询):")
print("=" * 80)
for g in doi_groups:
    print(g['DOI'])
