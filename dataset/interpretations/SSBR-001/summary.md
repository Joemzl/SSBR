---
sample_id: SSBR-001
doi: 10.1039/c9ra02783a
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
  reagent: 3-巯基丙醇（MPL）
  grafting_group: 巯基
  grafting_group_smiles: S
  core_functional_group_smiles: O
  core_functional_group_name: 羟基
  degree: 3.6 wt%
polymer_fingerprint: --185000.0-23.0-40.1-S---3.6wt%
---

# SSBR-001 综合档案

## 一句话总结

适用于需要改善白炭黑分散性、提升力学强度和湿地抓地力的轮胎胎面配方，采用羟基官能化实现界面氢键增强。

---

## 核心性能特点

### 【白炭黑分散改善】评价：良好

TEM 观察（Fig. 5C）显示白炭黑在 SSBR-g-MPL70 复合材料中分散相当均匀，团聚和空隙较少。相比未改性 SSBR，分散性显著改善。

> 文献原文："The dispersions of silica in the silica/F-SSBR composites were quite uniform with fewer aggregates and voids compared with silica/SSBR."

在三种官能化样品中，分散性排序为：MPTES（共价键）> MUA（羧基双氢键）> **MPL（羟基单氢键）**

### 【力学性能提升】评价：良好

官能化改性显著提升了复合材料的力学性能：

| 指标 | SSBR-g-MPL70 | 空白 SSBR | 提升幅度 |
|------|--------------|-----------|----------|
| 100%定伸应力 | 4.2 MPa | 2.7 MPa | +56% |
| 拉伸强度 | 14.2 MPa | 8.5 MPa | +67% |
| 断裂伸长率 | 200% | 120% | +67% |

### 【界面相互作用增强】评价：良好

多项指标反映出填料-橡胶界面相互作用的增强：

1. **结合橡胶含量**: 55.28%，高于空白样品
2. **Tg 上移幅度**: ΔTg = 23.9℃（纯聚合物 → 复合材料），显著高于空白组的 19.8℃
3. **界面作用机制**: 羟基与白炭黑表面硅羟基形成氢键

```
白炭黑表面        接枝链            SSBR 主链
   |                |                  |
 Si-OH ····· HO-CH₂-CH₂-CH₂-S-CH₂-CH= (聚合物链)
   ↑          ↑               ↑
  硅羟基    羟基氢键        巯基-烯加成点
```

### 【湿地抓地力特性】评价：优秀

- **tan δ (0℃) = 1.004**: 高 tan δ 值表明良好的湿滑路面制动性能
- **Tg (复合材料) = -0.9℃**: 玻璃化转变区域覆盖 0℃ 附近，有利于湿地抓地

---

---

## 适用场景

- ✅ 绿色轮胎胎面胶

---

## 技术要点摘要

### 官能化反应

- **反应类型**: 巯基-烯点击化学（UV 或热引发）
- **反应位点**: SSBR 主链的 1,2-乙烯基侧链双键
- **反应特点**: 选择性高，反应条件温和，官能团耐受性好

### 界面增强机制

羟基官能团与白炭黑表面硅羟基形成单氢键：
- 界面结合力中等（弱于共价键和双氢键）
- 填料分散性改善
- Payne 效应减弱

### NMR 表征特征

- **特征峰**: 3.70-3.85 ppm（-CH₂OH）
- **官能化确认**: 与空白 SSBR 相比出现新峰

---

---

## 关键性能指标

| 类别 | 指标 | 数值 | 单位 | 评价 |
|------|------|------|------|------|
| 力学性能 | 100%定伸应力 | 4.2 | MPa | - |
| 力学性能 | 300%定伸应力 | - | MPa | - |
| 力学性能 | 拉伸强度 | 14.2 | MPa | - |
| 力学性能 | 断裂伸长率 | 200 | % | - |
| 热学性能 | Tg | -0.9 | ℃ | - |
| 界面性能 | 结合橡胶含量 | 55.28 | % | - |

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

- **DOI**: 10.1039/c9ra02783a
- **引文**: Gao W, Lu J, Song W, et al. Interfacial interaction modes construction of various functional SSBR–silica towards high filler dispersion and excellent composites performances[J]. RSC Advances, 2019, 9(31): 18888-18897.

---

*本综合档案由 `ssbr-summary-generator` 脚本合并生成，保留了人工撰写的解读内容，用于 RAG 语义检索。*