---
sample_id: SSBR-015
interpretation_type: dsc
source_figure: Fig.3, Fig.12
source_doi: 10.1021/acs.iecr.6b02259
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: '2026-03-31'
data:
  tg_dsc:
    value: null
    unit: ℃
    source: Fig.3 显示 Tg 曲线但未给出具体数值
  tan_delta_0c:
    description: 随 DPES 含量增加而增大
    source: Fig.12, Table S5
  tan_delta_60c:
    description: 相比 SBDR-0 降低 30.8%
    source: Fig.12, Table S5
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
        source: "Fig. 3 (仅有曲线图，无具体数值)"
        confidence: null
        note: "三种 SBDR 样品 Tg 曲线位置相近，无显著差异"
      glass_transition_width:
        value: null
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: "poor"
      note: "文献 Fig.3 提供 DSC 曲线图但未标注具体 Tg 数值"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# 热学性能解读：SSBR-015

> **样本性质**: DPES 官能化 SSBR/炭黑复合材料（SBDR-5），5.1 wt% DPES 含量


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 一、基础信息

- **样本ID**: SSBR-015
- **文献中编号**: SBDR-5 / CB/SBDR-5 硫化胶
- **基体**: 溶聚苯乙烯-丁二烯-DPES 共聚物
- **测试方法**: DSC (Fig.3) 和 DMTA (Fig.12)
- **文献DOI**: 10.1021/acs.iecr.6b02259

## 二、玻璃化转变温度 (Tg)

### DSC 测试结果 (Fig.3)

文献 Fig.3 显示了 SBDR-0, SBDR-2, SBDR-5 的 DSC 曲线：
> "the DSC curves of SBDR displayed in Figure 3 show only one glass transition temperature, providing further evidence of the random distribution of monomers along the SBDR chain."

关键发现：
1. **单一 Tg**: 所有 SBDR 样品只显示一个玻璃化转变温度
2. **无规分布**: 单一 Tg 证明了 Bd、St、DPES 三种单体在聚合物链中的无规分布
3. **无相分离**: DPES 的引入未导致微相分离

### Tg 变化趋势

文献未给出具体 Tg 数值，但从 Fig.3 可以观察到 DPES 含量增加对 Tg 的影响较小，三种样品的 Tg 曲线位置相近。

## 三、动态力学热分析 (DMTA)

### 测试条件

- 仪器: VA 3000 动态力学热分析仪 (01 dB-Metravib)
- 模式: 拉伸模式
- 频率: 1 Hz
- 温度范围: -80℃ ~ 80℃
- 升温速率: 3℃/min
- 应变: 0.02%

### tan δ 温度扫描结果 (Fig.12)

文献 Fig.12 显示了 CB/SBDR 硫化胶的 tan δ-温度曲线。

## 四、轮胎性能指标

### 0℃ tan δ（湿地抓地力指标）

文献指出：
> "the value of the loss factor at 0 °C for SBDR vulcanizates increased with an increase in DPES content, indicating that the functionalization of a rubber matrix by introducing DPES groups along its backbone improves wet skid resistance."

CB/SBDR-5 在 0℃ 的 tan δ 值**增大**，表明：
- ✅ **湿地抓地力提高**

### 60℃ tan δ（滚动阻力指标）

文献指出：
> "The values of the loss factor at 60 °C for SBDR-2 and SBDR-5 vulcanizates were lower than that of SBDR-0, suggesting lowered rolling resistance."

具体数据（Table S5）：
> "1.9 wt % and 5.1 wt % DPES in SBDR led to **18.3%** and **30.8%** decreases in the value of tanδ at 60 °C, respectively."

| 样本 | DPES 含量 | 60℃ tan δ 变化 |
|------|----------|----------------|
| CB/SBDR-0 | 0% | 基准 |
| CB/SBDR-2 | 1.9% | -18.3% |
| **CB/SBDR-5** | **5.1%** | **-30.8%** |

CB/SBDR-5 的 60℃ tan δ 降低 **30.8%**，表明：
- ✅ **滚动阻力显著降低**

### 机理分析

文献解释了 tan δ 变化的机理：
> "This observation can be attributed to the strengthened interaction between CB and the DPES-functionalized rubber matrix as a result of the formation of covalent bonds. The strong interaction between CB and the rubber matrix lowered the mobility of the rubber chain and improved CB dispersion."

1. **共价键界面**: DPES 与炭黑形成共价键
2. **分子链运动受限**: 界面相互作用限制橡胶链的活动性
3. **填料分散改善**: 炭黑分散更均匀

## 五、轮胎应用性能总结

| 性能指标 | CB/SBDR-5 表现 | 对轮胎的意义 |
|---------|---------------|--------------|
| 0℃ tan δ | ↑ 增大 | ✅ 湿地抓地力提高 |
| 60℃ tan δ | ↓ 降低 30.8% | ✅ 滚动阻力降低 |

文献结论：
> "In particular, the introduction of DPES into a rubber matrix will be favorable for higher wet skid resistance and lower rolling resistance, indicating great potential for application in the tread rubber of green tires."

DPES 官能化 SSBR 同时实现了**更高的湿地抓地力**和**更低的滚动阻力**，是理想的绿色轮胎胎面材料。

## 六、综合评价

SSBR-015 (CB/SBDR-5) 的热学性能特点：
- ✅ 单一 Tg，表明无规共聚结构
- ✅ 0℃ tan δ 增大，湿地抓地力提高
- ✅ 60℃ tan δ 降低 30.8%，滚动阻力显著降低
- ✅ 适用于绿色轮胎胎面材料

---

## 文献来源

- **DOI**: 10.1021/acs.iecr.6b02259
- **图谱引用**: Fig.3 (DSC), Fig.12 (DMTA); Table S5
