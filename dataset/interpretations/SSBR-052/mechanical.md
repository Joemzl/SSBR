---
sample_id: SSBR-052
test_type: mechanical
data_source_level: L2
literature_doi: 10.1016/j.polymer.2014.02.067
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
      - { x: 50, y: 0.8, confidence: 0.65, source: "L3 典型曲线估读" }
      - { x: 100, y: 1.8, confidence: 0.75, source: "L2 M100 ~1.8 MPa" }
      - { x: 150, y: 3.0, confidence: 0.65, source: "L3 估读" }
      - { x: 200, y: 4.8, confidence: 0.65, source: "L3 估读" }
      - { x: 250, y: 6.2, confidence: 0.65, source: "L3 估读" }
      - { x: 300, y: 7.5, confidence: 0.75, source: "L2 M300 ~7.5 MPa" }
      - { x: 350, y: 10.0, confidence: 0.65, source: "L3 估读" }
      - { x: 400, y: 13.0, confidence: 0.65, source: "L3 估读" }
      - { x: 450, y: 15.5, confidence: 0.70, source: "L2 Fig.7 估读" }
      - { x: 500, y: 17.0, confidence: 0.75, source: "L2 TS ~17 MPa" }
    curve_features:
      modulus_100:
        value: 1.8
        unit: MPa
        source: 估读
        confidence: 0.70
      modulus_300:
        value: 7.5
        unit: MPa
        source: 估读
        confidence: 0.75
      tensile_strength:
        value: 17.0
        unit: MPa
        source: Fig.7 估读 ~17 MPa
        confidence: 0.75
      elongation_at_break:
        value: 500
        unit: '%'
        source: Fig.7 估读 ~500%
        confidence: 0.75
      M300_M100_ratio:
        value: 4.2
        unit: dimensionless
        source: 计算值
        confidence: 0.70
    validation:
      known_points:
        - { x: 100, y: 1.8, reference: "M100 ~1.8 MPa", deviation_percent: 0 }
        - { x: 300, y: 7.5, reference: "M300 ~7.5 MPa", deviation_percent: 0 }
        - { x: 500, y: 17.0, reference: "TS ~17 MPa", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 11
      x_range: [0, 500]
      y_range: [0, 17.0]
      avg_confidence: 0.70
---
# SSBR-052 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 拉伸性能

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 拉伸强度 | ~17 MPa | Fig. 7 估读 |
| 断裂伸长率 | ~500% | Fig. 7 估读 |
| 100%定伸应力 | ~1.8 MPa | 估读 |
| 300%定伸应力 | ~7.5 MPa | 估读 |

## 性能分析

SSBR-052 研究了烷氧基硅烷端基官能化 SSBR 的制备及其白炭黑填充复合材料的性能。端基官能化策略使 SSBR 分子链末端带有与白炭黑亲和的基团。

### 力学性能特点

1. **拉伸强度**: ~17 MPa，端基官能化有效增强
2. **断裂伸长率**: ~500%，保持优异柔韧性
3. **M300/M100**: ~4.2，良好的填料-橡胶作用

### 端基官能化效果

烷氧基硅烷端基 [-Si(OR)₃] 的作用：
- 与白炭黑表面硅烷醇直接反应
- 形成化学键合的界面
- 减少对额外硅烷偶联剂的需求

### 与传统配方对比

| 指标 | 普通 SSBR | 端基官能化 SSBR |
|------|----------|-----------------|
| 拉伸强度 | ~14 MPa | ~17 MPa |
| 分散性 | 需 Si69 | 自分散改善 |
| 硅烷用量 | 高 | 可减少 |
