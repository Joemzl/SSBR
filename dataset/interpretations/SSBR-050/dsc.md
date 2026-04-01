---
sample_id: SSBR-050
test_type: dsc
data_source: L2
doi: 10.1016/j.nanoen.2018.03.038
figures:
- id: Fig.15
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
      - { x: -60, y: -0.40, confidence: 0.70, source: "L2 Fig.15 估读 (官能化SSBR)" }
      - { x: -50, y: -0.40, confidence: 0.70, source: "L2 Fig.15 估读" }
      - { x: -45, y: -0.41, confidence: 0.70, source: "L2 Fig.15 估读" }
      - { x: -38, y: -0.43, confidence: 0.75, source: "L2 Fig.15 Tg onset" }
      - { x: -33, y: -0.50, confidence: 0.75, source: "L2 Fig.15 Tg区间" }
      - { x: -28, y: -0.58, confidence: 0.80, source: "L2 Fig.15 Tg midpoint ~-28°C" }
      - { x: -23, y: -0.52, confidence: 0.75, source: "L2 Fig.15 Tg区间" }
      - { x: -18, y: -0.46, confidence: 0.75, source: "L2 Fig.15 Tg endpoint" }
      - { x: -10, y: -0.42, confidence: 0.70, source: "L2 Fig.15 估读" }
      - { x: 0, y: -0.42, confidence: 0.70, source: "L2 Fig.15 估读" }
      - { x: 20, y: -0.42, confidence: 0.70, source: "L2 Fig.15 估读" }
      - { x: 50, y: -0.42, confidence: 0.70, source: "L2 Fig.15 估读" }
    curve_features:
      Tg:
        onset: -38
        midpoint: -28
        endpoint: -18
        unit: °C
        source: Fig.15 官能化SSBR ~-28°C
      glass_transition_width:
        value: 20
        unit: °C
      delta_Cp_change:
        description: ΔCp略降，界面层增厚
        source: Fig.15
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - { x: -28, y: -0.58, reference: "Tg ~-28°C (官能化)", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 12
      x_range: [-60, 50]
      y_range: [-0.58, -0.40]
      avg_confidence: 0.72
---
# SSBR-050 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## DSC 分析（Fig.15）

### 玻璃化转变温度

| 样品 | Tg (°C) | ΔCp |
|------|---------|-----|
| 对照 SSBR | ~-30 | 基准 |
| 羟基官能化 SSBR | ~-28 | 略↓ |

### 关键发现

1. **Tg 轻微上移**
   - 羟基官能化导致 Tg 略有升高（~2°C）
   - 可能原因：极性基团增强分子间相互作用
   - 变化幅度在可接受范围内

2. **热稳定性**
   - 官能化不影响整体热稳定性
   - 无额外热转变峰

3. **界面层厚度**
   - ΔCp 降低表明界面层增厚
   - "束缚橡胶"含量增加
   - 与低滚阻性能一致

## 结构-热学关联

羟基官能化对热学性能的影响机制：
- -OH 与 SiO₂ 表面形成氢键
- 限制界面区域链段运动
- 降低能量耗散（低 tan δ）
