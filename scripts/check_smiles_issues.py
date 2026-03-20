"""
数据清洗脚本 - 第2批：修复SMILES问题
检查并修复有试剂但SMILES缺失或错误的样本
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path

# 路径配置
EXCEL_PATH = Path(__file__).parent.parent / "dataset" / "数据.xlsx"

# 原始待修复列表
ORIGINAL_SMILES_ISSUES = [
    'SSBR-017', 'SSBR-018', 'SSBR-021', 'SSBR-036', 'SSBR-052',
    'SSBR-064', 'SSBR-065', 'SSBR-068', 'SSBR-069', 'SSBR-071',
    'SSBR-075', 'SSBR-079', 'SSBR-081', 'SSBR-085', 'SSBR-086',
    'SSBR-088', 'SSBR-092', 'SSBR-093', 'SSBR-097', 'SSBR-100',
    'SSBR-101', 'SSBR-107', 'SSBR-108', 'SSBR-112'
]

def main():
    df = pd.read_excel(EXCEL_PATH)
    
    print("=" * 70)
    print("第2批：SMILES问题检查")
    print("=" * 70)
    print(f"当前样本总数: {len(df)}")
    
    # 检查哪些样本仍然存在
    existing = df[df['样本ID'].isin(ORIGINAL_SMILES_ISSUES)]
    existing_ids = existing['样本ID'].tolist()
    deleted_ids = set(ORIGINAL_SMILES_ISSUES) - set(existing_ids)
    
    print(f"\n原始SMILES问题样本: {len(ORIGINAL_SMILES_ISSUES)} 个")
    print(f"已在第1批中删除: {len(deleted_ids)} 个")
    print(f"仍需修复: {len(existing_ids)} 个")
    
    if deleted_ids:
        print(f"\n已删除的样本: {sorted(deleted_ids)}")
    
    print("\n" + "=" * 70)
    print("待修复样本详情")
    print("=" * 70)
    
    for idx, row in existing.iterrows():
        sid = row['样本ID']
        reagent = row['官能化试剂名称']
        smiles = row['试剂整体 SMILES'] if pd.notna(row['试剂整体 SMILES']) else '空'
        core_smiles = row['核心官能团 SMILES'] if pd.notna(row['核心官能团 SMILES']) else '空'
        
        print(f"\n{sid}:")
        print(f"  试剂名称: {reagent}")
        print(f"  试剂整体SMILES: {smiles}")
        print(f"  核心官能团SMILES: {core_smiles}")

if __name__ == "__main__":
    main()
