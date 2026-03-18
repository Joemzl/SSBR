---
sample_id: SSBR-015
interpretation_type: tem
source_figure: "Fig.8, Fig.9"
source_doi: "10.1021/acs.iecr.6b02259"
skill_used: ssbr-tem-interpretation
created_at: 2026-03-18
updated_at: null

data:
  filler_type: "炭黑 (carbon black)"
  filler_grade: "N330"
  filler_properties:
    specific_surface_area: "78±5 m²/g"
    dbp_value: "121±5 mL/100g"
    average_particle_size: "25 nm"
  dispersion_quality: "显著改善"
  rg_saxs:
    value: 18.16
    unit: "nm"
    source: "Table 2"
  comparison_with_control:
    control_rg: 24.15
    control_sample: "CB/SBDR-0"
    improvement: "Rg 降低 25%"
---

# TEM 形貌解读：SSBR-015

> **样本性质**: DPES 官能化 SSBR/炭黑复合材料（CB/SBDR-5），5.1 wt% DPES 含量

## 一、基础信息

- **样本ID**: SSBR-015
- **文献中编号**: CB/SBDR-5 硫化胶
- **填料**: 炭黑 N330 (Cabot)
- **填料规格**:
  - 比表面积: 78±5 m²/g
  - DBP 值: 121±5 mL/100g
  - 平均粒径: 25 nm
- **测试仪器**: Tecnai G2 20 S-Twin 透射电子显微镜 (FEI)
- **加速电压**: 200 kV
- **文献DOI**: 10.1021/acs.iecr.6b02259

## 二、TEM 形貌观察 (Fig.8)

### 三种样本的对比

文献 Fig.8 展示了三种 CB/SBDR 硫化胶的 TEM 照片：

| 样本 | 分散特征 | 说明 |
|------|----------|------|
| CB/SBDR-0 (Fig.8a) | 明显的炭黑团聚 | 界面相互作用弱 |
| CB/SBDR-2 (Fig.8b) | 分散改善 | 1.9% DPES |
| **CB/SBDR-5 (Fig.8c)** | **分散最优** | **5.1% DPES** |

### CB/SBDR-0 的团聚现象

文献描述：
> "When CB particles were dispersed in the SBDR-0 matrix, clear CB aggregations were observed (Figure 8 (a)), as a result of the weak interfacial interaction between CB and the rubber matrix and strong interaction among CB particles, which created agglomerates of CB particles in the rubber matrix."

- 弱界面相互作用
- 炭黑粒子间相互作用强
- 形成团聚体

### CB/SBDR-5 的分散改善

文献描述：
> "When the DPES content was increased from 1.9 wt% to 5.1 wt%, a great improvement was observed in the dispersion states of CB particles in the SBDR matrix (Figure 8 (b) and 8 (c))."

CB/SBDR-5 中炭黑的分散显著改善，这归因于：
- **共价键界面**: DPES 与炭黑形成共价键
- **界面作用增强**: 界面相互作用远强于范德华力
- **阻止再聚集**: 更多共价键阻止炭黑粒子团聚

## 三、SAXS 定量分析 (Fig.9)

### Guinier 分析

文献使用小角 X 射线散射 (SAXS) 定量分析炭黑的分散状态，通过 Guinier 方程计算回转半径 Rg：

```
ln(I(q)) = ln(nI_n(ΔρV)²) - (Rg² × q²)/3
```

### Rg 结果 (Table 2)

| 样本 | DPES 含量 (wt%) | Rg (nm) |
|------|----------------|---------|
| CB/SBDR-0 | 0 | 24.15 |
| CB/SBDR-2 | 1.9 | 19.55 |
| **CB/SBDR-5** | **5.1** | **18.16** |

### 分析结论

> "The Rg of the CB dispersed aggregations is shown in Table 2. The Rg of CB in the rubber sample decreased from 24.15 to 18.16 nm as the DPES content increased, indicating that the size of CB aggregation in the rubber matrix decreased when DPES was introduced into the rubber matrix."

- **Rg 降低 25%**: 从 24.15 nm 降至 18.16 nm
- **团聚体尺寸减小**: 炭黑团聚体尺寸随 DPES 含量增加而减小
- **与 TEM 结果一致**: SAXS 定量结果支持 TEM 观察

## 四、分散改善机理

### 共价接枝机制 (Scheme 2)

文献 Scheme 2 展示了 SBDR 接枝到炭黑表面的机理：

1. **热解离**: DPES 中的 C-C 键在高温下均裂
2. **自由基生成**: 产生苄基自由基和二苯甲基自由基
3. **自由基捕获**: 炭黑表面的多环芳烃捕获聚合物自由基
4. **共价键形成**: 形成 SBDR-接枝-炭黑

### 接枝验证

文献通过多种方法验证了接枝的发生：

1. **溶剂分散实验 (Fig.4)**: 接枝后的炭黑可分散在环己烷相而非 DMF 相
2. **FTIR (Fig.5)**: 接枝炭黑出现 SBDR 的特征峰
3. **TGA (Fig.6)**: 接枝量约 16.9 wt%
4. **XPS (Fig.7)**: C-C 峰强度增加（24.1% → 26.3%）

## 五、综合评价

| 指标 | CB/SBDR-5 | 评价 |
|------|-----------|------|
| TEM 观察 | 分散最优 | ✅ 显著改善 |
| Rg (SAXS) | 18.16 nm | ✅ 比对照降低 25% |
| 团聚程度 | 最低 | ✅ 接枝阻止团聚 |
| Payne 效应 | 最低 | ✅ 与分散改善一致 |

DPES 官能化显著改善了炭黑在 SSBR 基体中的分散，这是通过共价接枝机制实现的。

---

## 文献来源

- **DOI**: 10.1021/acs.iecr.6b02259
- **图片引用**: Fig.8 (TEM), Fig.9 (SAXS); Table 2
- **机理**: Scheme 2
