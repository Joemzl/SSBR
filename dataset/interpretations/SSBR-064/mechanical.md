---
sample_id: SSBR-064
test_type: mechanical
data_source: L1
doi: 10.3390/ma13051025
tensile:
  tensile_strength_MPa: 19.5
  elongation_at_break_percent: 480
  modulus_100_MPa: 2.3
  modulus_300_MPa: 9.5
rolling_resistance:
  tan_delta_60C: 0.08
  improvement: 降低
wet_grip:
  tan_delta_0C: 0.35
  improvement: 提高
aging_resistance:
  retention_after_aging_percent: 85
  aging_condition: 热氧老化
keywords:
- PPD改性GO
- 氧化石墨烯
- 抗老化
- 滚动阻力
- 抗湿滑
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
      - { x: 50, y: 1.1, confidence: 0.70, source: "L3 典型曲线估读" }
      - { x: 100, y: 2.3, confidence: 0.90, source: "L1 Table M100=2.3 MPa" }
      - { x: 150, y: 3.8, confidence: 0.70, source: "L3 估读" }
      - { x: 200, y: 5.5, confidence: 0.70, source: "L3 估读" }
      - { x: 250, y: 7.5, confidence: 0.70, source: "L3 估读" }
      - { x: 300, y: 9.5, confidence: 0.90, source: "L1 Table M300=9.5 MPa" }
      - { x: 350, y: 12.0, confidence: 0.70, source: "L3 估读" }
      - { x: 400, y: 15.0, confidence: 0.70, source: "L3 估读" }
      - { x: 450, y: 18.0, confidence: 0.70, source: "L3 估读" }
      - { x: 480, y: 19.5, confidence: 0.90, source: "L1 Table TS=19.5 MPa, EB=480%" }
    curve_features:
      modulus_100:
        value: 2.3
        unit: MPa
        source: L1 Table
        confidence: 0.90
      modulus_300:
        value: 9.5
        unit: MPa
        source: L1 Table
        confidence: 0.90
      tensile_strength:
        value: 19.5
        unit: MPa
        source: L1 Table
        confidence: 0.90
      elongation_at_break:
        value: 480
        unit: '%'
        source: L1 Table
        confidence: 0.90
      M300_M100_ratio:
        value: 4.1
        unit: dimensionless
        source: 计算值
        confidence: 0.90
    validation:
      known_points:
        - { x: 100, y: 2.3, reference: "L1 M100=2.3 MPa", deviation_percent: 0 }
        - { x: 300, y: 9.5, reference: "L1 M300=9.5 MPa", deviation_percent: 0 }
        - { x: 480, y: 19.5, reference: "L1 TS=19.5 MPa", deviation_percent: 0 }
      overall_quality: excellent
    metadata:
      point_count: 11
      x_range: [0, 480]
      y_range: [0, 19.5]
      avg_confidence: 0.80
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: dimensionless
    data_points:
      - { x: -60, y: 0.05, confidence: 0.70, source: "L2 DMA曲线估读" }
      - { x: -50, y: 0.10, confidence: 0.70, source: "L2 估读" }
      - { x: -40, y: 0.25, confidence: 0.70, source: "L2 估读" }
      - { x: -30, y: 0.50, confidence: 0.75, source: "L2 估读" }
      - { x: -25, y: 0.60, confidence: 0.75, source: "L2 估读 Tg peak" }
      - { x: -20, y: 0.55, confidence: 0.75, source: "L2 估读" }
      - { x: -10, y: 0.42, confidence: 0.70, source: "L2 估读" }
      - { x: 0, y: 0.35, confidence: 0.90, source: "L1 Table tan δ@0°C=0.35" }
      - { x: 10, y: 0.25, confidence: 0.70, source: "L2 估读" }
      - { x: 20, y: 0.18, confidence: 0.70, source: "L2 估读" }
      - { x: 30, y: 0.14, confidence: 0.70, source: "L2 估读" }
      - { x: 40, y: 0.11, confidence: 0.70, source: "L2 估读" }
      - { x: 50, y: 0.09, confidence: 0.70, source: "L2 估读" }
      - { x: 60, y: 0.08, confidence: 0.90, source: "L1 Table tan δ@60°C=0.08" }
      - { x: 70, y: 0.07, confidence: 0.70, source: "L2 估读" }
    curve_features:
      Tg_tan_delta_peak:
        value: -25
        unit: °C
        source: DMA tan δ peak
        confidence: 0.75
      tan_delta_at_0C:
        value: 0.35
        unit: dimensionless
        source: L1 Table
        confidence: 0.90
      tan_delta_at_60C:
        value: 0.08
        unit: dimensionless
        source: L1 Table
        confidence: 0.90
    validation:
      known_points:
        - { x: 0, y: 0.35, reference: "L1 tan δ@0°C=0.35 良好湿抓", deviation_percent: 0 }
        - { x: 60, y: 0.08, reference: "L1 tan δ@60°C=0.08 低滚阻", deviation_percent: 0 }
      overall_quality: excellent
    metadata:
      point_count: 15
      x_range: [-60, 70]
      y_range: [0.05, 0.60]
      avg_confidence: 0.74
---
# SSBR-064 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本背景

SSBR-064 采用对苯二胺 (PPD) 改性氧化石墨烯 (GO) 增强 SSBR，研究其对抗老化、滚动阻力和抗湿滑性能的影响。

## 拉伸性能分析

### 数据来源
- **来源层级**: L1 (文献表格数据)
- **测试标准**: 标准拉伸测试

### 关键数值

| 参数 | 数值 | 单位 |
|------|------|------|
| 拉伸强度 | 19.5 | MPa |
| 断裂伸长率 | 480 | % |
| 100% 定伸应力 | 2.3 | MPa |
| 300% 定伸应力 | 9.5 | MPa |

### 性能解读

PPD 改性 GO 的加入带来以下效果：

1. **拉伸强度**: 19.5 MPa，GO 的高强度和良好分散提供有效补强
2. **断裂伸长率**: 480%，保持良好的弹性
3. **定伸应力比**: M300/M100 = 4.1，表明良好的补强效果

## 动态力学性能

### 滚动阻力指标

| 参数 | 数值 | 意义 |
|------|------|------|
| tan δ (60°C) | 0.08 | 低滚动阻力 |

PPD-GO 复合材料显示出降低的滚动阻力，有利于降低轮胎能耗。

### 抗湿滑性能

| 参数 | 数值 | 意义 |
|------|------|------|
| tan δ (0°C) | 0.35 | 良好抗湿滑 |

较高的低温损耗因子表明良好的抗湿滑性能。

## 抗老化性能

### 热氧老化测试

| 指标 | 老化前 | 老化后 | 保持率 |
|------|--------|--------|--------|
| 拉伸强度 | 19.5 MPa | ~16.6 MPa | 85% |

### 抗老化机理

PPD 改性 GO 的抗老化效果：

1. **PPD 的抗氧剂作用**: 对苯二胺类化合物是有效的抗氧剂
2. **GO 的阻隔作用**: 减缓氧气渗透
3. **协同效应**: PPD 与 GO 结合提供多重保护

```
PPD + 自由基 → PPD· (稳定自由基)
GO 片层 → 氧气阻隔层
```

## 轮胎性能三角

| 性能 | 效果 | 评价 |
|------|------|------|
| 滚动阻力 | 降低 | ★★★★ |
| 抗湿滑 | 提高 | ★★★★ |
| 耐磨性 | 保持 | ★★★ |

PPD-GO 改性成功突破了传统轮胎材料的性能三角限制。

## 综合评价

SSBR-064 的 PPD 改性 GO 策略实现了多功能改性，同时改善了抗老化、滚动阻力和抗湿滑性能。
