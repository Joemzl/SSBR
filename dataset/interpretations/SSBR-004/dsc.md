---
sample_id: SSBR-004
interpretation_type: dsc
source_doi: 10.1039/c9ra02783a
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-17
data:
  tg:
    value: -3.9
    unit: ℃
    source: SI Table S6
  tg_pure_polymer:
    value: -24.5
    unit: ℃
    source: Fig. 2 (估读)
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
      # 基于 Fig. 2 中 SSBR-g-MPTES42 曲线估读
      # 特征：纯聚合物 Tg 约 -24.5°C，复合材料 Tg 约 -3.9°C
      - {x: -80, y: -0.35, confidence: 0.60, source: "L3"}
      - {x: -60, y: -0.32, confidence: 0.60, source: "L3"}
      - {x: -40, y: -0.28, confidence: 0.65, source: "L3"}
      - {x: -30, y: -0.20, confidence: 0.70, source: "L3"}
      - {x: -24.5, y: -0.12, confidence: 0.85, source: "L2"}  # Tg onset (纯聚合物)
      - {x: -20, y: -0.05, confidence: 0.70, source: "L3"}
      - {x: -15, y: 0.05, confidence: 0.70, source: "L3"}
      - {x: -10, y: 0.12, confidence: 0.70, source: "L3"}
      - {x: 0, y: 0.16, confidence: 0.65, source: "L3"}
      - {x: 20, y: 0.19, confidence: 0.60, source: "L3"}
      - {x: 40, y: 0.21, confidence: 0.60, source: "L3"}
      - {x: 60, y: 0.23, confidence: 0.60, source: "L3"}
    curve_features:
      Tg:
        onset: -30
        midpoint: -24.5
        endpoint: -15
        unit: °C
        source: "Fig. 2 (估读)"
        confidence: 0.85
        note: "纯 SSBR-g-MPTES42 聚合物 Tg"
      Tg_composite:
        value: -3.9
        unit: °C
        source: "SI Table S6 (DMA)"
        confidence: 0.95
        note: "复合材料中 Tg 上移至 -3.9°C"
      glass_transition_width:
        value: 15
        unit: °C
        confidence: 0.70
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - temperature: -24.5
          note: "Tg midpoint from Fig. 2"
      overall_quality: "acceptable"
    metadata:
      point_count: 12
      x_range: [-80, 60]
      y_range: [-0.35, 0.23]
      avg_confidence: 0.67
---
# DSC 热分析解读：SSBR-004

Tg = -3.9℃（DMA），中等官能化程度导致中等的Tg上移。


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 文献来源
- **DOI**: 10.1039/c9ra02783a
