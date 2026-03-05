# SSBR-007 力学性能解读

```yaml
sample_id: SSBR-007
interpretation_type: mechanical
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Fig. 2, Table 5"

mechanical_properties:
  stress_100:
    value: null
    unit: MPa
    confidence: null
  stress_200:
    value: null
    unit: MPa
    confidence: null
  stress_300:
    value: null
    unit: MPa
    confidence: null
  tensile_strength:
    value: null
    unit: MPa
    confidence: null
  elongation_at_break:
    value: null
    unit: "%"
    confidence: null

payne_effect:
  delta_G_prime:
    value: null
    unit: MPa
    confidence: medium
    note: "Payne 效应进一步降低"
  activation_energy:
    value: 14.2
    unit: "kJ/mol"
    confidence: high

dma_properties:
  tan_delta_max:
    value: 1.19
    confidence: high
  tan_delta_0C:
    value: null
    confidence: null
  tan_delta_60C:
    value: null
    confidence: null
```

## 样本基本信息

- **样本编号**: SSBR-007（文献中标记为 M2）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 4.2 wt%
- **功能基团**: -COOH（羧基）
- **填料体系**: 白炭黑 (50 phr) + TESPT (4 phr)
- **文献来源**: Qu et al., RSC Advances, 2014

## 力学性能数据

### Payne 效应分析

| 参数 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 活化能 Ea | 14.2 | kJ/mol | 高 |
| Payne 效应变化 | 进一步降低 | - | 中 |

**系列样品对比**：
| 样品 | 官能化含量 | 活化能 Ea | 变化 vs M0 |
|------|------------|-----------|-----------|
| SSBR-005 (M0) | 0 | 11.3 kJ/mol | - |
| SSBR-006 (M1) | 2.4 wt% | 12.8 kJ/mol | +13% |
| SSBR-007 (M2) | 4.2 wt% | 14.2 kJ/mol | +26% |

### DMA 分析

| 指标 | 数值 | 置信度 |
|------|------|--------|
| tan δmax | 1.19 | 高 |
| Tg (DMA) | -2.7℃ | 高 |

## 性能解读

### 官能化效果分析

4.2 wt% 羧基官能化的改善效果：

1. **活化能大幅提升**：14.2 kJ/mol（比空白样高 26%）
   - 填料-橡胶-填料网络更加稳定
   - 破坏网络需要更高能量

2. **tan δmax 显著提升**：1.19（比空白样高 11%）
   - 更多聚合物链参与玻璃化转变
   - 填料分散性明显改善

3. **Payne 效应持续降低**：
   - 填料团聚进一步减少
   - 界面作用更强

### 性能优化趋势

官能化含量与性能的关系呈现正相关：

```
官能化含量 ↑ → 表面极性 ↑ → 界面作用 ↑ → 分散性 ↑ → 性能 ↑
   0%           0.9 mJ/m²     51.2 mJ/m²    差          基准
   2.4%         1.2 mJ/m²     53.3 mJ/m²    中等        +13%
   4.2%         2.3 mJ/m²     55.8 mJ/m²    良好        +26%
```

### 机理解释

更高官能化含量（4.2 wt%）带来的增益：
- 更多羧基参与氢键形成
- 更均匀的界面包覆
- 更有效的填料稳定化

## 数据来源与置信度说明

- 活化能数据来自 Table 5
- DMA 数据来自 Table 6
- 置信度"高"表示直接从表格读取
