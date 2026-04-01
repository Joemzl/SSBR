---
sample_id: SSBR-002
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
  reagent: 11-巯基十一烷酸（MUA）
  grafting_group: 巯基
  grafting_group_smiles: S
  core_functional_group_smiles: C(=O)O
  core_functional_group_name: 羧基
  degree: 8.7 wt%
polymer_fingerprint: --186000.0-20.9-39.5-S---8.7wt%
---

# SSBR-002 综合档案

## 一句话总结

综合性能最优的官能化SSBR：通过羧基双重界面作用（氢键+共价键）实现高强度（26 MPa）、良好延展性（340%）和优异湿地抓地力（tan δ 0℃ = 1.233）的完美平衡。

---

## 核心性能特点

### 【综合力学性能】评价：优秀 ⭐

SSBR-g-MUA70 在所有样品中实现了**最佳的强度-延展性平衡**：

| 指标 | SSBR-g-MUA70 | 空白 SSBR | 提升幅度 |
|------|--------------|-----------|----------|
| 拉伸强度 | 26.0 MPa | 15.0 MPa | +73% |
| 300%定伸应力 | 23.3 MPa | 9.0 MPa | +159% |
| 断裂伸长率 | 340% | 452% | -25% |

> 文献结论："Filler–rubber, filler–filler, and rubber–rubber networks reached **equilibrium** in the silica/SSBR-g-MUA composite."

### 【双重界面作用机制】评价：优秀 ⭐

MUA 的羧基提供独特的双重界面相互作用：

1. **氢键作用**: 羧基与白炭黑硅羟基形成强氢键（46 kJ/mol，是羟基氢键的 2.3 倍）
2. **共价键作用**: 羧基可与硅羟基发生酯化反应形成 Si-O-C 共价键

```
白炭黑表面              接枝链                    
   |                      |                          
 Si-OH ····· HOOC-(CH₂)₁₀-S-...  (氢键)
 Si-O-CO-(CH₂)₁₀-S-...           (酯化共价键)
```

### 【白炭黑分散性】评价：优

TEM 观察（Fig. 5D）显示白炭黑分散非常均匀，团聚和空隙很少：
- **分散性排名**: MPTES > **MUA** > MPL > 空白
- **结合橡胶含量**: 67.82%（MPL: 55.28%）

---

## 适用场景

- ✅ 绿色轮胎胎面胶

---

## 技术要点摘要

### 官能化反应

- **反应类型**: 巯基-烯点击化学
- **试剂结构**: HS-(CH₂)₁₀-COOH
- **反应位点**: SSBR 主链的 1,2-乙烯基侧链双键
- **约 4.8%** 的 1,2-聚丁二烯单元与 MUA 反应

### 界面增强机制

羧基官能团与白炭黑表面形成**双重相互作用**：
1. 氢键（羰基 C=O 和羟基 O-H 各提供一个氢键位点）
2. 酯化共价键（开放式两辊混炼过程中室温下发生）

### NMR 表征特征

- **特征峰**: 2.30-2.40 ppm（-CH₂COOH）
- **官能化确认**: 与空白 SSBR 相比出现新峰

---

---

## 关键性能指标

| 类别 | 指标 | 数值 | 单位 | 评价 |
|------|------|------|------|------|
| 力学性能 | 100%定伸应力 | 6.3 | MPa | - |
| 力学性能 | 300%定伸应力 | 23.3 | MPa | - |
| 力学性能 | 拉伸强度 | 26.0 | MPa | - |
| 力学性能 | 断裂伸长率 | 340 | % | - |
| 热学性能 | Tg | -2.1 | ℃ | - |
| 界面性能 | 结合橡胶含量 | 67.82 | % | - |

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


## 曲线数据概览 (v2.0)

本样本已完成全范围曲线数据提取，支持高精度分析和趋势外推。

### 应力-应变曲线
- **数据点数**: 14
- **应变范围**: 0-340%
- **应力范围**: 0-26.0 MPa
- **平均置信度**: 0.76
- **交叉验证**: excellent
- **拉伸强度**: 26.0 MPa
- **断裂伸长率**: 340%

### DMA tan δ-温度曲线
- **数据点数**: 17
- **温度范围**: -80-80℃
- **tan δ 范围**: 0.02-1.239
- **平均置信度**: 0.72
- **交叉验证**: excellent
- **关键特征值**:
  - Tg (tan δ 峰值): -2.1℃
  - tan δ (0℃): 1.233（湿地抓地力指标）
  - tan δ (60℃): ~0.13（滚动阻力指标）
  - 峰半高宽: ~48℃

### Payne G'-应变曲线
- **数据点数**: 12
- **应变范围**: 0.28-42% (对数间隔)
- **G' 范围**: 0.59-1.45 MPa
- **平均置信度**: 0.70
- **交叉验证**: good
- **关键特征值**:
  - G'₀: 1.45 MPa
  - G'∞: 0.59 MPa
  - ΔG': 0.856 MPa
  - 临界应变 γc: ~3.5%

### DSC 热流曲线
- **数据点数**: 16
- **温度范围**: -60-60℃
- **平均置信度**: 0.69
- **交叉验证**: good
- **玻璃化转变**:
  - Tg onset: -32℃
  - Tg midpoint: -23.7℃
  - Tg endpoint: -12℃
  - 转变宽度: ~20℃
---

*本综合档案由 `ssbr-summary-generator` 脚本合并生成，保留了人工撰写的解读内容，用于 RAG 语义检索。*