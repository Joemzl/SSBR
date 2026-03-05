# SSBR-006 力学性能解读

```yaml
sample_id: SSBR-006
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
    note: "Payne 效应较 M0 降低"
  G_prime_0:
    value: null
    unit: MPa
    confidence: null
  G_prime_inf:
    value: null
    unit: MPa
    confidence: null
  activation_energy:
    value: 12.8
    unit: "kJ/mol"
    confidence: high

dma_properties:
  tan_delta_max:
    value: 1.11
    confidence: high
  tan_delta_0C:
    value: null
    confidence: null
  tan_delta_60C:
    value: null
    confidence: null
```

## 样本基本信息

- **样本编号**: SSBR-006（文献中标记为 M1）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 2.4 wt%
- **功能基团**: -COOH（羧基）
- **填料体系**: 白炭黑 (50 phr) + TESPT (4 phr)
- **文献来源**: Qu et al., RSC Advances, 2014

## 力学性能数据

### Payne 效应分析

| 参数 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 活化能 Ea | 12.8 | kJ/mol | 高 |
| Payne 效应变化 | 降低 | - | 中 |

**与空白样对比**：
| 对比项 | SSBR-005 (M0) | SSBR-006 (M1) | 变化 |
|--------|---------------|---------------|------|
| 活化能 Ea | 11.3 kJ/mol | 12.8 kJ/mol | +13% |
| Payne 效应 | 最大 | 降低 | 改善 |

### DMA 分析

| 指标 | 数值 | 置信度 |
|------|------|--------|
| tan δmax | 1.11 | 高 |
| Tg (DMA) | -3.9℃ | 高 |

## 性能解读

### 官能化效果分析

2.4 wt% 羧基官能化带来的改善：

1. **活化能提升**：从 11.3 提升至 12.8 kJ/mol（+13%）
   - 表明填料网络更稳定
   - 需要更多能量破坏填料结构

2. **Payne 效应降低**：
   - 填料-填料网络被填料-橡胶-填料网络部分取代
   - 网络结构更稳定

3. **tan δmax 提升**：从 1.07 提升至 1.11（+4%）
   - 更多聚合物链参与玻璃化转变
   - 填料团聚减少释放出被束缚的橡胶链

### 机理解释

羧基官能化改善性能的机理：

```
SSBR-COOH + HO-Si≡ → SSBR-COOH···HO-Si≡
                     （氢键作用）
```

- **氢键形成**: -COOH 与 Si-OH 形成氢键
- **极性提升**: 表面极性部分从 0.9 提升至 1.2 mJ/m²
- **粘附功增加**: Wrf 从 51.2 提升至 53.3 mJ/m²

## 数据来源与置信度说明

- 活化能数据来自 Table 5
- DMA 数据来自 Table 6
- 置信度"高"表示直接从表格读取
