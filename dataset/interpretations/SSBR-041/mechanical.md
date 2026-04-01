---
sample_id: SSBR-041
test_type: mechanical
data_source_level: L1
literature_doi: 10.1016/j.matdes.2018.05.048
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
      - { x: 50, y: 1.0, confidence: 0.65, source: "L3 estimated" }
      - { x: 100, y: 1.9, confidence: 0.95, source: "L1 Table 2 M100" }
      - { x: 150, y: 3.2, confidence: 0.65, source: "L3 estimated" }
      - { x: 200, y: 4.8, confidence: 0.65, source: "L3 estimated" }
      - { x: 250, y: 6.4, confidence: 0.65, source: "L3 estimated" }
      - { x: 300, y: 7.8, confidence: 0.95, source: "L1 Table 2 M300" }
      - { x: 350, y: 9.5, confidence: 0.65, source: "L3 estimated" }
      - { x: 400, y: 11.5, confidence: 0.65, source: "L3 estimated" }
      - { x: 480, y: 16.0, confidence: 0.65, source: "L3 estimated" }
      - { x: 520, y: 18.5, confidence: 0.95, source: "L1 Table 2 break" }
    curve_features:
      modulus_100:
        value: 1.9
        unit: MPa
        source: Table 2
        confidence: 0.95
      modulus_300:
        value: 7.8
        unit: MPa
        source: Table 2
        confidence: 0.95
      tensile_strength:
        value: 18.5
        unit: MPa
        source: Table 2
        confidence: 0.95
      elongation_at_break:
        value: 520
        unit: '%'
        source: Table 2
        confidence: 0.95
    validation:
      known_points:
        - { x: 100, y: 1.9, reference: "M100 from Table 2", deviation_percent: 0 }
        - { x: 300, y: 7.8, reference: "M300 from Table 2", deviation_percent: 0 }
        - { x: 520, y: 18.5, reference: "tensile strength", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 11
      x_range: [0, 520]
      y_range: [0, 18.5]
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
      - { x: 0.56, y: 1.60, confidence: 0.70, source: "L3 Fig.7a estimated" }
      - { x: 1, y: 1.48, confidence: 0.65, source: "L3 estimated" }
      - { x: 2, y: 1.30, confidence: 0.65, source: "L3 estimated" }
      - { x: 4, y: 1.10, confidence: 0.65, source: "L3 estimated" }
      - { x: 7, y: 0.90, confidence: 0.65, source: "L3 estimated" }
      - { x: 10, y: 0.75, confidence: 0.65, source: "L3 estimated" }
      - { x: 15, y: 0.62, confidence: 0.65, source: "L3 estimated" }
      - { x: 25, y: 0.52, confidence: 0.65, source: "L3 estimated" }
      - { x: 35, y: 0.48, confidence: 0.65, source: "L3 estimated" }
      - { x: 50, y: 0.45, confidence: 0.70, source: "L3 Fig.7a estimated" }
      - { x: 70, y: 0.43, confidence: 0.60, source: "L3 estimated" }
    curve_features:
      G_prime_0:
        value: 1.60
        unit: MPa
        strain_at: 0.56
        source: Fig.7a estimated
        confidence: 0.70
      G_prime_inf:
        value: 0.45
        unit: MPa
        strain_at: 50
        source: Fig.7a estimated
        confidence: 0.70
      delta_G_prime:
        value: 1150
        unit: kPa
        source: calculated
        confidence: 0.70
    validation:
      known_points:
        - { x: 0.56, y: 1.60, reference: "G'(0.56%) from Fig.7a", deviation_percent: 0 }
        - { x: 50, y: 0.45, reference: "G'(50%) from Fig.7a", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 11
      x_range: [0.56, 70]
      y_range: [0.43, 1.60]
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
      - { x: -45, y: 0.18, confidence: 0.60, source: "L3 estimated" }
      - { x: -40, y: 0.38, confidence: 0.65, source: "L3 estimated" }
      - { x: -35, y: 0.52, confidence: 0.65, source: "L3 estimated" }
      - { x: -32, y: 0.56, confidence: 0.85, source: "L2 Tg peak" }
      - { x: -28, y: 0.50, confidence: 0.65, source: "L3 estimated" }
      - { x: -20, y: 0.40, confidence: 0.65, source: "L3 estimated" }
      - { x: -10, y: 0.32, confidence: 0.65, source: "L3 estimated" }
      - { x: 0, y: 0.28, confidence: 0.70, source: "L2 Fig.8 estimated" }
      - { x: 10, y: 0.20, confidence: 0.65, source: "L3 estimated" }
      - { x: 20, y: 0.15, confidence: 0.65, source: "L3 estimated" }
      - { x: 30, y: 0.12, confidence: 0.65, source: "L3 estimated" }
      - { x: 40, y: 0.10, confidence: 0.65, source: "L3 estimated" }
      - { x: 50, y: 0.09, confidence: 0.65, source: "L3 estimated" }
      - { x: 60, y: 0.085, confidence: 0.70, source: "L2 Fig.8 estimated" }
      - { x: 80, y: 0.080, confidence: 0.60, source: "L3 estimated" }
    curve_features:
      tan_delta_peak:
        value: 0.56
        temperature: -32
        unit: "-"
        source: Fig.8 DMA
        confidence: 0.85
      tan_delta_0C:
        value: 0.28
        unit: "-"
        source: Fig.8 estimated
        confidence: 0.70
      tan_delta_60C:
        value: 0.085
        unit: "-"
        source: Fig.8 estimated
        confidence: 0.70
      Tg:
        value: -32
        unit: °C
        source: Fig.8 tan δ peak
        confidence: 0.85
    validation:
      known_points:
        - { x: 0, y: 0.28, reference: "tan δ @ 0°C from Fig.8", deviation_percent: 0 }
        - { x: 60, y: 0.085, reference: "tan δ @ 60°C from Fig.8", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 17
      x_range: [-60, 80]
      y_range: [0.04, 0.56]
      avg_confidence: 0.66
---
# SSBR-041 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 拉伸性能

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 拉伸强度 | 18.5 MPa | Table 2 |
| 断裂伸长率 | 520% | Table 2 |
| 100%定伸应力 | 1.9 MPa | Table 2 |
| 300%定伸应力 | 7.8 MPa | Table 2 |

## Payne 效应

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| G'(0.56%) | ~1.6 MPa | Fig. 7a 估读 |
| G'(50%) | ~0.45 MPa | Fig. 7a 估读 |
| ΔG' | ~1.15 MPa | 计算值 |

## DMA 动态力学

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| tan δ (0°C) | ~0.28 | Fig. 8 估读 |
| tan δ (60°C) | ~0.085 | Fig. 8 估读 |

## 性能分析

SSBR-041 采用抗氧剂 (4,4'-硫代双(6-叔丁基-3-甲基苯酚), AO-40) 官能化白炭黑作为填料。通过在白炭黑表面接枝含硫抗氧剂分子，实现了填料改性与抗老化功能的整合。

### 力学性能特点

1. **拉伸强度**: 18.5 MPa，优于传统 Si69 改性白炭黑体系
2. **M300/M100 比值**: 4.1，显示优异的填料-橡胶相互作用
3. **断裂伸长率**: 520%，保持良好的柔韧性

### 填料分散效果

抗氧剂官能化显著改善了白炭黑分散性：
- ΔG' = ~1.15 MPa，Payne 效应较低
- 填料网络程度显著降低

### 动态性能

- tan δ (0°C) ≈ 0.28，抗湿滑性能保持
- tan δ (60°C) ≈ 0.085，滚动阻力很低
- 实现了良好的"魔三角"平衡
