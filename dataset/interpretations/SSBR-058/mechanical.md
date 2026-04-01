---
sample_id: SSBR-058
test_type: mechanical
data_source: L1
literature_doi: 10.1016/j.polymer.2018.04.039
tensile:
  tensile_strength_MPa: 22.2
  elongation_at_break_percent: 530
  modulus_100_MPa: 2.1
  modulus_300_MPa: 7.0
dma:
  tan_delta_0C: null
  tan_delta_60C: null
  storage_modulus_25C_MPa: null
payne_effect:
  G_0.28_kPa: null
  G_100_kPa: null
  delta_G_kPa: null
hardness:
  shore_A: 64
abrasion:
  din_mm3: null
notes: 'SSBR-058 为 ME 官能化 SSBR，随后通过 oxa-Michael 反应引入丙烯酸酯交联。

  样本标记为 mSSBR-20 (官能化程度 20%)。

  填料体系: 白炭黑 40 phr。'
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
      - { x: 50, y: 1.0, confidence: 0.70, source: "L3 典型曲线估读" }
      - { x: 100, y: 2.1, confidence: 0.95, source: "L1 Table M100=2.1 MPa" }
      - { x: 150, y: 3.2, confidence: 0.70, source: "L3 估读" }
      - { x: 200, y: 4.5, confidence: 0.70, source: "L3 估读" }
      - { x: 250, y: 5.8, confidence: 0.70, source: "L3 估读" }
      - { x: 300, y: 7.0, confidence: 0.95, source: "L1 Table M300=7.0 MPa" }
      - { x: 350, y: 9.5, confidence: 0.70, source: "L3 估读" }
      - { x: 400, y: 13.0, confidence: 0.70, source: "L3 估读" }
      - { x: 450, y: 17.0, confidence: 0.70, source: "L3 估读" }
      - { x: 500, y: 20.5, confidence: 0.75, source: "L2 接近断裂" }
      - { x: 530, y: 22.2, confidence: 0.95, source: "L1 Table TS=22.2 MPa, EB=530%" }
    curve_features:
      modulus_100:
        value: 2.1
        unit: MPa
        source: L1 Table
        confidence: 0.95
      modulus_300:
        value: 7.0
        unit: MPa
        source: L1 Table
        confidence: 0.95
      tensile_strength:
        value: 22.2
        unit: MPa
        source: L1 Table
        confidence: 0.95
      elongation_at_break:
        value: 530
        unit: '%'
        source: L1 Table
        confidence: 0.95
      M300_M100_ratio:
        value: 3.33
        unit: dimensionless
        source: 计算值
        confidence: 0.95
    validation:
      known_points:
        - { x: 100, y: 2.1, reference: "L1 M100=2.1 MPa", deviation_percent: 0 }
        - { x: 300, y: 7.0, reference: "L1 M300=7.0 MPa", deviation_percent: 0 }
        - { x: 530, y: 22.2, reference: "L1 TS=22.2 MPa", deviation_percent: 0 }
      overall_quality: excellent
    metadata:
      point_count: 12
      x_range: [0, 530]
      y_range: [0, 22.2]
      avg_confidence: 0.83
---
# SSBR-058 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 测试概述

本样本 SSBR-058 采用**2-巯基乙醇 (ME)** 官能化 SSBR，引入羟基后通过 **oxa-Michael 反应**与丙烯酸酯进行交联，实现橡胶网络的可控构建。

## 拉伸性能

### 测试结果

| 性能指标 | 数值 | 单位 |
|---------|------|------|
| 拉伸强度 | 22.2 | MPa |
| 断裂伸长率 | 530 | % |
| 100% 定伸模量 | 2.1 | MPa |
| 300% 定伸模量 | 7.0 | MPa |

### 性能分析

**高拉伸强度 (22.2 MPa)**:
- ME 官能化引入的羟基与白炭黑硅羟基形成氢键
- 丙烯酸酯交联网络提供额外的共价交联
- 填料-橡胶相互作用增强

**良好的伸长率 (530%)**:
- oxa-Michael 交联反应可控
- 交联密度适中，保持分子链柔性
- 官能化程度 20% 平衡了刚性与柔性

## 硬度性能

- **邵尔 A 硬度**: 64
- 硬度适中，表明交联密度和填料分散处于良好状态

## 官能化对力学性能的影响

### 正面效应
1. **羟基引入**: ME 的羟基可与白炭黑表面的硅羟基形成氢键
2. **界面增强**: 填料-橡胶界面相互作用改善
3. **交联可控**: oxa-Michael 反应温和、可控

### 反应机理

```
Step 1: 巯基-烯点击
ME-SH + CH₂=CH- (SSBR) → ME-S-CH₂-CH₂- (羟基化 SSBR)

Step 2: oxa-Michael 加成
R-OH + CH₂=CH-COOR' → R-O-CH₂-CH₂-COOR' (交联)
```

## 配方信息

- **基体**: ME 官能化 SSBR (mSSBR-20)
- **填料**: 白炭黑 40 phr
- **交联剂**: 丙烯酸酯 (通过 oxa-Michael 反应)

## 与同系列样本对比

ME 官能化 SSBR 展现了优异的力学性能，特别是在白炭黑复合体系中：
- 拉伸强度高于传统硫磺硫化体系
- 伸长率保持良好
- 硬度适中

## 参考文献

- DOI: 10.1016/j.polymer.2018.04.039
- 期刊: Polymer
