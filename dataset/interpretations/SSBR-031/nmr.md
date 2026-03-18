---
sample_id: SSBR-031
interpretation_type: nmr
source_figure: null
source_doi: "10.1039/c5ra24965a"
skill_used: ssbr-nmr-interpretation
created_at: 2026-03-18
updated_at: null

data:
  functionalization_degree:
    value: 9.6
    unit: "wt%"
    source: "Table 1"
  nmr_source: "referenced from previous experimental work"
---

# SSBR-031 核磁解读

## 样本基本信息

- **样本编号**: SSBR-031
- **官能化试剂**: 3-巯基丙酸 (3-MPA)
- **官能化程度**: 9.6 wt%

## 一、官能化程度

### 数值数据

| 样本 | 接枝量 (wt%) | 官能团数量 (模拟) |
|------|-------------|-----------------|
| M0/g0 | 0 | 0 |
| M1/g1 | 2.4 | 2 |
| M2/g2 | 4.2 | 3 |
| **M3/g3** | **9.6** | **8** |

### SSBR 单元组成

| 单元类型 | M0 (wt%) | M3 (wt%) |
|---------|---------|---------|
| 苯乙烯 | 21.0 | 20.1 |
| 1,2-聚丁二烯 | 47.4 | 40.2 |
| 1,4-聚丁二烯 | 31.6 | 30.1 |
| 接枝 3-MPA | 0 | 9.6 |

## 二、接枝反应

### 反应机理

3-MPA 通过巯基-烯点击化学反应接枝到 SSBR 的 1,2-聚丁二烯单元乙烯基上：

```
SSBR-CH=CH₂ + HS-CH₂-CH₂-COOH → SSBR-CH₂-CH₂-S-CH₂-CH₂-COOH
```

### 特征官能团

- **羧基 (-COOH)**: 提供氢键作用位点
- **硫醚键 (-S-)**: 连接 SSBR 主链和 3-MPA

## 三、备注

本文献为 MD 模拟研究，NMR 数据引用自前期实验工作（Ref. 2: RSC Adv., 2014, 4, 64354-64363）。文献重点在于通过 MD 模拟揭示官能化 SSBR 的结构-性能关系。
