---
sample_id: SSBR-031
doi: 10.1039/c5ra24965a
polymer_type: null
data_completeness:
  mechanical: true
  dsc: true
  nmr: true
  tem: true
created_at: '2026-03-21'
updated_at: '2026-03-24'
functionalization:
  type: in_chain
  reagent: 3-巯基丙酸 (3-MPA)
  grafting_group: 巯基
  grafting_group_smiles: S
  core_functional_group_smiles: C(=O)O
  core_functional_group_name: 羧基
  degree: 2.4 wt%
polymer_fingerprint: --214700.0-20.7---S---2.4wt%
---

# SSBR-031 综合档案

## 一句话总结

3-MPA 官能化 SSBR (9.6 wt%)，通过羧基与白炭黑形成氢键，显著提升填料-橡胶相互作用；MD 模拟揭示最优接枝量为 14.2 wt%，为分子设计提供理论指导。

---

## 研究亮点

### MD 模拟最优接枝量

文献通过分子动力学模拟发现：

| 指标 | 最优接枝量 | SSBR-031 接枝量 |
|------|----------|----------------|
| 结合能 | 14.2 wt% | 9.6 wt% |
| 自扩散系数 | 14.2 wt% | 9.6 wt% |
| 分散性 | 14.2 wt% | 9.6 wt% |

**结论**: SSBR-031 接近最优区间，但仍有提升空间

### 竞争效应机理

1. **氢键作用**: 羧基与硅羟基形成氢键，增强界面相互作用
2. **空间位阻**: 过多接枝导致空间位阻增大
3. **橡胶-橡胶相互作用**: 高接枝量下链间作用增强

三者竞争导致存在最优接枝量 (14.2 wt%)

---

## 核心性能特点

### 玻璃化转变温度 【良好】

Tg 为 -23.8℃，低温性能良好。

---

## 适用场景

- ✅ 绿色轮胎、高分散白炭黑复合材料

---

## 关键性能指标

| 类别 | 指标 | 数值 | 单位 | 评价 |
|------|------|------|------|------|
| 力学性能 | 100%定伸应力 | - | MPa | - |
| 力学性能 | 300%定伸应力 | - | MPa | - |
| 力学性能 | 拉伸强度 | - | MPa | - |
| 力学性能 | 断裂伸长率 | - | % | - |
| 热学性能 | Tg | -23.8 | ℃ | - |

---

## 解读文档完整性

| 文档类型 | 状态 | 备注 |
|----------|------|------|
| mechanical.md | ✓ | 已生成 |
| dsc.md | ✓ | 已生成 |
| nmr.md | ✓ | 已生成 |
| tem.md | ✓ | 已生成 |

---

## 文献来源

- **DOI**: 10.1039/c5ra24965a
- **引文**: Luo Y, Qu L, Su H, et al. Effect of chemical structure of elastomer on filler dispersion and interactions in silica/solution-polymerized styrene butadiene rubber composites through molecular dynamics simulation[J]. RSC Advances, 2016, 6(17): 14643-14650.

---


## 曲线数据概览 (v2.0)

本样本已完成全范围曲线数据提取，支持高精度分析和趋势外推。

### 应力-应变曲线
- **数据点数**: 0
- **应变范围**: 0-0%
- **应力范围**: 0-0 MPa
- **平均置信度**: N/A
- **交叉验证**: pending

### DMA tan δ-温度曲线
- **数据点数**: 15
- **温度范围**: -60-70℃
- **tan δ 范围**: 0.03-1.3
- **平均置信度**: 0.70
- **交叉验证**: good
- **关键特征值**:
  - Tg (tan δ 峰值): 0.1℃
  - tan δ (0℃): 1.2（湿地抓地力指标）
  - tan δ (60℃): ~0.11（滚动阻力指标）

### DSC 热流曲线
- **数据点数**: 12
- **温度范围**: -60-20℃
- **平均置信度**: 0.67
- **交叉验证**: good
- **玻璃化转变**:
  - Tg onset: -28℃
  - Tg midpoint: -23.8℃
  - Tg endpoint: -18℃
  - 转变宽度: ~10℃
---

*本综合档案由 `ssbr-summary-generator` 脚本合并生成，保留了人工撰写的解读内容，用于 RAG 语义检索。*