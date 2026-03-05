# SSBR-007 核磁共振解读

```yaml
sample_id: SSBR-007
interpretation_type: nmr
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Table 2, Fig. 1"

nmr_data:
  styrene_content:
    value: 20.4
    unit: "wt%"
    confidence: high
  vinyl_content:
    value: 44.2
    unit: "wt%"
    confidence: high
  cis_1_4_content:
    value: null
    unit: "wt%"
    confidence: null
  trans_1_4_content:
    value: null
    unit: "wt%"
    confidence: null
  total_1_4_content:
    value: 31.2
    unit: "wt%"
    confidence: high

molecular_weight:
  Mn:
    value: 200200
    unit: "g/mol"
    confidence: high
  Mw_Mn:
    value: 1.34
    confidence: high

functionalization:
  functional_group: "-COOH"
  functional_group_name: "羧基"
  reagent: "3-巯基丙酸（MPA）"
  modification_agent_content:
    value: 4.2
    unit: "wt%"
    confidence: high
```

## 样本基本信息

- **样本编号**: SSBR-007（文献中标记为 M2）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 4.2 wt%
- **功能基团**: -COOH（羧基）
- **文献来源**: Qu et al., RSC Advances, 2014

## 核磁共振数据

### 微观结构组成

| 组分 | 含量 | 单位 | 置信度 |
|------|------|------|--------|
| 苯乙烯单元 | 20.4 | wt% | 高 |
| 1,2-聚丁二烯（乙烯基） | 44.2 | wt% | 高 |
| 1,4-聚丁二烯 | 31.2 | wt% | 高 |
| 官能化试剂 | 4.2 | wt% | 高 |

### 分子量信息

| 参数 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 数均分子量 Mn | 2.002×10⁵ | g/mol | 高 |
| 分子量分布 Mw/Mn | 1.34 | - | 高 |

## 结构解读

### 官能化反应量化

系列样品乙烯基含量变化：

| 样品 | 官能化 | 乙烯基 (wt%) | 消耗量 | 转化率 |
|------|--------|--------------|--------|--------|
| M0 | 0 | 47.4 | - | - |
| M1 | 2.4% | 45.6 | 1.8% | 3.8% |
| M2 | 4.2% | 44.2 | 3.2% | 6.8% |

**关键发现**：
- 4.2 wt% 官能化消耗了 3.2% 的乙烯基
- 乙烯基转化率约 6.8%
- 1,4-丁二烯含量基本不变（31.2%）

### 官能化效率分析

官能化含量与乙烯基消耗的关系：

```
官能化含量 (wt%)     乙烯基消耗 (wt%)     效率
    2.4                  1.8              0.75
    4.2                  3.2              0.76
```

官能化效率基本恒定（~0.76），说明：
- 反应选择性一致
- 主要与 1,2-聚丁二烯反应
- 不会发生交联副反应

### 分子量稳定性

| 参数 | M0 | M2 | 变化 |
|------|-----|-----|------|
| Mn | 2.066×10⁵ | 2.002×10⁵ | -3.1% |
| PDI | 1.33 | 1.34 | +0.8% |

分子量和分布指数的微小变化在仪器误差范围内：
- 无链断裂
- 无交联
- 官能化反应温和可控

## 数据来源与置信度说明

- 微观结构数据来自 Table 2
- 分子量数据来自 Table 2
- 置信度"高"表示直接从表格读取
