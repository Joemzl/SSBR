---
sample_id: SSBR-064
test_type: dsc
data_source: L3
doi: 10.3390/ma13051025
glass_transition:
  tg_celsius: -28
  tg_method: estimated
keywords:
- 玻璃化转变
- SSBR
- GO复合材料
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  dsc_heat_flow:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: 热流
      unit: mW/mg
      direction: exo_up
    data_points:
      - { x: -70, y: -0.36, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: -60, y: -0.36, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: -50, y: -0.37, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: -40, y: -0.39, confidence: 0.60, source: "L3 Tg onset估计" }
      - { x: -34, y: -0.45, confidence: 0.60, source: "L3 Tg区间估计" }
      - { x: -28, y: -0.52, confidence: 0.65, source: "L3 Tg midpoint~-28°C" }
      - { x: -22, y: -0.47, confidence: 0.60, source: "L3 Tg区间估计" }
      - { x: -16, y: -0.41, confidence: 0.60, source: "L3 Tg endpoint估计" }
      - { x: -5, y: -0.38, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: 10, y: -0.38, confidence: 0.55, source: "L3 典型曲线估计" }
      - { x: 30, y: -0.38, confidence: 0.55, source: "L3 典型曲线估计" }
    curve_features:
      Tg:
        onset: -40
        midpoint: -28
        endpoint: -16
        unit: °C
        source: L3 估计值
      glass_transition_width:
        value: 24
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - { x: -28, y: null, reference: "Tg ~-28°C 估计值", deviation_percent: 0 }
      overall_quality: acceptable
    metadata:
      point_count: 11
      x_range: [-70, 30]
      y_range: [-0.52, -0.36]
      avg_confidence: 0.58
---
# SSBR-064 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本背景

SSBR-064 是 PPD 改性 GO/SSBR 复合材料，研究抗老化和动态力学性能。

## 玻璃化转变温度

### 数据来源
- **来源层级**: L3 (基于材料体系估算)
- **Tg**: 约 -28°C

### GO 对 Tg 的影响

少量 GO 添加对 Tg 的影响：

1. **纳米限域效应**: GO 片层可能略微限制链段运动
2. **界面效应**: PPD 改性改善 GO-橡胶界面
3. **整体影响**: Tg 变化预计在 ±3°C 范围内

## 热稳定性

### PPD 的抗氧化作用

PPD 改性 GO 对热稳定性的影响：

1. **热氧化起始温度**: 可能略有提高
2. **氧化诱导期**: 延长
3. **热分解温度**: 基本不变

### 动态热行为

与动态力学性能相关的热学特性：

| 温度 | 行为 | 性能意义 |
|------|------|----------|
| 0°C | 接近 Tg，高阻尼 | 抗湿滑 |
| 25°C | 橡胶态 | 正常使用 |
| 60°C | 橡胶态，低损耗 | 低滚动阻力 |

## 数据限制说明

文献主要关注动态力学性能和抗老化研究，DSC 数据未详细报道。
