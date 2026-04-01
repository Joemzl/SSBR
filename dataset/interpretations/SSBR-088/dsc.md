---
sample_id: SSBR-088
interpretation_type: dsc
source_figure: Fig.12
source_doi: 10.1016/j.polymer.2023.126082
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-19
updated_at: '2026-03-31'
data:
  tg:
    value: null
    range: null
    unit: ℃
    source: Fig.12 DSC 曲线
  thermal_source: Fig.12
skill_version: '2.0'
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
        source: L3
      - x: -70
        y: -0.34
        confidence: 0.70
        source: L3
      - x: -60
        y: -0.33
        confidence: 0.70
        source: L3
      - x: -50
        y: -0.32
        confidence: 0.70
        source: L3
      - x: -40
        y: -0.30
        confidence: 0.70
        source: L3
      - x: -35
        y: -0.28
        confidence: 0.75
        source: L3
      - x: -30
        y: -0.22
        confidence: 0.75
        source: L3
      - x: -25
        y: -0.15
        confidence: 0.75
        source: L3
      - x: -20
        y: -0.12
        confidence: 0.70
        source: L3
      - x: -10
        y: -0.10
        confidence: 0.70
        source: L3
      - x: 0
        y: -0.09
        confidence: 0.70
        source: L3
      - x: 20
        y: -0.08
        confidence: 0.65
        source: L3
    curve_features:
      Tg:
        onset: -35
        midpoint: -28
        endpoint: -22
        unit: °C
        source: L3 estimated from Fig.12
      glass_transition_width:
        value: 13
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: acceptable
    metadata:
      point_count: 12
      x_range:
        - -80
        - 20
      y_range:
        - -0.35
        - -0.08
      avg_confidence: 0.70
---
# DSC 热分析解读：SSBR-088

> **样本性质**: 环氧化 SSBR (ESSBR)，8% 环氧化程度


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-088
- **样品名称**: 环氧化 SSBR/EBR 纳米复合材料
- **环氧化程度**: 8%
- **文献DOI**: 10.1016/j.polymer.2023.126082

## 二、玻璃化转变

### 数据来源

文献 Fig.12 提供了 DSC 曲线。

### 核心发现

1. **Tg 变化**: 环氧化改性会影响 Tg
2. **极性增加**: 环氧基团的引入增加了链的极性，可能导致 Tg 略有上升
3. **共混效应**: ESSBR/EBR 共混体系可能显示单一或双 Tg

### 预期趋势

| 样品 | 预期 Tg 范围 | 说明 |
|------|-------------|------|
| 未环氧化 SSBR | -35℃ ~ -25℃ | 基础值 |
| ESSBR (8%) | -30℃ ~ -20℃ | 环氧基团略微提高 Tg |
| 复合材料 | 更高 | 填料限制链段运动 |

### 分析结论

环氧化改性引入的极性环氧基团会限制链段运动，导致 Tg 略有上升。在白炭黑填充复合材料中，这一效应会更加明显。

---

## 文献来源

- **DOI**: 10.1016/j.polymer.2023.126082
- **图注引用**: Fig.12
