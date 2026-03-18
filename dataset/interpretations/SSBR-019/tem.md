---
sample_id: SSBR-019
interpretation_type: tem
source_figure: "Fig.8"
source_doi: "10.1021/acs.iecr.6b02259"
skill_used: ssbr-tem-interpretation
created_at: 2026-03-18
updated_at: null

data:
  filler_type: "炭黑 N330"
  filler_loading: "参见 Table S2"
  dispersion_quality: "优"
  aggregate_size_nm:
    value: 18.16
    unit: "nm"
    source: "Table 2 (Rg from SAXS)"
  scale_bar: "200 nm"
  morphology_description: "炭黑分散均匀，无明显团聚"
---

# TEM 形貌解读：SSBR-019

> **样本性质**: DPES 官能化 SSBR/炭黑复合材料（CB/SBDR-5），5.1 wt% DPES 含量

## 一、基础信息

- **样本ID**: SSBR-019
- **文献中编号**: CB/SBDR-5 硫化胶
- **基体**: 溶聚苯乙烯-丁二烯-DPES 共聚物
- **官能化试剂**: DPES (p-(2,2'-二苯基乙基)苯乙烯)
- **官能化程度**: 5.1 wt% DPES
- **填料**: 炭黑 N330
- **文献DOI**: 10.1021/acs.iecr.6b02259

## 二、TEM 形貌分析

### 核心发现

文献 Fig.8 展示了三种 CB/SBDR 硫化胶的 TEM 图像：

**Fig.8 (c) - CB/SBDR-5**:
> "When the DPES content was increased from 1.9 wt% to 5.1wt%, a great improvement was observed in the dispersion states of CB particles in the SBDR matrix"

### 三种样本对比

| 样本 | DPES 含量 | 分散状态 | TEM 特征 |
|------|----------|----------|----------|
| CB/SBDR-0 (a) | 0% | 差 | 明显的炭黑团聚 |
| CB/SBDR-2 (b) | 1.9% | 中 | 团聚减少 |
| **CB/SBDR-5 (c)** | **5.1%** | **优** | **分散均匀，无明显团聚** |

### CB/SBDR-0 的团聚问题

文献解释了未改性样本的团聚原因：
> "When CB particles were dispersed in the SBDR-0 matrix, clear CB aggregations were observed (Figure 8 (a)), as a result of the weak interfacial interaction between CB and the rubber matrix and strong interaction among CB particles, which created agglomerates of CB particles in the rubber matrix."

### CB/SBDR-5 分散改善原因

文献指出：
> "Because these vulcanizates were prepared under the same conditions, the improved dispersion of CB particles in the rubber matrix was mainly attributed to the introduction of DPES."

> "The covalent bonding interfaces formed afterward were much stronger than those of conventional van der Waals forces. Moreover, when DPES content was increased, the numbers of covalent bonds at the interface increased correspondingly, leading to enhanced interfacial interaction that could further prevent the aggregation of CB particles."

---

## 三、SAXS 定量分析

### 炭黑团聚体尺寸

文献使用 SAXS 技术通过 Guinier 方程定量分析炭黑团聚体尺寸（回转半径 Rg）：

| 样本 | DPES 含量 | Rg (nm) | 说明 |
|------|----------|---------|------|
| CB/SBDR-0 | 0% | 24.15 | 最大团聚体 |
| CB/SBDR-2 | 1.9% | 19.55 | 团聚减小 |
| **CB/SBDR-5** | **5.1%** | **18.16** | **最小团聚体** |

文献结论：
> "The Rg of the CB dispersed aggregations... decreased from 24.15 to 18.16 nm as the DPES content increased, indicating that the size of CB aggregation in the rubber matrix decreased when DPES was introduced into the rubber matrix."

---

## 四、分散改善机理

### 共价键界面作用

文献通过多种方法证明了 SBDR 与炭黑之间形成共价键：

1. **溶解性测试** (Fig.4): SBDR-5 接枝炭黑转移到环己烷相
2. **FTIR** (Fig.5): 接枝后出现 SBDR 特征峰
3. **TGA** (Fig.6): 接枝量约 16.9 wt%
4. **XPS** (Fig.7): C-C 峰强度从 24.1% 增加到 26.3%

### 分散机理总结

```
DPES 热分解 → 产生聚合物自由基 → 被炭黑表面捕获
           ↓
      形成共价键界面
           ↓
    打破炭黑团聚体 → 粒子间距增加 → 分散改善
```

---

## 五、与 Payne 效应的关联

TEM 观察到的分散改善与 Payne 效应数据一致：

| 指标 | CB/SBDR-0 | CB/SBDR-5 | 变化 |
|------|-----------|-----------|------|
| TEM 分散 | 团聚明显 | 均匀分散 | 改善 |
| Rg (nm) | 24.15 | 18.16 | -25% |
| Payne 效应 | 高 | 低 | 降低 |

---

## 六、综合评价

SSBR-019 (CB/SBDR-5) 的 TEM 形貌特点：
- ✅ 炭黑分散质量优秀
- ✅ 无明显团聚体
- ✅ 团聚体尺寸（Rg）降至 18.16 nm（最小）
- ✅ 共价键界面有效阻止填料聚集
- ✅ TEM 与 SAXS 结果相互印证

---

## 文献来源

- **DOI**: 10.1021/acs.iecr.6b02259
- **数据引用**: Fig.8 (TEM), Fig.9 (SAXS), Table 2
