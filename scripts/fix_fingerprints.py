"""
数据清洗脚本 - 第3批：补充高分子指纹描述符
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from pathlib import Path
import shutil
from datetime import datetime

# 路径配置
DATASET_DIR = Path(__file__).parent.parent / "dataset"
EXCEL_PATH = DATASET_DIR / "数据.xlsx"
BACKUP_DIR = DATASET_DIR / "backups"

def check_fingerprint_needs():
    """检查哪些样本需要补充指纹"""
    df = pd.read_excel(EXCEL_PATH)
    
    print("=" * 70)
    print("第3批：高分子指纹描述符检查")
    print("=" * 70)
    print(f"当前样本总数: {len(df)}")
    
    # 检查哪些样本有试剂但缺少指纹
    needs_fingerprint = []
    
    for idx, row in df.iterrows():
        sid = row['样本ID']
        reagent = row['官能化试剂名称']
        fingerprint = row['高分子指纹描述符']
        
        has_reagent = pd.notna(reagent) and str(reagent).strip() != ''
        has_fingerprint = pd.notna(fingerprint) and str(fingerprint).strip() != ''
        
        if has_reagent and not has_fingerprint:
            # 收集可用于生成指纹的数据
            available_data = {}
            
            # 基本信息
            if pd.notna(row.get('苯乙烯含量_wt%')):
                available_data['苯乙烯含量'] = row['苯乙烯含量_wt%']
            if pd.notna(row.get('乙烯基含量_mol%')):
                available_data['乙烯基含量'] = row['乙烯基含量_mol%']
            if pd.notna(row.get('官能化程度_原始数值')):
                available_data['官能化程度'] = f"{row['官能化程度_原始数值']} {row.get('官能化程度_原始单位', '')}"
            
            # SMILES 信息
            reagent_smiles = row.get('试剂整体 SMILES', '')
            core_smiles = row.get('核心官能团 SMILES', '')
            
            needs_fingerprint.append({
                'sample_id': sid,
                'reagent': reagent,
                'reagent_smiles': reagent_smiles if pd.notna(reagent_smiles) else '',
                'core_smiles': core_smiles if pd.notna(core_smiles) else '',
                'available_data': available_data
            })
    
    print(f"\n需要补充指纹的样本: {len(needs_fingerprint)} 个")
    
    print("\n" + "=" * 70)
    print("详情:")
    print("=" * 70)
    
    for item in needs_fingerprint:
        print(f"\n{item['sample_id']}:")
        print(f"  试剂: {item['reagent']}")
        print(f"  试剂SMILES: {item['reagent_smiles'] or '空'}")
        print(f"  核心官能团SMILES: {item['core_smiles'] or '空'}")
        if item['available_data']:
            print(f"  可用数据: {item['available_data']}")
    
    return needs_fingerprint

def generate_fingerprint(row):
    """
    根据样本数据生成高分子指纹描述符
    
    格式: 试剂SMILES-苯乙烯含量-乙烯基含量-主链结构-核心官能团SMILES-官能化程度
    """
    parts = []
    
    # 1. 试剂整体 SMILES
    reagent_smiles = row.get('试剂整体 SMILES', '')
    if pd.notna(reagent_smiles) and str(reagent_smiles).strip() not in ['', '复杂材料']:
        parts.append(str(reagent_smiles).strip())
    else:
        parts.append('')
    
    # 2. 苯乙烯含量
    st = row.get('苯乙烯含量_wt%', '')
    if pd.notna(st) and str(st).strip() != '':
        parts.append(str(int(float(st))) if float(st) == int(float(st)) else str(st))
    else:
        parts.append('')
    
    # 3. 乙烯基含量
    vinyl = row.get('乙烯基含量_mol%', '')
    if pd.notna(vinyl) and str(vinyl).strip() != '':
        parts.append(str(int(float(vinyl))) if float(vinyl) == int(float(vinyl)) else str(vinyl))
    else:
        parts.append('')
    
    # 4. 主链结构 (SSBR固定为 C=C)
    parts.append('C=C')
    
    # 5. 核心官能团 SMILES
    core_smiles = row.get('核心官能团 SMILES', '')
    if pd.notna(core_smiles) and str(core_smiles).strip() != '':
        parts.append(str(core_smiles).strip())
    else:
        parts.append('')
    
    # 6. 官能化程度
    degree = row.get('官能化程度_原始数值', '')
    unit = row.get('官能化程度_原始单位', '')
    if pd.notna(degree) and str(degree).strip() != '':
        degree_str = str(degree).strip()
        if pd.notna(unit) and str(unit).strip() != '':
            degree_str += str(unit).strip()
        parts.append(degree_str)
    else:
        parts.append('')
    
    # 组合指纹
    fingerprint = '-'.join(parts)
    
    # 如果太空（大部分都是空的），返回空
    non_empty = sum(1 for p in parts if p and p != 'C=C')
    if non_empty < 2:
        return ''
    
    return fingerprint

def execute_fingerprint_generation(dry_run=True):
    """执行指纹生成"""
    df = pd.read_excel(EXCEL_PATH)
    
    if not dry_run:
        BACKUP_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f"数据_backup_fingerprint_{timestamp}.xlsx"
        shutil.copy(EXCEL_PATH, backup_path)
        print(f"✅ 已备份到: {backup_path}")
    
    updated_count = 0
    skipped_count = 0
    
    print("\n生成指纹...")
    
    for idx, row in df.iterrows():
        sid = row['样本ID']
        reagent = row['官能化试剂名称']
        current_fp = row['高分子指纹描述符']
        
        has_reagent = pd.notna(reagent) and str(reagent).strip() != ''
        has_fingerprint = pd.notna(current_fp) and str(current_fp).strip() != ''
        
        if has_reagent and not has_fingerprint:
            new_fp = generate_fingerprint(row)
            
            if new_fp:
                if dry_run:
                    print(f"  [DRY RUN] {sid}: 将生成指纹 = {new_fp}")
                else:
                    df.loc[idx, '高分子指纹描述符'] = new_fp
                    print(f"  ✅ {sid}: 指纹已生成 = {new_fp}")
                updated_count += 1
            else:
                if dry_run:
                    print(f"  [SKIP] {sid}: 数据不足，无法生成有意义的指纹")
                skipped_count += 1
    
    if not dry_run:
        df.to_excel(EXCEL_PATH, index=False)
        print(f"\n✅ Excel已保存")
    
    print(f"\n汇总: 生成 {updated_count} 个, 跳过 {skipped_count} 个")

def main(dry_run=True):
    needs = check_fingerprint_needs()
    
    if not needs:
        print("\n✅ 所有样本都已有指纹描述符，无需处理")
        return
    
    if dry_run:
        print("\n⚠️  当前为预览模式")
        print("   如需执行，请运行: python fix_fingerprints.py --execute")
    
    print("\n" + "-" * 70)
    execute_fingerprint_generation(dry_run=dry_run)
    
    print("\n" + "=" * 70)
    if dry_run:
        print("预览完成。")
    else:
        print("指纹生成完成！")
    print("=" * 70)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="执行生成")
    args = parser.parse_args()
    
    main(dry_run=not args.execute)
