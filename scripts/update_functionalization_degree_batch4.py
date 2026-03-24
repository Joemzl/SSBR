"""
第四批官能化程度数据更新脚本
更新样本：SSBR-052, 061, 064, 065, 068, 069
数据来源：Zotero 文献全文提取
"""

import pandas as pd
from pathlib import Path

# 配置
EXCEL_PATH = Path(__file__).parent.parent / "dataset" / "数据.xlsx"
VALUE_COL = "官能化程度_原始数值"
UNIT_COL = "官能化程度_原始单位"

# 第四批更新数据
updates = [
    # SSBR-052: 烷氧基硅烷 - 端基官能化效率71-76%
    # 来源: WED5BB3X - "end-functionalized efficiency reaches 71-76%"
    {'sample_id': 'SSBR-052', VALUE_COL: '71-76', UNIT_COL: '% (端基官能化效率)'},
    
    # SSBR-061: APTES - 封端效率86%
    # 来源: JAJGH3KV - Table 1 "APTES 0.05 ml", end-capping efficiency 86%
    {'sample_id': 'SSBR-061', VALUE_COL: '86', UNIT_COL: '% (封端效率)'},
    
    # SSBR-064: PPD-GO - 1-5 phr
    # 来源: 6X3JBY25 - Table 1 shows PPD-GO content 1-5 phr
    {'sample_id': 'SSBR-064', VALUE_COL: '1-5', UNIT_COL: 'phr'},
    
    # SSBR-065: TAD - 最高5.32 mol% (相对双键)
    # 来源: 6YQAZ6LD - "TAD grafting ratio up to 5.32%"
    {'sample_id': 'SSBR-065', VALUE_COL: '最高5.32', UNIT_COL: 'mol% (vs 双键)'},
    
    # SSBR-068: XSBR - 3 wt%
    # 来源: EIPI79IH - "XSBR used at 50 phr MEG" → 3 wt% XSBR/MEG composite
    {'sample_id': 'SSBR-068', VALUE_COL: '3', UNIT_COL: 'wt%'},
    
    # SSBR-069: DPG - 135.25 mmol/kg (vs SiO2)
    # 来源: X9ARSBPY - Table 1 "DNS-DPG-3: 135.25 mmol/kg SiO2"
    {'sample_id': 'SSBR-069', VALUE_COL: '135.25', UNIT_COL: 'mmol/kg (vs SiO2)'},
]

def main():
    print(f"读取 Excel 文件: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH)
    
    print(f"总样本数: {len(df)}")
    print(f"目标列: {VALUE_COL}, {UNIT_COL}")
    print()
    
    updated_count = 0
    for update in updates:
        sample_id = update['sample_id']
        mask = df['样本ID'] == sample_id
        
        if mask.sum() == 0:
            print(f"[X] {sample_id}: 未找到")
            continue
        
        old_value = df.loc[mask, VALUE_COL].iloc[0]
        old_unit = df.loc[mask, UNIT_COL].iloc[0]
        
        # 检查是否已有数据
        if pd.notna(old_value) and str(old_value).strip():
            print(f"[!] {sample_id}: 已有数据 ({old_value} {old_unit})，跳过")
            continue
        
        # 更新数据
        df.loc[mask, VALUE_COL] = update[VALUE_COL]
        df.loc[mask, UNIT_COL] = update[UNIT_COL]
        
        print(f"[OK] {sample_id}: {update[VALUE_COL]} {update[UNIT_COL]}")
        updated_count += 1
    
    print()
    print(f"更新了 {updated_count} 个样本")
    
    # 保存
    if updated_count > 0:
        df.to_excel(EXCEL_PATH, index=False)
        print(f"已保存到: {EXCEL_PATH}")
    else:
        print("无需保存")

if __name__ == "__main__":
    main()
