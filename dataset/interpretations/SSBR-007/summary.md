---
# SSBR-007 综合档案
sample_id: SSBR-007
version: "1.0"
created: "2026-03-18"
data_source: "10.1002/app.41182"

# 样本基本信息
sample_info:
  name: "S-SBR (Dycon Chemicals)"
  type: "未官能化工业级 S-SBR"
  application: "热塑性硫化橡胶 (TPV)"
  target_scenario: "汽车、电子、建筑工业领域"

# 高分子结构
polymer_structure:
  base_polymer: "溶聚丁苯橡胶 (S-SBR)"
  styrene_content:
    value: 23.5
    unit: "wt%"
  vinyl_content: null
  molecular_weight: null
  functionalization: null
  supplier: "Dycon Chemicals, Mumbai, India"

# 复合材料体系
composite_system:
  blend_partner: "S-EB-S (Kraton G1657)"
  blend_ratio: "50/50 wt%"
  filler: null
  vulcanization_systems:
    - name: "SEV (半有效硫化)"
      recipe: "ZnO 4, 硬脂酸 1, CBS 1, 硫黄 1 phr"
    - name: "EV (有效硫化)"
      recipe: "ZnO 4, 硬脂酸 1, CBS 1, TMTD 0.5, 硫黄 1 phr"
  processing:
    method: "动态硫化"
    temperature: "160°C"
    rotor_speed: "60 rpm"
    equipment: "Brabender Plastograph EC"

# 关键性能指标
key_properties:
  tensile_strength:
    SEV: "4.9 MPa → 6.3 MPa (再加工后)"
    EV: "4.8 MPa → 4.4 MPa (再加工后)"
  elongation_at_break:
    SEV: "672%"
    EV: "533%"
  hardness:
    SEV: "52 Shore A"
    EV: "55 Shore A"
  crosslink_density:
    SEV: "~7.1e-5 mol/mL → ~7.9e-5 mol/mL"
    EV: "~8.5e-5 mol/mL → ~8.6e-5 mol/mL"

# 形态学特征
morphology:
  type: "共连续形态"
  characterization: ["SEM", "AFM"]
  key_observation: "SEV 体系含拉长橡胶粒子，再加工后形成部分液滴形态"

# 文献信息
literature:
  title: "Meticulous Analysis and Consequences of Microstructure Changes on Melt Rheology and Dynamic Viscoelasticity of Thermoplastic Vulcanizates upon Reprocessing"
  authors: "Dey P, Naskar K, Nando GB, et al."
  journal: "Journal of Applied Polymer Science"
  year: 2014
  volume: 131
  issue: 23
  pages: 41182
  doi: "10.1002/app.41182"

# RAG 检索关键词
rag_keywords:
  - "热塑性硫化橡胶"
  - "TPV"
  - "动态硫化"
  - "再加工性"
  - "共连续形态"
  - "S-EB-S/S-SBR 共混"
  - "流变性能"
  - "蠕变"
  - "应力松弛"
  - "交联密度"
---

## 样本概述

SSBR-007 是一种未官能化的工业级溶聚丁苯橡胶（S-SBR），来源于印度 Dycon Chemicals 公司。该样本被用于与 S-EB-S（Kraton G1657）制备热塑性硫化橡胶（TPV）的研究中。

### 研究背景

热塑性硫化橡胶（TPV）是一类特殊的弹性体合金，通过动态硫化技术在热塑性基体中选择性交联弹性体相。这种材料兼具橡胶的弹性和热塑性塑料的可加工性，广泛应用于汽车、电子和建筑领域。

### 核心创新点

1. **硫化体系比较**: 系统对比了 SEV 和 EV 硫化体系对 TPV 性能的影响
2. **再加工性研究**: 揭示了不同硫化体系 TPV 的再加工行为差异
3. **形态-性能关联**: 建立了微观结构与宏观性能的直接联系

## 制备工艺

### 原材料

| 组分 | 规格 | 用量 |
|------|------|------|
| S-SBR | 苯乙烯 23.5 wt% | 50 wt% |
| S-EB-S | Kraton G1657, PS 13% | 50 wt% |
| ZnO | 锌含量 82% | 4 phr |
| 硬脂酸 | - | 1 phr |
| CBS | N-环己基-2-苯并噻唑次磺酰胺 | 1 phr |
| TMTD | 四甲基秋兰姆二硫化物 (仅 EV) | 0.5 phr |
| 硫黄 | - | 1 phr |

### 加工条件

- **混合设备**: Brabender Plastograph EC
- **混合温度**: 160°C
- **转子转速**: 60 rpm
- **加工顺序**: S-EB-S (2min) → S-SBR (1min) → ZnO/硬脂酸 → 硫黄/促进剂
- **压模条件**: 160°C, 5 MPa, 4 min

## 性能表现

### 力学性能对比

| 性能指标 | SEV (SST 1) | EV (SST 2) |
|----------|-------------|------------|
| 拉伸强度 (MPa) | 4.9 | 4.8 |
| 断裂伸长率 (%) | **672** | 533 |
| 100% 模量 (MPa) | 0.9 | 1.1 |
| 硬度 (Shore A) | 52 | 55 |

**关键发现**: SEV 体系的断裂伸长率比 EV 体系高 26%，这归因于二硫键/多硫键结构允许更大的分子链滑移。

### 再加工性能

| 性能指标 | SEV 初始 → 再加工 | EV 初始 → 再加工 |
|----------|-------------------|------------------|
| 拉伸强度 | 4.9 → **6.3 MPa** (+29%) | 4.8 → 4.4 MPa (-8%) |
| 断裂伸长率 | 672 → 666% | 533 → 510% |
| 交联密度变化 | +0.8×10⁻⁵ mol/mL | +0.1×10⁻⁵ mol/mL |

**关键发现**: SEV 体系在再加工后性能提升，这是由于后固化效应超过了降解效应。

### 流变性能

- **复数模量**: 随频率增加而增加，EV 体系 > SEV 体系
- **复数粘度**: 呈假塑性行为，交联密度越高初始粘度越高
- **Payne 类效应**: 在应变扫描中观察到，与交联密度成正比

### 动态粘弹性

- **蠕变柔量**: SEV 体系再加工后降低 20%，抗蠕变性能提升
- **应力松弛**: SEV 体系再加工后模量增加，弹性恢复能力提升

## 形态学特征

### SEM/AFM 观察

| 体系 | 初始形态 | 再加工后形态 |
|------|----------|--------------|
| SEV | 共连续 + 拉长粒子 | 共连续 + 液滴形态 |
| EV | 共连续 | 共连续（无变化）|

### 形态演变机理

1. **SEV 体系**: 二硫键/多硫键的键能较低 → 弹性网络弹性较低 → 再加工剪切力可使拉长粒子断裂成液滴
2. **EV 体系**: 单硫键的键能较高 → 弹性网络弹性较高 → 再加工剪切力不足以改变形态

## 应用建议

### 适用场景

1. **需要良好再加工性的 TPV 应用**: 选用 SEV 硫化体系
2. **需要高弹性和形态稳定性**: 选用 EV 硫化体系
3. **汽车密封件**: SEV 体系的高伸长率有利于密封性能

### 配方设计参考

- 若追求高伸长率和再加工性，使用 SEV 体系（低硫高促）
- 若追求高模量和形态稳定性，使用 EV 体系（高促或无硫）
- S-EB-S/S-SBR 体系的溶解度参数匹配是成功制备 TPV 的基础

## 数据完整性

| 文档 | 数据质量 | 主要内容 |
|------|----------|----------|
| mechanical.md | L2 | 拉伸、流变、DMA 数据完整 |
| dsc.md | N/A | 无 DSC 数据 |
| nmr.md | N/A | 无 NMR 数据 |
| tem.md | L2 | SEM/AFM 形态学数据完整 |

## 参考文献

Dey P, Naskar K, Nando GB, et al. Meticulous Analysis and Consequences of Microstructure Changes on Melt Rheology and Dynamic Viscoelasticity of Thermoplastic Vulcanizates upon Reprocessing[J]. Journal of Applied Polymer Science, 2014, 131(23): 41182.
