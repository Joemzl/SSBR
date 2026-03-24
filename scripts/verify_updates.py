#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""验证更新后的数据一致性"""

import pandas as pd
from pathlib import Path
import yaml
import re

def extract_yaml_from_md(content):
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except:
            return {}
    return {}

df = pd.read_excel('dataset/数据.xlsx')
interp_dir = Path('dataset/interpretations')

issues = []
for idx, row in df.iterrows():
    sample_id = row['样本ID']
    summary_path = interp_dir / sample_id / 'summary.md'
    
    if not summary_path.exists():
        continue
    
    content = summary_path.read_text(encoding='utf-8')
    yaml_data = extract_yaml_from_md(content)
    
    if not yaml_data:
        issues.append(f"{sample_id}: 无法解析 YAML")
        continue
    
    # 检查关键字段是否存在
    if 'functionalization' not in yaml_data:
        issues.append(f"{sample_id}: 缺少 functionalization")
    
    if 'polymer_fingerprint' not in yaml_data:
        excel_fp = row.get('高分子指纹描述符', '')
        if pd.notna(excel_fp) and str(excel_fp).strip():
            issues.append(f"{sample_id}: 缺少 polymer_fingerprint")

if issues:
    print(f"发现 {len(issues)} 个问题:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("所有样本的 summary.md 都已正确更新!")
    print(f"共检查 {len(df)} 个样本")
