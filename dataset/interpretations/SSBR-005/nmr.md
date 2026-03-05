# SSBR-005 核磁共振解读

```yaml
sample_id: SSBR-005
interpretation_type: nmr
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Table 2, Fig. 1"

nmr_data:
  styrene_content:
    value: 21.0
    unit: "wt%"
    confidence: high
  vinyl_content:
    value: 47.4
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
    value: 31.6
    unit: "wt%"
    confidence: high

molecular_weight:
  Mn:
    value: 206600
    unit: "g/mol"
    confidence: high
  Mw_Mn:
    value: 1.33
    confidence: high

functionalization:
  functional_group: null
  functional_group_name: "无（空白样品）"
  modification_agent_content:
    value: 0
    unit: "wt%"
    confidence: high
```

## 样本基本信息

- **样本编号**: SSBR-005（文献中标记为 M0）
- **官能团类型**: 无（空白未官能化 SSBR）
- **基体聚合物**: S-SBR2506
- **文献来源**: Qu et al., RSC Advances, 2014

## 核磁共振数据

### 微观结构组成

| 组分 | 含量 | 单位 | 置信度 |
|------|------|------|--------|
| 苯乙烯单元 | 21.0 | wt% | 高 |
| 1,2-聚丁二烯（乙烯基） | 47.4 | wt% | 高 |
| 1,4-聚丁二烯 | 31.6 | wt% | 高 |

### 分子量信息

| 参数 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 数均分子量 Mn | 2.066×10⁵ | g/mol | 高 |
| 分子量分布 Mw/Mn | 1.33 | - | 高 |

## 结构解读

### 微观结构特点

SSBR-005（M0）是燕山石化生产的商业 S-SBR2506：
- **苯乙烯含量 21%**: 标准轮胎胎面配方范围（20-25%）
- **乙烯基含量 47.4%**: 非常高的乙烯基含量，提供官能化反应位点
- **1,4-丁二烯 31.6%**: 提供弹性和低温性能

### 高乙烯基含量的意义

47.4% 的乙烯基含量为后续官能化提供了充足的反应位点：

```
乙烯基含量 47.4% → 可接受硫醇-烯反应
                  → 引入极性官能团
                  → 改善与白炭黑相容性
```

### 分子量分布

- Mn = 2.066×10⁵ g/mol
- PDI = 1.33（较窄的分子量分布）
- 窄分布有利于：
  - 均匀的加工性能
  - 一致的物理性能
  - 可控的官能化反应

### 作为基体材料的适用性

S-SBR2506 作为绿色轮胎用 SSBR 的典型代表：
- 高苯乙烯含量 → 抗湿滑性能
- 高乙烯基含量 → 高 Tg，有利于抓地力
- SiCl4 偶联 → 星形结构，改善加工性

## 数据来源与置信度说明

- 微观结构数据来自 Table 2
- 分子量数据来自 Table 2
- 置信度"高"表示直接从表格读取
