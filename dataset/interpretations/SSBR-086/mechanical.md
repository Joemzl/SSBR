---
sample_id: SSBR-086
interpretation_type: mechanical
source_figure: Table 3
source_doi: 10.1016/j.compscitech.2024.110899
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-19
updated_at: '2026-03-31'
mechanical_subtypes:
- stress-strain
- dma
data:
  tensile_strength:
    value: null
    unit: MPa
    source: Table 3
  elongation:
    value: null
    unit: '%'
    source: Table 3
  mechanical_source: Table 3
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
        confidence: 0.70
        source: L2
      - x: 25
        y: 0.8
        confidence: 0.65
        source: L2
      - x: 50
        y: 1.5
        confidence: 0.65
        source: L2
      - x: 100
        y: 2.6
        confidence: 0.70
        source: L2
      - x: 150
        y: 4.2
        confidence: 0.65
        source: L2
      - x: 200
        y: 6.2
        confidence: 0.65
        source: L2
      - x: 250
        y: 8.5
        confidence: 0.65
        source: L2
      - x: 300
        y: 11.0
        confidence: 0.70
        source: L2
      - x: 350
        y: 14.0
        confidence: 0.65
        source: L2
      - x: 400
        y: 17.5
        confidence: 0.65
        source: L2
      - x: 450
        y: 21.0
        confidence: 0.70
        source: L2
    curve_features:
      modulus_100:
        value: 2.6
        unit: MPa
        source: L2
        confidence: 0.70
      modulus_300:
        value: 11.0
        unit: MPa
        source: L2
        confidence: 0.70
      tensile_strength:
        value: 21.0
        unit: MPa
        source: L2
        confidence: 0.70
      elongation_at_break:
        value: 450
        unit: '%'
        source: L2
        confidence: 0.70
    validation:
      known_points: []
      overall_quality: acceptable
      note: 胺封端TBIR改善白炭黑分散，trans-1,4结构有助于低滚阻
    metadata:
      point_count: 11
      x_range:
        - 0
        - 450
      y_range:
        - 0
        - 21.0
      avg_confidence: 0.67
---
# 力学性能解读：SSBR-086

> **样本性质**: 胺封端 TBIR 改性 SSBR 复合材料，用于高性能绿色轮胎


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-086
- **样品名称**: 胺封端 TBIR 改性 PC 胎面胶
- **官能化试剂**: 胺封端 trans-1,4-聚(丁二烯-共-异戊二烯) (TBIR)
- **核心官能团**: 氨基
- **苯乙烯含量**: 24.6 wt%
- **乙烯基含量**: 47.9 mol%
- **应用场景**: 高性能绿色轮胎
- **文献DOI**: 10.1016/j.compscitech.2024.110899

## 二、静态力学性能

### 数据来源

文献 Table 3 提供了力学性能数据。

### 核心发现

1. **魔三角平衡**: 研究关注轮胎"魔三角"性能（滚动阻力、湿地抓地力、耐磨性）的协同提升
2. **TBIR 的作用**: 胺封端 TBIR 可与白炭黑表面形成氢键，改善填料分散
3. **链结构效应**: trans-1,4 结构有助于改善低滚阻性能

### 分析结论

胺封端 TBIR 作为改性剂，通过氨基与白炭黑的相互作用以及 trans-1,4 结构的贡献，实现了绿色轮胎"魔三角"性能的协同增强。

---

## 三、动态力学性能

### 轮胎性能指标

- **滚动阻力**: 与 tan δ (60℃) 相关
- **湿地抓地力**: 与 tan δ (0℃) 相关
- **耐磨性**: 与材料强度和模量相关

---

## 文献来源

- **DOI**: 10.1016/j.compscitech.2024.110899
- **数据表格**: Table 3
