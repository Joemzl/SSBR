# 曲线数据 JSON Schema 规范

**Version**: 1.0.0 | **Date**: 2026-03-31

---

## 概述

本文档定义了全范围曲线数据在 YAML front matter 中的存储格式和验证规则。

---

## 1. 通用曲线数据结构

### 1.1 基础字段定义

```yaml
curves:
  <curve_type>:                    # 曲线类型标识符
    x_axis:
      label: string                # X 轴标签
      unit: string                 # X 轴单位
    y_axis:
      label: string                # Y 轴标签
      unit: string                 # Y 轴单位
    data_points:                   # 数据点数组
      - x: number                  # X 值
        y: number                  # Y 值
        confidence: number         # 置信度 (0.0-1.0)
        source: string             # 数据来源 (L1/L2/L3)
    curve_features:                # 曲线特征（可选）
      <feature_name>: <value>
    metadata:
      point_count: integer         # 数据点总数
      x_range: [number, number]    # X 轴范围
      y_range: [number, number]    # Y 轴范围
      avg_confidence: number       # 平均置信度
```

### 1.2 数据来源标识

| 代码 | 含义 | 置信度建议 |
|------|------|-----------|
| `L1` | 文献表格/正文数值 | 0.95 |
| `L2` | 图面标注数字 | 0.85 |
| `L3` | 曲线视觉估读 | 0.60-0.75 |

---

## 2. 应力-应变曲线 Schema

### 2.1 完整定义

```yaml
curves:
  stress_strain:
    x_axis:
      label: "应变"
      unit: "%"
    y_axis:
      label: "应力"
      unit: "MPa"
    data_points:
      - x: 0
        y: 0
        confidence: 1.0
        source: "L1"
      - x: 50
        y: 1.2
        confidence: 0.70
        source: "L3"
      # ... 更多数据点
    curve_features:
      modulus_100:                 # 100% 定伸应力
        value: number
        unit: "MPa"
        source: string
      modulus_200:                 # 200% 定伸应力（可选）
        value: number
        unit: "MPa"
        source: string
      modulus_300:                 # 300% 定伸应力
        value: number
        unit: "MPa"
        source: string
      tensile_strength:            # 拉伸强度
        value: number
        unit: "MPa"
        source: string
      elongation_at_break:         # 断裂伸长率
        value: number
        unit: "%"
        source: string
      yield_point:                 # 屈服点（如果存在）
        strain: number
        stress: number
        exists: boolean
      strain_hardening_index:      # 应变硬化指数（计算值）
        value: number
        confidence: number
    validation:
      known_points:                # 用于交叉验证的已知点
        - strain: 100
          stress_expected: 2.5
          stress_measured: 2.6
          deviation_percent: 4.0
      overall_quality: string      # "good" / "acceptable" / "poor"
    metadata:
      point_count: 15
      x_range: [0, 450]
      y_range: [0, 18]
      avg_confidence: 0.72
```

### 2.2 必填字段

- `data_points`: 至少 10 个点
- `curve_features.modulus_100`
- `curve_features.tensile_strength`
- `curve_features.elongation_at_break`

### 2.3 推荐数据点间隔

| 应变范围 | 推荐间隔 | 最小点数 |
|----------|----------|----------|
| 0-100% | 20% | 6 |
| 100-300% | 50% | 5 |
| >300% | 100% | 2+ |

---

## 3. DMA tan δ-温度曲线 Schema

### 3.1 完整定义

```yaml
curves:
  dma_tan_delta:
    x_axis:
      label: "温度"
      unit: "°C"
    y_axis:
      label: "tan δ"
      unit: "无量纲"
    data_points:
      - x: -60
        y: 0.05
        confidence: 0.70
        source: "L3"
      - x: -40
        y: 0.45
        confidence: 0.70
        source: "L3"
      # ... 更多数据点
    curve_features:
      tan_delta_0C:                # 0℃ tan δ（湿地抓地力指标）
        value: number
        confidence: number
        source: string
      tan_delta_60C:               # 60℃ tan δ（滚动阻力指标）
        value: number
        confidence: number
        source: string
      tan_delta_max:               # tan δ 峰值
        value: number
        temperature: number        # 峰值对应温度
        confidence: number
        source: string
      Tg:                          # 玻璃化转变温度
        value: number
        unit: "°C"
        method: string             # "peak" / "onset" / "midpoint"
        source: string
      peak_width:                  # 峰半高宽
        value: number
        unit: "°C"
        confidence: number
      wet_grip_index:              # 湿地抓地力指数（计算值）
        value: number
        formula: "tan δ(0°C)"
      rolling_resistance_index:    # 滚动阻力指数（计算值）
        value: number
        formula: "tan δ(60°C)"
    validation:
      known_points:
        - temperature: 0
          tan_delta_expected: 0.52
          tan_delta_measured: 0.54
          deviation_percent: 3.8
    metadata:
      point_count: 17
      x_range: [-80, 80]
      y_range: [0, 0.8]
      avg_confidence: 0.71
```

### 3.2 必填字段

- `data_points`: 至少 12 个点
- `curve_features.tan_delta_0C`
- `curve_features.tan_delta_60C`
- `curve_features.Tg`

### 3.3 推荐数据点间隔

| 温度范围 | 推荐间隔 | 最小点数 |
|----------|----------|----------|
| -80°C ~ -40°C | 20°C | 3 |
| -40°C ~ 0°C | 10°C | 5 |
| 0°C ~ 40°C | 10°C | 5 |
| 40°C ~ 80°C | 20°C | 3 |

---

## 4. Payne 效应 G'-应变曲线 Schema

### 4.1 完整定义

```yaml
curves:
  payne_storage_modulus:
    x_axis:
      label: "应变"
      unit: "%"
      scale: "logarithmic"         # 对数坐标
    y_axis:
      label: "储能模量 G'"
      unit: "MPa"
    data_points:
      - x: 0.1
        y: 2.8
        confidence: 0.70
        source: "L3"
      - x: 0.5
        y: 2.6
        confidence: 0.70
        source: "L3"
      # ... 更多数据点（按对数间隔）
    curve_features:
      G_prime_0:                   # 初始模量（低应变极限）
        value: number
        unit: "MPa"
        strain_at: number          # 测量应变（通常 0.1%）
        source: string
      G_prime_inf:                 # 最终模量（高应变极限）
        value: number
        unit: "MPa"
        strain_at: number          # 测量应变（通常 100%）
        source: string
      delta_G_prime:               # 模量差
        value: number
        unit: "MPa"
        calculation: "G'₀ - G'∞"
      gamma_c:                     # 临界应变
        value: number
        unit: "%"
        definition: "G' 下降 50% 对应的应变"
        confidence: number
      filler_network_strength:     # 填料网络强度指数（计算值）
        value: number
        formula: "ΔG'/G'₀"
      multi_stage_network:         # 多级网络检测
        detected: boolean
        stages: integer
        transition_strains: [number]
    validation:
      known_points:
        - strain: 0.1
          G_expected: 2.85
          G_measured: 2.80
          deviation_percent: 1.8
    metadata:
      point_count: 12
      x_range: [0.1, 100]
      y_range: [0.8, 3.0]
      avg_confidence: 0.70
```

### 4.2 必填字段

- `data_points`: 至少 8 个点
- `curve_features.G_prime_0`
- `curve_features.G_prime_inf`
- `curve_features.delta_G_prime`

### 4.3 推荐数据点（对数间隔）

标准采样点：`0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100` (%)

---

## 5. DSC 热流曲线 Schema

### 5.1 完整定义

```yaml
curves:
  dsc_heat_flow:
    x_axis:
      label: "温度"
      unit: "°C"
    y_axis:
      label: "热流"
      unit: "mW/mg"
      direction: "exo_up"          # 放热方向向上
    data_points:
      - x: -80
        y: -0.5
        confidence: 0.65
        source: "L3"
      # ... 更多数据点
    curve_features:
      Tg:                          # 玻璃化转变温度
        onset: number              # 起始温度
        midpoint: number           # 中点温度
        endpoint: number           # 终止温度
        unit: "°C"
        source: string
      glass_transition_width:      # 玻璃化转变宽度
        value: number
        unit: "°C"
        calculation: "T_endpoint - T_onset"
      baseline_shift:              # 基线偏移（定性）
        magnitude: string          # "small" / "medium" / "large"
        direction: string          # "endothermic" / "exothermic"
      crystallization_peak:        # 冷结晶峰（如果存在）
        exists: boolean
        temperature: number
        confidence: number
      melting_peak:                # 熔融峰（如果存在）
        exists: boolean
        temperature: number
        confidence: number
    validation:
      known_points:
        - feature: "Tg_midpoint"
          expected: -25
          measured: -24
          deviation: 1
    metadata:
      point_count: 14
      x_range: [-80, 50]
      y_range: [-1.0, 0.5]
      avg_confidence: 0.65
```

### 5.2 必填字段

- `data_points`: 至少 10 个点
- `curve_features.Tg.midpoint`

### 5.3 推荐数据点间隔

| 温度范围 | 推荐间隔 | 备注 |
|----------|----------|------|
| 玻璃化转变前 | 20°C | 基线区 |
| 玻璃化转变区 | 5°C | 高密度采样 |
| 玻璃化转变后 | 20°C | 基线区 |

---

## 6. 验证规则

### 6.1 数据点验证

```python
def validate_data_point(point: dict) -> bool:
    """验证单个数据点"""
    required = ['x', 'y', 'confidence', 'source']
    if not all(k in point for k in required):
        return False
    
    if not 0 <= point['confidence'] <= 1:
        return False
    
    if point['source'] not in ['L1', 'L2', 'L3']:
        return False
    
    return True
```

### 6.2 曲线完整性验证

```python
def validate_curve(curve: dict, min_points: int) -> dict:
    """验证曲线数据完整性"""
    issues = []
    
    # 检查必填字段
    if 'data_points' not in curve:
        issues.append("缺少 data_points")
    elif len(curve['data_points']) < min_points:
        issues.append(f"数据点不足，需要 {min_points}，实际 {len(curve['data_points'])}")
    
    # 检查 X 单调性
    x_values = [p['x'] for p in curve.get('data_points', [])]
    if x_values != sorted(x_values):
        issues.append("X 值不单调递增")
    
    # 计算平均置信度
    confidences = [p['confidence'] for p in curve.get('data_points', [])]
    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'avg_confidence': avg_conf
    }
```

### 6.3 交叉验证规则

```python
def cross_validate(curve: dict) -> dict:
    """交叉验证估读值与已知值"""
    validation = curve.get('validation', {})
    known_points = validation.get('known_points', [])
    
    deviations = []
    for kp in known_points:
        dev = kp.get('deviation_percent', 0)
        deviations.append(dev)
    
    avg_deviation = sum(deviations) / len(deviations) if deviations else 0
    
    # 质量评级
    if avg_deviation < 5:
        quality = "excellent"
    elif avg_deviation < 10:
        quality = "good"
    elif avg_deviation < 15:
        quality = "acceptable"
    else:
        quality = "poor"
    
    return {
        'avg_deviation': avg_deviation,
        'quality': quality,
        'point_count': len(known_points)
    }
```

---

## 7. 数据来源置信度映射

### 7.1 建议置信度值

| 数据来源 | 描述 | 建议置信度 |
|----------|------|-----------|
| L1 - 表格数据 | 文献表格中的精确数值 | 0.95 |
| L1 - 正文数据 | 文献正文中的精确数值 | 0.90 |
| L2 - 图面标注 | 图上明确标注的数字 | 0.85 |
| L3 - 清晰曲线 | 网格清晰、曲线分辨率高 | 0.75 |
| L3 - 一般曲线 | 网格存在、曲线可读 | 0.65 |
| L3 - 模糊曲线 | 网格稀疏、曲线重叠 | 0.50 |

### 7.2 置信度自动调整规则

```yaml
confidence_adjustment:
  # 交叉验证偏差大时降低置信度
  if_deviation_gt_10: -0.10
  if_deviation_gt_20: -0.20
  
  # 多曲线重叠时降低置信度
  if_curve_overlap: -0.15
  
  # 网格稀疏时降低置信度
  if_sparse_grid: -0.10
```

---

## 8. 示例：完整的 YAML 文件

```yaml
---
sample_id: "SSBR-025"
source_doi: "10.1016/j.polymer.2024.xxxxx"

mechanical:
  modulus_100: 2.5
  modulus_300: 8.2
  tensile_strength: 16.8
  elongation_at_break: 420

curves:
  stress_strain:
    x_axis:
      label: "应变"
      unit: "%"
    y_axis:
      label: "应力"
      unit: "MPa"
    data_points:
      - {x: 0, y: 0, confidence: 1.0, source: "L1"}
      - {x: 50, y: 1.2, confidence: 0.70, source: "L3"}
      - {x: 100, y: 2.5, confidence: 0.95, source: "L1"}
      - {x: 150, y: 4.1, confidence: 0.70, source: "L3"}
      - {x: 200, y: 5.8, confidence: 0.70, source: "L3"}
      - {x: 250, y: 7.0, confidence: 0.70, source: "L3"}
      - {x: 300, y: 8.2, confidence: 0.95, source: "L1"}
      - {x: 350, y: 10.5, confidence: 0.65, source: "L3"}
      - {x: 400, y: 14.2, confidence: 0.65, source: "L3"}
      - {x: 420, y: 16.8, confidence: 0.95, source: "L1"}
    curve_features:
      modulus_100:
        value: 2.5
        unit: "MPa"
        source: "L1"
      modulus_300:
        value: 8.2
        unit: "MPa"
        source: "L1"
      tensile_strength:
        value: 16.8
        unit: "MPa"
        source: "L1"
      elongation_at_break:
        value: 420
        unit: "%"
        source: "L1"
    validation:
      known_points:
        - {strain: 100, stress_expected: 2.5, stress_measured: 2.5, deviation_percent: 0}
        - {strain: 300, stress_expected: 8.2, stress_measured: 8.2, deviation_percent: 0}
      overall_quality: "good"
    metadata:
      point_count: 10
      x_range: [0, 420]
      y_range: [0, 16.8]
      avg_confidence: 0.82
---
```

---

## 9. JSON Schema（机器可读）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CurveDataSchema",
  "type": "object",
  "properties": {
    "curves": {
      "type": "object",
      "properties": {
        "stress_strain": { "$ref": "#/definitions/StressStrainCurve" },
        "dma_tan_delta": { "$ref": "#/definitions/DMATanDeltaCurve" },
        "payne_storage_modulus": { "$ref": "#/definitions/PayneCurve" },
        "dsc_heat_flow": { "$ref": "#/definitions/DSCCurve" }
      }
    }
  },
  "definitions": {
    "DataPoint": {
      "type": "object",
      "required": ["x", "y", "confidence", "source"],
      "properties": {
        "x": { "type": "number" },
        "y": { "type": "number" },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
        "source": { "type": "string", "enum": ["L1", "L2", "L3"] }
      }
    },
    "Axis": {
      "type": "object",
      "required": ["label", "unit"],
      "properties": {
        "label": { "type": "string" },
        "unit": { "type": "string" },
        "scale": { "type": "string", "enum": ["linear", "logarithmic"] }
      }
    },
    "StressStrainCurve": {
      "type": "object",
      "required": ["x_axis", "y_axis", "data_points"],
      "properties": {
        "x_axis": { "$ref": "#/definitions/Axis" },
        "y_axis": { "$ref": "#/definitions/Axis" },
        "data_points": {
          "type": "array",
          "items": { "$ref": "#/definitions/DataPoint" },
          "minItems": 10
        }
      }
    }
  }
}
```

---

**本 Schema 规范为全范围数据捕捉提供了标准化的存储格式，确保数据的完整性、可验证性和可追溯性。**
