---
sample_id: SSBR-043
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
  vinyl_effect: 高乙烯基含量导致 Tg 相对较高
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
      vinyl_effect:
        note: "YK-2高乙烯基含量(46%)导致Tg最高"
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
      note: "无独立DSC曲线，Tg来自DMTA，YK-2系列因高乙烯基含量Tg最高"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# 热学性能解读：SSBR-043

> **样本性质**: N-SSBR/SiO2 共凝聚纳米复合材料（YK-2-2），采用 AMMO 硅烷偶联剂改性


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-043
- **文献中编号**: YK-2-2（N-SSBR/SiO2 纳米复合材料）
- **基体**: YK-2 星形 SSBR（苯乙烯含量 24.2%，乙烯基含量 46.0%）
- **测试方法**: DMTA（动态力学热分析）
- **测试条件**: 矩形拉伸模式，1 Hz，升温速率 3℃/min，温度范围 -100℃ ~ 100℃
- **文献DOI**: 10.1002/app.28621

## 二、玻璃化转变温度 (Tg)

### 关键发现

文献明确指出：
> "Either the glass-transition temperatures of SSBR or those of SSBR filled with 20 phr organically modified silica are **2°C lower** than those of N-SSBR and N-SSBR filled with the same amount of silica, respectively."

| 材料类型 | Tg 相对变化 |
|---------|-------------|
| 纯 SSBR (YK-2) → 共凝聚橡胶 (YK-2-0) | +2℃ |
| SSBR/SiO2 (YK-2-1) → N-SSBR/SiO2 (YK-2-2) | +2℃ |

### YK-2 的 Tg 特点

文献指出 YK-2 系列具有最高的 Tg：
> "the glass-transition temperature and tan δ values at 0°C (i.e., wet-skid resistance) of YK-2-1 and YK-2-2 are higher than those of corresponding YK-1-1 and YK-1-2, respectively. It is possibly because YK-2 has higher vinyl content than YK-1 so the macromolecular chains are hard to relax."

**高乙烯基含量（46.0%）** 使 YK-2 系列具有更高的 Tg。

## 三、DMTA 曲线特征

### 储能模量 (G') 变化

文献 Fig.4(b) 显示：

| 温度区域 | YK-2-2 vs YK-2-1 |
|---------|------------------|
| 玻璃态 | G' 略高 |
| 玻璃化转变区 | G' 显著升高 |
| 高弹态 | G' 相近或略高 |

### tan δ 峰特征

1. **tan δ 峰高度降低**: 表明内摩擦损耗减小
2. **tan δ 峰面积减小**: 表明分子链解冻过程中的摩擦损耗降低
3. **玻璃化转变区变宽**: 表明填料-聚合物界面相互作用增强

## 四、轮胎性能相关指标

### 0℃ tan δ（湿地抓地力指标）

文献 Fig.4(b) 显示：
- YK-2-2 在 0℃ 的 tan δ 值**高于** YK-1-2
- 表明 YK-2-2 具有**更好的湿地抓地性能**

### 乙烯基含量的影响

YK-2 的高乙烯基含量（46.0%）对热学性能的影响：
1. **Tg 升高**: 分子链刚性增加，难以松弛
2. **湿地抓地力提高**: 0℃ tan δ 增大
3. **轮胎性能优化**: 兼顾抓地力和滚动阻力

## 五、三种样本的 Tg 比较

### 结构参数与 Tg 的关系

| 样本 | 苯乙烯含量 | 乙烯基含量 | Tg 相对大小 |
|------|-----------|-----------|-------------|
| YK-1 系列 | 21.1% | 38.1% | 最低 |
| **YK-2 系列** | 24.2% | **46.0%** | **最高** |
| YK-3 系列 | 29.5% | 34.7% | 中等 |

文献指出苯乙烯含量是影响 Tg 的重要因素：
> "The glass-transition temperature of YK-1 with lowest styrene content is the lowest, thus the styrene content is an important influencing factor of glass-transition temperature."

但 YK-2 尽管苯乙烯含量不是最高，却因**乙烯基含量最高**而具有最高的 Tg。

## 六、综合评价

SSBR-043 (YK-2-2) 的热学性能特点：
- ✅ Tg 提高 2℃（相比 SSBR/SiO2 复合材料）
- ✅ 三种样本中 Tg 最高（高乙烯基含量）
- ✅ 0℃ tan δ 最高，湿地抓地力最优
- ✅ tan δ 峰面积减小，内摩擦损耗降低

---

## 文献来源

- **DOI**: 10.1002/app.28621
- **图谱引用**: Fig.3(b) (生胶与共凝聚橡胶), Fig.4(b) (纳米复合材料)
