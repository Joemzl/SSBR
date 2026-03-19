#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提取指定批次样本的元数据，用于生成解读文档"""

import sys
import io
import json
from pathlib import Path

# 设置输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))

from utils.excel_handler import ExcelHandler

PROJECT_ROOT = Path(__file__).parent.parent
INTERPRETATIONS_DIR = PROJECT_ROOT / "dataset" / "interpretations"
EXCEL_PATH = PROJECT_ROOT / "dataset" / "数据.xlsx"

def extract_batch(start_id: int, end_id: int):
    """提取指定范围的样本元数据"""
    eh = ExcelHandler(EXCEL_PATH)
    eh.open()
    all_samples = eh.get_all_samples()
    
    # 过滤目标样本
    batch_samples = []
    for sample in all_samples:
        sid = sample.get('sample_id', '')
        if sid.startswith('SSBR-'):
            try:
                num = int(sid.split('-')[1])
                if start_id <= num <= end_id:
                    batch_samples.append(sample)
            except:
                pass
    
    # 排序
    batch_samples.sort(key=lambda x: int(x['sample_id'].split('-')[1]))
    
    print(f"=" * 60)
    print(f"批次: SSBR-{start_id:03d} ~ SSBR-{end_id:03d}")
    print(f"样本数: {len(batch_samples)}")
    print(f"=" * 60)
    
    for sample in batch_samples:
        sid = sample.get('sample_id')
        print(f"\n### {sid}")
        print(f"")
        
        # 基本信息
        is_inchain = sample.get('is_inchain_functionalization', '')
        styrene = sample.get('styrene_content', '-')
        vinyl = sample.get('vinyl_content', '-')
        mn = sample.get('mn', '-')
        app = sample.get('application', '-')
        
        print(f"- **是否链中官能化**: {is_inchain if is_inchain else '否'}")
        print(f"- **苯乙烯含量**: {styrene if styrene else '-'} wt%")
        print(f"- **乙烯基含量**: {vinyl if vinyl else '-'} mol%")
        print(f"- **数均分子量**: {mn if mn else '-'}")
        print(f"- **应用场景**: {app if app else '-'}")
        
        # 官能化信息
        reagent = sample.get('reagent_name', '-')
        reagent_smiles = sample.get('reagent_smiles', '-')
        grafting = sample.get('grafting_group', '-')
        grafting_smiles = sample.get('grafting_group_smiles', '-')
        fg_name = sample.get('functional_group_name', '-')
        fg_smiles = sample.get('functional_group_smiles', '-')
        fg_formula = sample.get('functional_group_formula', '-')
        degree = sample.get('functionalization_degree', '-')
        degree_unit = sample.get('functionalization_unit', '-')
        
        print(f"- **官能化试剂**: {reagent if reagent else '-'}")
        print(f"- **试剂 SMILES**: {reagent_smiles if reagent_smiles else '-'}")
        print(f"- **接枝反应基团**: {grafting if grafting else '-'}")
        print(f"- **接枝基团 SMILES**: {grafting_smiles if grafting_smiles else '-'}")
        print(f"- **核心官能团**: {fg_name if fg_name else '-'}")
        print(f"- **官能团 SMILES**: {fg_smiles if fg_smiles else '-'}")
        print(f"- **官能团化学式**: {fg_formula if fg_formula else '-'}")
        print(f"- **官能化程度**: {degree if degree else '-'} {degree_unit if degree_unit else ''}")
        
        # 表征信息
        nmr = sample.get('nmr_figure', '-')
        tem = sample.get('tem_figure', '-')
        mech = sample.get('mechanical_figure', '-')
        dsc = sample.get('dsc_figure', '-')
        
        print(f"- **NMR 谱图**: {nmr if nmr else '-'}")
        print(f"- **TEM 图像**: {tem if tem else '-'}")
        print(f"- **力学图谱**: {mech if mech else '-'}")
        print(f"- **DSC 谱图**: {dsc if dsc else '-'}")
        
        # 文献信息
        citation = sample.get('citation', '-')
        doi = sample.get('doi', '-')
        doi_si = sample.get('doi_si', '-')
        
        print(f"- **引文**: {citation if citation else '-'}")
        print(f"- **DOI**: {doi if doi else '-'}")
        print(f"- **DOI_SI**: {doi_si if doi_si else '-'}")
        
        # 创建目录
        sample_dir = INTERPRETATIONS_DIR / sid
        if not sample_dir.exists():
            sample_dir.mkdir(parents=True)
            print(f"  [创建目录] {sample_dir}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, required=True, help='起始编号')
    parser.add_argument('--end', type=int, required=True, help='结束编号')
    args = parser.parse_args()
    
    extract_batch(args.start, args.end)
