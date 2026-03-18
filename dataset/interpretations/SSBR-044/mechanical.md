---
sample_id: SSBR-044
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
    value: 10.3
    range: null
    unit: MPa
    source: "Table II"
  elongation:
    value: 455
    range: null
    unit: "%"
    source: "Table II"
  tear_strength:
    value: 22.2
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
  tan_delta_strain:
    description: "tan δ 值略高于其他两种样本"
    source: "Fig.6"
---

# 力学性能解读：SSBR-044

> **样本性质**: N-SSBR/SiO2 共凝聚纳米复合材料（YK-3-2），采用 AMMO 硅烷偶联剂改性，20 phr 纳米白炭黑填充

## 一、基础信息

- **样本ID**: SSBR-044
- **文献中编号**: YK-3-2（N-SSBR/SiO2 纳米复合材料）
- **基体**: YK-3 星形 SSBR（苯乙烯含量 29.5%，乙烯基含量 34.7%）
- **官能化试剂**: AMMO（[3-(2-氨基乙基)氨基丙基]三甲氧基硅烷）
- **填料用量**: 20 phr 纳米白炭黑（平均粒径 20-40 nm）
- **制备方法**: 共凝聚法（co-coagulation）
- **文献DOI**: 10.1002/app.28621

## 二、静态力学性能（应力-应变曲线）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 300%定伸应力 | 3.7 | MPa | Table II |
| 拉伸强度 | 10.3 | MPa | Table II |
| 断裂伸长率 | 455 | % | Table II |
| 撕裂强度 | 22.2 | kN/m | Table II |
| 邵氏A硬度 | 56 | - | Table II |

### 与对照组对比

| 样本 | 300%应力 (MPa) | 拉伸强度 (MPa) | 伸长率 (%) | 撕裂强度 (kN/m) |
|------|----------------|----------------|------------|-----------------|
| YK-3-2 (N-SSBR/SiO2) | 3.7 | 10.3 | 455 | 22.2 |
| YK-3-1 (SSBR/SiO2) | 3.1 | 8.9 | 472 | 20.1 |
| 变化 | +19.4% | +15.7% | -3.6% | +10.4% |

### 核心发现

共凝聚法制备的 N-SSBR/SiO2 纳米复合材料（YK-3-2）相比传统混炼法的 SSBR/SiO2 复合材料（YK-3-1）：
- 300%定伸应力提高 **19.4%**（3.7 vs 3.1 MPa）
- 拉伸强度提高 **15.7%**（10.3 vs 8.9 MPa）
- 撕裂强度提高 **10.4%**（22.2 vs 20.1 kN/m）
- 断裂伸长率略有下降（455% vs 472%）

### YK-3 的结构特点

文献指出 YK-3 系列具有较低的伸长率：
> "YK-3-1 and YK-3-2 have slightly lower elongation at break than other two series of samples. It is possibly because higher styrene content of YK-3 leads to difficult deformation and orientation of its macromolecular chains under tensile stress."

YK-3 的高苯乙烯含量（29.5%）使分子链在拉伸应力下难以形变和取向，导致较低的断裂伸长率。

---

## 三、动态力学性能（Payne效应）

### 核心发现

文献 Fig.5(c) 显示：
1. **Payne 效应降低**: N-SSBR/SiO2 的 ΔG' 低于 SSBR/SiO2
2. **填料分散改善**: 共凝聚法提高了填料分散均匀性

### tan δ-应变曲线分析

文献 Fig.6(c) 显示 YK-3 系列的 tan δ 值特点：
> "the tan δ values (i.e., internal friction loss values) of YK-3-1 and YK-3-2 are slightly higher than the other two series of samples. It is possibly because higher styrene content of YK-3 leads to severe friction among these rigid groups under a certain strain."

YK-3 系列的 tan δ 值略高于其他两种样本，这是由于高苯乙烯含量导致刚性基团之间的摩擦增加。

---

## 四、动态力学性能（DMA温度扫描）

### 核心发现

1. **Tg 升高 ~2℃**: N-SSBR/SiO2 的玻璃化转变温度比 SSBR/SiO2 高约 2℃
2. **Tg 中等**: YK-3 的 Tg 介于 YK-1 和 YK-2 之间

### YK-3 的 Tg 特点

YK-3 尽管苯乙烯含量最高（29.5%），但 Tg 并非最高，因为：
- 乙烯基含量（34.7%）是三种中最低的
- 苯乙烯和乙烯基含量共同影响 Tg

---

## 五、与其他样本对比

### 三种 N-SSBR/SiO2 样本力学性能对比

| 指标 | YK-1-2 | YK-2-2 | **YK-3-2** |
|------|--------|--------|------------|
| 苯乙烯含量 | 21.1% | 24.2% | **29.5%** |
| 乙烯基含量 | 38.1% | 46.0% | 34.7% |
| 300%应力 (MPa) | 3.7 | 4.6 | 3.7 |
| 拉伸强度 (MPa) | 10.7 | 11.9 | 10.3 |
| 伸长率 (%) | 522 | 489 | **455** |
| 撕裂强度 (kN/m) | 21.5 | 25.5 | 22.2 |

YK-3-2 (SSBR-044) 的断裂伸长率最低（455%），这是高苯乙烯含量导致分子链刚性增加的结果。

---

## 六、综合评价

SSBR-044 (YK-3-2) 的特点：
- ✅ 共凝聚法使力学性能显著提升（拉伸强度 +15.7%）
- ✅ 300%定伸应力提升幅度最大（+19.4%）
- ✅ Payne 效应降低，填料分散改善
- ⚠️ 断裂伸长率最低（455%），高苯乙烯含量导致
- ⚠️ tan δ 值略高，刚性基团摩擦增加

---

## 文献来源

- **DOI**: 10.1002/app.28621
- **数据表格引用**: Table II; Fig.5(c), 6(c)
