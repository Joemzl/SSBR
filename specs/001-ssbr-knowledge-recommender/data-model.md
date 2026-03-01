# Data Model: SSBR官能化知识库

**Date**: 2026-02-28 | **Branch**: `001-ssbr-knowledge-recommender`

## Overview

本文档定义知识库的数据结构，基于 `/dataset/数据.xlsx` 文件。数据模型设计遵循以下原则：
- 与现有 Excel 结构兼容
- 支持推荐系统的匹配需求
- 兼容未来向 SQLite/PostgreSQL 迁移

---

## Entity: 官能化样本 (FunctionalizedSample)

### 核心标识字段

| 字段名 | 数据类型 | 必填 | 说明 |
|--------|----------|------|------|
| 样本ID | String | ✅ | 唯一标识符，格式：`SSBR-XXX` |
| 样品名称 | String | ✅ | 文献中使用的样品名称/编号 |

### 官能化信息字段

| 字段名 | 数据类型 | 必填 | 说明 | 示例 |
|--------|----------|------|------|------|
| 官能化试剂名称 | String | ✅ | 使用的官能化试剂全称 | 3-氨丙基三乙氧基硅烷 |
| 试剂整体 SMILES | String | ❌ | 试剂完整分子 SMILES | SCCC[Si](OCC)(OCC)OCC |
| 核心官能团 SMILES | String | ❌ | 关键功能基团 SMILES | [Si](OCC)(OCC)OCC |
| 核心官能团名称 | String | ✅ | 官能团中文名称 | 三乙氧基硅烷基 |
| 核心官能团化学式 | String | ✅ | 官能团化学式 | -Si(OC₂H₅)₃ |
| 官能化程度 | Decimal | ❌ | 接枝百分比，单位 % | 3.6 |
| 官能化方法 | String | ❌ | 改性方法描述 | 溶液接枝法 |

### 应用场景字段

| 字段名 | 数据类型 | 必填 | 说明 | 允许值 |
|--------|----------|------|------|--------|
| 应用场景 | String | ❌ | 目标应用领域 | 轮胎胎面、密封制品、减震材料、通用橡胶制品 |

### 力学性能字段

| 字段名 | 数据类型 | 必填 | 单位 | 数据来源层级 |
|--------|----------|------|------|--------------|
| 100%定伸应力 | Decimal/Range | ❌ | MPa | Level 1/2/3 |
| 200%定伸应力 | Decimal/Range | ❌ | MPa | Level 1/2/3 |
| 300%定伸应力 | Decimal/Range | ❌ | MPa | Level 1/2/3 |
| 拉伸强度 | Decimal/Range | ❌ | MPa | Level 1/2/3 |
| 断裂伸长率 | Decimal/Range | ❌ | % | Level 1/2/3 |
| 力学数据来源 | String | ❌ | - | Table X / 图面标注 / 曲线估读 |

**Range 格式**: 当数据为估读时，使用区间表示，如 `4.0-4.5`

### 热学性能字段

| 字段名 | 数据类型 | 必填 | 单位 | 数据来源层级 |
|--------|----------|------|------|--------------|
| 玻璃化转变温度Tg | Decimal/Range | ❌ | ℃ | Level 1/2/3 |
| 高弹性工作温度窗口 | String | ❌ | ℃ | - |
| 其他热转变 | String | ❌ | - | - |
| 热学数据来源 | String | ❌ | - | Table X / 图面标注 / 曲线估读 |

### 文献来源字段

| 字段名 | 数据类型 | 必填 | 说明 |
|--------|----------|------|------|
| 文献DOI | String | ✅ | 文献唯一标识 |
| 第一作者 | String | ❌ | 文献第一作者姓氏 |
| 发表年份 | Integer | ❌ | 发表年份 |
| 引文信息 | String | ❌ | 完整引文格式 |
| 本地PDF路径 | String (Computed) | ✅ | 自动生成：`/literature/{DOI}_{作者}_{年份}.pdf` |

### 表征图注字段

| 字段名 | 数据类型 | 必填 | 说明 |
|--------|----------|------|------|
| 核磁谱图 | String | ❌ | 图注信息，如 `Figure 2a` |
| 微相分离图片表征 | String | ❌ | TEM 图注信息 |
| 应力-应变曲线 | String | ❌ | 曲线图注信息 |
| DSC谱图 | String | ❌ | DSC 图注信息 |

### 表征解读字段

| 字段名 | 数据类型 | 必填 | 说明 |
|--------|----------|------|------|
| 核磁解读 | Text | ❌ | ¹H NMR 标准化解读结果 |
| TEM解读 | Text | ❌ | TEM 标准化解读结果 |
| 应力应变解读 | Text | ❌ | 应力-应变曲线标准化解读结果 |
| DSC解读 | Text | ❌ | DSC 谱图标准化解读结果 |

---

## Data Quality Rules

### 数据来源层级定义

| 层级 | 标识 | 定义 | 推荐权重 |
|------|------|------|----------|
| Level 1 | L1 | 图表/曲线上直接标注的精确数值 | 最高 |
| Level 2 | L2 | 文献正文或 Table 中明确给出 | 高 |
| Level 3 | L3 | 曲线上可观测但无标注，使用区间 | 中 |
| Level 4 | L4 | 文献未提供，填写 `-` | 不参与匹配 |

### 字段格式规范

| 字段类型 | 格式要求 | 示例 |
|----------|----------|------|
| 应力数值 | 最多保留1位小数 | `4.2 MPa` |
| 温度数值 | 最多保留1位小数 | `-25.1 ℃` |
| 区间数值 | 使用 `-` 连接 | `4.0-4.5 MPa` |
| 百分比 | 最多保留1位小数 | `3.6%` |
| 缺失数据 | 使用 `-` 表示 | `-` |

### 验证规则

1. **主键唯一性**: 样本ID 不可重复
2. **必填字段**: 样本ID、样品名称、官能化试剂名称、核心官能团、文献DOI 必须填写
3. **DOI 格式**: 必须为有效 DOI 格式（如 `10.1039/c9ra02783a`）
4. **数值范围**: 
   - 定伸应力: 0-50 MPa
   - Tg: -100 ~ 50 ℃
   - 官能化程度: 0-100 %

---

## State Transitions

### 样本数据生命周期

```
[新建] → [基础信息录入] → [表征解读完成] → [完整可用]
                              ↓
                         [部分解读]（可用于有限匹配）
```

### 状态定义

| 状态 | 定义 | 推荐可用性 |
|------|------|------------|
| 基础信息录入 | 官能化信息、文献来源已填写 | ❌ 不可用 |
| 部分解读 | 至少完成 1 类表征解读 | ⚠️ 有限可用 |
| 完整可用 | 核心性能数据（力学/热学）已录入 | ✅ 完全可用 |

---

## Relationships

```
官能化样本 (1) ←→ (1) 文献来源
官能化样本 (1) ←→ (0..1) 力学性能数据
官能化样本 (1) ←→ (0..1) 热学性能数据
官能化样本 (1) ←→ (0..4) 表征解读
```

---

## Future Migration Notes

当迁移到关系型数据库时，建议拆分为以下表结构：

```sql
-- 主表
CREATE TABLE samples (
    id VARCHAR(20) PRIMARY KEY,
    sample_name VARCHAR(100) NOT NULL,
    reagent_name VARCHAR(200) NOT NULL,
    functional_group VARCHAR(50) NOT NULL,
    functionalization_degree DECIMAL(5,2),
    application_scenario VARCHAR(100),
    doi VARCHAR(100) NOT NULL,
    first_author VARCHAR(50),
    publish_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 力学性能表
CREATE TABLE mechanical_properties (
    sample_id VARCHAR(20) PRIMARY KEY REFERENCES samples(id),
    stress_100 DECIMAL(5,2),
    stress_100_range VARCHAR(20),
    stress_200 DECIMAL(5,2),
    stress_300 DECIMAL(5,2),
    tensile_strength DECIMAL(5,2),
    elongation DECIMAL(6,2),
    data_source VARCHAR(50)
);

-- 热学性能表
CREATE TABLE thermal_properties (
    sample_id VARCHAR(20) PRIMARY KEY REFERENCES samples(id),
    tg DECIMAL(5,2),
    tg_range VARCHAR(20),
    working_temp_window VARCHAR(100),
    other_transitions TEXT,
    data_source VARCHAR(50)
);

-- 表征解读表
CREATE TABLE interpretations (
    id SERIAL PRIMARY KEY,
    sample_id VARCHAR(20) REFERENCES samples(id),
    type VARCHAR(20) CHECK (type IN ('NMR', 'TEM', 'StressStrain', 'DSC')),
    content TEXT,
    figure_ref VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Excel Column Mapping

以下为 Excel 列与数据模型字段的对应关系：

| Excel 列名 | 数据模型字段 | 备注 |
|------------|--------------|------|
| 样本ID | id | 主键 |
| 应用场景 | application_scenario | - |
| 官能化试剂名称 | reagent_name | - |
| 试剂整体 SMILES | reagent_smiles | 分子结构 |
| 核心官能团 SMILES | functional_group_smiles | 官能团 SMILES |
| 核心官能团名称 | functional_group_name | 中文名称 |
| 核心官能团化学式 | functional_group_formula | 化学式 |
| 官能化程度 | functionalization_degree | 百分比数值 |
| 核磁谱图 | nmr_figure_ref | 图注信息 |
| 微相分离图片表征 | tem_figure_ref | 图注信息 |
| 应力-应变曲线 | stress_strain_figure_ref | 图注信息 |
| DSC谱图 | dsc_figure_ref | 图注信息 |
| 引文 | citation | 完整引文 |
| DOI | doi | 文献标识 |
| DOI_SI | doi_si | SI 补充材料标识 |
| 100%定伸应力（MPa） | stress_100 | 可为区间 |
| 200%定伸应力（MPa） | stress_200 | 可为区间 |
| 300%定伸应力（MPa） | stress_300 | 可为区间 |
| 拉伸强度（MPa） | tensile_strength | - |
| 断裂伸长率（%） | elongation | - |
| 力学数据来源 | mechanical_source | Level 标注 |
| 玻璃化转变温度Tg（℃） | tg | 可为区间 |
| 热学数据来源 | thermal_source | Level 标注 |
