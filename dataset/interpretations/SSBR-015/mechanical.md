---
sample_id: SSBR-015
interpretation_type: mechanical
source_figure: Fig.11, Table S4, Fig.10
source_doi: 10.1021/acs.iecr.6b02259
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
mechanical_subtypes:
- stress-strain
- payne
data:
  stress_100:
    value: null
    range: null
    unit: MPa
    source: 文献未提供
  stress_200:
    value: null
    range: null
    unit: MPa
    source: 文献未提供
  stress_300:
    value: null
    range: null
    unit: MPa
    source: 文献提供应力应变曲线但无具体数值
  tensile_strength:
    description: 相比 SBDR-0 提高 43.8%
    source: Table S4
  elongation:
    description: 相比 SBDR-0 提高 11.6%
    source: Table S4
  mechanical_source: L2
  payne_effect:
    description: G∞'-G0' 随 DPES 含量增加而降低
    source: Fig.10, Table S3
  bound_rubber:
    value: 26.9
    unit: '%'
    source: 正文
skill_version: '2.0'
curves:
  # ---------- 应力-应变曲线 (Fig. 11) ----------
  stress_strain:
    x_axis:
      label: 应变
      unit: '%'
    y_axis:
      label: 应力
      unit: MPa
    data_points: []
    curve_features:
      modulus_100:
        value: null
        unit: MPa
        source: "文献未提供绝对数值"
        confidence: null
      modulus_300:
        value: null
        unit: MPa
        source: "文献仅提供图形曲线"
        confidence: null
      tensile_strength:
        value: null
        unit: MPa
        source: "Table S4"
        confidence: null
        note: "相比 SBDR-0 提高 43.8%"
      elongation_at_break:
        value: null
        unit: '%'
        source: "Table S4"
        confidence: null
        note: "相比 SBDR-0 提高 11.6%"
      yield_point:
        exists: false
    validation:
      known_points: []
      overall_quality: "poor"
      note: "文献仅提供百分比变化，无绝对数值，无法估读曲线"
    metadata:
      point_count: 0
      x_range: [0, 0]
      y_range: [0, 0]
      avg_confidence: 0

  # ---------- Payne 效应 G'-应变曲线 (Fig. 10) ----------
  payne_storage_modulus:
    x_axis:
      label: 应变
      unit: '%'
      scale: logarithmic
    y_axis:
      label: 储能模量 G'
      unit: MPa
    data_points: []
    curve_features:
      G_prime_0:
        value: null
        unit: MPa
        strain_at: 0.28
        source: "Fig. 10"
        confidence: null
      G_prime_inf:
        value: null
        unit: MPa
        strain_at: 42
        source: "Fig. 10"
        confidence: null
      delta_G_prime:
        value: null
        unit: kPa
        source: "Table S3"
        confidence: null
        note: "随 DPES 含量增加而降低"
    validation:
      known_points: []
      overall_quality: "poor"
      note: "文献仅提供趋势描述，无绝对数值"
    metadata:
      point_count: 0
      x_range: [0.1, 100]
      y_range: [0, 3]
      avg_confidence: 0
---
# 力学性能解读：SSBR-015

> **样本性质**: DPES 官能化 SSBR/炭黑复合材料（SBDR-5），5.1 wt% DPES 含量


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-015
- **文献中编号**: SBDR-5 / CB/SBDR-5 硫化胶
- **基体**: 溶聚苯乙烯-丁二烯-DPES 共聚物
- **官能化试剂**: DPES (p-(2,2'-二苯基乙基)苯乙烯)
- **官能化程度**: 5.1 wt% DPES
- **填料**: 炭黑 N330
- **文献DOI**: 10.1021/acs.iecr.6b02259

## 二、静态力学性能（应力-应变曲线）

### 核心发现

文献 Fig.11 和 Table S4 显示：
> "5.1 wt % DPES in the CB/SBDR-5 vulcanizate resulted in significant increases both in tensile strength and elongation at break of **43.8%** and **11.6%**, respectively, compared with the SBDR-0 vulcanizate."

| 指标 | CB/SBDR-5 vs CB/SBDR-0 | 说明 |
|------|------------------------|------|
| 拉伸强度 | **+43.8%** | 显著提升 |
| 断裂伸长率 | **+11.6%** | 同时提升 |

### 力学性能提升机理

文献解释了力学性能同时提升的原因：
> "The enhancements in tensile strength and elongation at break can be ascribed to the strong covalent interactions between CB and the SBDR matrix and the wide dispersion of CB particles, leading to excellent stress transfer through the filler–matrix interface."

1. **强共价键界面相互作用**: DPES 热分解产生的自由基被炭黑表面捕获，形成共价键
2. **填料分散改善**: 炭黑在基体中分散更均匀
3. **优异的应力传递**: 界面结合强度提高

### 交联密度的影响

文献 Table 3 显示：
> "the extent of the cross-linking density was increased with increasing DPES content"

DPES 基团参与硫化过程，提供额外的交联密度，这也有助于力学性能的提升。

---

## 三、动态力学性能（Payne效应）

### 核心发现

文献 Fig.10 和 Table S3 显示：
> "The values of (G∞'–G0'), as shown in Table S3, decreased with increasing DPES content, indicating that a wider dispersion of CB in the SBDR matrix was obtained by increasing the content of DPES in the rubber matrix."

### Payne 效应降低机理

文献解释：
> "a higher DPES content leads to a higher number of covalent bonds at the interface, which causes the breakage of CB aggregates. The distance between CB particles is then increased and the interaction between CB particles is reduced, leading to a lower Payne effect."

1. **更多共价键**: DPES 含量增加 → 界面共价键数量增加
2. **炭黑团聚体破坏**: 界面相互作用打破炭黑团聚
3. **粒子间距增加**: 炭黑粒子间相互作用减弱
4. **Payne 效应降低**: 填料网络贡献减小

### 结合橡胶含量

文献指出：
> "the bound rubber contents in CB/SBDR-0, CB/SBDR-2 and CB/SBDR-5 compounds were 13.5 wt %, 19.1 wt % and **26.9%**, respectively."

CB/SBDR-5 的结合橡胶含量达到 **26.9%**，是 SBDR-0 的近两倍，表明显著增强的界面相互作用。

---

## 四、与其他样本对比

### 三种 SBDR 样本力学性能对比

| 样本 | DPES 含量 | 拉伸强度变化 | 伸长率变化 | 结合橡胶 |
|------|----------|-------------|-----------|----------|
| CB/SBDR-0 | 0% | 基准 | 基准 | 13.5% |
| CB/SBDR-2 | 1.9% | 提升 | 提升 | 19.1% |
| **CB/SBDR-5** | **5.1%** | **+43.8%** | **+11.6%** | **26.9%** |

---

## 五、综合评价

SSBR-015 (CB/SBDR-5) 的力学性能特点：
- ✅ 拉伸强度显著提升 43.8%
- ✅ 断裂伸长率同时提升 11.6%（强度和伸长率同时提升较罕见）
- ✅ Payne 效应降低，填料分散改善
- ✅ 结合橡胶含量高达 26.9%
- ✅ 交联密度提高

---

## 文献来源

- **DOI**: 10.1021/acs.iecr.6b02259
- **数据引用**: Fig.10, 11; Table S3, S4
