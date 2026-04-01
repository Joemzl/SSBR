---
sample_id: SSBR-065
test_type: dsc
data_completeness:
  tg: true
  second_transition: true
  dma: true
data_source: L1
key_findings:
- SSBR 基体 Tg ≈ -60°C
- TAD 改性后出现第二转变温度区
- 第二转变归属于氢键簇的热行为
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
    note: "DMA测试，SSBR-TAD-5.32显示双转变特征"
    data_points:
      - { x: -80, y: 0.05, confidence: 0.75, source: "L2 DMA曲线估读" }
      - { x: -70, y: 0.15, confidence: 0.75, source: "L2 估读" }
      - { x: -65, y: 0.45, confidence: 0.80, source: "L2 估读" }
      - { x: -60, y: 0.75, confidence: 0.90, source: "L1 Tg≈-60°C (SSBR基体)" }
      - { x: -55, y: 0.50, confidence: 0.80, source: "L2 估读" }
      - { x: -50, y: 0.30, confidence: 0.75, source: "L2 估读" }
      - { x: -40, y: 0.18, confidence: 0.70, source: "L2 估读" }
      - { x: -20, y: 0.12, confidence: 0.70, source: "L2 估读" }
      - { x: 0, y: 0.10, confidence: 0.70, source: "L2 估读" }
      - { x: 25, y: 0.15, confidence: 0.75, source: "L2 第二转变上升" }
      - { x: 50, y: 0.20, confidence: 0.80, source: "L2 第二转变区" }
      - { x: 75, y: 0.18, confidence: 0.75, source: "L2 第二转变区" }
      - { x: 100, y: 0.12, confidence: 0.70, source: "L2 估读" }
      - { x: 130, y: 0.08, confidence: 0.70, source: "L2 估读" }
    curve_features:
      Tg:
        onset: -70
        midpoint: -60
        endpoint: -50
        unit: °C
        source: L1 DMA SSBR基体Tg≈-60°C
      second_transition:
        temperature_range: [25, 100]
        unit: °C
        description: 氢键簇热转变，TAD改性特有
        source: L1 DMA
      dielectric_alpha_star_relaxation:
        temperature_range: [100, 150]
        activation_energy_kJ_mol: 103.8
        description: 氢键多重态重取向和解离动力学
        source: L1 介电弛豫光谱
      glass_transition_width:
        value: 20
        unit: °C
    validation:
      known_points:
        - { x: -60, y: 0.75, reference: "L1 SSBR Tg≈-60°C", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 14
      x_range: [-80, 130]
      y_range: [0.05, 0.75]
      avg_confidence: 0.75
---
# SSBR-065 DSC/DMA 热分析解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本概述

SSBR-065 通过 TAD 点击化学引入脲唑基团，形成氢键网络。热分析用于表征改性前后的热转变行为。

## 玻璃化转变温度

### SSBR 基体 Tg

DMA 测试显示 SSBR 基体的 Tg ≈ -60°C，TAD 改性后基本不变。

这说明：
- 大部分脲唑基团形成多重态和簇
- 未参与氢键的脲唑基团很少
- SSBR 基体的链段运动不受显著影响

### 第二热转变

| 样品 | 第二转变温度区 | 特征 |
|------|----------------|------|
| SSBR | 无 | - |
| SSBR-TAD-2.75 | 出现 | 初步微相分离 |
| SSBR-TAD-3.56 | 室温以上宽区 | 明显微相分离 |
| SSBR-TAD-5.32 | 更高温度 | 高稳定性簇 |

### 转变机理

第二转变归属于：
1. **被困聚合物链段**: 与簇相邻的 SSBR 链段
2. **氢键簇的热行为**: 簇的重排和解离

## 介电弛豫光谱

### α-弛豫

- 归属: SSBR 链的动态玻璃化转变
- 温度: > -75°C 开始出现
- 特征: 热激活过程，峰位随温度升高向高频移动

### α*-弛豫

TAD 改性 SSBR 特有的弛豫过程：

| 特征 | SSBR | SSBR-TAD-2.75 | SSBR-TAD-5.32 |
|------|------|---------------|---------------|
| α*-弛豫 | 无 | 有 | 有 |
| 温度范围 | - | 100-150°C | 100-150°C |
| 表观活化能 | - | 87.2 kJ/mol | 103.8 kJ/mol |

### α*-弛豫机理

α*-弛豫归属于：
- 氢键多重态的重取向动力学
- 氢键的解离动力学

活化能略低于脲唑二聚体解离动力学 (112.5 kJ/mol)，表明重取向和解离动力学共同贡献。

## 形状记忆相关热行为

### 双重形状记忆

| 参数 | 值 | 温度 |
|------|-----|------|
| 形状固定率 Rf | 99% | 室温 |
| 形状恢复率 Rr | 94% | 90°C |

### 三重形状记忆

第二转变区在室温以上的宽温度范围为三重形状记忆提供可能：

| 参数 | 值 |
|------|-----|
| Rf1 (90°C→50°C) | 81% |
| Rf2 (50°C→25°C) | 75% |
| Rr2 (25°C→50°C) | 87% |
| Rr1 (50°C→90°C) | 80% |

Rf1 < Rf2 的原因：50°C 时形成高稳定性簇，小应变下不完全断裂，增加了材料弹性。

## 数据来源

- 文献: Macromol. Rapid Commun. 2017, DOI: 10.1002/marc.201600678
