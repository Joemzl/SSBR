---
sample_id: SSBR-034
test_type: mechanical
data_source: L2
literature_doi: 10.1016/j.cej.2019.04.215
tensile:
  tensile_strength_MPa: null
  elongation_at_break_percent: null
  modulus_100_MPa: null
  modulus_300_MPa: null
dma:
  tan_delta_0C: null
  tan_delta_60C: null
  storage_modulus_25C_MPa: null
payne_effect:
  G_0.28_kPa: null
  G_100_kPa: null
  delta_G_kPa: null
hardness:
  shore_A: null
abrasion:
  din_mm3: null
notes: '本文献主要研究 TMPMP/SBR 超疏水涂层的表面性质，非传统力学性能测试。

  涂层厚度约 5μm，应用于纸张基材。'
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
    data_points: []
    curve_features:
      modulus_100:
        value: null
        unit: MPa
        source: "超疏水涂层研究，无传统力学测试"
        confidence: null
      modulus_300:
        value: null
        unit: MPa
        source: "超疏水涂层研究，无传统力学测试"
        confidence: null
      tensile_strength:
        value: null
        unit: MPa
        source: "超疏水涂层研究，无传统力学测试"
        confidence: null
      elongation_at_break:
        value: null
        unit: '%'
        source: "超疏水涂层研究，无传统力学测试"
        confidence: null
    validation:
      known_points: []
      overall_quality: poor
      quality_note: "文献 10.1016/j.cej.2019.04.215 研究超疏水涂层技术，未进行传统拉伸、DMA等力学性能测试"
    metadata:
      point_count: 0
      x_range: [0, 0]
      y_range: [0, 0]
      avg_confidence: 0
---
# SSBR-034 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 测试概述

本样本 SSBR-034 采用**三羟甲基丙烷三(3-巯基丙酸)酯 (TMPMP)** 通过巯基-烯点击化学与 SBR 进行交联反应，主要用于制备超疏水涂层。

## 研究背景

该研究的重点是利用 TMPMP 作为**三官能团交联剂**，通过 UV 固化在 SBR 基材上形成超疏水表面涂层。与传统橡胶复合材料的力学性能研究不同，本文献主要关注涂层的表面性质和耐久性。

## 反应机理

TMPMP 含有三个巯基（-SH）基团，可与 SBR 分子链上的乙烯基双键发生巯基-烯点击反应：

```
TMPMP-SH + CH₂=CH- (SBR) → TMPMP-S-CH₂-CH₂- (交联点)
```

## 涂层特性

根据文献报道：
- **涂层厚度**: 约 5 μm
- **交联密度**: 通过 TMPMP/SBR 配比调控
- **固化方式**: UV 辐射引发自由基反应

## 备注

本样本的研究方向为超疏水涂层技术，未进行传统的拉伸、DMA 等力学性能测试。后续分析将聚焦于涂层的表面特性和润湿性能。
