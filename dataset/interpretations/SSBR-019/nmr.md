---
sample_id: SSBR-019
interpretation_type: nmr
source_figure: "Fig.1"
source_doi: "10.1021/acs.iecr.6b02259"
skill_used: ssbr-nmr-interpretation
created_at: 2026-03-18
updated_at: null

data:
  styrene_content:
    value: 20.1
    unit: "wt%"
    source: "Table 1"
  vinyl_content_1_2:
    value: null
    unit: "mol%"
    source: "文献未提供具体数值"
  functional_group_content:
    value: 5.1
    unit: "wt%"
    source: "Table 1"
  mn:
    value: 196000
    unit: "g/mol"
    source: "Table 1"
  pdi:
    value: 1.23
    unit: null
    source: "Table 1"
---

# 核磁共振解读：SSBR-019

> **样本性质**: DPES 官能化 SSBR（SBDR-5），5.1 wt% DPES 含量

## 一、基础信息

- **样本ID**: SSBR-019
- **文献中编号**: SBDR-5
- **基体**: 溶聚苯乙烯-丁二烯-DPES 共聚物
- **官能化试剂**: DPES (p-(2,2'-二苯基乙基)苯乙烯)
- **官能化程度**: 5.1 wt% DPES
- **文献DOI**: 10.1021/acs.iecr.6b02259

## 二、¹H NMR 谱图分析

### 核心发现

文献 Fig.1 显示了三种 SBDR 的 ¹H NMR 谱图（SBDR-0, SBDR-2, SBDR-5）。

### 关键峰归属

| 化学位移 (ppm) | 归属 | 说明 |
|---------------|------|------|
| 4.0 | DPES 的 methylidyne 质子 | **证明 DPES 引入成功** |
| 3.3 | DPES 的 methylene 质子 | **证明 DPES 引入成功** |
| 4.6-5.0 | 1,2-丁二烯双键上的 CH₂ 质子 | 乙烯基结构 |
| 5.0-5.6 | 1,2-Bd 和 1,4-Bd 的双键质子 | 丁二烯微观结构 |
| 6.7-7.3 | DPES 和苯乙烯的芳香质子 | 芳香环 |

文献指出：
> "The peaks at approximately 4.0 ppm and 3.3 ppm are assigned to methylidyne and methylene protons in DPES, demonstrating that DPES groups were successfully introduced to the backbones of rubber chains."

### 单体分布特征

文献分析表明单体随机分布：
> "the peaks of the block St sequences at 6.6 ppm disappeared in the 1H NMR spectra, indicating the random distribution of St and DPES in SBDR."

---

## 三、组成分析

### 定量计算方法

文献使用以下方程计算组成：

**方程 (1)**: 计算 1,2-Bd 和 1,4-Bd 的比例
```
N_Bd1,2 + N_Bd1,4 = (A_4.9-5 + A_5-5.6) / 2
```

**方程 (3)**: 计算 DPES 含量
```
N_DPES = (A_4-4.3) / 2
```

**方程 (4)**: 计算苯乙烯含量
```
(14×N_DPES + 5×N_St) = A_6.5-7.26
```

### SBDR-5 组成

| 组分 | 含量 | 来源 |
|------|------|------|
| 丁二烯 (Bd) | 74.8 wt% | Table 1 |
| 苯乙烯 (St) | 20.1 wt% | Table 1 |
| **DPES** | **5.1 wt%** | **Table 1** |

### 分子量

| 参数 | SBDR-5 值 | 说明 |
|------|-----------|------|
| Mn | 19.6 × 10⁴ g/mol | GPC 测定 |
| Mw/Mn | 1.23 | 分子量分布较窄 |

文献指出转化率为 100%：
> "the three monomer units were quantitatively introduced to the SBDR chain"

---

## 四、NMR 关键图谱特征

### SBDR-5 特征峰验证

1. **DPES 特征峰** (δ 3.3, 4.0 ppm):
   - 存在 → 证明 DPES 成功引入
   - 强度 → 与投料比一致

2. **芳香峰** (δ 6.7-7.3 ppm):
   - DPES 和 St 的芳香质子重叠
   - 无 6.6 ppm 峰 → 无嵌段 St 序列 → 随机分布

3. **丁二烯微观结构**:
   - 1,2-Bd: δ 4.6-5.0 ppm (CH₂=)
   - 1,4-Bd: δ 5.0-5.6 ppm (-CH=CH-)

---

## 五、综合评价

SSBR-019 (SBDR-5) 的 NMR 分析结果：
- ✅ DPES 成功引入聚合物主链（δ 3.3, 4.0 ppm 特征峰）
- ✅ 组成与设计一致（Bd 74.8%，St 20.1%，DPES 5.1%）
- ✅ 单体随机分布（无 6.6 ppm 嵌段 St 峰）
- ✅ 分子量适中（Mn = 19.6 × 10⁴），PDI 窄（1.23）
- ✅ 100% 转化率

---

## 文献来源

- **DOI**: 10.1021/acs.iecr.6b02259
- **数据引用**: Fig.1 (¹H NMR), Table 1, Eqs (1)-(5)
