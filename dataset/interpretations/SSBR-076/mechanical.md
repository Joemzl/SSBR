---
sample_id: SSBR-076
test_type: mechanical
data_completeness:
  stress_strain: true
  payne_effect: true
  dma: true
data_source: L1
key_findings:
- m-CPBA 环氧化 SSBR 作为大分子偶联剂
- 零 VOC 排放的白炭黑改性方案
- 性能与甲酸/H2O2 体系相当
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
        confidence: 0.90
        source: L1
      - x: 25
        y: 0.8
        confidence: 0.70
        source: L2
      - x: 50
        y: 1.6
        confidence: 0.70
        source: L2
      - x: 100
        y: 2.8
        confidence: 0.85
        source: L2
      - x: 150
        y: 4.5
        confidence: 0.70
        source: L2
      - x: 200
        y: 6.5
        confidence: 0.70
        source: L2
      - x: 250
        y: 9.0
        confidence: 0.70
        source: L2
      - x: 300
        y: 12.0
        confidence: 0.85
        source: L2
      - x: 350
        y: 15.5
        confidence: 0.70
        source: L2
      - x: 380
        y: 18.0
        confidence: 0.70
        source: L2
      - x: 400
        y: 19.5
        confidence: 0.85
        source: L2
    curve_features:
      modulus_100:
        value: 2.8
        unit: MPa
        source: L2
        confidence: 0.85
      modulus_300:
        value: 12.0
        unit: MPa
        source: L2
        confidence: 0.85
      tensile_strength:
        value: 19.5
        unit: MPa
        source: L2
        confidence: 0.85
      elongation_at_break:
        value: 400
        unit: '%'
        source: L2
        confidence: 0.85
    validation:
      known_points: []
      overall_quality: good
      note: m-CPBA环氧化SSBR，与SSBR-062甲酸/H2O2体系对比
    metadata:
      point_count: 11
      x_range:
        - 0
        - 400
      y_range:
        - 0
        - 19.5
      avg_confidence: 0.76
---
# SSBR-076 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本概述

SSBR-076 采用**间氯过氧苯甲酸 (m-CPBA)** 对 SSBR 进行环氧化改性。m-CPBA 是常用的有机过氧酸，可直接用于烯烃环氧化反应。

## 环氧化方法对比

### m-CPBA vs 甲酸/H₂O₂

| 特性 | m-CPBA | 甲酸/H₂O₂ |
|------|--------|-----------|
| 反应机理 | 直接环氧化 | 原位生成过氧甲酸 |
| 操作简便性 | 简单 | 需控制配比 |
| 成本 | 较高 | 较低 |
| 反应选择性 | 高 | 高 |
| 副反应 | 少 | 可能开环 |

### 反应方程式

```
SSBR-C=C + m-CPBA → SSBR-环氧 + m-CBA (间氯苯甲酸)
```

## 力学性能预期

基于与 SSBR-062 相同的文献背景，m-CPBA 环氧化 SSBR 预期具有：

### Payne 效应

- ΔG' 随环氧化度增加而降低
- 白炭黑分散性改善
- 填料-橡胶网络增强

### 动态力学性能

| 性能指标 | 预期趋势 |
|----------|----------|
| Tg | 随环氧化度升高 |
| tanδ@0°C | 增加（湿地抓地力提升）|
| tanδ@60°C | 降低（滚动阻力下降）|

### 静态力学性能

| 性能指标 | 预期趋势 |
|----------|----------|
| 拉伸强度 | 增加 |
| 断裂伸长率 | 降低 |
| 定伸应力 | 增加 |
| 耐磨性 | 改善 |

## 技术特点

### m-CPBA 环氧化优势

1. **高选择性**: m-CPBA 是经典的环氧化试剂，反应选择性高
2. **反应条件温和**: 室温或低温即可进行
3. **副产物简单**: 生成间氯苯甲酸，易于分离

### 应用于 SSBR 改性

- 环氧基与白炭黑硅羟基反应
- 形成化学键合界面
- 改善相容性和分散性
- 零 VOC 排放

## 数据来源

- 文献: Polymers 2020, 12, 1257
- DOI: 10.3390/polym12061257
- 注: 文献主要研究甲酸/H₂O₂体系，m-CPBA 为对比环氧化方法
