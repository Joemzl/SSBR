---
sample_id: SSBR-015
interpretation_type: nmr
source_figure: "Fig.1, Fig.2"
source_doi: "10.1021/acs.iecr.6b02259"
skill_used: ssbr-nmr-interpretation
created_at: 2026-03-18
updated_at: null

data:
  nmr_available: true
  nmr_type: "1H NMR"
  solvent: "CDCl3"
  frequency: "400 MHz"
  composition:
    butadiene:
      value: 74.8
      unit: "wt%"
    styrene:
      value: 20.1
      unit: "wt%"
    dpes:
      value: 5.1
      unit: "wt%"
  mn:
    value: 196000
    unit: "g/mol"
  pdi: 1.23
---

# 核磁共振 (NMR) 解读：SSBR-015

> **样本性质**: DPES 官能化 SSBR（SBDR-5），5.1 wt% DPES 含量

## 一、基础信息

- **样本ID**: SSBR-015
- **文献中编号**: SBDR-5
- **官能化试剂**: DPES (p-(2,2'-二苯基乙基)苯乙烯)
- **NMR 类型**: ¹H NMR
- **仪器**: Bruker ARX400 (400 MHz)
- **溶剂**: CDCl₃
- **内标**: 四甲基硅烷 (TMS)
- **文献DOI**: 10.1021/acs.iecr.6b02259

## 二、¹H NMR 谱图分析 (Fig.1)

文献 Fig.1 显示了 SBDR-0, SBDR-2, SBDR-5 的 ¹H NMR 谱图。

### 特征峰归属

| 化学位移 (ppm) | 归属 | 说明 |
|---------------|------|------|
| 6.7-7.3 | 芳香氢 | DPES 和 St 的苯环氢 |
| 5.0-5.6 | 烯烃氢 | 1,2-Bd 和 1,4-Bd 的双键氢 |
| 4.6-5.0 | 烯烃氢 | 1,2-Bd 的双键亚甲基氢 |
| ~4.0 | CH | DPES 的次甲基氢 |
| ~3.3 | CH₂ | DPES 的亚甲基氢 |

### DPES 特征峰

文献指出：
> "The peaks at approximately 4.0 ppm and 3.3 ppm are assigned to methylidyne and methylene protons in DPES, demonstrating that DPES groups were successfully introduced to the backbones of rubber chains."

- **~4.0 ppm**: DPES 的 CH（次甲基）氢
- **~3.3 ppm**: DPES 的 CH₂（亚甲基）氢

这两个峰的出现证明 DPES 单体已成功引入聚合物主链。

## 三、组成计算

### 计算方法

文献使用以下方程计算 SBDR 的组成：

```
方程 (1): N(Bd1,2) + N(Bd1,4) = A(5-5.6) / A(4.9-5)
方程 (2): N(Bd1,4) + N(Bd1,2) = 1
方程 (3): N(Bd1,2) / N(DPES) = A(4.9-5) / A(4-4.3)
方程 (4): (N(DPES) + N(St)) × 14 / 5 = A(6.5-7.26) / A(4-4.3)
方程 (5): M(Bd)×N(Bd1,4) + M(Bd)×N(Bd1,2) + M(St)×N(St) + M(DPES)×N(DPES) = Mn
```

### SBDR-5 的组成 (Table 1)

| 组分 | 含量 (wt%) |
|------|-----------|
| 丁二烯 (Bd) | 74.8 |
| 苯乙烯 (St) | 20.1 |
| **DPES** | **5.1** |

### 分子量

| 参数 | 数值 |
|------|------|
| 数均分子量 (Mn) | 19.6×10⁴ g/mol |
| 分子量分布 (PDI) | 1.23 |

## 四、无规分布的证据

### NMR 证据

文献指出：
> "the peaks of the block St sequences at 6.6 ppm disappeared in the ¹H NMR spectra, indicating the random distribution of St and DPES in SBDR."

嵌段 St 序列的特征峰（6.6 ppm）消失，证明 St 和 DPES 在 SBDR 链中呈**无规分布**。

### 组成-转化率曲线证据 (Fig.2)

> "the composition of SBDR-5 shown in Figure 2 remained unchanged throughout the entire reaction process"

在整个聚合过程中，SBDR-5 的组成保持不变，进一步证明了无规分布。

### DSC 证据 (Fig.3)

> "the DSC curves of SBDR displayed in Figure 3 show only one glass transition temperature, providing further evidence of the random distribution of monomers along the SBDR chain."

单一 Tg 也证明了单体的无规分布。

## 五、DPES 官能团结构

### DPES 单体结构

```
名称: p-(2,2'-二苯基乙基)苯乙烯
化学式: C22H20
SMILES: C=Cc1ccc(CCC(c2ccccc2)c3ccccc3)cc1
```

### 关键结构特征

DPES 含有一个**三苯乙烷 (ETB)** 悬挂基团：
- **热可分解 C-C 键**: 在加热条件下可均裂产生苄基和二苯甲基自由基
- **自由基捕获机制**: 产生的聚合物自由基被炭黑表面的多环芳烃捕获，形成共价键

## 六、综合评价

SSBR-015 (SBDR-5) 的 NMR 分析结果：
- ✅ DPES 成功引入聚合物主链（4.0 和 3.3 ppm 特征峰）
- ✅ 三种单体无规分布（无嵌段序列峰）
- ✅ 组成符合投料比（5.1 wt% DPES）
- ✅ 窄分子量分布（PDI = 1.23）

---

## 文献来源

- **DOI**: 10.1021/acs.iecr.6b02259
- **谱图引用**: Fig.1 (¹H NMR), Fig.2 (组成-转化率); Table 1
