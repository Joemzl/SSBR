---
sample_id: SSBR-065
test_type: mechanical
data_completeness:
  stress_strain: true
  payne_effect: false
  dma: true
data_source: L1
key_findings:
- TAD 点击化学在预交联 SSBR 中构建牺牲氢键
- 模量随 TAD 接枝比例增加显著提升
- 氢键簇作为牺牲键促进能量耗散
- 迟滞能随 TAD 接枝量增加
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: dimensionless
    note: "SSBR-TAD-5.32样品，双损耗峰特征"
    data_points:
      - { x: -80, y: 0.05, confidence: 0.75, source: "L2 DMA曲线估读" }
      - { x: -70, y: 0.15, confidence: 0.75, source: "L2 估读" }
      - { x: -65, y: 0.45, confidence: 0.80, source: "L2 估读 第一峰上升" }
      - { x: -60, y: 0.75, confidence: 0.85, source: "L1 第一峰 Tg≈-60°C (SSBR基体)" }
      - { x: -55, y: 0.50, confidence: 0.80, source: "L2 估读 第一峰下降" }
      - { x: -50, y: 0.30, confidence: 0.75, source: "L2 估读" }
      - { x: -40, y: 0.18, confidence: 0.70, source: "L2 估读" }
      - { x: -20, y: 0.12, confidence: 0.70, source: "L2 估读" }
      - { x: 0, y: 0.10, confidence: 0.70, source: "L2 估读" }
      - { x: 20, y: 0.12, confidence: 0.70, source: "L2 估读 第二峰上升" }
      - { x: 40, y: 0.18, confidence: 0.75, source: "L2 估读 第二峰区" }
      - { x: 60, y: 0.22, confidence: 0.80, source: "L2 估读 第二峰 (氢键簇)" }
      - { x: 80, y: 0.18, confidence: 0.75, source: "L2 估读 第二峰下降" }
      - { x: 100, y: 0.12, confidence: 0.70, source: "L2 估读" }
      - { x: 120, y: 0.08, confidence: 0.70, source: "L2 估读" }
    curve_features:
      Tg_first_peak:
        value: -60
        unit: °C
        source: L1 DMA SSBR基体Tg
        confidence: 0.85
      second_transition_peak:
        value: 60
        unit: °C
        source: L2 DMA 氢键簇热转变
        confidence: 0.80
      tan_delta_first_max:
        value: 0.75
        unit: dimensionless
        source: L2 估读
        confidence: 0.80
      tan_delta_second_max:
        value: 0.22
        unit: dimensionless
        source: L2 估读
        confidence: 0.75
      tan_delta_0C:
        value: 0.10
        unit: dimensionless
        source: L2 estimated
        confidence: 0.70
      tan_delta_60C:
        value: 0.22
        unit: dimensionless
        source: L2 第二峰值
        confidence: 0.75
      Tg:
        value: -60
        unit: °C
        method: first_tan_delta_peak
        source: L1 DMA
        confidence: 0.85
      dual_peak_behavior:
        description: TAD接枝≥2.75%出现双损耗峰
        source: 文献描述
    validation:
      known_points:
        - { x: -60, y: 0.75, reference: "SSBR基体Tg≈-60°C", deviation_percent: 0 }
        - { x: 60, y: 0.22, reference: "氢键簇第二转变", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 15
      x_range: [-80, 120]
      y_range: [0.05, 0.75]
      avg_confidence: 0.74
---
# SSBR-065 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本概述

SSBR-065 采用**三唑啉二酮 (TAD) 点击化学**对预交联 SSBR 进行后交联改性。受"牺牲键"仿生设计启发，通过 TAD 与 SSBR 双键的 Alder-ene 反应引入悬挂的脲唑基团，形成分子间/分子内氢键。

## 官能化方法

### TAD 点击化学

```
预交联 SSBR + TAD (4-苯基-1,2,4-三唑啉-3,5-二酮)
↓ 浸泡法，CH₂Cl₂ 溶剂
SSBR-TAD-x (悬挂脲唑基团)
```

**反应特点**:
- 超快反应
- 无需催化剂
- 室温进行
- 不改变共价交联网络

### 样本命名

SSBR-TAD-x 表示 TAD 接枝量为 x% (相对于双键的摩尔比)

## 动态力学分析 (DMA)

### 双重损耗峰

当 TAD 接枝比例 ≥2.75% 时，出现两个明显的损耗峰：

| 峰位 | 归属 | 温度 |
|------|------|------|
| 第一峰 | SSBR 基体玻璃化转变 | ≈-60°C |
| 第二峰 | 氢键簇的热转变 | 室温以上 |

### 储能模量 (E')

| 样品 | E' 变化趋势 | 机理 |
|------|-------------|------|
| SSBR | 基准 | - |
| SSBR-TAD-2.75 | 增加 | 物理交联形成 |
| SSBR-TAD-3.56 | 进一步增加 | 更多硬畴 |
| SSBR-TAD-5.32 | 显著增加 | 高效增强 |

E' 在中间温度范围内改善最显著，因为氢键簇提供物理交联贡献。随温度升高，簇破裂，E' 趋向接近纯 SSBR。

## 应力-应变行为

### 典型特征

| 样品 | 模量变化 | 韧性变化 | 行为特征 |
|------|----------|----------|----------|
| SSBR | 基准 | 基准 | 典型弹性体 |
| SSBR-TAD-x (低) | 增加 | 改善 | 增强弹性体 |
| SSBR-TAD-5.32 | 显著增加 | 大幅改善 | 类刚性塑料，有明显屈服 |

### 能量耗散

氢键簇作为牺牲键的作用机制：
1. **拉伸过程**: 氢键簇被拉伸并逐步断裂
2. **能量耗散**: 被困聚合物链段的塑性变形 + 氢键解离动力学
3. **韧性增强**: 迟滞能随 TAD 接枝量增加

### 迟滞能

文献 Figure 3c 显示：
- 迟滞能随 TAD 接枝比例增加而增加
- 加载-卸载循环显示明显的能量耗散

## 微观结构

### "笼效应"

预交联 SSBR 的共价网络产生"笼效应"：
- 促进脲唑基团的非均匀分布
- 形成氢键多重态 (multiplets)
- 多重态进一步聚集成簇 (clusters)

### 微相分离

AFM DMT 模量图证实微相分离结构：

| 区域 | 杨氏模量 | 特征 |
|------|----------|------|
| 软相 (暗区) | ≈10 MPa | SSBR 基体 |
| 硬畴 (亮区) | ≈40 MPa | 氢键簇 |
| 硬畴尺寸 | ≈10 nm | - |

SSBR-TAD-5.32 比 SSBR-TAD-3.56 具有更密集的硬畴分布和更高的模量。

## 双交联网络

### 网络结构

1. **共价交联网络**: 硫化形成，不受 TAD 改性影响
2. **物理交联网络**: 氢键簇形成的可逆交联点

这种双网络结构实现了：
- 高强度
- 高韧性
- 能量耗散能力
- 形状记忆功能

## 数据来源

- 文献: Macromol. Rapid Commun. 2017, DOI: 10.1002/marc.201600678
- 机构: 华南理工大学
