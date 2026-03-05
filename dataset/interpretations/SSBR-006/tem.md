# SSBR-006 TEM 形貌解读

```yaml
sample_id: SSBR-006
interpretation_type: tem
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c4ra09492a"
source_figure: "Fig. 8"

morphology:
  filler_dispersion:
    quality: "中等"
    uniformity: "中等"
    confidence: high
  
  aggregate_size:
    average: null
    unit: "nm"
    confidence: null
    note: "分散状态有所改善"
  
  filler_network:
    formation: "部分填料-橡胶-填料网络"
    connectivity: "中等"
    stability: "中等"
    confidence: high
  
  interface:
    quality: "较好"
    bound_rubber: "增加"
    confidence: medium

qualitative_assessment:
  dispersion_score: 5
  scale: "1-10"
  description: "分散性有所改善，团聚体尺寸减小"
```

## 样本基本信息

- **样本编号**: SSBR-006（文献中标记为 M1/Silica）
- **官能团类型**: 3-巯基丙酸（MPA）官能化 SSBR
- **官能化含量**: 2.4 wt%
- **功能基团**: -COOH（羧基）
- **填料体系**: 白炭黑 (50 phr) + TESPT (4 phr)
- **文献来源**: Qu et al., RSC Advances, 2014

## TEM 形貌观察

### 分散性评估

| 评价指标 | 评级 | 说明 |
|----------|------|------|
| 整体分散质量 | 中等 | 较空白样改善 |
| 分散均匀性 | 中等 | 仍存在不均匀区域 |
| 团聚程度 | 中等 | 团聚体尺寸减小 |
| 分散评分 | 5/10 | 较空白样提升 |

### 填料网络结构

| 参数 | 观察结果 | 置信度 |
|------|----------|--------|
| 网络类型 | 部分填料-橡胶-填料 | 高 |
| 网络连通性 | 中等 | 高 |
| 网络稳定性 | 中等 | 高 |
| 界面结合 | 较好 | 中 |

## 形貌解读

### 文献原文描述

根据文献 Fig. 8 的描述：
> "When 2.4 wt mol% modification agent is grafted on S-SBR, the dispersion state of silica is somewhat improved."

（当 2.4 wt% 的改性剂接枝到 S-SBR 上时，白炭黑的分散状态有所改善）

### 与空白样对比

| 对比项 | SSBR-005 (M0) | SSBR-006 (M1) | 变化 |
|--------|---------------|---------------|------|
| 分散评分 | 3/10 | 5/10 | +67% |
| 团聚程度 | 严重 | 中等 | 改善 |
| 网络类型 | 填料-填料 | 部分填料-橡胶-填料 | 改善 |
| 活化能 | 11.3 kJ/mol | 12.8 kJ/mol | +13% |

### 分散改善机理

2.4 wt% 羧基官能化改善分散的原因：

1. **表面能匹配改善**:
   - 极性部分从 0.9 提升至 1.2 mJ/m²
   - 与白炭黑表面能差异减小

2. **氢键作用**:
   - -COOH 与 Si-OH 形成氢键
   - 增强填料-橡胶界面结合

3. **热力学驱动力降低**:
   - ΔW 从 13.0 降至 11.8 mJ/m²
   - 填料絮凝倾向降低

4. **絮凝速率常数降低**:
   - ka 从 3.98×10⁻³ 降至 3.56×10⁻³ s⁻¹
   - 填料团聚速度减慢

### 性能关联

TEM 形貌改善与性能变化的关联：

| 形貌变化 | 性能影响 |
|----------|----------|
| 团聚体减小 | Payne 效应降低 |
| 网络稳定性提升 | 活化能增加 |
| 被束缚橡胶减少 | tan δmax 提升 |

## 数据来源与置信度说明

- 形貌观察来自 Fig. 8
- 表面能数据来自 Table 3, 4
- 分散评分为相对定性评估
