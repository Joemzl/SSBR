# SSBR-002 力学性能解读

```yaml
sample_id: SSBR-002
interpretation_type: mechanical
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c9ra02783a"
source_figure: "SI Table S5"

mechanical_properties:
  stress_100:
    value: 1.8
    unit: MPa
    confidence: high
  stress_200:
    value: null
    unit: MPa
    confidence: null
  stress_300:
    value: 10.5
    unit: MPa
    confidence: high
  tensile_strength:
    value: 17.5
    unit: MPa
    confidence: high
  elongation_at_break:
    value: 475
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

- **样本编号**: SSBR-002
- **官能团类型**: 3-巯基丙醇（MPL）官能化 SSBR
- **功能基团**: -OH（羟基）
- **填料体系**: 白炭黑 (60 phr)
- **文献来源**: Gao et al., RSC Advances, 2019

## 力学性能数据

### 应力-应变数据

| 指标 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| 100% 定伸应力 | 1.8 | MPa | 高 |
| 200% 定伸应力 | - | MPa | - |
| 300% 定伸应力 | 10.5 | MPa | 高 |
| 拉伸强度 | 17.5 | MPa | 高 |
| 断裂伸长率 | 475 | % | 高 |

### Payne 效应分析

暂无此项数据。

### DMA 分析

暂无此项数据。

## 性能解读

### 官能化效果分析

SSBR-002 采用 3-巯基丙醇（MPL）官能化，引入羟基（-OH）功能基团。与空白 SSBR-001 相比：

1. **100% 定伸应力提升**：从 1.5 MPa 提升至 1.8 MPa（+20%），表明填料-橡胶界面作用增强
2. **300% 定伸应力提升**：从 9.0 MPa 提升至 10.5 MPa（+17%），证明羟基与白炭黑表面硅羟基形成氢键
3. **拉伸强度提升**：从 15.0 MPa 提升至 17.5 MPa（+17%），整体力学性能改善
4. **断裂伸长率略增**：从 452% 提升至 475%（+5%），材料柔韧性保持良好

### 机理解释

羟基官能化 SSBR 通过以下机制改善性能：
- **氢键作用**: -OH 与白炭黑表面 Si-OH 形成氢键，增强界面结合
- **分散性改善**: 官能化改善了白炭黑在橡胶基体中的分散性
- **补强效率**: 更均匀的分散带来更高效的补强效果

## 数据来源与置信度说明

- 力学数据来自文献 SI Table S5
- 数据为标准硫化条件下测得
- 置信度"高"表示数据直接从文献表格读取
