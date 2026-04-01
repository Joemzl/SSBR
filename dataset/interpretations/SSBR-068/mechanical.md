---
sample_id: SSBR-068
test_type: mechanical
data_source: L1
doi: 10.1002/pen.23533
tensile:
  tensile_strength_MPa: 16.5
  elongation_at_break_percent: 380
  modulus_100_MPa: 2.0
  modulus_300_MPa: 7.5
filler_system:
  primary_filler: 膨胀石墨 (EG)
  modifier: 羧基化丁苯橡胶 (XSBR)
  carbon_black: 有/无对比
keywords:
- 膨胀石墨
- XSBR增容
- 纳米复合材料
- 羧基官能化
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
        confidence: 0.95
        source: L1
      - x: 20
        y: 0.6
        confidence: 0.70
        source: L2
      - x: 50
        y: 1.2
        confidence: 0.70
        source: L2
      - x: 100
        y: 2.0
        confidence: 0.95
        source: L1
      - x: 150
        y: 3.2
        confidence: 0.70
        source: L2
      - x: 200
        y: 4.6
        confidence: 0.70
        source: L2
      - x: 250
        y: 6.0
        confidence: 0.70
        source: L2
      - x: 300
        y: 7.5
        confidence: 0.95
        source: L1
      - x: 330
        y: 9.5
        confidence: 0.65
        source: L3
      - x: 355
        y: 12.5
        confidence: 0.65
        source: L3
      - x: 370
        y: 15.0
        confidence: 0.65
        source: L3
      - x: 380
        y: 16.5
        confidence: 0.95
        source: L1
    curve_features:
      modulus_100:
        value: 2.0
        unit: MPa
        source: L1
        confidence: 0.95
      modulus_300:
        value: 7.5
        unit: MPa
        source: L1
        confidence: 0.95
      tensile_strength:
        value: 16.5
        unit: MPa
        source: L1
        confidence: 0.95
      elongation_at_break:
        value: 380
        unit: '%'
        source: L1
        confidence: 0.95
    validation:
      known_points:
        - x: 100
          y_expected: 2.0
          y_actual: 2.0
          deviation_percent: 0
        - x: 300
          y_expected: 7.5
          y_actual: 7.5
          deviation_percent: 0
      overall_quality: good
    metadata:
      point_count: 12
      x_range:
        - 0
        - 380
      y_range:
        - 0
        - 16.5
      avg_confidence: 0.80
---
# SSBR-068 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本背景

SSBR-068 研究膨胀石墨 (EG) 填充 SSBR 复合材料，采用羧基化丁苯橡胶 (XSBR) 作为增容剂改善 EG 的分散和界面结合。

## 拉伸性能分析

### 数据来源
- **来源层级**: L1 (文献表格数据)
- **测试标准**: 标准拉伸测试

### 关键数值

| 参数 | 数值 | 单位 |
|------|------|------|
| 拉伸强度 | 16.5 | MPa |
| 断裂伸长率 | 380 | % |
| 100% 定伸应力 | 2.0 | MPa |
| 300% 定伸应力 | 7.5 | MPa |

### 性能解读

膨胀石墨/SSBR 复合材料的力学特点：

1. **拉伸强度**: 16.5 MPa，EG 提供一定的补强效果
2. **伸长率**: 380%，EG 片层可能略微限制基体变形
3. **定伸应力**: M300/M100 = 3.75，适中的补强效果

## XSBR 增容效果

### 增容机理

```
XSBR-COOH + EG 表面活性位点 → 界面相互作用增强
        ↓
   改善 EG 分散
        ↓
   提升力学性能
```

### 有/无增容剂对比

| 性能 | 无 XSBR | 有 XSBR |
|------|---------|---------|
| 分散性 | 差 | 好 |
| 拉伸强度 | 低 | 高 |
| 伸长率 | 低 | 较高 |

## 膨胀石墨特性

### EG 的结构特点

| 特性 | 描述 |
|------|------|
| 结构 | 层状石墨，层间膨胀 |
| 比表面积 | 高 |
| 导电性 | 良好 |
| 阻燃性 | 优异 |

### EG vs 常规填料

| 填料 | 补强效果 | 导电性 | 阻燃性 |
|------|----------|--------|--------|
| EG | 中 | 好 | 优 |
| 炭黑 | 高 | 好 | 差 |
| 白炭黑 | 高 | 无 | 差 |

## 炭黑复配效果

文献研究了 EG 与炭黑复配体系：

1. **协同补强**: 炭黑补充 EG 的补强效果
2. **导电网络**: EG 和炭黑形成协同导电网络
3. **成本优化**: 部分替代炭黑

## 综合评价

SSBR-068 展示了膨胀石墨作为功能性填料的潜力，XSBR 增容剂有效改善了 EG 的分散和界面结合。
