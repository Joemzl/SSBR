"""批次 2 样本完整信息"""
import pandas as pd
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

df = pd.read_excel('dataset/数据.xlsx')

# 批次 2 样本列表
batch2_samples = ['SSBR-035', 'SSBR-036', 'SSBR-039', 'SSBR-050', 'SSBR-051', 
                  'SSBR-053', 'SSBR-054', 'SSBR-056', 'SSBR-057', 'SSBR-060']

print("=" * 80)
print("批次 2 样本详细信息 (共 {} 个样本)".format(len(batch2_samples)))
print("=" * 80)

for sample_id in batch2_samples:
    row = df[df['样本ID'] == sample_id]
    if len(row) > 0:
        row = row.iloc[0]
        print(f"\n### {sample_id}")
        print(f"DOI: {row['DOI']}")
        print(f"是否链中官能化: {row['是否是链中官能化']}")
        print(f"苯乙烯含量: {row['苯乙烯含量_wt%']} wt%")
        print(f"乙烯基含量: {row['乙烯基含量_mol%']} mol%")
        print(f"Mn: {row['数均分子量 (Mn)']}")
        print(f"应用场景: {row['应用场景']}")
        print(f"官能化试剂: {row['官能化试剂名称']}")
        print(f"核心官能团: {row['核心官能团名称']}")
        print(f"官能化程度: {row['官能化程度_原始数值']} {row['官能化程度_原始单位']}")
        print(f"核磁谱图: {row['核磁谱图']}")
        print(f"TEM图: {row['微相分离图片表征']}")
        print(f"力学图谱: {row['核心力学图谱']}")
        print(f"DSC谱图: {row['DSC 谱图']}")
        print(f"引文: {row['引文']}")
        print("-" * 80)
    else:
        print(f"\n### {sample_id}: 未找到")
