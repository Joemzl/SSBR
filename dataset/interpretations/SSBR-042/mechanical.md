---
sample_id: SSBR-042
interpretation_type: mechanical
source_figure: "Table II, Fig.5, Fig.6"
source_doi: "10.1002/app.28621"
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: null
mechanical_subtypes:
  - stress-strain
  - payne
  - dma

data:
  # ========== 应力-应变数据 ==========
  stress_100:
    value: null
    range: null
    unit: MPa
    source: "文献未提供"
  stress_200:
    value: null
    range: null
    unit: MPa
    source: "文献未提供"
  stress_300:
    value: 3.7
    range: null
    unit: MPa
    source: "Table II"
  tensile_strength:
    value: 10.7
    range: null
    unit: MPa
    source: "Table II"
  elongation:
    value: 522
    range: null
    unit: "%"
    source: "Table II"
  tear_strength:
    value: 21.5
    range: null
    unit: "kN/m"
    source: "Table II"
  hardness:
    value: 56
    range: null
    unit: "Shore A"
    source: "Table II"
  mechanical_source: "L1"
  
  # ========== Payne 效应数据 ==========
  payne_effect:
    description: "DG' (0.28%-100% strain) 较低，表明填料分散良好"
    source: "Fig.5"
  
  # ========== DMA 数据 ==========
  tg_shift:
    value: "+2"
    unit: "℃"
    description: "相比 SSBR/SiO2 复合材料 Tg 升高 2℃"
    source: "Fig.4"
---

# 力学性能解读：SSBR-042

> **样本性质**: N-SSBR/SiO2 共凝聚纳米复合材料（YK-1-2），采用 AMMO 硅烷偶联剂改性，20 phr 纳米白炭黑填充

## 一、基础信息

- **样本ID**: SSBR-042
- **文献中编号**: YK-1-2（N-SSBR/SiO2 纳米复合材料）
- **基体**: YK-1 星形 SSBR（苯乙烯含量 21.1%，乙烯基含量 38.1%）
- **官能化试剂**: AMMO（[3-(2-氨基乙基)氨基丙基]三甲氧基硅烷）
- **填料用量**: 20 phr 纳米白炭黑（平均粒径 20-40 nm）
- **制备方法**: 共凝聚法（co-coagulation）
- **文献DOI**: 10.1002/app.28621

## 二、静态力学性能（应力-应变曲线）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 300%定伸应力 | 3.7 | MPa | Table II |
| 拉伸强度 | 10.7 | MPa | Table II |
| 断裂伸长率 | 522 | % | Table II |
| 撕裂强度 | 21.5 | kN/m | Table II |
| 邵氏A硬度 | 56 | - | Table II |

### 与对照组对比

| 样本 | 300%应力 (MPa) | 拉伸强度 (MPa) | 伸长率 (%) | 撕裂强度 (kN/m) |
|------|----------------|----------------|------------|-----------------|
| YK-1-2 (N-SSBR/SiO2) | 3.7 | 10.7 | 522 | 21.5 |
| YK-1-1 (SSBR/SiO2) | 3.5 | 9.8 | 535 | 20.3 |
| 变化 | +5.7% | +9.2% | -2.4% | +5.9% |

### 核心发现

共凝聚法制备的 N-SSBR/SiO2 纳米复合材料（YK-1-2）相比传统混炼法的 SSBR/SiO2 复合材料（YK-1-1）：
- 拉伸强度提高 **9.2%**（10.7 vs 9.8 MPa）
- 300%定伸应力提高 **5.7%**（3.7 vs 3.5 MPa）
- 撕裂强度提高 **5.9%**（21.5 vs 20.3 kN/m）
- 断裂伸长率略有下降（522% vs 535%）

---

## 三、动态力学性能（Payne效应）

### 核心发现

文献 Fig.5 显示：
> "compared with SSBR/SiO2 nanocomposites, the ΔG' (the difference value between G' in 0.28 and 100% of the strain) of N-SSBR/SiO2 nanocomposites are lower (i.e., a lower Payne effect)."

1. **Payne 效应降低**: N-SSBR/SiO2 的 ΔG'（储能模量变化）低于 SSBR/SiO2
2. **填料分散改善**: 较低的 Payne 效应表明填料-聚合物界面相互作用增强，填料-填料网络减弱

### tan δ-应变曲线分析

文献 Fig.6 指出：
> "Compared with SSBR/SiO2 nanocomposites, the values of tan δ of N-SSBR/SiO2 nanocomposites are all lower."

N-SSBR/SiO2 的 tan δ 值在全应变范围内均低于 SSBR/SiO2，表明：
- 内摩擦损耗降低
- 界面滑移减少
- 更好的填料分散

---

## 四、动态力学性能（DMA温度扫描）

### 核心发现

文献 Fig.4 显示：
> "N-SSBR filled with the same amount of silica exhibit slightly higher G' values in glassy state, higher glass-transition temperatures, and lower values of internal friction loss in the region of glass transition."

1. **Tg 升高 ~2℃**: N-SSBR/SiO2 的玻璃化转变温度比 SSBR/SiO2 高约 2℃
2. **玻璃态 G' 升高**: 表明纳米填料与聚合物链的强相互作用
3. **tan δ 峰面积减小**: 表明分子链运动受限

### 轮胎应用性能分析

文献 Fig.4 还指出：
> "tan δ values of N-SSBR/SiO2 nanocomposites are higher to some extent than those of corresponding SSBR/SiO2 nanocomposites at 0°C"

- **湿地抓地力 (0℃ tan δ)**: N-SSBR/SiO2 在 0℃ 的 tan δ 值略高，表明更好的湿地抓地性能

---

## 五、综合评价

文献结论：
> "N-SSBR might promote the dispersion of nanosilica powder in matrix and could be applied to green tire tread materials."

共凝聚法制备的 YK-1-2 样品具有以下优势：
- ✅ 纳米白炭黑分散更均匀（TEM 证实粒径 20-30 nm）
- ✅ 力学性能略有提升（拉伸强度、撕裂强度）
- ✅ Payne 效应降低，内摩擦损耗减小
- ✅ 适用于绿色轮胎胎面材料

---

## 文献来源

- **DOI**: 10.1002/app.28621
- **数据表格引用**: Table II; Fig.4, 5, 6
