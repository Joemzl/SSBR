---
sample_id: SSBR-001
interpretation_type: mechanical
source_figure: "文献 Fig.8 (A) 空白复合材料应力-应变曲线"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-05
updated_at: null
mechanical_subtypes:
  - stress-strain

data:
  # ========== 应力-应变数据 ==========
  stress_100:
    value: 1.5
    range: null
    unit: MPa
    source: "SI Table S5"
  stress_200:
    value: null
    range: null
    unit: MPa
    source: "文献未提供"
  stress_300:
    value: 9.0
    range: null
    unit: MPa
    source: "SI Table S5"
  tensile_strength:
    value: 15.0
    range: null
    unit: MPa
    source: "SI Table S5"
  elongation:
    value: 452
    range: null
    unit: "%"
    source: "SI Table S5"
  mechanical_source: "Gao et al. RSC Advances, 2019, SI Table S5"
---

# 力学性能解读：SSBR-001

> **样本性质**: 空白未官能化 SSBR / 白炭黑复合材料（silica/SSBR），作为本文献中所有官能化样本的对照组。

## 一、静态力学性能（应力-应变曲线）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100%定伸应力 | 1.5 | MPa | SI Table S5 |
| 200%定伸应力 | - | MPa | 文献未提供 |
| 300%定伸应力 | 9.0 | MPa | SI Table S5 |
| 拉伸强度 | 15.0 | MPa | SI Table S5 |
| 断裂伸长率 | 452 | % | SI Table S5 |

### 核心发现

1. **低定伸应力**: 100%定伸应力仅为1.5 MPa，300%定伸应力为9.0 MPa，表明未官能化 SSBR 与白炭黑之间的界面相互作用较弱。

2. **较高伸长率**: 断裂伸长率达452%，说明材料具有良好的延展性，但这是以牺牲强度为代价的。

3. **中等拉伸强度**: 15.0 MPa 的拉伸强度在同类材料中属于中等偏低水平，主要原因是填料-橡胶界面作用不足。

### 与官能化样本对比

| 样本 | 100%应力 (MPa) | 300%应力 (MPa) | 拉伸强度 (MPa) | 伸长率 (%) |
|------|----------------|----------------|----------------|------------|
| SSBR-001 (空白) | 1.5 | 9.0 | 15.0 | 452 |
| SSBR-g-MUA70 | 6.3 | 23.3 | 26.0 | 340 |
| 变化 | +320% | +159% | +73.3% | -24.8% |

### 分析结论

文献指出：由于白炭黑与 SSBR 之间的界面相互作用较弱（weak interfacial interaction），导致填料-填料网络（filler-filler networks）强而填料-橡胶网络（filler-rubber networks）弱，这不利于白炭黑的分散和复合材料综合性能的提升。

---

## 二、动态力学性能（Payne效应）

### 数值数据

| 指标 | 数值 | 单位 |
|------|------|------|
| ΔG' (compounds) | 873.53 | kPa |
| ΔG' (vulcanizates) | 4215.09 | kPa |
| δΔG' | 3341.56 | kPa |
| tan δ at 7% strain | 0.132 | - |

### 核心发现

空白 silica/SSBR 复合材料表现出最高的 Payne 效应（ΔG'=4215.09 kPa），表明填料分散性差、填料-填料网络强。tan δ at 7% strain 为0.132，是所有样本中最高的，意味着滚动阻力最大。

---

## 三、动态力学性能（DMA温度扫描）

### 数值数据

| 指标 | 数值 | 说明 |
|------|------|------|
| 0℃ tanδ | 0.472 | 湿地抓地力指标 |
| tanδmax | 0.640 | - |
| Tg (DMTA) | -9.0 ℃ | - |

### 核心发现

文献 SI Table S6 显示，空白 silica/SSBR 复合材料的 tan δ (0°C) 为0.472，是所有样本中最低的，表明湿地抓地性能最差。文献原文指出："a high tan δ value at 0°C implies excellent wet skid resistance"，因此空白样本的湿滑抗性表现不佳。

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **图注引用**: Fig.8 (A) 空白复合材料应力-应变曲线
- **表格引用**: SI Table S5 (力学性能), SI Table S6 (动态力学性能)
