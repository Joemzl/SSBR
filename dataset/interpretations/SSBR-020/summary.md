---
sample_id: SSBR-020
interpretation_type: summary
source_doi: "10.1021/acs.iecr.6b04146"
created_at: 2026-03-18
updated_at: null

# ===== 核心标识 =====
functionalization_reagent: "TMPMP"
functionalization_reagent_full: "三羟甲基丙烷三(3-巯基丙酸酯)"
core_functional_group: "巯基 (-SH)"
reaction_mechanism: "巯基-烯点击反应 (thiol-ene click)"
strategy: "Two-step (两步法)"

# ===== 关键性能指标 =====
performance_summary:
  tensile_strength:
    value: 15.6
    unit: "MPa"
    change_vs_control: "+6%"
  elongation:
    value: 290
    unit: "%"
    change_vs_control: "-21%"
  stress_100:
    value: 2.5
    unit: "MPa"
    change_vs_control: "+32%"
  stress_200:
    value: 7.8
    unit: "MPa"
    change_vs_control: "+42%"
  wet_grip: "提高"
  rolling_resistance: "显著降低"

# ===== 界面作用机制 =====
interface_interaction:
  type: "共价键 (化学偶联)"
  mechanism: "SiR-S-CH₂-SSBR 化学桥连"
  evidence: "TEM 图像显示模糊界面 (misty interface)"

# ===== 数据完整性 =====
data_availability:
  mechanical: true
  dsc: false
  nmr: false
  tem: true
---

# SSBR-020 综合档案

## 一句话总结

> TMPMP 两步法实现 SiR/SSBR 界面化学偶联，同时提升强度和模量，是改善不相容橡胶共混体系的创新策略。

## 样本概要

| 属性 | 值 |
|------|-----|
| 样本编号 | SSBR-020 |
| 官能化试剂 | TMPMP (三羟甲基丙烷三巯基丙酸酯) |
| 核心官能团 | 三巯基 (-SH)₃ |
| 反应机理 | 巯基-烯点击反应 |
| 官能化策略 | Two-step (两步法) ⭐ 核心创新 |
| 体系 | SiR/SSBR 共混物 (20/80 phr) |
| DOI | 10.1021/acs.iecr.6b04146 |

## 核心性能数据

### 力学性能

| 指标 | 数值 | 对比 blank | 对比 one-step | 来源 |
|------|------|-----------|---------------|------|
| 100% 定伸应力 | 2.5 MPa | +32% | -4% | Table 4 |
| 200% 定伸应力 | 7.8 MPa | +42% | -7% | Table 4 |
| 拉伸强度 | **15.6 MPa** | **+6%** | +11% | Table 4 |
| 伸长率 | 290% | -21% | +10% | Table 4 |
| 邵氏硬度 | 64 Shore A | +1 | +1 | Table 4 |

### 动态力学性能

| 指标 | 表现 | 轮胎意义 |
|------|------|----------|
| tan δ @ 0℃ | 高于 blank | **湿地抓地力提升** |
| tan δ @ 60℃ | 低于 blank | **滚动阻力降低** |

文献明确指出：
> "The two-step composite showed lower tan δ at 60 °C and higher tan δ at 0 °C compared to those of the blank, which correlated to lower rolling resistance and higher wet-skid resistance."

### TEM 形貌

| 特征 | blank | two-step |
|------|-------|----------|
| SiR 域尺寸 | > 100 nm | 显著减小 |
| 界面 | 清晰（相分离） | **模糊 (misty)** |
| 白炭黑分散 | 差 | 改善 |
| 透光性 | 低 | 高 |

## 技术要点

### 两步法核心创新

```
Step 1: SiR + TMPMP → T-SiR (带悬挂 -SH 基)
        (170°C, 15 min)
        
Step 2: T-SiR (-SH) + SSBR (C=C) → SiR-S-SSBR
        (原位界面偶联)
```

### 优势
1. **强度和模量同时提升** - 罕见的双赢结果
2. **界面化学偶联** - TEM 显示模糊界面
3. **相分离改善** - SiR 域尺寸减小
4. **优异的动态性能** - 低滚阻 + 高抓地力
5. **填料分散改善** - 白炭黑分散更均匀

### 为什么 Two-step 优于 One-step?

| 对比项 | One-step | Two-step |
|--------|----------|----------|
| TMPMP 反应对象 | 主要与 SSBR 反应 | 先与 SiR 反应 |
| 界面偶联效率 | 低 | **高** |
| 拉伸强度 | ↓ | **↑** |
| 伸长率 | ↓↓ | ↓ |

## 应用建议

✓ 适用场景:
- 轮胎胎面配方（低滚阻 + 高抓地力）
- SiR/SSBR 不相容共混体系
- 需要部分替代石油基橡胶的绿色配方

✗ 注意事项:
- 需要两步混炼工艺，工艺复杂度略增
- 仍有 21% 的伸长率损失

## 相关样本

- **SSBR-017**: 同一文献的 one-step 工艺样本，作为对比组
- **SSBR-034**: 另一篇使用 TMPMP 的文献（单独 SSBR 体系）

## 关键词

`TMPMP` `巯基-烯点击` `SiR/SSBR共混` `两步法` `界面偶联` `模糊界面` `低滚阻` `高抓地力` `轮胎胎面` `绿色橡胶`
