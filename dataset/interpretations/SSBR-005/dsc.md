# SSBR-005 DSC 热分析解读

```yaml
sample_id: SSBR-005
interpretation_type: dsc
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Table 6, Fig. 11"

thermal_properties:
  tg:
    value: -27.2
    unit: "℃"
    confidence: high
    method: DSC
  tg_dma:
    value: -5.9
    unit: "℃"
    confidence: high
    method: DMA
  
  heat_capacity:
    delta_cp:
      value: 0.23
      unit: "J/(g·K)"
      confidence: high

  thermal_stability:
    decomposition_onset:
      value: null
      unit: "℃"
      confidence: null
```

## 样本基本信息

- **样本编号**: SSBR-005（文献中标记为 M0）
- **官能团类型**: 无（空白未官能化 SSBR）
- **功能基团**: -
- **填料体系**: 白炭黑 (50 phr)
- **文献来源**: Qu et al., RSC Advances, 2014

## 热学性能数据

### 玻璃化转变温度 (Tg)

| 测试方法 | Tg 数值 | 单位 | 置信度 |
|----------|---------|------|--------|
| DSC | -27.2 | ℃ | 高 |
| DMA | -5.9 | ℃ | 高 |

### 热容变化 (ΔCp)

| 指标 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| ΔCp | 0.23 | J/(g·K) | 高 |

## 性能解读

### Tg 分析

**DSC vs DMA Tg 差异**：
- DSC 测得 Tg = -27.2℃（纯橡胶相的玻璃化转变）
- DMA 测得 Tg = -5.9℃（复合材料整体的动态响应）

两种方法测得的 Tg 差异约 21℃，主要原因：
1. **测试原理不同**: DSC 测量热流，DMA 测量力学响应
2. **频率效应**: DMA 在 10 Hz 频率下测试，Tg 会向高温偏移
3. **填料效应**: 白炭黑对 DMA 响应有显著影响

### ΔCp 的物理意义

ΔCp = 0.23 J/(g·K) 反映了参与玻璃化转变的聚合物链段比例：
- 较低的 ΔCp 表明部分聚合物链被填料束缚
- 在未官能化体系中，束缚橡胶主要来自物理吸附

### 系列对比（作为基准）

| 样品 | DSC Tg (℃) | DMA Tg (℃) | ΔCp (J/g·K) |
|------|------------|------------|-------------|
| SSBR-005 (M0) | -27.2 | -5.9 | 0.23 |

## 数据来源与置信度说明

- Tg-DSC 数据来自 Table 6 (T-c 列)
- Tg-DMA 数据来自 Table 6
- ΔCp 数据来自 Table 7
- 置信度"高"表示直接从表格读取
