# SSBR-003 核磁共振解读

```yaml
sample_id: SSBR-003
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
  functional_group: "-COOH"
  functional_group_name: "羧基"
  reagent: "11-巯基十一烷酸（MUA）"
  chain_length: 11
  grafting_rate:
    value: null
    unit: "%"
    confidence: null
  grafting_evidence: "文献未提供具体接枝率数据"
```

## 样本基本信息

- **样本编号**: SSBR-003
- **官能团类型**: 11-巯基十一烷酸（MUA）官能化 SSBR
- **功能基团**: -COOH（羧基）
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
| 功能基团 | -COOH | 羧基 |
| 官能化试剂 | 11-巯基十一烷酸（MUA） | 长链硫醇 |
| 碳链长度 | 11 | 碳原子数 |
| 接枝率 | - | 文献未提供具体数据 |

## 结构解读

### 微观结构分析

SSBR-003 的微观结构与基体 SSBR 保持一致：
- **苯乙烯含量 22.5%**: 提供耐磨性和抗湿滑性能
- **乙烯基含量 42.7%**: 高乙烯基含量是官能化反应的关键
- **1,4-丁二烯 34.8%**: 提供弹性和低温柔韧性

### 官能化机理

11-巯基十一烷酸（MUA）通过硫醇-烯点击化学反应接枝到 SSBR 分子链：

```
SSBR-CH=CH₂ + HS-(CH₂)₁₀-COOH → SSBR-CH₂-CH₂-S-(CH₂)₁₀-COOH
   (乙烯基)    (11-巯基十一烷酸)      (羧基官能化SSBR)
```

**MUA 官能化特点**：
1. **长碳链**: 11 个碳的长链提供柔性连接
2. **末端羧基**: 强极性基团，与白炭黑强相互作用
3. **间隔效应**: 长链起到"间隔臂"作用，使羧基充分暴露

### 长链官能化的优势

与短链官能化（如 SSBR-002 的 MPL）相比，MUA 的长链结构带来独特优势：

| 特点 | 短链（MPL, C3） | 长链（MUA, C11） |
|------|-----------------|------------------|
| 柔性 | 较低 | 较高 |
| 功能基团活性 | 受限 | 充分暴露 |
| 界面层厚度 | 薄 | 厚 |
| 应力传递 | 直接 | 缓冲式 |

### 对复合材料性能的影响

羧基官能化结合长碳链的综合效果：
- **更强的界面结合**: 羧基与白炭黑形成强氢键
- **更好的应力传递**: 长碳链提供柔性连接，改善应力传递
- **更优的力学性能**: 系列样品中力学性能最佳

## 数据来源与置信度说明

- 微观结构数据来自文献 SI Table S2
- 官能化证据来自文献 NMR 和 FTIR 表征
- 基体 SSBR 的微观结构在官能化前后保持不变
