---
sample_id: SSBR-045
test_type: dsc
data_source_level: L3
literature_doi: 10.1002/app.29646
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
    data_points: []
    curve_features:
      Tg:
        onset: -29
        midpoint: -25
        endpoint: -21
        unit: °C
        source: "估计值，文献未直接给出"
      glass_transition_width:
        value: 8
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: acceptable
      note: "文献主要研究应力松弛行为，未提供DSC/DMA热分析数据"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# SSBR-045 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 玻璃化转变

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| Tg | -25°C (估计) | 文献未直接给出 |

## 分析说明

文献主要聚焦于应力松弛行为研究，未提供 DSC 或 DMA 热分析数据。Tg 数据根据 SSBR 基体的典型值估计。

### 热学性能说明

基于 SSBR 的典型特性：
- 高乙烯基含量 SSBR 的 Tg 通常在 -25°C 左右
- 白炭黑填充会略微影响 Tg
- 未使用特殊改性策略，热性能应接近标准水平

### 应力松弛的温度依赖性

文献研究了不同温度下的应力松弛行为：
- 温度升高，松弛速率加快
- 符合时温等效原理 (WLF 方程)
- 松弛活化能约 30-40 kJ/mol
