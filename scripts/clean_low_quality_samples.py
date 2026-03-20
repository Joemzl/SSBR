"""
数据清洗脚本 - 第1批：删除无官能化试剂的低质量样本
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd

# 路径配置
DATASET_DIR = Path(__file__).parent.parent / "dataset"
EXCEL_PATH = DATASET_DIR / "数据.xlsx"
BACKUP_DIR = DATASET_DIR / "backups"
INTERPRETATIONS_DIR = DATASET_DIR / "interpretations"

# 要删除的样本列表（无官能化试剂）
SAMPLES_TO_DELETE = [
    'SSBR-006', 'SSBR-007', 'SSBR-008', 'SSBR-009', 'SSBR-010',
    'SSBR-011', 'SSBR-012', 'SSBR-013', 'SSBR-014',
    'SSBR-027', 'SSBR-028', 'SSBR-029', 'SSBR-032', 'SSBR-035',
    'SSBR-037', 'SSBR-039',
    'SSBR-053', 'SSBR-054', 'SSBR-055', 'SSBR-056', 'SSBR-057',
    'SSBR-059', 'SSBR-060', 'SSBR-063',
    'SSBR-066', 'SSBR-067', 'SSBR-070', 'SSBR-072', 'SSBR-073',
    'SSBR-074', 'SSBR-077', 'SSBR-080', 'SSBR-082', 'SSBR-083',
    'SSBR-087', 'SSBR-089', 'SSBR-091', 'SSBR-094', 'SSBR-096',
    'SSBR-098',
    'SSBR-102', 'SSBR-103', 'SSBR-105', 'SSBR-110', 'SSBR-113'
]

def backup_excel():
    """备份Excel文件"""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"数据_backup_{timestamp}.xlsx"
    shutil.copy(EXCEL_PATH, backup_path)
    print(f"✅ 已备份到: {backup_path}")
    return backup_path

def delete_samples_from_excel(dry_run=True):
    """从Excel中删除样本"""
    df = pd.read_excel(EXCEL_PATH)
    original_count = len(df)
    
    print(f"\n📊 原始样本数: {original_count}")
    print(f"🗑️  待删除样本数: {len(SAMPLES_TO_DELETE)}")
    
    # 检查哪些样本存在
    existing_samples = df[df['样本ID'].isin(SAMPLES_TO_DELETE)]['样本ID'].tolist()
    missing_samples = set(SAMPLES_TO_DELETE) - set(existing_samples)
    
    if missing_samples:
        print(f"\n⚠️  以下样本在Excel中不存在: {sorted(missing_samples)}")
    
    print(f"\n将删除以下 {len(existing_samples)} 个样本:")
    for sid in sorted(existing_samples):
        print(f"  - {sid}")
    
    if dry_run:
        print("\n🔍 [DRY RUN] 未实际执行删除")
        return
    
    # 执行删除
    df_cleaned = df[~df['样本ID'].isin(SAMPLES_TO_DELETE)]
    new_count = len(df_cleaned)
    
    # 保存
    df_cleaned.to_excel(EXCEL_PATH, index=False)
    print(f"\n✅ Excel已更新: {original_count} → {new_count} 样本")
    
    return existing_samples

def delete_interpretation_folders(samples, dry_run=True):
    """删除对应的解读文档文件夹"""
    deleted = []
    not_found = []
    
    for sid in samples:
        folder = INTERPRETATIONS_DIR / sid
        if folder.exists():
            if dry_run:
                print(f"  [DRY RUN] 将删除: {folder}")
            else:
                shutil.rmtree(folder)
                print(f"  🗑️  已删除: {folder}")
            deleted.append(sid)
        else:
            not_found.append(sid)
    
    print(f"\n📁 解读文档文件夹:")
    print(f"   已删除: {len(deleted)} 个")
    print(f"   未找到: {len(not_found)} 个")
    
    return deleted, not_found

def main(dry_run=True):
    print("=" * 60)
    print("SSBR 数据清洗 - 第1批：删除低质量样本")
    print("=" * 60)
    
    if dry_run:
        print("\n⚠️  当前为预览模式 (dry_run=True)")
        print("   如需执行，请运行: python clean_low_quality_samples.py --execute")
    
    # 1. 备份
    if not dry_run:
        backup_excel()
    
    # 2. 从Excel删除
    deleted = delete_samples_from_excel(dry_run=dry_run)
    
    # 3. 删除解读文档文件夹
    if deleted or dry_run:
        print("\n" + "-" * 40)
        samples_to_check = SAMPLES_TO_DELETE if dry_run else deleted
        delete_interpretation_folders(samples_to_check, dry_run=dry_run)
    
    print("\n" + "=" * 60)
    if dry_run:
        print("预览完成。确认无误后运行: python clean_low_quality_samples.py --execute")
    else:
        print("清洗完成！")
    print("=" * 60)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="执行删除（默认为预览模式）")
    args = parser.parse_args()
    
    main(dry_run=not args.execute)
