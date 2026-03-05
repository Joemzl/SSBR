# YAML Schema Contract: 解读文档格式规范

**Date**: 2026-03-05 | **Branch**: `002-rag-data-migration`

## Overview

本文档定义解读文档的 YAML front matter 结构规范，所有 Skills 输出必须遵循此契约。

---

## Base Schema (所有解读文档通用)

```yaml
# 必填字段
sample_id: string          # 格式: SSBR-XXX
interpretation_type: enum  # nmr | tem | mechanical | dsc | summary
skill_used: string         # 生成该文档的 Skill 名称
created_at: date           # 格式: YYYY-MM-DD

# 可选字段
source_figure: string      # 来源图注，如 "Figure 4"
source_doi: string         # 来源 DOI
updated_at: date           # 最后更新日期
```

---

## mechanical.md Schema

```yaml
---
sample_id: SSBR-XXX
interpretation_type: mechanical
source_figure: string | null
source_doi: string | null
skill_used: ssbr-mechanical-interpretation | ssbr-stress-strain-interpretation | ssbr-payne-interpretation | ssbr-dma-interpretation
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD | null

mechanical_subtypes:        # 必填：包含的子类型列表
  - stress-strain           # 可选值
  - payne                   # 可选值
  - dma                     # 可选值

data:
  # ========== 应力-应变数据 ==========
  stress_100:               # 100%定伸应力
    value: number | null    # 精确值，单位 MPa
    range: string | null    # 区间值，如 "1.4-1.6"
    unit: "MPa"             # 固定值
    source: string          # 数据来源，如 "SI Table S5"
  
  stress_200:               # 200%定伸应力
    value: number | null
    range: string | null
    unit: "MPa"
    source: string
  
  stress_300:               # 300%定伸应力
    value: number | null
    range: string | null
    unit: "MPa"
    source: string
  
  tensile_strength:         # 拉伸强度
    value: number | null
    range: string | null
    unit: "MPa"
    source: string
  
  elongation:               # 断裂伸长率
    value: number | null
    range: string | null
    unit: "%"
    source: string
  
  mechanical_source: string # 数据来源层级，如 "L1" | "L2" | "L3"
  
  # ========== Payne 效应数据 ==========
  delta_g_prime:            # ΔG' (Payne 效应幅度)
    value: number | null
    unit: "kPa"
    source: string
  
  delta_g_prime_reduction:  # ΔG' 下降百分比
    value: number | null
    unit: "%"
    source: string
  
  g_prime_0:                # 初始储能模量
    value: number | null
    unit: "kPa"
    source: string
  
  g_prime_inf:              # 稳定储能模量
    value: number | null
    unit: "kPa"
    source: string
  
  # ========== DMA 数据 ==========
  tan_delta_0c:             # 0℃ tanδ (湿地抓地力指标)
    value: number | null
    unit: "-"
    source: string
  
  tan_delta_60c:            # 60℃ tanδ (滚动阻力指标)
    value: number | null
    unit: "-"
    source: string
  
  performance_balance_factor:  # 0℃tanδ / 60℃tanδ
    value: number | null
    unit: "-"
    source: string
---
```

---

## dsc.md Schema

```yaml
---
sample_id: SSBR-XXX
interpretation_type: dsc
source_figure: string | null
source_doi: string | null
skill_used: ssbr-dsc-interpretation
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD | null

data:
  tg:                       # 玻璃化转变温度
    value: number | null    # 精确值，单位 ℃
    range: string | null    # 区间值，如 "-27 ~ -24"
    unit: "℃"
    source: string
  
  thermal_source: string    # 数据来源层级
  
  working_temp_window:      # 高弹性工作温度窗口
    value: string | null    # 如 "-50 ~ 80"
    unit: "℃"
    source: string
  
  other_transitions:        # 其他热转变
    value: string | null    # 文字描述
    source: string
---
```

---

## nmr.md Schema

```yaml
---
sample_id: SSBR-XXX
interpretation_type: nmr
source_figure: string | null
source_doi: string | null
skill_used: ssbr-nmr-interpretation
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD | null

data:
  functionalization_degree:  # 官能化程度（从 NMR 计算）
    value: number | null
    unit: "wt%"
    source: string
    calculation_method: string | null  # 计算方法说明
  
  characteristic_peaks:      # 特征峰列表
    - chemical_shift: number  # 化学位移 (ppm)
      assignment: string      # 峰归属
      integral: number | null # 积分比
  
  vinyl_content:            # 乙烯基含量
    value: number | null
    unit: "%"
    source: string
---
```

---

## tem.md Schema

```yaml
---
sample_id: SSBR-XXX
interpretation_type: tem
source_figure: string | null
source_doi: string | null
skill_used: ssbr-tem-interpretation
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD | null

data:
  domain_size:              # 相区尺寸
    value: number | null
    range: string | null    # 如 "20-50"
    unit: "nm"
    source: string
  
  dispersion_quality: string  # 分散质量评价：优/良/中/差
  
  morphology: string        # 形貌描述
  
  scale_bar: number | null  # 标尺长度 (nm)
---
```

---

## summary.md Schema

```yaml
---
sample_id: SSBR-XXX
interpretation_type: summary
skill_used: ssbr-summary-generator
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD | null

interpretations_included:   # 已纳入的解读文档类型
  - mechanical              # 枚举值列表
  - dsc
  - nmr
  - tem

interpretations_missing:    # 缺失的解读文档类型
  - nmr                     # 枚举值列表
  - tem
---
```

---

## Validation Rules

### 必填字段验证

| Schema | 必填字段 |
|--------|----------|
| Base | sample_id, interpretation_type, skill_used, created_at |
| mechanical | mechanical_subtypes, data |
| dsc | data.tg |
| summary | interpretations_included |

### 数值范围验证

| 字段 | 最小值 | 最大值 | 单位 |
|------|--------|--------|------|
| stress_* | 0 | 50 | MPa |
| tensile_strength | 0 | 100 | MPa |
| elongation | 0 | 1000 | % |
| tg | -100 | 50 | ℃ |
| tan_delta_* | 0 | 2 | - |
| delta_g_prime | 0 | 5000 | kPa |
| functionalization_degree | 0 | 100 | wt% |
| domain_size | 0 | 500 | nm |

### 格式验证

| 字段 | 格式 | 示例 |
|------|------|------|
| sample_id | `/^SSBR-\d{3}$/` | SSBR-001 |
| created_at | `/^\d{4}-\d{2}-\d{2}$/` | 2026-03-05 |
| source_doi | `/^10\.\d+\/.*$/` | 10.1039/c9ra02783a |
| range | `/^[\d.-]+\s*~\s*[\d.-]+$/` | -27 ~ -24 |

---

## Error Handling

### 缺失值处理

```yaml
# 文献未提供的数据：使用 null
stress_100:
  value: null
  source: "文献未提供"

# 估读数据：使用 range 替代 value
tg:
  value: null
  range: "-27 ~ -24"
  source: "曲线估读"
```

### 无效数据标记

```yaml
# 数据质量问题标记
stress_100:
  value: 1.5
  source: "SI Table S5"
  quality_flag: "uncertain"  # 可选：数据存疑标记
```

---

## Compatibility Notes

### 与 001-ssbr-knowledge-recommender 的兼容性

本 Schema 是对 001 版本的扩展，主要变更：
- 新增 `data` 嵌套结构存储迁移数据
- 新增 `mechanical_subtypes` 支持多类型力学文档
- 新增 `interpretations_included/missing` 追踪解读完整性

### 向后兼容性

- 现有 TEMPLATE.md 格式继续支持
- 新增字段为可选，不影响旧文档解析
