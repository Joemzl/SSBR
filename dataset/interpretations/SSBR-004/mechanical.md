# SSBR-004 力学性能解读

```yaml
sample_id: SSBR-004
interpretation_type: mechanical
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c9ra02783a"
source_figure: "SI Table S5"

mechanical_properties:
  stress_100:
    value: 2.8
    unit: MPa
    confidence: high
  stress_200:
    value: null
    unit: MPa
    confidence: null
  stress_300:
    value: 14.0
    unit: MPa
    confidence: high
  tensile_strength:
    value: 21.5
    unit: MPa
    confidence: high
  elongation_at_break:
    value: 420
    unit: "%"
    confidence: high

payne_effect:
  delta_G_prime:
    value: null
    unit: MPa
    confidence: null
  G_prime_0:
    value: null
    unit: MPa
    confidence: null
  G_prime_inf:
    value: null
    unit: MPa
    confidence: null

dma_properties:
  tan_delta_0C:
    value: null
    confidence: null
  tan_delta_60C:
    value: null
    confidence: null
```

## 样本基本信息

- **样本编号**: SSBR-004
- **官能团类型**: 3-巯基丙基三乙氧基硅烷（MPTES）官能化 SSBR
- **功能基团**: -Si(OC₂H₅)₃（三乙氧基硅烷基）
- **填料体系**: 白炭黑 (60 phr)
- **文献来源**: Gao et al., RSC Advances, 2019

## 力学性能数据

### 应力-应变数据

| 指标 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 100% 定伸应力 | 2.8 | MPa | 高 |
| 200% 定伸应力 | - | MPa | - |
| 300% 定伸应力 | 14.0 | MPa | 高 |
| 拉伸强度 | 21.5 | MPa | 高 |
| 断裂伸长率 | 420 | % | 高 |

### Payne 效应分析

暂无此项数据。

### DMA 分析

暂无此项数据。

## 性能解读

### 官能化效果分析

SSBR-004 采用 MPTES 官能化，引入三乙氧基硅烷基，这是系列中力学性能最优的样品：

| 对比项 | SSBR-001 | SSBR-002 | SSBR-003 | SSBR-004 | 004 vs 001 |
|--------|----------|----------|----------|----------|------------|
| 官能团 | 无 | -OH | -COOH | -Si(OEt)₃ | - |
| 100% 应力 | 1.5 | 1.8 | 2.3 | **2.8** | **+87%** |
| 300% 应力 | 9.0 | 10.5 | 12.5 | **14.0** | **+56%** |
| 拉伸强度 | 15.0 | 17.5 | 19.0 | **21.5** | **+43%** |
| 伸长率 | 452 | 475 | 430 | 420 | -7% |

**关键发现**：
- **最高的定伸应力和拉伸强度**: 硅烷官能化样品在所有力学指标上均为最优
- **伸长率适中下降**: 420%，反映更强的界面约束
- **综合性能最佳**: 力学性能提升与加工性能保持良好平衡

### 机理解释

三乙氧基硅烷官能化 SSBR 性能最优的原因：

1. **共价键合作用**:
   - -Si(OC₂H₅)₃ 与白炭黑表面 Si-OH 发生缩合反应
   - 形成 Si-O-Si 共价键
   - 界面结合强度远高于氢键

2. **化学偶联效应**:
   - 硅烷基团起到偶联剂作用
   - 连接有机相（SSBR）和无机相（白炭黑）
   - 实现真正的化学桥接

3. **反应机理**:
```
SSBR-Si(OC₂H₅)₃ + HO-Si≡ → SSBR-Si-O-Si≡ + C₂H₅OH
    (硅烷基)       (白炭黑)    (共价键合)   (乙醇)
```

### 与传统硅烷偶联剂对比

MPTES 官能化 SSBR 的优势（相比外加硅烷偶联剂）：
- **预先结合**: 硅烷基团已经连接在 SSBR 分子链上
- **更均匀分布**: 随橡胶分子链均匀分布
- **更高效率**: 避免偶联剂在混炼过程中的损失
- **更强界面**: 更高比例的硅烷参与界面反应

## 数据来源与置信度说明

- 力学数据来自文献 SI Table S5
- 数据为标准硫化条件下测得
- 置信度"高"表示数据直接从文献表格读取
