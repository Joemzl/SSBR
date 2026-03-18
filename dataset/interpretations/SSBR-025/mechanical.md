---
sample_id: SSBR-025
interpretation_type: mechanical
source_figure: "Table 2, Table 3"
source_doi: "10.1002/app.48696"
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: null
mechanical_subtypes:
  - stress-strain
  - payne
  - dma

data:
  # ========== 应力-应变数据 ==========
  tensile_strength:
    value: 19.2
    unit: MPa
    source: "Table 3"
  elongation:
    value: 375
    unit: "%"
    source: "Table 3"
  stress_100:
    value: 2.6
    unit: MPa
    source: "Table 3"
  stress_300:
    value: 11.3
    unit: MPa
    source: "Table 3"
  mechanical_source: "Table 3"
  
  # ========== Payne 效应数据 ==========
  bound_rubber:
    value: 68.5
    unit: "%"
    source: "Table 2"
  
  # ========== DMA 数据 ==========
  tg_dma:
    value: -8.5
    unit: "℃"
    source: "Table 3"
  tan_delta_0c:
    value: 0.9245
    unit: "-"
    source: "Table 3"
  tan_delta_60c:
    value: 0.0782
    unit: "-"
    source: "Table 3"
  performance_balance_factor:
    value: 11.82
    unit: "-"
    source: "计算值"
---

# SSBR-025 力学性能解读

## 一、静态力学性能（应力-应变）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100% 定伸应力 | 2.6 | MPa | Table 3 |
| 300% 定伸应力 | 11.3 | MPa | Table 3 |
| 拉伸强度 | 19.2 | MPa | Table 3 |
| 断裂伸长率 | 375 | % | Table 3 |

### 核心发现

DMPA（丙胺二甲氧基硅烷）官能化 SSBR 展现出优异的力学性能：
- 拉伸强度 19.2 MPa，较空白组显著提升
- 300% 定伸应力 11.3 MPa，模量大幅提高
- 伸长率 375%，保持良好的延展性

### 性能改善机理

DMPA 引入的硅烷基团可与白炭黑表面硅羟基形成共价键（Si-O-Si），建立强界面结合，同时氨基可与硅羟基形成氢键，实现双重界面作用。

## 二、动态力学性能（Payne效应）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 结合橡胶含量 | 68.5 | % | Table 2 |

### 核心发现

DMPA 官能化显著提升了结合橡胶含量：
- 68.5% 的结合橡胶含量表明强界面相互作用
- 填料分散性改善，Payne 效应降低

## 三、动态力学性能（DMA温度扫描）

### 数值数据

| 指标 | 数值 | 单位 | 说明 |
|------|------|------|------|
| Tg (DMA) | -8.5 | ℃ | tan δ 峰值温度 |
| tan δ (0℃) | 0.9245 | - | 湿地抓地力指标 |
| tan δ (60℃) | 0.0782 | - | 滚动阻力指标 |
| 性能平衡因子 | 11.82 | - | 计算值 |

### 核心发现

DMPA 官能化实现了出色的动态性能平衡：
- 性能平衡因子高达 11.82
- 湿地抓地力显著提升
- 滚动阻力有效降低

## 四、综合分析

### 官能化机理

DMPA（丙胺二甲氧基硅烷）通过巯基-烯点击化学接枝到 SSBR 主链，引入硅烷和氨基双官能团：
- 硅烷基团与白炭黑形成 Si-O-Si 共价键
- 氨基与硅羟基形成氢键
- 双重界面作用机制增强界面结合

### 适用场景

适用于需要强界面结合和优异动态性能的高性能轮胎配方。
