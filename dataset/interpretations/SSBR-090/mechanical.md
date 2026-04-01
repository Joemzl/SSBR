---
sample_id: SSBR-090
interpretation_type: mechanical
source_figure: Fig.5
source_doi: 10.1016/j.polymer.2024.128729
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-19
updated_at: '2026-03-31'
mechanical_subtypes:
- stress-strain
data:
  tensile_strength:
    value: null
    unit: MPa
    source: Fig.5
  elongation:
    value: null
    unit: '%'
    source: Fig.5
  mechanical_source: Fig.5
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
        y: 0.5
        confidence: 0.70
        source: L3
      - x: 50
        y: 1.0
        confidence: 0.70
        source: L3
      - x: 100
        y: 1.8
        confidence: 0.70
        source: L3
      - x: 150
        y: 2.8
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
        y: 7.2
        confidence: 0.70
        source: L3
      - x: 350
        y: 9.5
        confidence: 0.70
        source: L3
      - x: 400
        y: 12.0
        confidence: 0.70
        source: L3
      - x: 450
        y: 15.0
        confidence: 0.70
        source: L3
      - x: 500
        y: 18.0
        confidence: 0.70
        source: L3
      - x: 530
        y: 19.5
        confidence: 0.75
        source: L3
    curve_features:
      modulus_100:
        value: 1.8
        unit: MPa
        source: L3 estimated
        confidence: 0.70
      modulus_300:
        value: 7.2
        unit: MPa
        source: L3 estimated
        confidence: 0.70
      tensile_strength:
        value: 19.5
        unit: MPa
        source: Fig.5
        confidence: 0.75
      elongation_at_break:
        value: 530
        unit: '%'
        source: Fig.5
        confidence: 0.75
    validation:
      known_points:
        - x: 530
          y_expected: 19.5
          y_actual: 19.5
          deviation_percent: 0.0
      overall_quality: acceptable
    metadata:
      point_count: 13
      x_range:
        - 0
        - 530
      y_range:
        - 0
        - 19.5
      avg_confidence: 0.72
---
# 力学性能解读：SSBR-090

> **样本性质**: UPy 官能化 SSBR，通过氢键相互作用增强水下吸声性能


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-090
- **样品名称**: UPy-SSBR (脲基嘧啶酮官能化 SSBR)
- **官能化试剂**: UPy-NCO (脲基嘧啶酮异氰酸酯)
- **核心官能团**: 脲基嘧啶酮 (UPy)
- **是否链中官能化**: 是
- **应用场景**: 水下吸声材料、非共价键网络
- **文献DOI**: 10.1016/j.polymer.2024.128729

## 二、静态力学性能（应力-应变曲线）

### 数据来源

文献 Fig.5 提供了应力-应变曲线。

### 核心发现

1. **四重氢键**: UPy 基团可形成强四重氢键，作为物理交联点
2. **可逆网络**: 氢键网络具有可逆性，赋予材料自愈合潜力
3. **吸声性能**: 氢键网络的动态特性有利于声能耗散

### UPy 官能化策略

| 特性 | 说明 |
|------|------|
| 官能团 | 脲基嘧啶酮 (UPy) |
| 相互作用 | 四重氢键 (DDAA-AADD) |
| 结合强度 | 高（>10⁷ M⁻¹） |
| 可逆性 | 温度响应性解离 |

### 分析结论

UPy 官能化通过引入强四重氢键相互作用，构建了超分子物理交联网络。这种网络的动态特性使材料在力学性能和能量耗散（吸声）之间取得平衡。

---

## 文献来源

- **DOI**: 10.1016/j.polymer.2024.128729
- **图注引用**: Fig.5 应力-应变曲线
