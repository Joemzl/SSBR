---
sample_id: SSBR-002
interpretation_type: dsc
source_figure: "Fig. 2, SI Table S6"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-17
updated_at: null

data:
  tg:
    value: -2.1
    range: null
    unit: "℃"
    source: "SI Table S6 (复合材料)"
  tg_pure_polymer:
    value: -24.5
    range: null
    unit: "℃"
    source: "Fig. 2 (纯F-SSBR，估读)"
  thermal_source: "SI Table S6"
  working_temp_window:
    value: "8℃以上"
    unit: "℃"
    source: "基于Tg估算"
  other_transitions:
    value: null
    source: ""
---

# DSC 热分析解读：SSBR-002

> **样本性质**: MUA官能化SSBR（11-巯基十一烷酸接枝），官能化程度8.7 wt%，白炭黑填充复合材料

## 一、基础信息

- **样本ID**: SSBR-002
- **样品名称**: SSBR-g-MUA70（70 phr 白炭黑填充）
- **官能化试剂**: MUA（11-巯基十一烷酸）
- **官能化程度**: 8.7 wt%
- **文献DOI**: 10.1039/c9ra02783a

## 二、玻璃化转变

### 数值数据

| 样品状态 | Tg (℃) | 来源 |
|---------|--------|------|
| 纯 F-SSBR-g-MUA | ~-24.5 | Fig. 2 (估读) |
| 复合材料 SSBR-g-MUA70 | -2.1 | SI Table S6 |
| ΔTg (填充效应) | ~+22.4 | 计算值 |

### 测量条件

- **升温速率**: 10 ℃/min
- **气氛**: N₂
- **温度范围**: -80℃ ~ 160℃

### 核心发现

1. **纯 F-SSBR-g-MUA 的 Tg (~-24.5℃)**: 与空白SSBR相近，说明长链烷基的引入部分抵消了羧基极性对Tg的影响

2. **复合材料 Tg (-2.1℃)**: 相比纯聚合物显著升高约22℃，反映白炭黑填充效应

3. **与 MPL 样品对比**: MUA 样品的 Tg 略低于 MPL 样品（-0.9℃），这是因为十一烷基柔性链的引入增加了分子链运动的自由度

### 与对照组对比

| 样本 | Tg - 纯聚合物 (℃) | Tg - 复合材料 (℃) | ΔTg |
|------|-------------------|-------------------|-----|
| SSBR-g-MUA | ~-24.5 | -2.1 | ~+22.4 |
| SSBR-g-MPL | -24.8 | -0.9 | +23.9 |
| 空白 SSBR | -24.5 | -9.0 | +15.5 |

### 分析结论

MUA 官能化样品表现出较大的 Tg 上移幅度（ΔTg ≈ 22.4℃），介于 MPL（23.9℃）和空白组（15.5℃）之间，说明：

1. **双重界面作用**: 羧基同时通过氢键和共价键（酯化反应）与白炭黑结合
2. **柔性链平衡效应**: 十一烷基长链增加了分子柔顺性，部分抵消了界面约束
3. **界面层厚度**: 长烷基链可能形成更厚的界面层

---

## 三、其他热转变

文献中未报告其他热转变（如结晶、熔融等），SSBR 为非晶态橡胶。

---

## 四、高弹性工作温度窗口

基于复合材料 Tg = -2.1℃ 估算：

- **下限**: Tg + 10℃ ≈ 8℃
- **推荐工作温度**: 8℃ 以上
- **湿滑路面应用**: 0℃ 附近处于玻璃化转变区域，tan δ 值高（1.233），有利于湿地抓地力

---

## 文献对应结论

文献指出 MUA 样品的 Tg 变化特点：
> "The Tg of SSBR-g-MUA70 was slightly higher than that of SSBR; its increased range was lower than that of SSBR-g-MPL70. This was because the introduction of **flexible alkyl side chains** partially offset the intermolecular interactions within SSBR-g-MUA."

长链烷基的柔顺性与极性官能团的约束效应形成平衡，使 MUA 样品具有独特的热学特性。

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **图注引用**: Fig. 2, SI Table S6
