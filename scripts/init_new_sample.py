"""
新样本目录初始化脚本
为新样本创建标准目录结构和模板文件

Created: 2026-03-05
Task: T047
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import date

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
INTERPRETATIONS_DIR = PROJECT_ROOT / "dataset" / "interpretations"


def validate_sample_id(sample_id: str) -> bool:
    """
    验证样本 ID 格式
    
    Args:
        sample_id: 样本 ID
        
    Returns:
        是否有效
    """
    pattern = r'^SSBR-\d{3}$'
    return bool(re.match(pattern, sample_id))


def get_next_sample_id() -> str:
    """
    获取下一个可用的样本 ID
    
    Returns:
        下一个样本 ID
    """
    existing = []
    for d in INTERPRETATIONS_DIR.iterdir():
        if d.is_dir() and d.name.startswith('SSBR-'):
            try:
                num = int(d.name.split('-')[1])
                existing.append(num)
            except (ValueError, IndexError):
                continue
    
    next_num = max(existing) + 1 if existing else 1
    return f"SSBR-{next_num:03d}"


def create_template_file(filepath: Path, sample_id: str, doc_type: str) -> None:
    """
    创建模板文件
    
    Args:
        filepath: 文件路径
        sample_id: 样本 ID
        doc_type: 文档类型
    """
    today = date.today().isoformat()
    
    templates = {
        'mechanical': f"""---
sample_id: {sample_id}
interpretation_type: mechanical
source_figure: null
source_doi: null
skill_used: ssbr-mechanical-interpretation
created_at: {today}
updated_at: null
mechanical_subtypes: []

data: {{}}
---

# 力学性能解读：{sample_id}

> **待填充**: 请调用 ssbr-mechanical-interpretation Skill 生成解读内容
""",
        'dsc': f"""---
sample_id: {sample_id}
interpretation_type: dsc
source_figure: null
source_doi: null
skill_used: ssbr-dsc-interpretation
created_at: {today}
updated_at: null

data: {{}}
---

# DSC 热分析解读：{sample_id}

> **待填充**: 请调用 ssbr-dsc-interpretation Skill 生成解读内容
""",
        'nmr': f"""---
sample_id: {sample_id}
interpretation_type: nmr
source_figure: null
source_doi: null
skill_used: ssbr-nmr-interpretation
created_at: {today}
updated_at: null

data: {{}}
---

# NMR 核磁共振谱图解读：{sample_id}

> **待填充**: 请调用 ssbr-nmr-interpretation Skill 生成解读内容
""",
        'tem': f"""---
sample_id: {sample_id}
interpretation_type: tem
source_figure: null
source_doi: null
skill_used: ssbr-tem-interpretation
created_at: {today}
updated_at: null

data: {{}}
---

# TEM 形貌表征解读：{sample_id}

> **待填充**: 请调用 ssbr-tem-interpretation Skill 生成解读内容
""",
        'summary': f"""---
sample_id: {sample_id}
interpretation_type: summary
skill_used: ssbr-summary-generator
created_at: {today}
updated_at: null
interpretations_included: []
interpretations_missing:
  - mechanical
  - dsc
  - nmr
  - tem
---

# {sample_id} 综合档案

> **待填充**: 请先完成解读文档，然后调用 ssbr-summary-generator 生成综合档案
"""
    }
    
    content = templates.get(doc_type, '')
    if content:
        filepath.write_text(content, encoding='utf-8')


def init_sample_directory(sample_id: str, force: bool = False) -> dict:
    """
    初始化样本目录
    
    Args:
        sample_id: 样本 ID
        force: 是否强制覆盖已存在的文件
        
    Returns:
        初始化结果
    """
    result = {
        'sample_id': sample_id,
        'created_dir': False,
        'created_files': [],
        'skipped_files': [],
        'errors': []
    }
    
    # 验证 ID 格式
    if not validate_sample_id(sample_id):
        result['errors'].append(f"Invalid sample ID format: {sample_id}. Expected: SSBR-XXX")
        return result
    
    # 创建目录
    sample_dir = INTERPRETATIONS_DIR / sample_id
    if not sample_dir.exists():
        sample_dir.mkdir(parents=True)
        result['created_dir'] = True
        print(f"[OK] Created directory: {sample_dir}")
    else:
        print(f"[INFO] Directory already exists: {sample_dir}")
    
    # 创建模板文件
    doc_types = ['mechanical', 'dsc', 'nmr', 'tem', 'summary']
    
    for doc_type in doc_types:
        filepath = sample_dir / f"{doc_type}.md"
        
        if filepath.exists() and not force:
            result['skipped_files'].append(doc_type)
            print(f"[SKIP] File exists: {filepath.name}")
        else:
            try:
                create_template_file(filepath, sample_id, doc_type)
                result['created_files'].append(doc_type)
                print(f"[OK] Created template: {filepath.name}")
            except Exception as e:
                result['errors'].append(f"Failed to create {doc_type}.md: {e}")
                print(f"[ERROR] Failed to create {filepath.name}: {e}")
    
    return result


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='SSBR 新样本目录初始化工具',
        epilog='示例: python init_new_sample.py --sample-id SSBR-018'
    )
    parser.add_argument(
        '--sample-id', '-s',
        type=str,
        help='样本 ID (格式: SSBR-XXX)，不指定则自动分配下一个可用 ID'
    )
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='强制覆盖已存在的文件'
    )
    parser.add_argument(
        '--next-id',
        action='store_true',
        help='仅显示下一个可用的样本 ID，不执行初始化'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("SSBR New Sample Initialization Tool")
    print("=" * 60)
    
    # 仅显示下一个 ID
    if args.next_id:
        next_id = get_next_sample_id()
        print(f"\nNext available sample ID: {next_id}")
        return 0
    
    # 确定样本 ID
    sample_id = args.sample_id
    if not sample_id:
        sample_id = get_next_sample_id()
        print(f"\n[INFO] Auto-assigned sample ID: {sample_id}")
    
    # 执行初始化
    print(f"\nInitializing sample: {sample_id}")
    print("-" * 40)
    
    result = init_sample_directory(sample_id, force=args.force)
    
    # 显示结果
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Sample ID: {result['sample_id']}")
    print(f"  Directory created: {'Yes' if result['created_dir'] else 'No (already exists)'}")
    print(f"  Files created: {len(result['created_files'])}")
    print(f"  Files skipped: {len(result['skipped_files'])}")
    print(f"  Errors: {len(result['errors'])}")
    
    if result['errors']:
        print("\nErrors:")
        for err in result['errors']:
            print(f"  - {err}")
        return 1
    
    print(f"\n[OK] Sample {sample_id} initialized successfully!")
    print(f"\nNext steps:")
    print(f"  1. Add metadata to Excel: /dataset/data.xlsx")
    print(f"  2. Generate interpretations using Skills")
    print(f"  3. Generate summary: @ssbr-summary-generator")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
