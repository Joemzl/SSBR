"""第七批更新官能化程度数据"""
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

EXCEL_PATH = 'dataset/数据.xlsx'
VALUE_COL = '官能化程度_原始数值'
UNIT_COL = '官能化程度_原始单位'

# 第七批更新数据 - 基于文献全文提取
updates = [
    # SSBR-092 (TGDY) - DOI: 10.1016/j.compscitech.2022.109438
    # Table S1 配方: TGDY 1 phr (作为促进剂和填料分散剂)
    {'sample_id': 'SSBR-092', VALUE_COL: '1', UNIT_COL: 'phr'},
    
    # SSBR-100 (ENR) - DOI: 10.1002/app.52682
    # Table 1: ENR50/NR = 20/80 到 40/60，ENR用量 20-40 phr
    # ENR 环氧化度 33% 或 50%
    {'sample_id': 'SSBR-100', VALUE_COL: '20-40', UNIT_COL: 'phr (ENR50)'},
    
    # SSBR-101 (ESSBR) - DOI: 10.1002/app.70577
    # "The amounts of ESSBR used were 2.5%, 5%, 7.5%, and 10% of the mass of SiO2"
    {'sample_id': 'SSBR-101', VALUE_COL: '2.5-10', UNIT_COL: '% (vs SiO2)'},
]

def main():
    df = pd.read_excel(EXCEL_PATH, header=0)
    print(f'读取 Excel: {len(df)} 行')
    
    updated = 0
    for item in updates:
        sample_id = item['sample_id']
        mask = df['样本ID'] == sample_id
        
        if mask.sum() == 0:
            print(f'[X] 未找到样本: {sample_id}')
            continue
        
        df.loc[mask, VALUE_COL] = item[VALUE_COL]
        df.loc[mask, UNIT_COL] = item[UNIT_COL]
        print(f'[OK] {sample_id}: {item[VALUE_COL]} {item[UNIT_COL]}')
        updated += 1
    
    df.to_excel(EXCEL_PATH, index=False)
    print(f'\n已更新 {updated} 个样本')

if __name__ == '__main__':
    main()
