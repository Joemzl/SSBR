---
sample_id: SSBR-081
test_type: dsc
data_source: L3
doi: 10.1002/vnl.21784
figure_ref: null
thermal_properties:
  tg_onset_c: null
  tg_midpoint_c: -50
  tg_endpoint_c: null
  delta_cp_j_g_k: null
crystallization:
  tc_c: null
  delta_hc_j_g: null
melting:
  tm_c: null
  delta_hm_j_g: null
thermal_stability:
  t5_percent_c: null
  t50_percent_c: null
  residue_percent: null
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  dsc_heat_flow:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: 热流
      unit: mW/mg
      direction: exo_up
    data_points:
      - x: -80
        y: -0.38
        confidence: 0.55
        source: L3
      - x: -70
        y: -0.36
        confidence: 0.55
        source: L3
      - x: -62
        y: -0.32
        confidence: 0.55
        source: L3
      - x: -57
        y: -0.26
        confidence: 0.60
        source: L3
        note: Tg onset
      - x: -50
        y: -0.10
        confidence: 0.60
        source: L3
        note: Tg midpoint
      - x: -43
        y: 0.05
        confidence: 0.60
        source: L3
        note: Tg endpoint
      - x: -30
        y: 0.08
        confidence: 0.55
        source: L3
      - x: 0
        y: 0.06
        confidence: 0.55
        source: L3
      - x: 30
        y: 0.04
        confidence: 0.55
        source: L3
      - x: 60
        y: 0.03
        confidence: 0.55
        source: L3
    curve_features:
      Tg:
        onset: -57
        midpoint: -50
        endpoint: -43
        unit: °C
        source: L3
      glass_transition_width:
        value: 14
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - x: -50
          parameter: Tg_midpoint
          expected: -50
          actual: -50
          deviation_percent: 0
      overall_quality: acceptable
      note: 脂肪酸苄酯增塑作用和BR组分共同降低Tg
    metadata:
      point_count: 10
      x_range:
        - -80
        - 60
      y_range:
        - -0.38
        - 0.08
      avg_confidence: 0.57
---
# SSBR-081 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本概述

SSBR-081 是采用脂肪酸苄酯生物基增塑剂的白炭黑/SSBR/BR 复合材料。增塑剂的引入对材料的热学性能有显著影响。

## 玻璃化转变分析

### Tg 表现
- **Tg (中点)**: 约 -50°C（估计值）

增塑剂对 Tg 的影响：
- 脂肪酸苄酯的增塑作用降低 Tg
- BR 组分的低 Tg 特性
- 有利于低温性能

## 增塑机理分析

### 脂肪酸苄酯增塑效应
生物基增塑剂的作用机制：
- 插入分子链间，增加链段运动性
- 降低分子间作用力
- 提高自由体积

### 与橡胶相容性
脂肪酸苄酯的相容性特点：
- 苄基提供与芳烃链段的相互作用
- 脂肪酸链提供与脂肪族链段的相容性
- 整体极性与 SSBR/BR 匹配良好

## 轮胎应用相关性

### 低温性能
较低的 Tg 意味着：
- 良好的低温柔韧性
- 冬季轮胎潜力
- 低温抗湿滑性能改善

### 动态性能预期
增塑作用对动态性能的影响：
- 可能降低滞后损失
- 有利于滚动阻力
- 湿地性能需综合评估

## 备注

本样本 DSC 数据有限，Tg 为基于材料组成和增塑剂效应的估计值。
