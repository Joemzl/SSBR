---
sample_id: SSBR-030
interpretation_type: nmr
source_figure: "Fig. 1"
source_doi: "10.1039/c4ra09492a"
skill_used: ssbr-nmr-interpretation
created_at: 2026-03-18
updated_at: null

data:
  functionalization_degree:
    value: 9.6
    unit: "wt%"
    source: "Table 2"
  characteristic_peaks:
    - chemical_shift: 2.75
      assignment: "-SCH₂- (硫醚连接)"
      source: "Fig. 1"
---

# SSBR-030 核磁共振解读

## 一、官能化程度

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 改性剂含量 | 9.6 | wt% | Table 2 |
| 1,2-聚丁二烯单元 | 40.2 | wt% | Table 2 |

### 核心发现

¹H NMR 谱图确认了 3-MPA 成功接枝到 SSBR 主链：
- 2.75 ppm 处出现 -SCH₂- 特征峰，证实硫醚键形成
- 1,2-聚丁二烯单元含量从 47.4%（M0）降至 40.2%（M3）
- 1,4-聚丁二烯单元含量基本不变（31.6% → 30.1%）

## 二、反应选择性

### 结构单元变化

| 样本 | 苯乙烯 (wt%) | 1,2-PB (wt%) | 1,4-PB (wt%) | 改性剂 (wt%) |
|------|-------------|--------------|--------------|-------------|
| M0 | 21.0 | 47.4 | 31.6 | 0 |
| M3 | 20.1 | 40.2 | 30.1 | 9.6 |
| 变化 | -0.9 | -7.2 | -1.5 | +9.6 |

### 分析结论

NMR 结果表明：
1. **反应位点**：巯基-烯加成反应主要发生在 1,2-聚丁二烯的侧链乙烯基上
2. **选择性高**：1,4-聚丁二烯主链双键基本未参与反应
3. **分子量保持**：改性前后 Mn 基本不变（~20×10⁴ g/mol），表明未发生链断裂
