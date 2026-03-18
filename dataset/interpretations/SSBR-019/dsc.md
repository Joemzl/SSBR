---
sample_id: SSBR-019
interpretation_type: dsc
source_figure: "Fig.3, Fig.12"
source_doi: "10.1021/acs.iecr.6b02259"
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-18
updated_at: null

data:
  tg_composite:
    value: -45
    unit: "℃"
    source: "Fig.3 DSC曲线估读"
  tg_pure_polymer:
    value: null
    unit: "℃"
    source: "文献未提供"
  crystallization_temp:
    value: null
    unit: "℃"
    source: "文献未涉及"
  melting_temp:
    value: null
    unit: "℃"
    source: "文献未涉及"
  
  # DMA 动态力学数据
  tan_delta_0C:
    value: null
    description: "随 DPES 含量增加而增加"
    source: "Fig.12"
  tan_delta_60C:
    value: null
    description: "随 DPES 含量增加而降低，SBDR-5 降低 30.8%"
    source: "Fig.12, Table S5"
---

# 热学性能解读：SSBR-019

> **样本性质**: DPES 官能化 SSBR/炭黑复合材料（SBDR-5），5.1 wt% DPES 含量

## 一、基础信息

- **样本ID**: SSBR-019
- **文献中编号**: SBDR-5
- **基体**: 溶聚苯乙烯-丁二烯-DPES 共聚物
- **官能化试剂**: DPES (p-(2,2'-二苯基乙基)苯乙烯)
- **官能化程度**: 5.1 wt% DPES
- **文献DOI**: 10.1021/acs.iecr.6b02259

## 二、DSC 玻璃化转变

### 核心发现

文献 Fig.3 显示三种 SBDR 的 DSC 曲线：
> "the DSC curves of SBDR displayed in Figure 3 show only one glass transition temperature, providing further evidence of the random distribution of monomers along the SBDR chain."

| 样本 | DPES 含量 | Tg (℃) | 说明 |
|------|----------|--------|------|
| SBDR-0 | 0% | ~-47 | 基准 |
| SBDR-2 | 1.9% | ~-46 | 略微升高 |
| **SBDR-5** | **5.1%** | **~-45** | 略微升高 |

### Tg 变化分析

1. **单一 Tg**: 三种 SBDR 都只有一个 Tg，说明单体随机分布
2. **Tg 略升高**: 随 DPES 含量增加，Tg 略有升高
3. **原因**: DPES 中的刚性苯环结构限制链段运动

---

## 三、动态力学热分析（DMA）

### 核心发现

文献 Fig.12 和 Table S5 显示了动态力学性能数据，这对绿色轮胎胎面胶设计至关重要：

> "The loss factor, tanδ, at 0 °C and 60 °C is particularly relevant to the design of the tread rubber of green tires from the standpoints of safety and fuel consumption."

### 湿地抓地力（tan δ @ 0°C）

文献指出：
> "A higher loss factor at 0 °C... impart higher wet skid resistance"

> "the value of the loss factor at 0 °C for SBDR vulcanizates increased with an increase in DPES content, indicating that the functionalization of a rubber matrix by introducing DPES groups along its backbone improves wet skid resistance."

| 样本 | DPES 含量 | tan δ @ 0°C | 说明 |
|------|----------|-------------|------|
| CB/SBDR-0 | 0% | 基准 | - |
| CB/SBDR-2 | 1.9% | 增加 | 改善 |
| **CB/SBDR-5** | **5.1%** | **进一步增加** | **最佳** |

### 滚动阻力（tan δ @ 60°C）

文献指出：
> "lower loss factor at 60 °C... impart... lower rolling resistance"

> "The values of the loss factor at 60 °C for SBDR-2 and SBDR-5 vulcanizates were lower than that of SBDR-0, suggesting lowered rolling resistance."

| 样本 | DPES 含量 | tan δ @ 60°C 变化 | 说明 |
|------|----------|------------------|------|
| CB/SBDR-0 | 0% | 基准 | - |
| CB/SBDR-2 | 1.9% | **-18.3%** | 改善 |
| **CB/SBDR-5** | **5.1%** | **-30.8%** | **最佳** |

### 动态性能改善机理

文献解释：
> "This observation can be attributed to the strengthened interaction between CB and the DPES-functionalized rubber matrix as a result of the formation of covalent bonds. The strong interaction between CB and the rubber matrix lowered the mobility of the rubber chain and improved CB dispersion."

1. **共价键界面作用**: DPES 与炭黑形成共价键
2. **链段运动受限**: 强界面相互作用降低链段迁移率
3. **填料分散改善**: 更好的分散减少内耗

---

## 四、轮胎性能魔三角分析

### 绿色轮胎性能平衡

| 性能指标 | SBDR-5 表现 | 评价 |
|---------|------------|------|
| 湿地抓地力 (tan δ @ 0°C) | 最高 | ✅ 优秀 |
| 滚动阻力 (tan δ @ 60°C) | 降低 30.8% | ✅ 优秀 |
| 耐磨性 | 未测试 | - |

SSBR-019 成功实现了湿地抓地力和滚动阻力的双优化，打破了传统橡胶中两者的矛盾关系。

---

## 五、综合评价

SSBR-019 (SBDR-5) 的热学/动态力学特点：
- ✅ Tg 约 -45°C，保持良好低温性能
- ✅ 湿地抓地力（tan δ @ 0°C）最高
- ✅ 滚动阻力（tan δ @ 60°C）降低 30.8%
- ✅ 符合绿色轮胎高湿抓、低滚阻要求
- ⚠️ 具体 tan δ 数值需查阅 Table S5

---

## 文献来源

- **DOI**: 10.1021/acs.iecr.6b02259
- **数据引用**: Fig.3 (DSC), Fig.12 (DMA), Table S5
