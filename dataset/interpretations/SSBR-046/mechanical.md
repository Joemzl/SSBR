---
# SSBR-046 力学性能解读
sample_id: SSBR-046
test_type: mechanical
data_source: "10.1002/app.32372"
data_quality: L1

# 复合材料体系
composite_system:
  matrix: "SSBR (YL950)"
  filler_type: "SiO₂/CB 双相填料"
  total_filler_loading: "70 phr"
  filler_ratios:
    - "0/70 (纯 CB)"
    - "20/50"
    - "35/35"
    - "50/20"
    - "70/0 (纯 SiO₂)"
  coupling_agent: "Si-75 (7% of SiO₂ mass)"
  processing: "反应共混 (Haake, 150°C, 4min)"

# 拉伸测试数据 (Table II)
tensile_properties:
  SiO2_CB_0_70:
    modulus_300:
      value: 11.6
      unit: "MPa"
    tensile_strength:
      value: 17.3
      unit: "MPa"
    elongation_at_break:
      value: 356
      unit: "%"
    hardness:
      value: 68
      unit: "Shore A"
    tear_strength:
      value: 46.6
      unit: "kN/m"
  SiO2_CB_20_50:
    modulus_300:
      value: 18.3
      unit: "MPa"
    tensile_strength:
      value: 22.8
      unit: "MPa"
    elongation_at_break:
      value: 378
      unit: "%"
    hardness:
      value: 68
      unit: "Shore A"
    tear_strength:
      value: 48.1
      unit: "kN/m"
  SiO2_CB_35_35:
    modulus_300:
      value: 15.6
      unit: "MPa"
    tensile_strength:
      value: 22.2
      unit: "MPa"
    elongation_at_break:
      value: 409
      unit: "%"
    hardness:
      value: 65
      unit: "Shore A"
    tear_strength:
      value: 57.9
      unit: "kN/m"
  SiO2_CB_50_20:
    modulus_300:
      value: 15.1
      unit: "MPa"
    tensile_strength:
      value: 21.5
      unit: "MPa"
    elongation_at_break:
      value: 454
      unit: "%"
    hardness:
      value: 65
      unit: "Shore A"
    tear_strength:
      value: 50.7
      unit: "kN/m"
  SiO2_CB_70_0:
    modulus_300:
      value: 12.8
      unit: "MPa"
    tensile_strength:
      value: 20.3
      unit: "MPa"
    elongation_at_break:
      value: 402
      unit: "%"
    hardness:
      value: 64
      unit: "Shore A"
    tear_strength:
      value: 46.9
      unit: "kN/m"

# 磨耗性能 (Table II)
abrasion_properties:
  test_method: "Akron 磨耗"
  SiO2_CB_0_70: "0.3695 cm³/1.61km"
  SiO2_CB_20_50: "0.2560 cm³/1.61km (最佳)"
  SiO2_CB_35_35: "0.2783 cm³/1.61km"
  SiO2_CB_50_20: "0.2946 cm³/1.61km"
  SiO2_CB_70_0: "0.3576 cm³/1.61km"

# 动态压缩生热 (Table II)
heat_buildup:
  SiO2_CB_0_70: "20.1°C"
  SiO2_CB_20_50: "16.9°C"
  SiO2_CB_35_35: "16.7°C"
  SiO2_CB_50_20: "15.5°C"
  SiO2_CB_70_0: "10.7°C (最低)"

# 滚动功率损失 (Table IV)
rolling_power_loss:
  SiO2_CB_0_70: "4.26 J/r"
  SiO2_CB_20_50: "2.62 J/r (最低)"
  SiO2_CB_35_35: "2.97 J/r"
  SiO2_CB_50_20: "3.70 J/r"
  SiO2_CB_70_0: "3.23 J/r"

# Payne 效应 (Fig. 3)
payne_effect:
  test_conditions:
    temperature: "60°C"
    strain_range: "0.28-42%"
    frequency: "10 Hz"
  observation: "SiO₂/CB 双相填料复合材料 Payne 效应最低，20/50 配比最佳"
  DG_trend: "0/70 > 70/0 > 35/35 > 50/20 > 20/50"
---

## 力学性能解读

### 概述

SSBR-046 来自一项研究 SSBR/SiO₂/CB 复合材料结构-性能关系的工作。研究使用燕山石化 YL950 型 SSBR（苯乙烯 27.5 wt%，乙烯基 25.4 mol%），通过反应共混技术制备了不同 SiO₂/CB 配比的复合材料，系统研究了"魔三角"（滚动阻力、湿抓地力、耐磨性）的平衡问题。

### 拉伸性能分析

#### 最佳配方：SiO₂/CB = 20/50

| 性能指标 | 纯 CB (0/70) | **20/50** | 35/35 | 纯 SiO₂ (70/0) |
|----------|-------------|-----------|-------|----------------|
| 300% 模量 (MPa) | 11.6 | **18.3** | 15.6 | 12.8 |
| 拉伸强度 (MPa) | 17.3 | **22.8** | 22.2 | 20.3 |
| 断裂伸长率 (%) | 356 | 378 | 409 | 402 |
| 撕裂强度 (kN/m) | 46.6 | 48.1 | **57.9** | 46.9 |

**关键发现**：SiO₂/CB 双相填料复合材料表现出"协同效应"，当配比为 20/50 时综合力学性能最佳。

#### 协同增强机理

1. **纳米级分散**：双相填料显著削弱单一填料形成的网络
2. **填料-橡胶相互作用增强**：Si-75 偶联剂改善 SiO₂ 与 SSBR 的相容性
3. **剪切场增强**：少量 SiO₂ 预混提高混炼粘度，增强 CB 分散

### Payne 效应分析

Payne 效应（G' 随应变降低）反映填料分散状态：

| 体系 | ΔG' 大小 | 分散评价 |
|------|---------|---------|
| 0/70 (纯 CB) | **最大** | 差（聚集严重）|
| 70/0 (纯 SiO₂) | 较大 | 一般 |
| 35/35 | 中等 | 良好 |
| 50/20 | 较小 | 良好 |
| 20/50 | **最小** | **最佳** |

### 动态力学性能

tan δ - 应变曲线显示：
- 纯 SiO₂ 体系在低应变（<10%）时 tan δ 最低
- 高应变时纯 SiO₂ 的 tan δ 急剧增加（填料网络破坏）
- 双相填料体系在全应变范围内 tan δ 较低且稳定

### 轮胎性能预测

| 性能 | 评价指标 | 最佳配方 |
|------|---------|---------|
| 低滚动阻力 | tan δ (60°C) 低 | 20/50 (0.11) |
| 高湿抓地力 | tan δ (0°C) 高 | 20/50 (0.23) |
| 高耐磨性 | 磨耗量低 | 20/50 (0.256 cm³/1.61km) |
| 低生热 | 压缩生热低 | 70/0 (10.7°C) |

**结论**：SiO₂/CB = 20/50 配方实现了"魔三角"性能的最佳平衡。

### 滚动功率损失

滚动功率损失模拟轮胎在路面运动时的能量损耗：

- 纯 CB 体系：4.26 J/r（最高）
- 20/50 配方：**2.62 J/r**（最低，降低 38%）
- 纯 SiO₂ 体系：3.23 J/r

这与 tan δ 在 15-30% 应变范围的趋势一致。

### 数据来源

- Table II: 硫化和力学性能
- Table IV: 滚动过程功率损失
- Fig. 3: G'-应变和 tan δ-应变曲线
- Fig. 4: tan δ-温度曲线
