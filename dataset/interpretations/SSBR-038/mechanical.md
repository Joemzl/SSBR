---
sample_id: SSBR-038
test_type: mechanical
data_source_level: L1
literature_doi: 10.1016/j.compscitech.2018.03.036
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
      - { x: 50, y: 1.2, confidence: 0.65, source: "L3 estimated" }
      - { x: 100, y: 2.2, confidence: 0.95, source: "L1 Table 2 M100" }
      - { x: 150, y: 3.8, confidence: 0.65, source: "L3 estimated" }
      - { x: 200, y: 5.8, confidence: 0.65, source: "L3 estimated" }
      - { x: 250, y: 7.8, confidence: 0.65, source: "L3 estimated" }
      - { x: 300, y: 9.9, confidence: 0.95, source: "L1 Table 2 M300" }
      - { x: 350, y: 12.2, confidence: 0.65, source: "L3 estimated" }
      - { x: 400, y: 15.5, confidence: 0.65, source: "L3 estimated" }
      - { x: 410, y: 16.4, confidence: 0.95, source: "L1 Table 2 break" }
    curve_features:
      modulus_100:
        value: 2.2
        unit: MPa
        source: Table 2
        confidence: 0.95
      modulus_300:
        value: 9.9
        unit: MPa
        source: Table 2
        confidence: 0.95
      tensile_strength:
        value: 16.4
        unit: MPa
        source: Table 2
        confidence: 0.95
      elongation_at_break:
        value: 410
        unit: '%'
        source: Table 2
        confidence: 0.95
    validation:
      known_points:
        - { x: 100, y: 2.2, reference: "M100 from Table 2", deviation_percent: 0 }
        - { x: 300, y: 9.9, reference: "M300 from Table 2", deviation_percent: 0 }
        - { x: 410, y: 16.4, reference: "tensile strength", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 10
      x_range: [0, 410]
      y_range: [0, 16.4]
      avg_confidence: 0.79
  payne_storage_modulus:
    x_axis:
      label: 应变
      unit: '%'
      scale: logarithmic
    y_axis:
      label: 储能模量 G'
      unit: MPa
    data_points:
      - { x: 0.28, y: 1.75, confidence: 0.70, source: "L3 Fig.8a estimated" }
      - { x: 0.5, y: 1.65, confidence: 0.65, source: "L3 estimated" }
      - { x: 1, y: 1.50, confidence: 0.65, source: "L3 estimated" }
      - { x: 2, y: 1.30, confidence: 0.65, source: "L3 estimated" }
      - { x: 4, y: 1.10, confidence: 0.65, source: "L3 estimated" }
      - { x: 7, y: 0.90, confidence: 0.65, source: "L3 estimated" }
      - { x: 10, y: 0.75, confidence: 0.65, source: "L3 estimated" }
      - { x: 15, y: 0.62, confidence: 0.65, source: "L3 estimated" }
      - { x: 25, y: 0.52, confidence: 0.65, source: "L3 estimated" }
      - { x: 40, y: 0.45, confidence: 0.70, source: "L3 Fig.8a estimated" }
      - { x: 60, y: 0.42, confidence: 0.60, source: "L3 estimated" }
    curve_features:
      G_prime_0:
        value: 1.75
        unit: MPa
        strain_at: 0.28
        source: Fig.8a estimated
        confidence: 0.70
      G_prime_inf:
        value: 0.45
        unit: MPa
        strain_at: 40
        source: Fig.8a estimated
        confidence: 0.70
      delta_G_prime:
        value: 1300
        unit: kPa
        source: calculated
        confidence: 0.70
    validation:
      known_points:
        - { x: 0.28, y: 1.75, reference: "G'(0.28%) from Fig.8a", deviation_percent: 0 }
        - { x: 40, y: 0.45, reference: "G'(40%) from Fig.8a", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 11
      x_range: [0.28, 60]
      y_range: [0.42, 1.75]
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
      - { x: -40, y: 0.20, confidence: 0.60, source: "L3 estimated" }
      - { x: -35, y: 0.40, confidence: 0.65, source: "L3 estimated" }
      - { x: -30, y: 0.55, confidence: 0.65, source: "L3 estimated" }
      - { x: -28, y: 0.58, confidence: 0.85, source: "L2 Tg peak" }
      - { x: -25, y: 0.52, confidence: 0.65, source: "L3 estimated" }
      - { x: -20, y: 0.42, confidence: 0.65, source: "L3 estimated" }
      - { x: -10, y: 0.28, confidence: 0.65, source: "L3 estimated" }
      - { x: 0, y: 0.186, confidence: 0.95, source: "L1 Table 2" }
      - { x: 10, y: 0.155, confidence: 0.65, source: "L3 estimated" }
      - { x: 20, y: 0.135, confidence: 0.65, source: "L3 estimated" }
      - { x: 30, y: 0.120, confidence: 0.65, source: "L3 estimated" }
      - { x: 40, y: 0.108, confidence: 0.65, source: "L3 estimated" }
      - { x: 50, y: 0.102, confidence: 0.65, source: "L3 estimated" }
      - { x: 60, y: 0.099, confidence: 0.95, source: "L1 Table 2" }
      - { x: 80, y: 0.090, confidence: 0.60, source: "L3 estimated" }
    curve_features:
      tan_delta_peak:
        value: 0.58
        temperature: -28
        unit: "-"
        source: Fig.7 DMA
        confidence: 0.85
      tan_delta_0C:
        value: 0.186
        unit: "-"
        source: Table 2
        confidence: 0.95
      tan_delta_60C:
        value: 0.099
        unit: "-"
        source: Table 2
        confidence: 0.95
      Tg:
        value: -28
        unit: °C
        source: Fig.7 tan δ peak
        confidence: 0.85
    validation:
      known_points:
        - { x: 0, y: 0.186, reference: "tan δ @ 0°C from Table 2", deviation_percent: 0 }
        - { x: 60, y: 0.099, reference: "tan δ @ 60°C from Table 2", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 17
      x_range: [-60, 80]
      y_range: [0.04, 0.58]
      avg_confidence: 0.70
---
# SSBR-038 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 拉伸性能

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 拉伸强度 | 16.4 MPa | Table 2, TSb |
| 断裂伸长率 | 410% | Table 2, Eb |
| 100%定伸应力 | 2.2 MPa | Table 2, M100 |
| 300%定伸应力 | 9.9 MPa | Table 2, M300 |

## Payne 效应

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| G'(0.28%) | ~1.75 MPa | Fig. 8a 估读 |
| G'(40%) | ~0.45 MPa | Fig. 8a 估读 |
| ΔG' | ~1.30 MPa | 计算值 |

## DMA 动态力学

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| tan δ (0°C) | 0.186 | Table 2 |
| tan δ (60°C) | 0.099 | Table 2 |

## 性能分析

SSBR-038 采用烷基硫醇 (DT, dodecanethiol) 改性氧化石墨烯 (GO)，通过硫醇-烯点击反应将 C12 烷基链接枝到 GO 表面，改善了 GO 与 SSBR 基体的相容性。

### 力学性能特点

1. **拉伸强度**: 16.4 MPa，比未改性 GO 复合材料 (13.7 MPa) 提高 20%
2. **M300/M100 比值**: 4.5，显示良好的填料-橡胶相互作用
3. **断裂伸长率**: 410%，保持良好的柔韧性

### 填料分散效果

烷基硫醇改性显著改善了 GO 在 SSBR 中的分散性：
- ΔG' 从未改性 GO 的 ~2.0 MPa 降至 ~1.30 MPa
- 表明填料网络程度降低，分散性提升

### 动态性能

- tan δ (0°C) = 0.186，抗湿滑性能良好
- tan δ (60°C) = 0.099，滚动阻力较低
- 相比未改性 GO，60°C tan δ 降低约 15%
