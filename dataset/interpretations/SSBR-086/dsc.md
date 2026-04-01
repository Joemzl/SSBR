---
sample_id: SSBR-086
interpretation_type: dsc
source_figure: null
source_doi: 10.1016/j.compscitech.2024.110899
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-19
updated_at: '2026-03-31'
data:
  tg:
    value: null
    unit: ℃
    source: 文献未报告 DSC 数据
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
        y: -0.30
        confidence: 0.50
        source: L3
      - x: -60
        y: -0.28
        confidence: 0.50
        source: L3
      - x: -45
        y: -0.24
        confidence: 0.50
        source: L3
      - x: -35
        y: -0.18
        confidence: 0.55
        source: L3
        note: Tg onset
      - x: -25
        y: -0.05
        confidence: 0.55
        source: L3
        note: Tg midpoint
      - x: -17
        y: 0.08
        confidence: 0.55
        source: L3
        note: Tg endpoint
      - x: 0
        y: 0.10
        confidence: 0.50
        source: L3
      - x: 30
        y: 0.07
        confidence: 0.50
        source: L3
      - x: 60
        y: 0.05
        confidence: 0.50
        source: L3
      - x: 100
        y: 0.03
        confidence: 0.50
        source: L3
    curve_features:
      Tg:
        onset: -35
        midpoint: -25
        endpoint: -17
        unit: °C
        source: L3
        note: 基于苯乙烯24.6wt%和乙烯基47.9mol%估算
      glass_transition_width:
        value: 18
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: poor
      note: 文献未提供DSC数据，基于组成估算
    metadata:
      point_count: 10
      x_range:
        - -80
        - 100
      y_range:
        - -0.30
        - 0.10
      avg_confidence: 0.52
---
# DSC 热分析解读：SSBR-086

> **样本性质**: 胺封端 TBIR 改性 SSBR


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-086
- **文献DOI**: 10.1016/j.compscitech.2024.110899

## 二、DSC 数据

**文献未提供 DSC 热分析数据。**

### 预期 Tg 范围

基于苯乙烯含量 (24.6 wt%) 和乙烯基含量 (47.9 mol%)，预期 Tg 约为 -30℃ ~ -20℃。

---

## 文献来源

- **DOI**: 10.1016/j.compscitech.2024.110899
- **数据状态**: DSC 数据不可用
