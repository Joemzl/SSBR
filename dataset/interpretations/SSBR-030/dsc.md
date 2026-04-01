---
sample_id: SSBR-030
interpretation_type: dsc
source_figure: Table 6, Fig. 11
source_doi: 10.1039/c4ra09492a
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
data:
  tg:
    value: -23.9
    unit: ℃
    source: Table 6 (DSC)
  tg_pure_polymer:
    value: -24.4
    unit: ℃
    source: Table 6
  heat_capacity:
    value: 0.29
    unit: J/(g·K)
    source: Table 7
  thermal_source: DSC 测量
skill_version: '2.0'
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
      - { x: -60, y: -0.42, confidence: 0.60, source: L3 }
      - { x: -50, y: -0.41, confidence: 0.60, source: L3 }
      - { x: -40, y: -0.40, confidence: 0.60, source: L3 }
      - { x: -32, y: -0.38, confidence: 0.65, source: L3 }
      - { x: -28, y: -0.32, confidence: 0.70, source: L3 }
      - { x: -25, y: -0.25, confidence: 0.75, source: L3 }
      - { x: -23.9, y: -0.20, confidence: 0.95, source: L1 }
      - { x: -22, y: -0.15, confidence: 0.75, source: L3 }
      - { x: -18, y: -0.08, confidence: 0.70, source: L3 }
      - { x: -10, y: -0.04, confidence: 0.60, source: L3 }
      - { x: 0, y: -0.02, confidence: 0.60, source: L3 }
      - { x: 20, y: 0.00, confidence: 0.60, source: L3 }
    curve_features:
      Tg:
        onset: -28
        midpoint: -23.9
        endpoint: -18
        unit: °C
        source: Table 6 + L3 estimation
      glass_transition_width:
        value: 10
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - { x: -23.9, y: -0.20, reference: "Table 6 Tg midpoint", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 12
      x_range: [-60, 20]
      y_range: [-0.42, 0.00]
      avg_confidence: 0.67
---
# SSBR-030 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、玻璃化转变

### 数值数据

| 样品状态 | Tg (℃) | 来源 |
|---------|--------|------|
| 纯 F-SSBR (M3) | -24.4 | Table 6 |
| 复合材料 | -23.9 | Table 6 |
| ΔTg (填充效应) | +0.5 | 计算值 |

### 测量条件

- **升温速率**: 10 ℃/min
- **气氛**: N₂
- **温度范围**: -100℃ 至 50℃

### 核心发现

1. **Tg 轻微升高**：复合材料 Tg 较纯聚合物升高 0.5℃
2. **热容显著提升**：ΔCp 从 0.23（M0）升至 0.29 J/(g·K)
3. **物理意义**：更高的热容表明更多聚合物链段参与玻璃化转变

### 与 DMA 结果对比

| 测量方法 | Tg (℃) | 说明 |
|---------|--------|------|
| DSC | -23.9 | 热容变化 |
| DMA | 0.1 | tan δ 峰值 |
| 差值 | ~24℃ | 频率效应 |

DSC 和 DMA 测得的 Tg 差异是正常的，主要由于 DMA 测量频率（10 Hz）导致的频率效应。

### 分析结论

3-MPA 官能化显著改善了填料分散，导致：
- 被包埋在填料团聚体中的"occluded rubber"减少
- 更多聚合物链段可参与玻璃化转变
- 热容增加反映了分子运动自由度的增加
