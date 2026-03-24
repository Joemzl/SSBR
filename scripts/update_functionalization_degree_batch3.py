#!/usr/bin/env python3
"""
批量更新官能化程度 - 第三批
基于文献检索结果
"""

import pandas as pd
import os

# 配置
EXCEL_PATH = r'd:\SSBR\dataset\数据.xlsx'
VALUE_COL = '官能化程度_原始数值'
UNIT_COL = '官能化程度_原始单位'

# 第三批更新数据 (基于文献检索结果)
updates = [
    # SSBR-046: Si-75 用量为白炭黑质量的7%
    # 文献: "the mass fraction of Si-75 is 7% of the mass of the nano-SiO2 powder"
    {'sample_id': 'SSBR-046', VALUE_COL: '7', UNIT_COL: 'wt% (vs SiO2)'},
    
    # SSBR-047: TESPT/TESPD 用量为白炭黑质量的10%
    # 文献: "Ten grams of SCA (the mass of SCA accounts for 10% of the mass of silica particles)"
    {'sample_id': 'SSBR-047', VALUE_COL: '10', UNIT_COL: 'wt% (vs SiO2)'},
    
    # SSBR-048: 氨基丙基三甲氧基硅烷 用量为白炭黑质量的7%
    # 文献: "The [3-(2-aminoethyl)aminopropyl] trimethoxysilane amount was 7% of the mass of nanosilica powder"
    {'sample_id': 'SSBR-048', VALUE_COL: '7', UNIT_COL: 'wt% (vs SiO2)'},
    
    # SSBR-049: TESPT 用量为白炭黑质量的8%
    # 文献: "TESPT (8% w/w of silica) 6.4" 配方表
    {'sample_id': 'SSBR-049', VALUE_COL: '8', UNIT_COL: 'wt% (vs SiO2)'},
    
    # SSBR-050: 环氧乙烷用于链端官能化，但文献未给出具体用量
    {'sample_id': 'SSBR-050', VALUE_COL: '未公开', UNIT_COL: '-'},
    
    # SSBR-051: TBCSi 端基封端效率约0.51-0.71
    # 文献: end-capping efficiency: A2=0.54, A3=0.51, A4=0.71
    {'sample_id': 'SSBR-051', VALUE_COL: '51-71', UNIT_COL: '% (封端效率)'},
]

def main():
    # 读取Excel
    df = pd.read_excel(EXCEL_PATH)
    
    updated_count = 0
    
    for update in updates:
        sample_id = update['sample_id']
        mask = df['样本ID'] == sample_id
        
        if mask.any():
            df.loc[mask, VALUE_COL] = update[VALUE_COL]
            df.loc[mask, UNIT_COL] = update[UNIT_COL]
            print(f"[OK] 更新 {sample_id}: {update[VALUE_COL]} {update[UNIT_COL]}")
            updated_count += 1
        else:
            print(f"[X] 未找到样本: {sample_id}")
    
    # 保存
    df.to_excel(EXCEL_PATH, index=False)
    print(f"\n已更新 {updated_count} 个样本")

if __name__ == '__main__':
    main()
