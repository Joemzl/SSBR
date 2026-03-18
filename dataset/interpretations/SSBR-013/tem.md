---
sample_id: SSBR-013
interpretation_type: tem
source_figure: "N/A"
source_doi: "10.1039/c8ra00572a"
skill_used: ssbr-tem-interpretation
created_at: 2026-03-18
updated_at: null

data:
  filler_type: "无（纯橡胶/树脂体系）"
  filler_loading: "N/A"
  dispersion_quality: "N/A"
  morphology_description: "文献未提供TEM图像"
  
  # 模拟快照信息
  simulation_snapshot: true
  simulation_software: "Materials Studio 8.0"
  force_field: "COMPASS"
---

# TEM 形貌解读：SSBR-013

> **样本性质**: 工业官能化 SSBR (F-SSBR, SE0212)，用于石油树脂相容性研究

## 一、基础信息

- **样本ID**: SSBR-013
- **文献中编号**: F-SSBR (SE0212)
- **供应商**: Red Avenue New Materials Group
- **文献DOI**: 10.1039/c8ra00572a

## 二、TEM 表征情况

### 文献未提供 TEM 图像

本文献**没有进行 TEM 表征**，原因：
1. 研究体系为**纯橡胶/树脂共混物**（无纳米填料）
2. 研究重点是**相容性**而非形貌
3. 主要采用**分子动力学模拟**方法

---

## 三、分子动力学模拟结构

### 模拟方法

文献使用 **Materials Studio 8.0** 进行 MD 模拟，采用 **COMPASS 力场**。

### 构建过程 (Fig.2)

1. 在 3D 周期性边界条件下构建立方体晶胞
2. 从 200-400 K 退火 500 ps 消除内应力
3. 几何优化（最速下降、共轭梯度、牛顿法）
4. 298 K 下 NPT 平衡 2000 ps

### 平衡判据

文献使用两个判据确定系统平衡：
1. 密度在平均值附近长时间无大波动
2. 能量在平均值附近保持微小波动

**Fig.3** 显示了 F-SSBR/2# 树脂体系的密度和能量随时间变化曲线，证明系统达到平衡。

---

## 四、F-SSBR 模拟参数

### 构建参数

| 参数 | 值 |
|------|-----|
| 链数 (Nchain) | 10 |
| 重复单元数 (Nunit) | 50 |
| 构建密度 | 1.0 g/cm³ |
| 平衡密度 | 0.94 g/cm³ |

### 优化过程

**Fig.7** 和 **Fig.8** 显示了溶解度参数随链数和重复单元数的变化：
- Nunit = 50 时，溶解度参数收敛
- Nchain = 10 时，溶解度参数收敛

---

## 五、相容性预测

### 模拟快照分析

虽然文献未提供 TEM，但通过 MD 模拟可以预测相分离行为。

**结合能分析 (Table 13)**：

| 体系 | Ebinding (kcal/mol) | 预测相容性 |
|------|---------------------|-----------|
| F-SSBR/1# | 69.83 | ✅ 良好 |
| F-SSBR/2# | 76.85 | ✅ 良好 |
| F-SSBR/3# | **-462.30** | ❌ **可能相分离** |
| F-SSBR/4# | 94.86 | ✅ 最好 |
| F-SSBR/5# | 58.39 | ✅ 中等 |

文献指出：
> "since the F-SSBR/3# resin system has a negative Ebinding, we can predict that microphase separation may appear in this composite."

### 与 cis-BR 的对比 (Fig.12)

文献比较了 F-SSBR 和 cis-BR 与树脂的 R 值：
- F-SSBR 与大多数树脂的 R 值更小
- 说明 **F-SSBR 与树脂的相容性优于 cis-BR**

---

## 六、实验验证

### 溶胀实验

文献通过**溶胀实验**间接验证相容性：
- 交联橡胶在不同溶剂中溶胀
- 溶胀比越高，与溶剂相容性越好

### 相容性验证

模拟和实验得到的相容性趋势一致：
> **1# ≈ 4# > 2# ≈ 5# > 3#**

---

## 七、综合评价

SSBR-013 (F-SSBR) 的形貌/结构特点：
- ⚠️ 文献未提供 TEM 表征
- ✅ MD 模拟提供了分子级结构信息
- ✅ 与 4# 树脂（古马隆树脂-2）结合能最高
- ⚠️ 与 3# 树脂（C5/C9 共聚树脂）可能发生相分离
- ✅ 与树脂的相容性优于 cis-BR

---

## 文献来源

- **DOI**: 10.1039/c8ra00572a
- **数据引用**: Fig.2 (构建过程), Fig.3 (平衡验证), Table 13 (结合能)
