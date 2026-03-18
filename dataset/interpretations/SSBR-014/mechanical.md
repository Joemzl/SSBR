---
sample_id: SSBR-014
interpretation_type: mechanical
source_figure: "Table S3"
source_doi: "10.1039/c8ra00572a"
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: null
mechanical_subtypes:
  - stress-strain

data:
  stress_100:
    value: null
    unit: MPa
    source: "文献未提供"
  stress_200:
    value: null
    unit: MPa
    source: "文献未提供"
  stress_300:
    value: null
    unit: MPa
    source: "文献未提供"
  tensile_strength:
    value: null
    unit: MPa
    source: "文献主要关注相容性，未提供力学性能数据"
  elongation:
    value: null
    unit: "%"
    source: "文献主要关注相容性，未提供力学性能数据"
  mechanical_source: "N/A"
  
  note: "本文献主要研究SSBR与石油树脂的相容性，未提供力学测试数据"
---

# 力学性能解读：SSBR-014

> **样本性质**: 工业充油 SSBR (Oil sucked SSBR, Lanxess 4526)，用于石油树脂相容性研究

## 一、基础信息

- **样本ID**: SSBR-014
- **文献中编号**: Oil sucked SSBR (Lanxess 4526)
- **基体**: 充油溶聚苯乙烯-丁二烯橡胶
- **供应商**: Lanxess Chemical Co., Ltd.
- **苯乙烯含量**: 26 wt%
- **乙烯基含量**: 45 mol%
- **文献DOI**: 10.1039/c8ra00572a

## 二、文献研究范围

### 研究目的

本文献主要研究 SSBR 与石油树脂的**相容性**，采用：
1. 分子动力学 (MD) 模拟
2. 溶解度参数实验测试

文献关注的是橡胶与树脂的相容性，而非橡胶的力学性能。

---

## 三、力学相关信息

### 文献未提供的数据

本文献**未测试**以下力学性能：
- ❌ 拉伸强度
- ❌ 断裂伸长率
- ❌ 定伸应力
- ❌ Payne 效应
- ❌ DMA 动态力学

### 文献讨论的相关概念

文献提到相容性对性能的潜在影响：

> "if the petroleum resin exhibits a better miscibility with rubber matrix, then the motion of rubber chains will be confined and hence the damping peak moves to higher temperature and the effective damping temperature range is broadened too."

---

## 四、与 F-SSBR 的对比

### 链组成差异

| 参数 | Oil sucked SSBR | F-SSBR | 影响 |
|------|-----------------|--------|------|
| 苯乙烯 | 26% | 25% | 相近 |
| 乙烯基 | 45% | 57% | Oil SSBR 更低 |
| cis-1,4 | 14.5% | 9% | Oil SSBR 更高 |
| trans-1,4 | 14.5% | 9% | Oil SSBR 更高 |

### 相容性预测

由于 cis-1,4 单元与树脂的相互作用最弱：
- Oil sucked SSBR 的 cis-1,4 含量更高 (14.5% vs 9%)
- 预期与树脂的相容性略低于 F-SSBR

---

## 五、综合评价

SSBR-014 (Oil sucked SSBR) 的力学性能特点：
- ⚠️ 本文献未提供力学测试数据
- ⚠️ 文献主要关注相容性模拟和计算
- ℹ️ 是 Lanxess 公司的工业产品 (4526 型号)
- ℹ️ 相容性趋势与 F-SSBR 类似

如需 Oil sucked SSBR 的力学性能数据，请参考 Lanxess 官方技术数据。

---

## 文献来源

- **DOI**: 10.1039/c8ra00572a
- **文献类型**: 相容性研究（MD 模拟 + 实验验证）
- **数据局限**: 无力学测试数据
