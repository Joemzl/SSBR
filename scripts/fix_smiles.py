"""
数据清洗脚本 - 第2批：SMILES修复分类和执行
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

# SMILES 修复映射表
# 基于化学知识提供正确的 SMILES
SMILES_FIXES = {
    # 可以修复的样本
    'SSBR-017': {
        'reagent_smiles': 'OCC(C)(COC(=O)CCS)COC(=O)CCS',  # TMPMP: 三羟甲基丙烷三(3-巯基丙酸酯)
        'note': 'Trimethylolpropane tris(3-mercaptopropionate)'
    },
    'SSBR-018': {
        'reagent_smiles': 'CN(C)c1ccc(C(=C)c2ccccc2)cc1',  # DPE-NMe2: 4-(二甲基氨基)二苯乙烯
        'note': '4-Dimethylamino-1,1-diphenylethylene'
    },
    'SSBR-021': {
        'reagent_smiles': 'CN(C)c1ccc(C(=C)c2ccccc2)cc1',  # DPE-NMe2
        'note': '4-Dimethylamino-1,1-diphenylethylene'
    },
    'SSBR-036': {
        'reagent_smiles': 'C1OC1CSSSSCC2CO2',  # 双环氧丙基多硫化物 (简化结构)
        'note': 'Bis-epoxypropyl polysulfide'
    },
    'SSBR-052': {
        'reagent_smiles': '[Si](OC)(OC)(OC)C',  # 烷氧基硅烷 (通用结构: 甲基三甲氧基硅烷)
        'note': 'Alkoxy silane (generic)'
    },
    'SSBR-065': {
        'reagent_smiles': 'O=C1N=NC(=O)N1',  # 三唑啉二酮 (TAD)
        'note': '1,2,4-Triazolidine-3,5-dione'
    },
    'SSBR-069': {
        'reagent_smiles': 'c1ccc(NC(=Nc2ccccc2)N)cc1',  # 二苯胍 (DPG)
        'note': '1,3-Diphenylguanidine'
    },
    'SSBR-071': {
        'reagent_smiles': 'CCO[Si](CCCSSSSCCCO[Si](OCC)(OCC)OCC)(OCC)OCC',  # Si747 (简化结构)
        'note': 'Si747 silane coupling agent'
    },
    'SSBR-075': {
        'reagent_smiles': 'CCO[Si](CCCSSSSCCCC[Si](OCC)(OCC)OCC)(OCC)OCC',  # TESPT
        'note': 'Bis(triethoxysilylpropyl)tetrasulfide'
    },
}

# 无法用简单SMILES表示的样本（纳米材料、高分子材料等）
# 这些样本保留，但标记为"复杂材料，无SMILES"
COMPLEX_MATERIALS = {
    'SSBR-064': '对苯二胺改性氧化石墨烯 - 纳米复合材料',
    'SSBR-068': '羧基化丁苯橡胶 - 高分子材料',
    'SSBR-079': 'EVA改性白炭黑 - 纳米复合材料',
    'SSBR-081': '脂肪酸苄酯 - 混合物',
    'SSBR-085': '石墨烯润滑剂 - 纳米材料',
    'SSBR-086': '胺封端TBIR - 高分子材料',
    'SSBR-088': 'H2O2+催化剂 - 反应体系而非单一试剂',
    'SSBR-092': '三嗪基石墨炔 - 纳米碳材料',
    'SSBR-093': '硫醇官能化氧化石墨烯 - 纳米复合材料',
    'SSBR-097': '烃类树脂 - 混合物',
    'SSBR-100': '环氧化天然橡胶 - 高分子材料',
    'SSBR-101': '环氧化SSBR - 高分子材料',
    'SSBR-107': 'C3N4/SiO2纳米杂化材料 - 纳米复合材料',
    'SSBR-108': '硅氧烷改性氧化石墨烯 - 纳米复合材料',
    'SSBR-112': '液体聚丁二烯 - 高分子材料',
}

def show_plan():
    """显示修复计划"""
    print("=" * 70)
    print("第2批：SMILES修复计划")
    print("=" * 70)
    
    print("\n【A类】可以补充SMILES的样本 ({} 个):".format(len(SMILES_FIXES)))
    for sid, info in SMILES_FIXES.items():
        print(f"  {sid}: {info['note']}")
        print(f"        SMILES: {info['reagent_smiles']}")
    
    print("\n【B类】复杂材料，无法用简单SMILES表示 ({} 个):".format(len(COMPLEX_MATERIALS)))
    for sid, reason in COMPLEX_MATERIALS.items():
        print(f"  {sid}: {reason}")
    
    print("\n" + "=" * 70)
    print("建议:")
    print("  - A类样本: 补充SMILES")
    print("  - B类样本: 保留数据，在「试剂整体SMILES」列标记为「复杂材料」")
    print("=" * 70)

def execute_fixes(dry_run=True):
    """执行SMILES修复"""
    df = pd.read_excel(EXCEL_PATH)
    
    if not dry_run:
        # 备份
        BACKUP_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f"数据_backup_smiles_{timestamp}.xlsx"
        shutil.copy(EXCEL_PATH, backup_path)
        print(f"✅ 已备份到: {backup_path}")
    
    fixed_count = 0
    marked_count = 0
    
    # 修复A类样本
    print("\n修复A类样本...")
    for sid, info in SMILES_FIXES.items():
        mask = df['样本ID'] == sid
        if mask.any():
            if dry_run:
                print(f"  [DRY RUN] {sid}: 将设置SMILES = {info['reagent_smiles']}")
            else:
                df.loc[mask, '试剂整体 SMILES'] = info['reagent_smiles']
                print(f"  ✅ {sid}: SMILES已更新")
            fixed_count += 1
    
    # 标记B类样本
    print("\n标记B类样本...")
    for sid, reason in COMPLEX_MATERIALS.items():
        mask = df['样本ID'] == sid
        if mask.any():
            current_smiles = df.loc[mask, '试剂整体 SMILES'].values[0]
            if pd.isna(current_smiles) or str(current_smiles).strip() == '':
                if dry_run:
                    print(f"  [DRY RUN] {sid}: 将标记为「复杂材料」")
                else:
                    df.loc[mask, '试剂整体 SMILES'] = '复杂材料'
                    print(f"  ✅ {sid}: 已标记为「复杂材料」")
                marked_count += 1
    
    if not dry_run:
        df.to_excel(EXCEL_PATH, index=False)
        print(f"\n✅ Excel已保存")
    
    print(f"\n汇总: 修复 {fixed_count} 个, 标记 {marked_count} 个")

def main(dry_run=True):
    show_plan()
    
    if dry_run:
        print("\n⚠️  当前为预览模式")
        print("   如需执行，请运行: python fix_smiles.py --execute")
    
    print("\n" + "-" * 70)
    execute_fixes(dry_run=dry_run)
    
    print("\n" + "=" * 70)
    if dry_run:
        print("预览完成。")
    else:
        print("修复完成！")
    print("=" * 70)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="执行修复")
    args = parser.parse_args()
    
    main(dry_run=not args.execute)
