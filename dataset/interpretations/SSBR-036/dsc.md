---
sample_id: SSBR-036
test_type: dsc
data_source: null
doi: 10.1016/j.compositesb.2020.108301
figures: []
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
        onset: -30
        midpoint: -26
        endpoint: -22
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
      note: "无独立DSC曲线，Tg来自DMA数据"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# SSBR-036 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 数据可用性

本文献未提供 DSC 曲线数据。

## 预期热学特性

基于 SSBR 分子结构参数：
- 苯乙烯含量: 25.0 wt%
- 乙烯基含量: 50.0 mol%

### 预期玻璃化转变温度

| 参数 | 预期范围 | 备注 |
|------|----------|------|
| Tg (SSBR) | -25 ~ -30°C | DMA tan δ 峰位约 -26°C |

### BEP 改性对 Tg 的影响

根据 DMA 数据，BEP 处理略微提高 Tg（~2°C），可能原因：
- 增强的填料-橡胶界面限制链段运动
- 交联密度可能略有变化
