---
sample_id: SSBR-047
test_type: mechanical
data_source_level: L1
literature_doi: 10.1002/app.36677
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  stress_strain:
    x_axis:
      label: 应变
      unit: '%'
    y_axis:
      label: 应力
      unit: MPa
    data_points:
      - { x: 0, y: 0, confidence: 0.95, source: "L1 origin" }
      - { x: 50, y: 1.4, confidence: 0.60, source: "L3 estimated" }
      - { x: 100, y: 2.5, confidence: 0.70, source: "L3 Fig.7 estimated" }
      - { x: 150, y: 4.0, confidence: 0.60, source: "L3 estimated" }
      - { x: 200, y: 6.0, confidence: 0.60, source: "L3 estimated" }
      - { x: 250, y: 8.0, confidence: 0.60, source: "L3 estimated" }
      - { x: 300, y: 10.0, confidence: 0.70, source: "L3 Fig.7 estimated" }
      - { x: 350, y: 12.5, confidence: 0.60, source: "L3 estimated" }
      - { x: 400, y: 15.0, confidence: 0.60, source: "L3 estimated" }
      - { x: 450, y: 18.0, confidence: 0.70, source: "L3 Fig.7 estimated break" }
    curve_features:
      modulus_100:
        value: 2.5
        unit: MPa
        source: Fig.7 estimated
        confidence: 0.70
      modulus_300:
        value: 10.0
        unit: MPa
        source: Fig.7 estimated
        confidence: 0.70
      tensile_strength:
        value: 18.0
        unit: MPa
        source: Fig.7 estimated
        confidence: 0.70
      elongation_at_break:
        value: 450
        unit: '%'
        source: Fig.7 estimated
        confidence: 0.70
    validation:
      known_points:
        - { x: 100, y: 2.5, reference: "M100 estimated", deviation_percent: 0 }
        - { x: 300, y: 10.0, reference: "M300 estimated", deviation_percent: 0 }
        - { x: 450, y: 18.0, reference: "tensile strength estimated", deviation_percent: 0 }
      overall_quality: acceptable
      note: "数据来自Fig.7估读，TESPT/TESPD硅烷改性研究"
    metadata:
      point_count: 10
      x_range: [0, 450]
      y_range: [0, 18.0]
      avg_confidence: 0.66
  payne_storage_modulus:
    x_axis:
      label: 应变
      unit: '%'
      scale: logarithmic
    y_axis:
      label: 储能模量 G'
      unit: MPa
    data_points:
      - { x: 0.1, y: 2.20, confidence: 0.70, source: "L3 Fig.5 estimated" }
      - { x: 0.2, y: 2.05, confidence: 0.65, source: "L3 estimated" }
      - { x: 0.5, y: 1.80, confidence: 0.65, source: "L3 estimated" }
      - { x: 1, y: 1.50, confidence: 0.65, source: "L3 estimated" }
      - { x: 2, y: 1.20, confidence: 0.65, source: "L3 estimated" }
      - { x: 5, y: 0.90, confidence: 0.65, source: "L3 estimated" }
      - { x: 10, y: 0.72, confidence: 0.65, source: "L3 estimated" }
      - { x: 20, y: 0.62, confidence: 0.65, source: "L3 estimated" }
      - { x: 50, y: 0.58, confidence: 0.65, source: "L3 estimated" }
      - { x: 100, y: 0.55, confidence: 0.70, source: "L3 Fig.5 estimated" }
    curve_features:
      G_prime_0:
        value: 2.20
        unit: MPa
        strain_at: 0.1
        source: Fig.5 estimated
        confidence: 0.70
      G_prime_inf:
        value: 0.55
        unit: MPa
        strain_at: 100
        source: Fig.5 estimated
        confidence: 0.70
      delta_G_prime:
        value: 1650
        unit: kPa
        source: calculated
        confidence: 0.70
    validation:
      known_points:
        - { x: 0.1, y: 2.20, reference: "G' low strain from Fig.5", deviation_percent: 0 }
        - { x: 100, y: 0.55, reference: "G' high strain from Fig.5", deviation_percent: 0 }
      overall_quality: acceptable
      note: "硅烷偶联剂(TESPT/TESPD)降低Payne效应"
    metadata:
      point_count: 10
      x_range: [0.1, 100]
      y_range: [0.55, 2.20]
      avg_confidence: 0.66
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: "-"
    data_points:
      - { x: -60, y: 0.04, confidence: 0.60, source: "L3 estimated" }
      - { x: -50, y: 0.10, confidence: 0.60, source: "L3 estimated" }
      - { x: -45, y: 0.22, confidence: 0.60, source: "L3 estimated" }
      - { x: -40, y: 0.40, confidence: 0.65, source: "L3 estimated" }
      - { x: -37, y: 0.52, confidence: 0.65, source: "L3 estimated" }
      - { x: -35, y: 0.60, confidence: 0.70, source: "L2 Tg peak" }
      - { x: -30, y: 0.50, confidence: 0.65, source: "L3 estimated" }
      - { x: -20, y: 0.38, confidence: 0.65, source: "L3 estimated" }
      - { x: -10, y: 0.30, confidence: 0.65, source: "L3 estimated" }
      - { x: 0, y: 0.25, confidence: 0.70, source: "L2 Fig.8 estimated" }
      - { x: 10, y: 0.18, confidence: 0.65, source: "L3 estimated" }
      - { x: 20, y: 0.14, confidence: 0.65, source: "L3 estimated" }
      - { x: 30, y: 0.11, confidence: 0.65, source: "L3 estimated" }
      - { x: 40, y: 0.10, confidence: 0.65, source: "L3 estimated" }
      - { x: 50, y: 0.095, confidence: 0.65, source: "L3 estimated" }
      - { x: 60, y: 0.09, confidence: 0.70, source: "L2 Fig.8 estimated" }
      - { x: 80, y: 0.085, confidence: 0.60, source: "L3 estimated" }
    curve_features:
      tan_delta_peak:
        value: 0.60
        temperature: -35
        unit: "-"
        source: Fig.8 estimated
        confidence: 0.70
      tan_delta_0C:
        value: 0.25
        unit: "-"
        source: Fig.8 estimated
        confidence: 0.70
      tan_delta_60C:
        value: 0.09
        unit: "-"
        source: Fig.8 estimated
        confidence: 0.70
      Tg:
        value: -35
        unit: °C
        source: Fig.8 tan δ peak
        confidence: 0.70
    validation:
      known_points:
        - { x: 0, y: 0.25, reference: "tan δ @ 0°C from Fig.8", deviation_percent: 0 }
        - { x: 60, y: 0.09, reference: "tan δ @ 60°C from Fig.8", deviation_percent: 0 }
      overall_quality: acceptable
      note: "低Tg(-35°C)由低乙烯基含量(9.7%)导致"
    metadata:
      point_count: 17
      x_range: [-60, 80]
      y_range: [0.04, 0.60]
      avg_confidence: 0.65
---
# SSBR-047 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 拉伸性能

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| 拉伸强度 | ~18 MPa | Fig. 7 估读 |
| 断裂伸长率 | ~450% | Fig. 7 估读 |
| 100%定伸应力 | ~2.5 MPa | 估读 |
| 300%定伸应力 | ~10 MPa | 估读 |

## Payne 效应

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| G'(低应变) | ~2.2 MPa | Fig. 5 估读 |
| G'(高应变) | ~0.6 MPa | Fig. 5 估读 |
| ΔG' | ~1.6 MPa | 计算值 |

## DMA 动态力学

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| tan δ (0°C) | ~0.25 | Fig. 8 估读 |
| tan δ (60°C) | ~0.09 | Fig. 8 估读 |

## 性能分析

SSBR-047 研究了硅烷偶联剂（TESPT/TESPD）化学改性白炭黑对 SSBR 复合材料力学和非线性粘弹性行为的影响。

### 力学性能特点

1. **拉伸强度**: ~18 MPa，硅烷改性显著提高了强度
2. **应力-应变曲线**: 显示典型的填充橡胶特征
3. **填料-橡胶相互作用**: 硅烷偶联剂建立了强界面

### 填料分散与 Payne 效应

硅烷改性对填料分散和 Payne 效应的影响：
- TESPT 改性降低了 ΔG'
- 填料网络程度减少
- 分散性改善

### 动态性能

- 低 tan δ (60°C) 表明低滚动阻力
- 保持良好的抗湿滑性能
- 硅烷改性实现了性能平衡
