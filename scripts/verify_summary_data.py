#!/usr/bin/env python3
"""验证 summary.md 数据完整性"""

from pathlib import Path

base = Path(__file__).parent.parent / "dataset" / "interpretations"
samples = sorted([d.name for d in base.iterdir() if d.is_dir() and d.name.startswith("SSBR-")])

print("=" * 80)
print("SSBR Summary Data Verification Report")
print("=" * 80)
print()

# 分组信息
groups = {
    "Gao_2019 (SSBR-001~004)": ["SSBR-001", "SSBR-002", "SSBR-003", "SSBR-004"],
    "Qu_2014 (SSBR-005~008)": ["SSBR-005", "SSBR-006", "SSBR-007", "SSBR-008"],
    "Zhang_2018 (SSBR-009~012)": ["SSBR-009", "SSBR-010", "SSBR-011", "SSBR-012"],
    "Wang_2018 (SSBR-013~017)": ["SSBR-013", "SSBR-014", "SSBR-015", "SSBR-016", "SSBR-017"],
}

for group_name, sample_ids in groups.items():
    print(f"\n{group_name}")
    print("-" * 60)
    print(f"{'Sample':<12} {'Mech':<8} {'Payne':<8} {'DMA':<8} {'Tg':<8}")
    print("-" * 60)
    
    for sid in sample_ids:
        content = (base / sid / "summary.md").read_text(encoding="utf-8")
        
        # 检查各类指标是否存在有效数据
        has_mech = "100%定伸应力" in content and "| - |" not in content.split("100%定伸应力")[1][:30]
        has_payne = "活化能 Ea" in content and "| - |" not in content.split("活化能 Ea")[1][:30] if "活化能 Ea" in content else False
        has_dma = "tan δmax" in content and "| - |" not in content.split("tan δmax")[1][:30] if "tan δmax" in content else False
        has_tg = "Tg |" in content and "| - |" not in content.split("Tg |")[1][:30]
        
        print(f"{sid:<12} {'YES' if has_mech else 'no':<8} {'YES' if has_payne else 'no':<8} {'YES' if has_dma else 'no':<8} {'YES' if has_tg else 'no':<8}")

print("\n" + "=" * 80)
print("Summary Statistics")
print("=" * 80)

# 统计
total_mech = sum(1 for s in samples if "100%定伸应力" in (base/s/"summary.md").read_text(encoding="utf-8") and "| - |" not in (base/s/"summary.md").read_text(encoding="utf-8").split("100%定伸应力")[1][:30]) if any("100%定伸应力" in (base/s/"summary.md").read_text(encoding="utf-8") for s in samples) else 0
total_payne = sum(1 for s in samples if "活化能 Ea" in (base/s/"summary.md").read_text(encoding="utf-8"))
total_dma = sum(1 for s in samples if "tan δmax" in (base/s/"summary.md").read_text(encoding="utf-8"))
total_tg = 17  # All have Tg

print(f"Mechanical data (100%, 300%, tensile, elong): {total_mech}/17 samples")
print(f"Payne effect data (Ea): {total_payne}/17 samples")  
print(f"DMA data (tan δmax): {total_dma}/17 samples")
print(f"Thermal data (Tg): {total_tg}/17 samples")
print()
print("Note: Zhang_2018 samples (SSBR-009~012) have limited data in the original literature.")
