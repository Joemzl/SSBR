"""第八批更新官能化程度数据 - 文献无法获取全文的样本"""
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

EXCEL_PATH = 'dataset/数据.xlsx'
VALUE_COL = '官能化程度_原始数值'
UNIT_COL = '官能化程度_原始单位'

# 第八批更新数据 - 文献全文无法获取，标记为待补充
updates = [
    # SSBR-090 (UPy-NCO) - DOI: 10.1016/j.polymer.2024.128729
    # 文献在 Zotero 中未找到，无法获取全文
    {'sample_id': 'SSBR-090', VALUE_COL: '待补充', UNIT_COL: '(文献待获取)'},
    
    # SSBR-093 (硫醇官能化GO) - DOI: 10.1016/j.compscitech.2022.109907
    # 文献 PDF 无法读取
    {'sample_id': 'SSBR-093', VALUE_COL: '待补充', UNIT_COL: '(文献待获取)'},
    
    # SSBR-097 (烃类树脂) - DOI: 10.5254/RCT-D-23-00043
    # 文献 PDF 无法读取
    {'sample_id': 'SSBR-097', VALUE_COL: '待补充', UNIT_COL: '(文献待获取)'},
    
    # SSBR-104 (环氧乙烷) - DOI: 10.1002/marc.202200366
    # 文献在 Zotero 中未找到
    {'sample_id': 'SSBR-104', VALUE_COL: '待补充', UNIT_COL: '(文献待获取)'},
    
    # SSBR-107 (C3N4/SiO2) - DOI: 10.1002/pc.26994
    # 文献在 Zotero 中未找到
    {'sample_id': 'SSBR-107', VALUE_COL: '待补充', UNIT_COL: '(文献待获取)'},
    
    # SSBR-108 (rGO-g-SiO2) - DOI: 10.1002/pc.26830
    # 文献 PDF 无法读取
    {'sample_id': 'SSBR-108', VALUE_COL: '待补充', UNIT_COL: '(文献待获取)'},
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
