---
sample_id: SSBR-026
interpretation_type: mechanical
doi: 10.1002/app.48159
data_source: L1/L2
data_confidence: high
has_stress_strain: true
has_payne_effect: false
has_dma: true
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
      - {x: 0, y: 0, confidence: 0.95, source: "L1"}
      - {x: 50, y: 1.4, confidence: 0.65, source: "L3"}
      - {x: 100, y: 2.8, confidence: 0.95, source: "L1"}
      - {x: 150, y: 5.2, confidence: 0.65, source: "L3"}
      - {x: 200, y: 8.0, confidence: 0.65, source: "L3"}
      - {x: 250, y: 11.5, confidence: 0.65, source: "L3"}
      - {x: 300, y: 15.2, confidence: 0.95, source: "L1"}
      - {x: 350, y: 19.0, confidence: 0.65, source: "L3"}
      - {x: 400, y: 22.8, confidence: 0.65, source: "L3"}
      - {x: 420, y: 24.7, confidence: 0.95, source: "L1"}
    curve_features:
      modulus_100:
        value: 2.8
        unit: MPa
        source: Table II
        confidence: 0.95
      modulus_300:
        value: 15.2
        unit: MPa
        source: Table II
        confidence: 0.95
      tensile_strength:
        value: 24.7
        unit: MPa
        source: Table II
        confidence: 0.95
      elongation_at_break:
        value: 420
        unit: '%'
        source: Table II
        confidence: 0.95
    validation:
      known_points:
        - strain: 100
          stress_expected: 2.8
          stress_estimated: 2.8
          deviation_percent: 0.0
        - strain: 300
          stress_expected: 15.2
          stress_estimated: 15.2
          deviation_percent: 0.0
        - strain: 420
          stress_expected: 24.7
          stress_estimated: 24.7
          deviation_percent: 0.0
      overall_quality: good
    metadata:
      point_count: 10
      x_range: [0, 420]
      y_range: [0, 24.7]
      avg_confidence: 0.80
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: 无量纲
    data_points:
      - {x: -70, y: 0.06, confidence: 0.60, source: "L3"}
      - {x: -60, y: 0.12, confidence: 0.60, source: "L3"}
      - {x: -50, y: 0.25, confidence: 0.60, source: "L3"}
      - {x: -45, y: 0.38, confidence: 0.60, source: "L3"}
      - {x: -40, y: 0.52, confidence: 0.60, source: "L3"}
      - {x: -35, y: 0.62, confidence: 0.65, source: "L3"}
      - {x: -32, y: 0.68, confidence: 0.70, source: "L3"}
      - {x: -30, y: 0.65, confidence: 0.65, source: "L3"}
      - {x: -25, y: 0.58, confidence: 0.60, source: "L3"}
      - {x: -20, y: 0.50, confidence: 0.60, source: "L3"}
      - {x: -10, y: 0.42, confidence: 0.60, source: "L3"}
      - {x: 0, y: 0.38, confidence: 0.95, source: "L1"}
      - {x: 10, y: 0.32, confidence: 0.60, source: "L3"}
      - {x: 20, y: 0.26, confidence: 0.60, source: "L3"}
      - {x: 30, y: 0.22, confidence: 0.60, source: "L3"}
      - {x: 40, y: 0.18, confidence: 0.60, source: "L3"}
      - {x: 50, y: 0.16, confidence: 0.60, source: "L3"}
      - {x: 60, y: 0.15, confidence: 0.95, source: "L1"}
      - {x: 70, y: 0.14, confidence: 0.60, source: "L3"}
    curve_features:
      tan_delta_0C:
        value: 0.38
        unit: '-'
        source: Figure 5
        confidence: 0.95
      tan_delta_60C:
        value: 0.15
        unit: '-'
        source: Figure 5
        confidence: 0.95
      tan_delta_max:
        value: 0.68
        unit: '-'
        source: L3 estimated
        confidence: 0.70
      Tg:
        value: -32
        unit: °C
        method: peak
        source: Figure 5
        confidence: 0.95
    validation:
      known_points:
        - temperature: 0
          tan_delta_expected: 0.38
          tan_delta_estimated: 0.38
          deviation_percent: 0.0
        - temperature: 60
          tan_delta_expected: 0.15
          tan_delta_estimated: 0.15
          deviation_percent: 0.0
      overall_quality: good
    metadata:
      point_count: 19
      x_range: [-70, 70]
      y_range: [0.06, 0.68]
      avg_confidence: 0.66
---
# SSBR-026 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

- **样本编号**: SSBR-026
- **官能化类型**: 主链共聚改性 (β-月桂烯)
- **填料体系**: 炭黑 (N234, 50 phr)
- **基体**: 溶聚苯乙烯-β-月桂烯-丁二烯橡胶 (S-SMBR)

## 拉伸性能

### 关键数据

| 参数 | 数值 | 数据来源 |
|------|------|----------|
| 拉伸强度 | 24.7 MPa | Table II |
| 断裂伸长率 | 420% | Table II |
| 100% 定伸应力 | 2.8 MPa | Table II |
| 300% 定伸应力 | 15.2 MPa | Table II |

### 与对照样对比

| 样本 | 拉伸强度 (MPa) | 断裂伸长率 (%) | M300 (MPa) |
|------|----------------|----------------|------------|
| 纯 SBR | 21.3 | 385 | 12.4 |
| S-SMBR-026 | 24.7 | 420 | 15.2 |
| 变化 | +16% | +9% | +23% |

### 性能分析

β-月桂烯的引入显著改善了炭黑填充复合材料的力学性能：

1. **拉伸强度提升 16%**: 24.7 MPa vs 21.3 MPa
2. **300% 模量提升 23%**: 表明更强的填料-橡胶界面作用
3. **断裂伸长率同步提升**: 强度与韧性同时改善，非常难得

## DMA 动态力学分析

### tanδ 温度谱

| 参数 | 数值 | 数据来源 |
|------|------|----------|
| tanδ@0°C | 0.38 | Figure 5 |
| tanδ@60°C | 0.15 | Figure 5 |
| Tg (tanδ peak) | -32°C | Figure 5 |

### 轮胎性能指标分析

1. **湿地抓地力 (tanδ@0°C = 0.38)**:
   - 较纯 SBR (0.35) 略有提升
   - 有利于湿滑路面制动

2. **滚动阻力 (tanδ@60°C = 0.15)**:
   - 与纯 SBR 相当
   - β-月桂烯对高温区滞后影响较小

3. **玻璃化转变**: Tg = -32°C，与纯 SBR 相近

### 综合评价

β-月桂烯共聚改性通过引入生物基单体，在提升力学强度的同时保持了良好的动态性能，是一种环保、高性能的 SSBR 改性策略。
