---
sample_id: SSBR-052
test_type: dsc
data_source_level: L3
literature_doi: 10.1016/j.polymer.2014.02.067
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
      - { x: -70, y: -0.35, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: -60, y: -0.35, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: -50, y: -0.36, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: -42, y: -0.38, confidence: 0.60, source: "L3 Tg onset估计" }
      - { x: -36, y: -0.45, confidence: 0.60, source: "L3 Tg区间估计" }
      - { x: -30, y: -0.52, confidence: 0.65, source: "L3 Tg midpoint基于微观结构" }
      - { x: -24, y: -0.47, confidence: 0.60, source: "L3 Tg区间估计" }
      - { x: -18, y: -0.40, confidence: 0.60, source: "L3 Tg endpoint估计" }
      - { x: -10, y: -0.37, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: 0, y: -0.37, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: 20, y: -0.37, confidence: 0.55, source: "L3 典型曲线估计" }
    curve_features:
      Tg:
        onset: -42
        midpoint: -30
        endpoint: -18
        unit: °C
        source: L3 基于48.5mol%乙烯基+19.4wt%苯乙烯估计
      glass_transition_width:
        value: 24
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - { x: -30, y: null, reference: "Tg ~-30°C 基于微观结构估计", deviation_percent: 0 }
      overall_quality: acceptable
    metadata:
      point_count: 11
      x_range: [-70, 20]
      y_range: [-0.52, -0.35]
      avg_confidence: 0.58
---
# SSBR-052 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 玻璃化转变

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| Tg | ~-30°C | 估计值 |

## 分析说明

文献主要聚焦于合成和力学性能研究，未提供详细的 DSC 数据。

### 热学性能估计

基于 SSBR 微观结构参数：
- 19.4 wt% 苯乙烯含量（较低）
- 48.5 mol% 乙烯基含量（较高）
- 高乙烯基含量通常提高 Tg
- 低苯乙烯含量降低 Tg
- 综合估计 Tg 约为 -30°C

### 端基官能化影响

烷氧基硅烷端基对热学性能的影响：
- 端基数量相对主链很少
- 对整体 Tg 影响有限
- 界面相互作用可能略微影响松弛
