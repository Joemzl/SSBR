---
sample_id: SSBR-075
test_type: thermal
data_source: L3
doi: 10.3390/polym12010209
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
    data_points:
      - x: -80
        y: -0.32
        confidence: 0.50
        source: L3
      - x: -65
        y: -0.30
        confidence: 0.50
        source: L3
      - x: -50
        y: -0.27
        confidence: 0.50
        source: L3
      - x: -40
        y: -0.22
        confidence: 0.55
        source: L3
        note: Tg onset
      - x: -32
        y: -0.08
        confidence: 0.55
        source: L3
        note: Tg midpoint
      - x: -24
        y: 0.06
        confidence: 0.55
        source: L3
        note: Tg endpoint
      - x: -10
        y: 0.08
        confidence: 0.50
        source: L3
      - x: 10
        y: 0.06
        confidence: 0.50
        source: L3
      - x: 40
        y: 0.04
        confidence: 0.50
        source: L3
      - x: 80
        y: 0.02
        confidence: 0.50
        source: L3
    curve_features:
      Tg:
        onset: -40
        midpoint: -32
        endpoint: -24
        unit: °C
        source: L3
      glass_transition_width:
        value: 16
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points: []
      overall_quality: poor
      note: 文献未报道DSC数据，基于标准SSBR体系估算
    metadata:
      point_count: 10
      x_range:
        - -80
        - 80
      y_range:
        - -0.32
        - 0.08
      avg_confidence: 0.52
---
# SSBR-075 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

- **样本编号**: SSBR-075
- **高分子类型**: 轮胎胎面胶硅烷化研究用 SSBR
- **官能化类型**: TESPT 硅烷偶联剂
- **文献 DOI**: 10.3390/polym12010209

## DSC 测试数据

| 参数 | 数值 | 数据来源 |
|------|------|----------|
| Tg | 文献未明确报道 | L3 |

## 性能解读

### 硅烷化对热学性能的影响

- TESPT 主要影响填料分散和界面结合
- 对 Tg 的直接影响较小
- 可能影响 tan δ 峰强度

## 数据质量说明

- 文献未报道 DSC 测试数据
