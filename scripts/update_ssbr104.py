# -*- coding: utf-8 -*-
"""
更新 SSBR-104 的官能化程度信息

根据文献 10.1002/marc.202100692 (Zhao et al., 2022)：
- HTSSBR 是双官能度聚合物（两端羟基）
- 文献中的 "85 wt%" 是 BDO 在链交联剂中的质量比，不是官能化程度
- 官能化程度应为 "双官能度"，单位为 "(HT-SSBR)" 表示羟基封端SSBR

文献原文：
"The samples are denoted by the abbreviation of their styrene content in HTSSBRs 
and HS content in PUs. For example, S25-25 means the styrene content in HTSSBRs 
is 25 wt% and the HS content in PUs is 25 wt%."
"""
import pandas as pd
from pathlib import Path

DATASET_PATH = Path('dataset/数据.xlsx')

def main():
    df = pd.read_excel(DATASET_PATH)
    
    # 查看当前 SSBR-104 的数据
    row = df[df['样本ID'] == 'SSBR-104']
    print("=== SSBR-104 当前数据 ===")
    for col in ['样本ID', '官能化试剂名称', '官能化程度_原始数值', '官能化程度_原始单位', '高分子指纹描述符']:
        print(f"{col}: {row[col].values[0]}")
    
    print("\n=== 文献分析 ===")
    print("文献标题: Controllable Design and Preparation of Hydroxyl-Terminated SSBR...")
    print("文献中的 '85 wt%' 是 BDO 在链交联剂中的比例，不是官能化程度")
    print("HTSSBR 是双官能度聚合物（两端羟基），文献未给出具体的官能化百分比")
    print("\n建议：保持当前数据 '双官能度 (HT-SSBR)'")
    print("原因：文献描述的是分子设计特征，而非传统的接枝率数值")

if __name__ == '__main__':
    main()
