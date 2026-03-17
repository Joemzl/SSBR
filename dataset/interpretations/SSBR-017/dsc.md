---
sample_id: SSBR-017
interpretation_type: dsc
source_figure: null
source_doi: "10.1021/acs.iecr.6b04146"
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: null

data:
  tg:
    value: null
    range: null
    unit: "℃"
    source: ""
    note: "文献未提供 DSC 数据"
  tg_pure_polymer:
    value: null
    range: null
    unit: "℃"
    source: ""
  thermal_source: "N/A - 文献未包含 DSC 测试"
---

# SSBR-017 热学性能解读

## 数据可用性

**注意**: 该文献 (DOI: 10.1021/acs.iecr.6b04146) 未提供 DSC 测试数据。

文献使用 DMA 测量了玻璃化转变行为（见 mechanical.md 中的 DMA 部分），但未进行独立的 DSC 测试。

## 替代数据来源

从 DMA 数据（Figure 7）可知：
- SSBR 的玻璃化转变峰位置在 blank、one-step 和 two-step 三种配方间无显著差异
- 这表明界面偶联未显著改变 SSBR 的本体热力学性质

## 建议

如需 Tg 数据，请参考：
1. `mechanical.md` 中的 DMA 温度扫描数据
2. SSBR 2466 原料的技术数据手册（Tg 约 -20°C 附近）
