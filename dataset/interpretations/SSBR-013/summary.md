---
sample_id: SSBR-013
doi: 10.1039/c8ra00572a
polymer_type: SSBR
functionalization:
  is_functionalized: true
  type: unknown
  reagent: null
  functional_group: null
  degree: null
  method: null
filler_system: null
application: null
data_completeness:
  mechanical: true
  dsc: true
  nmr: true
  tem: true
keywords: []
created_at: 2026-03-18
updated_at: '2026-03-19'
---
# 综合档案：SSBR-013

> **一句话总结**: 工业官能化 SSBR (F-SSBR, SE0212) 与古马隆树脂相容性最佳，高乙烯基含量 (57%) 和苯乙烯单元的强相互作用有助于提升与石油树脂的相容性。

## 一、样本概述

| 属性 | 值 |
|------|-----|
| **样本ID** | SSBR-013 |
| **文献编号** | F-SSBR (SE0212) |
| **DOI** | 10.1039/c8ra00572a |
| **类型** | 工业官能化 SSBR |
| **供应商** | Red Avenue New Materials Group |
| **苯乙烯含量** | 25 wt% |
| **乙烯基含量** | 57 mol%（高） |
| **cis-1,4 含量** | 9 wt% |
| **trans-1,4 含量** | 9 wt% |
| **应用场景** | 轮胎用SSBR与石油树脂复合体系 |

## 二、研究背景

### 2.1 文献研究目的

本文献研究 SSBR 与石油树脂的**相容性**，采用：
- 分子动力学 (MD) 模拟
- 溶解度参数实验测试

### 2.2 石油树脂的作用

> "Due to a favorable compatibility between petroleum resins and elastomers, they are commonly regarded as tackifying resins and added to elastomers to improve surface bonding strength. Besides, C9 petroleum resin also has a reinforcement effect to vulcanized rubber."

石油树脂在橡胶中的作用：
- **增粘**: 提高表面粘合强度
- **增强**: C9 树脂中的刚性芳环和活性双键
- **软化**: 提高链段运动性

## 三、核心发现

### 3.1 相容性排序

实验和模拟一致得到相容性顺序：

| 排序 | 树脂 | 说明 |
|------|------|------|
| 1 | 1# 古马隆树脂-1 | 最佳 |
| 2 | 4# 古马隆树脂-2 | 最佳 |
| 3 | 2# α-甲基苯乙烯树脂 | 中等 |
| 4 | 5# C9 石油树脂 | 中等 |
| 5 | 3# C5/C9 共聚树脂 | **最差（可能相分离）** |

### 3.2 橡胶单元的相互作用

文献发现不同橡胶单元与树脂的相互作用强度不同：

| 橡胶单元 | 与树脂相互作用 |
|---------|---------------|
| 苯乙烯单元 | **最强** |
| trans-1,4 单元 | 较强 |
| 乙烯基单元 | 中等 |
| cis-1,4 单元 | **最弱** |

结论：
> "the five resins have better compatibility with F-SSBR compared with cis-polybutadiene (cis-BR) rubber"

### 3.3 F-SSBR 的优势

F-SSBR (SSBR-013) 与树脂相容性好的原因：
- ✅ **高苯乙烯含量 (25%)**: 苯乙烯单元与树脂相互作用最强
- ✅ **低 cis-1,4 含量 (9%)**: cis-1,4 与树脂相互作用最弱，低含量有利
- ✅ **官能化**: SE0212 是官能化产品

## 四、关键参数

### 4.1 溶解度参数

| 来源 | δ (J/cm³)^0.5 |
|------|---------------|
| 实验 (Fig.4) | 17.22 |
| 模拟 (Table 10) | 15.71 |

### 4.2 结合能

| 体系 | Ebinding (kcal/mol) | 相容性 |
|------|---------------------|--------|
| F-SSBR/4# | **94.86** | **最好** |
| F-SSBR/2# | 76.85 | 较好 |
| F-SSBR/1# | 69.83 | 较好 |
| F-SSBR/5# | 58.39 | 中等 |
| F-SSBR/3# | **-462.30** | **差（相分离）** |

### 4.3 自扩散系数

添加树脂后，F-SSBR 链的运动性增加：
> "petroleum resin softens the rubber matrix and acts like small molecule lubricants"

## 五、应用指导

### 5.1 树脂选择建议

对于 F-SSBR (SSBR-013)：
- ✅ **推荐**: 古马隆树脂 (1#, 4#)
- ⚠️ **可用**: α-甲基苯乙烯树脂 (2#), C9 树脂 (5#)
- ❌ **避免**: C5/C9 共聚树脂 (3#)

### 5.2 预期效果

良好相容性的影响：
- 阻尼峰向高温移动
- 有效阻尼温度范围展宽
- 链段运动受限

## 六、数据可靠性评估

| 数据类型 | 来源 | 可靠性 |
|---------|------|--------|
| 链组成 | Table 1 | L1 (供应商数据) |
| 溶解度参数 (实验) | Fig.4 | L1 |
| 溶解度参数 (模拟) | Table 10 | L2 |
| 结合能 | Table 13 | L2 (模拟) |
| 相容性排序 | Fig.9 | L1/L2 |

## 七、文献局限性

本文献**未提供**以下数据：
- ❌ 力学性能（拉伸、撕裂等）
- ❌ TEM 形貌表征
- ❌ DSC 测得的 Tg 数值
- ❌ NMR 谱图
- ❌ 分子量（Mn、Mw）

## 八、相关样本

| 样本ID | 关系 | 说明 |
|--------|------|------|
| SSBR-014 | 同源文献 | Oil sucked SSBR (Lanxess 4526) |

## 九、文献来源

- **完整引用**: Guo Y, Liu J, Lu Y, et al. A combined molecular dynamics simulation and experimental method to study the compatibility between elastomers and resins[J]. RSC Advances, 2018, 8(25): 14401-14413.
- **DOI**: 10.1039/c8ra00572a
- **研究方法**: MD 模拟 + 溶解度参数实验
