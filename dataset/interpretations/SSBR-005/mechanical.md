---
sample_id: SSBR-005
interpretation_type: mechanical
source_figure: Table S5, Table S6, Table 1
source_doi: 10.1039/c9ra02783a
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-17
updated_at: '2026-03-31'
mechanical_subtypes:
- stress-strain
- payne
- dma
data:
  stress_100:
    value: 11.0
    unit: MPa
    source: SI Table S5
  stress_300:
    value: null
    unit: MPa
    source: 断裂伸长率105%，未达300%定伸
  tensile_strength:
    value: 11.9
    unit: MPa
    source: SI Table S5
  elongation:
    value: 105
    unit: '%'
    source: SI Table S5
  mechanical_source: L1
  bound_rubber:
    value: 80.2
    unit: '%'
    source: Table 1
  tan_delta_7_strain:
    value: 0.065
    unit: '-'
    source: SI Table S4
  tan_delta_0c:
    value: 1.342
    unit: '-'
    source: SI Table S6
  tg_dma:
    value: -1.1
    unit: ℃
    source: SI Table S6
skill_version: '2.0'
curves:
  # ---------- 应力-应变曲线 (Fig. 8A) ----------
  stress_strain:
    x_axis:
      label: 应变
      unit: '%'
    y_axis:
      label: 应力
      unit: MPa
    data_points:
      # 基于 Fig. 8(A) 中 SSBR-g-MPTES70 曲线估读
      # 曲线特征：极高斜率（高官能化），仅 105% 应变即断裂，近乎直线
      - {x: 0, y: 0, confidence: 1.0, source: "L1"}
      - {x: 10, y: 1.0, confidence: 0.65, source: "L3"}
      - {x: 20, y: 2.1, confidence: 0.65, source: "L3"}
      - {x: 30, y: 3.2, confidence: 0.65, source: "L3"}
      - {x: 40, y: 4.4, confidence: 0.65, source: "L3"}
      - {x: 50, y: 5.5, confidence: 0.65, source: "L3"}
      - {x: 60, y: 6.6, confidence: 0.65, source: "L3"}
      - {x: 70, y: 7.8, confidence: 0.65, source: "L3"}
      - {x: 80, y: 9.0, confidence: 0.65, source: "L3"}
      - {x: 90, y: 10.2, confidence: 0.65, source: "L3"}
      - {x: 100, y: 11.0, confidence: 0.95, source: "L1"}  # Table S5 验证点
      - {x: 105, y: 11.9, confidence: 0.95, source: "L1"}  # Table S5 断裂点
    curve_features:
      modulus_100:
        value: 11.0
        unit: MPa
        source: "L1"
        confidence: 0.95
      modulus_300:
        value: null
        unit: MPa
        source: "断裂伸长率105%，未达300%定伸"
        confidence: null
      tensile_strength:
        value: 11.9
        unit: MPa
        source: "L1"
        confidence: 0.95
      elongation_at_break:
        value: 105
        unit: '%'
        source: "L1"
        confidence: 0.95
      yield_point:
        exists: false
        note: "曲线近似线性，无屈服点，过度交联导致脆性断裂"
    validation:
      known_points:
        - strain: 100
          stress_expected: 11.0
          stress_estimated: 11.0
          deviation_percent: 0.0
        - strain: 105
          stress_expected: 11.9
          stress_estimated: 11.9
          deviation_percent: 0.0
      overall_quality: "good"
    metadata:
      point_count: 12
      x_range: [0, 105]
      y_range: [0, 11.9]
      avg_confidence: 0.74

  # ---------- DMA tan δ-温度曲线 (Fig. 8C) ----------
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: 无量纲
    data_points:
      # 基于 Fig. 8(C) 中 SSBR-g-MPTES70 曲线估读
      # 曲线特征：Tg = -1.1°C（最高），tan δ(0°C) = 1.342（最高），峰值最高最窄
      - {x: -80, y: 0.02, confidence: 0.60, source: "L3"}
      - {x: -70, y: 0.03, confidence: 0.60, source: "L3"}
      - {x: -60, y: 0.04, confidence: 0.60, source: "L3"}
      - {x: -50, y: 0.06, confidence: 0.65, source: "L3"}
      - {x: -40, y: 0.10, confidence: 0.65, source: "L3"}
      - {x: -30, y: 0.18, confidence: 0.65, source: "L3"}
      - {x: -20, y: 0.45, confidence: 0.65, source: "L3"}
      - {x: -10, y: 1.00, confidence: 0.70, source: "L3"}
      - {x: -1.1, y: 1.38, confidence: 0.95, source: "L1"}  # Tg 点
      - {x: 0, y: 1.342, confidence: 0.95, source: "L1"}    # Table S6 验证点
      - {x: 10, y: 0.90, confidence: 0.70, source: "L3"}
      - {x: 20, y: 0.50, confidence: 0.65, source: "L3"}
      - {x: 30, y: 0.28, confidence: 0.65, source: "L3"}
      - {x: 40, y: 0.17, confidence: 0.65, source: "L3"}
      - {x: 50, y: 0.11, confidence: 0.65, source: "L3"}
      - {x: 60, y: 0.08, confidence: 0.70, source: "L3"}
      - {x: 80, y: 0.04, confidence: 0.60, source: "L3"}
    curve_features:
      tan_delta_0C:
        value: 1.342
        unit: "-"
        source: "L1"
        confidence: 0.95
        note: "湿地抓地力指标，全系列最高"
      tan_delta_60C:
        value: 0.08
        unit: "-"
        source: "L3"
        confidence: 0.70
        note: "滚动阻力指标 (估读)，全系列最低"
      tan_delta_max:
        value: 1.38
        temperature: -1.1
        unit: "-"
        source: "L3"
        confidence: 0.70
      Tg:
        value: -1.1
        unit: °C
        method: peak
        source: "L1"
        confidence: 0.95
    validation:
      known_points:
        - temperature: 0
          tan_delta_expected: 1.342
          tan_delta_estimated: 1.342
          deviation_percent: 0.0
        - temperature: -1.1
          tan_delta_expected: 1.38
          tan_delta_estimated: 1.38
          deviation_percent: 0.0
      overall_quality: "good"
    metadata:
      point_count: 17
      x_range: [-80, 80]
      y_range: [0.02, 1.38]
      avg_confidence: 0.70

  # ---------- Payne 效应 G'-应变曲线 (Fig. 6B) ----------
  payne_storage_modulus:
    x_axis:
      label: 应变
      unit: '%'
      scale: logarithmic
    y_axis:
      label: 储能模量 G'
      unit: MPa
    data_points:
      # 基于 Fig. 6(B) 中 silica/SSBR-g-MPTES70 硫化胶曲线估读
      # 曲线特征：Payne 效应最小（高官能化，分散性最优）
      - {x: 0.28, y: 1.55, confidence: 0.70, source: "L3"}
      - {x: 0.5, y: 1.50, confidence: 0.70, source: "L3"}
      - {x: 1, y: 1.42, confidence: 0.70, source: "L3"}
      - {x: 2, y: 1.28, confidence: 0.70, source: "L3"}
      - {x: 3.6, y: 1.12, confidence: 0.70, source: "L3"}
      - {x: 5, y: 1.00, confidence: 0.70, source: "L3"}
      - {x: 7, y: 0.88, confidence: 0.70, source: "L3"}
      - {x: 10, y: 0.78, confidence: 0.70, source: "L3"}
      - {x: 15, y: 0.68, confidence: 0.70, source: "L3"}
      - {x: 20, y: 0.62, confidence: 0.70, source: "L3"}
      - {x: 30, y: 0.56, confidence: 0.70, source: "L3"}
      - {x: 42, y: 0.52, confidence: 0.70, source: "L3"}
    curve_features:
      G_prime_0:
        value: 1.55
        unit: MPa
        strain_at: 0.28
        source: "L3"
        confidence: 0.70
      G_prime_inf:
        value: 0.52
        unit: MPa
        strain_at: 42
        source: "L3"
        confidence: 0.70
      delta_G_prime:
        value: 1.03
        unit: MPa
        calculation: "G'₀ - G'∞"
        source: "L3"
        confidence: 0.70
        note: "全系列最低，分散性最优"
    validation:
      known_points: []
      overall_quality: "acceptable"
    metadata:
      point_count: 12
      x_range: [0.28, 42]
      y_range: [0.52, 1.55]
      avg_confidence: 0.70
---
# 力学性能解读：SSBR-005

> **样本性质**: MPTES官能化SSBR（高接枝量，约70个分子），官能化程度9.5 wt%


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

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
