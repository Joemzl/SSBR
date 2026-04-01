---
sample_id: SSBR-021
interpretation_type: dsc
doi: 10.1021/acs.iecr.8b05738
data_source: L1/L2
data_confidence: high
has_tg: true
has_crystallization: false
has_melting: false
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
      - {x: -70, y: -0.45, confidence: 0.60, source: "L3"}
      - {x: -60, y: -0.44, confidence: 0.60, source: "L3"}
      - {x: -55, y: -0.42, confidence: 0.60, source: "L3"}
      - {x: -50, y: -0.38, confidence: 0.60, source: "L3"}
      - {x: -48, y: -0.32, confidence: 0.65, source: "L3"}
      - {x: -46, y: -0.25, confidence: 0.70, source: "L3"}
      - {x: -44, y: -0.18, confidence: 0.65, source: "L3"}
      - {x: -42, y: -0.14, confidence: 0.60, source: "L3"}
      - {x: -38, y: -0.12, confidence: 0.60, source: "L3"}
      - {x: -30, y: -0.11, confidence: 0.60, source: "L3"}
      - {x: -20, y: -0.10, confidence: 0.60, source: "L3"}
      - {x: 0, y: -0.09, confidence: 0.60, source: "L3"}
    curve_features:
      Tg:
        onset: -50
        midpoint: -46
        endpoint: -42
        unit: °C
        source: Table 2
      glass_transition_width:
        value: 8
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - temperature: -46
          parameter: Tg_midpoint
          expected: -46
          estimated: -46
          deviation_percent: 0.0
      overall_quality: good
    metadata:
      point_count: 12
      x_range: [-70, 0]
      y_range: [-0.45, -0.09]
      avg_confidence: 0.62
---
# SSBR-021 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

- **样本编号**: SSBR-021
- **官能化类型**: α,ω-双端官能化 (DPE-NMe₂)
- **测试方法**: DSC

## 玻璃化转变

### 关键数据

| 参数 | 数值 | 数据来源 |
|------|------|----------|
| Tg | -46°C | Table 2 |
| ΔTg | - | 未报道 |

### 数据解读

α,ω-SSBR-021 的 Tg 为 -46°C，与 α-SSBR-018 的 Tg (-47°C) 基本相同。这表明：

1. **链端官能化对 Tg 影响有限**: 无论单端还是双端官能化，主链微观结构保持一致
2. **胺基基团的影响局限于链端**: DPE-NMe₂ 基团仅在链末端引入，不改变主链的分子链段运动

### 与填充后 DMA Tg 对比

- DSC 测得 Tg: -46°C (纯聚合物)
- DMA 测得 Tg: -22°C (填充复合材料)

ΔTg ≈ 24°C 的差异反映了白炭黑填料对橡胶链段运动的约束效应。
