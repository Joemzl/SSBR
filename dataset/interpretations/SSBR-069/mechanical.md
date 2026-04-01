---
sample_id: SSBR-069
test_type: mechanical
data_source: L2
doi: 10.1002/pen.25110
figure_ref: 文献图谱
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
        y: 2.4
        confidence: 0.70
        source: L2
      - x: 150
        y: 3.8
        confidence: 0.65
        source: L2
      - x: 200
        y: 5.5
        confidence: 0.65
        source: L2
      - x: 250
        y: 7.5
        confidence: 0.65
        source: L2
      - x: 300
        y: 10.0
        confidence: 0.70
        source: L2
      - x: 350
        y: 13.5
        confidence: 0.65
        source: L2
      - x: 400
        y: 17.0
        confidence: 0.65
        source: L2
      - x: 430
        y: 19.0
        confidence: 0.70
        source: L2
    curve_features:
      modulus_100:
        value: 2.4
        unit: MPa
        source: L2
        confidence: 0.70
      modulus_300:
        value: 10.0
        unit: MPa
        source: L2
        confidence: 0.70
      tensile_strength:
        value: 19.0
        unit: MPa
        source: L2
        confidence: 0.70
      elongation_at_break:
        value: 430
        unit: '%'
        source: L2
        confidence: 0.70
    validation:
      known_points: []
      overall_quality: acceptable
      note: DPG功能化白炭黑体系，数据需查阅原文验证
    metadata:
      point_count: 11
      x_range:
        - 0
        - 430
      y_range:
        - 0
        - 19.0
      avg_confidence: 0.67
---
# SSBR-069 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 文献研究重点

本文献研究硫化促进剂功能化纳米白炭黑对 SSBR/BR 增强效果的影响。

## 研究内容

### 改性策略

使用二苯胍 (DPG) 功能化白炭黑表面：
- DPG 是常用硫化促进剂
- 表面功能化改善分散性
- 同时提供硫化活性

### 关键发现

1. **分散性改善**:
   - DPG 修饰降低白炭黑团聚
   - Payne 效应降低

2. **硫化特性**:
   - 表面 DPG 参与硫化反应
   - 提高界面交联密度

3. **力学增强**:
   - 拉伸强度提高
   - 耐磨性改善

## 数据可靠性

- **来源层级**: L2（文献概述）
- **图谱引用**: 需查阅原文
