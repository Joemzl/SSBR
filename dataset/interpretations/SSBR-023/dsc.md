---
sample_id: SSBR-023
interpretation_type: dsc
source_figure: Table VII
source_doi: 10.1002/app.46653
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
data:
  tg:
    value: -7.3
    unit: ℃
    source: Table VII (DMA)
  thermal_source: DMA
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
    data_points: []
    curve_features:
      Tg:
        onset: null
        midpoint: -7.3
        endpoint: null
        unit: °C
        source: DMA_derived
      glass_transition_width:
        value: null
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: acceptable
      notes: "Tg 来源于 DMA 测量而非 DSC，文献未提供纯 DSC 数据"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# SSBR-023 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

- **官能化试剂**: 3-MPA (3-巯基丙酸)
- **核心官能团**: 羧基 (-COOH)
- **接枝工艺**: 固态原位接枝

## 玻璃化转变

### 数值数据

| 样品状态 | Tg (℃) | 来源 |
|---------|--------|------|
| 复合材料 (DMA) | -7.3 | Table VII |

*注：本文献未提供纯聚合物 Tg 数据*

### 核心发现

DMA 测得的 Tg 为 -7.3℃，处于 SSBR 复合材料的典型范围内。

### 分析结论

Tg 值反映了 3-MPA 接枝对聚合物链段运动的影响，羧基官能团与白炭黑的氢键作用可能导致 Tg 略有升高。
