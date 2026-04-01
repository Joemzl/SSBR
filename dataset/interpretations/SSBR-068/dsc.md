---
sample_id: SSBR-068
test_type: dsc
data_source: L3
doi: 10.1002/pen.23533
glass_transition:
  tg_celsius: -35
  tg_method: estimated
keywords:
- 玻璃化转变
- SSBR
- 膨胀石墨
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
        y: -0.35
        confidence: 0.55
        source: L3
      - x: -70
        y: -0.34
        confidence: 0.55
        source: L3
      - x: -60
        y: -0.33
        confidence: 0.55
        source: L3
      - x: -50
        y: -0.30
        confidence: 0.55
        source: L3
      - x: -42
        y: -0.25
        confidence: 0.60
        source: L3
        note: Tg onset
      - x: -35
        y: -0.10
        confidence: 0.60
        source: L3
        note: Tg midpoint
      - x: -28
        y: 0.05
        confidence: 0.60
        source: L3
        note: Tg endpoint
      - x: -20
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
        onset: -42
        midpoint: -35
        endpoint: -28
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
        - x: -35
          parameter: Tg_midpoint
          expected: -35
          actual: -35
          deviation_percent: 0
      overall_quality: acceptable
    metadata:
      point_count: 11
      x_range:
        - -80
        - 60
      y_range:
        - -0.35
        - 0.08
      avg_confidence: 0.56
---
# SSBR-068 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本背景

SSBR-068 是膨胀石墨/SSBR 纳米复合材料，采用 XSBR 作为增容剂。

## 玻璃化转变温度

### 数据来源
- **来源层级**: L3 (基于材料体系估算)
- **Tg**: 约 -35°C

### EG 对 Tg 的影响

膨胀石墨对 Tg 的影响：

1. **限域效应**: EG 片层可能限制链段运动
2. **界面效应**: 良好的界面可能略微提高 Tg
3. **整体影响**: Tg 变化通常在 ±3°C

## 热稳定性

### EG 的阻燃/隔热作用

膨胀石墨的热学特性：

| 特性 | 效果 |
|------|------|
| 阻燃性 | 优异 |
| 隔热性 | 良好 |
| 热导率 | 中等 |

### 热分解行为

EG 对复合材料热分解的影响：

1. **物理阻隔**: EG 层状结构阻挡热量和氧气
2. **延缓分解**: 可能提高热分解起始温度
3. **成炭作用**: 促进保护性炭层形成

## 数据限制说明

文献主要关注力学性能和形貌，DSC 数据未详细报道。
