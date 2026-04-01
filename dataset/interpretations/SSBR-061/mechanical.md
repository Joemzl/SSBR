---
sample_id: SSBR-061
test_type: mechanical
data_source: L1
doi: 10.1016/j.polymertesting.2020.106431
tensile:
  tensile_strength_MPa: 20.0
  elongation_at_break_percent: 450
  modulus_100_MPa: 2.5
  modulus_300_MPa: 10.0
hardness:
  shore_A: 65
abrasion:
  din_abrasion_mm3: 85
keywords:
- 端基官能化
- APTES
- 白炭黑分散
- 耐磨性
- 氨基官能化
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
      - { x: 50, y: 1.2, confidence: 0.70, source: "L3 典型曲线估读" }
      - { x: 100, y: 2.5, confidence: 0.95, source: "L1 Table M100=2.5 MPa" }
      - { x: 150, y: 4.0, confidence: 0.70, source: "L3 估读" }
      - { x: 200, y: 6.0, confidence: 0.70, source: "L3 估读" }
      - { x: 250, y: 8.0, confidence: 0.70, source: "L3 估读" }
      - { x: 300, y: 10.0, confidence: 0.95, source: "L1 Table M300=10.0 MPa" }
      - { x: 350, y: 13.0, confidence: 0.70, source: "L3 估读" }
      - { x: 400, y: 16.5, confidence: 0.70, source: "L3 估读" }
      - { x: 450, y: 20.0, confidence: 0.95, source: "L1 Table TS=20.0 MPa, EB=450%" }
    curve_features:
      modulus_100:
        value: 2.5
        unit: MPa
        source: L1 Table
        confidence: 0.95
      modulus_300:
        value: 10.0
        unit: MPa
        source: L1 Table
        confidence: 0.95
      tensile_strength:
        value: 20.0
        unit: MPa
        source: L1 Table
        confidence: 0.95
      elongation_at_break:
        value: 450
        unit: '%'
        source: L1 Table
        confidence: 0.95
      M300_M100_ratio:
        value: 4.0
        unit: dimensionless
        source: 计算值
        confidence: 0.95
    validation:
      known_points:
        - { x: 100, y: 2.5, reference: "L1 M100=2.5 MPa", deviation_percent: 0 }
        - { x: 300, y: 10.0, reference: "L1 M300=10.0 MPa", deviation_percent: 0 }
        - { x: 450, y: 20.0, reference: "L1 TS=20.0 MPa", deviation_percent: 0 }
      overall_quality: excellent
    metadata:
      point_count: 10
      x_range: [0, 450]
      y_range: [0, 20.0]
      avg_confidence: 0.83
---
# SSBR-061 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本背景

SSBR-061 是通过 3-(氨基丙基)三乙氧基硅烷 (APTES) 进行端基官能化的溶聚丁苯橡胶，旨在改善白炭黑在橡胶基体中的分散性，从而提升复合材料的耐磨性能。

## 拉伸性能分析

### 数据来源
- **来源层级**: L1 (文献 Table 9)
- **测试条件**: 标准拉伸测试

### 关键数值
| 参数 | 数值 | 单位 |
|------|------|------|
| 拉伸强度 | 20.0 | MPa |
| 断裂伸长率 | 450 | % |
| 100% 定伸应力 | 2.5 | MPa |
| 300% 定伸应力 | 10.0 | MPa |

### 性能解读

APTES 端基官能化 SSBR 显示出良好的拉伸性能：

1. **拉伸强度**: 20.0 MPa 的拉伸强度表明 APTES 官能化有效改善了白炭黑与橡胶基体的界面结合
2. **定伸应力**: 较高的 M300/M100 比值 (4.0) 表明优异的补强效果
3. **断裂伸长率**: 450% 的伸长率保持了良好的弹性

## 硬度性能

| 参数 | 数值 | 单位 |
|------|------|------|
| 邵氏硬度 A | 65 | - |

硬度值适中，符合轮胎胎面材料的要求。

## 耐磨性能

### DIN 磨耗测试
| 参数 | 数值 | 单位 |
|------|------|------|
| DIN 磨耗量 | 85 | mm³ |

### 磨耗性能解读

文献重点研究了 APTES 官能化对耐磨性的影响：

1. **分散改善**: APTES 的烷氧基硅烷基团与白炭黑表面硅羟基反应，改善了填料分散
2. **界面增强**: 氨基端基与橡胶基体形成更好的界面结合
3. **磨耗降低**: 相比未官能化样品，磨耗量显著降低

## 官能化机理

APTES 官能化的作用机制：

```
橡胶链—NH2 + HO—Si(白炭黑) → 橡胶链—NH—Si(白炭黑) + H2O
```

氨基端基：
- 与白炭黑表面形成氢键
- 提供化学键合位点
- 改善填料-橡胶界面相互作用

## 综合评价

SSBR-061 的 APTES 端基官能化策略成功改善了白炭黑/SSBR 复合材料的耐磨性能，主要通过：
1. 改善白炭黑分散状态
2. 增强填料-橡胶界面结合
3. 优化应力传递效率
