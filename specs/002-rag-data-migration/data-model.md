# Data Model: RAG 推荐系统数据架构

**Date**: 2026-03-14 | **Branch**: `002-rag-data-migration`

## Overview

本文档定义重构后的数据架构，核心变更为：
- Excel 存储元数据（A-W 列，23 列）
- 性能数值迁移到解读文档（YAML front matter）
- 新增 summary.md 作为 RAG 检索的核心文档
- **Zotero 集成**：通过 Zotero MCP 获取文献 PDF，替代本地 `literature/` 目录匹配
- **新增字段**：苯乙烯含量、乙烯基含量、数均分子量等 SSBR 基体特征参数

### 文献来源变更（2026-03-14）

| 项目 | 旧方案 | 新方案 |
|------|--------|--------|
| PDF 存储 | `literature/*.pdf` | Zotero 管理 |
| PDF 查找 | 按 DOI 匹配文件名 | Zotero MCP 获取路径 |
| DOI 格式 | 路径安全格式（`/` → `_`） | 原始 DOI 格式 |
| DOI_SI 列 | SI 文件名 | SI 存在性标记（`有`/`-`） |
| Fallback | — | 本地 `literature/` 目录 |

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

### 字段定义（A-W 列，共 23 列）

| 列 | 字段名 | 数据类型 | 必填 | 说明 |
|----|--------|----------|------|------|
| A | 样本ID | String | ✅ | 主键，格式 `SSBR-XXX` |
| B | 是否是 SSBR | String | ✅ | 过滤字段，"是"/"否" |
| C | 是否是链中官能化 | String | ✅ | 过滤字段，"是"/"否" |
| D | 苯乙烯含量_wt% | Decimal | ❌ | SSBR 基体苯乙烯质量分数 |
| E | 乙烯基含量_mol% | Decimal | ❌ | 丁二烯中乙烯基摩尔占比 |
| F | 数均分子量 (Mn) | Integer | ❌ | 改性前基础 SSBR 的 Mn |
| G | 应用场景 | String | ❌ | 目标应用领域 |
| H | 官能化试剂名称 | String | ✅ | 试剂全称 |
| I | 试剂整体 SMILES | String | ❌ | 分子结构 |
| J | 接枝反应基团 | String | ✅ | 与主链反应的锚点基团 |
| K | 核心官能团 SMILES | String | ❌ | 官能团结构 |
| L | 核心官能团名称 | String | ✅ | 中文名称 |
| M | 核心官能团化学式 | String | ✅ | 化学式 |
| N | 官能化程度_原始数值 | Decimal | ❌ | 接枝程度数值 |
| O | 官能化程度_原始单位 | String | ❌ | 单位（wt%/mol%/phr 等） |
| P | 高分子指纹描述符 | String | ❌ | 复合标识符（自动生成） |
| Q | 核磁谱图 | String | ❌ | 图注引用 |
| R | 微相分离图片表征 | String | ❌ | TEM 图注 |
| S | 核心力学图谱 | String | ❌ | 力学图注（支持多类型） |
| T | DSC 谱图 | String | ❌ | DSC 图注 |
| U | 引文 | String | ✅ | 完整引文 |
| V | DOI | String | ✅ | **原始 DOI 格式**（保留 `/`） |
| W | DOI_SI | String | ❌ | **SI 存在性标记**：`有` 或 `-` |

### 新增字段说明（2026-03-14）

| 列 | 字段名 | 来源 | 用途 |
|----|--------|------|------|
| B | 是否是 SSBR | 提示词提取 | 数据过滤，非 SSBR 文献可标记后跳过 |
| C | 是否是链中官能化 | 提示词提取 | 数据过滤，排除端基改性/单体共聚 |
| D | 苯乙烯含量_wt% | 文献 | RAG 相似性比较 |
| E | 乙烯基含量_mol% | 文献 | RAG 相似性比较 |
| F | 数均分子量 (Mn) | 文献 | RAG 相似性比较 |
| J | 接枝反应基团 | 文献 | 反应类型分类 |
| P | 高分子指纹描述符 | 自动计算 | 样本唯一性校验 |

### DOI 格式变更说明

| 项目 | 旧格式 | 新格式 |
|------|--------|--------|
| DOI 列 | `10.1039_c4ra09492a_Qu_2014` | `10.1039/c4ra09492a` |
| DOI_SI 列 | `10.1039_c4ra09492a_Qu_2014_SI` | `有` 或 `-` |
| 用途 | 文件名匹配 | 文献标识 + Zotero 查询 |

### 已移除的列说明

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
┌─────────────────────────────────────────────────────────────────────────┐
│                          Sample (样本)                                   │
│                           sample_id                                     │
└─────────────────────────────────────────────────────────────────────────┘
         │                      │                         │
         │ 1:1                  │ 1:1                     │ 1:N
         ▼                      ▼                         ▼
┌─────────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐
│  Excel Metadata     │  │  Zotero Item    │  │  Interpretation Documents    │
│  (数据.xlsx A-W列)   │  │  (via MCP)      │  │  (/interpretations/{id}/)    │
│                     │  │                 │  │                              │
│  - SSBR 基体信息     │  │  - PDF 路径     │  │  - nmr.md (0..1)             │
│  - 官能化信息        │  │  - SI 路径      │  │  - tem.md (0..1)             │
│  - 图注引用          │  │  - 元数据       │  │  - mechanical.md (1) *必需   │
│  - 文献来源 (DOI)    │──│  (通过DOI关联)  │  │  - dsc.md (1) *必需          │
└─────────────────────┘  └─────────────────┘  │  - summary.md (1) *必需      │
                                             └─────────────────────────────┘
                                             
         │
         │ Fallback (Zotero 不可用时)
         ▼
┌─────────────────────┐
│  Local Literature   │
│  - /literature/     │
│  - /literature_SI/  │
└─────────────────────┘
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
