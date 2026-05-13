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
│   ├── qa_engine.py                 # 问答引擎主入口
│   ├── rag_search.py                # RAG 检索核心
│   ├── answer_generator.py          # GPT 回答生成
│   ├── reranker.py                  # 交叉编码器重排
│   ├── quality_scorer.py            # 样本质量评估
│   ├── models.py                    # 数据类定义
│   ├── build_vector_cache.py        # 向量缓存构建
│   ├── build_quality_cache.py       # 质量缓存构建
│   ├── generate_summaries.py        # 批量生成 summary.md
│   ├── init_new_sample.py           # 新样本初始化
│   ├── import_metadata.py           # 元数据导入
│   ├── zotero_bridge.py             # Zotero 桥接工具
│   ├── utils/                       # 工具函数库
│   │   ├── vector_store.py          # ChromaDB 向量存储
│   │   ├── embedding.py             # Embedding 服务
│   │   ├── yaml_parser.py           # YAML 解析
│   │   ├── excel_handler.py         # Excel 读写
│   │   ├── prompt_templates.py      # Prompt 模板
│   │   └── ...
│   ├── synthesis/                   # 多文献综合模块
│   │   ├── aggregator.py            # 样本聚合
│   │   ├── trend_analyzer.py        # 趋势分析
│   │   ├── extrapolator.py          # 外推估计
│   │   ├── formula_designer.py      # 配方设计
│   │   └── ...
│   ├── evaluation/                  # 评测模块
│   │   └── ragas_evaluator.py       # RAGAS 评测
│   └── archive/                     # 归档的临时脚本
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

## Scripts 模块详解

### 核心模块依赖关系

```
qa_engine.py (主入口)
├── rag_search.py (检索)
│   └── utils/vector_store.py (ChromaDB)
│   └── utils/embedding.py (OpenAI Embedding)
├── reranker.py (重排)
├── quality_scorer.py (质量评估)
├── answer_generator.py (GPT生成)
│   └── utils/prompt_templates.py
└── synthesis/ (多文献综合)
    ├── aggregator.py
    ├── trend_analyzer.py
    └── extrapolator.py
```

### utils/ - 工具函数库

| 文件 | 用途 |
|------|------|
| `yaml_parser.py` | YAML front matter 解析 |
| `excel_handler.py` | Excel 数据读写 (数据.xlsx) |
| `embedding.py` | OpenAI Embedding API 封装 |
| `similarity.py` | 余弦相似度计算、相关性分类 |
| `validators.py` | 数据验证（样本ID、YAML字段） |
| `query_preprocessor.py` | 查询预处理（分词、同义词扩展） |
| `vector_store.py` | ChromaDB 向量存储封装 |
| `vector_cache.py` | 向量缓存管理（性能优化） |
| `prompt_templates.py` | GPT Prompt 模板 |
| `exceptions.py` | 自定义异常类 |
| `llm_client.py` | LLM API 客户端封装 |
| `curve_validator.py` | 曲线数据验证 |

### synthesis/ - 多文献综合模块

实现多文献综合推理功能 (Feature 004)。

| 文件 | 用途 |
|------|------|
| `aggregator.py` | 样本聚合器 - 提取和聚合多个样本摘要 |
| `trend_analyzer.py` | 趋势分析器 - 识别数据趋势和规律 |
| `extrapolator.py` | 外推估计器 - 保守外推（50%边界） |
| `formula_designer.py` | 配方设计器 - 根据目标性能生成配方建议 |
| `comparison_table.py` | 对比表格生成器 - 多方案结构化对比 |
| `citation_validator.py` | 引用验证器 - 验证和格式化引用 |
| `hallucination_validator.py` | 幻觉验证器 - 确保数据可追溯 |

### evaluation/ - 评测模块

| 文件 | 用途 |
|------|------|
| `ragas_evaluator.py` | RAGAS 评测框架 - 评估检索和生成质量 |

### 批处理脚本

| 文件 | 用途 |
|------|------|
| `batch_generate_docs.py` | 批量生成解读文档 |
| `batch_interpret.py` | 批量调用解读 Skill |
| `batch_migrate_v2.py` | 批量迁移到 v2 格式 |
| `standardize_summaries.py` | 标准化 summary 格式 |
| `migrate_excel_data.py` | Excel 数据迁移 |
| `validate_migration.py` | 验证迁移结果 |

### archive/ - 归档脚本

包含 57 个已归档的临时脚本（一次性数据检查、修复脚本），不再日常使用。

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

### 许可证

本项目仅用于学术研究和毕业设计演示。

---

*SSBR 官能化知识库 · RAG 语义检索系统 · 2026*

---

### 新机器启动项目改动说明：

本节说明：当前部署在 `E:\桌面\SSBR` 的本机版项目，相比这份原始 README 对应的 GitHub 原项目，实际做过哪些代码、配置、脚本、文档和评测产物改动；这些改动哪些属于功能增强，哪些只是为了让项目能在 Windows 本机成功部署和稳定运行。

#### 1. 总体判断

这次改动不是单纯“让项目能在我的电脑上启动”的临时改动，而是分为三类：

| 改动类别 | 是否改变原项目功能 | 说明 |
|---|---|---|
| 本机部署适配 | 基本不改变原业务功能 | 让项目能在 Windows、PowerShell、`.venv`、阿里云百炼 OpenAI-compatible API、DashScope embedding 环境下稳定运行。 |
| RAG 链路增强 | 会增强原项目能力 | 增加多 embedding backend、Markdown chunk 切分、向量库统计、metadata、RAGAS qwen 兼容等能力，使检索、问答、评测更完整。 |
| 诊断与验收工具 | 不改变问答输出逻辑 | 新增 doctor、smoke test、一键脚本和本地运行文档，方便新机器复现部署、检查问题和做最小验收。 |

结论：这些改动既包含“本机成功部署运行所必需的适配”，也包含“让 RAG 流程更完整、更可验证、更接近原作者预期运行效果的功能增强”。没有使用 fake embedding、random embedding、mock API、硬编码检索结果或硬编码 LLM 回答。

#### 2. 已修改的项目文件

| 文件 | 改动类型 | 具体改动 | 对原项目的功能变化 |
|---|---|---|---|
| `.env.example` | 配置模板增强 | 增加 OpenAI-compatible、DashScope、本地 embedding、RAG chunk、Gradio 端口等配置示例。 | 功能增强 + 部署适配。原项目更偏 OpenAI 配置，现在新机器可按模板切换不同模型供应商。 |
| `demo/app.py` | 本机部署适配 | 支持从 `.env` 读取 `GRADIO_SERVER_PORT`。 | 主要是部署适配。Web UI 功能不变，但端口可配置，避免端口冲突。 |
| `scripts/utils/llm_client.py` | LLM 接入增强 | 支持 OpenAI-compatible `base_url` 与 `.env` 模型名，适配阿里云百炼兼容接口；当前验证模型为 `qwen3.6-flash`。 | 功能增强。原项目主要按 OpenAI 方式调用，现在可走百炼兼容接口。 |
| `scripts/utils/embedding.py` | Embedding 链路增强 | 新增 `EMBEDDING_BACKEND`，支持 `openai`、`openai_compatible`、`dashscope`、`local`；支持读取 `EMBEDDING_MODEL`、`EMBEDDING_API_KEY`、`EMBEDDING_BASE_URL`、`LOCAL_EMBEDDING_MODEL`、`LOCAL_EMBEDDING_DEVICE`。 | 功能增强。原项目 embedding 更容易卡在 OpenAI Key，现在可使用 DashScope embedding 或本地 sentence-transformers。 |
| `scripts/utils/vector_store.py` | 向量库与 chunk 增强 | 增加 Markdown chunk 切分、chunk metadata、ChromaDB 统计、向量维度一致性处理。 | 功能增强。原项目偏整篇 `summary.md` 入库，现在可细粒度检索，chunk 数明显多于文档数。 |
| `scripts/build_vector_cache.py` | 向量库构建增强 | 构建时输出原始文档数、chunk 数、平均/最大/最小 chunk 长度，并支持强制重建验证。 | 功能增强 + 部署验收。更容易判断向量库是否真实构建成功。 |
| `scripts/rag_search.py` | 检索链路增强 | 适配新的 embedding/vector store 配置；search-only 能输出真实来源、分数和片段。 | 功能增强。方便判断检索结果是否来自知识库，而不是模型自由发挥。 |
| `scripts/qa_engine.py` | 问答链路适配 | 统一使用新的 embedding、检索和 LLM 配置；保留 search-only 与完整问答两种路径。 | 主要是稳定性增强。业务目标不变，但链路更可验证。 |
| `scripts/reranker.py` | 重排验证增强 | 保留 `BAAI/bge-reranker-base` 完整模型，增强 warmup、日志和失败提示。 | 部署适配 + 可靠性增强。避免 reranker 失败时被静默当作成功。 |
| `scripts/evaluation/ragas_evaluator.py` | RAGAS 评测增强 | RAGAS LLM 不再硬编码 `gpt-4o-mini`，改为读取 `RAGAS_OPENAI_MODEL` 或 `OPENAI_MODEL`；RAGAS embedding 读取 `RAGAS_EMBEDDING_MODEL` 或 `EMBEDDING_MODEL`；适配 `qwen3.6-flash`；修复 qwen 偶发结构化输出不符合 RAGAS `StringIO` 解析器的问题；清理 `nan` 与 `0.000` 显示问题。 | 功能增强。原项目 RAGAS 默认更偏 OpenAI/gpt-4o-mini，现在可用百炼模型完成真实评测。 |
| `evaluation/ragas_reports/synthesis_report.md` | 评测产物 | 运行 RAGAS 后生成/更新 Markdown 报告。 | 不是源码功能改动，是验收结果文件。 |
| `evaluation/ragas_reports/synthesis_report.csv` | 评测产物 | 运行 RAGAS 后生成/更新 CSV 报告。 | 不是源码功能改动，是验收结果文件。 |
| `README.md` | 文档更新 | 项目内 README 曾追加本机适配说明。 | 文档改动，不影响运行。当前这份新 README 是以桌面原始 README 为底稿重新追加说明。 |

#### 3. 新增的项目文件

| 文件 | 用途 | 属于功能增强还是部署适配 |
|---|---|---|
| `README_LOCAL_RUN.md` | 本地运行、配置、排错、推荐命令说明。 | 部署适配文档。 |
| `scripts/doctor.py` | 一键检查 Python、虚拟环境、依赖、`.env`、embedding、LLM、reranker、dataset、ChromaDB、search-only、Web UI 入口。 | 诊断工具，不改变原问答功能。 |
| `scripts/smoke_test.py` | 最小 RAG 验收：文档数量、chunk 数量、向量数量、检索 top-k、reranker 状态、LLM 状态。 | 验收工具，不改变原问答功能。 |
| `run_build_index.ps1` | Windows 下一键重建向量库。 | 部署适配脚本。 |
| `run_search_test.ps1` | Windows 下一键执行 search-only 检索测试。 | 部署适配脚本。 |
| `run_qa_test.ps1` | Windows 下一键执行完整问答测试。 | 部署适配脚本。 |
| `run_app.ps1` | Windows 下一键启动 Gradio Web UI。 | 部署适配脚本。 |
| `run_all_check.ps1` | Windows 下一键执行 doctor、构建索引、reranker warmup、检索测试、问答测试。 | 部署适配 + 验收脚本。 |

#### 4. 本机生成但不属于核心源码的内容

| 文件或目录 | 说明 | 是否建议提交到 Git |
|---|---|---|
| `.env` | 本机真实 API Key 与模型配置文件。真实 Key 不应写入 README 或代码。 | 不建议提交。 |
| `.cache/chroma_db` | 本机生成的 ChromaDB 向量库。当前已验证向量数为 850。 | 通常不提交，新机器重新构建。 |
| Hugging Face 模型缓存 | reranker 模型缓存，例如 `~/.cache/huggingface/`。 | 不提交，新机器按需下载或复用缓存。 |
| `scripts/evaluation/evaluation/` | 早期运行评测时生成的额外输出目录，不是核心代码。 | 不建议作为核心改动提交，可确认后清理。 |
| `desktop.ini` | Windows 系统自动生成文件。 | 不建议提交。 |

#### 5. 真正带来功能变化的改动

以下改动属于“功能增强”，不只是为了启动项目：

1. Embedding 后端从单一 OpenAI 扩展为多后端。
2. 支持 DashScope / 阿里云百炼 embedding。
3. 支持本地 sentence-transformers embedding 作为兜底方案。
4. 文档入库从偏整篇 `summary.md` 入库，增强为 Markdown chunk 切分。
5. ChromaDB metadata 更完整，检索结果更容易追踪到 `source_file`、`sample_id`、`section_heading`、`chunk_id`。
6. 构建向量库时能报告文档数、chunk 数、向量数和 chunk 长度统计。
7. search-only 能返回真实 top-k 检索结果，便于独立验证检索链路。
8. RAGAS 评测可使用 `.env` 中的百炼 qwen 模型，而不是固定 `gpt-4o-mini`。
9. RAGAS 对 qwen 结构化输出不稳定做了兼容处理，避免合法 JSON 因格式包装差异导致评分失败。
10. 检索、问答、重排、评测都增加了更清晰的日志和失败提示。

这些增强不会改变项目的领域目标：项目仍然是 SSBR 官能化方案 RAG 问答/推荐系统。

#### 6. 主要只是为了本机部署运行的改动

以下改动主要是为了让项目在你的电脑上更容易跑通，不改变原项目核心业务逻辑：

1. `demo/app.py` 支持通过 `GRADIO_SERVER_PORT` 配置端口。
2. 新增 PowerShell 一键脚本，减少手动输入长命令。
3. 新增 `README_LOCAL_RUN.md`，整理本地运行步骤。
4. 新增 `scripts/doctor.py` 和 `scripts/smoke_test.py` 作为检查和验收工具。
5. `.env.example` 增加本机配置模板。
6. RAGAS 报告文件作为最近一次验收记录保存。

#### 7. 当前本机已验证的运行效果

当前在 `E:\桌面\SSBR` 已验证：

```text
[PASS] 虚拟环境可用
[PASS] requirements 已安装
[PASS] pip check 无依赖冲突
[PASS] 阿里云百炼 / DashScope LLM 可调用
[PASS] DashScope embedding 可调用
[PASS] ChromaDB 向量库可构建
[PASS] summary.md 文档数为 67
[PASS] Markdown chunk 数为 850
[PASS] ChromaDB 向量数为 850
[PASS] search-only 可返回真实检索结果
[PASS] reranker 模型可 warmup
[PASS] qa_engine 可基于检索结果生成回答
[PASS] Gradio Web UI 可启动
[PASS] RAGAS 评测可运行并生成报告
```

最近一次 RAGAS 统计结果：

```text
样本数: 12
faithfulness: avg=0.193, missing=0, nan=0
answer_relevancy: avg=0.402, missing=0, nan=0
context_precision: avg=0.017, missing=0, nan=0
context_recall: avg=0.243, missing=0, nan=0
citation_accuracy: avg=1.000, missing=0, nan=0
recommendation_completeness: avg=1.000, missing=0, nan=0
```

#### 8. 新机器启动时需要重新生成或重新配置的内容

如果把项目复制到另一台新电脑，真正必须重新准备的是：

1. `.env`
   - 新机器需要重新填写 API Key、base URL、模型名。
   - 不要把真实 API Key 写进代码或 README。

2. `.cache/chroma_db`
   - 这是本机向量库目录。
   - 新机器建议执行 `scripts/build_vector_cache.py --force` 重新构建。

3. reranker 模型缓存
   - `BAAI/bge-reranker-base` 会缓存在用户目录，例如 `~/.cache/huggingface/`。
   - 新机器首次运行可能需要重新下载。

4. Python 虚拟环境 `.venv`
   - 新机器应重新创建，避免复制旧机器环境导致路径或依赖异常。

#### 9. 新机器推荐启动命令

在新机器上，推荐按下面顺序执行：

```powershell
cd E:\桌面\SSBR
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

创建 `.env`，至少填写：

```env
OPENAI_API_KEY=你的百炼或 OpenAI-compatible Key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen3.6-flash

EMBEDDING_BACKEND=dashscope
EMBEDDING_MODEL=text-embedding-v4
EMBEDDING_API_KEY=你的百炼或 DashScope Key
EMBEDDING_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

RAG_CHUNK_MODE=markdown
RAG_CHUNK_SIZE=800
RAG_CHUNK_OVERLAP=120
GRADIO_SERVER_PORT=7861
```

然后执行：

```powershell
.\run_all_check.ps1
.\run_app.ps1
```

如果不用一键脚本，也可以手动执行核心命令：

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\doctor.py
.\.venv\Scripts\python.exe -X utf8 scripts\build_vector_cache.py --force
.\.venv\Scripts\python.exe -X utf8 scripts\reranker.py --warmup
.\.venv\Scripts\python.exe -X utf8 scripts\qa_engine.py --query "改善白炭黑分散性" --search-only --top-k 3
.\.venv\Scripts\python.exe -X utf8 scripts\qa_engine.py --query "如何改善白炭黑分散性？" --top-k 3
.\.venv\Scripts\python.exe -X utf8 demo\app.py
```

结论：源码中的这些改动是为了让项目在新机器上可重复部署、可诊断、可验证；其中 embedding、chunk、RAGAS qwen 兼容属于真实功能增强，PowerShell 脚本、doctor、smoke test、端口配置等主要属于本机部署和验收便利化改动。
