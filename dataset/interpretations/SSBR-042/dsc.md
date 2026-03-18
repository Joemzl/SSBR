---
sample_id: SSBR-042
interpretation_type: dsc
source_figure: "Fig.3, Fig.4"
source_doi: "10.1002/app.28621"
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: null

data:
  tg_dsc:
    value: null
    unit: "℃"
    source: "文献使用 DMTA 测定 Tg，未提供 DSC 数据"
  tg_dmta:
    value: null
    unit: "℃"
    source: "Fig.3, Fig.4 仅提供曲线图，未给出具体数值"
  tg_shift_vs_pure:
    value: "+2"
    unit: "℃"
    description: "共凝聚橡胶 Tg 比纯 SSBR 高 2℃"
    source: "文献正文"
  tg_shift_vs_blend:
    value: "+2"
    unit: "℃"
    description: "N-SSBR/SiO2 复合材料 Tg 比 SSBR/SiO2 高 2℃"
    source: "文献正文"
---

# 热学性能解读：SSBR-042

> **样本性质**: N-SSBR/SiO2 共凝聚纳米复合材料（YK-1-2），采用 AMMO 硅烷偶联剂改性

## 一、基础信息

- **样本ID**: SSBR-042
- **文献中编号**: YK-1-2（N-SSBR/SiO2 纳米复合材料）
- **基体**: YK-1 星形 SSBR（苯乙烯含量 21.1%，乙烯基含量 38.1%）
- **测试方法**: DMTA（动态力学热分析）
- **测试条件**: 矩形拉伸模式，1 Hz，升温速率 3℃/min，温度范围 -100℃ ~ 100℃
- **文献DOI**: 10.1002/app.28621

## 二、玻璃化转变温度 (Tg)

### 关键发现

文献明确指出：
> "Either the glass-transition temperatures of SSBR or those of SSBR filled with 20 phr organically modified silica are **2°C lower** than those of N-SSBR and N-SSBR filled with the same amount of silica, respectively."

| 材料类型 | Tg 相对变化 |
|---------|-------------|
| 纯 SSBR (YK-1) → 共凝聚橡胶 (YK-1-0) | +2℃ |
| SSBR/SiO2 (YK-1-1) → N-SSBR/SiO2 (YK-1-2) | +2℃ |

### 机理分析

Tg 升高的原因：
> "The stronger adsorption between the organically modified nanosilica particles and macromolecular chains results in the lower flexibility of the macromolecular chains and higher glass-transition temperature of rubber."

1. **纳米白炭黑与聚合物链的强吸附作用**
2. **分子链柔顺性降低**
3. **链段运动受限**

## 三、DMTA 曲线特征

### 储能模量 (G') 变化

文献 Fig.4 显示：
> "N-SSBR filled with the same amount of silica exhibit slightly higher G' values in glassy state"

| 温度区域 | N-SSBR/SiO2 vs SSBR/SiO2 |
|---------|--------------------------|
| 玻璃态 | G' 略高 |
| 玻璃化转变区 | G' 显著升高 20-120% |
| 高弹态 | G' 相近或略高 |

### tan δ 峰特征

文献指出：
> "compared with the corresponding pure rubbers, the values of tan δ peak height of the co-coagulated rubbers in the region of glass-transition all drop and the values of peak area reduce."

1. **tan δ 峰高度降低**: 表明内摩擦损耗减小
2. **tan δ 峰面积减小**: 表明分子链解冻过程中的摩擦损耗降低
3. **玻璃化转变区变宽**: 表明填料-聚合物界面相互作用增强

## 四、轮胎性能相关指标

### 0℃ tan δ（湿地抓地力指标）

文献 Fig.4 指出：
> "tan δ values of N-SSBR/SiO2 nanocomposites are higher to some extent than those of corresponding SSBR/SiO2 nanocomposites at 0°C, thus the N-SSBR/SiO2 nanocomposites exhibit the better performance of wet-skid resistance."

N-SSBR/SiO2 在 0℃ 的 tan δ 值略高于 SSBR/SiO2，表明：
- ✅ **更好的湿地抓地性能**

### 60℃ tan δ（滚动阻力指标）

文献 Fig.6 显示 N-SSBR/SiO2 在高应变下的 tan δ 值较低，表明：
- ✅ **较低的内摩擦损耗**
- ✅ **有利于降低滚动阻力**

## 五、YK-1 系列样品的 Tg 影响因素

### 结构参数

| 参数 | YK-1 | 对 Tg 的影响 |
|------|------|-------------|
| 苯乙烯含量 | 21.1% | 最低，Tg 相对较低 |
| 乙烯基含量 | 38.1% | 中等 |
| 分子量 (Mn) | 25.8×10⁴ | 最低 |

文献还指出：
> "The glass-transition temperature of YK-1 with lowest styrene content is the lowest, thus the styrene content is an important influencing factor of glass-transition temperature."

苯乙烯含量是影响 Tg 的重要因素，YK-1 因苯乙烯含量最低而具有最低的 Tg。

## 六、综合评价

共凝聚法制备的 YK-1-2 样品的热学性能特点：
- ✅ Tg 提高 2℃，表明填料-聚合物界面相互作用增强
- ✅ tan δ 峰面积减小，内摩擦损耗降低
- ✅ 0℃ tan δ 略高，湿地抓地性能改善
- ✅ 玻璃态 G' 提高，刚性增强

---

## 文献来源

- **DOI**: 10.1002/app.28621
- **图谱引用**: Fig.3 (生胶与共凝聚橡胶), Fig.4 (纳米复合材料)
