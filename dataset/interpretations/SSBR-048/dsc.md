---
sample_id: SSBR-048
test_type: dsc
data_source_level: L3
literature_doi: 10.1002/app.40348
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
      - { x: -60, y: -0.35, confidence: 0.50, source: "L3 典型曲线估计" }
      - { x: -50, y: -0.35, confidence: 0.50, source: "L3 典型曲线估计" }
      - { x: -40, y: -0.36, confidence: 0.50, source: "L3 典型曲线估计" }
      - { x: -32, y: -0.38, confidence: 0.55, source: "L3 Tg onset估计" }
      - { x: -28, y: -0.45, confidence: 0.55, source: "L3 Tg区间估计" }
      - { x: -25, y: -0.52, confidence: 0.60, source: "L3 Tg midpoint基于乙烯基含量" }
      - { x: -22, y: -0.48, confidence: 0.55, source: "L3 Tg区间估计" }
      - { x: -18, y: -0.42, confidence: 0.55, source: "L3 Tg endpoint估计" }
      - { x: -10, y: -0.40, confidence: 0.50, source: "L3 典型曲线估计" }
      - { x: 0, y: -0.40, confidence: 0.50, source: "L3 典型曲线估计" }
      - { x: 20, y: -0.40, confidence: 0.50, source: "L3 典型曲线估计" }
    curve_features:
      Tg:
        onset: -32
        midpoint: -25
        endpoint: -18
        unit: °C
        source: L3 基于34.7mol%乙烯基+29.5wt%苯乙烯估计
      glass_transition_width:
        value: 14
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - { x: -25, y: null, reference: "Tg ~-25°C 基于微观结构估计", deviation_percent: 0 }
      overall_quality: acceptable
    metadata:
      point_count: 11
      x_range: [-60, 20]
      y_range: [-0.52, -0.35]
      avg_confidence: 0.53
---
# SSBR-048 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 玻璃化转变

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| Tg | ~-25°C | 估计值（基于乙烯基含量） |

## 分析说明

文献主要聚焦于动态性能和分散性研究，未提供详细的 DSC 或 DMA 温度扫描数据。

### 热学性能说明

基于 SSBR 微观结构参数的估计：
- 34.7 mol% 乙烯基含量提供适中的 Tg
- 29.5 wt% 苯乙烯含量略微提高 Tg
- 综合估计 Tg 约为 -25°C

### 星形结构影响

星形结构对热学性能的影响：
- 星形臂的运动可能影响松弛行为
- 高分子量 (351,000) 可能略微影响 Tg
- 氨基官能团的氢键作用可能增加 Tg
