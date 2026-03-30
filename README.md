# SSBR 官能化方案智能推荐系统

基于 RAG 语义检索的绿色轮胎材料解决方案推荐系统。

> 💡 **新用户？** 跳转到 [快速开始](#快速开始) 章节，**5 分钟**完成配置并运行！

---

> ## ⚠️ 新设备 / 首次使用必读
>
> 本项目有两个**必须在本地构建**的组件，不会通过 Git 同步：
>
> | 组件 | 存储位置 | 首次下载大小 | 构建命令 |
> |------|----------|--------------|----------|
> | **向量数据库** | `.cache/chroma_db/` | ~50 MB (生成) | `python scripts/build_vector_cache.py --force` |
> | **重排模型** | `~/.cache/huggingface/` | **~1.1 GB** | 首次运行时自动下载 |
>
> **请在克隆后按照 [快速开始](#快速开始) 完成初始化！**

---

## 目录

- [快速开始](#快速开始)
- [环境配置](#环境配置)
- [模型下载说明](#模型下载说明)
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

> ⏱️ **安装时间**: 首次安装约需 5-10 分钟，主要取决于 `sentence-transformers` 和 `chromadb` 的下载速度。

<details>
<summary>📦 主要依赖说明（点击展开）</summary>

| 依赖 | 版本 | 用途 | 大小 |
|------|------|------|------|
| `openai` | ≥1.0.0 | Embedding API (text-embedding-3-small) | ~1 MB |
| `chromadb` | ≥0.4.0 | 向量数据库 | ~50 MB |
| `sentence-transformers` | ==2.7.0 | 交叉编码器重排 (bge-reranker-base) | ~200 MB |
| `transformers` | ==4.40.0 | Hugging Face 模型库 | ~300 MB |
| `gradio` | ≥4.0.0 | Web Demo 界面 | ~50 MB |
| `openpyxl` | ≥3.1.0 | Excel 读写 | ~5 MB |
| `anthropic` | ≥0.18.0 | Claude API (问答生成，可选) | ~5 MB |

**⚠️ 注意**: `sentence-transformers` 和 `transformers` 版本必须严格匹配，否则模型加载会失败。

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

> **🔴 重要**：向量缓存（`.cache/chroma_db/`）**不会通过 Git 同步**，每台设备首次使用时必须重建。
>
> **此步骤会调用 OpenAI API**，请确保已配置 `OPENAI_API_KEY` 环境变量。

```bash
python scripts/build_vector_cache.py --force
```

预期输出：
```
============================================================
SSBR 向量缓存构建工具
============================================================

正在扫描 summary.md 文件...
  发现 68 个 summary.md 文件

正在构建向量缓存 (使用 ChromaDB)...
  处理进度: 100%|████████████████████████| 68/68 [00:45<00:00]

构建完成:
  总文档数: 68
  新增: 68
  耗时: 45.2 秒
  API 调用: ~68 次
  预估费用: < $0.01
```

**⏱️ 耗时**: 约 30-60 秒（取决于网络和 API 速度）

### 5. 🤖 预下载重排模型（推荐）

> **📦 模型大小**: `BAAI/bge-reranker-base` 约 **1.1 GB**
>
> 首次运行问答或检索功能时会自动下载。为避免首次使用时卡顿，建议提前下载：

```bash
python scripts/reranker.py --warmup
```

预期输出：
```
============================================================
Reranker 交叉编码器模块
============================================================

正在加载模型 BAAI/bge-reranker-base...
Downloading model.safetensors: 100%|██████████| 1.11G/1.11G [02:30<00:00]
模型加载完成！

设备: cuda (NVIDIA GeForce RTX 3060)  # 或 cpu
模型: BAAI/bge-reranker-base
预热完成，模型已就绪
```

**⏱️ 耗时**: 首次下载约 2-5 分钟（取决于网速），之后约 5-10 秒

**📁 模型存储位置**:
- Windows: `C:\Users\<用户名>\.cache\huggingface\hub\`
- Linux/Mac: `~/.cache/huggingface/hub/`

### 6. 启动 Web Demo

```bash
python demo/app.py
```

打开浏览器访问 http://localhost:7861

### 7. 验证安装

在 Web Demo 中尝试以下测试查询，验证系统是否正常工作：

| 测试查询 | 预期结果 |
|---------|----------|
| "改善白炭黑分散性" | 返回含硅烷偶联剂相关的样本 |
| "降低轮胎滚动阻力" | 返回低滞后损耗的官能化方案 |
| "提高湿地抓地力" | 返回高 tan δ (0°C) 的样本 |

如果能正常返回检索结果，说明安装成功！🎉

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

## 模型下载说明

本项目使用两个远程资源，首次运行时需要下载：

### 1. OpenAI Embedding API（在线调用）

- **模型**: `text-embedding-3-small`
- **维度**: 1536
- **调用方式**: 在线 API（需要 `OPENAI_API_KEY`）
- **费用**: ~$0.00002 / 1K tokens（非常便宜）
- **网络要求**: 需要能访问 `api.openai.com`（或配置 `OPENAI_BASE_URL` 代理）

### 2. 重排模型（本地下载）

- **模型**: `BAAI/bge-reranker-base`
- **大小**: **~1.1 GB**
- **存储位置**: `~/.cache/huggingface/hub/models--BAAI--bge-reranker-base/`
- **下载方式**: 首次调用时自动从 Hugging Face Hub 下载
- **网络要求**: 需要能访问 `huggingface.co`

#### 国内用户加速下载

如果下载速度慢，可以配置 Hugging Face 镜像：

```bash
# Windows (PowerShell)
$env:HF_ENDPOINT = "https://hf-mirror.com"

# Linux/Mac
export HF_ENDPOINT="https://hf-mirror.com"

# 然后运行
python scripts/reranker.py --warmup
```

#### 手动下载（离线环境）

```bash
# 安装 huggingface-cli
pip install huggingface_hub

# 下载模型到本地
huggingface-cli download BAAI/bge-reranker-base --local-dir ./models/bge-reranker-base

# 然后修改 scripts/reranker.py 中的模型路径
# model_name = "./models/bge-reranker-base"
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
├── .cache/                          # ⚠️ 缓存目录（不提交到 Git，需本地构建）
│   └── chroma_db/                   # ChromaDB 向量数据库
│       ├── chroma.sqlite3           # 元数据
│       └── [uuid]/                  # HNSW 索引文件
│
├── .gitignore                       # Git 忽略规则
├── CODEBUDDY.md                     # 开发指南（AI 生成）
├── README.md                        # 本文档
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
└── requirements.txt                 # Python 依赖
```

---

## 核心功能

### 1. 语义检索推荐

基于 OpenAI Embedding API 的 RAG 检索系统，从 68 个官能化样本中智能匹配最相关的方案。

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

## 新设备一键初始化

如果你是在**新设备**上首次使用本项目，可以按以下顺序执行：

```bash
# 1. 克隆项目
git clone <repository-url>
cd SSBR

# 2. 创建虚拟环境（推荐）
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. 安装依赖 (约 5-10 分钟)
pip install -r requirements.txt

# 4. 配置环境变量 (必须)
# Windows PowerShell:
$env:OPENAI_API_KEY = "sk-xxx"
# 可选：如果使用 Claude 进行问答生成
$env:ANTHROPIC_API_KEY = "sk-ant-xxx"

# 5. 构建向量缓存 (约 1 分钟)
python scripts/build_vector_cache.py --force

# 6. 预下载重排模型 (约 2-5 分钟，1.1GB)
python scripts/reranker.py --warmup

# 7. 启动 Web Demo
python demo/app.py
```

**完成后访问**: http://localhost:7861

---

## 数据规模

| 指标 | 数值 |
|------|------|
| 官能化样本数 | 68 |
| 解读文档数 | ~340 (每样本 5 个) |
| 文献来源 | 多篇 SCI 论文 |
| 覆盖官能团 | 羟基、羧基、氨基、环氧基、硅烷、胍基等 |
| 向量维度 | 1536 (text-embedding-3-small) |
| 向量数据库 | ChromaDB (HNSW 索引) |

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
| 新样本录入 | `specs/002-rag-data-migration/new-sample-sop.md` |

---

## 许可证

本项目仅用于学术研究和毕业设计演示。

---

*SSBR 官能化知识库 · RAG 语义检索系统 · 2026*
