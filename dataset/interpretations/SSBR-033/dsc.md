---
sample_id: SSBR-033
test_type: thermal
data_source: L3
doi: 10.3389/fchem.2018.00240
figure_ref: N/A
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  dsc_heat_flow:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: 热流
      unit: mW/mg
      direction: exo_up
    data_points: []
    curve_features:
      Tg:
        onset: null
        midpoint: null
        endpoint: null
        unit: °C
        source: "文献未报道DSC数据"
      glass_transition_width:
        value: null
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: poor
      quality_note: "文献 10.3389/fchem.2018.00240 未报道 DSC 热分析数据"
    metadata:
      point_count: 0
      x_range: [-80, 100]
      y_range: [-1, 1]
      avg_confidence: 0
---
# SSBR-033 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

- **样本编号**: SSBR-033
- **高分子类型**: 高性能轮胎、节能环保轮胎用 SSBR
- **官能化类型**: NDI (1,5-萘二异氰酸酯) 官能化
- **文献 DOI**: 10.3389/fchem.2018.00240

## DSC 测试数据

### 玻璃化转变温度

| 参数 | 数值 | 数据来源 |
|------|------|----------|
| Tg | 文献未明确报道 | L3 |

## 性能解读

### NDI 官能化对热学性能的影响

1. **Tg 变化**: NDI 官能化可能略微提高 Tg
2. **萘环效应**: 刚性萘环可能增加链段刚性
3. **交联效应**: 交联密度增加可能影响热转变

## 数据质量说明

- 文献未报道 DSC 测试数据
- 热学性能推测基于官能化类型 (L3)
