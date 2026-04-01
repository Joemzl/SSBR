---
sample_id: SSBR-025
interpretation_type: dsc
source_figure: Table 3
source_doi: 10.1002/app.48696
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
data:
  tg:
    value: -8.5
    unit: ℃
    source: Table 3 (DMA)
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
        midpoint: -8.5
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
# SSBR-025 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、玻璃化转变

### 数值数据

| 样品状态 | Tg (℃) | 来源 |
|---------|--------|------|
| 复合材料 | -8.5 | Table 3 (DMA) |

### 测量条件

- **测量方法**: DMA（tan δ 峰值温度）
- **频率**: 10 Hz

### 核心发现

DMPA 官能化 SSBR/白炭黑复合材料的 Tg 为 -8.5℃，较空白组有所升高，表明：
- 硅烷共价键形成增强了界面结合
- 聚合物链段运动受到更强的限制
- 界面层厚度增加

### 分析结论

Tg 升高反映了 DMPA 双官能团（硅烷+氨基）带来的强界面相互作用，限制了聚合物链段的运动自由度，与结合橡胶含量提升的趋势一致。
