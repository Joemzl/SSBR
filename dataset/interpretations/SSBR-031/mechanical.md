---
sample_id: SSBR-031
interpretation_type: mechanical
source_figure: Fig. 2-4
source_doi: 10.1039/c5ra24965a
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
mechanical_subtypes:
- dma
data:
  tg_dma:
    value: 0.1
    unit: ℃
    source: Table 5
  tan_delta_max:
    value: 1.3
    unit: '-'
    source: Table 5
  activation_energy:
    value: 17.7
    unit: kJ/mol
    source: Table 5
  mechanical_source: MD simulation + experimental validation
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
        source: v1.0 data
        confidence: null
      modulus_300:
        value: null
        unit: MPa
        source: v1.0 data
        confidence: null
      tensile_strength:
        value: null
        unit: MPa
        source: v1.0 data
        confidence: null
      elongation_at_break:
        value: null
        unit: '%'
        source: v1.0 data
        confidence: null
    validation:
      known_points: []
      overall_quality: pending
    metadata:
      point_count: 0
      x_range:
      - 0
      - 0
      y_range:
      - 0
      - 0
      avg_confidence: 0
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: 无量纲
    data_points:
      - { x: -60, y: 0.03, confidence: 0.65, source: L3 }
      - { x: -50, y: 0.04, confidence: 0.65, source: L3 }
      - { x: -40, y: 0.06, confidence: 0.65, source: L3 }
      - { x: -30, y: 0.10, confidence: 0.65, source: L3 }
      - { x: -20, y: 0.20, confidence: 0.65, source: L3 }
      - { x: -10, y: 0.55, confidence: 0.65, source: L3 }
      - { x: 0, y: 1.20, confidence: 0.70, source: L3 }
      - { x: 0.1, y: 1.30, confidence: 0.95, source: L1 }
      - { x: 10, y: 0.75, confidence: 0.65, source: L3 }
      - { x: 20, y: 0.40, confidence: 0.65, source: L3 }
      - { x: 30, y: 0.25, confidence: 0.65, source: L3 }
      - { x: 40, y: 0.18, confidence: 0.65, source: L3 }
      - { x: 50, y: 0.14, confidence: 0.65, source: L3 }
      - { x: 60, y: 0.11, confidence: 0.65, source: L3 }
      - { x: 70, y: 0.09, confidence: 0.65, source: L3 }
    curve_features:
      tan_delta_0C:
        value: 1.20
        unit: '-'
        source: L3 interpolated
        confidence: 0.70
      tan_delta_60C:
        value: 0.11
        unit: '-'
        source: L3 interpolated
        confidence: 0.65
      tan_delta_max:
        value: 1.30
        unit: '-'
        source: Table 5
        confidence: 0.95
      Tg:
        value: 0.1
        unit: °C
        method: peak
        source: Table 5
        confidence: 0.95
    validation:
      known_points:
        - { x: 0.1, y: 1.30, reference: "Table 5 tan δ max", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 15
      x_range: [-60, 70]
      y_range: [0.03, 1.30]
      avg_confidence: 0.70
---
# SSBR-031 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本基本信息

- **样本编号**: SSBR-031
- **官能化试剂**: 3-巯基丙酸 (3-MPA)
- **官能化程度**: 9.6 wt%
- **研究类型**: 分子动力学模拟 + 实验验证
- **文献来源**: RSC Advances, 2016, 6, 14643-14650

## 一、动态力学性能（DMA温度扫描）

### 数值数据

| 指标 | 数值 | 单位 | 说明 |
|------|------|------|------|
| Tg (DMA) | 0.1 | ℃ | tan δ 峰值温度 |
| tan δ max | 1.30 | - | 损耗因子峰值 |
| Ea (活化能) | 17.7 | kJ/mol | 橡胶链活化能 |

### 与对照组对比

| 样品 | 接枝量 (wt%) | Tg (℃) | tan δ max | Ea (kJ/mol) |
|------|-------------|--------|-----------|-------------|
| M0 (空白) | 0 | -5.9 | 1.07 | 11.3 |
| M1 | 2.4 | -3.9 | 1.11 | 12.8 |
| M2 | 4.3 | -2.7 | 1.19 | 14.2 |
| **M3 (SSBR-031)** | **9.6** | **0.1** | **1.30** | **17.7** |

### 核心发现

1. **Tg 显著提升**: 官能化使 Tg 从 -5.9℃ 提升至 0.1℃，提升约 6℃
2. **tan δ max 增加**: 从 1.07 增至 1.30，增幅 21.5%
3. **活化能增加**: 从 11.3 kJ/mol 增至 17.7 kJ/mol，增幅 56.6%

## 二、分子动力学模拟结果

### 最优接枝量分析

文献通过 MD 模拟发现存在最优接枝量：

| 模拟样本 | 接枝量 (wt%) | 结合能 (kcal/mol) | 自扩散系数 |
|---------|-------------|-------------------|-----------|
| g0 | 0 | -337.8 | 最高 |
| g3 | 9.5 | 257.5 | 降低 |
| **g4** | **14.2** | **294.1** | **最低** |
| g5 | 20.8 | 138.4 | 升高 |

### 关键结论

- **最优接枝量为 14.2 wt%**：此时结合能最高、自扩散系数最低、白炭黑分散最佳
- **竞争效应**：氢键作用、空间位阻和橡胶-橡胶相互作用共同决定最优值
- **SSBR-031 (9.6 wt%)** 接近最优区间，性能优异

## 三、性能机理分析

### 界面相互作用机制

3-MPA 的羧基 (-COOH) 与白炭黑表面硅羟基形成**氢键**：

```
SSBR-COOH ··· HO-Si (白炭黑)
     ↑
   氢键作用
```

### 分散性改善原因

1. **氢键网络**：羧基与硅羟基形成稳定氢键
2. **极性匹配**：官能化 SSBR 极性增加，与白炭黑亲和性提高
3. **链段活动受限**：填料-橡胶相互作用增强，分子链运动受限

## 四、综合评价

### 优势

- Tg 和 tan δ max 同步提升，有利于湿地抓地力
- 活化能显著增加，表明填料-橡胶相互作用增强
- MD 模拟与实验结果吻合良好

### 设计建议

基于 MD 模拟结论，建议将 3-MPA 接枝量控制在 **10-14 wt%** 范围内，以获得最佳白炭黑分散和界面相互作用。
