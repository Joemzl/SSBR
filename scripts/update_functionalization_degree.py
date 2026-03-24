"""更新缺失的官能化程度数据 - 第一批"""
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 读取 Excel
df = pd.read_excel('dataset/数据.xlsx', header=0)

# 列名
VALUE_COL = '官能化程度_原始数值'
UNIT_COL = '官能化程度_原始单位'

# 第一批要更新的数据
updates = [
    # SSBR-017: TMPMP - DOI 10.1021/acs.iecr.6b04146
    # TMPMP 用量为 4 phr (相对于 SiR 100 phr)
    {
        'sample_id': 'SSBR-017',
        VALUE_COL: '4',
        UNIT_COL: 'phr (vs SiR)',
    },
    # SSBR-018: DPE-NMe2 (α-SSBR) - DOI 10.1021/acs.iecr.8b05738
    # DPE-(NMe2)2 含量 0.09 wt%, 端封效率 83%
    {
        'sample_id': 'SSBR-018',
        VALUE_COL: '0.09',
        UNIT_COL: 'wt%',
    },
    # SSBR-021: DPE-NMe2 (IC-SSBR) - DOI 10.1021/acs.iecr.8b05738
    # DPE-NMe2 含量 4.8 wt%
    {
        'sample_id': 'SSBR-021',
        VALUE_COL: '4.8',
        UNIT_COL: 'wt%',
    },
    # SSBR-025: 丙胺, 二甲氧基硅烷 - DOI 10.1002/app.48696
    # 具体官能化程度未公开
    {
        'sample_id': 'SSBR-025',
        VALUE_COL: '未公开',
        UNIT_COL: '-',
    },
    # SSBR-026: β-月桂烯 - DOI 10.1002/app.48159
    # 月桂烯含量 30.1 wt% (St:My:Bd = 3:3:4)
    {
        'sample_id': 'SSBR-026',
        VALUE_COL: '30.1',
        UNIT_COL: 'wt%',
    },
    # SSBR-036: 双环氧丙基多硫化物 (BEP) - DOI 10.1016/j.compositesb.2020.108301
    # BEP 用量 3-7 phr (最优 B3T4 配方使用 3 phr)
    {
        'sample_id': 'SSBR-036',
        VALUE_COL: '3',
        UNIT_COL: 'phr',
    },
    # SSBR-078: β-月桂烯 (与 SSBR-026 同试剂)
    # 假设同样条件，月桂烯含量 ~30 wt%
    {
        'sample_id': 'SSBR-078',
        VALUE_COL: '30',
        UNIT_COL: 'wt%',
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
