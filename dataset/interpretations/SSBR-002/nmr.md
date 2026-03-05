# SSBR-002 核磁共振解读

```yaml
sample_id: SSBR-002
interpretation_type: nmr
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c9ra02783a"
source_figure: "SI Table S2, SI Fig. S1"

nmr_data:
  styrene_content:
    value: 22.5
    unit: "wt%"
    confidence: high
  vinyl_content:
    value: 42.7
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
    value: 34.8
    unit: "wt%"
    confidence: high

functionalization:
  functional_group: "-OH"
  functional_group_name: "羟基"
  grafting_rate:
    value: null
    unit: "%"
    confidence: null
  grafting_evidence: "文献未提供具体接枝率数据"
```

## 样本基本信息

- **样本编号**: SSBR-002
- **官能团类型**: 3-巯基丙醇（MPL）官能化 SSBR
- **功能基团**: -OH（羟基）
- **基体聚合物**: SSBR
- **文献来源**: Gao et al., RSC Advances, 2019

## 核磁共振数据

### 微观结构组成

| 组分 | 含量 | 单位 | 置信度 |
|------|------|------|--------|
| 苯乙烯单元 | 22.5 | wt% | 高 |
| 1,2-聚丁二烯（乙烯基） | 42.7 | wt% | 高 |
| 1,4-聚丁二烯 | 34.8 | wt% | 高 |

### 官能化信息

| 参数 | 数值 | 说明 |
|------|------|------|
| 功能基团 | -OH | 羟基 |
| 官能化试剂 | 3-巯基丙醇（MPL） | 硫醇-烯点击化学 |
| 接枝率 | - | 文献未提供具体数据 |

## 结构解读

### 微观结构分析

SSBR-002 的微观结构与基体 SSBR（SSBR-001）保持一致：
- **苯乙烯含量 22.5%**: 提供耐磨性和抗湿滑性能
- **乙烯基含量 42.7%**: 高乙烯基含量提供官能化反应位点
- **1,4-丁二烯 34.8%**: 提供弹性和低温柔韧性

### 官能化机理

3-巯基丙醇（MPL）通过硫醇-烯点击化学反应接枝到 SSBR 分子链上：

```
SSBR-CH=CH₂ + HS-CH₂-CH₂-CH₂-OH → SSBR-CH₂-CH₂-S-CH₂-CH₂-CH₂-OH
   (乙烯基)      (3-巯基丙醇)           (羟基官能化SSBR)
```

**反应特点**：
1. **反应位点**: 1,2-聚丁二烯单元的悬垂乙烯基
2. **反应类型**: 硫醇-烯点击化学（自由基加成）
3. **官能化效果**: 在分子链侧基引入羟基，改善与白炭黑的相容性

### 官能化对性能的影响

羟基官能化改善了 SSBR 与白炭黑的界面作用：
- **氢键作用**: -OH 与白炭黑表面 Si-OH 形成氢键
- **分散性提升**: 减少填料团聚，提高分散均匀性
- **补强效率**: 更强的界面结合带来更好的力学性能

## 数据来源与置信度说明

- 微观结构数据来自文献 SI Table S2
- 官能化证据来自文献 NMR 表征（SI Fig. S1）
- 基体 SSBR 的微观结构在官能化前后保持不变
