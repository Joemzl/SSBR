---
sample_id: SSBR-017
interpretation_type: mechanical
source_figure: "Table 4, Figure 7"
source_doi: "10.1021/acs.iecr.6b04146"
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: null
mechanical_subtypes:
  - stress-strain
  - dma

data:
  # ========== 应力-应变数据 ==========
  stress_100:
    value: 2.6
    range: null
    unit: MPa
    source: "Table 4"
  stress_200:
    value: 8.4
    range: null
    unit: MPa
    source: "Table 4"
  stress_300:
    value: null
    range: null
    unit: MPa
    source: ""
  tensile_strength:
    value: 14.1
    range: null
    unit: MPa
    source: "Table 4"
  elongation:
    value: 264
    range: null
    unit: "%"
    source: "Table 4"
  mechanical_source: "Table 4"
  hardness:
    value: 63
    unit: "Shore A"
    source: "Table 4"
  
  # ========== DMA 数据 ==========
  tg_dma:
    value: null
    unit: "℃"
    source: "Figure 7"
    note: "从 Figure 7 曲线可见 SSBR 的 Tg 峰在约 -20℃ 附近"
  tan_delta_0c:
    value: null
    unit: "-"
    source: "Figure 7"
    note: "从曲线估读，高于 blank"
  tan_delta_60c:
    value: null
    unit: "-"
    source: "Figure 7"
    note: "从曲线估读，低于 blank"
---

# SSBR-017 力学性能解读

## 样本信息

- **样本编号**: SSBR-017
- **官能化试剂**: TMPMP (三羟甲基丙烷三巯基丙酸酯)
- **官能化策略**: One-step (一步法)
- **体系**: SiR/SSBR 共混物 (SiR 20 phr / SSBR 80 phr)

## 一、应力-应变性能

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100% 定伸应力 | 2.6 | MPa | Table 4 |
| 200% 定伸应力 | 8.4 | MPa | Table 4 |
| 拉伸强度 | 14.1 | MPa | Table 4 |
| 断裂伸长率 | 264 | % | Table 4 |
| 邵氏硬度 | 63 | Shore A | Table 4 |

### 与对照组对比

| 样本 | 拉伸强度 (MPa) | 伸长率 (%) | 100% 应力 (MPa) | 200% 应力 (MPa) |
|------|---------------|-----------|----------------|----------------|
| blank (无 TMPMP) | 14.7 | 368 | 1.9 | 5.5 |
| **SSBR-017 (one-step)** | **14.1** | **264** | **2.6** | **8.4** |
| SSBR-020 (two-step) | 15.6 | 290 | 2.5 | 7.8 |

### 核心发现

1. **模量显著提升**: 100% 和 200% 定伸应力分别提高了 37% 和 53%，表明 TMPMP 有效交联了 SSBR
2. **伸长率下降**: 断裂伸长率从 368% 下降到 264%，降幅 28%
3. **拉伸强度略降**: 从 14.7 MPa 降至 14.1 MPa，这是由于 TMPMP 倾向于交联 SSBR 而非偶联 SiR/SSBR 界面

### 分析结论

One-step 工艺中，由于 SSBR 的乙烯基含量（41.3 wt%）远高于 SiR（0.15 mol%），TMPMP 优先与 SSBR 反应，形成过度交联的 SSBR 网络，导致应力集中增加、伸长率下降。

## 二、动态力学性能（DMA温度扫描）

### 核心发现

文献 Figure 7 显示：
- SSBR 的玻璃化转变峰位置在三种配方间无显著差异
- One-step 复合材料在高温区的 tan δ 低于 blank，归因于更强的界面相互作用降低了界面摩擦

### 轮胎性能指标

相比 blank：
- **湿地抓地力 (tan δ @ 0℃)**: 略有提高
- **滚动阻力 (tan δ @ 60℃)**: 降低

### 分析结论

尽管 one-step 工艺提升了模量，但由于 TMPMP 倾向于交联 SSBR 而非偶联 SiR/SSBR 界面，其对界面相互作用的改善效果弱于 two-step 工艺。

## 三、综合评价

| 评价维度 | 评分 | 说明 |
|----------|------|------|
| 模量提升 | ★★★★☆ | 显著提高 |
| 强度保持 | ★★★☆☆ | 略有下降 |
| 韧性保持 | ★★☆☆☆ | 伸长率明显下降 |
| 滚动阻力 | ★★★★☆ | 有所降低 |
| 湿地抓地 | ★★★☆☆ | 略有提高 |

**总体评价**: One-step 工艺通过 TMPMP 提升了复合材料的模量和动态性能，但由于 TMPMP 优先与高乙烯基含量的 SSBR 反应，导致交联效率高于界面偶联效率，伸长率下降明显。适用于需要高模量但对韧性要求不高的场合。
