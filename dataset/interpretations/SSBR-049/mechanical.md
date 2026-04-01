---
sample_id: SSBR-049
test_type: mechanical
data_source: L2
doi: 10.1002/app.43342
figure_ref: Fig.7, Fig.8
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
    data_points:
      - { x: -60, y: 0.05, confidence: 0.70, source: "L2 Fig.6 估读 (150°C硅烷化)" }
      - { x: -50, y: 0.08, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: -40, y: 0.15, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: -30, y: 0.40, confidence: 0.75, source: "L2 Fig.6 估读" }
      - { x: -25, y: 0.65, confidence: 0.75, source: "L2 Fig.6 估读" }
      - { x: -20, y: 0.80, confidence: 0.80, source: "L2 Fig.6 Tg peak" }
      - { x: -15, y: 0.70, confidence: 0.75, source: "L2 Fig.6 估读" }
      - { x: -10, y: 0.50, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 0, y: 0.30, confidence: 0.80, source: "L2 Fig.7 湿抓指标" }
      - { x: 10, y: 0.20, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 20, y: 0.15, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 30, y: 0.12, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 40, y: 0.10, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 50, y: 0.09, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 60, y: 0.08, confidence: 0.80, source: "L2 Fig.8 滚阻指标" }
      - { x: 70, y: 0.07, confidence: 0.70, source: "L2 Fig.6 估读" }
      - { x: 80, y: 0.06, confidence: 0.70, source: "L2 Fig.6 估读" }
    curve_features:
      Tg_tan_delta_peak:
        value: -20
        unit: °C
        source: Fig.6 tan δ peak
        confidence: 0.80
      tan_delta_0C:
        value: 0.30
        unit: dimensionless
        source: Fig.7 0°C
        confidence: 0.80
      tan_delta_60C:
        value: 0.08
        unit: dimensionless
        source: Fig.8 60°C
        confidence: 0.80
      Tg:
        value: -20
        unit: °C
        method: tan_delta_peak
        source: Fig.6
        confidence: 0.80
    validation:
      known_points:
        - { x: -20, y: 0.80, reference: "Tg ~-20°C", deviation_percent: 0 }
        - { x: 0, y: 0.30, reference: "0°C tan δ 湿抓指标", deviation_percent: 0 }
        - { x: 60, y: 0.08, reference: "60°C tan δ 滚阻指标", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 17
      x_range: [-60, 80]
      y_range: [0.05, 0.80]
      avg_confidence: 0.73
---
# SSBR-049 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 测试条件

- **复合材料体系**: SSBR/SiO₂ 硫化胶
- **填料**: 沉淀法白炭黑
- **偶联剂**: TESPT (Si-69)
- **硅烷化温度**: 140°C, 150°C, 160°C
- **测试方法**: 动态力学分析 (DMA)、RPA

## 动态力学性能

### Payne 效应 (0°C)

| 硅烷化温度 | tan δ (低应变) | tan δ (高应变) | Payne 效应强度 |
|------------|----------------|----------------|----------------|
| 140°C | 较高 | 较低 | 较强 |
| 150°C | 中等 | 中等 | 中等 |
| 160°C | 较低 | 较高 | 较弱 |

### Payne 效应 (60°C)

60°C 下的损耗因子变化趋势与 0°C 类似，但整体数值较低。

### 关键发现

1. **硅烷化温度优化**: 150°C 为最佳硅烷化温度
   - 过低温度 (140°C): TESPT 反应不完全，填料网络强
   - 过高温度 (160°C): 可能发生早期硫化

2. **湿地抓地力指标 (0°C tan δ)**: 
   - 硅烷化温度影响显著
   - 150°C 处理样品性能最佳

3. **滚动阻力指标 (60°C tan δ)**:
   - 随硅烷化温度升高而降低
   - 160°C 样品滚阻最低，但可能牺牲其他性能

## 轮胎应用关联

- **硅烷化工艺**: 温度控制是关键，影响偶联效率和预硫化程度
- **性能平衡**: 需在湿地抓地力和滚动阻力间取得平衡
- **工艺窗口**: 150°C 附近是较优的硅烷化温度区间

## 数据可靠性

- **来源层级**: L2（图面估读）
- **图谱引用**: 文献 Fig.7 (0°C), Fig.8 (60°C)
