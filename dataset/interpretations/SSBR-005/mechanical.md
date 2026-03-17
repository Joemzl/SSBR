---
sample_id: SSBR-005
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
  stress_100:
    value: 11.0
    unit: MPa
    source: "SI Table S5"
  stress_300:
    value: null
    unit: MPa
    source: "断裂伸长率105%，未达300%定伸"
  tensile_strength:
    value: 11.9
    unit: MPa
    source: "SI Table S5"
  elongation:
    value: 105
    unit: "%"
    source: "SI Table S5"
  mechanical_source: "L1"
  bound_rubber:
    value: 80.20
    unit: "%"
    source: "Table 1"
  tan_delta_7_strain:
    value: 0.065
    unit: "-"
    source: "SI Table S4"
  tan_delta_0c:
    value: 1.342
    unit: "-"
    source: "SI Table S6"
  tg_dma:
    value: -1.1
    unit: "℃"
    source: "SI Table S6"
---

# 力学性能解读：SSBR-005

> **样本性质**: MPTES官能化SSBR（高接枝量，约70个分子），官能化程度9.5 wt%

## 核心数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100%定伸应力 | 11.0 | MPa | SI Table S5 |
| 拉伸强度 | 11.9 | MPa | SI Table S5 |
| 断裂伸长率 | **105** | % | SI Table S5 |
| 结合橡胶含量 | **80.20** | % | Table 1 |
| tan δ (7% strain) | **0.065** | - | SI Table S4 |
| Tg (DMA) | -1.1 | ℃ | SI Table S6 |
| tan δ (0℃) | **1.342** | - | SI Table S6 |

## 核心发现

SSBR-g-MPTES70 展现极端界面特性：

1. **最高结合橡胶**: 80.20%，表明最强的界面网络
2. **最低 Payne 效应**: tan δ (7%) = 0.065，分散性最优
3. **最低伸长率**: 105%，过强的界面限制了链段运动

文献原文：
> "The excessively strong rubber–rubber networks led to **poor mechanical properties**."

---

## 轮胎性能

- **滚动阻力降低**: 50.8%（所有样品最优）
- **湿地抓地力提升**: 184.3%（所有样品最优）

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
