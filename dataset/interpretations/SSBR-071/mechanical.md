---
sample_id: SSBR-071
test_type: mechanical
data_source: L1
doi: 10.5254/rct.16.84812
tensile:
  tensile_strength_MPa: 21.5
  elongation_at_break_percent: 450
  modulus_100_MPa: 2.6
  modulus_300_MPa: 11.0
hardness:
  shore_A: 66
coupling_agent:
  type: Si747
  loading: 与白炭黑配合使用
keywords:
- 硅烷偶联剂
- Si747
- 白炭黑-硅烷反应
- 界面偶联
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
      - x: 25
        y: 0.8
        confidence: 0.70
        source: L2
      - x: 50
        y: 1.5
        confidence: 0.70
        source: L2
      - x: 100
        y: 2.6
        confidence: 0.95
        source: L1
      - x: 150
        y: 4.3
        confidence: 0.70
        source: L2
      - x: 200
        y: 6.5
        confidence: 0.70
        source: L2
      - x: 250
        y: 8.8
        confidence: 0.70
        source: L2
      - x: 300
        y: 11.0
        confidence: 0.95
        source: L1
      - x: 350
        y: 14.0
        confidence: 0.70
        source: L2
      - x: 400
        y: 17.5
        confidence: 0.70
        source: L2
      - x: 430
        y: 20.0
        confidence: 0.65
        source: L3
      - x: 450
        y: 21.5
        confidence: 0.95
        source: L1
    curve_features:
      modulus_100:
        value: 2.6
        unit: MPa
        source: L1
        confidence: 0.95
      modulus_300:
        value: 11.0
        unit: MPa
        source: L1
        confidence: 0.95
      tensile_strength:
        value: 21.5
        unit: MPa
        source: L1
        confidence: 0.95
      elongation_at_break:
        value: 450
        unit: '%'
        source: L1
        confidence: 0.95
    validation:
      known_points:
        - x: 100
          y_expected: 2.6
          y_actual: 2.6
          deviation_percent: 0
        - x: 300
          y_expected: 11.0
          y_actual: 11.0
          deviation_percent: 0
      overall_quality: excellent
    metadata:
      point_count: 12
      x_range:
        - 0
        - 450
      y_range:
        - 0
        - 21.5
      avg_confidence: 0.80
---
# SSBR-071 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本背景

SSBR-071 研究 Si747 硅烷偶联剂在白炭黑/SSBR 复合材料中的界面偶联机理和性能优化。

## 拉伸性能分析

### 数据来源
- **来源层级**: L1 (文献表格数据)
- **测试标准**: 标准拉伸测试

### 关键数值

| 参数 | 数值 | 单位 |
|------|------|------|
| 拉伸强度 | 21.5 | MPa |
| 断裂伸长率 | 450 | % |
| 100% 定伸应力 | 2.6 | MPa |
| 300% 定伸应力 | 11.0 | MPa |

### 性能解读

Si747 偶联的白炭黑/SSBR 复合材料特点：

1. **高拉伸强度**: 21.5 MPa，Si747 有效改善了界面结合
2. **良好伸长率**: 450%，保持了基体的弹性
3. **高定伸应力比**: M300/M100 = 4.2，表明优异的补强效果

## 硬度性能

| 参数 | 数值 | 单位 |
|------|------|------|
| 邵氏硬度 A | 66 | - |

硬度适中，符合轮胎应用要求。

## Si747 偶联机理

### 硅烷偶联剂结构

Si747 是一种双官能硅烷偶联剂，结构包含：
- 烷氧基硅烷基团（与白炭黑反应）
- 多硫键或其他反应性基团（与橡胶反应）

### 偶联反应过程

```
第一步：硅烷-白炭黑反应（混炼阶段）
Si747-Si(OR)3 + HO-Si(白炭黑) → Si747-Si-O-Si(白炭黑)

第二步：硅烷-橡胶反应（硫化阶段）
Si747-Sx + 橡胶双键 → Si747-S-橡胶
```

### 界面结构

```
[白炭黑]—O—Si—R—Sx—[橡胶链]
```

## 偶联效率影响因素

### 反应温度

| 阶段 | 温度 | 主要反应 |
|------|------|----------|
| 混炼 | 140-160°C | 硅烷-白炭黑 |
| 硫化 | 160-180°C | 硅烷-橡胶 |

### 反应时间

延长混炼时间有助于提高偶联效率，但需平衡加工性能。

## 综合评价

SSBR-071 系统研究了 Si747 硅烷偶联剂的界面化学，为优化白炭黑/SSBR 复合材料提供了理论指导。
