"""更新缺失的接枝反应基团数据 - 第九批（最终批次）"""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 读取 Excel
df = pd.read_excel('dataset/数据.xlsx', header=0)

# 列名
GRAFT_GROUP_COL = '接枝反应基团'
GRAFT_SMILES_COL = '接枝反应基团SMILES'

# 第九批要更新的数据
# 这批样本多为填料改性或添加剂，基于试剂名称的化学性质推断
updates = [
    # SSBR-069: 二苯胍 (DPG)
    # DPG 是硫化促进剂，含有胍基 (=N-C(=NH)-N=)
    # 可与白炭黑表面羟基形成氢键
    {
        'sample_id': 'SSBR-069',
        '接枝反应基团': '胍基（促进剂）',
        '接枝反应基团SMILES': 'NC(=N)N',
    },
    # SSBR-079: EVA 改性白炭黑
    # EVA (乙烯-醋酸乙烯共聚物) 含有乙酸酯基
    {
        'sample_id': 'SSBR-079',
        '接枝反应基团': '乙酸酯基（填料改性）',
        '接枝反应基团SMILES': 'CC(=O)O',
    },
    # SSBR-081: 脂肪酸苄酯
    # 酯类增塑剂，含有苄酯基
    {
        'sample_id': 'SSBR-081',
        '接枝反应基团': '苄酯基（增塑剂）',
        '接枝反应基团SMILES': 'c1ccccc1COC(=O)',
    },
    # SSBR-085: 石墨烯润滑剂
    # 纯石墨烯无活性官能团，仅作物理润滑
    {
        'sample_id': 'SSBR-085',
        '接枝反应基团': '无（物理润滑剂）',
        '接枝反应基团SMILES': '-',
    },
    # SSBR-093: 硫醇官能化氧化石墨烯
    # 硫醇基 (-SH) 与橡胶双键发生硫醇-乙烯基点击反应
    {
        'sample_id': 'SSBR-093',
        '接枝反应基团': '巯基（填料表面改性）',
        '接枝反应基团SMILES': 'S',
    },
    # SSBR-097: 烃类树脂
    # 无活性基团的增粘树脂
    {
        'sample_id': 'SSBR-097',
        '接枝反应基团': '无（增粘树脂）',
        '接枝反应基团SMILES': '-',
    },
    # SSBR-104: 环氧乙烷
    # 链端封端，生成羟基端基
    {
        'sample_id': 'SSBR-104',
        '接枝反应基团': '羟基（链端）',
        '接枝反应基团SMILES': 'O',
    },
    # SSBR-107: C3N4/SiO2 纳米杂化材料
    # 石墨相氮化碳含有氨基和 C-N 键
    {
        'sample_id': 'SSBR-107',
        '接枝反应基团': '氨基（氮化碳表面）',
        '接枝反应基团SMILES': 'N',
    },
    # SSBR-108: 硅氧烷改性氧化石墨烯 (rGO-g-SiO2)
    # 硅氧烷基团改性
    {
        'sample_id': 'SSBR-108',
        '接枝反应基团': '硅氧烷基（填料改性）',
        '接枝反应基团SMILES': '[Si](O)(O)O',
    },
    # SSBR-112: 液体聚丁二烯 (LPB)
    # 低分子量聚丁二烯，含有乙烯基双键
    {
        'sample_id': 'SSBR-112',
        '接枝反应基团': '乙烯基（低聚物）',
        '接枝反应基团SMILES': 'C=C',
    },
]

# 显示当前值
print("=== 更新前 ===")
sample_ids = [u['sample_id'] for u in updates]
cols = ['样本ID', '官能化试剂名称', GRAFT_GROUP_COL, GRAFT_SMILES_COL]
print(df[df['样本ID'].isin(sample_ids)][cols].to_string())

# 更新数据
for update in updates:
    mask = df['样本ID'] == update['sample_id']
    if mask.any():
        df.loc[mask, GRAFT_GROUP_COL] = update['接枝反应基团']
        df.loc[mask, GRAFT_SMILES_COL] = update['接枝反应基团SMILES']
        print(f"已更新 {update['sample_id']}")

# 显示更新后的值
print("\n=== 更新后 ===")
print(df[df['样本ID'].isin(sample_ids)][cols].to_string())

# 保存
df.to_excel('dataset/数据.xlsx', index=False)
print("\n✅ 已保存到 dataset/数据.xlsx")
