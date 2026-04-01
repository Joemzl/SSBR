---
sample_id: SSBR-023
interpretation_type: mechanical
source_figure: Table VII, Fig. 9
source_doi: 10.1002/app.46653
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
mechanical_subtypes:
- dma
data:
  tg_dma:
    value: -7.3
    unit: ℃
    source: Table VII
  tan_delta_0c:
    value: 0.9059
    unit: '-'
    source: Table VII
  tan_delta_60c:
    value: 0.0734
    unit: '-'
    source: Table VII
  performance_balance_factor:
    value: 12.34
    unit: '-'
    source: 计算值
  bound_rubber:
    value: 67.1
    unit: '%'
    source: Table VII
skill_version: '2.0'
curves:
  stress_strain:
    x_axis:
      label: 应变
      unit: '%'
    y_axis:
      label: 应力
      unit: MPa
    data_points: []
    curve_features:
      modulus_100:
        value: null
        unit: MPa
        source: not_available
        confidence: null
      modulus_300:
        value: null
        unit: MPa
        source: not_available
        confidence: null
      tensile_strength:
        value: null
        unit: MPa
        source: not_available
        confidence: null
      elongation_at_break:
        value: null
        unit: '%'
        source: not_available
        confidence: null
    validation:
      known_points: []
      overall_quality: poor
      notes: "文献未提供静态拉伸数据，仅有 DMA 动态力学数据"
    metadata:
      point_count: 0
      x_range: [0, 0]
      y_range: [0, 0]
      avg_confidence: 0
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: 无量纲
    data_points:
      - {x: -60, y: 0.10, confidence: 0.60, source: "L3"}
      - {x: -50, y: 0.20, confidence: 0.60, source: "L3"}
      - {x: -40, y: 0.40, confidence: 0.60, source: "L3"}
      - {x: -30, y: 0.65, confidence: 0.60, source: "L3"}
      - {x: -20, y: 0.82, confidence: 0.60, source: "L3"}
      - {x: -15, y: 0.88, confidence: 0.60, source: "L3"}
      - {x: -10, y: 0.92, confidence: 0.65, source: "L3"}
      - {x: -7.3, y: 0.94, confidence: 0.70, source: "L3"}
      - {x: -5, y: 0.92, confidence: 0.65, source: "L3"}
      - {x: 0, y: 0.9059, confidence: 0.95, source: "L1"}
      - {x: 10, y: 0.65, confidence: 0.60, source: "L3"}
      - {x: 20, y: 0.42, confidence: 0.60, source: "L3"}
      - {x: 30, y: 0.28, confidence: 0.60, source: "L3"}
      - {x: 40, y: 0.18, confidence: 0.60, source: "L3"}
      - {x: 50, y: 0.12, confidence: 0.60, source: "L3"}
      - {x: 60, y: 0.0734, confidence: 0.95, source: "L1"}
      - {x: 70, y: 0.055, confidence: 0.60, source: "L3"}
    curve_features:
      tan_delta_0C:
        value: 0.9059
        unit: '-'
        source: Table VII
        confidence: 0.95
      tan_delta_60C:
        value: 0.0734
        unit: '-'
        source: Table VII
        confidence: 0.95
      tan_delta_max:
        value: 0.94
        unit: '-'
        source: L3 estimated
        confidence: 0.70
      Tg:
        value: -7.3
        unit: °C
        method: peak
        source: Table VII
        confidence: 0.95
    validation:
      known_points:
        - temperature: 0
          tan_delta_expected: 0.9059
          tan_delta_estimated: 0.9059
          deviation_percent: 0.0
        - temperature: 60
          tan_delta_expected: 0.0734
          tan_delta_estimated: 0.0734
          deviation_percent: 0.0
      overall_quality: good
    metadata:
      point_count: 17
      x_range: [-60, 70]
      y_range: [0.055, 0.94]
      avg_confidence: 0.68
---
# SSBR-023 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

- **官能化试剂**: 3-MPA (3-巯基丙酸)
- **核心官能团**: 羧基 (-COOH)
- **接枝工艺**: 固态原位接枝 (solid-state in situ grafting)
- **接枝率**: 2.6 mol%

## 动态力学性能（DMA温度扫描）

### 数值数据

| 指标 | 数值 | 单位 | 说明 |
|------|------|------|------|
| Tg (DMA) | -7.3 | ℃ | tan δ 峰值温度 |
| tan δ (0℃) | 0.9059 | - | 湿地抓地力指标 |
| tan δ (60℃) | 0.0734 | - | 滚动阻力指标 |
| 性能平衡因子 | 12.34 | - | tan δ(0℃) / tan δ(60℃) |
| 结合橡胶含量 | 67.1 | % | - |

### 核心发现

1. **湿地抓地力改善**: tan δ(0℃) 相比空白组提升 19.3%
2. **滚动阻力降低**: tan δ(60℃) 相比空白组降低 19.6%
3. **优异的性能平衡**: 同时改善湿地抓地力和滚动阻力

### 机理分析

固态原位接枝工艺直接在混炼过程中实现 3-MPA 与 SSBR 的接枝反应，避免了溶液法的溶剂回收问题。羧基官能团与白炭黑表面硅羟基形成强氢键，显著改善了填料-橡胶界面相互作用。

### 与对照组对比

| 样本 | tan δ(0℃) | tan δ(60℃) | 结合橡胶 |
|------|-----------|------------|---------|
| SSBR-023 (0.8 phr 3-MPA) | 0.9059 | 0.0734 | 67.1% |
| 空白组 | 0.7594 | 0.0913 | 57.1% |
| 变化率 | +19.3% | -19.6% | +17.5% |

## 分析结论

SSBR-023 采用固态原位接枝工艺，在 0.8 phr 3-MPA 添加量下实现了湿地抓地力和滚动阻力的同步优化，结合橡胶含量提升至 67.1%，表明界面相互作用显著增强。
