---
sample_id: SSBR-044
interpretation_type: dsc
source_figure: Fig.3, Fig.4
source_doi: 10.1002/app.28621
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
data:
  tg_dsc:
    value: null
    unit: ℃
    source: 文献使用 DMTA 测定 Tg，未提供 DSC 数据
  tg_dmta:
    value: null
    unit: ℃
    source: Fig.3, Fig.4 仅提供曲线图，未给出具体数值
  tg_shift_vs_pure:
    value: '+2'
    unit: ℃
    description: 共凝聚橡胶 Tg 比纯 SSBR 高 2℃
    source: 文献正文
  tg_shift_vs_blend:
    value: '+2'
    unit: ℃
    description: N-SSBR/SiO2 复合材料 Tg 比 SSBR/SiO2 高 2℃
    source: 文献正文
  styrene_effect: 最高苯乙烯含量，但 Tg 并非最高
skill_version: '2.0'
curves:
  dsc_heat_flow:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: 热流
      unit: mW/mg
      direction: exo_up
    data_points: []
    curve_features:
      Tg:
        onset: null
        midpoint: null
        endpoint: null
        unit: °C
        source: "文献使用DMTA测定，未给出具体Tg值，仅提供相对变化"
      Tg_shift:
        value: +2
        unit: °C
        reference: "vs SSBR/SiO2"
        source: 文献正文
      styrene_effect:
        note: "YK-3最高苯乙烯含量(29.5%)但Tg中等，乙烯基含量(34.7%)最低"
      glass_transition_width:
        value: null
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: acceptable
      note: "无独立DSC曲线，Tg来自DMTA"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# 热学性能解读：SSBR-044

> **样本性质**: N-SSBR/SiO2 共凝聚纳米复合材料（YK-3-2），采用 AMMO 硅烷偶联剂改性


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-044
- **文献中编号**: YK-3-2（N-SSBR/SiO2 纳米复合材料）
- **基体**: YK-3 星形 SSBR（苯乙烯含量 29.5%，乙烯基含量 34.7%）
- **测试方法**: DMTA（动态力学热分析）
- **测试条件**: 矩形拉伸模式，1 Hz，升温速率 3℃/min，温度范围 -100℃ ~ 100℃
- **文献DOI**: 10.1002/app.28621

## 二、玻璃化转变温度 (Tg)

### 关键发现

文献明确指出：
> "Either the glass-transition temperatures of SSBR or those of SSBR filled with 20 phr organically modified silica are **2°C lower** than those of N-SSBR and N-SSBR filled with the same amount of silica, respectively."

| 材料类型 | Tg 相对变化 |
|---------|-------------|
| 纯 SSBR (YK-3) → 共凝聚橡胶 (YK-3-0) | +2℃ |
| SSBR/SiO2 (YK-3-1) → N-SSBR/SiO2 (YK-3-2) | +2℃ |

### YK-3 的 Tg 特点

YK-3 具有最高的苯乙烯含量（29.5%），但其 Tg 并非三种样本中最高的。

文献指出苯乙烯含量是影响 Tg 的重要因素：
> "The glass-transition temperature of YK-1 with lowest styrene content is the lowest, thus the styrene content is an important influencing factor of glass-transition temperature."

然而，YK-2（苯乙烯 24.2%，乙烯基 46.0%）的 Tg 高于 YK-3（苯乙烯 29.5%，乙烯基 34.7%），说明**乙烯基含量**对 Tg 的影响可能更为显著。

## 三、DMTA 曲线特征

### 储能模量 (G') 变化

文献 Fig.3(c) 显示 YK-3 系列的 G' 特点：

在共凝聚橡胶 (YK-3-0) 中：
> "For the composite (YK-3-0) which contains 7% silica, its G' value is larger than that of YK-3 with an increment of 22-26% in the region of glassy state, and with an increment of 21-32% in the region of high-elastic state."

YK-3-0 的 G' 值在各温度区域均显著高于纯 YK-3 橡胶：
- 玻璃态：+22-26%
- 高弹态：+21-32%

这是因为 YK-3-0 中的白炭黑含量（7 phr）高于 YK-1-0 和 YK-2-0（3 phr）。

### tan δ 峰特征

1. **tan δ 峰高度降低**: 表明内摩擦损耗减小
2. **tan δ 峰面积减小**: 表明分子链解冻过程中的摩擦损耗降低

## 四、动态摩擦特性

### 高应变下的 tan δ

文献 Fig.6 指出 YK-3 系列的特殊行为：
> "the tan δ values (i.e., internal friction loss values) of YK-3-1 and YK-3-2 are slightly higher than the other two series of samples. It is possibly because higher styrene content of YK-3 leads to severe friction among these rigid groups under a certain strain."

YK-3 系列在应变扫描时的 tan δ 值略高，原因是：
- 高苯乙烯含量（29.5%）
- 刚性苯乙烯基团之间的摩擦增加

## 五、三种样本的 Tg 比较

### 结构参数与 Tg 的关系

| 样本 | 苯乙烯含量 | 乙烯基含量 | Tg 相对大小 |
|------|-----------|-----------|-------------|
| YK-1 系列 | 21.1% | 38.1% | 最低 |
| YK-2 系列 | 24.2% | **46.0%** | **最高** |
| **YK-3 系列** | **29.5%** | 34.7% | **中等** |

### 苯乙烯与乙烯基的综合影响

尽管 YK-3 的苯乙烯含量最高，但其 Tg 并非最高，这表明：
1. 乙烯基含量对 Tg 的贡献可能更大
2. YK-3 的乙烯基含量（34.7%）是三种中最低的
3. Tg 由苯乙烯和乙烯基含量共同决定

## 六、共凝聚橡胶 YK-3-0 的特殊性

YK-3-0 与其他两种共凝聚橡胶的区别：
- **白炭黑含量更高**: 7 phr（vs 3 phr）
- **G' 提升更显著**: 玻璃态 +22-26%，高弹态 +21-32%
- **无规度稍低**: 91.5%（vs 100%）

文献 Table I 显示 YK-3 的无规度为 91.5%，表明有部分嵌段苯乙烯序列。

## 七、综合评价

SSBR-044 (YK-3-2) 的热学性能特点：
- ✅ Tg 提高 2℃（相比 SSBR/SiO2 复合材料）
- ⚠️ Tg 并非最高，尽管苯乙烯含量最高
- ⚠️ 高应变下 tan δ 略高（刚性基团摩擦）
- ✅ tan δ 峰面积减小，内摩擦损耗降低

---

## 文献来源

- **DOI**: 10.1002/app.28621
- **图谱引用**: Fig.3(c) (生胶与共凝聚橡胶), Fig.4 (纳米复合材料)
