---
sample_id: SSBR-084
interpretation_type: mechanical
source_figure: Fig.7
source_doi: 10.1016/j.europolj.2024.113653
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-19
updated_at: '2026-03-31'
mechanical_subtypes:
- stress-strain
data:
  tensile_strength:
    value: null
    range: null
    unit: MPa
    source: Fig.7 应力-应变曲线
  elongation:
    value: null
    range: null
    unit: '%'
    source: Fig.7 应力-应变曲线
  mechanical_source: Fig.7
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
      - x: 50
        y: 0.8
        confidence: 0.65
        source: L2
      - x: 100
        y: 1.5
        confidence: 0.70
        source: L2
      - x: 150
        y: 2.1
        confidence: 0.65
        source: L2
      - x: 200
        y: 2.8
        confidence: 0.65
        source: L2
      - x: 300
        y: 4.2
        confidence: 0.70
        source: L2
      - x: 400
        y: 6.0
        confidence: 0.65
        source: L2
      - x: 500
        y: 8.5
        confidence: 0.65
        source: L2
      - x: 600
        y: 11.5
        confidence: 0.65
        source: L2
      - x: 700
        y: 14.0
        confidence: 0.70
        source: L2
    curve_features:
      modulus_100:
        value: 1.5
        unit: MPa
        source: L2
        confidence: 0.70
        note: 未硫化CNO官能化SSBR，弹性模量低
      modulus_300:
        value: 4.2
        unit: MPa
        source: L2
        confidence: 0.70
      tensile_strength:
        value: 14.0
        unit: MPa
        source: L2
        confidence: 0.70
      elongation_at_break:
        value: 700
        unit: '%'
        source: L2
        confidence: 0.70
    validation:
      known_points: []
      overall_quality: acceptable
      note: CNO点击反应引入吡啶基/羧基，离子交联提供物理交联点
    metadata:
      point_count: 10
      x_range:
        - 0
        - 700
      y_range:
        - 0
        - 14.0
      avg_confidence: 0.67
---
# 力学性能解读：SSBR-084

> **样本性质**: 腈氧化物 (CNO) 官能化 SSBR，通过无催化剂点击反应引入吡啶基/羧基，官能化程度 1.9-16.8%


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-084
- **样品名称**: CNO-py/CNO-COOH 官能化 SSBR
- **官能化试剂**: 腈氧化物 (CNO-py: 吡啶基腈氧化物; CNO-COOH: 羧基腈氧化物)
- **官能化程度**: 1.9-16.8%
- **是否链中官能化**: 是
- **文献DOI**: 10.1016/j.europolj.2024.113653

## 二、静态力学性能（应力-应变曲线）

### 数据来源

文献 Fig.7 提供了不同官能化程度样品的应力-应变曲线。

### 核心发现

1. **离子交联网络**: CNO-py 和 CNO-COOH 可通过酸碱相互作用形成离子交联
2. **可逆网络**: 这种离子交联具有可逆性，可用于自愈合材料设计
3. **官能化程度影响**: 官能化程度 (1.9-16.8%) 对力学性能有显著影响

### 官能化策略

- **CNO-py**: 引入吡啶基（碱性），SMILES: c1cc[n+]cc1C=N[O-]
- **CNO-COOH**: 引入羧基（酸性），可与吡啶基形成离子对

### 力学性能特点

1. **模量变化**: 随官能化程度增加，模量可能增加（取决于交联密度）
2. **伸长率**: 离子交联的可逆性可能保持较好的伸长率
3. **强度**: 离子相互作用提供额外的物理交联点

### 分析结论

通过腈氧化物与 SSBR 主链双键的无催化剂点击反应，成功引入了吡啶基和羧基官能团。这些官能团可形成可逆的离子交联网络，为材料赋予独特的力学性能和自愈合潜力。

---

## 文献来源

- **DOI**: 10.1016/j.europolj.2024.113653
- **图注引用**: Fig.7 应力-应变曲线
