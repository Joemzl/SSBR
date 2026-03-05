# Quick Start: RAG 推荐系统数据架构重构

**Date**: 2026-03-05 | **Branch**: `002-rag-data-migration`

## 概述

本指南帮助你快速理解和参与 RAG 数据架构重构项目。

---

## 架构变更总览

### Before (001 架构)

```
数据.xlsx (A-W 列)
├── A-O: 元数据 + 图注 + 文献
└── P-W: 力学/热学数值 ← 冗余存储

/skills/ssbr-recommender/
└── 基于 Excel 精确匹配推荐
```

### After (002 架构)

```
数据.xlsx (A-O 列)
└── 只保留元数据

/interpretations/SSBR-XXX/
├── mechanical.md  ← 力学数值 + 解读
├── dsc.md         ← 热学数值 + 解读
├── nmr.md         ← 核磁解读
├── tem.md         ← TEM 解读
└── summary.md     ← RAG 检索核心

/skills/ssbr-recommender/
└── 基于 summary.md 语义检索推荐
```

---

## 快速开始

### 1. 环境检查

确认以下文件/目录存在：

```bash
# 检查数据文件
ls dataset/数据.xlsx

# 检查解读模板
ls dataset/interpretations/TEMPLATE.md

# 检查 Skills
ls skills/ssbr-recommender/SKILL.md
```

### 2. 理解数据流

```
用户查询 → Embedding API → 查询向量
                              ↓
summary.md → Embedding API → 文档向量
                              ↓
                        余弦相似度计算
                              ↓
                        Top-K 样本
                              ↓
                        LLM 生成推荐
```

### 3. 关键文件说明

| 文件 | 作用 | 格式 |
|------|------|------|
| `数据.xlsx` | 元数据存储 | Excel (A-O 列) |
| `interpretations/SSBR-XXX/mechanical.md` | 力学解读 + 数值 | YAML + Markdown |
| `interpretations/SSBR-XXX/dsc.md` | 热学解读 + 数值 | YAML + Markdown |
| `interpretations/SSBR-XXX/summary.md` | **RAG 检索核心** | YAML + Markdown |

---

## 常用操作

### 查看样本解读文档

```bash
# 查看 SSBR-001 的所有解读
ls dataset/interpretations/SSBR-001/

# 查看 summary.md 内容
cat dataset/interpretations/SSBR-001/summary.md
```

### 调用推荐 Skill

在 CodeBuddy IDE 中：

```
@ssbr-recommender 我需要改善白炭黑分散性并降低滚动阻力
```

### 生成样本综合档案

```
@ssbr-summary-generator 请为样本 SSBR-001 生成综合档案
```

### 执行力学解读

```
@ssbr-mechanical-interpretation 请解读 SSBR-001 的核心力学图谱
```

---

## YAML Front Matter 快速参考

### mechanical.md 必填字段

```yaml
---
sample_id: SSBR-XXX           # 必填
interpretation_type: mechanical  # 必填
skill_used: ssbr-mechanical-interpretation  # 必填
created_at: 2026-03-05        # 必填
mechanical_subtypes:          # 必填
  - stress-strain

data:
  stress_100:
    value: 1.5
    unit: MPa
    source: "SI Table S5"
---
```

### summary.md 必填字段

```yaml
---
sample_id: SSBR-XXX
interpretation_type: summary
skill_used: ssbr-summary-generator
created_at: 2026-03-05
interpretations_included:
  - mechanical
  - dsc
---
```

---

## 故障排查

### 推荐结果为空

**可能原因**：
1. summary.md 未生成
2. summary.md 内容过短

**解决方案**：
```bash
# 检查 summary.md 是否存在
ls dataset/interpretations/*/summary.md

# 检查内容长度
wc -c dataset/interpretations/SSBR-001/summary.md
```

### YAML 解析错误

**可能原因**：
1. 缩进不一致
2. 特殊字符未转义

**解决方案**：
```bash
# 在线 YAML 验证器
# https://www.yamllint.com/
```

### Embedding API 失败

**可能原因**：
1. 网络不可用
2. API 配额用尽

**解决方案**：
- 检查网络连接
- 查看 API 使用量
- 等待配额重置或升级

---

## 开发规范

### 提交代码前检查

- [ ] YAML front matter 格式正确
- [ ] sample_id 与目录名一致
- [ ] summary.md 包含 4 个必需章节
- [ ] 数值单位标注正确

### 分支命名

```
002-rag-data-migration  # 主开发分支
```

### 提交信息格式

```
feat(002): 添加 SSBR-001 的 summary.md
fix(002): 修复 mechanical.md YAML 格式错误
docs(002): 更新数据模型文档
```

---

## 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 功能规范 | `specs/002-rag-data-migration/spec.md` | 需求定义 |
| 实施计划 | `specs/002-rag-data-migration/plan.md` | 技术方案 |
| 数据模型 | `specs/002-rag-data-migration/data-model.md` | 实体定义 |
| YAML Schema | `specs/002-rag-data-migration/contracts/yaml-schema.md` | 格式规范 |
| 检索接口 | `specs/002-rag-data-migration/contracts/search-api.md` | API 契约 |
| 解读模板 | `dataset/interpretations/TEMPLATE.md` | 文件模板 |

---

## 联系方式

如有问题，请在项目仓库提交 Issue 或联系项目维护者。
