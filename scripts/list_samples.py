import pandas as pd
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_excel('d:/SSBR/dataset/数据.xlsx')

# 已完成的样本（检查目录中有文件的）
interp_dir = 'd:/SSBR/dataset/interpretations'
done = []
for folder in os.listdir(interp_dir):
    folder_path = os.path.join(interp_dir, folder)
    if os.path.isdir(folder_path) and folder.startswith('SSBR-'):
        files = os.listdir(folder_path)
        if len(files) >= 5:  # 有5个文件才算完成
            done.append(folder)

# 筛选链中官能化样本
chain_func = df[df['是否是链中官能化'] == '是']

print(f"已完成样本 ({len(done)} 个): {sorted(done)}")
print(f"\n待生成样本（按 DOI 分组）:")
print("=" * 70)

pending_count = 0
for doi, group in chain_func.groupby('DOI'):
    samples = group['样本ID'].tolist()
    pending = [s for s in samples if s not in done]
    if pending:
        pending_count += len(pending)
        print(f"\nDOI: {doi}")
        print(f"  待生成: {pending}")
        print(f"  试剂: {group['官能化试剂名称'].unique().tolist()}")

print(f"\n总计待生成: {pending_count} 个样本")
