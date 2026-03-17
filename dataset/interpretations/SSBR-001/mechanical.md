---
sample_id: SSBR-001
interpretation_type: mechanical
source_figure: "Table S5, Table S6"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-17
updated_at: null
mechanical_subtypes:
  - stress-strain
  - payne
  - dma

data:
  # ========== 应力-应变数据 ==========
  stress_100:
    value: 4.2
    range: null
    unit: MPa
    source: "SI Table S5"
  stress_200:
    value: null
    range: null
    unit: MPa
    source: "断裂伸长率约200%，未达200%定伸"
  stress_300:
    value: null
    range: null
    unit: MPa
    source: "断裂伸长率约200%，未达300%定伸"
  tensile_strength:
    value: 14.2
    range: null
    unit: MPa
    source: "SI Table S5"
  elongation:
    value: 200
    range: null
    unit: "%"
    source: "SI Table S5"
  mechanical_source: "SI Table S5"
  
  # ========== Payne 效应数据 ==========
  bound_rubber:
    value: 55.28
    unit: "%"
    source: "Table 1"
  tan_delta_7_strain:
    value: 0.104
    unit: "-"
    source: "SI Table S4"
  
  # ========== DMA 数据 ==========
  tan_delta_0c:
    value: 1.004
    unit: "-"
    source: "SI Table S6"
  tg_dma:
    value: -0.9
    unit: "℃"
    source: "SI Table S6"
---

# 力学性能解读：SSBR-001

> **样本性质**: MPL官能化SSBR（3-巯基丙醇接枝），官能化程度3.6 wt%，白炭黑填充复合材料

## 一、基础信息

- **样本ID**: SSBR-001
- **样品名称**: SSBR-g-MPL70（70 phr 白炭黑填充）
- **官能化试剂**: MPL（3-巯基丙醇，3-Mercapto-1-propanol）
- **官能化程度**: 3.6 wt%
- **文献DOI**: 10.1039/c9ra02783a

## 二、静态力学性能（应力-应变曲线）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100%定伸应力 | 4.2 | MPa | SI Table S5 |
| 200%定伸应力 | - | MPa | 断裂伸长率约200%，未达此定伸 |
| 300%定伸应力 | - | MPa | 断裂伸长率约200%，未达此定伸 |
| 拉伸强度 | 14.2 | MPa | SI Table S5 |
| 断裂伸长率 | 200 | % | SI Table S5 |

### 核心发现

SSBR-g-MPL70 复合材料展现出中等强度、中等伸长率的力学特性。相比空白SSBR/silica复合材料（拉伸强度8.5 MPa，伸长率120%），官能化改性显著提升了力学性能：

1. **拉伸强度提升**: 从 8.5 MPa → 14.2 MPa，提升 67%
2. **断裂伸长率提升**: 从 120% → 200%，提升 67%
3. **100%定伸应力**: 4.2 MPa，表明良好的模量特性

### 与对照组对比

| 样本 | 100%应力 (MPa) | 拉伸强度 (MPa) | 伸长率 (%) |
|------|----------------|----------------|------------|
| SSBR-g-MPL70 | 4.2 | 14.2 | 200 |
| 空白 SSBR/silica | 2.7 | 8.5 | 120 |
| 变化 | +56% | +67% | +67% |

### 分析结论

MPL官能化通过引入羟基（-OH）官能团，显著改善了SSBR与白炭黑的界面相互作用。羟基可与白炭黑表面的硅羟基形成氢键，增强了填料-橡胶界面结合力，从而提升整体力学性能。

---

## 三、动态力学性能（Payne效应）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 结合橡胶含量 | 55.28 | % | Table 1 |
| tan δ (7% strain) | 0.104 | - | SI Table S4 |

### 核心发现

1. **结合橡胶含量 55.28%**: 高于空白样品，表明官能化改善了填料-橡胶界面结合
2. **tan δ 在高应变下为 0.104**: 反映了填料网络的解构程度

### 与空白组对比

文献指出：官能化SSBR的 Payne 效应减弱，表明白炭黑分散性改善，填料网络结构更均匀。

---

## 四、动态力学性能（DMA温度扫描）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| Tg (DMA) | -0.9 | ℃ | SI Table S6 |
| tan δ (0℃) | 1.004 | - | SI Table S6 |

### 核心发现

1. **Tg 约 -0.9℃**: 相比纯SSBR略有升高，说明官能化和填料限制了链段运动
2. **tan δ (0℃) = 1.004**: 高tan δ值表明良好的湿地抓地力特性

### 轮胎应用性能分析

- **湿地抓地力指标** (tan δ @ 0℃ = 1.004): 较高，有利于湿滑路面制动性能
- **滚动阻力**: 需要60℃数据进一步评估

---

## 文献对应结论

> "The silica dispersion was improved by different functional SSBR from the TEM results, and better interface interaction was constructed between silica and rubber compared with the blank group, which resulted in outstanding mechanical and dynamic mechanical properties of the composites."

官能化通过改善白炭黑分散和构建更好的填料-橡胶界面，使复合材料获得了优异的力学和动态力学性能。

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **数据表格引用**: SI Table S4, S5, S6; Table 1
