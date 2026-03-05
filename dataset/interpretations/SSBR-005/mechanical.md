# SSBR-005 力学性能解读

```yaml
sample_id: SSBR-005
interpretation_type: mechanical
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Fig. 2, Table 5"

mechanical_properties:
  stress_100:
    value: null
    unit: MPa
    confidence: null
  stress_200:
    value: null
    unit: MPa
    confidence: null
  stress_300:
    value: null
    unit: MPa
    confidence: null
  tensile_strength:
    value: null
    unit: MPa
    confidence: null
  elongation_at_break:
    value: null
    unit: "%"
    confidence: null

payne_effect:
  delta_G_prime:
    value: null
    unit: MPa
    confidence: medium
    note: "从 Fig. 2 可见 M0 的 Payne 效应最大"
  G_prime_0:
    value: null
    unit: MPa
    confidence: null
  G_prime_inf:
    value: null
    unit: MPa
    confidence: null
  activation_energy:
    value: 11.3
    unit: "kJ/mol"
    confidence: high

dma_properties:
  tan_delta_max:
    value: 1.07
    confidence: high
  tan_delta_0C:
    value: null
    confidence: null
  tan_delta_60C:
    value: null
    confidence: null
```

## 样本基本信息

- **样本编号**: SSBR-005（文献中标记为 M0）
- **官能团类型**: 无（空白未官能化 SSBR）
- **功能基团**: -
- **填料体系**: 白炭黑 (50 phr) + TESPT 偶联剂 (4 phr)
- **文献来源**: Qu et al., RSC Advances, 2014

## 力学性能数据

### 应力-应变数据

文献主要聚焦于动态力学性能，未提供完整的静态拉伸数据。

### Payne 效应分析

| 参数 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 活化能 Ea | 11.3 | kJ/mol | 高 |
| Payne 效应幅度 | 最大 | - | 中（图谱读取）|

**关键发现**：
- M0（空白 SSBR）的 Payne 效应幅度在系列样品中最大
- 活化能 Ea = 11.3 kJ/mol，是系列中最低的
- 表明填料网络不稳定，易被应变破坏

### DMA 分析

| 指标 | 数值 | 置信度 |
|------|------|--------|
| tan δmax | 1.07 | 高 |
| Tg (DMA) | -5.9℃ | 高 |

## 性能解读

### 作为对照样品的意义

SSBR-005 是系列研究的空白对照样品，用于评估 3-巯基丙酸官能化的效果：

1. **最大 Payne 效应**: 填料分散性差，白炭黑团聚严重
2. **最低活化能**: 填料网络结构不稳定
3. **最低 tan δmax**: 能量耗散能力最低

### 机理解释

未官能化 SSBR 与白炭黑界面作用弱：
- 白炭黑表面极性高（Si-OH），SSBR 非极性
- 表面能差异大导致填料自聚集
- 形成不稳定的填料-填料网络

## 数据来源与置信度说明

- 活化能数据来自文献 Table 5
- DMA 数据来自 Table 6
- 置信度"高"表示直接从表格读取
