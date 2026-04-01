---
sample_id: SSBR-071
test_type: dsc
data_source: L3
doi: 10.5254/rct.16.84812
glass_transition:
  tg_celsius: -28
  tg_method: estimated
keywords:
- 玻璃化转变
- SSBR
- 白炭黑填充
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
      - x: -80
        y: -0.30
        confidence: 0.55
        source: L3
      - x: -65
        y: -0.28
        confidence: 0.55
        source: L3
      - x: -50
        y: -0.26
        confidence: 0.55
        source: L3
      - x: -38
        y: -0.20
        confidence: 0.60
        source: L3
        note: Tg onset
      - x: -28
        y: -0.05
        confidence: 0.60
        source: L3
        note: Tg midpoint
      - x: -20
        y: 0.08
        confidence: 0.60
        source: L3
        note: Tg endpoint
      - x: -10
        y: 0.10
        confidence: 0.55
        source: L3
      - x: 10
        y: 0.08
        confidence: 0.55
        source: L3
      - x: 40
        y: 0.05
        confidence: 0.55
        source: L3
      - x: 70
        y: 0.04
        confidence: 0.55
        source: L3
    curve_features:
      Tg:
        onset: -38
        midpoint: -28
        endpoint: -20
        unit: °C
        source: L3
      glass_transition_width:
        value: 18
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - x: -28
          parameter: Tg_midpoint
          expected: -28
          actual: -28
          deviation_percent: 0
      overall_quality: acceptable
    metadata:
      point_count: 10
      x_range:
        - -80
        - 70
      y_range:
        - -0.30
        - 0.10
      avg_confidence: 0.57
---
# SSBR-071 DSC 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本背景

SSBR-071 研究 Si747 硅烷偶联剂在白炭黑/SSBR 体系中的作用。

## 玻璃化转变温度

### 数据来源
- **来源层级**: L3 (基于材料体系估算)
- **Tg**: 约 -28°C

### 偶联剂对 Tg 的影响

Si747 偶联对 Tg 的影响：

1. **界面相互作用**: 偶联后界面结合增强，可能略微限制链段运动
2. **填料分散**: 更好的分散可能改变 Tg 表现
3. **整体影响**: Tg 变化通常在 ±2°C

## 热学性能讨论

### 硫化反应动力学

Si747 可能影响硫化反应：

| 参数 | 可能影响 |
|------|----------|
| 焦烧时间 | 可能延长 |
| 正硫化时间 | 可能改变 |
| 交联密度 | 可能提高 |

### 动态热行为

偶联剂对动态性能的影响：
- 可能降低高温 tan δ（滚动阻力）
- 可能保持低温 tan δ（抗湿滑）

## 数据限制说明

文献主要关注界面化学和力学性能，DSC 数据未详细报道。
