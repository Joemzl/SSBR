# 新样本录入 SOP（Standard Operating Procedure）

**Date**: 2026-03-05 | **Branch**: `002-rag-data-migration`

---

## 概述

本文档定义向 SSBR 官能化知识库添加新样本的标准操作流程。

### MVP 模式声明

**⚠️ 当前版本为 MVP 单用户模式**：
- 不支持多用户并发录入
- 不支持分布式部署
- 录入过程中请勿关闭 IDE 或终止脚本

---

## 前置条件

录入新样本前，请确保：

1. ✅ 已获取文献 PDF 和 SI 补充材料
2. ✅ 文献 PDF 放置在 `/literature/` 目录
3. ✅ SI 补充材料放置在 `/literature_SI/` 目录
4. ✅ PDF 命名符合规范：`{DOI}.pdf`（将 `/` 替换为 `_`）

---

## 录入流程

### Step 1：初始化新样本目录

运行初始化脚本创建样本目录结构：

```bash
python scripts/init_new_sample.py --sample-id SSBR-XXX
```

这将创建：
```
dataset/interpretations/SSBR-XXX/
├── mechanical.md   (空模板)
├── dsc.md          (空模板)
├── nmr.md          (空模板)
├── tem.md          (空模板)
└── summary.md      (空模板)
```

### Step 2：在 Excel 中添加元数据

打开 `/dataset/数据.xlsx`，在新行中填写以下字段：

| 列 | 字段名 | 必填 | 说明 |
|----|--------|------|------|
| A | 样本ID | ✅ | 格式 `SSBR-XXX`，必须与 Step 1 一致 |
| B | 应用场景 | ❌ | 目标应用领域 |
| C | 官能化试剂名称 | ✅ | 试剂全称 |
| D | 试剂整体 SMILES | ❌ | 分子结构 |
| E | 核心官能团 SMILES | ❌ | 官能团结构 |
| F | 核心官能团名称 | ✅ | 中文名称 |
| G | 核心官能团化学式 | ✅ | 化学式 |
| H | 官能化程度 (wt%) | ❌ | 接枝程度 |
| I | 核磁谱图 | ❌ | 图注引用 |
| J | 微相分离图片表征 | ❌ | TEM 图注 |
| K | 核心力学图谱 | ❌ | 力学图注 |
| L | DSC 谱图 | ❌ | DSC 图注 |
| M | 引文 | ✅ | 完整引文 |
| N | DOI | ✅ | 文献 DOI |
| O | DOI_SI | ❌ | SI 补充材料 DOI |

**保存并关闭 Excel 文件。**

### Step 3：生成解读文档

根据文献内容，调用对应的解读 Skills：

```
# 在 CodeBuddy IDE 中执行

# 力学解读
@ssbr-mechanical-interpretation 请解读样本 SSBR-XXX 的核心力学图谱

# DSC 解读
@ssbr-dsc-interpretation 请解读样本 SSBR-XXX 的 DSC 谱图

# NMR 解读（如有）
@ssbr-nmr-interpretation 请解读样本 SSBR-XXX 的核磁谱图

# TEM 解读（如有）
@ssbr-tem-interpretation 请解读样本 SSBR-XXX 的 TEM 图片
```

Skills 会自动将输出保存到对应目录。

### Step 4：生成综合档案

调用 summary 生成 Skill：

```
@ssbr-summary-generator 请为样本 SSBR-XXX 生成综合档案
```

或使用脚本：

```bash
python scripts/generate_summaries.py --sample SSBR-XXX
```

### Step 5：验证录入结果

检查录入完整性：

```bash
# 检查目录结构
ls dataset/interpretations/SSBR-XXX/

# 检查 summary.md 生成
cat dataset/interpretations/SSBR-XXX/summary.md

# 测试 RAG 检索
python scripts/rag_search.py --query "新样本相关关键词" --top-k 3
```

---

## 向量索引更新

### 自动更新（推荐）

summary.md 生成后，RAG 检索会在下次查询时自动读取新文件，无需手动触发向量化。

### 手动更新（可选）

如需预先计算向量缓存：

```bash
python scripts/update_vector_index.py --sample SSBR-XXX
```

---

## 文件命名规范

### PDF 文献命名

| 原始 DOI | 文件名 |
|----------|--------|
| `10.1039/c9ra02783a` | `10.1039_c9ra02783a.pdf` |
| `10.1016/j.polymer.2018.04.039` | `10.1016_j.polymer.2018.04.039.pdf` |

### 样本 ID 格式

- 格式：`SSBR-XXX`（XXX 为三位数字）
- 示例：`SSBR-001`, `SSBR-018`, `SSBR-123`
- 编号必须唯一且递增

---

## 常见问题

### Q1：如何确定新样本的 ID？

查看现有最大 ID，+1 即可：
```bash
ls dataset/interpretations/ | sort | tail -1
```

### Q2：文献中没有某类图谱怎么办？

在对应解读文档中标注"暂无此项数据"，summary.md 会自动记录 `interpretations_missing`。

### Q3：录入过程中 IDE 崩溃怎么办？

从 Step 1 重新开始，脚本会自动跳过已存在的文件。

### Q4：如何批量录入多个样本？

目前 MVP 版本仅支持单样本录入，请逐个执行上述流程。

---

## 完整录入检查清单

- [ ] PDF 文献已放置到 `/literature/`
- [ ] SI 补充材料已放置到 `/literature_SI/`（如有）
- [ ] 样本目录已创建 `/dataset/interpretations/SSBR-XXX/`
- [ ] Excel 元数据已填写（A-O 列）
- [ ] mechanical.md 已生成
- [ ] dsc.md 已生成
- [ ] nmr.md 已生成或标注"暂无数据"
- [ ] tem.md 已生成或标注"暂无数据"
- [ ] summary.md 已生成
- [ ] RAG 检索测试通过

---

*本 SOP 适用于 002-rag-data-migration MVP 版本，后续版本可能支持批量导入和并发录入。*
