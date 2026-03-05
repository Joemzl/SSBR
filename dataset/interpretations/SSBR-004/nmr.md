# SSBR-004 核磁共振解读

```yaml
sample_id: SSBR-004
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
  functional_group: "-Si(OC2H5)3"
  functional_group_name: "三乙氧基硅烷基"
  reagent: "3-巯基丙基三乙氧基硅烷（MPTES）"
  chain_length: 3
  grafting_rate:
    value: null
    unit: "%"
    confidence: null
  grafting_evidence: "文献 NMR 和 FTIR 证实官能化成功"
```

## 样本基本信息

- **样本编号**: SSBR-004
- **官能团类型**: 3-巯基丙基三乙氧基硅烷（MPTES）官能化 SSBR
- **功能基团**: -Si(OC₂H₅)₃（三乙氧基硅烷基）
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
| 功能基团 | -Si(OC₂H₅)₃ | 三乙氧基硅烷基 |
| 官能化试剂 | MPTES | 3-巯基丙基三乙氧基硅烷 |
| 碳链长度 | 3 | 碳原子数（短链） |
| 接枝率 | - | 文献未提供具体数据 |

## 结构解读

### 微观结构分析

SSBR-004 的基体 SSBR 微观结构与其他样品一致：
- **苯乙烯含量 22.5%**: 提供耐磨性和抗湿滑性能
- **乙烯基含量 42.7%**: 官能化反应的反应位点
- **1,4-丁二烯 34.8%**: 提供弹性和低温柔韧性

### 官能化机理

MPTES 通过硫醇-烯点击化学反应接枝到 SSBR 分子链：

```
SSBR-CH=CH₂ + HS-CH₂-CH₂-CH₂-Si(OC₂H₅)₃ → SSBR-CH₂-CH₂-S-CH₂-CH₂-CH₂-Si(OC₂H₅)₃
   (乙烯基)       (MPTES)                        (硅烷官能化SSBR)
```

**MPTES 官能化特点**：
1. **硅烷末端基**: 可与白炭黑发生缩合反应
2. **硫醚连接**: 通过硫醚键连接 SSBR 主链
3. **短碳链**: 3 碳短链确保硅烷基团贴近主链

### 三乙氧基硅烷的反应活性

硅烷基团与白炭黑的缩合反应：

```
-Si(OC₂H₅)₃ + 3 HO-Si≡ → -Si(-O-Si≡)₃ + 3 C₂H₅OH
  (三乙氧基)   (白炭黑)      (共价键合)     (乙醇)
```

**反应特点**：
- **多点锚定**: 每个硅烷基团可形成最多 3 个 Si-O-Si 键
- **共价结合**: 界面强度远高于氢键
- **不可逆**: 共价键合是永久性的

### 官能团系列对比

不同官能团的化学特性对比：

| 官能团 | 类型 | 与白炭黑作用 | 结合强度 | 可逆性 |
|--------|------|--------------|----------|--------|
| -OH | 羟基 | 氢键 | 中 | 可逆 |
| -COOH | 羧基 | 强氢键 | 中高 | 可逆 |
| -Si(OEt)₃ | 硅烷 | 共价键 | 高 | 不可逆 |

### 对复合材料性能的影响

三乙氧基硅烷官能化的独特优势：
- **最强界面结合**: 共价键合实现最强界面
- **最高力学性能**: 系列中力学性能最优
- **最高 Tg**: 强界面约束导致 Tg 升高最多
- **最佳分散性**: 化学相容性最好

## 数据来源与置信度说明

- 微观结构数据来自文献 SI Table S2
- 官能化证据来自文献 NMR、FTIR 表征
- 基体 SSBR 的微观结构在官能化前后保持不变
