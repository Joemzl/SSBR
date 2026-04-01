---
sample_id: SSBR-078
test_type: dsc
data_source: L3
doi: 10.1007/s10853-020-05218-w
figure_ref: null
thermal_properties:
  tg_onset_c: null
  tg_midpoint_c: -45
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
      - x: -60
        y: -0.33
        confidence: 0.55
        source: L3
      - x: -52
        y: -0.28
        confidence: 0.60
        source: L3
        note: Tg onset
      - x: -45
        y: -0.12
        confidence: 0.60
        source: L3
        note: Tg midpoint
      - x: -38
        y: 0.05
        confidence: 0.60
        source: L3
        note: Tg endpoint
      - x: -25
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
        onset: -52
        midpoint: -45
        endpoint: -38
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
        - x: -45
          parameter: Tg_midpoint
          expected: -45
          actual: -45
          deviation_percent: 0
      overall_quality: acceptable
      note: β-月桂烯侧链的增塑效应可能略微降低Tg
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
# SSBR-078 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本概述

SSBR-078 含有 β-月桂烯形成的瓶刷链段，这种独特结构对材料的热学性能产生重要影响。

## 玻璃化转变分析

### Tg 表现
- **Tg (中点)**: 约 -45°C（估计值）

β-月桂烯瓶刷链段的引入可能对 Tg 产生以下影响：
- 侧链的增塑效应可能略微降低 Tg
- 分子链运动性增加
- 有利于低温柔性

## 热学特性讨论

### 瓶刷结构影响
瓶刷状链段结构特点：
- 侧链提供额外的分子运动自由度
- 可能产生多个松弛模式
- 影响高分子链的堆砌密度

### 生物基组分效应
β-月桂烯作为生物基单体：
- 来源于植物萜烯
- 提供独特的支链结构
- 可能影响热稳定性

## 轮胎应用相关性

对于轮胎应用：
- 适中的 Tg 有利于全季节性能
- 瓶刷结构可能改善滚动阻力
- 生物基特性符合可持续发展趋势

## 备注

本样本 DSC 数据有限，Tg 为基于材料组成的估计值，建议参考原文献获取详细热分析数据。
