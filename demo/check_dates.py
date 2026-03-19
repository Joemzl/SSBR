"""检查各样本 summary.md 的创建日期和格式类型"""
import os
import re
from pathlib import Path

base_dir = Path("../dataset/interpretations")
samples = sorted([d.name for d in base_dir.iterdir() if d.is_dir() and d.name.startswith("SSBR-")])

# 统计不同格式类型
format_stats = {
    "skill_used": [],        # 标准模板
    "version_1.0": [],       # 版本 1.0 格式
    "sample_info": [],       # sample_info 嵌套
    "functionalizing_agent": [],  # functionalizing_agent 嵌套
    "polymer_nested": [],    # polymer 嵌套
    "functionalization_field": [],  # functionalization/functionalization_type 字段
    "functional_group": [],  # 顶层 functional_group
    "other": []
}

for sample in samples:
    summary_path = base_dir / sample / "summary.md"
    if not summary_path.exists():
        continue
    
    content = summary_path.read_text(encoding='utf-8')[:1000]
    
    if "skill_used:" in content:
        format_stats["skill_used"].append(sample)
    elif "version:" in content and '"1.0"' in content:
        format_stats["version_1.0"].append(sample)
    elif "sample_info:" in content:
        format_stats["sample_info"].append(sample)
    elif "functionalizing_agent:" in content:
        format_stats["functionalizing_agent"].append(sample)
    elif "polymer:" in content:
        format_stats["polymer_nested"].append(sample)
    else:
        format_stats["other"].append(sample)

print("=" * 60)
print("Summary.md 格式类型统计")
print("=" * 60)

for fmt, samples_list in format_stats.items():
    print(f"\n{fmt}: {len(samples_list)} 个样本")
    if samples_list:
        print(f"  示例: {', '.join(samples_list[:5])}")

print("\n" + "=" * 60)
print("格式分布饼图")
print("=" * 60)
total = sum(len(v) for v in format_stats.values())
for fmt, samples_list in format_stats.items():
    pct = len(samples_list) / total * 100 if total > 0 else 0
    bar = "█" * int(pct / 5)
    print(f"  {fmt:25s}: {len(samples_list):3d} ({pct:5.1f}%) {bar}")
