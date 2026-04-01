---
sample_id: SSBR-062
test_type: dsc
data_completeness:
  tg: true
  crystallization: false
  melting: false
data_source: L2
key_findings:
- 环氧化度增加导致 Tg 升高
- 分子链极性增强，内旋转位阻增大
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
    note: "E25-SSBR (25%环氧化度) 样品，环氧化使Tg升高"
    data_points:
      - { x: -60, y: -0.35, confidence: 0.70, source: "L2 Fig.3c 估读" }
      - { x: -50, y: -0.35, confidence: 0.70, source: "L2 Fig.3c 估读" }
      - { x: -40, y: -0.36, confidence: 0.70, source: "L2 Fig.3c 估读" }
      - { x: -30, y: -0.38, confidence: 0.70, source: "L2 Fig.3c 估读" }
      - { x: -22, y: -0.42, confidence: 0.75, source: "L2 Fig.3c Tg onset" }
      - { x: -15, y: -0.52, confidence: 0.80, source: "L2 Fig.3c Tg区间 (环氧化升高)" }
      - { x: -8, y: -0.48, confidence: 0.75, source: "L2 Fig.3c Tg区间" }
      - { x: 0, y: -0.42, confidence: 0.75, source: "L2 Fig.3c Tg endpoint" }
      - { x: 10, y: -0.38, confidence: 0.70, source: "L2 Fig.3c 估读" }
      - { x: 30, y: -0.38, confidence: 0.70, source: "L2 Fig.3c 估读" }
      - { x: 50, y: -0.38, confidence: 0.70, source: "L2 Fig.3c 估读" }
    curve_features:
      Tg:
        onset: -22
        midpoint: -15
        endpoint: 0
        unit: °C
        source: L2 Fig.3c E25-SSBR (比未改性高约15°C)
      glass_transition_width:
        value: 22
        unit: °C
      Tg_shift_vs_unmodified:
        description: 环氧化25%使Tg升高约15°C
        source: Fig.3c对比
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - { x: -15, y: -0.52, reference: "Tg升高，环氧化效应", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 11
      x_range: [-60, 50]
      y_range: [-0.52, -0.35]
      avg_confidence: 0.72
---
# SSBR-062 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本概述

SSBR-062 为使用甲酸/H₂O₂体系原位生成过氧甲酸进行环氧化的 SSBR 样本。DSC 分析用于表征环氧化对玻璃化转变温度的影响。

## 玻璃化转变温度

### Tg 随环氧化度变化

文献 Figure 3c 显示了 SSBR 及不同环氧化度 ESSBR 的 DSC 曲线：

| 样品 | 环氧化度 (%) | Tg 变化趋势 |
|------|--------------|-------------|
| SSBR2557 | 0 | 基准 |
| ESSBR7% | 7 | 略有升高 |
| ESSBR10% | 10 | 升高 |
| ESSBR15% | 15 | 明显升高 |
| ESSBR20% | 20 | 显著升高 |
| ESSBR25% | 25 | 最高 |

### Tg 升高机理

1. **极性增强**: 环氧基团引入增加了分子链极性
2. **位阻效应**: 环氧基的三元环结构增加内旋转位阻
3. **链刚性**: 分子链活动能力下降，需要更高温度才能发生玻璃化转变

## 热性能与轮胎性能关联

Tg 升高对轮胎性能的影响：

| 性能指标 | Tg 升高效果 | 机理 |
|----------|-------------|------|
| 湿地抓地力 | 提高 | tanδ@0°C 增加 |
| 滚动阻力 | 需综合考虑 | 与填料分散共同决定 |
| 耐磨性 | 改善 | 模量增加 |

## 复合材料热性能

在白炭黑填充体系中，ESSBR 的热性能受以下因素影响：

1. **界面相互作用**: 环氧基与白炭黑硅羟基反应形成化学键
2. **受限链段**: 界面附近橡胶链段运动受限，有效 Tg 升高
3. **结合胶含量**: 环氧化度越高，结合胶越多

## 数据来源

- 文献: Polymers 2020, 12, 1257
- DOI: 10.3390/polym12061257
- 数据层级: L2 (图面估读)
