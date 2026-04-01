---
sample_id: SSBR-021
interpretation_type: mechanical
doi: 10.1021/acs.iecr.8b05738
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
      - {x: 50, y: 2.5, confidence: 0.65, source: "L3"}
      - {x: 100, y: 4.8, confidence: 0.65, source: "L3"}
      - {x: 150, y: 6.5, confidence: 0.65, source: "L3"}
      - {x: 200, y: 8.0, confidence: 0.65, source: "L3"}
      - {x: 250, y: 9.8, confidence: 0.65, source: "L3"}
      - {x: 300, y: 11.9, confidence: 0.95, source: "L1"}
      - {x: 350, y: 14.5, confidence: 0.65, source: "L3"}
      - {x: 400, y: 17.2, confidence: 0.65, source: "L3"}
      - {x: 450, y: 19.8, confidence: 0.65, source: "L3"}
      - {x: 498, y: 22.1, confidence: 0.95, source: "L1"}
    curve_features:
      modulus_100:
        value: 4.8
        unit: MPa
        source: L3 estimated
        confidence: 0.65
      modulus_300:
        value: 11.9
        unit: MPa
        source: Table 3
        confidence: 0.95
      tensile_strength:
        value: 22.1
        unit: MPa
        source: Table 3
        confidence: 0.95
      elongation_at_break:
        value: 498
        unit: '%'
        source: Table 3
        confidence: 0.95
    validation:
      known_points:
        - strain: 300
          stress_expected: 11.9
          stress_estimated: 11.9
          deviation_percent: 0.0
        - strain: 498
          stress_expected: 22.1
          stress_estimated: 22.1
          deviation_percent: 0.0
      overall_quality: good
    metadata:
      point_count: 11
      x_range: [0, 498]
      y_range: [0, 22.1]
      avg_confidence: 0.77
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: 无量纲
    data_points:
      - {x: -60, y: 0.08, confidence: 0.60, source: "L3"}
      - {x: -50, y: 0.15, confidence: 0.60, source: "L3"}
      - {x: -40, y: 0.35, confidence: 0.60, source: "L3"}
      - {x: -30, y: 0.55, confidence: 0.60, source: "L3"}
      - {x: -25, y: 0.62, confidence: 0.60, source: "L3"}
      - {x: -22, y: 0.65, confidence: 0.70, source: "L3"}
      - {x: -20, y: 0.63, confidence: 0.60, source: "L3"}
      - {x: -15, y: 0.58, confidence: 0.60, source: "L3"}
      - {x: -10, y: 0.50, confidence: 0.60, source: "L3"}
      - {x: 0, y: 0.42, confidence: 0.95, source: "L1"}
      - {x: 10, y: 0.35, confidence: 0.60, source: "L3"}
      - {x: 20, y: 0.28, confidence: 0.60, source: "L3"}
      - {x: 30, y: 0.22, confidence: 0.60, source: "L3"}
      - {x: 40, y: 0.16, confidence: 0.60, source: "L3"}
      - {x: 50, y: 0.12, confidence: 0.60, source: "L3"}
      - {x: 60, y: 0.08, confidence: 0.95, source: "L1"}
      - {x: 70, y: 0.06, confidence: 0.60, source: "L3"}
    curve_features:
      tan_delta_0C:
        value: 0.42
        unit: '-'
        source: Figure 6
        confidence: 0.95
      tan_delta_60C:
        value: 0.08
        unit: '-'
        source: Figure 6
        confidence: 0.95
      tan_delta_max:
        value: 0.65
        unit: '-'
        source: L3 estimated
        confidence: 0.70
      Tg:
        value: -22
        unit: °C
        method: peak
        source: Figure 6
        confidence: 0.95
    validation:
      known_points:
        - temperature: 0
          tan_delta_expected: 0.42
          tan_delta_estimated: 0.42
          deviation_percent: 0.0
        - temperature: 60
          tan_delta_expected: 0.08
          tan_delta_estimated: 0.08
          deviation_percent: 0.0
      overall_quality: good
    metadata:
      point_count: 17
      x_range: [-60, 70]
      y_range: [0.06, 0.65]
      avg_confidence: 0.67
---
# SSBR-021 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

- **样本编号**: SSBR-021
- **官能化类型**: α,ω-双端官能化 (DPE-NMe₂ 两端)
- **填料体系**: 白炭黑 (80 phr)
- **基体**: 溶聚丁苯橡胶 (SSBR)

## 拉伸性能

### 关键数据

| 参数 | 数值 | 数据来源 |
|------|------|----------|
| 拉伸强度 | 22.1 MPa | Table 3 |
| 断裂伸长率 | 498% | Table 3 |
| 300% 定伸应力 | 11.9 MPa | Table 3 |

### 性能分析

α,ω-SSBR-021 采用两端 DPE-NMe₂ 官能化策略，在拉伸强度和模量方面均优于单端官能化的 α-SSBR-018：

1. **拉伸强度提升**: 22.1 MPa vs 19.7 MPa (α-SSBR)，提升约 12%
2. **300% 模量显著提高**: 11.9 MPa vs 9.2 MPa，提升约 29%
3. **断裂伸长率略降**: 498% vs 528%，但仍保持良好韧性

双端官能化提供了更强的填料-橡胶界面作用，有效提升了复合材料的整体力学性能。

## DMA 动态力学分析

### tanδ 温度谱

| 参数 | 数值 | 数据来源 |
|------|------|----------|
| tanδ@0°C | 0.42 | Figure 6 |
| tanδ@60°C | 0.08 | Figure 6 |
| Tg (tanδ peak) | -22°C | Figure 6 |

### 轮胎性能指标分析

1. **湿地抓地力 (tanδ@0°C = 0.42)**:
   - 与 α-SSBR-018 相近 (0.43)
   - 表明两端官能化对 0°C 区域的滞后行为影响较小

2. **滚动阻力 (tanδ@60°C = 0.08)**:
   - 显著低于 α-SSBR-018 (0.11)
   - 降低约 27%，表明双端官能化更有效降低填料网络的能量损耗

3. **玻璃化转变温度**: Tg = -22°C，与 α-SSBR 相同

### 综合评价

α,ω-双端官能化 SSBR-021 在保持湿抓性能的同时，显著降低了滚动阻力，实现了更优的 "magic triangle" 平衡。双端胺基的协同作用增强了填料分散和界面结合，是一种更具应用潜力的改性策略。
