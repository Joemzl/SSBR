import pandas as pd
import os
import sys
import yaml
import re
sys.stdout.reconfigure(encoding='utf-8')

def extract_yaml_from_md(filepath):
    """从Markdown文件提取YAML front matter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
    except:
        pass
    return None

# 读取Excel数据
df = pd.read_excel('dataset/数据.xlsx')
print(f"Excel中样本总数: {len(df)}")
print(f"Excel列名: {list(df.columns)}")

interp_dir = 'dataset/interpretations'

# 检查关键字段是否一致
mismatches = []

for idx, row in df.iterrows():
    sample_id = row['样本ID']
    summary_path = os.path.join(interp_dir, sample_id, 'summary.md')
    
    if os.path.exists(summary_path):
        yaml_data = extract_yaml_from_md(summary_path)
        if yaml_data:
            # 检查关键字段
            checks = []
            
            # 检查DOI
            excel_doi = str(row.get('DOI', ''))
            yaml_doi = str(yaml_data.get('source', {}).get('doi', '') or '')
            if excel_doi != yaml_doi and excel_doi != 'nan':
                checks.append(f"DOI: Excel='{excel_doi}' vs YAML='{yaml_doi}'")
            
            # 检查官能化试剂
            excel_reagent = str(row.get('官能化试剂名称', ''))
            yaml_reagent = str(yaml_data.get('functionalization', {}).get('reagent', '') or '')
            if excel_reagent != yaml_reagent and excel_reagent != 'nan':
                checks.append(f"试剂: Excel='{excel_reagent[:30]}' vs YAML='{yaml_reagent[:30]}'")
            
            # 检查官能化程度
            excel_degree = str(row.get('官能化程度_原始数值', ''))
            yaml_degree = str(yaml_data.get('functionalization', {}).get('degree', '') or '')
            if excel_degree != yaml_degree and excel_degree != 'nan':
                checks.append(f"程度: Excel='{excel_degree}' vs YAML='{yaml_degree}'")
            
            if checks:
                mismatches.append((sample_id, checks))

print(f"\n=== 检查到 {len(mismatches)} 个样本存在差异 ===")

# 统计各类差异
doi_missing = 0
reagent_diff = 0
degree_diff = 0

for sample_id, checks in mismatches:
    for check in checks:
        if check.startswith("DOI:") and "YAML=''" in check:
            doi_missing += 1
        elif check.startswith("试剂:"):
            reagent_diff += 1
        elif check.startswith("程度:"):
            degree_diff += 1

print(f"\n--- 差异统计 ---")
print(f"  DOI缺失: {doi_missing}")
print(f"  试剂名称差异: {reagent_diff}")
print(f"  官能化程度差异: {degree_diff}")

print(f"\n--- 前10个差异详情 ---")
for sample_id, checks in mismatches[:10]:
    print(f"\n{sample_id}:")
    for check in checks:
        print(f"  {check}")
