---
# SSBR-046 核磁解读
sample_id: SSBR-046
test_type: nmr
data_source: "10.1002/app.32372"
data_quality: N/A

# NMR 数据状态
nmr_data:
  available: false
  reason: "文献未提供 NMR 测试数据"

# 已知组成信息
composition_info:
  polymer:
    trade_name: "YL950"
    supplier: "燕山石化研究院 (Beijing Yanshan Petrochemical)"
    Mn: 123000
    Mn_unit: "g/mol"
    Mw: 258000
    Mw_unit: "g/mol"
    MWD: 2.1
    styrene_content: 27.5
    styrene_unit: "wt%"
    vinyl_content: 25.4
    vinyl_unit: "mol%"
  coupling_agent:
    name: "Si-75"
    full_name: "Bis[γ-(triethoxysilyl)propyl]disulfide"
    chemical_formula: "C18H42O6S2Si2"
    SMILES: "CCO[Si](CCCSSCCC[Si](OCC)(OCC)OCC)(OCC)OCC"
    dosage: "7% of SiO₂ mass"
    supplier: "Jingzhou Jianghan Fine Chemical"
---

## 核磁解读

### 数据可用性

本文献（DOI: 10.1002/app.32372）未提供 NMR（核磁共振）测试数据。文献主要关注 SSBR/SiO₂/CB 复合材料的力学性能、动态力学性能和抗静电特性，未进行分子结构表征。

### 已知组成信息

#### SSBR (YL950) 组成

| 参数 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 数均分子量 (Mn) | 123,000 | g/mol | 文献 Materials 部分 |
| 重均分子量 (Mw) | 258,000 | g/mol | 文献 Materials 部分 |
| 分子量分布 (MWD) | 2.1 | - | 文献 Materials 部分 |
| 苯乙烯含量 | 27.5 | wt% | 文献 Materials 部分 |
| 乙烯基含量 | 25.4 | mol% | 文献 Materials 部分 |
| 供应商 | 燕山石化研究院 | - | 北京 |

#### 微观结构推算

基于苯乙烯含量（27.5 wt%）和乙烯基含量（25.4 mol%），可推算：
- 丁二烯单元约 72.5 wt%
- 丁二烯单元中：
  - 1,2-结构（乙烯基）：~25.4 mol%
  - 1,4-结构：~74.6 mol%（顺/反比例未知）

#### Si-75 偶联剂

| 参数 | 信息 |
|------|------|
| 化学名称 | 双[γ-(三乙氧基硅基)丙基]二硫化物 |
| SMILES | CCO[Si](CCCSSCCC[Si](OCC)(OCC)OCC)(OCC)OCC |
| 功能 | 改善 SiO₂ 与 SSBR 的亲和性 |
| 用量 | SiO₂ 质量的 7% |
| 作用机理 | 乙氧基与 SiO₂ 表面羟基反应，二硫键在硫化过程中参与交联 |

### 偶联反应机理

Si-75 的作用原理：

1. **水解缩合**：乙氧基（-OC₂H₅）与 SiO₂ 表面的 Si-OH 反应
   ```
   Si-75-Si-OC₂H₅ + HO-Si-SiO₂ → Si-75-Si-O-Si-SiO₂ + C₂H₅OH
   ```

2. **硫化交联**：二硫键（-S-S-）在硫化过程中断裂，与橡胶分子链形成化学键
   ```
   Si-75-S-S-Si-75 + 橡胶 → Si-75-S-橡胶-S-Si-75
   ```

### 反应共混工艺

文献采用 Haake 流变仪进行反应共混（150°C，4 min）：
1. 首先在开炼机上将 SSBR 与 SiO₂/Si-75 混合
2. 室温放置 1 天
3. 在 Haake 流变仪中 150°C 反应共混 4 min
4. 再添加 CB 和其他助剂

这种工艺确保了 Si-75 与 SiO₂ 和 SSBR 充分反应。

### 建议

如需获取 YL950 SSBR 的详细微观结构（顺/反式 1,4-比例、嵌段/无规分布等），建议：
1. 联系燕山石化研究院获取产品技术数据表
2. 进行 ¹H NMR 和 ¹³C NMR 表征
