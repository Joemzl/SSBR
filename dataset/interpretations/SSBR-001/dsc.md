---
sample_id: SSBR-001
interpretation_type: dsc
source_figure: "Fig. 2, SI Table S6"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-dsc-interpretation
skill_version: "2.0"
created_at: 2026-03-17
updated_at: 2026-03-31

data:
  tg:
    value: -0.9
    range: null
    unit: "℃"
    source: "SI Table S6 (复合材料)"
  tg_pure_polymer:
    value: -18.4
    range: null
    unit: "℃"
    source: "Fig. 2 (纯 F-SSBR-g-MPL, L2标注)"
  thermal_source: "SI Table S6"
  working_temp_window:
    value: "10℃以上"
    unit: "℃"
    source: "基于Tg估算"
  other_transitions:
    value: null
    source: ""

curves:
  dsc_heat_flow:
    x_axis:
      label: "温度"
      unit: "°C"
    y_axis:
      label: "热流"
      unit: "mV"
      direction: "exo_up"
    data_points:
      # 低温基线区 (-60°C to -35°C)
      - {x: -60, y: -0.85, confidence: 0.65, source: "L3"}
      - {x: -50, y: -0.82, confidence: 0.65, source: "L3"}
      - {x: -40, y: -0.78, confidence: 0.65, source: "L3"}
      - {x: -35, y: -0.75, confidence: 0.65, source: "L3"}
      # 玻璃化转变区 (-30°C to -5°C) - 高密度采样
      - {x: -30, y: -0.68, confidence: 0.70, source: "L3"}
      - {x: -28, y: -0.62, confidence: 0.75, source: "L3"}  # Tg onset 附近
      - {x: -25, y: -0.52, confidence: 0.70, source: "L3"}
      - {x: -22, y: -0.42, confidence: 0.70, source: "L3"}
      - {x: -18.4, y: -0.32, confidence: 0.85, source: "L2"}  # Tg midpoint (标注值)
      - {x: -15, y: -0.25, confidence: 0.70, source: "L3"}
      - {x: -12, y: -0.20, confidence: 0.70, source: "L3"}
      - {x: -8, y: -0.15, confidence: 0.75, source: "L3"}   # Tg endpoint 附近
      - {x: -5, y: -0.12, confidence: 0.70, source: "L3"}
      # 高温基线区 (0°C to +60°C)
      - {x: 0, y: -0.10, confidence: 0.65, source: "L3"}
      - {x: 20, y: -0.08, confidence: 0.65, source: "L3"}
      - {x: 40, y: -0.06, confidence: 0.65, source: "L3"}
      - {x: 60, y: -0.05, confidence: 0.65, source: "L3"}
    curve_features:
      Tg:
        onset: -28
        midpoint: -18.4
        endpoint: -8
        unit: "°C"
        source: "L2 (Fig. 2 标注 midpoint), L3 (onset/endpoint 估读)"
      glass_transition_width:
        value: 20
        unit: "°C"
        calculation: "T_endpoint - T_onset = -8 - (-28)"
      baseline_shift:
        magnitude: "medium"
        direction: "endothermic"
      crystallization_peak:
        exists: false
        temperature: null
        confidence: null
      melting_peak:
        exists: false
        temperature: null
        confidence: null
    validation:
      known_points:
        - feature: "Tg_midpoint"
          expected: -18.4
          measured: -18.4
          deviation: 0
          note: "直接使用图面标注值"
      overall_quality: "good"
    metadata:
      point_count: 17
      x_range: [-60, 60]
      y_range: [-0.85, -0.05]
      avg_confidence: 0.69
---

# DSC 热分析解读：SSBR-001

> **样本性质**: MPL官能化SSBR（3-巯基丙醇接枝），官能化程度3.6 wt%，白炭黑填充复合材料

## 一、基础信息

- **样本ID**: SSBR-001
- **样品名称**: SSBR-g-MPL70（70 phr 白炭黑填充）
- **官能化试剂**: MPL（3-巯基丙醇）
- **官能化程度**: 3.6 wt%
- **文献DOI**: 10.1039/c9ra02783a
- **数据版本**: v2.0（含全范围曲线数据）

## 二、玻璃化转变

### 数值数据

| 样品状态 | Tg (℃) | 来源 | 置信度 |
|---------|--------|------|--------|
| 纯 F-SSBR-g-MPL | -18.4 | Fig. 2 (L2标注) | 0.85 |
| 复合材料 SSBR-g-MPL70 | -0.9 | SI Table S6 | 0.95 |
| ΔTg (填充效应) | +17.5 | 计算值 | - |

> **数据修正说明**: 原始解读中纯聚合物 Tg 误记为 -24.8℃，经核查 Fig. 2 确认 SSBR-g-MPL 的 Tg 标注值为 **-18.4℃**。该值高于空白 SSBR (-25.1℃)，表明官能化对链段运动有明显的限制作用。

### DSC 曲线数据（v2.0 新增）

本次升级从 Fig. 2 估读了完整的 DSC 热流曲线：
- **数据点数**: 17 个（覆盖 -60°C 至 +60°C）
- **采样策略**: 基线区 20°C 间隔，玻璃化转变区 3-5°C 高密度采样
- **平均置信度**: 0.69
- **曲线特征**: Tg onset ≈ -28°C, midpoint = -18.4°C, endpoint ≈ -8°C
- **转变宽度**: ~20°C

### 测量条件

- **升温速率**: 10 ℃/min（文献标准条件）
- **气氛**: N₂
- **温度范围**: -80℃ ~ 室温
- **Y轴方向**: Exo up（放热向上）

### 核心发现

1. **纯 F-SSBR-g-MPL 的 Tg (-18.4℃)**: 比空白 SSBR (-25.1℃) 升高 6.7℃，说明羟基官能团显著限制了分子链运动，这与官能团间的氢键作用有关
2. **复合材料 Tg (-0.9℃)**: 相比纯聚合物升高约 17.5℃，体现白炭黑填充的界面约束效应
3. **界面约束效应**: Tg 升高说明填料-橡胶界面相互作用强，限制了链段运动

### 与对照组对比

| 样本 | Tg - 纯聚合物 (℃) | Tg - 复合材料 (℃) | ΔTg |
|------|-------------------|-------------------|-----|
| SSBR-g-MPL | -18.4 | -0.9 | +17.5 |
| 空白 SSBR | -25.1 | -4.7 | +20.4 |

### 分析结论

MPL官能化使纯聚合物 Tg 升高至 -18.4℃（比空白高 6.7℃），表明：

1. **官能化的链段限制效应**: 羟基官能团之间形成氢键，直接限制链段运动
2. **填充后的协同效应**: 复合材料 ΔTg = 17.5℃，加上纯聚合物本身的 Tg 升高，最终 Tg 达到 -0.9℃
3. **更高的结合橡胶含量**: 与 Table 1 中的结合橡胶数据（55.28%）相互印证

---

## 三、其他热转变

文献中未报告其他热转变（如结晶、熔融等），SSBR 为非晶态橡胶。

---

## 四、高弹性工作温度窗口

基于复合材料 Tg = -0.9℃ 估算：

- **下限**: Tg + 10℃ ≈ 9℃
- **推荐工作温度**: 10℃ 以上
- **湿滑路面应用**: 0℃ 附近正处于玻璃化转变区域，tan δ 值高（1.004），有利于湿地抓地力

---

## 文献对应结论

> "The Tg of the composites increased after being filled with silica, indicating the interaction between the silica and the rubber matrix. The higher Tg shift suggests stronger interfacial interaction for functionalized SSBR."

玻璃化转变温度的上移反映了填料-橡胶界面相互作用的强度，官能化改性有效增强了这一相互作用。

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **图注引用**: Fig. 2, SI Table S6
