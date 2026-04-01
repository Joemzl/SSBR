---
sample_id: SSBR-026
interpretation_type: dsc
doi: 10.1002/app.48159
data_source: L1
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
      - {x: -80, y: -0.52, confidence: 0.60, source: "L3"}
      - {x: -75, y: -0.50, confidence: 0.60, source: "L3"}
      - {x: -70, y: -0.48, confidence: 0.60, source: "L3"}
      - {x: -65, y: -0.42, confidence: 0.60, source: "L3"}
      - {x: -63, y: -0.35, confidence: 0.65, source: "L3"}
      - {x: -61, y: -0.28, confidence: 0.70, source: "L3"}
      - {x: -59, y: -0.22, confidence: 0.65, source: "L3"}
      - {x: -55, y: -0.18, confidence: 0.60, source: "L3"}
      - {x: -50, y: -0.16, confidence: 0.60, source: "L3"}
      - {x: -40, y: -0.14, confidence: 0.60, source: "L3"}
      - {x: -20, y: -0.12, confidence: 0.60, source: "L3"}
      - {x: 0, y: -0.11, confidence: 0.60, source: "L3"}
    curve_features:
      Tg:
        onset: -65
        midpoint: -61
        endpoint: -57
        unit: °C
        source: Table I
      glass_transition_width:
        value: 8
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - temperature: -61
          parameter: Tg_midpoint
          expected: -61
          estimated: -61
          deviation_percent: 0.0
      overall_quality: good
    metadata:
      point_count: 12
      x_range: [-80, 0]
      y_range: [-0.52, -0.11]
      avg_confidence: 0.62
---
# SSBR-026 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

- **样本编号**: SSBR-026
- **官能化类型**: β-月桂烯共聚
- **测试方法**: DSC

## 玻璃化转变

### 关键数据

| 参数 | 数值 | 数据来源 |
|------|------|----------|
| Tg | -61°C | Table I |
| ΔTg | - | 未报道 |

### 数据解读

S-SMBR-026 的 Tg 为 -61°C，较标准 SBR (Tg ≈ -55°C) 略低，原因分析：

1. **β-月桂烯的柔性贡献**: β-月桂烯单元引入了较长的侧链，增加了链段柔性
2. **苯乙烯含量**: 苯乙烯含量为 27 wt%，适中的刚性贡献
3. **微观结构平衡**: 乙烯基含量 50% 保持了良好的低温性能

### 与填充后 DMA Tg 对比

- DSC 测得 Tg: -61°C (纯聚合物)
- DMA 测得 Tg: -32°C (填充复合材料)

ΔTg ≈ 29°C 的差异主要来自炭黑填料对链段运动的约束作用。
