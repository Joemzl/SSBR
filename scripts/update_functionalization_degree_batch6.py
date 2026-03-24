"""第六批更新官能化程度数据"""
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

EXCEL_PATH = 'dataset/数据.xlsx'
VALUE_COL = '官能化程度_原始数值'
UNIT_COL = '官能化程度_原始单位'

# 第六批更新数据 - 基于文献全文提取
updates = [
    # SSBR-112 (LPB) - DOI: 10.1002/pen.25931
    # Table 2 配方显示：LPB 12 wt% 替代 TDAE 作为环保增塑剂
    {'sample_id': 'SSBR-112', VALUE_COL: '12', UNIT_COL: 'wt%'},
    
    # SSBR-114 (VTMS) - DOI: 10.1007/s10965-023-03446-7
    # 文献："add a certain volume of VTMO (nVTMO=n-CH=CH2 of SSBR)"
    # VTMS用量与SSBR主链双键等摩尔，催化剂仅0.01‰
    {'sample_id': 'SSBR-114', VALUE_COL: '等摩尔', UNIT_COL: '(vs 双键)'},
    
    # SSBR-116 (mCPBA) - DOI: 10.1002/vnl.22007
    # 合成 ESSBR-x (x=5,10,15,20,30)，x为环氧化双键摩尔比
    # 文献："x represents the molar percentage of the epoxidized butadiene units"
    # 研究发现 ESSBR-15% 效果最佳
    {'sample_id': 'SSBR-116', VALUE_COL: '5-30', UNIT_COL: '% (环氧化双键摩尔比)'},
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
