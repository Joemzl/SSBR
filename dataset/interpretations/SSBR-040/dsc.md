---
sample_id: SSBR-040
test_type: dsc
data_source_level: L2
literature_doi: 10.1016/j.compscitech.2020.108482
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
      note: "无独立DSC曲线，Tg来自DMA Fig.7a数据"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# SSBR-040 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 玻璃化转变

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| Tg | -25°C | Fig. 7a, DMA tan δ 峰值 |

## 分析说明

文献中未提供单独的 DSC 测试数据，Tg 数据来自 DMA 测试的 tan δ 峰值温度。

### 玻璃化转变特点

1. **Tg 位置**: -25°C，典型的官能化 SSBR 范围
2. **HMDS 改性影响**: 表面改性对基体 Tg 影响较小
3. **界面相互作用**: HMDS 改性可能略微影响界面层的分子链运动

### 热性能说明

HMDS 改性白炭黑：
- 表面羟基被三甲基硅基取代
- 减少了填料-填料的氢键相互作用
- 对基体热性能影响有限
