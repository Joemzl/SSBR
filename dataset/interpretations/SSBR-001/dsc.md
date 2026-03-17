---
sample_id: SSBR-001
interpretation_type: dsc
source_figure: "Fig. 2, SI Table S6"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-17
updated_at: null

data:
  tg:
    value: -0.9
    range: null
    unit: "℃"
    source: "SI Table S6 (复合材料)"
  tg_pure_polymer:
    value: -24.8
    range: null
    unit: "℃"
    source: "Fig. 2 (纯F-SSBR)"
  thermal_source: "SI Table S6"
  working_temp_window:
    value: "10℃以上"
    unit: "℃"
    source: "基于Tg估算"
  other_transitions:
    value: null
    source: ""
---

# DSC 热分析解读：SSBR-001

> **样本性质**: MPL官能化SSBR（3-巯基丙醇接枝），官能化程度3.6 wt%，白炭黑填充复合材料

## 一、基础信息

- **样本ID**: SSBR-001
- **样品名称**: SSBR-g-MPL70（70 phr 白炭黑填充）
- **官能化试剂**: MPL（3-巯基丙醇）
- **官能化程度**: 3.6 wt%
- **文献DOI**: 10.1039/c9ra02783a

## 二、玻璃化转变

### 数值数据

| 样品状态 | Tg (℃) | 来源 |
|---------|--------|------|
| 纯 F-SSBR-g-MPL | -24.8 | Fig. 2 |
| 复合材料 SSBR-g-MPL70 | -0.9 | SI Table S6 |
| ΔTg (填充效应) | +23.9 | 计算值 |

### 测量条件

- **升温速率**: 10 ℃/min（文献标准条件）
- **气氛**: N₂
- **温度范围**: -80℃ ~ 室温

### 核心发现

1. **纯 F-SSBR-g-MPL 的 Tg (-24.8℃)**: 与空白SSBR相比略有升高，说明官能团的引入对分子链运动有轻微限制
2. **复合材料 Tg (-0.9℃)**: 相比纯聚合物显著升高约24℃，这是白炭黑填充效应的典型表现
3. **界面约束效应**: Tg升高说明填料-橡胶界面相互作用强，限制了链段运动

### 与对照组对比

| 样本 | Tg - 纯聚合物 (℃) | Tg - 复合材料 (℃) | ΔTg |
|------|-------------------|-------------------|-----|
| SSBR-g-MPL | -24.8 | -0.9 | +23.9 |
| 空白 SSBR | -24.5 | -4.7 | +19.8 |

### 分析结论

MPL官能化样品在填充白炭黑后表现出更大的 Tg 上移幅度（ΔTg = 23.9℃ vs 空白组 19.8℃），说明：

1. **更强的界面相互作用**: 羟基官能团与白炭黑表面的硅羟基形成氢键
2. **更多的受限链段**: 界面层橡胶分子链运动受限程度更高
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
