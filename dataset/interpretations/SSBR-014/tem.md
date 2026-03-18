---
sample_id: SSBR-014
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
  
  simulation_snapshot: true
  simulation_software: "Materials Studio 8.0"
  force_field: "COMPASS"
---

# TEM 形貌解读：SSBR-014

> **样本性质**: 工业充油 SSBR (Oil sucked SSBR, Lanxess 4526)，用于石油树脂相容性研究

## 一、基础信息

- **样本ID**: SSBR-014
- **文献中编号**: Oil sucked SSBR (Lanxess 4526)
- **供应商**: Lanxess Chemical Co., Ltd.
- **文献DOI**: 10.1039/c8ra00572a

## 二、TEM 表征情况

### 文献未提供 TEM 图像

本文献**没有进行 TEM 表征**，原因与 SSBR-013 相同：
1. 研究体系为**纯橡胶/树脂共混物**（无纳米填料）
2. 研究重点是**相容性**而非形貌
3. 主要采用**分子动力学模拟**方法

---

## 三、分子动力学模拟结构

### 模拟方法

文献使用 **Materials Studio 8.0** 进行 MD 模拟，采用 **COMPASS 力场**。

### Oil sucked SSBR 模拟参数

| 参数 | 值 |
|------|-----|
| 链数 (Nchain) | 10 |
| 重复单元数 (Nunit) | 50 |
| 构建密度 | 1.0 g/cm³ |
| 平衡密度 | 0.95 g/cm³ |

### 与 F-SSBR 的密度对比

| 样本 | 构建密度 | 平衡密度 |
|------|---------|---------|
| F-SSBR | 1.0 g/cm³ | 0.94 g/cm³ |
| Oil sucked SSBR | 1.0 g/cm³ | **0.95 g/cm³** |

Oil sucked SSBR 的平衡密度略高，可能与其较高的 cis/trans-1,4 含量有关。

---

## 四、相容性预测

### 与树脂的 R 值对比

**Fig.9** 显示两种 SSBR 与五种树脂的 R 值：

两种 SSBR 的相容性排序**相同**：
> **1# ≈ 4# > 2# ≈ 5# > 3#**

### 文献结论

虽然两种 SSBR 与树脂的相容性趋势相同，但：
- F-SSBR 与树脂的相容性略优于 Oil sucked SSBR
- 原因：F-SSBR 的 cis-1,4 含量更低

---

## 五、与 cis-BR 的对比

### 相容性差异 (Fig.12)

文献比较了 F-SSBR 和 cis-BR 与树脂的 R 值：
- SSBR（包括 Oil sucked SSBR）与树脂的相容性优于 cis-BR
- 原因：SSBR 含有苯乙烯单元，与树脂相互作用强

---

## 六、综合评价

SSBR-014 (Oil sucked SSBR) 的形貌/结构特点：
- ⚠️ 文献未提供 TEM 表征
- ✅ MD 模拟提供了分子级结构信息
- ✅ 与树脂的相容性趋势与 F-SSBR 相同
- ℹ️ 相容性略低于 F-SSBR（因 cis-1,4 含量较高）
- ✅ 是 Lanxess 公司的成熟工业产品

---

## 文献来源

- **DOI**: 10.1039/c8ra00572a
- **数据引用**: Table 10 (模拟参数), Fig.9 (R值)
