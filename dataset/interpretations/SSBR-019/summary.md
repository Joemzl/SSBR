---
sample_id: SSBR-019
doi: 10.1021/acs.iecr.6b02259
polymer_type: 二苯基乙基 (triphenylethane pendant)官能化 SSBR
functionalization:
  is_functionalized: true
  type: in_chain
  reagent: p-(2,2'-二苯基乙基)苯乙烯 (DPES)
  functional_group: 二苯基乙基 (triphenylethane pendant)
  degree: null
  method: null
filler_system: null
application: null
data_completeness:
  mechanical: true
  dsc: true
  nmr: true
  tem: true
keywords: []
created_at: 2026-03-18
updated_at: '2026-03-19'
---
# 综合档案：SSBR-019

> **一句话总结**: DPES 官能化 SSBR 通过热分解产生自由基与炭黑形成共价键界面，显著改善炭黑分散、力学性能和动态性能，适用于绿色轮胎胎面胶。

## 一、样本概述

| 属性 | 值 |
|------|-----|
| **样本ID** | SSBR-019 |
| **文献编号** | SBDR-5 / CB/SBDR-5 |
| **DOI** | 10.1021/acs.iecr.6b02259 |
| **官能化类型** | 链中官能化（共聚单体） |
| **官能化试剂** | p-(2,2'-二苯基乙基)苯乙烯 (DPES) |
| **核心官能团** | 二苯基乙基 (triphenylethane pendant) |
| **官能化程度** | 5.1 wt% DPES |
| **苯乙烯含量** | 20.1 wt% |
| **分子量 (Mn)** | 196,000 g/mol |
| **PDI** | 1.23 |
| **填料** | 炭黑 N330 |

## 二、核心创新点

### 2.1 热分解自由基接枝机理

DPES 含有三苯基乙烷 (ETB) 悬挂基团，在加工温度下可热分解产生聚合物自由基：

```
DPES 热分解 (>100°C) → 苄基自由基 + 二苯甲基自由基
         ↓
聚合物自由基被炭黑表面多环芳烃捕获
         ↓
     形成共价键界面
```

这是一种**通用方法**，可用于改善含少量官能团的碳材料（如炭黑、碳纳米管、石墨烯）在聚合物中的分散。

### 2.2 与传统方法的比较

| 方法 | 局限性 | DPES 方法优势 |
|------|--------|--------------|
| 改性炭黑 | 多步骤、条件苛刻 | 原位反应 |
| 添加相容剂 | 额外组分 | 一体化 |
| 环氧/羧基/氨基改性橡胶 | 需要炭黑表面官能团 | **不依赖炭黑官能团** |

## 三、关键性能对比

### 3.1 力学性能

| 指标 | CB/SBDR-0 | CB/SBDR-5 | 变化 |
|------|-----------|-----------|------|
| 拉伸强度 | 基准 | **+43.8%** | ✅ 显著提升 |
| 断裂伸长率 | 基准 | **+11.6%** | ✅ 同时提升 |
| 结合橡胶 | 13.5% | **26.9%** | ✅ 2倍 |

**特别之处**: 拉伸强度和伸长率同时提升（通常二者相互制约）。

### 3.2 动态性能（轮胎性能）

| 指标 | CB/SBDR-0 | CB/SBDR-5 | 变化 | 轮胎意义 |
|------|-----------|-----------|------|----------|
| tan δ @ 0°C | 基准 | 增加 | ✅ | **湿地抓地力↑** |
| tan δ @ 60°C | 基准 | **-30.8%** | ✅ | **滚动阻力↓** |

### 3.3 填料分散

| 指标 | CB/SBDR-0 | CB/SBDR-5 | 变化 |
|------|-----------|-----------|------|
| TEM 分散质量 | 明显团聚 | **均匀分散** | ✅ |
| 团聚体 Rg (nm) | 24.15 | **18.16** | ✅ -25% |
| Payne 效应 | 高 | **低** | ✅ 降低 |

## 四、结构-性能关系

```
DPES (5.1 wt%)
      │
      ├─→ 热分解产生自由基 ─→ 与炭黑形成共价键
      │                           │
      │                           ├─→ 界面强度↑ ─→ 应力传递↑ ─→ 拉伸强度↑
      │                           │
      │                           └─→ 填料分散↑ ─→ Payne效应↓ ─→ 滚动阻力↓
      │
      └─→ 参与硫化反应 ─→ 交联密度↑ ─→ 力学性能↑
```

## 五、应用场景

### 5.1 绿色轮胎胎面胶

SSBR-019 特别适用于绿色轮胎胎面胶：

| 性能 | 要求 | SSBR-019 表现 |
|------|------|--------------|
| 湿地抓地力 | 高 | ✅ tan δ @ 0°C 增加 |
| 滚动阻力 | 低 | ✅ tan δ @ 60°C 降低 30.8% |
| 耐磨性 | 高 | 未测试 |

### 5.2 其他碳材料复合材料

文献指出该方法具有普适性：
> "This DPES-functionalized rubber matrix can also interact covalently with other carbon materials, such as carbon nanotubes and graphene"

## 六、数据可靠性评估

| 数据类型 | 来源 | 可靠性 |
|---------|------|--------|
| 组成 | Table 1, NMR | L1 |
| 力学性能提升比例 | Table S4 | L1 |
| tan δ 变化比例 | Table S5 | L1 |
| 结合橡胶 | 正文 | L1 |
| Tg | Fig.3 DSC | L2 |
| 团聚体 Rg | Table 2 SAXS | L1 |
| 分散质量 | Fig.8 TEM | L2 |

## 七、相关样本

| 样本ID | 关系 | 说明 |
|--------|------|------|
| SSBR-015 | 同源 | 同一文献 SBDR-5 |
| SSBR-016 | 同源 | 同一文献 SBDR-5 |

## 八、文献来源

- **完整引用**: Huang M, Lu J, Han B, et al. A covalent grafting approach for improving the dispersion of carbon black in styrene-butadiene rubber composites by copolymerizing p-(2,2'-diphenylethyl)styrene with a thermally decomposed triphenylethane pendant[J]. Industrial & Engineering Chemistry Research, 2016, 55(34): 9190-9198.
- **DOI**: 10.1021/acs.iecr.6b02259
- **关键图表**: Fig.1 (NMR), Fig.3 (DSC), Fig.8 (TEM), Fig.10 (Payne), Fig.11 (力学), Fig.12 (DMA)
