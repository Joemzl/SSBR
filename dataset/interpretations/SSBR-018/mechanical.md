---
sample_id: SSBR-018
interpretation_type: mechanical
source_figure: Fig.5, Table S3, Table S4
source_doi: 10.1021/acs.iecr.8b05738
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
mechanical_subtypes:
- stress-strain
- payne
- dma
data:
  tensile_strength:
    value: 优于原始SSBR
    range: null
    unit: MPa
    source: Table S3
  elongation:
    value: 优于原始SSBR
    range: null
    unit: '%'
    source: Table S3
  tear_strength:
    value: 优于原始SSBR
    range: null
    unit: kN/m
    source: Table S3
  hardness:
    value: 低于原始SSBR
    unit: Shore A
    source: Table S3
  mechanical_source: Table S3
  delta_g_prime:
    value: 最小
    unit: kPa
    source: Table S2
  tan_delta_0c:
    value: 较高
    unit: '-'
    source: Table S4
  tan_delta_60c:
    value: 较低
    unit: '-'
    source: Table S4
skill_version: '2.0'
curves:
  # ---------- 应力-应变曲线 (Fig. 5b) ----------
  stress_strain:
    x_axis:
      label: 应变
      unit: '%'
    y_axis:
      label: 应力
      unit: MPa
    data_points: []
    curve_features:
      modulus_100:
        value: null
        unit: MPa
        source: "文献未提供绝对数值"
        confidence: null
      modulus_300:
        value: null
        unit: MPa
        source: "文献未提供绝对数值"
        confidence: null
      tensile_strength:
        value: null
        unit: MPa
        source: "Table S3"
        confidence: null
        note: "优于原始 SSBR"
      elongation_at_break:
        value: null
        unit: '%'
        source: "Table S3"
        confidence: null
        note: "优于原始 SSBR"
      tear_strength:
        value: null
        unit: kN/m
        source: "Table S3"
        note: "优于原始 SSBR"
      yield_point:
        exists: false
    validation:
      known_points: []
      overall_quality: "poor"
      note: "文献仅提供相对比较（优于/劣于），无绝对数值"
    metadata:
      point_count: 0
      x_range: [0, 0]
      y_range: [0, 0]
      avg_confidence: 0

  # ---------- DMA tan δ-温度曲线 (Fig. 7) ----------
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: 无量纲
    data_points: []
    curve_features:
      tan_delta_0C:
        value: null
        unit: "-"
        source: "Table S4"
        confidence: null
        note: "较高 (相比原始 SSBR)，有利于湿地抓地力"
      tan_delta_60C:
        value: null
        unit: "-"
        source: "Table S4"
        confidence: null
        note: "较低 (相比原始 SSBR)，有利于滚动阻力"
      tan_delta_max:
        value: null
        unit: "-"
        source: "Fig. 7"
        confidence: null
      Tg:
        value: -17.4
        unit: °C
        method: "DSC (Table 1)"
        source: "L1"
        confidence: 0.95
        note: "α-SSBR 纯聚合物 Tg"
    validation:
      known_points: []
      overall_quality: "poor"
      note: "文献仅提供相对比较，无绝对 tan δ 数值"
    metadata:
      point_count: 0
      x_range: [-80, 80]
      y_range: [0, 1]
      avg_confidence: 0

  # ---------- Payne 效应 G'-应变曲线 (Fig. 4) ----------
  payne_storage_modulus:
    x_axis:
      label: 应变
      unit: '%'
      scale: logarithmic
    y_axis:
      label: 储能模量 G'
      unit: MPa
    data_points: []
    curve_features:
      G_prime_0:
        value: null
        unit: MPa
        strain_at: 0.28
        source: "Fig. 4"
        confidence: null
      G_prime_inf:
        value: null
        unit: MPa
        strain_at: 42
        source: "Fig. 4"
        confidence: null
      delta_G_prime:
        value: null
        unit: kPa
        source: "Table S2"
        confidence: null
        note: "α-SSBR 的 ΔG' 最小，分散性最好"
    validation:
      known_points: []
      overall_quality: "poor"
      note: "文献仅提供相对比较和趋势描述，无绝对数值"
    metadata:
      point_count: 0
      x_range: [0.1, 100]
      y_range: [0, 3]
      avg_confidence: 0
---
# 力学性能解读：SSBR-018


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

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
