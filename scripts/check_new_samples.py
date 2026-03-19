#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查需要生成解读文档的新样本"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.excel_handler import ExcelHandler

PROJECT_ROOT = Path(__file__).parent.parent
INTERPRETATIONS_DIR = PROJECT_ROOT / "dataset" / "interpretations"
EXCEL_PATH = PROJECT_ROOT / "dataset" / "数据.xlsx"

def main():
    # 加载 Excel 数据
    eh = ExcelHandler(EXCEL_PATH)
    eh.open()
    all_samples = eh.get_all_samples()
    excel_ids = set(s.get('sample_id') for s in all_samples if s.get('sample_id'))
    
    # 检查已有解读文档的样本
    existing_ids = set()
    for d in INTERPRETATIONS_DIR.iterdir():
        if d.is_dir() and d.name.startswith('SSBR-'):
            summary_path = d / 'summary.md'
            if summary_path.exists():
                existing_ids.add(d.name)
    
    # 找出缺失的样本
    missing_ids = excel_ids - existing_ids
    
    print(f"Excel 总样本数: {len(excel_ids)}")
    print(f"已有解读文档: {len(existing_ids)}")
    print(f"缺少解读文档: {len(missing_ids)}")
    
    if missing_ids:
        # 按编号排序
        sorted_missing = sorted(missing_ids, key=lambda x: int(x.split('-')[1]))
        print(f"\n需要生成解读文档的样本:")
        for sid in sorted_missing:
            print(f"  - {sid}")
        
        # 输出最后几个 Excel 样本的详细信息
        print(f"\n最新 5 个样本信息:")
        for sample in all_samples[-5:]:
            sid = sample.get('sample_id', 'N/A')
            doi = sample.get('doi', 'N/A')
            reagent = sample.get('reagent_name', 'N/A')
            print(f"  {sid}: {reagent[:30] if reagent else 'N/A'}... | DOI: {doi}")

if __name__ == '__main__':
    main()
