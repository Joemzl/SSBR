# SSBR-008 DSC 热分析解读

```yaml
sample_id: SSBR-008
interpretation_type: dsc
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Table 6, Table 7, Fig. 11"

thermal_properties:
  tg:
    value: -23.9
    unit: "℃"
    confidence: high
    method: DSC
  tg_dma:
    value: 0.1
    unit: "℃"
    confidence: high
    method: DMA
  
  heat_capacity:
    delta_cp:
      value: 0.29
      unit: "J/(g·K)"
      confidence: high

  thermal_stability:
    decomposition_onset:
      value: null
      unit: "℃"
      confidence: null
```

## 样本基本信息

- **样本编号**: SSBR-008（文献中标记为 M3）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 9.6 wt%
- **功能基团**: -COOH（羧基）
- **填料体系**: 白炭黑 (50 phr)
- **文献来源**: Qu et al., RSC Advances, 2014

## 热学性能数据

### 玻璃化转变温度 (Tg)

| 测试方法 | Tg 数值 | 单位 | 置信度 |
|----------|---------|------|--------|
| DSC | -23.9 | ℃ | 高 |
| DMA | 0.1 | ℃ | 高 |

### 热容变化 (ΔCp)

| 指标 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| ΔCp | 0.29 | J/(g·K) | 高 |

## 性能解读

### 完整系列 Tg 趋势

| 样品 | 官能化 | Tg-DSC | Tg-DMA | ΔCp | tan δmax |
|------|--------|--------|--------|-----|----------|
| M0 | 0 | -27.2℃ | -5.9℃ | 0.23 | 1.07 |
| M1 | 2.4% | -26.7℃ | -3.9℃ | 0.24 | 1.11 |
| M2 | 4.2% | -25.4℃ | -2.7℃ | 0.26 | 1.19 |
| **M3** | **9.6%** | **-23.9℃** | **0.1℃** | **0.29** | **1.30** |

### Tg 升高的综合分析

**DSC Tg 升高 3.3℃**（-27.2 → -23.9℃）：
- 羧基引入增加了分子链极性
- 分子间相互作用增强
- 链段运动受到更多约束

**DMA Tg 升高 6.0℃**（-5.9 → 0.1℃）：
- 强界面作用限制橡胶链段运动
- 填料-橡胶相互作用最强
- 有效交联密度增加

### ΔCp 增加的物理意义

ΔCp 从 0.23 增至 0.29 J/(g·K)（+26%）：

根据文献讨论：
> "ΔCp, which is related to the fraction of the polymer participating in the glass transition and is proportional to the number of internal degrees of freedom of molecular motion, shows an increasing tendency with the content of polar groups."

这表明：
- 更高比例的聚合物链参与玻璃化转变
- 被填料团聚体束缚的橡胶减少
- 分散性改善释放了更多可动链段

### Tg 与性能的关联

**文献关于 Tg 变化来源的讨论**：
> "It can be observed that the Tg does not exhibit distinct variation after compounding with silica in comparison with that of raw rubber. Therefore, it can be concluded that the Tg shifted from DMA with the modification agent due to the raw rubber rather than the interactions between silica and the M-S-SBR."

即：DMA Tg 的升高主要来自原胶本身的 Tg 变化，而非填料-橡胶相互作用。

### 对轮胎性能的影响

| 性能指标 | 影响 | 说明 |
|----------|------|------|
| 湿抓地力 | 显著提升 | DMA Tg 升高 6℃ |
| 能量耗散（低温）| 最高 | tan δmax = 1.30 |
| 滚动阻力 | 最低 | 高温区 tan δ 最小 |

## 数据来源与置信度说明

- Tg-DSC 数据来自 Table 6 (T-c 列)
- Tg-DMA 数据来自 Table 6
- ΔCp 数据来自 Table 7
- 置信度"高"表示直接从表格读取
