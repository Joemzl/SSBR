---
sample_id: SSBR-043
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
    value: 4.6
    range: null
    unit: MPa
    source: "Table II"
  tensile_strength:
    value: 11.9
    range: null
    unit: MPa
    source: "Table II"
  elongation:
    value: 489
    range: null
    unit: "%"
    source: "Table II"
  tear_strength:
    value: 25.5
    range: null
    unit: "kN/m"
    source: "Table II"
  hardness:
    value: 57
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

# 力学性能解读：SSBR-043

> **样本性质**: N-SSBR/SiO2 共凝聚纳米复合材料（YK-2-2），采用 AMMO 硅烷偶联剂改性，20 phr 纳米白炭黑填充

## 一、基础信息

- **样本ID**: SSBR-043
- **文献中编号**: YK-2-2（N-SSBR/SiO2 纳米复合材料）
- **基体**: YK-2 星形 SSBR（苯乙烯含量 24.2%，乙烯基含量 46.0%）
- **官能化试剂**: AMMO（[3-(2-氨基乙基)氨基丙基]三甲氧基硅烷）
- **填料用量**: 20 phr 纳米白炭黑（平均粒径 20-40 nm）
- **制备方法**: 共凝聚法（co-coagulation）
- **文献DOI**: 10.1002/app.28621

## 二、静态力学性能（应力-应变曲线）

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 300%定伸应力 | 4.6 | MPa | Table II |
| 拉伸强度 | 11.9 | MPa | Table II |
| 断裂伸长率 | 489 | % | Table II |
| 撕裂强度 | 25.5 | kN/m | Table II |
| 邵氏A硬度 | 57 | - | Table II |

### 与对照组对比

| 样本 | 300%应力 (MPa) | 拉伸强度 (MPa) | 伸长率 (%) | 撕裂强度 (kN/m) |
|------|----------------|----------------|------------|-----------------|
| YK-2-2 (N-SSBR/SiO2) | 4.6 | 11.9 | 489 | 25.5 |
| YK-2-1 (SSBR/SiO2) | 3.9 | 10.3 | 538 | 23.7 |
| 变化 | +17.9% | +15.5% | -9.1% | +7.6% |

### 核心发现

SSBR-043 (YK-2-2) 是三种样本中**综合力学性能最优**的：
- 拉伸强度 11.9 MPa，**最高**
- 300%定伸应力 4.6 MPa，**最高**
- 撕裂强度 25.5 kN/m，**最高**

### YK-2 的结构优势

文献指出 YK-2 具有较高的撕裂强度：
> "YK-2-1 and YK-2-2 have relatively higher tear strength than other two series of samples. It is possibly because higher vinyl content of YK-2 leads to increasing chain tear resistance."

YK-2 的高乙烯基含量（46.0%）提高了分子链的撕裂抗性。

---

## 三、动态力学性能（Payne效应）

### 核心发现

文献 Fig.5(b) 显示：
1. **Payne 效应降低**: N-SSBR/SiO2 的 ΔG' 低于 SSBR/SiO2
2. **填料分散改善**: 较低的 Payne 效应表明更好的填料分散

### tan δ-应变曲线分析

文献 Fig.6(b) 显示 YK-2-2 的 tan δ 值在全应变范围内均低于 YK-2-1，表明：
- 内摩擦损耗降低
- 界面滑移减少

---

## 四、动态力学性能（DMA温度扫描）

### 核心发现

文献 Fig.4(b) 显示：
1. **Tg 升高 ~2℃**: N-SSBR/SiO2 的玻璃化转变温度比 SSBR/SiO2 高约 2℃
2. **Tg 和湿地抓地力最高**: YK-2 系列因高乙烯基含量而具有最高的 Tg

文献指出：
> "the glass-transition temperature and tan δ values at 0°C (i.e., wet-skid resistance) of YK-2-1 and YK-2-2 are higher than those of corresponding YK-1-1 and YK-1-2, respectively. It is possibly because YK-2 has higher vinyl content than YK-1 so the macromolecular chains are hard to relax."

### 轮胎应用性能分析

- **湿地抓地力**: YK-2-2 在 0℃ 的 tan δ 值高于 YK-1-2，表明更好的湿地抓地性能
- **高乙烯基的优势**: 高乙烯基含量使分子链难以松弛，提高 Tg 和湿地抓地力

---

## 五、与其他样本对比

### 三种 N-SSBR/SiO2 样本力学性能对比

| 指标 | YK-1-2 | **YK-2-2** | YK-3-2 |
|------|--------|------------|--------|
| 苯乙烯含量 | 21.1% | **24.2%** | 29.5% |
| 乙烯基含量 | 38.1% | **46.0%** | 34.7% |
| 300%应力 (MPa) | 3.7 | **4.6** | 3.7 |
| 拉伸强度 (MPa) | 10.7 | **11.9** | 10.3 |
| 伸长率 (%) | 522 | 489 | 455 |
| 撕裂强度 (kN/m) | 21.5 | **25.5** | 22.2 |

**YK-2-2 (SSBR-043)** 在强度和撕裂性能上均优于其他两种样本。

---

## 六、综合评价

SSBR-043 (YK-2-2) 是该系列中综合性能最优的样品：
- ✅ 最高拉伸强度（11.9 MPa）
- ✅ 最高撕裂强度（25.5 kN/m）
- ✅ 最高 300%定伸应力（4.6 MPa）
- ✅ Payne 效应降低，动态性能改善
- ✅ 高乙烯基含量带来的优异湿地抓地力

---

## 文献来源

- **DOI**: 10.1002/app.28621
- **数据表格引用**: Table II; Fig.4(b), 5(b), 6(b)
