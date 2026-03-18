---
sample_id: SSBR-013
interpretation_type: nmr
source_figure: "Table 1"
source_doi: "10.1039/c8ra00572a"
skill_used: ssbr-nmr-interpretation
created_at: 2026-03-18
updated_at: null

data:
  styrene_content:
    value: 25
    unit: "wt%"
    source: "Table 1"
  vinyl_content:
    value: 57
    unit: "mol%"
    source: "Table 1 (ethenyl)"
  cis_1_4_content:
    value: 9
    unit: "wt%"
    source: "Table 1"
  trans_1_4_content:
    value: 9
    unit: "wt%"
    source: "Table 1"
  mn:
    value: null
    unit: "g/mol"
    source: "文献未提供"
  pdi:
    value: null
    source: "文献未提供"
---

# 核磁共振解读：SSBR-013

> **样本性质**: 工业官能化 SSBR (F-SSBR, SE0212)，用于石油树脂相容性研究

## 一、基础信息

- **样本ID**: SSBR-013
- **文献中编号**: F-SSBR (SE0212)
- **供应商**: Red Avenue New Materials Group
- **文献DOI**: 10.1039/c8ra00572a

## 二、链组成

### Table 1 数据

文献 Table 1 给出了两种 SSBR 的链组成：

| 橡胶 | 苯乙烯 (St) | cis-1,4 | trans-1,4 | 乙烯基 (ethenyl) |
|------|------------|---------|-----------|-----------------|
| **F-SSBR (SE0212)** | **25** | **9** | **9** | **57** |
| Oil sucked SSBR (Lanxess 4526) | 26 | 14.5 | 14.5 | 45 |

单位：wt%

### F-SSBR 特点

1. **高乙烯基含量**: 57 wt%（远高于普通 SSBR）
2. **苯乙烯含量**: 25 wt%（典型轮胎用 SSBR 范围）
3. **低 cis/trans-1,4 含量**: 各 9 wt%
4. **官能化**: SE0212 是官能化产品（具体官能团未说明）

### 与 Oil sucked SSBR 对比

| 参数 | F-SSBR | Oil sucked SSBR | 差异 |
|------|--------|-----------------|------|
| 苯乙烯 | 25% | 26% | 相近 |
| 乙烯基 | **57%** | 45% | F-SSBR 更高 |
| cis-1,4 | 9% | 14.5% | F-SSBR 更低 |
| trans-1,4 | 9% | 14.5% | F-SSBR 更低 |

---

## 三、微观结构对相容性的影响

### 橡胶单元与树脂的相互作用

文献通过 MD 模拟研究了橡胶各单元与树脂的非键相互作用 (Enon-bond)：

**Table 11 数据摘要**（每克树脂与每克橡胶单元的 Enon-bond，单位 kcal）：

| 橡胶单元 | 与 1# 树脂 | 与 2# 树脂 | 平均相互作用 |
|---------|-----------|-----------|-------------|
| 苯乙烯 | -0.1117 | -0.0692 | **最强** |
| trans-1,4 | -0.1005 | -0.0605 | 较强 |
| 乙烯基 | -0.0879 | -0.0614 | 中等 |
| cis-1,4 | -0.0941 | -0.0573 | **最弱** |

> 注：Enon-bond 越负，相互作用越强。

### 对 F-SSBR 相容性的影响

F-SSBR 特点分析：
- ✅ **高苯乙烯含量 (25%)**: 苯乙烯单元与树脂相互作用最强 → 有利于相容性
- ✅ **高乙烯基含量 (57%)**: 乙烯基单元与树脂有中等相互作用
- ⚠️ **低 cis-1,4 含量 (9%)**: cis-1,4 与树脂相互作用最弱 → 低含量有利

文献结论：
> "the styrene unit has the strongest interaction with all five resins, while the cis-1,4 unit has the weakest interaction with the resins... we infer that the five resins have better compatibility with F-SSBR compared with cis-polybutadiene (cis-BR) rubber."

---

## 四、NMR 测试方法

### 文献未提供 NMR 谱图

本文献的链组成数据来自**供应商提供的技术规格**，而非实验室 NMR 测试。

### 典型 SSBR NMR 分析方法

对于 SSBR 的 NMR 分析，通常使用以下峰归属：

| 化学位移 (ppm) | 归属 |
|---------------|------|
| 6.5-7.3 | 苯乙烯芳香质子 |
| 5.0-5.6 | 1,4-丁二烯内烯质子 |
| 4.8-5.0 | 1,2-丁二烯（乙烯基）端基质子 |
| 1.0-2.5 | 主链 CH2 和 CH 质子 |

---

## 五、分子量信息

### 文献未提供

本文献未报告 F-SSBR 的分子量数据（Mn、Mw、PDI）。

### 模拟参数

在 MD 模拟中，文献使用了以下参数：
- **链数 (Nchain)**: 10
- **重复单元数 (Nunit)**: 50
- **构建密度**: 1.0 g/cm³
- **平衡密度**: 0.94 g/cm³

---

## 六、综合评价

SSBR-013 (F-SSBR) 的 NMR/组成特点：
- ✅ 苯乙烯含量 25 wt%（典型轮胎用 SSBR）
- ✅ 乙烯基含量 57 wt%（高于普通 SSBR）
- ✅ cis-1,4 含量低（9%），有利于与树脂相容
- ✅ 官能化产品（SE0212）
- ⚠️ 文献未提供 NMR 谱图和分子量数据

---

## 文献来源

- **DOI**: 10.1039/c8ra00572a
- **数据引用**: Table 1 (链组成), Table 11 (单元相互作用)
