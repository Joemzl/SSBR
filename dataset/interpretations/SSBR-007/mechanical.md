---
# SSBR-007 力学性能解读
sample_id: SSBR-007
test_type: mechanical
data_source: "10.1002/app.41182"
data_quality: L2

# 复合材料体系
composite_system:
  matrix: "S-EB-S/S-SBR TPV (50/50 wt%)"
  filler: null
  filler_loading: null
  coupling_agent: null
  processing: "动态硫化 (160°C, 60 rpm)"

# 拉伸测试数据 (Table II, III)
tensile_properties:
  # SEV 硫化体系 (SST 1)
  SST1:
    tensile_strength:
      value: 4.9
      unit: "MPa"
      std: 0.62
    elongation_at_break:
      value: 672
      unit: "%"
      std: 79.79
    modulus_100:
      value: 0.9
      unit: "MPa"
    modulus_200:
      value: 1.4
      unit: "MPa"
    modulus_300:
      value: 2.0
      unit: "MPa"
    hardness:
      value: 52
      unit: "Shore A"
  # EV 硫化体系 (SST 2)
  SST2:
    tensile_strength:
      value: 4.8
      unit: "MPa"
      std: 0.38
    elongation_at_break:
      value: 533
      unit: "%"
      std: 42.03
    modulus_100:
      value: 1.1
      unit: "MPa"
    modulus_200:
      value: 1.7
      unit: "MPa"
    modulus_300:
      value: 2.6
      unit: "MPa"
    hardness:
      value: 55
      unit: "Shore A"

# 流变性能 (Fig. 7, 8)
rheological_properties:
  test_temperature: "120°C"
  complex_modulus_frequency:
    description: "G* 随频率增加而增加"
    trend: "EV 体系 (SST 2) > SEV 体系 (SST 1)"
    frequency_range: "0.5-32 Hz"
  complex_modulus_strain:
    description: "Payne 类效应"
    trend: "EV 体系模量更高"
    strain_range: "0.7-1250%"
  complex_viscosity:
    description: "假塑性行为，g* 随频率增加而降低"
    trend: "交联密度越高，初始粘度越高"

# 动态力学分析
dma_properties:
  creep_study:
    test_temperature: "25°C"
    constant_stress: "0.3 MPa"
    observation: "SEV 体系再加工后蠕变柔量显著降低"
  stress_relaxation:
    test_temperature: "25°C"
    constant_strain: "0.05%"
    observation: "SEV 体系再加工后应力松弛模量增加"
  storage_modulus_25C:
    SSBR_vulcanizate: 2.79
    SEB_S: 4.50
    SST1: 3.41
    SST2: 3.90
    unit: "MPa"

# 交联密度 (Fig. 2)
crosslink_density:
  SEV_system:
    initial: "~7.1e-5"
    after_reprocessing: "~7.9e-5"
    unit: "mol/mL"
    change: "+0.8e-5 mol/mL"
  EV_system:
    initial: "~8.5e-5"
    after_reprocessing: "~8.6e-5"
    unit: "mol/mL"
    change: "~0.1e-5 mol/mL (marginal)"
---

## 力学性能解读

### 概述

SSBR-007 来自 S-EB-S/S-SBR (50/50 wt%) 热塑性硫化橡胶（TPV）体系。该文献研究了半有效硫化（SEV）和有效硫化（EV）两种硫化体系对 TPV 力学性能和再加工性的影响。S-SBR 是未官能化的工业级产品（苯乙烯含量 23.5 wt%），来源于 Dycon Chemicals。

### 拉伸性能比较

两种硫化体系的 TPV 表现出相似的拉伸强度（~4.8-4.9 MPa），但 SEV 体系（SST 1）的断裂伸长率（672%）显著高于 EV 体系（533%），提高了 26%。这是由于：

1. **交联结构差异**：SEV 体系形成二硫键和多硫键（键能较低），而 EV 体系主要形成单硫键（键能较高）
2. **形态学差异**：SEV 体系形成共连续形态并带有拉长的橡胶粒子，有利于延展性

### 流变行为

复数剪切模量（G*）随频率增加而增加，这是由于在高频下分子链无法跟随外加应变，表现出类似橡胶的弹性行为。EV 体系由于具有更高的交联密度，G* 值更高。

在应变扫描中观察到类 Payne 效应，这是由于橡胶网络贡献的应变无关效应，与交联密度成正比。

### 再加工性能

SEV 体系在再加工后力学性能改善：
- 拉伸强度：4.9 → 6.3 MPa（+29%）
- 交联密度增加 0.8×10⁻⁵ mol/mL

这归因于 SEV 体系的后固化效应超过了热/机械降解的影响。

### 关键发现

1. 在 TPV 应用中，SEV 硫化体系提供更好的断裂伸长率和再加工性
2. 交联密度和形态演变决定了 TPV 的最终性能
3. 该体系无填料，性能完全来自橡胶网络和共混物形态

### 数据来源

- Table II: 硫化 TPV 的力学性能
- Table III: 再加工后的力学性能
- Fig. 7: 复数模量-频率曲线
- Fig. 8: 复数模量-应变曲线
- Fig. 10: 复数粘度-频率曲线
- Fig. 11: 储能模量-温度曲线
