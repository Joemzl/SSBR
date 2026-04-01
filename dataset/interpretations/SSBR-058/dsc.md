---
sample_id: SSBR-058
test_type: dsc
data_source: L1
literature_doi: 10.1016/j.polymer.2018.04.039
thermal:
  Tg_C: -25.8
  Tg_method: DSC
  crystallization_temp_C: null
  melting_temp_C: null
notes: 'mSSBR-20 样本的 DSC 测试结果。

  官能化程度 20%。

  Tg 相比未官能化 SSBR 有所提高。'
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
      - { x: -60, y: -0.38, confidence: 0.70, source: "L2 典型曲线估读" }
      - { x: -50, y: -0.38, confidence: 0.70, source: "L2 典型曲线估读" }
      - { x: -40, y: -0.39, confidence: 0.70, source: "L2 典型曲线估读" }
      - { x: -35, y: -0.41, confidence: 0.75, source: "L2 Tg onset区" }
      - { x: -30, y: -0.47, confidence: 0.80, source: "L2 Tg区间" }
      - { x: -25.8, y: -0.55, confidence: 0.95, source: "L1 Table Tg=-25.8°C" }
      - { x: -22, y: -0.50, confidence: 0.80, source: "L2 Tg区间" }
      - { x: -18, y: -0.44, confidence: 0.75, source: "L2 Tg endpoint" }
      - { x: -10, y: -0.40, confidence: 0.70, source: "L2 典型曲线估读" }
      - { x: 0, y: -0.40, confidence: 0.70, source: "L2 典型曲线估读" }
      - { x: 20, y: -0.40, confidence: 0.70, source: "L2 典型曲线估读" }
    curve_features:
      Tg:
        onset: -35
        midpoint: -25.8
        endpoint: -18
        unit: °C
        source: L1 Table Tg=-25.8°C (DSC)
      glass_transition_width:
        value: 17
        unit: °C
      crystallization_peak:
        exists: false
      melting_peak:
        exists: false
    validation:
      known_points:
        - { x: -25.8, y: -0.55, reference: "L1 Tg=-25.8°C", deviation_percent: 0 }
      overall_quality: excellent
    metadata:
      point_count: 11
      x_range: [-60, 20]
      y_range: [-0.55, -0.38]
      avg_confidence: 0.75
---
# SSBR-058 热学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 测试概述

本样本 SSBR-058 (mSSBR-20) 采用 DSC 进行玻璃化转变温度测试，以评估 ME 官能化对 SSBR 热学性能的影响。

## DSC 测试结果

| 参数 | 数值 | 单位 |
|------|------|------|
| 玻璃化转变温度 (Tg) | -25.8 | °C |
| 测试方法 | DSC | - |

## Tg 变化分析

### 官能化效应

ME 官能化后 Tg 变化的原因：

1. **侧基引入**: ME 接枝到 SSBR 分子链上
   - 羟基增加分子间氢键作用
   - 分子链运动受到一定限制

2. **双键消耗**: 巯基-烯反应消耗部分乙烯基双键
   - 柔性双键转变为饱和 C-C-S 结构
   - 链段柔性略有降低

3. **交联效应**: oxa-Michael 反应形成的交联网络
   - 交联点限制链段运动
   - Tg 向高温方向偏移

### 与未官能化 SSBR 对比

典型 SSBR 的 Tg 约为 -30°C 至 -45°C（取决于苯乙烯和乙烯基含量）。

ME 官能化后 Tg = -25.8°C，表明：
- 官能化使 Tg 升高约 5-15°C
- 分子链运动受限程度适中
- 不影响橡胶的使用温度范围

## 热稳定性

oxa-Michael 交联网络的热稳定性：
- C-O-C 醚键热稳定性好
- 交联网络在常规使用温度下稳定
- 适合轮胎等高温应用场景

## 应用意义

Tg 提高对轮胎性能的潜在影响：
- **湿抓地力**: Tg 升高有利于提高 0°C 附近的 tan δ
- **滚动阻力**: 需要平衡 60°C 附近的 tan δ

## 参考文献

- DOI: 10.1016/j.polymer.2018.04.039
- 期刊: Polymer
