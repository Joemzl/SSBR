---
sample_id: SSBR-018
interpretation_type: dsc
source_figure: null
source_doi: 10.1021/acs.iecr.8b05738
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
data:
  tg:
    value: -17.4
    range: null
    unit: ℃
    source: Table 1
  tg_pure_polymer:
    value: -17.4
    range: null
    unit: ℃
    source: Table 1
  thermal_source: Table 1
  working_temp_window:
    value: null
    unit: ℃
    source: ''
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
    data_points: []
    curve_features:
      Tg:
        onset: null
        midpoint: -17.4
        endpoint: null
        unit: °C
        source: "Table 1"
        confidence: 0.95
        note: "α-SSBR 纯聚合物 Tg，文献未提供 DSC 曲线图"
      glass_transition_width:
        value: null
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - temperature: -17.4
          note: "Tg from Table 1 (L1 数据)"
      overall_quality: "acceptable"
      note: "有 Tg 数值 (Table 1) 但无 DSC 曲线图可供估读"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# DSC 热分析解读：SSBR-018


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、玻璃化转变

### 数值数据

| 样品 | Tg (℃) | 来源 |
|------|--------|------|
| α-SSBR | -17.4 | Table 1 |
| 原始 SSBR | -16.5 | Table 1 |
| α,ω-SSBR | -16.5 | Table 1 |
| IC-SSBR | -20.8 | Table 1 |

### 核心发现

1. **Tg 对比**：α-SSBR 的 Tg（-17.4°C）与原始 SSBR（-16.5°C）非常接近
2. **官能化影响**：DPE 衍生物的引入对 Tg 影响很小
3. **特殊情况**：IC-SSBR 的 Tg 最低（-20.8°C），可能与链中官能团改变了分子链运动能力有关

### 分析结论

α-SSBR 的链端氨基官能化对玻璃化转变温度几乎没有影响，这意味着：
- 材料的使用温度范围基本不变
- 官能化不会牺牲低温性能
- 适合轮胎胎面等需要宽工作温度范围的应用

---

## 二、高弹性工作温度窗口

基于 Tg 数据估算：

- **下限**: -17.4 + 10 ≈ **-7°C**
- **上限**: 取决于热稳定性和硫化网络
- **推荐工作温度**: -7°C 以上

---

## 文献来源

- **DOI**: 10.1021/acs.iecr.8b05738
- **图注引用**: Table 1
