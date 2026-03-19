"""批量生成详细解读文档的脚本"""

import sys
import io
from pathlib import Path
from datetime import date

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.excel_handler import ExcelHandler

EXCEL_PATH = Path(__file__).parent.parent / "dataset" / "数据.xlsx"
INTERP_DIR = Path(__file__).parent.parent / "dataset" / "interpretations"
TODAY = date.today().isoformat()


def create_mechanical_md(sample_id: str, meta: dict) -> str:
    """生成 mechanical.md 内容"""
    doi = meta.get('DOI', '-')
    mech_fig = meta.get('核心力学图谱', '-')
    app = meta.get('应用场景', '-')
    func_agent = meta.get('官能化试剂名称', '-')
    func_group = meta.get('核心官能团名称', '-')
    
    source_fig = mech_fig if mech_fig != '-' else 'null'
    
    func_desc = func_agent if func_agent != '-' else '未官能化'
    func_suffix = ' 改性' if func_agent != '-' else ''
    mech_data_section = f'文献 {mech_fig} 提供了力学性能数据。' if mech_fig != '-' else '**文献未提供力学图谱数据。**'
    mech_source_line = f'- **图注引用**: {mech_fig}' if mech_fig != '-' else '- **数据状态**: 力学数据不可用'
    
    content = f'''---
sample_id: {sample_id}
interpretation_type: mechanical
source_figure: "{source_fig}"
source_doi: "{doi}"
skill_used: ssbr-mechanical-interpretation
created_at: {TODAY}
updated_at: null

data:
  mechanical_source: "{source_fig}"
---

# 力学性能解读：{sample_id}

> **样本性质**: {func_desc}{func_suffix} SSBR 复合材料

## 一、基础信息

- **样本ID**: {sample_id}
- **应用场景**: {app}
- **官能化试剂**: {func_agent}
- **核心官能团**: {func_group}
- **文献DOI**: {doi}

## 二、力学性能

### 数据来源

{mech_data_section}

---

## 文献来源

- **DOI**: {doi}
{mech_source_line}
'''
    return content


def create_nmr_md(sample_id: str, meta: dict) -> str:
    """生成 nmr.md 内容"""
    doi = meta.get('DOI', '-')
    nmr_fig = meta.get('核磁谱图', '-')
    func_degree = meta.get('官能化程度_原始数值', '-')
    func_unit = meta.get('官能化程度_原始单位', '-')
    styrene = meta.get('苯乙烯含量_wt%', '-')
    vinyl = meta.get('乙烯基含量_mol%', '-')
    
    source_fig = nmr_fig if nmr_fig != '-' else 'null'
    
    func_val = func_degree if func_degree != '-' else 'null'
    func_unit_val = func_unit if func_unit != '-' else ''
    styrene_val = styrene if styrene != '-' else 'null'
    vinyl_val = vinyl if vinyl != '-' else 'null'
    nmr_source = nmr_fig if nmr_fig != '-' else '文献未报告 NMR 数据'
    nmr_data_section = f'### 数据来源\n\n文献 {nmr_fig} 提供了 NMR 谱图。' if nmr_fig != '-' else '**文献未提供 NMR 谱图。**'
    nmr_source_line = f'- **图注引用**: {nmr_fig}' if nmr_fig != '-' else '- **数据状态**: NMR 数据不可用'
    
    content = f'''---
sample_id: {sample_id}
interpretation_type: nmr
source_figure: "{source_fig}"
source_doi: "{doi}"
skill_used: ssbr-nmr-interpretation
created_at: {TODAY}
updated_at: null

data:
  functionalization_degree:
    value: {func_val}
    unit: "{func_unit_val}"
    source: "{nmr_source}"
  styrene_content:
    value: {styrene_val}
    unit: "wt%"
  vinyl_content:
    value: {vinyl_val}
    unit: "mol%"
---

# ¹H NMR 核磁共振解读：{sample_id}

## 一、基础信息

- **样本ID**: {sample_id}
- **苯乙烯含量**: {styrene} wt%
- **乙烯基含量**: {vinyl} mol%
- **官能化程度**: {func_degree} {func_unit_val}
- **文献DOI**: {doi}

## 二、NMR 数据

{nmr_data_section}

---

## 文献来源

- **DOI**: {doi}
{nmr_source_line}
'''
    return content


def create_dsc_md(sample_id: str, meta: dict) -> str:
    """生成 dsc.md 内容"""
    doi = meta.get('DOI', '-')
    dsc_fig = meta.get('DSC 谱图', '-')
    
    source_fig = dsc_fig if dsc_fig != '-' else 'null'
    dsc_source = dsc_fig if dsc_fig != '-' else '文献未报告 DSC 数据'
    dsc_data_section = f'### 数据来源\n\n文献 {dsc_fig} 提供了 DSC 曲线。' if dsc_fig != '-' else '**文献未提供 DSC 热分析数据。**'
    dsc_source_line = f'- **图注引用**: {dsc_fig}' if dsc_fig != '-' else '- **数据状态**: DSC 数据不可用'
    
    content = f'''---
sample_id: {sample_id}
interpretation_type: dsc
source_figure: "{source_fig}"
source_doi: "{doi}"
skill_used: ssbr-dsc-interpretation
created_at: {TODAY}
updated_at: null

data:
  tg:
    value: null
    unit: "℃"
    source: "{dsc_source}"
---

# DSC 热分析解读：{sample_id}

## 一、基础信息

- **样本ID**: {sample_id}
- **文献DOI**: {doi}

## 二、DSC 数据

{dsc_data_section}

---

## 文献来源

- **DOI**: {doi}
{dsc_source_line}
'''
    return content


def create_tem_md(sample_id: str, meta: dict) -> str:
    """生成 tem.md 内容"""
    doi = meta.get('DOI', '-')
    tem_fig = meta.get('微相分离图片表征', '-')
    
    source_fig = tem_fig if tem_fig != '-' else 'null'
    
    # 判断是 TEM/SEM/AFM
    fig_type = "TEM"
    if tem_fig != '-':
        if 'SEM' in tem_fig.upper():
            fig_type = "SEM"
        elif 'AFM' in tem_fig.upper():
            fig_type = "AFM"
    
    morphology_line = f'"{fig_type} 形貌"' if tem_fig != '-' else 'null'
    data_section = f'### 数据来源\n\n文献 {tem_fig} 提供了 {fig_type} 图像。' if tem_fig != '-' else '**文献未提供形貌图像（TEM/SEM/AFM）。**'
    source_line = f'- **图注引用**: {tem_fig}' if tem_fig != '-' else '- **数据状态**: 形貌数据不可用'
    
    content = f'''---
sample_id: {sample_id}
interpretation_type: tem
source_figure: "{source_fig}"
source_doi: "{doi}"
skill_used: ssbr-tem-interpretation
created_at: {TODAY}
updated_at: null

data:
  dispersion_quality: null
  morphology: {morphology_line}
---

# {fig_type} 形貌解读：{sample_id}

## 一、基础信息

- **样本ID**: {sample_id}
- **文献DOI**: {doi}

## 二、形貌表征

{data_section}

---

## 文献来源

- **DOI**: {doi}
{source_line}
'''
    return content


def generate_docs_for_sample(sample_id: str, meta: dict):
    """为单个样本生成所有详细解读文档"""
    sample_dir = INTERP_DIR / sample_id
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # 检查是否已有文档（跳过已存在的）
    docs = [
        ('mechanical.md', create_mechanical_md),
        ('nmr.md', create_nmr_md),
        ('dsc.md', create_dsc_md),
        ('tem.md', create_tem_md),
    ]
    
    for filename, creator in docs:
        filepath = sample_dir / filename
        if not filepath.exists():
            content = creator(sample_id, meta)
            filepath.write_text(content, encoding='utf-8')
            print(f"  创建: {filename}")
        else:
            print(f"  跳过: {filename} (已存在)")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='批量生成详细解读文档')
    parser.add_argument('--start', type=int, required=True, help='起始样本编号')
    parser.add_argument('--end', type=int, required=True, help='结束样本编号')
    args = parser.parse_args()
    
    # 加载 Excel
    eh = ExcelHandler(EXCEL_PATH)
    eh.open()
    all_samples = eh.get_all_samples()
    
    # 构建样本字典
    samples_dict = {s.get('sample_id'): s for s in all_samples}
    
    print("=" * 60)
    print(f"批量生成详细解读文档: SSBR-{args.start:03d} ~ SSBR-{args.end:03d}")
    print("=" * 60)
    
    generated_count = 0
    for num in range(args.start, args.end + 1):
        sample_id = f"SSBR-{num:03d}"
        if sample_id in samples_dict:
            print(f"\n处理: {sample_id}")
            generate_docs_for_sample(sample_id, samples_dict[sample_id])
            generated_count += 1
        else:
            print(f"\n跳过: {sample_id} (Excel 中不存在)")
    
    print("\n" + "=" * 60)
    print(f"完成！共处理 {generated_count} 个样本")


if __name__ == "__main__":
    main()
