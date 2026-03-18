---
sample_id: SSBR-013
interpretation_type: dsc
source_figure: "Fig.4, Fig.7, Table 7"
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
    value: 17.22
    unit: "(J/cm³)^0.5"
    source: "Fig.4 实验测试"
  solubility_parameter_simulated:
    value: 15.71
    unit: "(J/cm³)^0.5"
    source: "Table 10 MD模拟"
---

# 热学性能解读：SSBR-013

> **样本性质**: 工业官能化 SSBR (F-SSBR, SE0212)，用于石油树脂相容性研究

## 一、基础信息

- **样本ID**: SSBR-013
- **文献中编号**: F-SSBR (SE0212)
- **链组成**: St/cis-1,4/trans-1,4/ethenyl = 25/9/9/57 (wt%)
- **苯乙烯含量**: 25 wt%
- **乙烯基含量**: 57 mol%
- **供应商**: Red Avenue New Materials Group
- **文献DOI**: 10.1039/c8ra00572a

## 二、溶解度参数测试

### 实验方法

文献使用**平衡溶胀法**测试橡胶的溶解度参数：

> "Based on this theory, the higher the equilibrium swelling mass ratio (Qm) is, the more closely the solubility parameter of a polymer is to that of the solvent."

### 溶解度参数结果

**Fig.4 (a)** 显示 F-SSBR 的溶胀比-溶解度参数曲线：

| 样本 | 实验溶解度参数 δ (J/cm³)^0.5 | 来源 |
|------|---------------------------|------|
| **F-SSBR** | **17.22** | Fig.4 (a) |
| Oil sucked SSBR | 17.41 | Fig.4 (b) |

### 溶解度参数模拟

**Table 10** 给出了 MD 模拟的溶解度参数：

| 样本 | δtotal | δvdw | δele |
|------|--------|------|------|
| **F-SSBR** | **15.71** | 15.20 | 2.70 |
| Oil sucked SSBR | 15.85 | 15.33 | 2.76 |

> 注：实验值与模拟值存在差异，文献解释这是由于实验使用溶剂作为媒介所致。

---

## 三、玻璃化转变温度（Tg）相关

### 模拟方法

文献通过 **V-T 曲线法**（体积-温度曲线）模拟 Tg：

> "By implementing a sequence of NPT conditions with well-defined temperature (T), we obtained a series of cell volumes (V) accordingly. Through the V–T curve, the Tg can easily be calculated."

### 橡胶单元的相互作用

**Table 11** 和 **Fig.11** 分析了橡胶单元与树脂的非键相互作用：

| 橡胶单元 | 与树脂相互作用强度 |
|---------|------------------|
| 苯乙烯单元 | **最强** |
| trans-1,4 单元 | 较强 |
| 乙烯基单元 | 中等 |
| cis-1,4 单元 | **最弱** |

文献结论：
> "the styrene unit has the strongest interaction with all five resins, while the cis-1,4 unit has the weakest interaction with the resins"

### 对 F-SSBR Tg 的影响

由于 F-SSBR 含有较高的乙烯基（57 mol%）和苯乙烯（25 wt%）含量：
- 苯乙烯单元与树脂强相互作用 → 有助于相容性
- 高乙烯基含量 → 影响链段柔性

---

## 四、相容性评估

### R 值法（溶解度参数差异）

文献定义 R 值来评估相容性：

```
R = √[(δvdw,A - δvdw,B)² + (δele,A - δele,B)²]
```

**Fig.9** 给出 F-SSBR 与五种树脂的 R 值：

| 树脂 | R 值 | 相容性排序 |
|------|------|-----------|
| 1# 古马隆树脂-1 | 最小 | 1 (最好) |
| 4# 古马隆树脂-2 | 较小 | 2 |
| 2# α-甲基苯乙烯树脂 | 中等 | 3 |
| 5# C9 石油树脂 | 中等 | 4 |
| 3# C5/C9 共聚树脂 | 最大 | 5 (最差) |

### 相容性排序

实验和模拟得到的相容性顺序：
> **1# ≈ 4# > 2# ≈ 5# > 3#**

---

## 五、自扩散系数

### F-SSBR 链在复合体系中的运动性

**Table 14** 和 **Fig.13** 给出了 F-SSBR 链的自扩散系数 (Ds)：

| 体系 | Ds (×10⁻⁷ cm²/s) | 说明 |
|------|-------------------|------|
| 纯 F-SSBR | 0.5867 | 基准 |
| F-SSBR/1# | 0.7583 | 运动性增加 |
| F-SSBR/2# | **0.8917** | **最高** |
| F-SSBR/3# | 0.6700 | 较低 |
| F-SSBR/4# | 0.8200 | 较高 |
| F-SSBR/5# | 0.7083 | 中等 |

文献结论：
> "with the addition of petroleum resin, the chain mobility of F-SSBR was improved and this result fits well with experimental findings in which petroleum resin softens the rubber matrix and acts like small molecule lubricants."

---

## 六、综合评价

SSBR-013 (F-SSBR) 的热学特性：
- ✅ 实验溶解度参数: 17.22 (J/cm³)^0.5
- ✅ 模拟溶解度参数: 15.71 (J/cm³)^0.5
- ✅ 苯乙烯单元与树脂相互作用最强
- ✅ 与古马隆树脂（1#, 4#）相容性最佳
- ✅ 添加树脂后链段运动性增加
- ⚠️ 文献未直接提供 DSC 测得的 Tg 数值

---

## 文献来源

- **DOI**: 10.1039/c8ra00572a
- **数据引用**: Fig.4 (溶解度参数), Table 10 (模拟参数), Fig.9 (R值), Table 14 (Ds)
