---
sample_id: SSBR-038
test_type: dsc
data_source_level: L2
literature_doi: 10.1016/j.compscitech.2018.03.036
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
        onset: -32
        midpoint: -28
        endpoint: -24
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
      note: "无独立DSC曲线，Tg来自DMA Fig.7数据"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# SSBR-038 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 玻璃化转变

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| Tg | -28°C | Fig. 7, DMA tan δ 峰值 |

## 分析说明

文献中未提供 DSC 测试数据，Tg 数据来自 DMA 测试的 tan δ 峰值温度。

### 玻璃化转变特点

1. **Tg 位置**: -28°C，与纯 SSBR 相近
2. **改性影响**: 烷基硫醇改性 GO 对 SSBR 的 Tg 影响较小
3. **相容性**: 良好的相容性使得基体相结构保持稳定

### 热稳定性

文献中提到 DT-GO 改性提高了复合材料的热稳定性，但未给出具体 DSC 数据。
