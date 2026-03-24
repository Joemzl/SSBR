"""更新缺失的官能化程度数据 - 第二批
基于 Zotero 文献检索结果提取的数据
"""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 读取 Excel
df = pd.read_excel('dataset/数据.xlsx', header=0)

# 列名
VALUE_COL = '官能化程度_原始数值'
UNIT_COL = '官能化程度_原始单位'

# 第二批要更新的数据
updates = [
    # SSBR-033: 1,5-萘二异氰酸酯 (NDI) - DOI 10.3389/fchem.2018.00240
    # 文献描述使用 HTSSBR (~3000 Mn) 与 NDI 合成聚氨酯，未给出 NDI 具体用量
    {
        'sample_id': 'SSBR-033',
        VALUE_COL: '未公开',
        UNIT_COL: '-',
    },
    # SSBR-038: 1-庚硫醇、1-十八烷硫醇 - DOI 10.1016/j.compscitech.2018.03.036
    # TGA 显示 alkanethiol 接枝含量: C7GO 12.8 wt%, C18GO 14.0 wt%
    # 文献使用 0.5-3 phr CxGO，选择最优 C18GO 接枝率
    {
        'sample_id': 'SSBR-038',
        VALUE_COL: '14.0',
        UNIT_COL: 'wt% (on GO)',
    },
    # SSBR-040: 六甲基二硅氮烷 (HMDS) - DOI 10.1016/j.compscitech.2020.108482
    # 文献研究了 10%, 20%, 30%, 40% HMDS 质量分数，HB220 (20%) 表现最优
    {
        'sample_id': 'SSBR-040',
        VALUE_COL: '20',
        UNIT_COL: 'wt% (of silica)',
    },
    # SSBR-041: N-(4-苯胺基苯基)马来酰亚胺 (MC) - DOI 10.1016/j.matdes.2018.05.048
    # TGA 显示 KH590-MC 接枝含量约 9.4 wt%
    {
        'sample_id': 'SSBR-041',
        VALUE_COL: '9.4',
        UNIT_COL: 'wt% (on silica)',
    },
    # SSBR-042: AMMO - DOI 10.1002/app.28621
    # 文献明确: "the mass fraction of AMMO was 7% of the mass of the nanosilica powder"
    {
        'sample_id': 'SSBR-042',
        VALUE_COL: '7',
        UNIT_COL: 'wt% (of silica)',
    },
    # SSBR-043: AMMO - 同上
    {
        'sample_id': 'SSBR-043',
        VALUE_COL: '7',
        UNIT_COL: 'wt% (of silica)',
    },
    # SSBR-044: AMMO - 同上
    {
        'sample_id': 'SSBR-044',
        VALUE_COL: '7',
        UNIT_COL: 'wt% (of silica)',
    },
    # SSBR-045: 3-辛酰硫基-1-丙基三乙氧基硅烷 - DOI 10.1002/app.29646
    # 文献未给出硅烷偶联剂的具体用量
    {
        'sample_id': 'SSBR-045',
        VALUE_COL: '未公开',
        UNIT_COL: '-',
    },
]

# 更新数据
updated_count = 0
for update in updates:
    sample_id = update['sample_id']
    mask = df['样本ID'] == sample_id
    if mask.sum() == 1:
        df.loc[mask, VALUE_COL] = update[VALUE_COL]
        df.loc[mask, UNIT_COL] = update[UNIT_COL]
        print(f"✓ 更新 {sample_id}: {update[VALUE_COL]} {update[UNIT_COL]}")
        updated_count += 1
    else:
        print(f"✗ 样本 {sample_id} 未找到或有重复")

# 保存
if updated_count > 0:
    df.to_excel('dataset/数据.xlsx', index=False)
    print(f"\n已更新 {updated_count} 个样本")
else:
    print("\n没有需要更新的数据")
