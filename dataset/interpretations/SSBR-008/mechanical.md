# SSBR-008 力学性能解读

```yaml
sample_id: SSBR-008
interpretation_type: mechanical
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Fig. 2, 3, 9, 10, Table 5"

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
    note: "Payne 效应最小，G'0 最低"
  activation_energy:
    value: 17.7
    unit: "kJ/mol"
    confidence: high

dma_properties:
  tan_delta_max:
    value: 1.30
    confidence: high
  tan_delta_60C:
    value: null
    confidence: null
    note: "50-80℃区间 tan δ 最低"
  loss_modulus_high_temp:
    value: null
    confidence: medium
    note: "高温区 G'' 最低"
```

## 样本基本信息

- **样本编号**: SSBR-008（文献中标记为 M3）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 9.6 wt%
- **功能基团**: -COOH（羧基）
- **填料体系**: 白炭黑 (50 phr) + TESPT (4 phr)
- **文献来源**: Qu et al., RSC Advances, 2014

## 力学性能数据

### Payne 效应分析

| 参数 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 活化能 Ea | 17.7 | kJ/mol | 高 |
| Payne 效应 | 最小 | - | 高 |
| G'0 | 最低 | - | 中 |

**系列完整对比**：
| 样品 | 官能化 | Ea (kJ/mol) | vs M0 |
|------|--------|-------------|-------|
| M0 | 0 | 11.3 | - |
| M1 | 2.4% | 12.8 | +13% |
| M2 | 4.2% | 14.2 | +26% |
| **M3** | **9.6%** | **17.7** | **+57%** |

### DMA 分析

| 指标 | 数值 | 置信度 | 说明 |
|------|------|--------|------|
| tan δmax | 1.30 | 高 | 系列最高 |
| Tg (DMA) | 0.1℃ | 高 | 系列最高 |
| 高温区 tan δ | 最低 | 高 | 50-80℃ |
| 高温区 G'' | 最低 | 中 | 滞后损耗最小 |

## 性能解读

### 最优官能化效果

9.6 wt% 羧基官能化实现了最优性能：

1. **活化能最高**：17.7 kJ/mol（比空白样高 57%）
   - 填料网络稳定性最高
   - 完全转变为填料-橡胶-填料网络

2. **tan δmax 最高**：1.30（比空白样高 21%）
   - 最多聚合物链参与玻璃化转变
   - 低温区能量耗散能力最强

3. **高温区性能最优**：
   - 50-80℃区间 tan δ 最低
   - 滞后损耗最小，滚动阻力最低

### 轮胎性能平衡

文献的核心结论之一：

> "A combination of higher energy dissipation in the low temperature range and higher elasticity in the high temperature region were achieved for M-S-SBR/Silica when compared with their non-modified counterpart."

M3（SSBR-008）实现了：
- **低温区**（-10~10℃）：高能量耗散 → 优异湿抓地力
- **高温区**（50~80℃）：低滞后损耗 → 低滚动阻力

这是绿色轮胎追求的理想"魔三角"平衡！

### 机理解释

高官能化含量带来综合性能优化的机理：

1. **界面作用最强**: 粘附功 Wrf = 62.1 mJ/m²（最高）
2. **絮凝驱动力最低**: ΔW = 4.6 mJ/m²（最低）
3. **分散性最好**: 均匀细腻的填料分散
4. **网络结构优化**: 稳定的填料-橡胶-填料网络

## 数据来源与置信度说明

- 活化能数据来自 Table 5
- DMA 数据来自 Table 6, Fig. 9, 10
- 置信度"高"表示直接从表格/图谱读取
