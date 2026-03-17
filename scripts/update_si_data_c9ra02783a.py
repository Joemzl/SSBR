"""
从 Zotero 文献中提取的数据，用于补充 Excel 中的缺失字段
基于 DOI: 10.1039/c9ra02783a (SI Table S2)
"""
import pandas as pd
from pathlib import Path
import sys

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')

# 读取数据
excel_path = Path(__file__).parent.parent / "dataset" / "数据.xlsx"
df = pd.read_excel(excel_path)

# 从 SI Table S2 提取的数据
# 注意：乙烯基含量在原文中是 1,2-Polybutadiene units (wt%)
si_data = {
    'SSBR-001': {  # SSBR-g-MPL70
        '苯乙烯含量_wt%': 23.0,
        '乙烯基含量_mol%': 40.1,  # 原文是 wt%，但我们列名是 mol%，需要确认
        '数均分子量 (Mn)': '185 kDa',
    },
    'SSBR-002': {  # SSBR-g-MUA70
        '苯乙烯含量_wt%': 20.9,
        '乙烯基含量_mol%': 39.5,
        '数均分子量 (Mn)': '186 kDa',
    },
    'SSBR-003': {  # SSBR-g-MPTES13 (最低接枝度)
        '苯乙烯含量_wt%': 18.4,
        '乙烯基含量_mol%': 47.8,
        '数均分子量 (Mn)': '186 kDa',
    },
    'SSBR-004': {  # SSBR-g-MPTES42 (中等接枝度)
        '苯乙烯含量_wt%': 17.9,
        '乙烯基含量_mol%': 45.0,
        '数均分子量 (Mn)': '187 kDa',
    },
    'SSBR-005': {  # SSBR-g-MPTES70 (最高接枝度)
        '苯乙烯含量_wt%': 21.1,
        '乙烯基含量_mol%': 38.7,
        '数均分子量 (Mn)': '196 kDa',
    },
}

# 检查是否为 dry-run 模式
dry_run = '--dry-run' in sys.argv

print("=" * 60)
print("从 DOI: 10.1039/c9ra02783a 补充数据")
print("数据来源: SI Table S2")
print("=" * 60)

if dry_run:
    print("\n[DRY RUN MODE - 不会实际修改文件]\n")

updates = []
for sample_id, data in si_data.items():
    # 找到对应行
    mask = df['样本ID'] == sample_id
    if not mask.any():
        print(f"❌ 未找到样本: {sample_id}")
        continue
    
    idx = df[mask].index[0]
    current = df.loc[idx]
    
    print(f"\n{sample_id} ({current['官能化试剂名称']}):")
    
    for field, value in data.items():
        old_value = current[field]
        if pd.isna(old_value):
            print(f"  {field}: [空] → {value}")
            if not dry_run:
                df.loc[idx, field] = value
            updates.append((sample_id, field, value))
        else:
            print(f"  {field}: {old_value} (已有值，跳过)")

print("\n" + "=" * 60)
print(f"总计: {len(updates)} 个字段将被更新")
print("=" * 60)

if not dry_run and updates:
    # 保存更新后的数据
    df.to_excel(excel_path, index=False)
    print(f"\n✅ 数据已保存到 {excel_path}")
elif dry_run:
    print("\n要实际执行更新，请运行:")
    print(f"  python {Path(__file__).name}")
