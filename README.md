# SSBR 官能化方案智能推荐系统

基于 RAG 语义检索的绿色轮胎材料解决方案推荐系统。

---

## 目录

- [快速开始](#快速开始)
- [环境配置](#环境配置)
- [常用命令](#常用命令)
- [项目结构](#项目结构)
- [核心功能](#核心功能)
- [数据规模](#数据规模)
- [故障排查](#故障排查)
- [开发指南](#开发指南)

---

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd SSBR
```

### 2. 安装依赖

**系统要求**: Python 3.10+

```bash
pip install -r requirements.txt
```

<details>
<summary>主要依赖说明</summary>

| 依赖 | 版本 | 用途 |
|------|------|------|
| `openai` | ≥1.0.0 | Embedding API (text-embedding-3-small) |
| `chromadb` | ≥0.4.0 | 向量数据库 |
| `sentence-transformers` | ≥2.2.0 | 交叉编码器重排 (bge-reranker-base) |
| `gradio` | ≥4.0.0 | Web Demo 界面 |
| `openpyxl` | ≥3.1.0 | Excel 读写 |
| `anthropic` | ≥0.18.0 | Claude API (问答生成，可选) |

</details>

### 3. 配置环境变量

**必须配置** OpenAI API（用于 Embedding）：

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY = "sk-xxx"
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"  # 可选，使用代理时设置

# Windows (CMD)
set OPENAI_API_KEY=sk-xxx
set OPENAI_BASE_URL=https://api.openai.com/v1

# Linux/Mac
export OPENAI_API_KEY=sk-xxx
export OPENAI_BASE_URL=https://api.openai.com/v1
```

**可选配置** Anthropic API（用于问答生成，优先于 OpenAI）：

```bash
$env:ANTHROPIC_API_KEY = "sk-ant-xxx"
```

### 4. ⚠️ 构建向量缓存（首次使用/跨设备必需）

> **重要**：向量缓存（`.cache/chroma_db/`）不会通过 Git 同步，每台设备首次使用时必须重建。

```bash
python scripts/build_vector_cache.py --force
```

预期输出：
```
============================================================
SSBR 向量缓存构建工具
============================================================

正在扫描 summary.md 文件...
  发现 71 个 summary.md 文件

正在构建向量缓存 (使用 ChromaDB)...
  处理进度: 100%|████████████████████████| 71/71 [00:03<00:00]

构建完成:
  总文档数: 71
  新增: 71
  耗时: 3.2 秒
```

### 5. 启动 Web Demo

```bash
python demo/app.py
```

打开浏览器访问 http://localhost:7861

---

## 环境配置

### 环境变量一览

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `OPENAI_API_KEY` | ✅ | OpenAI API Key，用于 Embedding |
| `OPENAI_BASE_URL` | ❌ | OpenAI API 代理地址，默认官方 |
| `ANTHROPIC_API_KEY` | ❌ | Anthropic API Key，用于问答生成 |

### 永久配置（推荐）

**Windows**: 系统属性 → 高级 → 环境变量 → 新建用户变量

**Linux/Mac**: 添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
export OPENAI_API_KEY="sk-xxx"
```

---

## 常用命令

### 向量缓存管理

```bash
# 查看缓存状态
python scripts/build_vector_cache.py --stats

# 增量更新缓存（仅处理新增/修改的文档）
python scripts/build_vector_cache.py

# 强制重建缓存（首次使用/跨设备必需）
python scripts/build_vector_cache.py --force
```

### RAG 检索

```bash
# 命令行检索测试
python scripts/rag_search.py --query "改善白炭黑分散性" --top-k 5

# 问答测试（包含 GPT 回答生成）
python scripts/qa_engine.py --query "如何改善白炭黑分散性？"

# 仅检索，不生成回答
python scripts/qa_engine.py --query "提高湿地抓地力" --search-only
```

### Web Demo

```bash
# 启动 Web 界面
python demo/app.py

# 指定端口
python demo/app.py --port 7862
```

### 样本管理

```bash
# 初始化新样本目录
python scripts/init_new_sample.py --sample-id SSBR-072

# 批量生成 summary.md
python scripts/generate_summaries.py

# 验证数据完整性
python scripts/update_vector_index.py --validate-only
```

### 元数据导入

```bash
# 预览导入（不实际写入）
python scripts/import_metadata.py --file dataset/extracted_data.md --dry-run

# 执行导入
python scripts/import_metadata.py --file dataset/extracted_data.md
```

---

## 项目结构

```
SSBR/
├── .cache/                          # 缓存目录（不提交到 Git）
│   └── chroma_db/                   # ChromaDB 向量数据库
│       ├── chroma.sqlite3           # 元数据
│       └── [uuid]/                  # HNSW 索引文件
│
├── dataset/
│   ├── 数据.xlsx                    # 元数据 (A-X 列，24 列)
│   └── interpretations/             # 解读文档库
│       ├── SSBR-XXX/                # 各样本目录
│       │   ├── mechanical.md        # 力学解读
│       │   ├── dsc.md               # 热学解读
│       │   ├── nmr.md               # 核磁解读
│       │   ├── tem.md               # TEM 解读
│       │   └── summary.md           # 综合档案（RAG 检索核心）
│       └── TEMPLATE_*.md            # 模板文件
│
├── demo/
│   └── app.py                       # Gradio Web 应用
│
├── scripts/
│   ├── rag_search.py                # RAG 检索引擎
│   ├── qa_engine.py                 # 问答引擎
│   ├── build_vector_cache.py        # 向量缓存构建
│   ├── generate_summaries.py        # 批量生成 summary.md
│   ├── init_new_sample.py           # 新样本初始化
│   ├── import_metadata.py           # 元数据导入
│   ├── reranker.py                  # 交叉编码器重排
│   └── utils/                       # 工具函数库
│       ├── vector_store.py          # ChromaDB 向量存储
│       ├── embedding.py             # Embedding 服务
│       └── ...
│
├── skills/                          # CodeBuddy AI Skills
│   ├── ssbr-recommender/            # RAG 推荐 Skill
│   ├── ssbr-summary-generator/      # 综合档案生成 Skill
│   └── ssbr-*-interpretation/       # 各类解读 Skills
│
├── specs/                           # 规范文档
│   ├── 001-ssbr-knowledge-recommender/
│   ├── 002-rag-data-migration/
│   └── 003-rag-qa-enhancement/
│
├── literature/                      # 原始文献 PDF
├── CODEBUDDY.md                     # 开发指南（AI 生成）
├── README.md                        # 本文档
└── requirements.txt                 # Python 依赖
```

---

## 核心功能

### 1. 语义检索推荐

基于 OpenAI Embedding API 的 RAG 检索系统，从 71 个官能化样本中智能匹配最相关的方案。

**示例查询**：
- "改善白炭黑分散性"
- "降低轮胎滚动阻力"
- "提高湿地抓地力"

### 2. 智能问答

集成 GPT/Claude 的自然语言问答系统，三级回答类型：

| 类型 | 相似度阈值 | 说明 |
|------|------------|------|
| DIRECT | ≥0.7 | 直接回答，置信度高 |
| REFERENCE | 0.5-0.7 | 参考回答，需用户判断 |
| GUIDANCE | <0.5 | 引导性建议 |

### 3. 多维度数据解读

11 个专用 AI Skills 支持：
- 力学解读（应力-应变、Payne 效应、DMA）
- 热学解读（DSC）
- 核磁解读（¹H NMR）
- TEM 形貌解读
- 综合档案生成

### 4. 交叉编码器重排

使用 `bge-reranker-base` 模型对检索结果进行精排，提升检索精度。

---

## 数据规模

| 指标 | 数值 |
|------|------|
| 官能化样本数 | 71 |
| 解读文档数 | ~355 (每样本 5 个) |
| 文献来源 | 多篇 SCI 论文 |
| 覆盖官能团 | 羟基、羧基、硅氧烷、oxa-Michael 等 |
| 向量维度 | 1536 (text-embedding-3-small) |

---

## 故障排查

### 向量缓存相关

#### ❌ 错误: "ChromaDB collection not found"

**原因**: 首次使用或跨设备未构建缓存

**解决**:
```bash
python scripts/build_vector_cache.py --force
```

#### ❌ 错误: "No summaries found"

**原因**: `dataset/interpretations/*/summary.md` 文件不存在

**解决**:
```bash
# 检查 summary.md 文件是否存在
ls dataset/interpretations/*/summary.md

# 如果不存在，重新生成
python scripts/generate_summaries.py
```

### API 相关

#### ❌ 错误: "OpenAI API key not found"

**原因**: 环境变量未设置

**解决**: 参考 [环境配置](#环境配置) 设置 `OPENAI_API_KEY`

#### ❌ 错误: "Rate limit exceeded"

**原因**: OpenAI API 调用频率过高

**解决**: 等待几分钟后重试，或升级 API 计划

### Reranker 相关

#### ❌ 错误: "Model not found: BAAI/bge-reranker-base"

**原因**: 首次使用需要下载模型（约 1.1GB）

**解决**: 确保网络畅通，首次运行会自动下载：
```bash
python scripts/reranker.py --warmup
```

### 依赖相关

#### ❌ 错误: "No module named 'chromadb'"

**原因**: 依赖未安装

**解决**:
```bash
pip install -r requirements.txt
```

---

## 开发指南

### 新样本录入 SOP

详见 `specs/002-rag-data-migration/new-sample-sop.md`

```bash
# 1. 初始化目录
python scripts/init_new_sample.py --sample-id SSBR-072

# 2. 在 Excel 中添加元数据

# 3. 使用 Skills 生成解读文档
# @ssbr-mechanical-interpretation 请解读 SSBR-072 的力学数据

# 4. 生成综合档案
python scripts/generate_summaries.py --sample SSBR-072

# 5. 更新向量缓存
python scripts/build_vector_cache.py
```

### 代码规范

- Python: PEP 8
- YAML: 2 空格缩进，字符串用双引号
- Markdown: 标准 CommonMark

### 相关文档

| 文档 | 路径 |
|------|------|
| 数据模型 | `specs/002-rag-data-migration/data-model.md` |
| YAML Schema | `specs/002-rag-data-migration/contracts/yaml-schema.md` |
| 检索接口 | `specs/002-rag-data-migration/contracts/search-api.md` |
| 问答系统设计 | `specs/003-rag-qa-enhancement/spec.md` |

---

## 许可证

本项目仅用于学术研究和毕业设计演示。

---

*SSBR 官能化知识库 · RAG 语义检索系统 · 2026*
