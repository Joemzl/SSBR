"""
第五批官能化程度数据更新脚本
更新样本：SSBR-071, 075, 079, 081, 085, 086
数据来源：Zotero 文献全文提取
"""

import pandas as pd
from pathlib import Path

# 配置
EXCEL_PATH = Path(__file__).parent.parent / "dataset" / "数据.xlsx"
VALUE_COL = "官能化程度_原始数值"
UNIT_COL = "官能化程度_原始单位"

# 第五批更新数据
updates = [
    # SSBR-071: Si747 - 9 phr
    # 来源: D63LFM29 - Table I "Silane (Si747) 9.0 phr", silica 80 phr
    {'sample_id': 'SSBR-071', VALUE_COL: '9', UNIT_COL: 'phr'},
    
    # SSBR-075: TESPT - 8.1 phr / 9 wt% vs SiO2
    # 来源: J2EXIFQ4 - Table 1 "TESPT 8.1 phr", silica 90 phr (即约 9 wt%)
    {'sample_id': 'SSBR-075', VALUE_COL: '8.1', UNIT_COL: 'phr'},
    
    # SSBR-079: EVA改性白炭黑 - 文献仅表述EVA固含量40%用于包覆
    # 来源: IULL4IWX - "EVA with a solid content of around 40%"
    {'sample_id': 'SSBR-079', VALUE_COL: '40', UNIT_COL: '% (EVA固含量)'},
    
    # SSBR-081: 脂肪酸苄酯 - 20 phr 作为增塑剂
    # 来源: Z4UEHRFD - Table 2 "fatty acid benzyl esters 20 phr"
    {'sample_id': 'SSBR-081', VALUE_COL: '20', UNIT_COL: 'phr'},
    
    # SSBR-085: 石墨烯润滑剂 - 外部润滑剂非配方添加
    # 来源: L432E5AV - graphene lubricant used as external lubricant for mixer
    {'sample_id': 'SSBR-085', VALUE_COL: '外部润滑剂', UNIT_COL: '-'},
    
    # SSBR-086: 胺封端TBIR - 10 phr, 封端效率10-60 mol%
    # 来源: XYYJ6G8Y - Table 2 "TBIR or F-TBIR 10 phr", CE = 10-60 mol%
    {'sample_id': 'SSBR-086', VALUE_COL: '10', UNIT_COL: 'phr (封端效率10-60 mol%)'},
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
