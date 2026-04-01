---
sample_id: SSBR-090
interpretation_type: dsc
source_figure: Fig.4
source_doi: 10.1016/j.polymer.2024.128729
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-19
updated_at: '2026-03-31'
data:
  tg:
    value: null
    range: null
    unit: ℃
    source: Fig.4 DSC 曲线
  thermal_source: Fig.4
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
        y: -0.32
        confidence: 0.70
        source: L3
      - x: -70
        y: -0.31
        confidence: 0.70
        source: L3
      - x: -60
        y: -0.30
        confidence: 0.70
        source: L3
      - x: -50
        y: -0.29
        confidence: 0.70
        source: L3
      - x: -40
        y: -0.27
        confidence: 0.70
        source: L3
      - x: -30
        y: -0.24
        confidence: 0.75
        source: L3
      - x: -25
        y: -0.18
        confidence: 0.75
        source: L3
      - x: -20
        y: -0.12
        confidence: 0.75
        source: L3
      - x: -15
        y: -0.10
        confidence: 0.70
        source: L3
      - x: -5
        y: -0.08
        confidence: 0.70
        source: L3
      - x: 10
        y: -0.07
        confidence: 0.65
        source: L3
      - x: 30
        y: -0.06
        confidence: 0.65
        source: L3
    curve_features:
      Tg:
        onset: -30
        midpoint: -22
        endpoint: -15
        unit: °C
        source: L3 estimated from Fig.4
      glass_transition_width:
        value: 15
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
        - 30
      y_range:
        - -0.32
        - -0.06
      avg_confidence: 0.70
---
# DSC 热分析解读：SSBR-090

> **样本性质**: UPy 官能化 SSBR


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-090
- **样品名称**: UPy-SSBR
- **文献DOI**: 10.1016/j.polymer.2024.128729

## 二、玻璃化转变

### 数据来源

文献 Fig.4 提供了 DSC 曲线。

### 核心发现

1. **Tg 变化**: UPy 官能化引入极性基团，可能导致 Tg 上升
2. **氢键解离**: 高温下四重氢键可能解离，表现为额外的热转变
3. **物理交联**: 氢键网络作为物理交联点影响链段运动

### 预期热行为

| 转变类型 | 预期温度范围 | 说明 |
|----------|-------------|------|
| Tg | -30℃ ~ -10℃ | 玻璃化转变 |
| 氢键解离 | 80℃ ~ 120℃ | UPy 四重氢键解离 |

### 分析结论

DSC 分析可揭示 UPy 官能化对 SSBR 热性能的影响，特别是氢键网络的热响应行为对材料的高温性能有重要影响。

---

## 文献来源

- **DOI**: 10.1016/j.polymer.2024.128729
- **图注引用**: Fig.4
