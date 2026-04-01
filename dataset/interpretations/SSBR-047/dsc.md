---
sample_id: SSBR-047
test_type: dsc
data_source_level: L2
literature_doi: 10.1002/app.36677
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
        onset: -39
        midpoint: -35
        endpoint: -31
        unit: °C
        source: DMA tan δ peak Fig.8
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
      note: "无独立DSC曲线，Tg来自DMA Fig.8，低Tg(-35°C)由低乙烯基含量(9.7%)导致"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0.70
---
# SSBR-047 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 玻璃化转变

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| Tg | ~-35°C | Fig. 8, DMA tan δ 峰值估读 |

## DMA 温度扫描

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| E' (玻璃态) | ~3000 MPa | Fig. 8 估读 |
| E' (橡胶态) | ~10 MPa | Fig. 8 估读 |
| tan δ 峰值 | ~0.6 | Fig. 8 估读 |

## 分析说明

文献主要通过 DMA 研究了复合材料的热-力学性能，未提供单独的 DSC 数据。

### 玻璃化转变特点

1. **Tg 位置**: ~-35°C，较低的 Tg 有利于低温性能
2. **乙烯基含量影响**: 9.7% 乙烯基含量是 Tg 较低的主要原因
3. **填料影响**: 硅烷改性后界面相互作用对 Tg 影响有限

### 热学性能意义

- 低 Tg 有利于轮胎的低温抗湿滑性能
- 宽温度范围内的粘弹性行为影响轮胎动态性能
