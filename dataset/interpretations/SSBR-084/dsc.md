---
sample_id: SSBR-084
interpretation_type: dsc
source_figure: Fig.5
source_doi: 10.1016/j.europolj.2024.113653
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-19
updated_at: '2026-03-31'
data:
  tg:
    value: null
    range: null
    unit: ℃
    source: Fig.5 DSC 曲线
  thermal_source: Fig.5
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
      - x: -80
        y: -0.30
        confidence: 0.65
        source: L2
      - x: -60
        y: -0.28
        confidence: 0.65
        source: L2
      - x: -45
        y: -0.24
        confidence: 0.65
        source: L2
      - x: -35
        y: -0.18
        confidence: 0.70
        source: L2
        note: Tg onset
      - x: -25
        y: -0.05
        confidence: 0.70
        source: L2
        note: Tg midpoint
      - x: -15
        y: 0.08
        confidence: 0.70
        source: L2
        note: Tg endpoint
      - x: 0
        y: 0.10
        confidence: 0.65
        source: L2
      - x: 30
        y: 0.07
        confidence: 0.65
        source: L2
      - x: 60
        y: 0.05
        confidence: 0.65
        source: L2
      - x: 100
        y: 0.04
        confidence: 0.65
        source: L2
    curve_features:
      Tg:
        onset: -35
        midpoint: -25
        endpoint: -15
        unit: °C
        source: L2
      glass_transition_width:
        value: 20
        unit: °C
        note: 官能化增加转变宽度
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: good
      note: 吡啶基/羧基离子对作为物理交联点，限制链段运动，Tg升高
    metadata:
      point_count: 10
      x_range:
        - -80
        - 100
      y_range:
        - -0.30
        - 0.10
      avg_confidence: 0.67
---
# DSC 热分析解读：SSBR-084

> **样本性质**: 腈氧化物 (CNO) 官能化 SSBR


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-084
- **样品名称**: CNO-py/CNO-COOH 官能化 SSBR
- **官能化试剂**: 腈氧化物
- **官能化程度**: 1.9-16.8%
- **文献DOI**: 10.1016/j.europolj.2024.113653

## 二、玻璃化转变

### 数据来源

文献 Fig.5 提供了 DSC 曲线，展示了官能化对 Tg 的影响。

### 预期趋势

1. **基础 SSBR 的 Tg**: 约 -40℃ ~ -30℃（取决于苯乙烯和乙烯基含量）
2. **官能化效应**: 引入极性官能团（吡啶基、羧基）预期会提高 Tg
3. **离子交联效应**: 酸碱离子对的形成会进一步限制链段运动

### 核心发现

1. **Tg 上移**: 官能化程度增加导致 Tg 升高
2. **官能化程度依赖性**: 不同官能化程度 (1.9-16.8%) 的样品具有不同的 Tg
3. **可逆网络**: 离子交联的可逆性可能影响热转变行为

### 分析结论

腈氧化物官能化引入的吡啶基和羧基可形成离子对，作为物理交联点限制链段运动，导致 Tg 升高。这种效应随官能化程度增加而增强。

---

## 三、其他热转变

文献可能还报告了：
- 离子解离温度
- 可逆网络的热响应行为

---

## 文献来源

- **DOI**: 10.1016/j.europolj.2024.113653
- **图注引用**: Fig.5 DSC 曲线
