# 新样本录入 SOP（Standard Operating Procedure）

**Date**: 2026-03-14 | **Branch**: `002-rag-data-migration`

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
2. ✅ **方式一**：文献已导入 Zotero 的 SSBR 目录（推荐）
3. ✅ **方式二**：文献 PDF 放置在 `/literature/` 目录（备选）

---

## 录入流程

### 方式 A：使用 AI 提取 + 脚本导入（推荐）

#### Step A1：使用 AI 提取元数据

1. 打开 Zotero，找到目标文献的 PDF
2. 使用豆包/Gemini 等 AI，上传 PDF 并发送 `other/解析数据的提示词.txt` 中的提示词
3. AI 会输出 Markdown 表格格式的结构化数据

#### Step A2：导入元数据到 Excel

将 AI 输出的 Markdown 表格保存为文件，运行导入脚本：

```bash
# 试运行（预览，不实际写入）
python scripts/import_metadata.py --file extracted_data.md --dry-run

# 正式导入
python scripts/import_metadata.py --file extracted_data.md
```

或使用剪贴板导入：
```bash
# 复制 AI 输出的表格后
python scripts/import_metadata.py --clipboard
```

脚本会：
- 自动分配样本 ID（如 SSBR-015）
- 验证必填字段
- 检查 DOI 重复
- 备份 Excel 文件

#### Step A3：初始化样本目录

导入完成后，为新样本创建解读文档目录：

```bash
python scripts/init_new_sample.py --sample-id SSBR-XXX
```

---

### 方式 B：手动录入

#### Step B1：初始化新样本目录

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

#### Step B2：在 Excel 中添加元数据

打开 `/dataset/数据.xlsx`，在新行中填写以下字段（A-W 列，共 23 列）：

| 列 | 字段名 | 必填 | 说明 |
|----|--------|------|------|
| A | 样本ID | ✅ | 格式 `SSBR-XXX`，必须与 Step 1 一致 |
| B | 是否是 SSBR | ✅ | 填"是"或"否" |
| C | 是否是链中官能化 | ✅ | 填"是"或"否" |
| D | 苯乙烯含量_wt% | ❌ | 基体苯乙烯质量分数 |
| E | 乙烯基含量_mol% | ❌ | 丁二烯中乙烯基摩尔占比 |
| F | 数均分子量 (Mn) | ❌ | 基础 SSBR 的 Mn |
| G | 应用场景 | ❌ | 目标应用领域 |
| H | 官能化试剂名称 | ✅ | 试剂全称 |
| I | 试剂整体 SMILES | ❌ | 分子结构 |
| J | 接枝反应基团 | ✅ | 与主链反应的锚点基团 |
| K | 核心官能团 SMILES | ❌ | 官能团结构 |
| L | 核心官能团名称 | ✅ | 中文名称 |
| M | 核心官能团化学式 | ✅ | 化学式 |
| N | 官能化程度_原始数值 | ❌ | 接枝程度数值 |
| O | 官能化程度_原始单位 | ❌ | 单位（wt%/mol%/phr） |
| P | 高分子指纹描述符 | ❌ | 自动生成的复合标识符 |
| Q | 核磁谱图 | ❌ | 图注引用 |
| R | 微相分离图片表征 | ❌ | TEM 图注 |
| S | 核心力学图谱 | ❌ | 力学图注 |
| T | DSC 谱图 | ❌ | DSC 图注 |
| U | 引文 | ✅ | 完整引文 |
| V | DOI | ✅ | 文献 DOI（原始格式） |
| W | DOI_SI | ❌ | SI 存在性标记（`有`/`-`） |

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

Skills 会自动：
1. 通过 Zotero MCP 获取 PDF 路径（或从 `literature/` 目录 fallback）
2. 生成解读并保存到对应目录

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

## 文献获取方式

### 方式一：Zotero MCP（推荐）

Skills 会通过 Zotero MCP 自动获取 PDF 路径：
- 确保文献已导入 Zotero 的 SSBR 目录
- 确保 Zotero 已启动且 MCP 服务正常运行

测试 Zotero 连接：
```bash
python scripts/zotero_bridge.py search "文献DOI"
```

### 方式二：本地 literature/ 目录（备选）

如果 Zotero 不可用，Skills 会自动 fallback 到本地目录：

| 原始 DOI | 文件名 |
|----------|--------|
| `10.1039/c9ra02783a` | `10.1039_c9ra02783a.pdf` |
| `10.1016/j.polymer.2018.04.039` | `10.1016_j.polymer.2018.04.039.pdf` |

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

## 常见问题

### Q1：如何确定新样本的 ID？

使用导入脚本会自动分配 ID。手动录入时查看现有最大 ID：
```bash
python -c "from scripts.utils.excel_handler import ExcelHandler; e=ExcelHandler('dataset/数据.xlsx'); e.open(); print(e.get_next_sample_id())"
```

### Q2：文献中没有某类图谱怎么办？

在对应解读文档中标注"暂无此项数据"，summary.md 会自动记录 `interpretations_missing`。

### Q3：录入过程中 IDE 崩溃怎么办？

从 Step 1 重新开始，脚本会自动跳过已存在的文件。Excel 备份文件在 `dataset/` 目录中。

### Q4：如何批量录入多个样本？

使用 AI 提取多个样本的数据，合并到一个 Markdown 表格后一次性导入：
```bash
python scripts/import_metadata.py --file batch_data.md
```

### Q5：Zotero MCP 连接失败怎么办？

1. 确保 Zotero 已启动
2. 检查 MCP 服务状态
3. Skills 会自动 fallback 到 `literature/` 目录

---

## 完整录入检查清单

- [ ] 文献 PDF 已导入 Zotero 或放置到 `/literature/`
- [ ] SI 补充材料已导入 Zotero 或放置到 `/literature_SI/`（如有）
- [ ] Excel 元数据已填写（A-W 列）
- [ ] 样本目录已创建 `/dataset/interpretations/SSBR-XXX/`
- [ ] mechanical.md 已生成
- [ ] dsc.md 已生成
- [ ] nmr.md 已生成或标注"暂无数据"
- [ ] tem.md 已生成或标注"暂无数据"
- [ ] summary.md 已生成
- [ ] RAG 检索测试通过

---

*本 SOP 适用于 002-rag-data-migration 版本（2026-03-14 更新），支持 Zotero MCP 集成和 AI 辅助元数据提取。*
