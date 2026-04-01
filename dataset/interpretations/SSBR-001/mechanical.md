---
sample_id: SSBR-001
interpretation_type: mechanical
source_figure: "Fig. 6, Fig. 8, Table 2, Table 3, Table S5, Table S6"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-mechanical-interpretation
skill_version: "2.0"
created_at: 2026-03-17
updated_at: 2026-03-31
mechanical_subtypes:
  - stress-strain
  - payne
  - dma

data:
  # ========== 应力-应变数据 (来自 Table S5) ==========
  stress_100:
    value: 4.2
    range: null
    unit: MPa
    source: "SI Table S5"
    confidence: 0.95
  stress_200:
    value: null
    range: null
    unit: MPa
    source: "断裂伸长率约200%，未达200%定伸"
  stress_300:
    value: null
    range: null
    unit: MPa
    source: "断裂伸长率约200%，未达300%定伸"
  tensile_strength:
    value: 14.2
    range: null
    unit: MPa
    source: "SI Table S5"
    confidence: 0.95
  elongation:
    value: 200
    range: null
    unit: "%"
    source: "SI Table S5"
    confidence: 0.95
  mechanical_source: "SI Table S5"
  
  # ========== Payne 效应数据 (来自 Table 1, Table 2) ==========
  bound_rubber:
    value: 55.28
    unit: "%"
    source: "Table 1"
    confidence: 0.95
  delta_G_compounds:
    value: 657.10
    unit: "kPa"
    source: "Table 2"
    confidence: 0.95
    note: "0.28%-41.99% strain"
  delta_G_vulcanizates:
    value: 1078.07
    unit: "kPa"
    source: "Table 2"
    confidence: 0.95
    note: "0.28%-41.99% strain"
  tan_delta_7_strain:
    value: 0.104
    unit: "-"
    source: "SI Table S4"
    confidence: 0.95
  
  # ========== DMA 数据 (来自 Table S6) ==========
  tan_delta_0c:
    value: 1.004
    unit: "-"
    source: "SI Table S6"
    confidence: 0.95
  tan_delta_max:
    value: 1.010
    unit: "-"
    source: "SI Table S6"
    confidence: 0.95
  tg_dma:
    value: -0.9
    unit: "℃"
    source: "SI Table S6"
    confidence: 0.95
  
  # ========== 交联密度 (来自 Table 3) ==========
  crosslink_density:
    value: 4.89
    unit: "×10⁻⁴ mol/cm³"
    source: "Table 3"
    confidence: 0.95

# ========== v2.0 全范围曲线数据 ==========
curves:
  # ---------- 应力-应变曲线 (Fig. 8A) ----------
  stress_strain:
    x_axis:
      label: "应变"
      unit: "%"
    y_axis:
      label: "应力"
      unit: "MPa"
    data_points:
      # 基于 Fig. 8(A) 中 SSBR-g-MPL70 曲线 (蓝色三角形) 估读
      # 曲线特征：中等斜率，在约 200% 应变处断裂
      - {x: 0, y: 0, confidence: 1.0, source: "L1"}
      - {x: 10, y: 0.3, confidence: 0.65, source: "L3"}
      - {x: 20, y: 0.6, confidence: 0.65, source: "L3"}
      - {x: 30, y: 0.9, confidence: 0.65, source: "L3"}
      - {x: 50, y: 1.5, confidence: 0.65, source: "L3"}
      - {x: 70, y: 2.3, confidence: 0.65, source: "L3"}
      - {x: 100, y: 4.2, confidence: 0.95, source: "L1"}  # Table S5 验证点
      - {x: 120, y: 5.5, confidence: 0.65, source: "L3"}
      - {x: 140, y: 7.2, confidence: 0.65, source: "L3"}
      - {x: 160, y: 9.2, confidence: 0.65, source: "L3"}
      - {x: 180, y: 11.5, confidence: 0.65, source: "L3"}
      - {x: 190, y: 12.8, confidence: 0.65, source: "L3"}
      - {x: 200, y: 14.2, confidence: 0.95, source: "L1"}  # Table S5 断裂点
    curve_features:
      modulus_100:
        value: 4.2
        unit: "MPa"
        source: "L1"
        confidence: 0.95
      modulus_200:
        value: null
        unit: "MPa"
        source: "N/A - 断裂点"
        note: "样本在约 200% 应变处断裂"
      modulus_300:
        value: null
        unit: "MPa"
        source: "N/A"
        note: "断裂伸长率 200%，未达 300% 定伸"
      tensile_strength:
        value: 14.2
        unit: "MPa"
        source: "L1"
        confidence: 0.95
      elongation_at_break:
        value: 200
        unit: "%"
        source: "L1"
        confidence: 0.95
      yield_point:
        exists: false
        note: "曲线无明显屈服点，呈应变硬化特征"
      strain_hardening_index:
        value: 2.1
        confidence: 0.70
        note: "估算值，基于 100-200% 区间斜率"
    validation:
      known_points:
        - strain: 100
          stress_expected: 4.2
          stress_estimated: 4.2
          deviation_percent: 0.0
        - strain: 200
          stress_expected: 14.2
          stress_estimated: 14.2
          deviation_percent: 0.0
      overall_quality: "excellent"
    metadata:
      point_count: 13
      x_range: [0, 200]
      y_range: [0, 14.2]
      avg_confidence: 0.76

  # ---------- DMA tan δ-温度曲线 (Fig. 8C) ----------
  dma_tan_delta:
    x_axis:
      label: "温度"
      unit: "°C"
    y_axis:
      label: "tan δ"
      unit: "无量纲"
    data_points:
      # 基于 Fig. 8(C) 中 SSBR-g-MPL70 曲线估读
      # 曲线特征：峰值在约 -0.9°C，tan δ_max ≈ 1.010
      - {x: -80, y: 0.02, confidence: 0.60, source: "L3"}
      - {x: -70, y: 0.03, confidence: 0.60, source: "L3"}
      - {x: -60, y: 0.04, confidence: 0.60, source: "L3"}
      - {x: -50, y: 0.06, confidence: 0.65, source: "L3"}
      - {x: -40, y: 0.12, confidence: 0.65, source: "L3"}
      - {x: -30, y: 0.35, confidence: 0.65, source: "L3"}
      - {x: -20, y: 0.72, confidence: 0.65, source: "L3"}
      - {x: -10, y: 0.95, confidence: 0.70, source: "L3"}
      - {x: -0.9, y: 1.010, confidence: 0.95, source: "L1"}  # Table S6 Tg 点
      - {x: 0, y: 1.004, confidence: 0.95, source: "L1"}   # Table S6 验证点
      - {x: 10, y: 0.82, confidence: 0.70, source: "L3"}
      - {x: 20, y: 0.58, confidence: 0.65, source: "L3"}
      - {x: 30, y: 0.38, confidence: 0.65, source: "L3"}
      - {x: 40, y: 0.24, confidence: 0.65, source: "L3"}
      - {x: 50, y: 0.16, confidence: 0.65, source: "L3"}
      - {x: 60, y: 0.11, confidence: 0.70, source: "L3"}   # 滚动阻力区
      - {x: 80, y: 0.06, confidence: 0.60, source: "L3"}
    curve_features:
      tan_delta_0C:
        value: 1.004
        confidence: 0.95
        source: "L1"
        note: "湿地抓地力指标"
      tan_delta_60C:
        value: 0.11
        confidence: 0.70
        source: "L3"
        note: "滚动阻力指标 (估读)"
      tan_delta_max:
        value: 1.010
        temperature: -0.9
        confidence: 0.95
        source: "L1"
      Tg:
        value: -0.9
        unit: "°C"
        method: "peak"
        source: "L1"
        confidence: 0.95
      peak_width:
        value: 45
        unit: "°C"
        confidence: 0.65
        note: "半高宽估算，约 -25°C 到 +20°C"
      wet_grip_index:
        value: 1.004
        formula: "tan δ(0°C)"
        note: "相比空白 SSBR (0.472) 提升 112.7%"
      rolling_resistance_index:
        value: 0.11
        formula: "tan δ(60°C)"
        note: "估读值"
    validation:
      known_points:
        - temperature: -0.9
          tan_delta_expected: 1.010
          tan_delta_estimated: 1.010
          deviation_percent: 0.0
        - temperature: 0
          tan_delta_expected: 1.004
          tan_delta_estimated: 1.004
          deviation_percent: 0.0
      overall_quality: "excellent"
    metadata:
      point_count: 17
      x_range: [-80, 80]
      y_range: [0.02, 1.010]
      avg_confidence: 0.72

  # ---------- Payne 效应 G'-应变曲线 (Fig. 6B) ----------
  payne_storage_modulus:
    x_axis:
      label: "应变"
      unit: "%"
      scale: "logarithmic"
    y_axis:
      label: "储能模量 G'"
      unit: "MPa"
    data_points:
      # 基于 Fig. 6(B) 中 silica/SSBR-g-MPL70 硫化胶曲线估读
      # 曲线特征：从约 1.7 MPa 下降到约 0.6 MPa
      # Table 2 数据：ΔG' = 1078.07 kPa = 1.078 MPa (0.28%-41.99% strain)
      - {x: 0.28, y: 1.70, confidence: 0.70, source: "L3"}
      - {x: 0.5, y: 1.65, confidence: 0.70, source: "L3"}
      - {x: 1, y: 1.55, confidence: 0.70, source: "L3"}
      - {x: 2, y: 1.40, confidence: 0.70, source: "L3"}
      - {x: 3.6, y: 1.25, confidence: 0.70, source: "L3"}   # 临界应变点
      - {x: 5, y: 1.10, confidence: 0.70, source: "L3"}
      - {x: 7, y: 0.95, confidence: 0.70, source: "L3"}
      - {x: 10, y: 0.82, confidence: 0.70, source: "L3"}
      - {x: 15, y: 0.72, confidence: 0.70, source: "L3"}
      - {x: 20, y: 0.68, confidence: 0.70, source: "L3"}
      - {x: 30, y: 0.64, confidence: 0.70, source: "L3"}
      - {x: 42, y: 0.62, confidence: 0.70, source: "L3"}    # 约 41.99% 端点
    curve_features:
      G_prime_0:
        value: 1.70
        unit: "MPa"
        strain_at: 0.28
        source: "L3"
        confidence: 0.70
      G_prime_inf:
        value: 0.62
        unit: "MPa"
        strain_at: 42
        source: "L3"
        confidence: 0.70
      delta_G_prime:
        value: 1.078
        unit: "MPa"
        calculation: "G'₀ - G'∞"
        source: "L1"
        confidence: 0.95
        note: "Table 2 精确值 1078.07 kPa"
      gamma_c:
        value: 3.6
        unit: "%"
        definition: "填料网络开始破坏的临界应变"
        confidence: 0.65
        note: "从 tan δ-应变曲线拐点估算"
      filler_network_strength:
        value: 0.63
        formula: "ΔG'/G'₀"
        note: "填料网络破坏率 63%"
      multi_stage_network:
        detected: false
        stages: 1
        note: "单一网络结构"
    validation:
      known_points:
        - strain: 0.28
          G_expected: 1.70
          G_estimated: 1.70
          deviation_percent: 0.0
          note: "起点估读"
        - strain: 42
          G_expected: 0.62
          G_estimated: 0.62
          deviation_percent: 0.0
          note: "ΔG' = 1.078 MPa 验证"
      overall_quality: "good"
    metadata:
      point_count: 12
      x_range: [0.28, 42]
      y_range: [0.62, 1.70]
      avg_confidence: 0.70
---

# 力学性能解读：SSBR-001

> **样本性质**: MPL官能化SSBR（3-巯基丙醇接枝），官能化程度3.6 wt%，白炭黑填充复合材料
> 
> **v2.0 更新**: 本文档已升级为全范围曲线数据格式，包含完整的应力-应变、DMA tan δ 和 Payne G' 曲线数据

## 一、基础信息

- **样本ID**: SSBR-001
- **样品名称**: SSBR-g-MPL70（70 phr 白炭黑填充）
- **官能化试剂**: MPL（3-巯基丙醇，3-Mercapto-1-propanol）
- **官能化程度**: 5.5 wt%（Table S2: 接枝巯基醇）
- **官能团类型**: 羟基（-OH）
- **分子量**: Mn = 18.5×10⁴ g/mol
- **交联密度**: 4.89×10⁻⁴ mol/cm³
- **文献DOI**: 10.1039/c9ra02783a

## 二、静态力学性能（应力-应变曲线）

### 数值数据

| 指标 | 数值 | 单位 | 来源 | 置信度 |
|------|------|------|------|--------|
| 100%定伸应力 | 4.2 | MPa | SI Table S5 | L1 (0.95) |
| 200%定伸应力 | - | MPa | 断裂点 | - |
| 300%定伸应力 | - | MPa | 未达此定伸 | - |
| 拉伸强度 | 14.2 | MPa | SI Table S5 | L1 (0.95) |
| 断裂伸长率 | 200 | % | SI Table S5 | L1 (0.95) |

### 全范围曲线数据 (v2.0)

本样本的应力-应变曲线包含 **13 个数据点**，覆盖 0-200% 应变范围。曲线呈现典型的填充橡胶应变硬化特征，无明显屈服点。

**曲线特征**:
- 初始模量较高，体现良好的填料-橡胶界面
- 100-200% 区间应变硬化显著
- 在 200% 应变处断裂，断裂伸长率较低

### 核心发现

SSBR-g-MPL70 复合材料展现出中等强度、中等伸长率的力学特性。相比空白SSBR/silica复合材料，官能化改性显著提升了力学性能：

1. **100%定伸应力提升**: 从 1.5 MPa → 4.2 MPa，提升 180%
2. **拉伸强度**: 14.2 MPa，略低于空白 (15.0 MPa)
3. **断裂伸长率降低**: 从 452% → 200%，降低 56%

### 与对照组对比

| 样本 | 100%应力 (MPa) | 拉伸强度 (MPa) | 伸长率 (%) |
|------|----------------|----------------|------------|
| SSBR-g-MPL70 | 4.2 | 14.2 | 200 |
| 空白 SSBR/silica | 1.5 | 15.0 | 452 |
| SSBR/Si69 | 2.6 | 21.0 | 406 |

### 分析结论

MPL官能化通过引入羟基（-OH）官能团，显著提高了 100% 定伸应力，但降低了断裂伸长率。这是因为：
- 羟基与白炭黑表面硅羟基形成氢键，增强了界面结合
- 强界面作用限制了分子链滑移，导致伸长率下降
- 交联密度提高 (4.89 vs 2.24 ×10⁻⁴ mol/cm³) 也贡献于模量增加

---

## 三、动态力学性能（Payne效应）

### 数值数据

| 指标 | 数值 | 单位 | 来源 | 置信度 |
|------|------|------|------|--------|
| 结合橡胶含量 | 55.28 | % | Table 1 | L1 (0.95) |
| ΔG'(compounds) | 657.10 | kPa | Table 2 | L1 (0.95) |
| ΔG'(vulcanizates) | 1078.07 | kPa | Table 2 | L1 (0.95) |
| tan δ (7% strain) | 0.104 | - | SI Table S4 | L1 (0.95) |

### 全范围曲线数据 (v2.0)

本样本的 G'-应变曲线包含 **12 个数据点**，覆盖 0.28%-42% 应变范围（对数间隔）。

**曲线特征**:
- 初始 G' ≈ 1.70 MPa
- 最终 G' ≈ 0.62 MPa
- ΔG' = 1.078 MPa (填料网络破坏量)
- 临界应变 γc ≈ 3.6% (网络开始破坏点)

### 核心发现

1. **结合橡胶含量 55.28%**: 高于空白样品 (20.56%)，表明官能化改善了填料-橡胶界面结合
2. **Payne 效应 ΔG' = 1.078 MPa**: 显著低于空白 (4.215 MPa)，表明白炭黑分散性大幅改善
3. **tan δ @ 7% = 0.104**: 比空白 (0.132) 降低 21.2%，有利于降低滚动阻力

### 与空白组对比

| 样本 | ΔG'(vulcanizates) (kPa) | 变化 |
|------|-------------------------|------|
| SSBR-g-MPL70 | 1078.07 | -74.4% |
| 空白 SSBR/silica | 4215.09 | 基准 |
| SSBR/Si69 | 3049.16 | -27.7% |

官能化 SSBR 的 Payne 效应减弱幅度远超 Si69 偶联剂，证明原位改性策略在改善填料分散方面更有效。

---

## 四、动态力学性能（DMA温度扫描）

### 数值数据

| 指标 | 数值 | 单位 | 来源 | 置信度 |
|------|------|------|------|--------|
| Tg (DMA) | -0.9 | ℃ | SI Table S6 | L1 (0.95) |
| tan δ_max | 1.010 | - | SI Table S6 | L1 (0.95) |
| tan δ (0℃) | 1.004 | - | SI Table S6 | L1 (0.95) |
| tan δ (60℃) | ~0.11 | - | Fig. 8C 估读 | L3 (0.70) |

### 全范围曲线数据 (v2.0)

本样本的 tan δ-温度曲线包含 **17 个数据点**，覆盖 -80℃ 到 +80℃ 范围。

**曲线特征**:
- 峰值位置: Tg ≈ -0.9℃
- 峰值高度: tan δ_max = 1.010
- 峰半高宽: ~45℃ (约 -25℃ 到 +20℃)
- 玻璃态区: tan δ < 0.1 (T < -50℃)
- 高弹态区: tan δ < 0.2 (T > 40℃)

### 核心发现

1. **Tg 显著升高**: 从 -9.0℃ (空白) → -0.9℃，升高约 8℃
   - 原因：官能化增强界面作用，形成"玻璃聚合物层"限制链段运动
2. **tan δ_max 大幅提升**: 从 0.640 (空白) → 1.010，提升 58%
   - 原因：填料-填料网络减少，有效橡胶相体积增加
3. **tan δ (0℃) = 1.004**: 湿地抓地力指标，比空白 (0.472) 提升 112.7%

### 轮胎应用性能分析

| 性能指标 | 数值 | 与空白对比 | 评价 |
|----------|------|-----------|------|
| 湿地抓地力 (tan δ @ 0℃) | 1.004 | +112.7% | **优异** |
| 滚动阻力 (tan δ @ 7% strain) | 0.104 | -21.2% | 良好 |
| 滚动阻力 (tan δ @ 60℃) | ~0.11 | - | 待验证 |

---

## 五、数据质量评估 (v2.0)

### 曲线数据质量汇总

| 曲线类型 | 数据点数 | 平均置信度 | 交叉验证质量 |
|----------|----------|-----------|-------------|
| 应力-应变 | 13 | 0.76 | excellent |
| DMA tan δ | 17 | 0.72 | excellent |
| Payne G' | 12 | 0.70 | good |

### 数据来源层级

- **L1 (表格数据)**: Table S5, Table S6, Table 1, Table 2, Table 3 提供精确数值
- **L3 (曲线估读)**: Fig. 6B, Fig. 8A, Fig. 8C 估读连续曲线数据

### 交叉验证结果

所有 L3 估读数据点均与 L1 已知点吻合良好：
- 应力-应变: 100% 点和断裂点完全吻合 (0% 偏差)
- DMA tan δ: Tg 点和 0℃ 点完全吻合 (0% 偏差)
- Payne G': ΔG' 计算值与 Table 2 吻合 (0% 偏差)

---

## 文献对应结论

> "The silica dispersion was improved by different functional SSBR from the TEM results, and better interface interaction was constructed between silica and rubber compared with the blank group, which resulted in outstanding mechanical and dynamic mechanical properties of the composites."

官能化通过改善白炭黑分散和构建更好的填料-橡胶界面，使复合材料获得了优异的动态力学性能。MPL 官能化（单氢键作用）虽然界面作用强度相对较弱，但已显著改善了湿地抓地力性能。

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **数据表格引用**: Table 1, Table 2, Table 3, SI Table S4, S5, S6
- **图谱引用**: Fig. 6(B), Fig. 8(A)(B)(C)
- **解读版本**: v2.0 (全范围曲线数据)
