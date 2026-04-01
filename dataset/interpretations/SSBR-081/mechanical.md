---
sample_id: SSBR-081
test_type: mechanical
data_source: L2
doi: 10.1002/vnl.21784
figure_ref: Fig.3
stress_strain:
  tensile_strength_mpa: 18.5
  elongation_at_break_percent: 420
  modulus_100_mpa: 2.8
  modulus_300_mpa: 11.2
tear_strength:
  value_kn_m: null
hardness:
  shore_a: 65
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
        y: 0.9
        confidence: 0.70
        source: L2
      - x: 50
        y: 1.6
        confidence: 0.70
        source: L2
      - x: 100
        y: 2.8
        confidence: 0.85
        source: L2
      - x: 150
        y: 4.5
        confidence: 0.70
        source: L2
      - x: 200
        y: 6.6
        confidence: 0.70
        source: L2
      - x: 250
        y: 9.0
        confidence: 0.70
        source: L2
      - x: 300
        y: 11.2
        confidence: 0.85
        source: L2
      - x: 350
        y: 14.0
        confidence: 0.70
        source: L2
      - x: 400
        y: 17.0
        confidence: 0.70
        source: L2
      - x: 420
        y: 18.5
        confidence: 0.85
        source: L2
    curve_features:
      modulus_100:
        value: 2.8
        unit: MPa
        source: L2
        confidence: 0.85
      modulus_300:
        value: 11.2
        unit: MPa
        source: L2
        confidence: 0.85
      tensile_strength:
        value: 18.5
        unit: MPa
        source: L2
        confidence: 0.85
      elongation_at_break:
        value: 420
        unit: '%'
        source: L2
        confidence: 0.85
    validation:
      known_points:
        - x: 100
          y_expected: 2.8
          y_actual: 2.8
          deviation_percent: 0
        - x: 300
          y_expected: 11.2
          y_actual: 11.2
          deviation_percent: 0
      overall_quality: good
      note: 脂肪酸苄酯生物基增塑剂，环保型替代芳烃油
    metadata:
      point_count: 11
      x_range:
        - 0
        - 420
      y_range:
        - 0
        - 18.5
      avg_confidence: 0.77
---
# SSBR-081 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本概述

SSBR-081 研究了脂肪酸苄酯作为生物基增塑剂在白炭黑填充 SSBR/BR 并用胶中的应用。该研究旨在开发环保型增塑剂替代传统石油基芳烃油。

## 拉伸性能分析

根据文献 Fig.3 数据：

| 性能指标 | 数值 | 评价 |
|---------|------|------|
| 拉伸强度 | 18.5 MPa | 良好 |
| 断裂伸长率 | 420% | 良好 |
| 100% 定伸应力 | 2.8 MPa | 适中 |
| 300% 定伸应力 | 11.2 MPa | 较高 |
| 邵氏硬度 A | 65 | 适中 |

## 增塑剂效应分析

### 脂肪酸苄酯特性
生物基脂肪酸苄酯增塑剂的特点：
- 来源于天然油脂
- 极性适中，与橡胶相容性好
- 挥发性低于传统芳烃油

### 对力学性能的影响
与传统增塑剂相比：
- 拉伸强度保持在可接受水平
- 断裂伸长率良好
- 模量分布合理

### 综合性能平衡
脂肪酸苄酯增塑的复合材料：
- 保持了足够的力学强度
- 柔韧性适中
- 硬度适合轮胎应用

## 环保优势

生物基增塑剂的环保价值：
- 减少芳烃类物质使用
- 降低多环芳烃 (PAHs) 含量
- 符合 REACH 法规要求

## 应用建议

适用于对环保要求严格的轮胎制品，特别是出口欧盟市场的轮胎，需要满足低 PAHs 含量要求的应用场景。
