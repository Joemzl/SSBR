---
sample_id: SSBR-014
interpretation_type: dsc
source_figure: "Fig.4, Table 10"
source_doi: "10.1039/c8ra00572a"
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: null

data:
  tg_composite:
    value: null
    unit: "℃"
    source: "文献未直接提供DSC数据"
  tg_pure_polymer:
    value: null
    unit: "℃"
    source: "文献通过V-T曲线模拟Tg"
  
  # 溶解度参数
  solubility_parameter:
    value: 17.41
    unit: "(J/cm³)^0.5"
    source: "Fig.4 实验测试"
  solubility_parameter_simulated:
    value: 15.85
    unit: "(J/cm³)^0.5"
    source: "Table 10 MD模拟"
---

# 热学性能解读：SSBR-014

> **样本性质**: 工业充油 SSBR (Oil sucked SSBR, Lanxess 4526)，用于石油树脂相容性研究

## 一、基础信息

- **样本ID**: SSBR-014
- **文献中编号**: Oil sucked SSBR (Lanxess 4526)
- **链组成**: St/cis-1,4/trans-1,4/ethenyl = 26/14.5/14.5/45 (wt%)
- **苯乙烯含量**: 26 wt%
- **乙烯基含量**: 45 mol%
- **供应商**: Lanxess Chemical Co., Ltd.
- **文献DOI**: 10.1039/c8ra00572a

## 二、溶解度参数测试

### 实验方法

文献使用**平衡溶胀法**测试橡胶的溶解度参数。

### 溶解度参数结果

**Fig.4 (b)** 显示 Oil sucked SSBR 的溶胀比-溶解度参数曲线：

| 样本 | 实验溶解度参数 δ (J/cm³)^0.5 | 来源 |
|------|---------------------------|------|
| F-SSBR | 17.22 | Fig.4 (a) |
| **Oil sucked SSBR** | **17.41** | **Fig.4 (b)** |

### 溶解度参数模拟

**Table 10** 给出了 MD 模拟的溶解度参数：

| 样本 | δtotal | δvdw | δele |
|------|--------|------|------|
| F-SSBR | 15.71 | 15.20 | 2.70 |
| **Oil sucked SSBR** | **15.85** | **15.33** | **2.76** |

---

## 三、与 F-SSBR 的对比

### 溶解度参数对比

| 参数 | F-SSBR | Oil sucked SSBR | 差异 |
|------|--------|-----------------|------|
| δ (实验) | 17.22 | **17.41** | Oil SSBR 更高 |
| δ (模拟) | 15.71 | **15.85** | Oil SSBR 更高 |
| δvdw | 15.20 | **15.33** | Oil SSBR 更高 |
| δele | 2.70 | **2.76** | Oil SSBR 更高 |

### 相容性差异

两种 SSBR 与五种树脂的相容性顺序**相同**：
> **1# ≈ 4# > 2# ≈ 5# > 3#**

---

## 四、链组成对热学性能的影响

### 微观结构差异

| 单元 | F-SSBR | Oil sucked SSBR |
|------|--------|-----------------|
| 苯乙烯 | 25% | 26% |
| 乙烯基 | **57%** | 45% |
| cis-1,4 | 9% | **14.5%** |
| trans-1,4 | 9% | **14.5%** |

### 对 Tg 的预期影响

- **乙烯基含量**: F-SSBR 更高 → Tg 可能更高
- **苯乙烯含量**: 相近
- **cis-1,4 含量**: Oil SSBR 更高 → 链段柔性更好

---

## 五、自扩散系数对比

虽然文献未直接给出 Oil sucked SSBR 的自扩散系数数据，但基于 F-SSBR 的数据可以推测，添加树脂后链段运动性增加。

---

## 六、综合评价

SSBR-014 (Oil sucked SSBR) 的热学特性：
- ✅ 实验溶解度参数: 17.41 (J/cm³)^0.5
- ✅ 模拟溶解度参数: 15.85 (J/cm³)^0.5
- ✅ 与树脂的相容性顺序与 F-SSBR 相同
- ✅ 是 Lanxess 公司的成熟工业产品
- ⚠️ 文献未直接提供 DSC 测得的 Tg 数值

---

## 文献来源

- **DOI**: 10.1039/c8ra00572a
- **数据引用**: Fig.4 (溶解度参数), Table 10 (模拟参数)
