# Data Model: RAG 推荐系统数据架构

**Date**: 2026-03-05 | **Branch**: `002-rag-data-migration`

## Overview

本文档定义重构后的数据架构，核心变更为：
- Excel 仅存储元数据（A-O 列）
- 性能数值迁移到解读文档（YAML front matter）
- 新增 summary.md 作为 RAG 检索的核心文档

---

## Entity: 样本 (Sample)

### 定义
一条 SSBR 官能化案例记录，由 Excel 元数据行和 interpretations 目录下的文档集合组成。

### 唯一标识
- **字段**: `sample_id`
- **格式**: `SSBR-XXX`（XXX 为三位数字编号）
- **示例**: `SSBR-001`, `SSBR-017`

### 组成结构
```
Sample = Excel 元数据行 + Interpretations 文档集合

样本 SSBR-001
├── Excel Row (数据.xlsx A1-O1)
│   ├── 样本ID: SSBR-001
│   ├── 官能化信息 (B-H列)
│   ├── 图注引用 (I-L列)
│   └── 文献来源 (M-O列)
│
└── /interpretations/SSBR-001/
    ├── nmr.md          # 可选
    ├── tem.md          # 可选
    ├── mechanical.md   # 必需（含迁移数据）
    ├── dsc.md          # 必需（含迁移数据）
    └── summary.md      # 必需（RAG 检索核心）
```

---

## Entity: Excel 元数据 (Metadata)

### 字段定义（A-O 列）

| 列 | 字段名 | 数据类型 | 必填 | 说明 |
|----|--------|----------|------|------|
| A | 样本ID | String | ✅ | 主键，格式 `SSBR-XXX` |
| B | 应用场景 | String | ❌ | 目标应用领域 |
| C | 官能化试剂名称 | String | ✅ | 试剂全称 |
| D | 试剂整体 SMILES | String | ❌ | 分子结构 |
| E | 核心官能团 SMILES | String | ❌ | 官能团结构 |
| F | 核心官能团名称 | String | ✅ | 中文名称 |
| G | 核心官能团化学式 | String | ✅ | 化学式 |
| H | 官能化程度 (wt%) | Decimal | ❌ | 接枝程度 |
| I | 核磁谱图 | String | ❌ | 图注引用 |
| J | 微相分离图片表征 | String | ❌ | TEM 图注 |
| K | 核心力学图谱 | String | ❌ | 力学图注（支持多类型） |
| L | DSC 谱图 | String | ❌ | DSC 图注 |
| M | 引文 | String | ✅ | 完整引文 |
| N | DOI | String | ✅ | 文献 DOI |
| O | DOI_SI | String | ❌ | SI 补充材料 DOI |

### 已移除的列（P-W）

以下列在数据迁移后删除，数据存储于解读文档：

| 原列 | 原字段名 | 迁移目标 |
|------|----------|----------|
| P | 100%定伸应力（MPa） | mechanical.md → `data.stress_100` |
| Q | 200%定伸应力（MPa） | mechanical.md → `data.stress_200` |
| R | 300%定伸应力（MPa） | mechanical.md → `data.stress_300` |
| S | 拉伸强度（MPa） | mechanical.md → `data.tensile_strength` |
| T | 断裂伸长率（%） | mechanical.md → `data.elongation` |
| U | 力学数据来源 | mechanical.md → `data.mechanical_source` |
| V | 玻璃化转变温度Tg（℃） | dsc.md → `data.tg` |
| W | 热学数据来源 | dsc.md → `data.thermal_source` |

---

## Entity: 解读文档 (Interpretation Document)

### 定义
存储特定类型表征解读结果的 Markdown 文件，包含 YAML 结构化数值和自然语言描述。

### 文档类型

| 文件名 | type 值 | 说明 |
|--------|---------|------|
| nmr.md | nmr | ¹H NMR 解读 |
| tem.md | tem | TEM 形貌解读 |
| mechanical.md | mechanical | 力学性能解读（支持多子类型） |
| dsc.md | dsc | DSC 热分析解读 |
| summary.md | summary | 综合档案（RAG 检索核心） |

### YAML Front Matter 基础结构

```yaml
---
sample_id: SSBR-XXX           # 必填：样本 ID
interpretation_type: mechanical # 必填：文档类型
source_figure: Figure 4        # 可选：来源图注
source_doi: 10.1039/xxxxxxx    # 可选：来源 DOI
skill_used: ssbr-stress-strain-interpretation  # 必填：生成该文档的 Skill
created_at: 2026-03-05         # 必填：创建日期
updated_at: 2026-03-05         # 可选：最后更新日期

data:                          # 结构化数值数据
  field_name:
    value: 1.5
    unit: MPa
    source: "SI Table S5"
---
```

---

## Entity: mechanical.md 详细结构

### YAML Front Matter

```yaml
---
sample_id: SSBR-XXX
interpretation_type: mechanical
source_figure: Figure 4, Figure 5
source_doi: 10.1039/xxxxxxx
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-05
mechanical_subtypes:           # 包含的子类型
  - stress-strain
  - payne
  - dma

data:
  # 应力-应变数据（迁移自 Excel P-T 列）
  stress_100:
    value: 1.5                 # 数值，可为 null
    range: "1.4-1.6"           # 区间（估读时使用）
    unit: MPa
    source: "SI Table S5"
  stress_200:
    value: 4.5
    unit: MPa
    source: "SI Table S5"
  stress_300:
    value: 9.0
    unit: MPa
    source: "SI Table S5"
  tensile_strength:
    value: 15.0
    unit: MPa
    source: "SI Table S5"
  elongation:
    value: 452
    unit: "%"
    source: "SI Table S5"
  mechanical_source: "L2"      # 数据来源层级
  
  # Payne 效应数据
  delta_g_prime:
    value: 850
    unit: kPa
    source: "Figure 5"
  delta_g_prime_reduction:
    value: 45
    unit: "%"
    source: "calculated"
  
  # DMA 数据
  tan_delta_0c:
    value: 0.45
    unit: "-"
    source: "SI Table S6"
  tan_delta_60c:
    value: 0.08
    unit: "-"
    source: "SI Table S6"
---
```

### Markdown 正文结构

```markdown
# 力学性能解读：SSBR-XXX

## 一、静态力学性能（应力-应变曲线）
### 核心发现
...

## 二、动态力学性能（Payne效应）
### 核心发现
...

## 三、动态力学性能（DMA温度扫描）
### 核心发现
...
```

---

## Entity: dsc.md 详细结构

### YAML Front Matter

```yaml
---
sample_id: SSBR-XXX
interpretation_type: dsc
source_figure: Figure 6
source_doi: 10.1039/xxxxxxx
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-05

data:
  tg:
    value: -25.5               # 精确值
    range: "-27 ~ -24"         # 区间（估读时使用）
    unit: "℃"
    source: "Table 2"
  thermal_source: "L1"         # 数据来源层级
  working_temp_window:
    value: "-50 ~ 80"
    unit: "℃"
    source: "estimated"
---
```

---

## Entity: summary.md 详细结构

### YAML Front Matter

```yaml
---
sample_id: SSBR-XXX
interpretation_type: summary
created_at: 2026-03-05
updated_at: 2026-03-05
interpretations_included:      # 已纳入的解读文档
  - mechanical
  - dsc
interpretations_missing:       # 缺失的解读文档
  - nmr
  - tem
---
```

### Markdown 正文结构（用于向量化）

```markdown
# SSBR-XXX 综合档案

## 一句话总结
[自然语言：核心价值 + 适用场景]

## 官能化信息
- **试剂**：[官能化试剂名称]
- **核心官能团**：[核心官能团名称] ([化学式])
- **官能化程度**：[X] wt%
- **改性方法**：巯基-烯点击化学

## 核心性能特点
### [特点一标题] 【评价】
[自然语言描述，引用具体数值]

### [特点二标题] 【评价】
[自然语言描述，引用具体数值]

## 适用场景
- ✅ [场景一]
- ✅ [场景二]
- ⚠️ [注意事项]

## 关键性能指标
| 类别 | 指标 | 数值 | 评价 |
|------|------|------|------|
| ... | ... | ... | ... |

## 文献来源
- **DOI**: [DOI]
- **引文**: [完整引文]
```

---

## Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                     Sample (样本)                            │
│                      sample_id                              │
└─────────────────────────────────────────────────────────────┘
         │                                    │
         │ 1:1                                │ 1:N
         ▼                                    ▼
┌─────────────────────┐          ┌─────────────────────────────┐
│  Excel Metadata     │          │  Interpretation Documents    │
│  (数据.xlsx A-O列)   │          │  (/interpretations/{id}/)    │
│                     │          │                              │
│  - 官能化信息        │          │  - nmr.md (0..1)             │
│  - 图注引用          │          │  - tem.md (0..1)             │
│  - 文献来源          │          │  - mechanical.md (1) *必需   │
└─────────────────────┘          │  - dsc.md (1) *必需          │
                                 │  - summary.md (1) *必需      │
                                 └─────────────────────────────┘
```

---

## State Transitions

### 样本完整性状态

```
[新建] → [元数据录入] → [数据迁移完成] → [解读完善] → [RAG 可用]
                              │
                              ▼
                        summary.md 生成
```

### 状态定义

| 状态 | 条件 | RAG 可用性 |
|------|------|------------|
| 元数据录入 | Excel A-O 列已填写 | ❌ 不可用 |
| 数据迁移完成 | mechanical.md + dsc.md 存在且含迁移数据 | ⚠️ 部分可用 |
| 解读完善 | 至少 2 个解读文档有完整内容 | ⚠️ 部分可用 |
| RAG 可用 | summary.md 存在且内容完整 | ✅ 完全可用 |

---

## Validation Rules

### 样本 ID 验证
- 格式：`/^SSBR-\d{3}$/`
- 唯一性：不可重复

### YAML Front Matter 验证
- `sample_id`：必填，格式正确
- `interpretation_type`：必填，枚举值
- `created_at`：必填，日期格式 `YYYY-MM-DD`
- `skill_used`：必填，有效 Skill 名称

### 数值验证
| 字段 | 范围 | 单位 |
|------|------|------|
| stress_100/200/300 | 0-50 | MPa |
| tensile_strength | 0-100 | MPa |
| elongation | 0-1000 | % |
| tg | -100 ~ 50 | ℃ |
| tan_delta_* | 0-2 | - |

### summary.md 完整性验证
- 必须包含章节：一句话总结、官能化信息、核心性能特点、适用场景、文献来源
- 自然语言内容长度：≥ 200 字符
- 必须引用至少 2 个具体数值

---

## Migration Mapping

### Excel → 解读文档 字段映射

```
数据.xlsx                          /interpretations/SSBR-XXX/
┌──────────────────────────┐       ┌─────────────────────────────┐
│ P: 100%定伸应力          │ ──→   │ mechanical.md               │
│ Q: 200%定伸应力          │ ──→   │   data.stress_100.value     │
│ R: 300%定伸应力          │ ──→   │   data.stress_200.value     │
│ S: 拉伸强度              │ ──→   │   data.stress_300.value     │
│ T: 断裂伸长率            │ ──→   │   data.tensile_strength.value│
│ U: 力学数据来源          │ ──→   │   data.elongation.value     │
└──────────────────────────┘       │   data.mechanical_source    │
                                   └─────────────────────────────┘

┌──────────────────────────┐       ┌─────────────────────────────┐
│ V: Tg                    │ ──→   │ dsc.md                      │
│ W: 热学数据来源          │ ──→   │   data.tg.value             │
└──────────────────────────┘       │   data.thermal_source       │
                                   └─────────────────────────────┘
```

---

## Index Structure (for RAG)

### 向量索引逻辑结构

```
VectorIndex = {
    sample_id: str,           # 样本 ID
    embedding: float[1536],   # summary.md 内容的向量表示
    summary_path: str,        # summary.md 文件路径
    last_updated: datetime    # 最后更新时间
}
```

### MVP 实现（无持久化）

```python
# 运行时内存结构
index = {
    "SSBR-001": {
        "embedding": None,    # 实时计算，不缓存
        "summary_path": "/dataset/interpretations/SSBR-001/summary.md"
    },
    ...
}
```

### 未来 Chroma 结构

```python
collection.add(
    documents=[summary_content],
    ids=[sample_id],
    metadatas=[{"path": summary_path, "updated": updated_at}]
)
```
