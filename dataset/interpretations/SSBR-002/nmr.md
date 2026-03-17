---
sample_id: SSBR-002
interpretation_type: nmr
source_figure: "Fig. 1(B)"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-nmr-interpretation
created_at: 2026-03-17
updated_at: null

data:
  functionalization_degree:
    value: 8.7
    unit: "wt%"
    source: "Table S2, calculated from NMR"
    calculation_method: "根据 NMR 积分比使用 Eq. (S9) 计算"
  characteristic_peaks:
    - chemical_shift: 2.30
      assignment: "-CH₂COOH (MUA末端羧基相邻亚甲基)"
      integral: null
    - chemical_shift: 2.40
      assignment: "-CH₂COOH (羧基α位亚甲基)"
      integral: null
  vinyl_content:
    value: 39.5
    unit: "%"
    source: "Table S2"
---

# ¹H NMR 核磁共振解读：SSBR-002

> **样本性质**: MUA官能化SSBR（11-巯基十一烷酸接枝），官能化程度8.7 wt%

## 一、基础信息

- **样本ID**: SSBR-002
- **样品名称**: F-SSBR-g-MUA70（官能化溶聚丁苯橡胶）
- **官能化试剂**: MUA（11-巯基十一烷酸，11-Mercaptoundecanoic acid）
- **官能化程度**: 8.7 wt%
- **文献DOI**: 10.1039/c9ra02783a

## 二、官能化确认

### 特征峰归属

| 化学位移 (ppm) | 归属 | 说明 |
|----------------|------|------|
| 2.30-2.40 | -CH₂COOH | MUA末端羧基相邻亚甲基的特征峰 |
| 5.0-5.4 | =CH₂ (1,2-乙烯基) | SSBR主链乙烯基氢 |
| 5.4-5.6 | -CH=CH- (1,4-结构) | SSBR主链内双键氢 |
| 6.5-7.2 | 苯环氢 | 苯乙烯单元芳香氢 |

### 官能化程度

- **计算值**: 8.7 wt%
- **数据来源**: Table S2，通过 Eq. (S9) 计算
- **计算方法**: 
  - A_Methylene-H 取 δ = 2.30–2.40 ppm 范围的峰面积
  - "x" = 2（-CH₂COOH 中的亚甲基氢原子数）

### 核心发现

从 Fig. 1(B) 的 ¹H NMR 谱图可以明确观察到：

1. **官能化成功确认**: 在 2.30-2.40 ppm 处出现了 MUA 特征峰（-CH₂COOH），证明 11-巯基十一烷酸成功接枝到 SSBR 主链上

2. **接枝位点**: 巯基（-SH）通过巯基-烯点击反应与 SSBR 主链上的乙烯基双键发生加成反应

3. **乙烯基消耗**: 约 4.8% 的 1,2-聚丁二烯单元与 MUA 反应

---

## 三、SSBR 主链结构

### 微观结构特征

| 结构单元 | 含量 (wt%) | 说明 |
|----------|------------|------|
| 苯乙烯 | 20.9 | 提供刚性和高 Tg |
| 1,2-乙烯基 | 39.5 | 接枝位点 |
| 1,4-结构 | 29.6 | 主链内双键 |
| 接枝 MUA | 10.0 | 官能化单元 |

### 反应选择性

MUA 分子结构为 HS-(CH₂)₁₀-COOH：
- 巯基端（-SH）与 SSBR 的 1,2-乙烯基反应
- 羧基端（-COOH）保持游离，用于与白炭黑相互作用

---

## 四、与其他官能化样品对比

Fig. 1 展示了三种官能化 SSBR 的 NMR 谱图：

| 样品 | 特征峰位置 (ppm) | 特征基团 | 官能化程度 |
|------|------------------|----------|-----------|
| SSBR-g-MPL | 3.70-3.85 | -CH₂OH (羟基) | 3.6 wt% |
| **SSBR-g-MUA** | **2.30-2.40** | **-CH₂COOH (羧基)** | **8.7 wt%** |
| SSBR-g-MPTES | 3.80-3.92 | -Si-(OCH₂CH₃)₃ | 1.7-9.5 wt% |

MUA 的官能化程度（8.7%）高于 MPL（3.6%），这可能与以下因素有关：
1. MUA 分子量较大（218 g/mol），单位质量贡献更多
2. 反应条件和投料比的差异

---

## 五、溶剂峰和杂质峰

- **溶剂峰**: CDCl₃ (δ 7.26 ppm)
- **杂质峰**: 文献未报告明显杂质峰

---

## 六、结论

¹H NMR 谱图明确证实了 MUA（11-巯基十一烷酸）成功接枝到 SSBR 主链上：
1. **特征峰出现**: 2.30-2.40 ppm 处的 -CH₂COOH 峰
2. **官能化程度**: 8.7 wt%，在三种试剂中最高
3. **反应完整性**: 主链结构保持完整，无副反应产物峰

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **图注引用**: Fig. 1(B)
- **数据表格**: Table S2
