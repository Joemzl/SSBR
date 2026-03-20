# -*- coding: utf-8 -*-
"""
补充核心官能团数据并修正高分子指纹描述符格式

任务：
1. 根据「核心官能团名称」补充「核心官能团 SMILES」和「核心官能团化学式」
2. 按照提示词规范修正「高分子指纹描述符」格式
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 核心官能团映射表：名称 -> (SMILES, 化学式)
FUNCTIONAL_GROUP_MAP = {
    # 常见官能团
    '羧基': ('C(=O)O', '-COOH'),
    '羟基': ('O', '-OH'),
    '氨基': ('N', '-NH2'),
    '环氧基': ('C1OC1', '-C2H2O-'),
    '酯基': ('C(=O)OC', '-COOR'),
    
    # 硅烷基类
    '硅烷基': ('[Si](O)(O)O', '-Si(OR)3'),
    '三乙氧基硅烷基': ('[Si](OCC)(OCC)OCC', '-Si(OC₂H₅)₃'),
    '烷氧基硅烷基': ('[Si](OC)(OC)OC', '-Si(OR)3'),
    '三甲基硅基': ('[Si](C)(C)C', '-Si(CH3)3'),
    '三甲氧基硅烷基': ('[Si](OC)(OC)OC', '-Si(OCH₃)₃'),
    '三苯基硅基': ('[Si](c1ccccc1)(c2ccccc2)c3ccccc3', '-SiPh₃'),
    '硅基': ('[Si]', '-SiR3'),
    
    # 芳香族类
    '二苯基乙基': ('c1ccc(C(CCc2ccccc2)c3ccccc3)cc1', '-CHPh2'),
    '三苯基乙基': ('c1ccc(C(c2ccccc2)(c3ccccc3)c4ccccc4)cc1', '-CPh3'),
    
    # 含氮杂环类
    '咪唑鎓': ('C[n+]1ccn(C)c1', '-Im+'),
    '吡啶基/羧基': ('c1ccncc1.C(=O)O', '-Py/-COOH'),
    '脲基嘧啶酮': ('O=C1NC(=O)NC(=O)N1', '-UPy'),
    '三嗪基': ('c1ncncn1', '-C₃N₃-'),
    '胍基': ('NC(=N)N', '-C(=NH)(NH2)'),
    
    # 含硫官能团
    '硫醇基': ('S', '-SH'),
    '二硫化物': ('SS', '-S-S-'),
    '四硫化物': ('SSSS', '-S₄-'),
    
    # 其他
    '对苯二胺衍生物': ('Nc1ccc(N)cc1', '-C6H4(NH2)2'),
    '脲唑基': ('NC(=O)N', '-NHCONH-'),
    '聚氨酯硬段': ('NC(=O)O', '-NHCOO-'),
    '异亚丙基侧链': ('CC(C)', '-C(CH3)2-'),
    '烷基链': ('CCCCCC', '-(CH2)n-'),
    '萜烯基': ('CC(=C)C', '-萜烯-'),
    '石墨烯': ('c1ccccc1', '-石墨烯-'),
    '纳米材料': ('-', '-纳米材料-'),
    '聚丁二烯': ('C=CC=C', '-PB-'),
    
    # 复合官能团
    '氨基/硅烷基': ('N.[Si](O)(O)O', '-NH2/-Si(OR)3'),
    '氨基/三甲氧基硅烷基': ('N.[Si](OC)(OC)OC', '-NH2/-Si(OCH₃)₃'),
}

# 根据试剂名称推断核心官能团的映射
REAGENT_TO_FUNCTIONAL_GROUP = {
    # 氨基硅烷类
    '[3-(2-氨基乙基)氨基丙基]三甲氧基硅烷（AMMO）': ('氨基/三甲氧基硅烷基', 'N.[Si](OC)(OC)OC', '-NH2/-Si(OCH₃)₃'),
    '[3-(2-氨基乙基)氨基丙基]三甲氧基硅烷': ('氨基/三甲氧基硅烷基', 'N.[Si](OC)(OC)OC', '-NH2/-Si(OCH₃)₃'),
    
    # 硫代硅烷类
    '3-辛酰硫基-1-丙基三乙氧基硅烷': ('三乙氧基硅烷基', '[Si](OCC)(OCC)OCC', '-Si(OC₂H₅)₃'),
    '双[γ-(三乙氧基硅基)丙基]二硫化物（Si-75）': ('三乙氧基硅烷基/二硫化物', '[Si](OCC)(OCC)OCC.SS', '-Si(OC₂H₅)₃/-S-S-'),
    '双-(三乙氧基硅基丙基)-四硫化物（TESPT）、双-(三乙氧基硅基丙基)-二硫化物（TESPD）': ('三乙氧基硅烷基/多硫化物', '[Si](OCC)(OCC)OCC.SSSS', '-Si(OC₂H₅)₃/-Sₓ-'),
    '双-(3-(三乙氧基硅基)-丙基)-四硫化物（TESPT，Si-69）': ('三乙氧基硅烷基/四硫化物', '[Si](OCC)(OCC)OCC.SSSS', '-Si(OC₂H₅)₃/-S₄-'),
    'Si747 (硅烷偶联剂)': ('三乙氧基硅烷基', '[Si](OCC)(OCC)OCC', '-Si(OC₂H₅)₃'),
    
    # 胍类
    '二苯胍 (DPG)': ('胍基', 'NC(=Nc1ccccc1)Nc2ccccc2', '-C(=NPh)(NHPh)'),
    
    # 萜烯类
    'β-月桂烯': ('萜烯基', 'CC(=C)C=CC=C(C)C', '-萜烯-'),
    
    # 改性填料
    'EVA 改性白炭黑': ('酯基/乙烯基', 'CC(=O)OC=C', '-OCOCH₃/-CH=CH₂'),
    
    # 酯类
    '脂肪酸苄酯': ('酯基', 'C(=O)OCc1ccccc1', '-COOBn'),
    
    # 纳米材料/复合材料
    '石墨烯润滑剂': ('石墨烯', '-', '-石墨烯-'),
    '烃类树脂': ('烃基', 'C', '-烃类-'),
    '环氧化天然橡胶 (ENR)': ('环氧基', 'C1OC1', '-环氧-'),
    'C3N4/SiO2 纳米杂化材料': ('纳米材料', '-', '-C₃N₄/SiO₂-'),
    '硅氧烷改性氧化石墨烯 (rGO-g-SiO2)': ('硅基/石墨烯', '[Si].c1ccccc1', '-Si-/rGO'),
    '液体聚丁二烯 (LPB)': ('聚丁二烯', 'C=CC=C', '-PB-'),
}

def backup_excel(filepath: Path) -> Path:
    """创建 Excel 备份"""
    backup_dir = filepath.parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"{filepath.stem}_backup_{timestamp}{filepath.suffix}"
    shutil.copy2(filepath, backup_path)
    return backup_path

def fill_functional_group_data(df: pd.DataFrame) -> pd.DataFrame:
    """根据核心官能团名称或试剂名称填充 SMILES 和化学式"""
    
    filled_smiles = 0
    filled_formula = 0
    filled_name = 0
    
    for idx, row in df.iterrows():
        name = row.get('核心官能团名称')
        reagent = row.get('官能化试剂名称')
        current_smiles = row.get('核心官能团 SMILES')
        current_formula = row.get('核心官能团化学式')
        
        # 检查是否需要填充
        need_smiles = pd.isna(current_smiles) or str(current_smiles).strip() in ['', '-']
        need_formula = pd.isna(current_formula) or str(current_formula).strip() in ['', '-']
        need_name = pd.isna(name) or str(name).strip() in ['', '-']
        
        if not (need_smiles or need_formula):
            continue
        
        # 首先尝试从官能团名称映射
        if not (pd.isna(name) or str(name).strip() in ['', '-']):
            name_str = str(name).strip()
            if name_str in FUNCTIONAL_GROUP_MAP:
                smiles, formula = FUNCTIONAL_GROUP_MAP[name_str]
                if need_smiles:
                    df.at[idx, '核心官能团 SMILES'] = smiles
                    filled_smiles += 1
                if need_formula:
                    df.at[idx, '核心官能团化学式'] = formula
                    filled_formula += 1
                continue
            else:
                print(f"  ⚠️ 未知官能团名称: '{name_str}' (样本 {row.get('样本ID', idx)})")
        
        # 如果官能团名称为空，尝试从试剂名称推断
        if need_name and not (pd.isna(reagent) or str(reagent).strip() in ['', '-']):
            reagent_str = str(reagent).strip()
            if reagent_str in REAGENT_TO_FUNCTIONAL_GROUP:
                inferred_name, smiles, formula = REAGENT_TO_FUNCTIONAL_GROUP[reagent_str]
                # 填充官能团名称
                df.at[idx, '核心官能团名称'] = inferred_name
                filled_name += 1
                # 填充 SMILES
                if need_smiles:
                    df.at[idx, '核心官能团 SMILES'] = smiles
                    filled_smiles += 1
                # 填充化学式
                if need_formula:
                    df.at[idx, '核心官能团化学式'] = formula
                    filled_formula += 1
            else:
                print(f"  ⚠️ 无法推断官能团，试剂: '{reagent_str}' (样本 {row.get('样本ID', idx)})")
    
    print(f"  填充官能团名称: {filled_name} 条")
    print(f"  填充 SMILES: {filled_smiles} 条")
    print(f"  填充化学式: {filled_formula} 条")
    
    return df

def build_fingerprint(row: pd.Series) -> str:
    """
    按照提示词规范构建高分子指纹描述符
    
    格式: [试剂整体SMILES]-[数均分子量]-[苯乙烯含量_wt%]-[乙烯基含量_mol%]-[接枝反应基团SMILES]-[核心官能团SMILES]-[官能化程度_原始数值][官能化程度_原始单位]
    
    缺失项保留 "-"
    """
    def get_value(col_name):
        val = row.get(col_name)
        if pd.isna(val) or str(val).strip() in ['', '-', 'nan', 'NaN']:
            return '-'
        return str(val).strip()
    
    # 获取各字段
    reagent_smiles = get_value('试剂整体 SMILES')
    mn = get_value('数均分子量 (Mn)')
    styrene = get_value('苯乙烯含量_wt%')
    vinyl = get_value('乙烯基含量_mol%')
    graft_smiles = get_value('接枝反应基团SMILES')
    core_smiles = get_value('核心官能团 SMILES')
    func_degree = get_value('官能化程度_原始数值')
    func_unit = get_value('官能化程度_原始单位')
    
    # 构建最后一部分：官能化程度数值+单位（无空格）
    if func_degree != '-' and func_unit != '-':
        func_part = f"{func_degree}{func_unit}"
    elif func_degree != '-':
        func_part = func_degree
    else:
        func_part = '-'
    
    # 按公式拼接
    fingerprint = f"{reagent_smiles}-{mn}-{styrene}-{vinyl}-{graft_smiles}-{core_smiles}-{func_part}"
    
    return fingerprint

def fix_fingerprints(df: pd.DataFrame) -> pd.DataFrame:
    """修正所有高分子指纹描述符"""
    
    fixed_count = 0
    
    for idx, row in df.iterrows():
        new_fingerprint = build_fingerprint(row)
        old_fingerprint = row.get('高分子指纹描述符')
        
        if pd.isna(old_fingerprint) or str(old_fingerprint) != new_fingerprint:
            df.at[idx, '高分子指纹描述符'] = new_fingerprint
            fixed_count += 1
    
    print(f"  修正指纹: {fixed_count} 条")
    
    return df

def main():
    excel_path = Path('dataset/数据.xlsx')
    
    print("=" * 60)
    print("核心官能团数据补充与指纹修正工具")
    print("=" * 60)
    
    # 读取 Excel
    print("\n1. 读取 Excel...")
    df = pd.read_excel(excel_path)
    print(f"  共 {len(df)} 条记录")
    
    # 备份
    print("\n2. 创建备份...")
    backup_path = backup_excel(excel_path)
    print(f"  备份: {backup_path}")
    
    # 统计修改前状态
    print("\n3. 修改前状态:")
    print(f"  核心官能团 SMILES 缺失: {df['核心官能团 SMILES'].isna().sum() + (df['核心官能团 SMILES'] == '-').sum()}")
    print(f"  核心官能团化学式 缺失: {df['核心官能团化学式'].isna().sum() + (df['核心官能团化学式'] == '-').sum()}")
    
    # 填充官能团数据
    print("\n4. 填充核心官能团数据...")
    df = fill_functional_group_data(df)
    
    # 修正指纹
    print("\n5. 修正高分子指纹描述符...")
    df = fix_fingerprints(df)
    
    # 保存
    print("\n6. 保存 Excel...")
    df.to_excel(excel_path, index=False)
    print(f"  已保存: {excel_path}")
    
    # 统计修改后状态
    print("\n7. 修改后状态:")
    print(f"  核心官能团 SMILES 缺失: {df['核心官能团 SMILES'].isna().sum() + (df['核心官能团 SMILES'] == '-').sum()}")
    print(f"  核心官能团化学式 缺失: {df['核心官能团化学式'].isna().sum() + (df['核心官能团化学式'] == '-').sum()}")
    
    print("\n" + "=" * 60)
    print("完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
