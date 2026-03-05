# SSBR-003 力学性能解读

```yaml
sample_id: SSBR-003
interpretation_type: mechanical
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c9ra02783a"
source_figure: "SI Table S5"

mechanical_properties:
  stress_100:
    value: 2.3
    unit: MPa
    confidence: high
  stress_200:
    value: null
    unit: MPa
    confidence: null
  stress_300:
    value: 12.5
    unit: MPa
    confidence: high
  tensile_strength:
    value: 19.0
    unit: MPa
    confidence: high
  elongation_at_break:
    value: 430
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

- **样本编号**: SSBR-003
- **官能团类型**: 11-巯基十一烷酸（MUA）官能化 SSBR
- **功能基团**: -COOH（羧基）
- **填料体系**: 白炭黑 (60 phr)
- **文献来源**: Gao et al., RSC Advances, 2019

## 力学性能数据

### 应力-应变数据

| 指标 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 100% 定伸应力 | 2.3 | MPa | 高 |
| 200% 定伸应力 | - | MPa | - |
| 300% 定伸应力 | 12.5 | MPa | 高 |
| 拉伸强度 | 19.0 | MPa | 高 |
| 断裂伸长率 | 430 | % | 高 |

### Payne 效应分析

暂无此项数据。

### DMA 分析

暂无此项数据。

## 性能解读

### 官能化效果分析

SSBR-003 采用 11-巯基十一烷酸（MUA）官能化，引入羧基（-COOH）功能基团。与其他样品对比：

| 对比项 | SSBR-001 (空白) | SSBR-002 (-OH) | SSBR-003 (-COOH) | SSBR-003 vs 001 |
|--------|-----------------|----------------|------------------|-----------------|
| 100% 应力 | 1.5 MPa | 1.8 MPa | 2.3 MPa | +53% |
| 300% 应力 | 9.0 MPa | 10.5 MPa | 12.5 MPa | +39% |
| 拉伸强度 | 15.0 MPa | 17.5 MPa | 19.0 MPa | +27% |
| 伸长率 | 452% | 475% | 430% | -5% |

**关键发现**：
1. **最高的定伸应力**: 羧基官能化样品的 100% 和 300% 定伸应力最高
2. **最高的拉伸强度**: 19.0 MPa，明显优于空白和羟基官能化样品
3. **伸长率略降**: 430%，较空白样略有下降，表明更强的界面约束

### 机理解释

羧基官能化 SSBR 性能最优的原因：

1. **强氢键作用**: -COOH 与白炭黑表面 Si-OH 形成强氢键
2. **长碳链效应**: MUA 含有 11 个碳的长链，起到"内增塑剂"作用
3. **界面层优化**: 长碳链在填料表面形成有序排列，改善应力传递
4. **高极性**: 羧基极性强，与白炭黑亲和力更高

### 与其他官能团对比

羧基 (-COOH) vs 羟基 (-OH)：
- 羧基酸性更强，氢键能力更强
- 长碳链提供额外的界面优化效果
- 整体力学性能提升更显著

## 数据来源与置信度说明

- 力学数据来自文献 SI Table S5
- 数据为标准硫化条件下测得
- 置信度"高"表示数据直接从文献表格读取
