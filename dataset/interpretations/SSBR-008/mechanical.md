---
sample_id: SSBR-008
interpretation_type: mechanical
source_figure: "Fig.2 应力-应变曲线, Fig.4 储能模量-应变曲线"
source_doi: "10.1002/vnl.21635"
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: null
mechanical_subtypes:
  - stress-strain
  - payne

data:
  # ========== 应力-应变数据 ==========
  stress_100:
    value: 1.08
    range: null
    unit: MPa
    source: "Table 3"
  tensile_strength:
    value: 1.74
    range: null
    unit: MPa
    source: "Table 3"
  elongation:
    value: 235
    range: null
    unit: "%"
    source: "Table 3"
  hardness:
    value: 53.16
    unit: "Shore A"
    source: "Table 3"
  mechanical_source: "Table 3"
  
  # ========== Payne 效应数据 ==========
  delta_g_prime:
    value: 16.36
    unit: "N·m"
    source: "Table 2 (ΔH)"
  ml_torque:
    value: 1.98
    unit: "N·m"
    source: "Table 2"
  mh_torque:
    value: 18.34
    unit: "N·m"
    source: "Table 2"
---

# 力学性能解读：SSBR-008

## 一、静态力学性能（应力-应变曲线）

### 数值数据

本样本为未填充参比样本（neat SSBR），用于对比 RBC/SiO₂ 杂化填料增强效果。

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100%定伸应力 | 1.08±0.11 | MPa | Table 3 |
| 拉伸强度 | 1.74±0.16 | MPa | Table 3 |
| 断裂伸长率 | 235±21 | % | Table 3 |
| 硬度 | 53.16±1.04 | Shore A | Table 3 |

### 核心发现

作为未填充参比样本，SSBR-008 展示了 SOL-5130H 型 SSBR 的本征力学性能：
- 拉伸强度较低（1.74 MPa），这是未填充橡胶的典型特征
- 断裂伸长率中等（235%）
- 硬度适中（53.16 Shore A）

### 与填充样本对比

| 样本 | 100%应力 (MPa) | 拉伸强度 (MPa) | 伸长率 (%) | 硬度 (Shore A) |
|------|----------------|----------------|------------|----------------|
| SSBR（未填充） | 1.08 | 1.74 | 235 | 53.16 |
| SSBR/R40S0（40 phr RBC） | 1.48 | 3.15 | 381 | 62 |
| SSBR/R20S20（RBC/SiO₂杂化） | 1.99 | 7.48 | 643 | 67 |

### 分析结论

1. **RBC 单独填充效果**：40 phr RBC 使拉伸强度提升 81%（1.74→3.15 MPa），伸长率提升 62%
2. **RBC/SiO₂ 杂化协同效应**：当 RBC:SiO₂=20:20 时，拉伸强度达到最高（7.48 MPa，提升 330%），伸长率达 643%（提升 174%）
3. **杂化填料机理**：TESPT 改性气相 SiO₂ 的引入改善了填料-橡胶界面相互作用，小粒径 SiO₂ 提供了更高的比表面积

---

## 二、动态力学性能（Payne效应）

### 数值数据

| 样本 | ML (N·m) | MH (N·m) | ΔH (N·m) | ts2 (min) | t90 (min) | CRI (min⁻¹) |
|------|----------|----------|----------|-----------|-----------|-------------|
| SSBR（未填充） | 1.98 | 18.34 | 16.36 | 2.95 | 5.4 | 40.81 |
| SSBR/R40S0 | 3.46 | 30.53 | 27.07 | 3.55 | 8.22 | 21.41 |
| SSBR/R20S20 | 5.47 | 38.68 | 33.21 | 3.43 | 11.12 | 13 |

### 核心发现

1. **Payne 效应分析**（Fig.4）：
   - 未填充 SSBR 的初始储能模量较低，随应变增加变化不明显，说明填料网络较弱
   - SSBR/R40S0 表现为"柔性填料网络"，初始模量较低，模量下降缓慢
   - SSBR/R20S20 表现为"刚性填料网络"，初始模量最高，模量下降迅速

2. **填料网络类型**：
   - R35S5、R30S10：混合型填料网络
   - R25S15、R20S20：刚性填料网络（填料颗粒直接接触）

3. **硫化特性**：随 SiO₂ 含量增加，t90 延长（5.4→11.12 min），这是由于 SiO₂ 吸附硫化剂导致

---

## 三、动态力学性能（DMA温度扫描）

*暂无此项数据*

文献未报道 DMA 温度扫描数据。

---

## 文献来源

- **DOI**: 10.1002/vnl.21635
- **图注引用**: Fig.2 应力-应变曲线, Fig.4 储能模量-应变曲线, Table 2-3
