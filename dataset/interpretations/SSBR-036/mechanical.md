---
sample_id: SSBR-036
test_type: mechanical
data_source: L2
doi: 10.1016/j.compositesb.2020.108301
figures:
- id: Fig.11
  type: tan_delta
  description: 损耗因子温度扫描
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  stress_strain:
    x_axis:
      label: 应变
      unit: '%'
    y_axis:
      label: 应力
      unit: MPa
    data_points:
      - { x: 0, y: 0, confidence: 0.95, source: "L1 origin" }
      - { x: 50, y: 1.5, confidence: 0.65, source: "L3 estimated" }
      - { x: 100, y: 3.2, confidence: 0.65, source: "L3 estimated" }
      - { x: 150, y: 4.8, confidence: 0.65, source: "L3 estimated" }
      - { x: 200, y: 6.2, confidence: 0.65, source: "L3 estimated" }
      - { x: 250, y: 7.5, confidence: 0.65, source: "L3 estimated" }
      - { x: 275, y: 8.0, confidence: 0.65, source: "L3 estimated" }
      - { x: 300, y: 8.5, confidence: 0.95, source: "L1 Table" }
      - { x: 350, y: 11.0, confidence: 0.65, source: "L3 estimated" }
      - { x: 400, y: 18.0, confidence: 0.95, source: "L1 Table break" }
    curve_features:
      modulus_100:
        value: 3.2
        unit: MPa
        source: L3 estimated
        confidence: 0.65
      modulus_300:
        value: 8.5
        unit: MPa
        source: Table
        confidence: 0.95
      tensile_strength:
        value: 18
        unit: MPa
        source: Table
        confidence: 0.95
      elongation_at_break:
        value: 400
        unit: '%'
        source: Table
        confidence: 0.95
    validation:
      known_points:
        - { x: 300, y: 8.5, reference: "M300 from Table", deviation_percent: 0 }
        - { x: 400, y: 18, reference: "tensile strength", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 10
      x_range: [0, 400]
      y_range: [0, 18]
      avg_confidence: 0.76
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: "-"
    data_points:
      - { x: -60, y: 0.05, confidence: 0.60, source: "L3 estimated" }
      - { x: -50, y: 0.10, confidence: 0.60, source: "L3 estimated" }
      - { x: -40, y: 0.25, confidence: 0.60, source: "L3 estimated" }
      - { x: -35, y: 0.45, confidence: 0.65, source: "L3 estimated" }
      - { x: -30, y: 0.65, confidence: 0.65, source: "L3 estimated" }
      - { x: -26, y: 0.72, confidence: 0.85, source: "L2 Tg peak" }
      - { x: -20, y: 0.55, confidence: 0.65, source: "L3 estimated" }
      - { x: -10, y: 0.42, confidence: 0.65, source: "L3 estimated" }
      - { x: 0, y: 0.40, confidence: 0.85, source: "L2 Table" }
      - { x: 10, y: 0.32, confidence: 0.65, source: "L3 estimated" }
      - { x: 20, y: 0.22, confidence: 0.65, source: "L3 estimated" }
      - { x: 30, y: 0.15, confidence: 0.65, source: "L3 estimated" }
      - { x: 40, y: 0.12, confidence: 0.65, source: "L3 estimated" }
      - { x: 50, y: 0.09, confidence: 0.65, source: "L3 estimated" }
      - { x: 60, y: 0.08, confidence: 0.85, source: "L2 Table" }
      - { x: 70, y: 0.07, confidence: 0.60, source: "L3 estimated" }
      - { x: 80, y: 0.065, confidence: 0.60, source: "L3 estimated" }
    curve_features:
      tan_delta_peak:
        value: 0.72
        temperature: -26
        unit: "-"
        source: L2 estimated from Table
        confidence: 0.85
      tan_delta_0C:
        value: 0.40
        unit: "-"
        source: Table
        confidence: 0.85
      tan_delta_60C:
        value: 0.08
        unit: "-"
        source: Table
        confidence: 0.85
      Tg:
        value: -26
        unit: °C
        source: Table tan δ peak
        confidence: 0.85
    validation:
      known_points:
        - { x: 0, y: 0.40, reference: "tan δ @ 0°C", deviation_percent: 0 }
        - { x: 60, y: 0.08, reference: "tan δ @ 60°C", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 17
      x_range: [-60, 80]
      y_range: [0.065, 0.72]
      avg_confidence: 0.68
---
# SSBR-036 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

| 参数 | 数值 |
|------|------|
| 样本编号 | SSBR-036 |
| SSBR型号 | Buna VSL 5025-2HM |
| 苯乙烯含量 | 25.0 wt% |
| 乙烯基含量 | 50.0 mol% |
| 填料体系 | SiO₂ + BEP 界面改性 |
| 官能化试剂 | 双环氧丙基多硫化物 (BEP) |
| 核心官能团 | 环氧基 |

## 研究背景

本研究开发了一种无 VOC（挥发性有机化合物）的硅烷偶联剂替代物——双环氧丙基多硫化物（BEP），用于改善 SiO₂ 填充 SSBR 复合材料的界面结合。

## 动态力学分析（Fig.11）

### 损耗因子温度扫描

| 参数 | 对照 (Si-69) | BEP 处理 | 变化 |
|------|--------------|----------|------|
| tan δ @ 0°C | ~0.35 | ~0.40 | ↑ 湿抓地力 |
| tan δ @ 60°C | ~0.12 | ~0.08 | ↓ 滚动阻力 |
| Tg (tan δ peak) | -28°C | -26°C | 略↑ |

### 关键发现

1. **VOC-Free 优势**
   - BEP 不释放乙醇等挥发性副产物
   - 环保合规性更好
   - 混炼过程更安全

2. **界面改性机制**
   - 环氧基与 SiO₂ 表面硅羟基反应
   - 多硫键参与橡胶硫化交联
   - 形成共价键连接填料与橡胶

3. **性能改善**
   - 显著降低 60°C tan δ（滚动阻力↓ ~33%）
   - 维持或略提高湿抓地力
   - 力学性能无显著损失

## 静态力学性能

| 性能指标 | Si-69 对照 | BEP 处理 |
|----------|------------|----------|
| 拉伸强度 (MPa) | ~17 | ~18 |
| 断裂伸长率 (%) | ~420 | ~400 |
| 300%定伸应力 (MPa) | ~7.5 | ~8.5 |
| 硬度 (Shore A) | ~65 | ~67 |

## 结论

SSBR-036 采用 BEP 作为无 VOC 界面改性剂：
- 成功替代传统硅烷偶联剂
- 显著改善滚动阻力性能
- 满足环保法规要求
- 为绿色轮胎提供可持续解决方案
