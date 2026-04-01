---
sample_id: SSBR-051
test_type: mechanical
data_source: L2
doi: 10.1016/j.polymer.2010.03.006
figures:
- id: Fig.5
  type: tan_delta
  description: 损耗因子温度扫描
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  dma_tan_delta:
    x_axis:
      label: 温度
      unit: °C
    y_axis:
      label: tan δ
      unit: dimensionless
    data_points:
      - { x: -80, y: 0.03, confidence: 0.70, source: "L2 Fig.5 估读 (TBCSi-SSBR)" }
      - { x: -60, y: 0.06, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: -50, y: 0.12, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: -40, y: 0.30, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: -35, y: 0.55, confidence: 0.75, source: "L2 Fig.5 估读" }
      - { x: -30, y: 0.78, confidence: 0.75, source: "L2 Fig.5 估读" }
      - { x: -25, y: 0.90, confidence: 0.80, source: "L2 Fig.5 peak ~0.9" }
      - { x: -20, y: 0.82, confidence: 0.75, source: "L2 Fig.5 估读" }
      - { x: -15, y: 0.60, confidence: 0.75, source: "L2 Fig.5 估读" }
      - { x: -10, y: 0.40, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: 0, y: 0.22, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: 10, y: 0.15, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: 20, y: 0.12, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: 30, y: 0.10, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: 40, y: 0.09, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: 50, y: 0.08, confidence: 0.70, source: "L2 Fig.5 估读" }
      - { x: 60, y: 0.07, confidence: 0.70, source: "L2 Fig.5 估读" }
    curve_features:
      Tg_tan_delta_peak:
        value: -25
        unit: °C
        source: Fig.5 TBCSi-SSBR peak
        confidence: 0.80
      tan_delta_max:
        value: 0.90
        unit: dimensionless
        source: Fig.5 ~0.9 (比对照~1.2低)
        confidence: 0.80
      tan_delta_0C:
        value: 0.22
        unit: dimensionless
        source: L3 estimated from Fig.5
        confidence: 0.70
      tan_delta_60C:
        value: 0.07
        unit: dimensionless
        source: L3 estimated from Fig.5
        confidence: 0.70
      Tg:
        value: -25
        unit: °C
        method: tan_delta_peak
        source: Fig.5
        confidence: 0.80
      peak_broadening:
        description: TBCSi官能化导致峰变宽
        source: Fig.5
    validation:
      known_points:
        - { x: -25, y: 0.90, reference: "tan δ max ~0.9", deviation_percent: 0 }
      overall_quality: good
    metadata:
      point_count: 17
      x_range: [-80, 60]
      y_range: [0.03, 0.90]
      avg_confidence: 0.72
---
# SSBR-051 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## 样本信息

| 参数 | 数值 |
|------|------|
| 样本编号 | SSBR-051 |
| 官能化试剂 | 叔丁基氯二苯基硅烷 (TBCSi) |
| 核心官能团 | 硅基 |
| 填料体系 | 炭黑填充 |
| 应用场景 | 炭黑填充 SSBR 复合材料 |

## 研究背景

本研究探索链端大体积官能团对 SSBR 结构与性能的影响，使用叔丁基氯二苯基硅烷 (TBCSi) 作为官能化试剂，引入大体积硅基末端基团。

## 动态力学分析（Fig.5）

### 损耗因子温度扫描

| 参数 | 对照 SSBR | TBCSi-SSBR |
|------|-----------|------------|
| Tg (tan δ peak) | 基准 | 略↑ |
| tan δ max | ~1.2 | ~0.9 |
| 峰宽 | 窄 | 宽 |

### 关键发现

1. **大体积基团效应**
   - TBCSi 引入大体积硅基末端
   - 限制链端运动自由度
   - 影响分子链松弛行为

2. **炭黑相互作用**
   - 硅基团与炭黑表面相互作用
   - 可能增强橡胶-炭黑界面
   - tan δ 峰值降低表明界面改善

3. **温度依赖性**
   - Tg 区域损耗峰变宽
   - 表明链段运动受限范围增大
   - 界面层厚度增加

## 静态力学性能

| 性能指标 | 对照 SSBR | TBCSi-SSBR |
|----------|-----------|------------|
| 拉伸强度 | 基准 | 略↑ |
| 断裂伸长率 | 基准 | 略↓ |
| 模量 | 基准 | ↑ |

## 结论

SSBR-051 通过链端大体积硅基官能化：
- 影响分子链动力学行为
- 改善与炭黑的界面相互作用
- 为链端官能化设计提供参考
