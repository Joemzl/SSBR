---
sample_id: SSBR-044
interpretation_type: summary
source_doi: "10.1002/app.28621"
created_at: 2026-03-18
updated_at: null

# ========== 样本基本信息 ==========
sample_name: "YK-3-2"
sample_type: "N-SSBR/SiO2 共凝聚纳米复合材料"
is_chain_functionalized: false
functionalization_type: "硅烷偶联剂改性"
functionalization_reagent: "[3-(2-氨基乙基)氨基丙基]三甲氧基硅烷 (AMMO)"
reagent_smiles: "COC[Si](CCC(NCCN)OC)(OC)OC"

# ========== 聚合物结构参数 ==========
polymer_structure:
  styrene_content:
    value: 29.5
    unit: "wt%"
  vinyl_content:
    value: 34.7
    unit: "mol%"
  mn:
    value: 351000
    unit: "g/mol"
  mw:
    value: 574000
    unit: "g/mol"
  pdi: 1.63
  random_degree: 91.5
  architecture: "星形 (4支链)"

# ========== 填料信息 ==========
filler:
  type: "纳米白炭黑"
  grade: "Rhodia Tixosil 383"
  loading: 20
  unit: "phr"
  particle_size: "20-40 nm"
  surface_area: "100-200 m²/g"
  coupling_agent: "AMMO (7 wt% of silica)"
  pre_dispersion: "7 phr in N-SSBR (highest among three)"

# ========== 力学性能数据 ==========
mechanical_properties:
  stress_300:
    value: 3.7
    unit: "MPa"
    source: "Table II"
  tensile_strength:
    value: 10.3
    unit: "MPa"
    source: "Table II"
  elongation:
    value: 455
    unit: "%"
    source: "Table II"
  tear_strength:
    value: 22.2
    unit: "kN/m"
    source: "Table II"
  hardness:
    value: 56
    unit: "Shore A"
    source: "Table II"

# ========== 热学性能数据 ==========
thermal_properties:
  tg_shift:
    value: "+2"
    unit: "℃"
    description: "相比 SSBR/SiO2 复合材料"
  tg_rank: "中等"
  tan_delta_strain: "略高于其他两种样本"

# ========== 形貌数据 ==========
morphology:
  dispersion_quality: "最优"
  particle_size_observed: "20-30 nm"
  fb_value: 0.30
  fb_control: 0.45
  improvement: "FB 值降低 33%"

# ========== 动态性能数据 ==========
dynamic_properties:
  payne_effect: "降低"
  tan_delta_strain: "略高（高苯乙烯含量导致）"
  internal_friction: "降低"

# ========== 应用场景 ==========
application: "绿色轮胎胎面材料"
---

# 综合档案：SSBR-044

> **一句话总结**: 高苯乙烯含量的星形 SSBR 共凝聚纳米复合材料，具有该系列**最佳的填料分散**，但因结构刚性导致断裂伸长率最低。

## 一、样本概述

| 属性 | 内容 |
|------|------|
| **样本ID** | SSBR-044 |
| **文献编号** | YK-3-2 |
| **材料类型** | N-SSBR/SiO2 共凝聚纳米复合材料 |
| **基体** | 星形 SSBR (YK-3)，4 支链结构 |
| **核心特点** | **高苯乙烯含量 (29.5%)，最佳分散** |
| **改性方法** | AMMO 硅烷偶联剂改性 |
| **填料** | 20 phr 纳米白炭黑 |
| **制备工艺** | 共凝聚法 (co-coagulation) |
| **DOI** | 10.1002/app.28621 |

## 二、聚合物结构

### 基体 SSBR (YK-3) 结构参数

| 参数 | 数值 | 在三种 SSBR 中的排名 |
|------|------|----------------------|
| **苯乙烯含量** | **29.5 wt%** | **最高** |
| 乙烯基含量 | 34.7 mol% | 最低 |
| 数均分子量 (Mn) | **35.1×10⁴ g/mol** | **最高** |
| 分子量分布 (PDI) | 1.63 | 中等 |
| **无规度** | **91.5%** | **最低** |
| 分子结构 | 星形，平均 4 支链 | - |

### 高苯乙烯含量的影响

YK-3 的苯乙烯含量（29.5%）是三种 SSBR 中最高的，带来：
1. **分子链刚性增加**: 苯乙烯基团限制链段运动
2. **断裂伸长率降低**: 分子链难以形变和取向
3. **高应变 tan δ 增加**: 刚性基团之间的摩擦增加

### 无规度的特殊性

YK-3 的无规度为 91.5%（vs 其他两种的 100%），表明存在约 8.5% 的嵌段苯乙烯序列，可能影响微相结构。

## 三、关键性能数据

### 力学性能

| 指标 | SSBR-044 (YK-3-2) | 对照 (YK-3-1) | 变化 | 三种样本排名 |
|------|-------------------|---------------|------|-------------|
| 300%定伸应力 | 3.7 MPa | 3.1 MPa | **+19.4%** | 第 2 (与 YK-1-2 并列) |
| 拉伸强度 | 10.3 MPa | 8.9 MPa | **+15.7%** | 第 3 |
| 断裂伸长率 | **455%** | 472% | -3.6% | **最低** |
| 撕裂强度 | 22.2 kN/m | 20.1 kN/m | **+10.4%** | 第 2 |
| 邵氏A硬度 | 56 | 56 | 持平 | 第 2 (与 YK-1-2 并列) |

### 热学与动态性能

| 指标 | SSBR-044 (YK-3-2) | 说明 |
|------|-------------------|------|
| Tg 变化 | +2℃ | 相比 SSBR/SiO2 |
| Tg 排名 | 中等 | 苯乙烯最高但乙烯基最低 |
| Payne 效应 | 降低 | ΔG' 减小 |
| tan δ (应变扫描) | **略高** | 高苯乙烯导致刚性基团摩擦 |

### 形貌特征（最优）

| 指标 | SSBR-044 (YK-3-2) | 对照 (YK-3-1) | 三种样本排名 |
|------|-------------------|---------------|-------------|
| 粒径 | 20-30 nm | >30 nm | - |
| 形态 | 球形，均匀分散 | 团聚体 | - |
| FB 值 | **0.30 ± 0.02** | 0.45 ± 0.02 | **最低（最优）** |
| FB 改善 | **33%** | - | **最大** |

## 四、与其他样本对比

### 三种 N-SSBR/SiO2 样本综合对比

| 指标 | SSBR-042 (YK-1-2) | SSBR-043 (YK-2-2) | **SSBR-044 (YK-3-2)** |
|------|-------------------|-------------------|----------------------|
| 苯乙烯含量 | 21.1% | 24.2% | **29.5%** |
| 乙烯基含量 | 38.1% | **46.0%** | 34.7% |
| 拉伸强度 | 10.7 MPa | **11.9 MPa** | 10.3 MPa |
| 伸长率 | 522% | 489% | **455%** |
| Tg 排名 | 最低 | **最高** | 中等 |
| **FB 值** | 0.33 | 0.31 | **0.30** |

**SSBR-044 具有最佳的填料分散（FB 值最低），但力学性能和伸长率较低。**

## 五、性能优势与机理

### 主要优势

1. ✅ **最佳填料分散**: FB 值 0.30，三种样本中最低
2. ✅ **最大分散改善**: 相比对照组 FB 值降低 33%
3. ✅ **最高分子量**: Mn = 35.1×10⁴，有利于基体力学性能
4. ✅ **共凝聚法效果显著**: 力学性能提升幅度大

### 局限性

1. ⚠️ **断裂伸长率最低**: 455%，高苯乙烯含量导致
2. ⚠️ **高应变 tan δ 略高**: 刚性基团摩擦
3. ⚠️ **无规度略低**: 91.5%，可能存在微相分离

### 机理分析

文献解释了 YK-3 系列的特点：
> "higher styrene content of YK-3 leads to difficult deformation and orientation of its macromolecular chains under tensile stress so that YK-3-1 and YK-3-2 samples are ruptured at lower elongation."

高苯乙烯含量使分子链刚性增加，导致：
- 分子链难以形变和取向
- 断裂伸长率降低
- 刚性基团之间摩擦增加

## 六、应用前景

**目标应用**: 绿色轮胎胎面材料

SSBR-044 的特点使其适合特定应用场景：
- ✅ 最佳填料分散 → 材料均匀性和可靠性
- ✅ 高分子量 → 加工稳定性
- ⚠️ 较低伸长率 → 可能限制某些应用
- ⚠️ 高应变 tan δ → 需要权衡滚动阻力

## 七、数据完整性

| 解读类型 | 状态 | 数据来源 |
|---------|------|----------|
| 力学 (mechanical) | ✅ 完整 | Table II, Fig.5-6 |
| 热学 (dsc) | ✅ 完整 | Fig.3-4 |
| 核磁 (nmr) | ⚠️ 无数据 | 文献未提供 |
| 形貌 (tem) | ✅ 完整 | Fig.1, 7-8 |

---

## 文献来源

- **标题**: Study on Structure and Properties of SSBR/SiO2 Co-coagulated Rubber and SSBR Filled with Nanosilica Composites
- **作者**: Xiao Liu, Suhe Zhao
- **期刊**: Journal of Applied Polymer Science
- **年份**: 2008
- **DOI**: 10.1002/app.28621
