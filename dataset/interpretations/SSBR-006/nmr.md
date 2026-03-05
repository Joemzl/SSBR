# SSBR-006 核磁共振解读

```yaml
sample_id: SSBR-006
interpretation_type: nmr
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Table 2, Fig. 1"

nmr_data:
  styrene_content:
    value: 20.7
    unit: "wt%"
    confidence: high
  vinyl_content:
    value: 45.6
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
    value: 31.3
    unit: "wt%"
    confidence: high

molecular_weight:
  Mn:
    value: 214700
    unit: "g/mol"
    confidence: high
  Mw_Mn:
    value: 1.41
    confidence: high

functionalization:
  functional_group: "-COOH"
  functional_group_name: "羧基"
  reagent: "3-巯基丙酸（MPA）"
  modification_agent_content:
    value: 2.4
    unit: "wt%"
    confidence: high
```

## 样本基本信息

- **样本编号**: SSBR-006（文献中标记为 M1）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 2.4 wt%
- **功能基团**: -COOH（羧基）
- **文献来源**: Qu et al., RSC Advances, 2014

## 核磁共振数据

### 微观结构组成

| 组分 | 含量 | 单位 | 置信度 |
|------|------|------|--------|
| 苯乙烯单元 | 20.7 | wt% | 高 |
| 1,2-聚丁二烯（乙烯基） | 45.6 | wt% | 高 |
| 1,4-聚丁二烯 | 31.3 | wt% | 高 |
| 官能化试剂 | 2.4 | wt% | 高 |

### 分子量信息

| 参数 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 数均分子量 Mn | 2.147×10⁵ | g/mol | 高 |
| 分子量分布 Mw/Mn | 1.41 | - | 高 |

## 结构解读

### 官能化反应分析

与空白样（M0）对比乙烯基含量变化：

| 样品 | 乙烯基 (wt%) | 变化 | 转化量 |
|------|--------------|------|--------|
| M0 | 47.4 | - | - |
| M1 | 45.6 | -1.8 | ~3.8% 乙烯基反应 |

**关键发现**：
- 乙烯基含量从 47.4% 降至 45.6%（减少 1.8%）
- 证实官能化反应消耗了 1,2-聚丁二烯的乙烯基
- 1,4-丁二烯含量几乎不变（31.6% → 31.3%）

### 官能化机理

3-巯基丙酸（MPA）通过硫醇-烯反应接枝：

```
SSBR-CH=CH₂ + HS-CH₂-CH₂-COOH → SSBR-CH₂-CH₂-S-CH₂-CH₂-COOH
   (乙烯基)    (3-巯基丙酸)           (羧基官能化SSBR)
```

**反应特点**：
1. **选择性**: 优先与 1,2-聚丁二烯的悬垂乙烯基反应
2. **保持主链**: 1,4-聚丁二烯主链基本不受影响
3. **引发剂**: AIBN 引发自由基反应

### NMR 表征证据

从文献 Fig. 1 的 ¹H NMR 谱图可观察到：
- **新峰 δ 2.75 ppm**: -SCH₂- 质子信号
- 证实硫醚键形成，官能化反应成功

### 分子量变化

| 参数 | M0 | M1 | 变化 |
|------|-----|-----|------|
| Mn | 2.066×10⁵ | 2.147×10⁵ | +3.9% |
| PDI | 1.33 | 1.41 | +6.0% |

分子量和分布指数的微小增加在仪器误差范围内，表明官能化反应未导致显著的分子量变化。

## 数据来源与置信度说明

- 微观结构数据来自 Table 2
- 分子量数据来自 Table 2
- NMR 表征证据来自 Fig. 1
- 置信度"高"表示直接从表格读取
