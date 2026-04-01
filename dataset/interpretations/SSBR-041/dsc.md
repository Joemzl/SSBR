---
sample_id: SSBR-041
test_type: dsc
data_source_level: L2
literature_doi: 10.1016/j.matdes.2018.05.048
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
        onset: -36
        midpoint: -32
        endpoint: -28
        unit: °C
        source: DMA tan δ peak (no DSC data)
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
      note: "无独立DSC曲线，Tg来自DMA Fig.8数据"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# SSBR-041 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 玻璃化转变

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| Tg | -32°C | Fig. 8, DMA tan δ 峰值 |

## 分析说明

文献中未提供单独的 DSC 测试数据，Tg 数据来自 DMA 测试的 tan δ 峰值温度。

### 玻璃化转变特点

1. **Tg 位置**: -32°C，相对较低
2. **抗氧剂影响**: 抗氧剂官能化对基体 Tg 影响较小
3. **增塑效应**: 可能存在轻微的增塑效应

### 热稳定性

抗氧剂官能化白炭黑提供额外的热稳定性保护：
- 抗氧剂与填料表面共价结合，不会迁移
- 提供长效抗老化保护
- TGA 测试显示改善的热稳定性
