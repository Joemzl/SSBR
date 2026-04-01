---
sample_id: SSBR-061
test_type: dsc
data_source: L3
doi: 10.1016/j.polymertesting.2020.106431
glass_transition:
  tg_celsius: -25
  tg_method: estimated
keywords:
- 玻璃化转变
- SSBR
- 端基官能化
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
      - { x: -60, y: -0.36, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: -50, y: -0.36, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: -40, y: -0.37, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: -35, y: -0.40, confidence: 0.60, source: "L3 Tg onset估计" }
      - { x: -30, y: -0.47, confidence: 0.60, source: "L3 Tg区间估计" }
      - { x: -25, y: -0.52, confidence: 0.65, source: "L3 Tg midpoint基于25wt%苯乙烯" }
      - { x: -20, y: -0.47, confidence: 0.60, source: "L3 Tg区间估计" }
      - { x: -15, y: -0.42, confidence: 0.60, source: "L3 Tg endpoint估计" }
      - { x: -5, y: -0.38, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: 10, y: -0.38, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: 30, y: -0.38, confidence: 0.55, source: "L3 典型曲线估计" }
    curve_features:
      Tg:
        onset: -35
        midpoint: -25
        endpoint: -15
        unit: °C
        source: L3 基于25wt%苯乙烯估计
      glass_transition_width:
        value: 20
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - { x: -25, y: null, reference: "Tg ~-25°C 基于苯乙烯含量估计", deviation_percent: 0 }
      overall_quality: acceptable
    metadata:
      point_count: 11
      x_range: [-60, 30]
      y_range: [-0.52, -0.36]
      avg_confidence: 0.58
---
# SSBR-061 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本背景

SSBR-061 采用 APTES 端基官能化，苯乙烯含量为 25 wt%。文献主要关注耐磨性能，热学数据有限。

## 玻璃化转变温度

### 数据来源
- **来源层级**: L3 (基于苯乙烯含量估算)
- **Tg**: 约 -25°C

### 估算依据

基于 25 wt% 苯乙烯含量，Tg 估算约为 -25°C，这是典型的 SSBR 玻璃化转变温度范围。

## 热学性能讨论

### APTES 官能化对 Tg 的影响

端基官能化对 Tg 的影响通常较小：

1. **端基效应有限**: 仅链端官能化，对主链运动能力影响不大
2. **填料相互作用**: 与白炭黑的相互作用可能略微限制链段运动
3. **整体 Tg 变化**: 预计变化在 ±2°C 范围内

## 数据限制说明

文献未提供详细的 DSC 测试数据，热学分析主要基于材料组成估算。如需精确数据，建议查阅补充信息或相关文献。
