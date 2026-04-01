---
sample_id: SSBR-024
interpretation_type: dsc
source_figure: Table III
source_doi: 10.1002/app.48243
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
data:
  tg:
    value: -10.0
    unit: ℃
    source: Table III (DMA)
  thermal_source: DMA 测量
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
        midpoint: -10.0
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
      notes: "Tg 来源于 DMA 测量 (tan δ peak)，文献未提供独立 DSC 数据"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# SSBR-024 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、玻璃化转变

### 数值数据

| 样品状态 | Tg (℃) | 来源 |
|---------|--------|------|
| 复合材料 | -10.0 | Table III (DMA) |

### 测量条件

- **测量方法**: DMA（tan δ 峰值温度）
- **频率**: 10 Hz

### 核心发现

MMP 官能化 SSBR/白炭黑复合材料的 Tg 为 -10.0℃，与空白组（-12.5℃）相比略有升高，表明官能化改善了聚合物链段与填料的相互作用。

### 分析结论

Tg 的轻微升高反映了 MMP 官能化带来的界面相互作用增强，酯基与白炭黑硅羟基形成的氢键限制了聚合物链段的运动自由度。
