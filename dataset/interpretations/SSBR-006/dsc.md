# SSBR-006 DSC 热分析解读

```yaml
sample_id: SSBR-006
interpretation_type: dsc
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Table 6, Fig. 11"

thermal_properties:
  tg:
    value: -26.7
    unit: "℃"
    confidence: high
    method: DSC
  tg_dma:
    value: -3.9
    unit: "℃"
    confidence: high
    method: DMA
  
  heat_capacity:
    delta_cp:
      value: 0.24
      unit: "J/(g·K)"
      confidence: high

  thermal_stability:
    decomposition_onset:
      value: null
      unit: "℃"
      confidence: null
```

## 样本基本信息

- **样本编号**: SSBR-006（文献中标记为 M1）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 2.4 wt%
- **功能基团**: -COOH（羧基）
- **填料体系**: 白炭黑 (50 phr)
- **文献来源**: Qu et al., RSC Advances, 2014

## 热学性能数据

### 玻璃化转变温度 (Tg)

| 测试方法 | Tg 数值 | 单位 | 置信度 |
|----------|---------|------|--------|
| DSC | -26.7 | ℃ | 高 |
| DMA | -3.9 | ℃ | 高 |

### 热容变化 (ΔCp)

| 指标 | 数值 | 单位 | 置信度 |
|------|------|------|--------|
| ΔCp | 0.24 | J/(g·K) | 高 |

## 性能解读

### Tg 变化分析

与空白样（SSBR-005）对比：

| 参数 | SSBR-005 | SSBR-006 | 变化 |
|------|----------|----------|------|
| Tg-DSC | -27.2℃ | -26.7℃ | +0.5℃ |
| Tg-DMA | -5.9℃ | -3.9℃ | +2.0℃ |
| ΔCp | 0.23 | 0.24 | +4.3% |

**Tg 变化原因分析**：
1. **DSC Tg 略升高**: 羧基引入增加了分子链刚性
2. **DMA Tg 升高更明显**: 填料-橡胶界面作用增强
3. **ΔCp 增加**: 更多橡胶链段参与玻璃化转变

### ΔCp 增加的物理意义

ΔCp 从 0.23 增至 0.24 J/(g·K)，表明：
- 被填料团聚体束缚的橡胶减少
- 分散性改善释放了部分被包埋的橡胶链
- 更多聚合物链段可自由运动

### 对轮胎性能的影响

| 性能指标 | 影响 | 说明 |
|----------|------|------|
| 湿抓地力 | 轻微提升 | DMA Tg 升高 2℃ |
| 滚动阻力 | 基本不变 | 变化幅度小 |
| 低温性能 | 影响很小 | DSC Tg 变化仅 0.5℃ |

## 数据来源与置信度说明

- Tg-DSC 数据来自 Table 6 (T-c 列)
- Tg-DMA 数据来自 Table 6
- ΔCp 数据来自 Table 7
- 置信度"高"表示直接从表格读取
