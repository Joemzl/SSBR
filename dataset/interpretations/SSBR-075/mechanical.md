---
sample_id: SSBR-075
test_type: mechanical
data_source: L2
doi: 10.3390/polym12010209
figure_ref: Fig.3
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
        y: 1.4
        confidence: 0.65
        source: L2
      - x: 100
        y: 2.5
        confidence: 0.70
        source: L2
      - x: 150
        y: 4.0
        confidence: 0.65
        source: L2
      - x: 200
        y: 5.8
        confidence: 0.65
        source: L2
      - x: 250
        y: 8.0
        confidence: 0.65
        source: L2
      - x: 300
        y: 10.5
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
      - x: 420
        y: 18.5
        confidence: 0.70
        source: L2
    curve_features:
      modulus_100:
        value: 2.5
        unit: MPa
        source: L2
        confidence: 0.70
      modulus_300:
        value: 10.5
        unit: MPa
        source: L2
        confidence: 0.70
      tensile_strength:
        value: 18.5
        unit: MPa
        source: L2
        confidence: 0.70
      elongation_at_break:
        value: 420
        unit: '%'
        source: L2
        confidence: 0.70
    validation:
      known_points: []
      overall_quality: acceptable
      note: 数据来源于文献Fig.3图面读取
    metadata:
      point_count: 11
      x_range:
        - 0
        - 420
      y_range:
        - 0
        - 18.5
      avg_confidence: 0.67
---
# SSBR-075 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

- **样本编号**: SSBR-075
- **高分子类型**: 轮胎胎面胶硅烷化研究用 SSBR
- **官能化类型**: TESPT 硅烷偶联剂
- **文献 DOI**: 10.3390/polym12010209

## 力学测试数据

### 力学性能（Fig.3）

文献 Fig.3 展示了力学性能数据：

| 参数 | 数值 | 数据来源 |
|------|------|----------|
| 拉伸强度 | 文献图面读取 | L2 |
| 断裂伸长率 | 文献图面读取 | L2 |
| 定伸模量 | 文献图面读取 | L2 |

## 性能解读

### TESPT 硅烷化效果

1. **界面改性**: TESPT 改善白炭黑与橡胶的界面结合
2. **硅烷化反应**: 硅烷偶联剂与白炭黑表面羟基反应
3. **性能提升**: 提高力学强度和动态性能

### 轮胎胎面胶应用

- 改善白炭黑分散
- 降低 Payne 效应
- 平衡滚阻和抓地力

## 数据质量说明

- 力学数据来源于文献图面读取 (L2)
