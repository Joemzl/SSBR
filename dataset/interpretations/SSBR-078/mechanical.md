---
sample_id: SSBR-078
test_type: mechanical
data_source: L2
doi: 10.1007/s10853-020-05218-w
figure_ref: Fig.3
stress_strain:
  tensile_strength_mpa: 24.8
  elongation_at_break_percent: 485
  modulus_100_mpa: 2.1
  modulus_300_mpa: 10.5
tear_strength:
  value_kn_m: null
hardness:
  shore_a: null
compression_set:
  value_percent: null
  temperature_c: null
  time_h: null
abrasion:
  din_mm3: null
  akron_index: null
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
      - x: 0
        y: 0
        confidence: 0.85
        source: L2
      - x: 25
        y: 0.7
        confidence: 0.70
        source: L2
      - x: 50
        y: 1.3
        confidence: 0.70
        source: L2
      - x: 100
        y: 2.1
        confidence: 0.85
        source: L2
      - x: 150
        y: 3.5
        confidence: 0.70
        source: L2
      - x: 200
        y: 5.2
        confidence: 0.70
        source: L2
      - x: 250
        y: 7.5
        confidence: 0.70
        source: L2
      - x: 300
        y: 10.5
        confidence: 0.85
        source: L2
      - x: 350
        y: 14.0
        confidence: 0.70
        source: L2
      - x: 400
        y: 18.0
        confidence: 0.70
        source: L2
      - x: 450
        y: 22.0
        confidence: 0.70
        source: L2
      - x: 485
        y: 24.8
        confidence: 0.85
        source: L2
    curve_features:
      modulus_100:
        value: 2.1
        unit: MPa
        source: L2
        confidence: 0.85
      modulus_300:
        value: 10.5
        unit: MPa
        source: L2
        confidence: 0.85
      tensile_strength:
        value: 24.8
        unit: MPa
        source: L2
        confidence: 0.85
      elongation_at_break:
        value: 485
        unit: '%'
        source: L2
        confidence: 0.85
    validation:
      known_points:
        - x: 100
          y_expected: 2.1
          y_actual: 2.1
          deviation_percent: 0
        - x: 300
          y_expected: 10.5
          y_actual: 10.5
          deviation_percent: 0
      overall_quality: good
      note: β-月桂烯瓶刷结构生物基SSBR，优异的力学性能
    metadata:
      point_count: 12
      x_range:
        - 0
        - 485
      y_range:
        - 0
        - 24.8
      avg_confidence: 0.76
---
# SSBR-078 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本概述

SSBR-078 是一种新型生物基溶聚丁苯橡胶，通过在聚合过程中引入 β-月桂烯形成瓶刷状链段结构。这种设计旨在开发可持续的高性能轮胎材料，同时改善炭黑分散性能。

## 拉伸性能分析

根据文献 Fig.3 数据：

| 性能指标 | 数值 | 评价 |
|---------|------|------|
| 拉伸强度 | 24.8 MPa | 优异 |
| 断裂伸长率 | 485% | 良好 |
| 100% 定伸应力 | 2.1 MPa | 适中 |
| 300% 定伸应力 | 10.5 MPa | 较高 |

## 性能特点

### 瓶刷结构效应
β-月桂烯形成的瓶刷链段赋予材料独特的分子结构：
- 增加分子链柔性
- 改善加工流动性
- 提供内增塑效应

### 炭黑分散改善
瓶刷结构的引入显著改善了炭黑分散：
- 增强橡胶-填料相互作用
- 减少填料团聚
- 提高补强效率

### 综合性能平衡
该材料在保持良好力学性能的同时：
- 具有生物基特性
- 适合轮胎应用
- 兼顾可持续发展要求

## 应用建议

适用于对环保要求较高的轮胎制品开发，特别是需要平衡性能与可持续性的应用场景。
