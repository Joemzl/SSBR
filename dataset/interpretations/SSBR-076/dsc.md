---
sample_id: SSBR-076
test_type: dsc
data_completeness:
  tg: true
  crystallization: false
  melting: false
data_source: L2
key_findings:
- m-CPBA 环氧化导致 Tg 升高
- 环氧基引入增加分子链极性
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
        confidence: 0.70
        source: L2
      - x: -65
        y: -0.33
        confidence: 0.70
        source: L2
      - x: -50
        y: -0.30
        confidence: 0.70
        source: L2
      - x: -40
        y: -0.25
        confidence: 0.75
        source: L2
        note: Tg onset
      - x: -32
        y: -0.10
        confidence: 0.75
        source: L2
        note: Tg midpoint
      - x: -24
        y: 0.05
        confidence: 0.75
        source: L2
        note: Tg endpoint
      - x: -10
        y: 0.08
        confidence: 0.70
        source: L2
      - x: 10
        y: 0.06
        confidence: 0.70
        source: L2
      - x: 40
        y: 0.04
        confidence: 0.70
        source: L2
      - x: 70
        y: 0.03
        confidence: 0.70
        source: L2
    curve_features:
      Tg:
        onset: -40
        midpoint: -32
        endpoint: -24
        unit: °C
        source: L2
      glass_transition_width:
        value: 16
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - x: -32
          parameter: Tg_midpoint
          note: 环氧化导致Tg升高
      overall_quality: good
      note: m-CPBA环氧化与甲酸/H2O2体系具有相同的环氧化效果
    metadata:
      point_count: 10
      x_range:
        - -80
        - 70
      y_range:
        - -0.35
        - 0.08
      avg_confidence: 0.72
---
# SSBR-076 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本概述

SSBR-076 为使用间氯过氧苯甲酸 (m-CPBA) 进行环氧化的 SSBR 样本。

## 玻璃化转变温度

### Tg 变化机理

m-CPBA 环氧化与甲酸/H₂O₂体系具有相同的环氧化效果：

1. **极性增强**: 环氧基团引入增加分子链极性
2. **位阻效应**: 三元环氧结构增加内旋转位阻
3. **链刚性增加**: 分子链活动能力下降

### 预期 Tg 变化

| 环氧化度 | Tg 变化 |
|----------|---------|
| 0% (未改性) | 基准 |
| 7% | 略升高 |
| 15% | 明显升高 |
| 25% | 显著升高 |

## 热性能与轮胎性能

Tg 升高对轮胎性能的积极影响：
- tanδ@0°C 增加 → 湿地抓地力提升
- 配合填料分散改善 → 滚动阻力可控

## 数据来源

- 文献: Polymers 2020, 12, 1257
- DOI: 10.3390/polym12061257
