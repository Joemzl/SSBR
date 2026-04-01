---
sample_id: SSBR-045
test_type: mechanical
data_source_level: L1
literature_doi: 10.1002/app.29646
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
      - { x: 50, y: 1.3, confidence: 0.65, source: "L3 estimated" }
      - { x: 100, y: 2.3, confidence: 0.95, source: "L1 Table 1 M100" }
      - { x: 150, y: 3.8, confidence: 0.65, source: "L3 estimated" }
      - { x: 200, y: 5.8, confidence: 0.65, source: "L3 estimated" }
      - { x: 250, y: 8.0, confidence: 0.65, source: "L3 estimated" }
      - { x: 300, y: 10.5, confidence: 0.95, source: "L1 Table 1 M300" }
      - { x: 330, y: 12.0, confidence: 0.65, source: "L3 estimated" }
      - { x: 360, y: 13.5, confidence: 0.65, source: "L3 estimated" }
      - { x: 380, y: 14.2, confidence: 0.95, source: "L1 Table 1 break" }
    curve_features:
      modulus_100:
        value: 2.3
        unit: MPa
        source: Table 1
        confidence: 0.95
      modulus_300:
        value: 10.5
        unit: MPa
        source: Table 1
        confidence: 0.95
      tensile_strength:
        value: 14.2
        unit: MPa
        source: Table 1
        confidence: 0.95
      elongation_at_break:
        value: 380
        unit: '%'
        source: Table 1
        confidence: 0.95
    validation:
      known_points:
        - { x: 100, y: 2.3, reference: "M100 from Table 1", deviation_percent: 0 }
        - { x: 300, y: 10.5, reference: "M300 from Table 1", deviation_percent: 0 }
        - { x: 380, y: 14.2, reference: "tensile strength", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 10
      x_range: [0, 380]
      y_range: [0, 14.2]
      avg_confidence: 0.80
  payne_storage_modulus:
    x_axis:
      label: 应变
      unit: '%'
      scale: logarithmic
    y_axis:
      label: 储能模量 G'
      unit: MPa
    data_points:
      - { x: 0.1, y: 1.80, confidence: 0.70, source: "L3 Fig.2 estimated" }
      - { x: 0.2, y: 1.70, confidence: 0.65, source: "L3 estimated" }
      - { x: 0.5, y: 1.50, confidence: 0.65, source: "L3 estimated" }
      - { x: 1, y: 1.25, confidence: 0.65, source: "L3 estimated" }
      - { x: 2, y: 1.02, confidence: 0.65, source: "L3 estimated" }
      - { x: 4, y: 0.82, confidence: 0.65, source: "L3 estimated" }
      - { x: 6, y: 0.72, confidence: 0.65, source: "L3 estimated" }
      - { x: 8, y: 0.65, confidence: 0.65, source: "L3 estimated" }
      - { x: 10, y: 0.60, confidence: 0.70, source: "L3 Fig.2 estimated" }
      - { x: 15, y: 0.55, confidence: 0.60, source: "L3 estimated" }
    curve_features:
      G_prime_0:
        value: 1.80
        unit: MPa
        strain_at: 0.1
        source: Fig.2 estimated
        confidence: 0.70
      G_prime_inf:
        value: 0.60
        unit: MPa
        strain_at: 10
        source: Fig.2 estimated
        confidence: 0.70
      delta_G_prime:
        value: 1200
        unit: kPa
        source: calculated
        confidence: 0.70
    validation:
      known_points:
        - { x: 0.1, y: 1.80, reference: "G'(0.1%) from Fig.2", deviation_percent: 0 }
        - { x: 10, y: 0.60, reference: "G'(10%) from Fig.2", deviation_percent: 0 }
      overall_quality: good
      note: "应力松弛研究，τ₁~50s快速松弛，τ₂~500s慢速松弛"
    metadata:
      point_count: 10
      x_range: [0.1, 15]
      y_range: [0.55, 1.80]
      avg_confidence: 0.66
---
# SSBR-045 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 拉伸性能

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 拉伸强度 | 14.2 MPa | Table 1 |
| 断裂伸长率 | 380% | Table 1 |
| 100%定伸应力 | 2.3 MPa | Table 1 |
| 300%定伸应力 | 10.5 MPa | Table 1 |

## 应力松弛特性

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 松弛时间 τ₁ | ~50 s | Fig. 4 |
| 松弛时间 τ₂ | ~500 s | Fig. 4 |
| 松弛幅度 (100% strain) | ~15% | Fig. 3 |

## Payne 效应

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| G'(0.1%) | ~1.8 MPa | Fig. 2 估读 |
| G'(10%) | ~0.6 MPa | Fig. 2 估读 |
| ΔG' | ~1.2 MPa | 计算值 |

## 性能分析

SSBR-045 是一种标准的白炭黑/SSBR 复合材料，文献重点研究了其应力松弛行为和填料网络动力学。

### 力学性能特点

1. **拉伸强度**: 14.2 MPa，典型白炭黑填充 SSBR 水平
2. **M300/M100 比值**: 4.6，显示较强的填料-橡胶相互作用
3. **断裂伸长率**: 380%，中等水平

### 应力松弛行为

文献系统研究了应力松弛特性：
- 存在快速松弛 (τ₁ ~50 s) 和慢速松弛 (τ₂ ~500 s) 两个过程
- 快速松弛与分子链重排相关
- 慢速松弛与填料网络重组相关

### 填料网络动力学

- Payne 效应表明存在显著的填料网络
- 应力松弛实验揭示了填料网络的可逆性
- 网络破坏-重建是一个动态平衡过程
