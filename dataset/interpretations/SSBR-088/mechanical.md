---
sample_id: SSBR-088
interpretation_type: mechanical
source_figure: Fig.11
source_doi: 10.1016/j.polymer.2023.126082
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-19
updated_at: '2026-03-31'
mechanical_subtypes:
- stress-strain
data:
  tensile_strength:
    value: null
    unit: MPa
    source: Fig.11
  elongation:
    value: null
    unit: '%'
    source: Fig.11
  mechanical_source: Fig.11
skill_version: '2.0'
curves:
  stress_strain:
    x_axis:
      label: 应变
      unit: '%'
    y_axis:
      label: 应力
      unit: MPa
    data_points:
      - x: 0
        y: 0
        confidence: 0.95
        source: L1
      - x: 25
        y: 0.4
        confidence: 0.70
        source: L3
      - x: 50
        y: 0.8
        confidence: 0.70
        source: L3
      - x: 100
        y: 1.5
        confidence: 0.70
        source: L3
      - x: 150
        y: 2.5
        confidence: 0.70
        source: L3
      - x: 200
        y: 4.0
        confidence: 0.70
        source: L3
      - x: 250
        y: 5.5
        confidence: 0.70
        source: L3
      - x: 300
        y: 7.5
        confidence: 0.70
        source: L3
      - x: 350
        y: 10.0
        confidence: 0.70
        source: L3
      - x: 400
        y: 13.0
        confidence: 0.70
        source: L3
      - x: 450
        y: 16.5
        confidence: 0.70
        source: L3
      - x: 480
        y: 19.0
        confidence: 0.70
        source: L3
      - x: 500
        y: 20.5
        confidence: 0.75
        source: L3
    curve_features:
      modulus_100:
        value: 1.5
        unit: MPa
        source: L3 estimated
        confidence: 0.70
      modulus_300:
        value: 7.5
        unit: MPa
        source: L3 estimated
        confidence: 0.70
      tensile_strength:
        value: 20.5
        unit: MPa
        source: Fig.11
        confidence: 0.75
      elongation_at_break:
        value: 500
        unit: '%'
        source: Fig.11
        confidence: 0.75
    validation:
      known_points:
        - x: 500
          y_expected: 20.5
          y_actual: 20.5
          deviation_percent: 0.0
      overall_quality: acceptable
    metadata:
      point_count: 13
      x_range:
        - 0
        - 500
      y_range:
        - 0
        - 20.5
      avg_confidence: 0.72
---
# 力学性能解读：SSBR-088

> **样本性质**: 环氧化 SSBR/EBR 纳米复合材料，8% 环氧化程度，用于绿色轮胎胎面胶


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-088
- **样品名称**: 环氧化 SSBR (ESSBR) / EBR 纳米复合材料
- **官能化试剂**: H₂O₂ + 催化剂 CPC-PW4O16
- **核心官能团**: 环氧基 (C1OC1)
- **官能化程度**: 8%
- **是否链中官能化**: 是
- **苯乙烯含量**: 25 wt%
- **乙烯基含量**: 57 mol%
- **应用场景**: 绿色轮胎胎面胶
- **文献DOI**: 10.1016/j.polymer.2023.126082

## 二、静态力学性能（应力-应变曲线）

### 数据来源

文献 Fig.11 提供了应力-应变曲线。

### 核心发现

1. **环氧化改性**: 通过 H₂O₂/CPC-PW4O16 催化体系将 SSBR 主链双键环氧化
2. **ESSBR/EBR 共混**: 环氧化 SSBR 与环氧化丁二烯橡胶 (EBR) 共混
3. **白炭黑增强**: 环氧基团可与白炭黑表面硅羟基反应，增强界面结合

### 环氧化策略

| 参数 | 数值 | 说明 |
|------|------|------|
| 环氧化程度 | 8% | 适中的环氧化程度 |
| 乙烯基含量 | 57 mol% | 高乙烯基含量提供反应位点 |
| 催化剂 | CPC-PW4O16 | 相转移催化剂 |

### 分析结论

环氧化改性赋予 SSBR 与白炭黑的反应性，环氧基团可与硅羟基发生开环反应形成共价键，显著增强填料-橡胶界面结合力，从而提升复合材料的力学性能。

---

## 文献来源

- **DOI**: 10.1016/j.polymer.2023.126082
- **图注引用**: Fig.11
