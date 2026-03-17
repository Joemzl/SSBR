# 文献检索流程说明（Zotero MCP 集成版）

**Date**: 2026-03-14 | **Version**: 2.0

## 概述

本文档定义 SSBR Skills 的统一文献检索流程。自 2026-03-14 起，文献检索采用 **Zotero MCP 优先** 策略，保留本地 `literature/` 目录作为 fallback。

## 检索策略

```
┌─────────────────────────────────────────────────────────────┐
│                   文献检索优先级                              │
├─────────────────────────────────────────────────────────────┤
│  1. Zotero MCP (优先)                                       │
│     - 通过 DOI 搜索 Zotero 库                                │
│     - 获取 PDF 本地存储路径                                   │
│     - 自动识别主文献和 SI 补充材料                            │
│                                                             │
│  2. 本地 literature/ 目录 (Fallback)                         │
│     - 按 DOI 匹配文件名                                      │
│     - 用于 Zotero 不可用时的兜底                              │
└─────────────────────────────────────────────────────────────┘
```

## 统一检索流程

### Step 1：读取 Excel 元数据

从 `/dataset/数据.xlsx` 读取样本信息：

| 列 | 字段 | 用途 |
|----|------|------|
| A | 样本ID | 唯一标识 |
| V | DOI | **文献检索主键**（原始 DOI 格式） |
| W | DOI_SI | SI 存在性标记（`有` 或 `-`） |
| Q-T | 各类图注 | 定位具体图表 |

### Step 2：Zotero MCP 检索（优先）

**调用方式**（在 CodeBuddy IDE 中）：

```
使用 zotero-mcp 的 search_library 工具：
- 参数: {"q": "{DOI}", "limit": 3}
- 返回: 条目信息及 PDF 附件路径
```

**成功标志**：
- 返回结果中包含 `attachments` 数组
- 附件 `contentType` 为 `application/pdf`
- 附件 `filePath` 不为空

**SI 文件识别**：
- 文件名包含 `SI`、`Supporting`、`Supplementary` 等关键词
- 同一条目下的第二个 PDF 附件

### Step 3：Fallback 到本地目录

若 Zotero MCP 不可用或未找到，则：

1. **主文献**：在 `/literature/` 目录搜索文件名包含 DOI 的 PDF
2. **SI 补充材料**：在 `/literature_SI/` 目录搜索

**DOI 匹配规则**：
- DOI 中的 `/` 可能被替换为 `_`
- 匹配时忽略大小写
- 文件名可能包含作者和年份后缀

### Step 4：错误处理

| 错误场景 | 输出信息 |
|----------|----------|
| Zotero MCP 不可用 | 「提示：Zotero MCP 连接失败，尝试使用本地文献目录」 |
| 两种方式均未找到 | 「错误：未找到 DOI 为 {DOI} 的对应文献，请确认文献已导入 Zotero 或放置在 literature/ 目录」 |
| 未找到 SI 文件 | 「提示：未找到 SI 补充材料，部分详细数据可能无法获取」 |

## Excel 字段变更说明

### DOI 列（V 列）

- **旧格式**：路径安全格式（`10.1039_c4ra09492a_Qu_2014`）
- **新格式**：原始 DOI（`10.1039/c4ra09492a`）
- **用途变更**：从"文件名匹配"变为"Zotero 搜索 + 文献标识"

### DOI_SI 列（W 列）

- **旧格式**：SI 文件名（`10.1039_c4ra09492a_Qu_2014_SI`）
- **新格式**：存在性标记（`有` 或 `-`）
- **用途变更**：仅标记 SI 是否存在，不再用于文件查找

## 脚本工具

`scripts/zotero_bridge.py` 提供以下功能：

```bash
# 按 DOI 搜索
python zotero_bridge.py search 10.1039/c4ra09492a

# 获取 PDF 路径
python zotero_bridge.py path --doi 10.1039/c4ra09492a

# 获取 SI 路径
python zotero_bridge.py path --doi 10.1039/c4ra09492a --si

# 列出 SSBR 目录文献
python zotero_bridge.py list --with-pdf
```

## 兼容性

- 本地 `literature/` 和 `literature_SI/` 目录保留不删除
- 支持渐进式迁移：新录入的样本使用 Zotero，旧样本仍可使用本地文件
- Skills 自动检测并选择可用的检索方式
