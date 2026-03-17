---
sample_id: SSBR-002
interpretation_type: mechanical
source_figure: "Table S5, Table S6, Table 1"
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
    value: 6.3
    range: null
    unit: MPa
    source: "SI Table S5"
  stress_200:
    value: null
    range: null
    unit: MPa
    source: "未达200%定伸时已测得300%数据"
  stress_300:
    value: 23.3
    range: null
    unit: MPa
    source: "SI Table S5"
  tensile_strength:
    value: 26.0
    range: null
    unit: MPa
    source: "SI Table S5"
  elongation:
    value: 340
    range: null
    unit: "%"
    source: "SI Table S5"
  mechanical_source: "L1"
  
  # ========== Payne 效应数据 ==========
  bound_rubber:
    value: 67.82
    unit: "%"
    source: "Table 1"
  tan_delta_7_strain:
    value: 0.096
    unit: "-"
    source: "SI Table S4"
  
  # ========== DMA 数据 ==========
  tan_delta_0c:
    value: 1.233
    unit: "-"
    source: "SI Table S6"
  tg_dma:
    value: -2.1
    unit: "℃"
    source: "SI Table S6"
---

# 力学性能解读：SSBR-002

> **样本性质**: MUA官能化SSBR（11-巯基十一烷酸接枝），官能化程度8.7 wt%，白炭黑填充复合材料

## 一、基础信息

- **样本ID**: SSBR-002
- **样品名称**: SSBR-g-MUA70（70 phr 白炭黑填充）
- **官能化试剂**: MUA（11-巯基十一烷酸，11-Mercaptoundecanoic acid）
- **官能化程度**: 8.7 wt%
- **文献DOI**: 10.1039/c9ra02783a

## 二、静态力学性能（应力-应变曲线）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100%定伸应力 | 6.3 | MPa | SI Table S5 |
| 200%定伸应力 | - | MPa | - |
| 300%定伸应力 | 23.3 | MPa | SI Table S5 |
| 拉伸强度 | 26.0 | MPa | SI Table S5 |
| 断裂伸长率 | 340 | % | SI Table S5 |

### 核心发现

SSBR-g-MUA70 复合材料展现出**最优异的综合力学性能**：
- 拉伸强度 26.0 MPa，在所有官能化样品中最高
- 断裂伸长率 340%，保持良好的延展性
- 300%定伸应力 23.3 MPa，表明高模量特性

### 与对照组对比

| 样本 | 100%应力 (MPa) | 300%应力 (MPa) | 拉伸强度 (MPa) | 伸长率 (%) |
|------|----------------|----------------|----------------|------------|
| SSBR-g-MUA70 | 6.3 | 23.3 | 26.0 | 340 |
| 空白 SSBR/silica | 1.5 | 9.0 | 15.0 | 452 |
| SSBR/Si69 | 2.6 | 12.8 | 21.0 | 406 |
| 变化 vs 空白 | +320% | +159% | +73% | -25% |

### 分析结论

MUA 官能化通过引入羧基（-COOH）官能团，实现了**双重界面相互作用**：
1. **氢键作用**: 羧基与白炭黑表面硅羟基形成强氢键（平均能量 46 kJ/mol）
2. **共价键作用**: 羧基可与硅羟基发生酯化反应形成共价键

这种双重作用机制使 SSBR-g-MUA70 在强度和伸长率之间达到**最佳平衡**。

---

## 三、动态力学性能（Payne效应）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 结合橡胶含量 | 67.82 | % | Table 1 |
| tan δ (7% strain) | 0.096 | - | SI Table S4 |

### 核心发现

1. **结合橡胶含量 67.82%**: 在三种单一官能化样品中最高（MPL: 55.28%, MPTES13: 46.23%）
2. **tan δ (7% strain) = 0.096**: 较低，表明 Payne 效应减弱

### 与其他样品对比

| 样本 | 结合橡胶 (%) | tan δ (7%) | 界面作用模式 |
|------|-------------|-----------|--------------|
| SSBR-g-MUA70 | 67.82 | 0.096 | 氢键 + 共价键 |
| SSBR-g-MPL70 | 55.28 | 0.104 | 单氢键 |
| SSBR-g-MPTES70 | 80.20 | 0.065 | 单共价键 |
| 空白 SSBR | 20.56 | 0.132 | 无 |

---

## 四、动态力学性能（DMA温度扫描）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| Tg (DMA) | -2.1 | ℃ | SI Table S6 |
| tan δ (0℃) | 1.233 | - | SI Table S6 |

### 核心发现

1. **Tg = -2.1℃**: 相比 MPL 样品略低，因长链烷基（十一烷基）增加了柔顺性
2. **tan δ (0℃) = 1.233**: 极高，表明优异的湿地抓地力特性

### 轮胎应用性能分析

文献指出：
> "The wet skid resistances of silica/SSBR-g-MUA composites increased by **161.2%**."

- **湿地抓地力**: tan δ @ 0℃ = 1.233，提升 161.2%
- **滚动阻力**: 降低 27.3%

---

## 五、综合评价

文献原文：
> "Filler–rubber, filler–filler, and rubber–rubber networks reached **equilibrium** in the silica/SSBR-g-MUA composite, which had **excellent overall performances** of high strength, low rolling resistance, and high wet skid resistance."

SSBR-g-MUA70 是该系列中综合性能最优的样品，实现了：
- ✅ 高拉伸强度（26.0 MPa）
- ✅ 良好伸长率（340%）
- ✅ 优异湿地抓地力（tan δ 0℃ = 1.233）
- ✅ 较低滚动阻力（降低 27.3%）

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **数据表格引用**: SI Table S4, S5, S6; Table 1
