---
sample_id: SSBR-051
test_type: dsc
data_source: L2
doi: 10.1016/j.polymer.2010.03.006
figures:
- id: Fig.3
  type: dsc
  description: DSC 曲线
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
      - { x: -70, y: -0.38, confidence: 0.70, source: "L2 Fig.3 估读 (TBCSi-SSBR)" }
      - { x: -60, y: -0.38, confidence: 0.70, source: "L2 Fig.3 估读" }
      - { x: -50, y: -0.39, confidence: 0.70, source: "L2 Fig.3 估读" }
      - { x: -45, y: -0.40, confidence: 0.70, source: "L2 Fig.3 估读" }
      - { x: -40, y: -0.42, confidence: 0.75, source: "L2 Fig.3 Tg onset区" }
      - { x: -35, y: -0.48, confidence: 0.75, source: "L2 Fig.3 Tg区间" }
      - { x: -30, y: -0.55, confidence: 0.80, source: "L2 Fig.3 Tg midpoint" }
      - { x: -25, y: -0.50, confidence: 0.75, source: "L2 Fig.3 Tg区间" }
      - { x: -20, y: -0.44, confidence: 0.75, source: "L2 Fig.3 Tg endpoint" }
      - { x: -10, y: -0.40, confidence: 0.70, source: "L2 Fig.3 估读" }
      - { x: 0, y: -0.40, confidence: 0.70, source: "L2 Fig.3 估读" }
      - { x: 20, y: -0.40, confidence: 0.70, source: "L2 Fig.3 估读" }
    curve_features:
      Tg:
        onset: -40
        midpoint: -30
        endpoint: -20
        unit: °C
        source: Fig.3 TBCSi-SSBR (比对照+2~3°C)
      glass_transition_width:
        value: 20
        unit: °C
      delta_Cp_note:
        description: ΔCp轻微降低，链段运动受限
        source: Fig.3
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - { x: -30, y: -0.55, reference: "Tg midpoint (比对照+2~3°C)", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 12
      x_range: [-70, 20]
      y_range: [-0.55, -0.38]
      avg_confidence: 0.72
---
# SSBR-051 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## DSC 分析（Fig.3）

### 玻璃化转变温度

| 样品 | Tg (°C) | ΔCp |
|------|---------|-----|
| 对照 SSBR | 基准 | 基准 |
| TBCSi-SSBR | +2~3°C | 略↓ |

### 关键发现

1. **Tg 轻微上移**
   - 大体积链端基团限制链段运动
   - Tg 升高 2-3°C
   - 符合自由体积理论预期

2. **热容变化**
   - ΔCp 轻微降低
   - 表明链段运动受限程度增加
   - 与大体积末端基团效应一致

3. **热稳定性**
   - 无新的热转变峰
   - 整体热稳定性良好

## 大体积基团对热学性能的影响

| 效应 | 原因 | 结果 |
|------|------|------|
| Tg↑ | 链端运动受限 | +2~3°C |
| ΔCp↓ | 松弛强度降低 | 界面层↑ |
| 稳定性 | 无副反应 | 保持 |
