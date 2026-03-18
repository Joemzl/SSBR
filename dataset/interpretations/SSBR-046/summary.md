---
# SSBR-046 综合档案
sample_id: SSBR-046
version: "1.0"
created: "2026-03-18"
data_source: "10.1002/app.32372"

# 样本基本信息
sample_info:
  name: "SSBR (YL950)"
  type: "未官能化工业级 SSBR"
  modifier: "Si-75 硅烷偶联剂"
  application: "绿色轮胎胎面材料"
  target_scenario: "低滚动阻力、高湿抓地力、高耐磨性"

# 高分子结构
polymer_structure:
  base_polymer: "溶聚丁苯橡胶 (SSBR)"
  trade_name: "YL950"
  styrene_content:
    value: 27.5
    unit: "wt%"
  vinyl_content:
    value: 25.4
    unit: "mol%"
  Mn:
    value: 123000
    unit: "g/mol"
  Mw:
    value: 258000
    unit: "g/mol"
  MWD: 2.1
  supplier: "燕山石化研究院 (Beijing Yanshan Petrochemical)"

# 复合材料体系
composite_system:
  filler_system: "SiO₂/CB 双相填料"
  total_loading: "70 phr"
  optimal_ratio: "SiO₂/CB = 20/50"
  coupling_agent:
    name: "Si-75"
    full_name: "Bis[γ-(triethoxysilyl)propyl]disulfide"
    SMILES: "CCO[Si](CCCSSCCC[Si](OCC)(OCC)OCC)(OCC)OCC"
    dosage: "7% of SiO₂ mass"
  CB_grade: "N234 (ISAF)"
  SiO2_grade: "Tixosil 383 (Rhodia)"
  processing:
    method: "反应共混"
    equipment: "Haake PolyLab"
    temperature: "150°C"
    time: "4 min"

# 关键性能指标 (最佳配方 20/50)
key_properties:
  tensile_strength: "22.8 MPa"
  modulus_300: "18.3 MPa"
  elongation_at_break: "378%"
  tear_strength: "48.1 kN/m"
  hardness: "68 Shore A"
  abrasion: "0.256 cm³/1.61km (最低)"
  heat_buildup: "16.9°C"
  rolling_power_loss: "2.62 J/r (最低)"
  Tg: "-29.1°C"
  tan_delta_0C: "0.23 (最高)"
  tan_delta_60C: "0.11 (最低)"

# 形态学特征
morphology:
  characterization: "TEM"
  optimal_dispersion: "SiO₂/CB = 20/50"
  observation: "SiO₂ 嵌入 CB 网络，协同分散"
  filler_size:
    CB: "~30 nm 球形"
    SiO2: "20-40 nm 不规则"

# 抗静电特性
antistatic:
  percolation_threshold: "SiO₂/CB = 35/35"
  mechanism: "隧道导电理论"
  requirement: "SiO₂/CB < 1/1 以保持抗静电性"

# 文献信息
literature:
  title: "Study on the Structure-Mechanical Properties Relationship and Antistatic Characteristics of SSBR Composites Filled with SiO2/CB"
  authors: "Wang L, Zhao SH"
  journal: "Journal of Applied Polymer Science"
  year: 2010
  volume: 118
  issue: 1
  pages: "338-345"
  doi: "10.1002/app.32372"

# RAG 检索关键词
rag_keywords:
  - "绿色轮胎"
  - "魔三角"
  - "滚动阻力"
  - "湿抓地力"
  - "耐磨性"
  - "SiO₂/CB 双相填料"
  - "Si-75 硅烷偶联剂"
  - "反应共混"
  - "Payne 效应"
  - "抗静电"
  - "渗滤阈值"
  - "纳米复合材料"
---

## 样本概述

SSBR-046 是燕山石化 YL950 型溶聚丁苯橡胶，用于研究 SiO₂/CB 双相填料体系对绿色轮胎胎面材料"魔三角"性能的平衡优化。

### 研究背景

轮胎工业面临的核心挑战是"魔三角"问题：
- **滚动阻力** ↔ **湿抓地力** ↔ **耐磨性**

改善其中一两项性能往往会牺牲另外的性能。本研究通过 SiO₂/CB 双相填料体系和反应共混技术，实现了"魔三角"性能的良好平衡。

### 核心创新点

1. **双相填料协同效应**：SiO₂ 和 CB 协同分散，力学性能优于单一填料体系
2. **反应共混技术**：150°C 下 Si-75 与 SiO₂ 和 SSBR 反应，增强界面结合
3. **抗静电渗滤阈值**：首次确定 SSBR/SiO₂/CB 体系的抗静电渗滤阈值
4. **最佳配方优化**：SiO₂/CB = 20/50 实现综合性能最优

## 材料与配方

### SSBR 基础信息

| 参数 | 数值 | 单位 |
|------|------|------|
| 商品名 | YL950 | - |
| 苯乙烯含量 | 27.5 | wt% |
| 乙烯基含量 | 25.4 | mol% |
| Mn | 123,000 | g/mol |
| Mw | 258,000 | g/mol |
| MWD | 2.1 | - |

### 复合材料配方 (phr)

| 组分 | 功能 | 用量 |
|------|------|------|
| SSBR | 基体 | 100 |
| SiO₂/CB | 填料 | 70（总量） |
| Si-75 | 偶联剂 | SiO₂ 的 7% |
| ZnO | 活化剂 | 4 |
| 硬脂酸 | 活化剂/增塑剂 | 2 |
| 防老剂 4010NA | 防护 | 1 |
| 促进剂 CZ | 硫化促进 | 1.5 |
| 促进剂 D | 硫化促进 | SiO₂ 的 2.5% |
| 芳烃油 | 增塑剂 | 20 |
| 硫黄 | 交联剂 | 1.8 |

## 性能表现

### 力学性能对比

| SiO₂/CB | 拉伸强度 (MPa) | 300% 模量 (MPa) | 断裂伸长 (%) | 撕裂强度 (kN/m) |
|---------|---------------|-----------------|--------------|-----------------|
| 0/70 | 17.3 | 11.6 | 356 | 46.6 |
| **20/50** | **22.8** | **18.3** | 378 | 48.1 |
| 35/35 | 22.2 | 15.6 | 409 | **57.9** |
| 50/20 | 21.5 | 15.1 | **454** | 50.7 |
| 70/0 | 20.3 | 12.8 | 402 | 46.9 |

**最佳配方 (20/50)** 的拉伸强度比纯 CB 体系提高 **32%**。

### "魔三角"性能平衡

| 性能指标 | 评价参数 | 0/70 | **20/50** | 35/35 | 70/0 |
|----------|---------|------|-----------|-------|------|
| 滚动阻力 | tan δ (60°C) | 0.12 | **0.11** | **0.11** | 0.12 |
| 湿抓地力 | tan δ (0°C) | 0.18 | **0.23** | 0.22 | 0.21 |
| 耐磨性 | 磨耗 (cm³/1.61km) | 0.370 | **0.256** | 0.278 | 0.358 |

**结论**：SiO₂/CB = 20/50 配方实现了"魔三角"的最佳平衡。

### Payne 效应与填料分散

| SiO₂/CB | ΔG' (Payne 效应) | 分散评价 |
|---------|------------------|---------|
| 0/70 | 最大 | 差 |
| **20/50** | **最小** | **最佳** |
| 35/35 | 较小 | 良好 |
| 70/0 | 较大 | 中等 |

Payne 效应最低表明 20/50 配方具有最佳的纳米级分散。

### 抗静电特性

| SiO₂/CB | 表面电阻率 (Ω·cm) | 体积电阻率 (Ω·cm) | 抗静电性 |
|---------|------------------|------------------|---------|
| 0/70 | ~10⁶ | ~10⁶ | ✓ 优异 |
| 20/50 | ~10⁷ | ~10⁷ | ✓ 良好 |
| 35/35 | ~10⁸ | ~10⁸ | ✓ **渗滤阈值** |
| 50/20 | ~10¹³ | ~10¹³ | ✗ 绝缘 |
| 70/0 | ~10¹⁴ | ~10¹⁴ | ✗ 绝缘 |

**安全要求**：为满足抗静电要求（10⁶-10¹⁰ Ω·cm），SiO₂/CB 配比应 **< 1/1**。

## 形态学分析

### TEM 观察

| 配方 | 形态特征 | 分散评价 |
|------|---------|---------|
| 0/70 | CB 形成网络，~30 nm 球形 | 存在聚集 |
| 20/50 | SiO₂ 嵌入 CB 网络 | **最佳** |
| 35/35 | 双相交织网络 | 良好 |
| 70/0 | SiO₂ 形成网络，20-40 nm 不规则 | 存在聚集 |

### 协同分散机理

1. SiO₂ 的不规则形状打断 CB 链状聚集
2. Si-75 增强 SiO₂-SSBR 界面结合
3. 预混工艺提高后续 CB 分散

## 应用建议

### 配方设计

- **追求综合性能平衡**：SiO₂/CB = 20/50
- **追求高撕裂强度**：SiO₂/CB = 35/35
- **追求低生热**：增加 SiO₂ 比例
- **需要抗静电**：SiO₂/CB < 35/35

### 加工工艺

1. **第一阶段**：开炼机混合 SSBR + SiO₂ + Si-75
2. **室温存放**：1 天
3. **第二阶段**：Haake 流变仪 150°C 反应共混 4 min
4. **第三阶段**：开炼机添加 CB 和其他助剂

### 注意事项

- SiO₂ 用量增加会延长硫化时间（需调整促进剂 D 用量）
- 轮胎胎面需同时考虑抗静电安全性
- 35/35 为抗静电渗滤阈值，实际配方应留有余量

## 数据完整性

| 文档 | 数据质量 | 主要内容 |
|------|----------|----------|
| mechanical.md | L1 | 拉伸、磨耗、Payne 效应、滚动功率损失 |
| dsc.md | L1 | DMTA 温度扫描、Tg、tan δ |
| nmr.md | N/A | 无 NMR 数据（组成信息来自文献） |
| tem.md | L2 | TEM 形貌、填料分散、网络结构 |

## 参考文献

Wang L, Zhao SH. Study on the Structure-Mechanical Properties Relationship and Antistatic Characteristics of SSBR Composites Filled with SiO2/CB[J]. Journal of Applied Polymer Science, 2010, 118(1): 338-345.
