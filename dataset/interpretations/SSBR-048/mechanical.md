---
sample_id: SSBR-048
test_type: mechanical
data_source_level: L2
literature_doi: 10.1002/app.40348
skill_version: '2.0'
updated_at: '2026-03-31'
curves:
  payne_effect:
    x_axis:
      label: 应变
      unit: '%'
    y_axis:
      label: 储能模量
      unit: MPa
    data_points:
      - { x: 0.1, y: 2.0, confidence: 0.70, source: "L2 Fig.4 估读" }
      - { x: 0.2, y: 1.95, confidence: 0.70, source: "L2 Fig.4 估读" }
      - { x: 0.5, y: 1.85, confidence: 0.70, source: "L2 Fig.4 估读" }
      - { x: 1.0, y: 1.70, confidence: 0.70, source: "L2 Fig.4 估读" }
      - { x: 2.0, y: 1.50, confidence: 0.70, source: "L2 Fig.4 估读" }
      - { x: 5.0, y: 1.15, confidence: 0.70, source: "L2 Fig.4 估读" }
      - { x: 10.0, y: 0.85, confidence: 0.70, source: "L2 Fig.4 估读" }
      - { x: 20.0, y: 0.65, confidence: 0.70, source: "L2 Fig.4 估读" }
      - { x: 50.0, y: 0.50, confidence: 0.70, source: "L2 Fig.4 估读" }
      - { x: 100.0, y: 0.50, confidence: 0.70, source: "L2 Fig.4 估读" }
    curve_features:
      G_prime_low_strain:
        value: 2.0
        unit: MPa
        source: Fig.4 估读
        confidence: 0.70
      G_prime_high_strain:
        value: 0.50
        unit: MPa
        source: Fig.4 估读
        confidence: 0.70
      delta_G_prime:
        value: 1.5
        unit: MPa
        source: 计算值
        confidence: 0.70
      tan_delta_max:
        value: 0.18
        unit: dimensionless
        source: Fig.4 估读
        confidence: 0.70
    validation:
      known_points:
        - { x: 0.1, y: 2.0, reference: "G'低应变 ~2.0 MPa", deviation_percent: 0 }
        - { x: 100.0, y: 0.50, reference: "G'高应变 ~0.5 MPa", deviation_percent: 0 }
      overall_quality: acceptable
    metadata:
      point_count: 10
      x_range: [0.1, 100.0]
      y_range: [0.50, 2.0]
      avg_confidence: 0.70
---
# SSBR-048 力学性能解读


> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。

## Payne 效应

| 指标 | 数值 | 数据来源 |
|------|------|----------|
| G'(低应变) | ~2.0 MPa | Fig. 4 估读 |
| G'(高应变) | ~0.5 MPa | Fig. 4 估读 |
| ΔG' | ~1.5 MPa | 计算值 |
| tan δ (最大值) | ~0.18 | Fig. 4 估读 |

## 性能分析

SSBR-048 研究了星形结构、含氨基官能团的 N-SSBR 与白炭黑/炭黑复合填料体系的动态性能。

### 星形结构特点

| 参数 | 数值 | 意义 |
|------|------|------|
| 苯乙烯含量 | 29.5 wt% | 较高 |
| 乙烯基含量 | 34.7 mol% | 中等 |
| Mn | 351,000 | 高分子量 |

### 动态性能特点

1. **Payne 效应**: ΔG' ~1.5 MPa，氨基官能化有效改善分散
2. **tan δ 行为**: 动态应变扫描显示良好的能量耗散特性
3. **填料网络**: 氨基与白炭黑的相互作用减少了填料-填料团聚

### 氨基官能化作用

氨基官能团 (来自 [3-(2-氨基乙基)氨基丙基]三甲氧基硅烷) 的作用：
- 与白炭黑表面硅烷醇形成氢键
- 提高橡胶-填料相互作用
- 改善复合填料体系的分散性

## 复合填料体系

白炭黑/炭黑复合填料：
- 结合白炭黑的低滚动阻力优势
- 结合炭黑的高强度和耐磨优势
- 氨基官能化改善整体分散
