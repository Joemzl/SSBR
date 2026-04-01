---
sample_id: SSBR-079
test_type: thermal
data_source: null
doi: 10.1007/s13726-020-00843-3
figure_ref: null
extraction_date: 2026-03-18
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
      - x: -80
        y: -0.32
        confidence: 0.50
        source: L3
      - x: -65
        y: -0.30
        confidence: 0.50
        source: L3
      - x: -50
        y: -0.27
        confidence: 0.50
        source: L3
      - x: -40
        y: -0.22
        confidence: 0.55
        source: L3
        note: Tg onset
      - x: -32
        y: -0.08
        confidence: 0.55
        source: L3
        note: Tg midpoint
      - x: -24
        y: 0.06
        confidence: 0.55
        source: L3
        note: Tg endpoint
      - x: -10
        y: 0.08
        confidence: 0.50
        source: L3
      - x: 20
        y: 0.05
        confidence: 0.50
        source: L3
      - x: 50
        y: 0.04
        confidence: 0.50
        source: L3
      - x: 80
        y: 0.02
        confidence: 0.50
        source: L3
    curve_features:
      Tg:
        onset: -40
        midpoint: -32
        endpoint: -24
        unit: °C
        source: L3
      glass_transition_width:
        value: 16
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: poor
      note: 文献未明确报道DSC数据，基于SSBR基体估算
    metadata:
      point_count: 9
      x_range:
        - -80
        - 50
      y_range:
        - -0.32
        - 0.08
      avg_confidence: 0.52
---
# SSBR-079 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 数据状态

⚠️ **本文献 DSC 数据需查阅原文**

## 文献研究重点

本文献关注 EVA 改性白炭黑的轮胎应用，可能涉及 DMA 动态性能分析。

## 数据可靠性

- **来源层级**: 无明确数据
- **图谱引用**: 需查阅原文
