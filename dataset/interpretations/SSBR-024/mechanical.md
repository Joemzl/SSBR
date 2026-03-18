---
sample_id: SSBR-024
interpretation_type: mechanical
source_figure: "Table III, Fig. 7-8"
source_doi: "10.1002/app.48243"
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
    value: 18.7
    unit: MPa
    source: "Table III"
  elongation:
    value: 389
    unit: "%"
    source: "Table III"
  stress_100:
    value: 2.4
    unit: MPa
    source: "Table III"
  stress_300:
    value: 10.1
    unit: MPa
    source: "Table III"
  mechanical_source: "Table III"
  
  # ========== Payne 效应数据 ==========
  bound_rubber:
    value: 63.3
    unit: "%"
    source: "Table II"
  tan_delta_7_strain:
    value: 0.098
    unit: "-"
    source: "Table III"
  
  # ========== DMA 数据 ==========
  tg_dma:
    value: -10.0
    unit: "℃"
    source: "Table III"
  tan_delta_0c:
    value: 0.8726
    unit: "-"
    source: "Table III"
  tan_delta_60c:
    value: 0.0859
    unit: "-"
    source: "Table III"
  performance_balance_factor:
    value: 10.16
    unit: "-"
    source: "计算值"
---

# SSBR-024 力学性能解读

## 一、静态力学性能（应力-应变）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100% 定伸应力 | 2.4 | MPa | Table III |
| 300% 定伸应力 | 10.1 | MPa | Table III |
| 拉伸强度 | 18.7 | MPa | Table III |
| 断裂伸长率 | 389 | % | Table III |

### 核心发现

MMP 官能化 SSBR（样本 4，0.8 phr MMP）展现出优异的力学性能：
- 拉伸强度 18.7 MPa，较空白组（14.1 MPa）提升 32.6%
- 伸长率 389%，保持良好的延展性
- 300% 定伸应力 10.1 MPa，模量显著提升

### 与空白组对比

| 样本 | 拉伸强度 (MPa) | 伸长率 (%) | Δ强度 |
|------|---------------|-----------|-------|
| SSBR-024 (MMP) | 18.7 | 389 | +32.6% |
| 空白 SSBR | 14.1 | 426 | 基准 |

## 二、动态力学性能（Payne效应）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 结合橡胶含量 | 63.3 | % | Table II |
| tan δ (7% strain) | 0.098 | - | Table III |

### 核心发现

MMP 官能化显著改善了填料-橡胶界面相互作用：
- 结合橡胶含量 63.3%，较空白组（52.8%）提升 19.9%
- 表明填料分散性和界面结合强度的改善

## 三、动态力学性能（DMA温度扫描）

### 数值数据

| 指标 | 数值 | 单位 | 说明 |
|------|------|------|------|
| Tg (DMA) | -10.0 | ℃ | tan δ 峰值温度 |
| tan δ (0℃) | 0.8726 | - | 湿地抓地力指标 |
| tan δ (60℃) | 0.0859 | - | 滚动阻力指标 |
| 性能平衡因子 | 10.16 | - | 计算值 |

### 核心发现

MMP 官能化实现了优异的动态性能平衡：
- 湿地抓地力（tan δ @ 0℃）提升 15.0%
- 滚动阻力（tan δ @ 60℃）降低 6.2%
- 性能平衡因子 10.16，表明良好的抓地力/滚阻平衡

## 四、综合分析

### 官能化机理

MMP（甲基丙烯酸甲酯）通过巯基-烯点击化学接枝到 SSBR 主链，引入酯基官能团。酯基通过氢键与白炭黑表面硅羟基相互作用，改善界面相容性。

### 性能改善原因

1. **界面相互作用增强**：酯基与白炭黑形成氢键，结合橡胶含量提升
2. **填料分散改善**：减少填料团聚，降低 Payne 效应
3. **动态性能优化**：湿地抓地力提升，滚动阻力降低

### 适用场景

适用于需要综合力学性能和动态性能平衡的轮胎胎面配方，特别是注重湿地安全性的应用。
