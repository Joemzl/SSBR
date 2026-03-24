#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""更新 SSBR-104 和 SSBR-114 的官能化程度为「未公开」，并确认 SSBR-085 删除"""

import pandas as pd
from pathlib import Path

excel_path = Path('dataset/数据.xlsx')

# 读取数据
df = pd.read_excel(excel_path)
print(f"当前样本数: {len(df)}")

# 确认 SSBR-085 是否已删除
if 'SSBR-085' in df['样本ID'].values:
    print("⚠️ SSBR-085 仍在 Excel 中")
else:
    print("[OK] SSBR-085 已从 Excel 中删除")

# 更新 SSBR-104 和 SSBR-114
updates = {
    'SSBR-104': {'官能化程度_原始数值': '未公开', '官能化程度_原始单位': None},
    'SSBR-114': {'官能化程度_原始数值': '未公开', '官能化程度_原始单位': None},
}

for sample_id, new_values in updates.items():
    mask = df['样本ID'] == sample_id
    if mask.any():
        old_val = df.loc[mask, '官能化程度_原始数值'].values[0]
        old_unit = df.loc[mask, '官能化程度_原始单位'].values[0]
        
        df.loc[mask, '官能化程度_原始数值'] = new_values['官能化程度_原始数值']
        df.loc[mask, '官能化程度_原始单位'] = new_values['官能化程度_原始单位']
        
        print(f"\n{sample_id}:")
        print(f"  原始数值: {old_val} → {new_values['官能化程度_原始数值']}")
        print(f"  原始单位: {old_unit} → {new_values['官能化程度_原始单位']}")
    else:
        print(f"\n⚠️ {sample_id} 未找到")

# 保存
df.to_excel(excel_path, index=False)
print(f"\n[OK] 已保存到 {excel_path}")
print(f"最终样本数: {len(df)}")
