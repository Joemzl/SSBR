---
sample_id: SSBR-018
interpretation_type: mechanical
source_figure: "Fig.5, Table S3, Table S4"
source_doi: "10.1021/acs.iecr.8b05738"
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: null
mechanical_subtypes:
  - stress-strain
  - payne
  - dma

data:
  # ========== 应力-应变数据 (α-SSBR/silica composite) ==========
  tensile_strength:
    value: "优于原始SSBR"
    range: null
    unit: MPa
    source: "Table S3"
  elongation:
    value: "优于原始SSBR"
    range: null
    unit: "%"
    source: "Table S3"
  tear_strength:
    value: "优于原始SSBR"
    range: null
    unit: "kN/m"
    source: "Table S3"
  hardness:
    value: "低于原始SSBR"
    unit: "Shore A"
    source: "Table S3"
  mechanical_source: "Table S3"
  
  # ========== Payne 效应数据 ==========
  delta_g_prime:
    value: "最小"
    unit: kPa
    source: "Table S2"
  
  # ========== DMA 数据 ==========
  tan_delta_0c:
    value: "较高"
    unit: "-"
    source: "Table S4"
  tan_delta_60c:
    value: "较低"
    unit: "-"
    source: "Table S4"
---

# 力学性能解读：SSBR-018

## 一、样本说明

SSBR-018 对应文献中的 **α-SSBR**，通过阴离子聚合在 SSBR 链端引入 DPE-(NMe₂)₂ 基团（氨基官能团），端基封装效率为 **83%**。

### 结构特征

| 参数 | α-SSBR | 原始 SSBR |
|------|--------|-----------|
| DPE 单元含量 | 0.09 wt% | 0 |
| 端基封装效率 | 83% | - |
| 苯乙烯含量 | 27.8 wt% | 28.3 wt% |
| 乙烯基含量 | 64.3 wt% | 64.0 wt% |
| Mn | 93.6 kg/mol | 97.3 kg/mol |
| PDI | 1.15 | 1.16 |
| Tg | -17.4°C | -16.5°C |

---

## 二、静态力学性能（应力-应变曲线）

### 核心发现

根据 Fig.5(b) 和 Table S3，α-SSBR/白炭黑复合材料相比原始 SSBR/白炭黑复合材料：

1. **拉伸强度**：明显提升
2. **断裂伸长率**：明显提升  
3. **撕裂强度**：明显提升
4. **硬度**：降低（表明弹性更好）

### 改善机理

氨基官能团与白炭黑表面羟基形成**氢键相互作用**（Fig.6 示意图）：
- 氢键在机械共混过程中传递剪切力，有助于减小团聚体尺寸
- 强界面相互作用增强了复合材料强度
- 改善的白炭黑分散带来更低的硬度和更好的弹性

---

## 三、动态力学性能（Payne效应）

### 数值数据

根据 Fig.4 和 Table S2：

| 样本 | ΔG' (相对值) | 白炭黑分散性 |
|------|-------------|--------------|
| 原始 SSBR/silica | 高 | 差 |
| **α-SSBR/silica** | **最小** | **最好** |
| α,ω-SSBR/silica | 最高 | - |
| IC-SSBR/silica | 中等 | 中等 |

### 核心发现

**α-SSBR/silica 具有最小的 Payne 效应（ΔG'）**，表明：
- 链端氨基官能团有利于白炭黑团聚体的分散
- 氨基-羟基氢键改善了填料-橡胶界面相互作用
- 填料网络结构更加均匀

---

## 四、动态力学性能（DMA温度扫描）

### 数值数据

根据 Fig.7 和 Table S4：

| 指标 | α-SSBR/silica | 原始 SSBR/silica |
|------|---------------|------------------|
| tan δ 峰温度（Tg） | 相似 | 基准 |
| tan δ (0°C) | 较高 | 基准 |
| tan δ (60°C) | 较低 | 基准 |

### 核心发现

1. **湿地抓地力（0°C tanδ）**：α-SSBR 复合材料表现较好
2. **滚动阻力（60°C tanδ）**：α-SSBR 复合材料较低
3. **综合性能**：α-SSBR 在四种样本中展现出最佳的综合性能平衡

### 绿色轮胎适用性

> α-SSBR/silica composite showed higher static mechanical properties, better wet-skid resistance, and lower loss factors, making it an appropriate material towards the manufacturing of high-performance green tire.

---

## 文献来源

- **DOI**: 10.1021/acs.iecr.8b05738
- **图注引用**: Fig.4 Payne effect, Fig.5 Stress-strain, Fig.7 DMA, Table S2-S4
