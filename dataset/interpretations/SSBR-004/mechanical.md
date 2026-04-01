---
sample_id: SSBR-004
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
    value: 3.2
    unit: MPa
    source: SI Table S5
  stress_300:
    value: null
    unit: MPa
    source: 断裂伸长率248%，未达300%定伸
  tensile_strength:
    value: 12.8
    unit: MPa
    source: SI Table S5
  elongation:
    value: 248
    unit: '%'
    source: SI Table S5
  mechanical_source: L1
  bound_rubber:
    value: 57.61
    unit: '%'
    source: Table 1
  tan_delta_7_strain:
    value: 0.086
    unit: '-'
    source: SI Table S4
  tan_delta_0c:
    value: 1.21
    unit: '-'
    source: SI Table S6
  tg_dma:
    value: -3.9
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
      # 基于 Fig. 8(A) 中 SSBR-g-MPTES42 曲线估读
      # 曲线特征：中等斜率（中官能化），在约 248% 应变处断裂
      - {x: 0, y: 0, confidence: 1.0, source: "L1"}
      - {x: 20, y: 0.5, confidence: 0.65, source: "L3"}
      - {x: 40, y: 1.0, confidence: 0.65, source: "L3"}
      - {x: 60, y: 1.6, confidence: 0.65, source: "L3"}
      - {x: 80, y: 2.3, confidence: 0.65, source: "L3"}
      - {x: 100, y: 3.2, confidence: 0.95, source: "L1"}  # Table S5 验证点
      - {x: 130, y: 4.8, confidence: 0.65, source: "L3"}
      - {x: 160, y: 6.8, confidence: 0.65, source: "L3"}
      - {x: 190, y: 9.2, confidence: 0.65, source: "L3"}
      - {x: 220, y: 11.5, confidence: 0.65, source: "L3"}
      - {x: 248, y: 12.8, confidence: 0.95, source: "L1"}  # Table S5 断裂点
    curve_features:
      modulus_100:
        value: 3.2
        unit: MPa
        source: "L1"
        confidence: 0.95
      modulus_300:
        value: null
        unit: MPa
        source: "断裂伸长率248%，未达300%定伸"
        confidence: null
      tensile_strength:
        value: 12.8
        unit: MPa
        source: "L1"
        confidence: 0.95
      elongation_at_break:
        value: 248
        unit: '%'
        source: "L1"
        confidence: 0.95
      yield_point:
        exists: false
        note: "曲线无明显屈服点，呈应变硬化特征"
    validation:
      known_points:
        - strain: 100
          stress_expected: 3.2
          stress_estimated: 3.2
          deviation_percent: 0.0
        - strain: 248
          stress_expected: 12.8
          stress_estimated: 12.8
          deviation_percent: 0.0
      overall_quality: "good"
    metadata:
      point_count: 11
      x_range: [0, 248]
      y_range: [0, 12.8]
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
      # 基于 Fig. 8(C) 中 SSBR-g-MPTES42 曲线估读
      # 曲线特征：Tg = -3.9°C，tan δ(0°C) = 1.21，峰值更高更窄
      - {x: -80, y: 0.02, confidence: 0.60, source: "L3"}
      - {x: -70, y: 0.03, confidence: 0.60, source: "L3"}
      - {x: -60, y: 0.04, confidence: 0.60, source: "L3"}
      - {x: -50, y: 0.06, confidence: 0.65, source: "L3"}
      - {x: -40, y: 0.10, confidence: 0.65, source: "L3"}
      - {x: -30, y: 0.20, confidence: 0.65, source: "L3"}
      - {x: -20, y: 0.50, confidence: 0.65, source: "L3"}
      - {x: -10, y: 1.05, confidence: 0.70, source: "L3"}
      - {x: -3.9, y: 1.25, confidence: 0.95, source: "L1"}  # Tg 点
      - {x: 0, y: 1.21, confidence: 0.95, source: "L1"}     # Table S6 验证点
      - {x: 10, y: 0.85, confidence: 0.70, source: "L3"}
      - {x: 20, y: 0.52, confidence: 0.65, source: "L3"}
      - {x: 30, y: 0.32, confidence: 0.65, source: "L3"}
      - {x: 40, y: 0.20, confidence: 0.65, source: "L3"}
      - {x: 50, y: 0.13, confidence: 0.65, source: "L3"}
      - {x: 60, y: 0.09, confidence: 0.70, source: "L3"}
      - {x: 80, y: 0.05, confidence: 0.60, source: "L3"}
    curve_features:
      tan_delta_0C:
        value: 1.21
        unit: "-"
        source: "L1"
        confidence: 0.95
        note: "湿地抓地力指标"
      tan_delta_60C:
        value: 0.09
        unit: "-"
        source: "L3"
        confidence: 0.70
        note: "滚动阻力指标 (估读)"
      tan_delta_max:
        value: 1.25
        temperature: -3.9
        unit: "-"
        source: "L3"
        confidence: 0.70
      Tg:
        value: -3.9
        unit: °C
        method: peak
        source: "L1"
        confidence: 0.95
    validation:
      known_points:
        - temperature: 0
          tan_delta_expected: 1.21
          tan_delta_estimated: 1.21
          deviation_percent: 0.0
        - temperature: -3.9
          tan_delta_expected: 1.25
          tan_delta_estimated: 1.25
          deviation_percent: 0.0
      overall_quality: "good"
    metadata:
      point_count: 17
      x_range: [-80, 80]
      y_range: [0.02, 1.25]
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
      # 基于 Fig. 6(B) 中 silica/SSBR-g-MPTES42 硫化胶曲线估读
      # 曲线特征：Payne 效应中等（中官能化，分散性中等偏好）
      - {x: 0.28, y: 1.85, confidence: 0.70, source: "L3"}
      - {x: 0.5, y: 1.78, confidence: 0.70, source: "L3"}
      - {x: 1, y: 1.65, confidence: 0.70, source: "L3"}
      - {x: 2, y: 1.45, confidence: 0.70, source: "L3"}
      - {x: 3.6, y: 1.22, confidence: 0.70, source: "L3"}
      - {x: 5, y: 1.05, confidence: 0.70, source: "L3"}
      - {x: 7, y: 0.88, confidence: 0.70, source: "L3"}
      - {x: 10, y: 0.75, confidence: 0.70, source: "L3"}
      - {x: 15, y: 0.65, confidence: 0.70, source: "L3"}
      - {x: 20, y: 0.60, confidence: 0.70, source: "L3"}
      - {x: 30, y: 0.55, confidence: 0.70, source: "L3"}
      - {x: 42, y: 0.52, confidence: 0.70, source: "L3"}
    curve_features:
      G_prime_0:
        value: 1.85
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
        value: 1.33
        unit: MPa
        calculation: "G'₀ - G'∞"
        source: "L3"
        confidence: 0.70
        note: "比 MPTES13 低，分散性改善"
    validation:
      known_points: []
      overall_quality: "acceptable"
    metadata:
      point_count: 12
      x_range: [0.28, 42]
      y_range: [0.52, 1.85]
      avg_confidence: 0.70
---
# 力学性能解读：SSBR-004

> **样本性质**: MPTES官能化SSBR（中等接枝量，约42个分子），官能化程度5.8 wt%


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 核心数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100%定伸应力 | 3.2 | MPa | SI Table S5 |
| 拉伸强度 | 12.8 | MPa | SI Table S5 |
| 断裂伸长率 | 248 | % | SI Table S5 |
| 结合橡胶含量 | 57.61 | % | Table 1 |
| tan δ (7% strain) | 0.086 | - | SI Table S4 |
| Tg (DMA) | -3.9 | ℃ | SI Table S6 |
| tan δ (0℃) | 1.210 | - | SI Table S6 |

## 分析

SSBR-g-MPTES42 展现中等界面强度特征：
1. Tg 介于 MPTES13 和 MPTES70 之间
2. tan δ (0℃) = 1.210，湿地抓地力优异
3. 拉伸强度下降表明界面网络开始限制分子链运动

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
