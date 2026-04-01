---
sample_id: SSBR-040
test_type: mechanical
data_source_level: L1
literature_doi: 10.1016/j.compscitech.2020.108482
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  stress_strain:
    x_axis:
      label: 应变
      unit: '%'
    y_axis:
      label: 应力
      unit: MPa
    data_points:
      - { x: 0, y: 0, confidence: 0.95, source: "L1 origin" }
      - { x: 50, y: 1.1, confidence: 0.65, source: "L3 estimated" }
      - { x: 100, y: 2.0, confidence: 0.95, source: "L1 Table 1 M100" }
      - { x: 150, y: 3.2, confidence: 0.65, source: "L3 estimated" }
      - { x: 200, y: 4.6, confidence: 0.65, source: "L3 estimated" }
      - { x: 250, y: 6.0, confidence: 0.65, source: "L3 estimated" }
      - { x: 300, y: 7.3, confidence: 0.95, source: "L1 Table 1 M300" }
      - { x: 350, y: 9.0, confidence: 0.65, source: "L3 estimated" }
      - { x: 400, y: 11.5, confidence: 0.65, source: "L3 estimated" }
      - { x: 450, y: 14.5, confidence: 0.65, source: "L3 estimated" }
      - { x: 486, y: 17.2, confidence: 0.95, source: "L1 Table 1 break" }
    curve_features:
      modulus_100:
        value: 2.0
        unit: MPa
        source: Table 1
        confidence: 0.95
      modulus_300:
        value: 7.3
        unit: MPa
        source: Table 1
        confidence: 0.95
      tensile_strength:
        value: 17.2
        unit: MPa
        source: Table 1
        confidence: 0.95
      elongation_at_break:
        value: 486
        unit: '%'
        source: Table 1
        confidence: 0.95
    validation:
      known_points:
        - { x: 100, y: 2.0, reference: "M100 from Table 1", deviation_percent: 0 }
        - { x: 300, y: 7.3, reference: "M300 from Table 1", deviation_percent: 0 }
        - { x: 486, y: 17.2, reference: "tensile strength", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 11
      x_range: [0, 486]
      y_range: [0, 17.2]
      avg_confidence: 0.78
  payne_storage_modulus:
    x_axis:
      label: 应变
      unit: '%'
      scale: logarithmic
    y_axis:
      label: 储能模量 G'
      unit: MPa
    data_points:
      - { x: 0.28, y: 2.10, confidence: 0.70, source: "L3 Fig.6a estimated" }
      - { x: 0.5, y: 1.95, confidence: 0.65, source: "L3 estimated" }
      - { x: 1, y: 1.75, confidence: 0.65, source: "L3 estimated" }
      - { x: 2, y: 1.50, confidence: 0.65, source: "L3 estimated" }
      - { x: 4, y: 1.25, confidence: 0.65, source: "L3 estimated" }
      - { x: 7, y: 1.00, confidence: 0.65, source: "L3 estimated" }
      - { x: 10, y: 0.85, confidence: 0.65, source: "L3 estimated" }
      - { x: 20, y: 0.68, confidence: 0.65, source: "L3 estimated" }
      - { x: 40, y: 0.58, confidence: 0.65, source: "L3 estimated" }
      - { x: 60, y: 0.55, confidence: 0.70, source: "L3 Fig.6a estimated" }
      - { x: 80, y: 0.53, confidence: 0.60, source: "L3 estimated" }
    curve_features:
      G_prime_0:
        value: 2.10
        unit: MPa
        strain_at: 0.28
        source: Fig.6a estimated
        confidence: 0.70
      G_prime_inf:
        value: 0.55
        unit: MPa
        strain_at: 60
        source: Fig.6a estimated
        confidence: 0.70
      delta_G_prime:
        value: 1550
        unit: kPa
        source: calculated
        confidence: 0.70
    validation:
      known_points:
        - { x: 0.28, y: 2.10, reference: "G'(0.28%) from Fig.6a", deviation_percent: 0 }
        - { x: 60, y: 0.55, reference: "G'(60%) from Fig.6a", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 11
      x_range: [0.28, 80]
      y_range: [0.53, 2.10]
      avg_confidence: 0.66
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: "-"
    data_points:
      - { x: -60, y: 0.04, confidence: 0.60, source: "L3 estimated" }
      - { x: -50, y: 0.08, confidence: 0.60, source: "L3 estimated" }
      - { x: -40, y: 0.22, confidence: 0.60, source: "L3 estimated" }
      - { x: -35, y: 0.42, confidence: 0.65, source: "L3 estimated" }
      - { x: -30, y: 0.55, confidence: 0.65, source: "L3 estimated" }
      - { x: -25, y: 0.62, confidence: 0.85, source: "L2 Tg peak" }
      - { x: -20, y: 0.52, confidence: 0.65, source: "L3 estimated" }
      - { x: -10, y: 0.40, confidence: 0.65, source: "L3 estimated" }
      - { x: 0, y: 0.32, confidence: 0.70, source: "L2 Fig.7b estimated" }
      - { x: 10, y: 0.24, confidence: 0.65, source: "L3 estimated" }
      - { x: 20, y: 0.18, confidence: 0.65, source: "L3 estimated" }
      - { x: 30, y: 0.14, confidence: 0.65, source: "L3 estimated" }
      - { x: 40, y: 0.11, confidence: 0.65, source: "L3 estimated" }
      - { x: 50, y: 0.10, confidence: 0.65, source: "L3 estimated" }
      - { x: 60, y: 0.095, confidence: 0.70, source: "L2 Fig.7b estimated" }
      - { x: 70, y: 0.090, confidence: 0.60, source: "L3 estimated" }
      - { x: 80, y: 0.085, confidence: 0.60, source: "L3 estimated" }
    curve_features:
      tan_delta_peak:
        value: 0.62
        temperature: -25
        unit: "-"
        source: Fig.7a DMA
        confidence: 0.85
      tan_delta_0C:
        value: 0.32
        unit: "-"
        source: Fig.7b estimated
        confidence: 0.70
      tan_delta_60C:
        value: 0.095
        unit: "-"
        source: Fig.7b estimated
        confidence: 0.70
      Tg:
        value: -25
        unit: °C
        source: Fig.7a tan δ peak
        confidence: 0.85
    validation:
      known_points:
        - { x: 0, y: 0.32, reference: "tan δ @ 0°C from Fig.7b", deviation_percent: 0 }
        - { x: 60, y: 0.095, reference: "tan δ @ 60°C from Fig.7b", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 17
      x_range: [-60, 80]
      y_range: [0.04, 0.62]
      avg_confidence: 0.66
---
# SSBR-040 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 拉伸性能

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 拉伸强度 | 17.2 MPa | Table 1 |
| 断裂伸长率 | 486% | Table 1 |
| 100%定伸应力 | 2.0 MPa | Table 1 |
| 300%定伸应力 | 7.3 MPa | Table 1 |

## Payne 效应

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| G'(0.28%) | ~2.1 MPa | Fig. 6a 估读 |
| G'(60%) | ~0.55 MPa | Fig. 6a 估读 |
| ΔG' | ~1.55 MPa | 计算值 |

## DMA 动态力学

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| tan δ (0°C) | ~0.32 | Fig. 7b 估读 |
| tan δ (60°C) | ~0.095 | Fig. 7b 估读 |

## 性能分析

SSBR-040 采用六甲基二硅氮烷 (HMDS) 原位改性纳米白炭黑，通过气相沉积法在白炭黑表面引入三甲基硅基团，提高了填料的疏水性和与 SSBR 的相容性。

### 力学性能特点

1. **拉伸强度**: 17.2 MPa，显示良好的增强效果
2. **M300/M100 比值**: 3.65，表明中等填料-橡胶相互作用
3. **断裂伸长率**: 486%，保持优异的柔韧性

### 填料分散效果

HMDS 改性有效降低了白炭黑的团聚倾向：
- ΔG' = ~1.55 MPa，Payne 效应较低
- 与未改性白炭黑相比，填料网络程度显著降低

### 动态性能

- tan δ (0°C) ≈ 0.32，保持良好的抗湿滑性能
- tan δ (60°C) ≈ 0.095，滚动阻力较低
- 综合展现了"魔三角"性能平衡的潜力
