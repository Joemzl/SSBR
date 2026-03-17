---
sample_id: SSBR-020
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
    value: 2.5
    range: null
    unit: MPa
    source: "Table 4"
  stress_200:
    value: 7.8
    range: null
    unit: MPa
    source: "Table 4"
  stress_300:
    value: null
    range: null
    unit: MPa
    source: ""
  tensile_strength:
    value: 15.6
    range: null
    unit: MPa
    source: "Table 4"
  elongation:
    value: 290
    range: null
    unit: "%"
    source: "Table 4"
  mechanical_source: "Table 4"
  hardness:
    value: 64
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
    note: "高于 blank，优于 one-step"
  tan_delta_60c:
    value: null
    unit: "-"
    source: "Figure 7"
    note: "低于 blank，与 one-step 相近"
---

# SSBR-020 力学性能解读

## 样本信息

- **样本编号**: SSBR-020
- **官能化试剂**: TMPMP (三羟甲基丙烷三巯基丙酸酯)
- **官能化策略**: Two-step (两步法)
- **体系**: SiR/SSBR 共混物 (SiR 20 phr / SSBR 80 phr)

## 一、应力-应变性能

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 100% 定伸应力 | 2.5 | MPa | Table 4 |
| 200% 定伸应力 | 7.8 | MPa | Table 4 |
| 拉伸强度 | 15.6 | MPa | Table 4 |
| 断裂伸长率 | 290 | % | Table 4 |
| 邵氏硬度 | 64 | Shore A | Table 4 |

### 与对照组对比

| 样本 | 拉伸强度 (MPa) | 伸长率 (%) | 100% 应力 (MPa) | 200% 应力 (MPa) |
|------|---------------|-----------|----------------|----------------|
| blank (无 TMPMP) | 14.7 | 368 | 1.9 | 5.5 |
| SSBR-017 (one-step) | 14.1 | 264 | 2.6 | 8.4 |
| **SSBR-020 (two-step)** | **15.6** | **290** | **2.5** | **7.8** |

### 核心发现

1. **拉伸强度提升**: 从 blank 的 14.7 MPa 提升至 15.6 MPa，提高 6%
2. **模量适度提升**: 100% 和 200% 定伸应力分别提高了 32% 和 42%
3. **伸长率保持较好**: 断裂伸长率 290%，优于 one-step 的 264%

### 分析结论

Two-step 工艺的优势在于：
1. **第一步**: TMPMP 先与 SiR 反应（170℃，15 min），形成带有悬挂巯基的 T-SiR
2. **第二步**: T-SiR 的悬挂巯基再与 SSBR 的乙烯基反应，形成 SiR-SSBR 化学偶联

这种策略确保 TMPMP 优先修饰 SiR，避免了 one-step 工艺中 TMPMP 倾向于交联 SSBR 的问题，从而提高了 SiR/SSBR 界面相互作用，实现了强度和模量的同时提升。

## 二、动态力学性能（DMA温度扫描）

### 核心发现

文献 Figure 7 显示 two-step 复合材料具有：
- **更低的 tan δ @ 60℃**: 对应更低的滚动阻力
- **更高的 tan δ @ 0℃**: 对应更高的湿地抓地力

### 轮胎性能指标

相比 blank：
- **湿地抓地力 (tan δ @ 0℃)**: 提高
- **滚动阻力 (tan δ @ 60℃)**: 降低

文献明确指出："The two-step composite showed lower tan δ at 60 °C and higher tan δ at 0 °C compared to those of the blank, which correlated to lower rolling resistance and higher wet-skid resistance when the compound was used as treads."

### 分析结论

Two-step 工艺通过化学偶联增强了 SiR/SSBR 界面相互作用，降低了界面摩擦导致的能量损失。在轮胎应用中，这意味着更好的滚动阻力与湿地抓地力的平衡。

## 三、综合评价

| 评价维度 | 评分 | 说明 |
|----------|------|------|
| 模量提升 | ★★★★☆ | 适度提高 |
| 强度保持 | ★★★★★ | 反而提升 |
| 韧性保持 | ★★★☆☆ | 伸长率下降 21% |
| 滚动阻力 | ★★★★★ | 显著降低 |
| 湿地抓地 | ★★★★☆ | 提高 |

**总体评价**: Two-step 工艺是本研究的核心创新。通过先让 TMPMP 与 SiR 反应形成 T-SiR，再让悬挂的巯基与 SSBR 偶联，成功实现了 SiR/SSBR 界面化学偶联。复合材料同时展现了更高的拉伸强度、适度的模量提升、以及优异的滚阻/抓地力平衡。

**应用建议**: 适用于轮胎胎面配方，可部分替代石油基橡胶（如 cis-BR），降低滚动阻力和磨耗。
