---
sample_id: SSBR-079
test_type: mechanical
data_source: L2
doi: 10.1007/s13726-020-00843-3
figure_ref: Fig.4
extraction_date: 2026-03-18
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
      - x: 0
        y: 0
        confidence: 0.70
        source: L2
      - x: 25
        y: 0.7
        confidence: 0.65
        source: L2
      - x: 50
        y: 1.3
        confidence: 0.65
        source: L2
      - x: 100
        y: 2.3
        confidence: 0.70
        source: L2
      - x: 150
        y: 3.6
        confidence: 0.65
        source: L2
      - x: 200
        y: 5.2
        confidence: 0.65
        source: L2
      - x: 250
        y: 7.2
        confidence: 0.65
        source: L2
      - x: 300
        y: 9.5
        confidence: 0.70
        source: L2
      - x: 350
        y: 12.5
        confidence: 0.65
        source: L2
      - x: 400
        y: 16.0
        confidence: 0.65
        source: L2
      - x: 440
        y: 19.0
        confidence: 0.70
        source: L2
    curve_features:
      modulus_100:
        value: 2.3
        unit: MPa
        source: L2
        confidence: 0.70
      modulus_300:
        value: 9.5
        unit: MPa
        source: L2
        confidence: 0.70
      tensile_strength:
        value: 19.0
        unit: MPa
        source: L2
        confidence: 0.70
      elongation_at_break:
        value: 440
        unit: '%'
        source: L2
        confidence: 0.70
    validation:
      known_points: []
      overall_quality: acceptable
      note: 羧基化EVA改性白炭黑改善分散，数据来源于Fig.4
    metadata:
      point_count: 11
      x_range:
        - 0
        - 440
      y_range:
        - 0
        - 19.0
      avg_confidence: 0.67
---
# SSBR-079 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 文献研究重点

本文献研究羧基化乙烯/醋酸乙烯酯共聚物 (EVA) 改性纳米白炭黑在轮胎胎面胶中的应用。

## 研究内容

### EVA 改性策略

使用羧基化 EVA 改性白炭黑：
- EVA 与白炭黑表面羟基反应
- 改善白炭黑与橡胶的相容性
- 提高分散性

### 力学性能分析

根据文献 Fig.4，分析了 EVA 改性对力学性能的影响：

| 性能 | 未改性 | EVA 改性 | 变化 |
|------|--------|----------|------|
| 拉伸强度 | 基准 | 提高 | ↑ |
| 撕裂强度 | 基准 | 提高 | ↑ |
| 耐磨性 | 基准 | 改善 | ↑ |

### 关键发现

1. **分散性改善**:
   - EVA 改性降低白炭黑表面能
   - 减少团聚，改善分散

2. **界面增强**:
   - EVA 形成过渡界面层
   - 改善应力传递

## 数据可靠性

- **来源层级**: L2（图面分析）
- **图谱引用**: 文献 Fig.4
