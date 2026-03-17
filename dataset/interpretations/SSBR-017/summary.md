---
sample_id: SSBR-017
interpretation_type: summary
source_doi: "10.1021/acs.iecr.6b04146"
created_at: 2026-03-18
updated_at: null

# ===== 核心标识 =====
functionalization_reagent: "TMPMP"
functionalization_reagent_full: "三羟甲基丙烷三(3-巯基丙酸酯)"
core_functional_group: "巯基 (-SH)"
reaction_mechanism: "巯基-烯点击反应 (thiol-ene click)"
strategy: "One-step (一步法)"

# ===== 关键性能指标 =====
performance_summary:
  tensile_strength:
    value: 14.1
    unit: "MPa"
    change_vs_control: "-4%"
  elongation:
    value: 264
    unit: "%"
    change_vs_control: "-28%"
  stress_100:
    value: 2.6
    unit: "MPa"
    change_vs_control: "+37%"
  stress_200:
    value: 8.4
    unit: "MPa"
    change_vs_control: "+53%"
  wet_grip: "略有提高"
  rolling_resistance: "降低"

# ===== 界面作用机制 =====
interface_interaction:
  type: "共价键 + 交联网络"
  mechanism: "TMPMP 三巯基与 SSBR 乙烯基的点击反应"
  limitation: "TMPMP 倾向于交联 SSBR 而非偶联 SiR/SSBR 界面"

# ===== 数据完整性 =====
data_availability:
  mechanical: true
  dsc: false
  nmr: false
  tem: false
  note: "文献未提供 one-step 样品的 TEM 图像"
---

# SSBR-017 综合档案

## 一句话总结

> TMPMP 一步法官能化 SSBR，显著提升模量但伸长率下降，适用于需要高刚度的 SiR/SSBR 共混体系。

## 样本概要

| 属性 | 值 |
|------|-----|
| 样本编号 | SSBR-017 |
| 官能化试剂 | TMPMP (三羟甲基丙烷三巯基丙酸酯) |
| 核心官能团 | 三巯基 (-SH)₃ |
| 反应机理 | 巯基-烯点击反应 |
| 官能化策略 | One-step (一步法) |
| 体系 | SiR/SSBR 共混物 (20/80 phr) |
| DOI | 10.1021/acs.iecr.6b04146 |

## 核心性能数据

### 力学性能

| 指标 | 数值 | 对比 blank | 来源 |
|------|------|-----------|------|
| 100% 定伸应力 | 2.6 MPa | +37% | Table 4 |
| 200% 定伸应力 | 8.4 MPa | +53% | Table 4 |
| 拉伸强度 | 14.1 MPa | -4% | Table 4 |
| 伸长率 | 264% | -28% | Table 4 |
| 邵氏硬度 | 63 Shore A | 持平 | Table 4 |

### 动态力学性能

| 指标 | 表现 | 轮胎意义 |
|------|------|----------|
| tan δ @ 0℃ | 略高于 blank | 湿地抓地力提升 |
| tan δ @ 60℃ | 低于 blank | 滚动阻力降低 |

## 技术要点

### 优势
1. 模量显著提升 (+37%~53%)
2. 动态性能改善（低滚阻、高抓地力）
3. 工艺简单（一步法）

### 局限性
1. 伸长率明显下降 (-28%)
2. 拉伸强度略降 (-4%)
3. TMPMP 优先与 SSBR 反应，界面偶联效率低

### 机理分析

One-step 工艺的问题：
- SSBR 乙烯基含量 (41.3 wt%) >> SiR 乙烯基含量 (0.15 mol%)
- TMPMP 巯基/SSBR 乙烯基摩尔比 = 1:101 (巯基不足)
- 结果：TMPMP 倾向于交联 SSBR，而非偶联 SiR/SSBR 界面

## 应用建议

✓ 适用场景:
- 需要高模量的 SiR/SSBR 共混体系
- 对韧性要求不高的制品

✗ 不适用场景:
- 需要高伸长率的应用
- 追求最佳界面偶联效果（建议使用 two-step 工艺）

## 相关样本

- **SSBR-020**: 同一文献的 two-step 工艺样本，界面偶联效果更优

## 关键词

`TMPMP` `巯基-烯点击` `SiR/SSBR共混` `一步法` `界面偶联` `高模量` `轮胎胎面`
