---
sample_id: SSBR-013
interpretation_type: mechanical
source_figure: "Table S3, Fig.11"
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
  
  # 该样本无力学数据，文献主要关注相容性模拟
  note: "本文献主要研究SSBR与石油树脂的相容性，未提供力学测试数据"
---

# 力学性能解读：SSBR-013

> **样本性质**: 工业官能化 SSBR (F-SSBR, SE0212)，用于石油树脂相容性研究

## 一、基础信息

- **样本ID**: SSBR-013
- **文献中编号**: F-SSBR (SE0212)
- **基体**: 官能化溶聚苯乙烯-丁二烯橡胶
- **供应商**: Red Avenue New Materials Group
- **苯乙烯含量**: 25 wt%
- **乙烯基含量**: 57 mol%
- **文献DOI**: 10.1039/c8ra00572a

## 二、文献研究范围

### 研究目的

本文献主要研究 SSBR 与石油树脂的**相容性**，采用：
1. 分子动力学 (MD) 模拟
2. 溶解度参数实验测试

### 研究内容

> "In order to have an insight into structural influence on compatibility, we chose five commonly used petroleum resins and two industrial rubbers to find the most suitable resin for one specific rubber."

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

### 文献提供的相关信息

文献讨论了相容性对力学性能的**潜在影响**：

> "if the petroleum resin exhibits a better miscibility with rubber matrix, then the motion of rubber chains will be confined and hence the damping peak moves to higher temperature and the effective damping temperature range is broadened too."

这表明良好的相容性可能导致：
- 橡胶链运动受限
- 阻尼峰向高温移动
- 有效阻尼温度范围展宽

---

## 四、相容性与力学性能的关联

### 结合能与相容性

文献通过结合能 (Ebinding) 评估相容性：

| 体系 | Ebinding (kcal/mol) | 相容性 |
|------|---------------------|--------|
| F-SSBR/4# | 94.86 | 最好 |
| F-SSBR/1# | 69.83 | 较好 |
| F-SSBR/5# | 58.39 | 中等 |
| F-SSBR/2# | 76.85 | 较好 |
| F-SSBR/3# | -462.30 | 差（可能相分离）|

### 相容性对性能的预期影响

根据文献理论分析：
- **高相容性** → 树脂分子与橡胶链均匀混合 → 链段运动受限 → 可能提高硬度和模量
- **低相容性** → 相分离 → 力学性能下降

---

## 五、综合评价

SSBR-013 (F-SSBR) 的力学性能特点：
- ⚠️ 本文献未提供力学测试数据
- ⚠️ 文献主要关注相容性模拟和计算
- ℹ️ F-SSBR 与 4# 树脂（古马隆树脂-2）相容性最佳
- ℹ️ F-SSBR 与 3# 树脂（C5/C9 共聚树脂）相容性最差

如需 F-SSBR 的力学性能数据，请参考其他文献或供应商技术数据。

---

## 文献来源

- **DOI**: 10.1039/c8ra00572a
- **文献类型**: 相容性研究（MD 模拟 + 实验验证）
- **数据局限**: 无力学测试数据
