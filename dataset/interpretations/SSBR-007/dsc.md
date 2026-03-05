# SSBR-007 DSC 热分析解读

```yaml
sample_id: SSBR-007
interpretation_type: dsc
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Table 6, Fig. 11"

thermal_properties:
  tg:
    value: -25.4
    unit: "℃"
    confidence: high
    method: DSC
  tg_dma:
    value: -2.7
    unit: "℃"
    confidence: high
    method: DMA
  
  heat_capacity:
    delta_cp:
      value: 0.26
      unit: "J/(g·K)"
      confidence: high

  thermal_stability:
    decomposition_onset:
      value: null
      unit: "℃"
      confidence: null
```

## 样本基本信息

- **样本编号**: SSBR-007（文献中标记为 M2）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 4.2 wt%
- **功能基团**: -COOH（羧基）
- **填料体系**: 白炭黑 (50 phr)
- **文献来源**: Qu et al., RSC Advances, 2014

## 热学性能数据

### 玻璃化转变温度 (Tg)

| 测试方法 | Tg 数值 | 单位 | 置信度 |
|----------|---------|------|--------|
| DSC | -25.4 | ℃ | 高 |
| DMA | -2.7 | ℃ | 高 |

### 热容变化 (ΔCp)

| 指标 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| ΔCp | 0.26 | J/(g·K) | 高 |

## 性能解读

### Tg 变化趋势

系列样品 Tg 对比：

| 样品 | 官能化 | Tg-DSC | Tg-DMA | ΔCp |
|------|--------|--------|--------|-----|
| M0 | 0 | -27.2℃ | -5.9℃ | 0.23 |
| M1 | 2.4% | -26.7℃ | -3.9℃ | 0.24 |
| M2 | 4.2% | -25.4℃ | -2.7℃ | 0.26 |

**趋势分析**：
- DSC Tg: 随官能化含量增加逐步升高（-27.2 → -25.4℃）
- DMA Tg: 随官能化含量增加逐步升高（-5.9 → -2.7℃）
- ΔCp: 随官能化含量增加逐步增大（0.23 → 0.26）

### ΔCp 增加的意义

ΔCp 从 0.23 增至 0.26 J/(g·K)（+13%），表明：
- 分散性改善释放了更多被束缚的橡胶链
- 参与玻璃化转变的聚合物比例增加
- 与 tan δmax 提升（1.07 → 1.19）一致

### 文献机理解释

根据文献讨论：
> "This means that less polymer chains are occluded in the filler agglomerates and more can be engaged in Tg transition, which leads to a higher tan δmax."

（这意味着更少的聚合物链被包埋在填料团聚体中，更多链段可以参与 Tg 转变，从而导致更高的 tan δmax）

### 对轮胎性能的影响

| 性能指标 | 影响 | 说明 |
|----------|------|------|
| 湿抓地力 | 提升 | DMA Tg 升高 3.2℃ |
| 能量耗散 | 提升 | tan δmax 增加 11% |
| 低温性能 | 轻微影响 | DSC Tg 升高 1.8℃ |

## 数据来源与置信度说明

- Tg-DSC 数据来自 Table 6 (T-c 列)
- Tg-DMA 数据来自 Table 6
- ΔCp 数据来自 Table 7
- 置信度"高"表示直接从表格读取
