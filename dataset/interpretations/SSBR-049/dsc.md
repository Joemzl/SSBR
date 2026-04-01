---
sample_id: SSBR-049
test_type: thermal
data_source: L2
doi: 10.1002/app.43342
figure_ref: Fig.6
extraction_date: 2026-03-18
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: dimensionless
    note: "文献使用DMA而非标准DSC，此处记录DMA温度扫描数据"
    data_points:
      - { x: -60, y: 0.05, confidence: 0.70, source: "L2 Fig.6 估读 (150°C硅烷化)" }
      - { x: -50, y: 0.08, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: -40, y: 0.15, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: -30, y: 0.40, confidence: 0.75, source: "L2 Fig.6 估读" }
      - { x: -25, y: 0.65, confidence: 0.75, source: "L2 Fig.6 估读" }
      - { x: -20, y: 0.80, confidence: 0.80, source: "L2 Fig.6 Tg peak" }
      - { x: -15, y: 0.70, confidence: 0.75, source: "L2 Fig.6 估读" }
      - { x: -10, y: 0.50, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 0, y: 0.30, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 10, y: 0.20, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 20, y: 0.15, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 30, y: 0.12, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 40, y: 0.10, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 50, y: 0.09, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 60, y: 0.08, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 70, y: 0.07, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 80, y: 0.06, confidence: 0.70, source: "L2 Fig.6 估读" }
    curve_features:
      Tg:
        onset: -28
        midpoint: -20
        endpoint: -12
        unit: °C
        source: DMA tan δ peak
      glass_transition_width:
        value: 16
        unit: °C
      tan_delta_peak_height:
        value: 0.80
        unit: dimensionless
    validation:
      known_points:
        - { x: -20, y: 0.80, reference: "Tg ~-20°C (DMA)", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 17
      x_range: [-60, 80]
      y_range: [0.05, 0.80]
      avg_confidence: 0.71
---
# SSBR-049 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 测试条件

- **测试方法**: DMA 温度扫描（非标准 DSC）
- **温度范围**: -80°C 至 80°C
- **频率**: 10 Hz
- **样品状态**: 硫化胶

## 动态热机械分析

### tan δ 温度扫描结果

| 硅烷化温度 | Tg (tan δ 峰值) | tan δ 峰高 |
|------------|-----------------|------------|
| 140°C | ~ -20°C | 较高 |
| 150°C | ~ -20°C | 中等 |
| 160°C | ~ -20°C | 较低 |

### 关键发现

1. **Tg 位置**: 硅烷化温度对 Tg 影响较小
   - SSBR 本身 Tg 主要由苯乙烯/乙烯基含量决定
   - 偶联程度对 Tg 影响有限

2. **tan δ 峰高变化**:
   - 140°C: 偶联不完全，聚合物链段运动较自由
   - 160°C: 偶联较完全，界面约束强，tan δ 降低

3. **高温区 tan δ (60°C)**:
   - 与滚动阻力直接相关
   - 150°C 硅烷化样品表现最佳

## 材料特性

- **苯乙烯含量**: 34.6 wt%（较高）
- **乙烯基含量**: 40.1 mol%
- 较高的苯乙烯含量使 Tg 偏高，有利于湿地抓地力

## 数据可靠性

- **来源层级**: L2（图面估读）
- **图谱引用**: 文献 Fig.6 (tan δ-温度曲线)
- **注意**: 文献使用 DMA 而非标准 DSC
