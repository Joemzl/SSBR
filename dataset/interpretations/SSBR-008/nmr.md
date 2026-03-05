# SSBR-008 核磁共振解读

```yaml
sample_id: SSBR-008
interpretation_type: nmr
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Table 2, Fig. 1"

nmr_data:
  styrene_content:
    value: 20.1
    unit: "wt%"
    confidence: high
  vinyl_content:
    value: 40.2
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
    value: 30.1
    unit: "wt%"
    confidence: high

molecular_weight:
  Mn:
    value: 225600
    unit: "g/mol"
    confidence: high
  Mw_Mn:
    value: 1.44
    confidence: high

functionalization:
  functional_group: "-COOH"
  functional_group_name: "羧基"
  reagent: "3-巯基丙酸（MPA）"
  modification_agent_content:
    value: 9.6
    unit: "wt%"
    confidence: high
```

## 样本基本信息

- **样本编号**: SSBR-008（文献中标记为 M3）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 9.6 wt%（系列最高）
- **功能基团**: -COOH（羧基）
- **文献来源**: Qu et al., RSC Advances, 2014

## 核磁共振数据

### 微观结构组成

| 组分 | 含量 | 单位 | 置信度 |
|------|------|------|--------|
| 苯乙烯单元 | 20.1 | wt% | 高 |
| 1,2-聚丁二烯（乙烯基） | 40.2 | wt% | 高 |
| 1,4-聚丁二烯 | 30.1 | wt% | 高 |
| 官能化试剂 | 9.6 | wt% | 高 |

### 分子量信息

| 参数 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 数均分子量 Mn | 2.256×10⁵ | g/mol | 高 |
| 分子量分布 Mw/Mn | 1.44 | - | 高 |

## 结构解读

### 官能化反应完整分析

系列样品完整对比：

| 样品 | 官能化 | 乙烯基 | 消耗 | 转化率 |
|------|--------|--------|------|--------|
| M0 | 0 | 47.4% | - | - |
| M1 | 2.4% | 45.6% | 1.8% | 3.8% |
| M2 | 4.2% | 44.2% | 3.2% | 6.8% |
| **M3** | **9.6%** | **40.2%** | **7.2%** | **15.2%** |

**关键发现**：
- 9.6 wt% 官能化消耗了 7.2% 的乙烯基
- 乙烯基转化率约 15.2%（最高）
- 仍保留 40.2% 乙烯基，保持材料基本性能

### 反应选择性验证

| 参数 | M0 | M3 | 变化 | 说明 |
|------|-----|-----|------|------|
| 乙烯基 | 47.4% | 40.2% | -7.2% | 主要反应位点 |
| 1,4-丁二烯 | 31.6% | 30.1% | -1.5% | 基本不变 |
| 苯乙烯 | 21.0% | 20.1% | -0.9% | 基本不变 |

证实反应高度选择性地发生在 1,2-聚丁二烯的悬垂乙烯基上。

### 分子量分析

| 参数 | M0 | M3 | 变化 |
|------|-----|-----|------|
| Mn | 2.066×10⁵ | 2.256×10⁵ | +9.2% |
| PDI | 1.33 | 1.44 | +8.3% |

分子量的轻微增加可能来自：
- 接枝官能团的质量贡献
- 测量误差
- 少量偶联副反应

重要的是，未观察到显著的交联或降解。

### 高官能化含量的结构特点

9.6 wt% 羧基官能化带来的结构变化：

```
每 100 g SSBR 链上：
- 9.6 g 3-巯基丙酸接枝
- 约 0.09 mol 羧基引入
- 平均每条链（Mn=225600）约 20 个羧基

羧基分布：
SSBR 主链 —— 乙烯基 → SSBR-CH₂-CH₂-S-CH₂-CH₂-COOH
            （~15% 转化）
```

### 对材料性能的影响

高羧基含量（9.6 wt%）带来的效果：
- **极性大幅提升**: 表面能极性部分从 0.9 → 4.8 mJ/m²
- **与白炭黑相容性最好**: ΔW 最低 (4.6 mJ/m²)
- **分散性最优**: TEM 显示均匀细腻分散
- **动态性能最佳**: tan δmax 最高，滚动阻力最低

## 数据来源与置信度说明

- 微观结构数据来自 Table 2
- 分子量数据来自 Table 2
- 置信度"高"表示直接从表格读取
