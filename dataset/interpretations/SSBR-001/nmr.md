---
sample_id: SSBR-001
interpretation_type: nmr
source_figure: "文献 Fig.1 (A/B/C) 基础 SSBR 核磁谱图"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-nmr-interpretation
created_at: 2026-03-05
updated_at: null

data:
  functionalization_degree:
    value: 0
    unit: "wt%"
    source: "空白未官能化样本"
    calculation_method: null
  characteristic_peaks:
    - region: "4.45-5.10 ppm"
      assignment: "1,2-聚丁二烯单元 =CH-"
    - region: "5.10-5.90 ppm"
      assignment: "1,4-聚丁二烯单元 -CH=CH-"
    - region: "6.70-7.23 ppm"
      assignment: "苯乙烯单元芳环质子"
  vinyl_content:
    value: 42.7
    unit: "wt%"
    source: "SI Table S2"
---

# ¹H NMR 核磁共振解读：SSBR-001

> **样本性质**: 空白未官能化 SSBR，作为本文献中所有官能化样本的结构对照组。

## 一、官能化确认

### 特征峰归属

| 化学位移 (ppm) | 归属 | 积分比 |
|----------------|------|--------|
| 4.45-5.10 | 1,2-聚丁二烯单元 =CH- | 基准 |
| 5.10-5.90 | 1,4-聚丁二烯单元 -CH=CH- | 见下表 |
| 6.70-7.23 | 苯乙烯单元芳环质子 | 见下表 |

### 官能化程度

- **计算值**: 0 wt%（空白未官能化样本）
- **计算方法**: 无官能化，无需计算

### 核心发现

作为空白对照组，SSBR-001 的 ¹H NMR 谱图（Fig.1 A/B/C）呈现典型的溶聚丁苯橡胶特征：

1. **无新增特征峰**: 与官能化样本相比，SSBR-001 谱图中不存在官能团新增峰（如 3.70-3.85 ppm 的 -CH₂OH、2.30-2.40 ppm 的 -CH₂COOH、3.80-3.92 ppm 的 -Si-(OCH₂CH₃)₃）

2. **基线清洁**: 谱图基线平整，无杂峰，证明 SSBR 合成纯度良好

---

## 二、SSBR 主链结构

### 微观结构分析

| 结构单元 | 含量 (wt%) | 计算依据 |
|----------|----------|----------|
| 苯乙烯 | 22.5 | SI Table S2, Eq.(S4)-(S8) |
| 1,2-聚丁二烯（乙烯基） | 42.7 | SI Table S2, Eq.(S4)-(S8) |
| 1,4-聚丁二烯 | 34.8 | SI Table S2, Eq.(S4)-(S8) |

### 结构解析

文献 SI Table S2 提供了 SSBR 的详细组成：
- **苯乙烯/丁二烯质量比**: 25:75（合成配方）
- **乙烯基含量**: 42.7 wt%，属于高乙烯基 SSBR
- **分子量**: Mn = 18.1×10⁴ g/mol, Mw/Mn = 1.11

> 高乙烯基含量（42.7%）对于后续巯基-烯烃点击反应至关重要，因为1,2-聚丁二烯单元是官能化反应的主要反应位点。

---

## 三、溶剂峰和杂质峰

- **溶剂峰**: CDCl₃（约 7.26 ppm）
- **杂质峰**: 文献未报告明显杂质峰，表明 SSBR 纯度良好

---

## 四、定量计算方法

文献采用以下公式计算 SSBR 组成（Eq. S4-S8）：

1. **丁二烯单元比例**:
   ```
   (2N_{Bd1,4} + N_{Bd1,2}) / (2N_{Bd1,2}) = A_{5.10-5.90} / A_{4.45-5.10}
   ```

2. **苯乙烯单元比例**:
   ```
   (5N_{St}) / (2N_{Bd1,2}) = A_{6.70-7.23} / A_{4.45-5.10}
   ```

3. **分子量守恒**:
   ```
   M_{Bd}×N_{Bd1,4} + M_{Bd}×N_{Bd1,2} + M_{St}×N_{St} = M_n
   ```

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **图注引用**: Fig.1 (A/B/C) 基础 SSBR 核磁谱图
- **表格引用**: SI Table S2 (SSBR 和 F-SSBRs 的组成特征)
