# SSBR 官能化方案智能推荐系统

基于 RAG 语义检索的绿色轮胎材料解决方案推荐系统，用于毕业设计项目演示。

## 项目简介

本系统构建了一个 SSBR（溶聚丁苯橡胶）官能化改性知识库，通过语义检索技术，根据用户的研究需求智能推荐最相关的官能化方案。

### 核心功能

- **语义检索推荐**：基于 OpenAI Embedding API 的 RAG 检索系统
- **多维度数据解读**：力学、热学、核磁、TEM 四类专业解读文档
- **AI Skills 辅助**：11 个专用 Skill 支持数据解读和文档生成
- **Web 演示界面**：Gradio 构建的交互式推荐系统

### 数据规模

- **13 个样本**：来自 4 篇文献的官能化 SSBR 配方
- **65 篇解读文档**：每个样本 5 个文档（力学、热学、核磁、TEM、综合档案）
- **覆盖官能团**：羟基、羧基、硅氧烷、oxa-Michael 等

## 安装

### 环境要求

- Python 3.9+
- OpenAI API Key（用于 Embedding 服务）

### 依赖安装

```bash
pip install gradio openai pandas openpyxl pyyaml numpy
```

### 环境配置

设置 OpenAI API：

```bash
# Windows
set OPENAI_API_KEY=your-api-key
set OPENAI_BASE_URL=https://api.openai.com/v1

# Linux/Mac
export OPENAI_API_KEY=your-api-key
export OPENAI_BASE_URL=https://api.openai.com/v1
```

## 快速启动

### 启动 Web Demo

```bash
python demo/app.py
```

然后在浏览器中打开 http://localhost:7860

### 命令行检索

```bash
python scripts/rag_search.py --query "改善白炭黑分散性" --top-k 5
```

### 运行 RAG 评估

```bash
python scripts/evaluate_rag.py --top-k 5
```

评估报告将保存到 `evaluation/report.md`。

## 项目结构

```
SSBR/
├── dataset/
│   ├── 数据.xlsx                    # 元数据（样本基础信息）
│   └── interpretations/             # 解读文档库
│       ├── SSBR-XXX/                # 各样本目录
│       │   ├── mechanical.md        # 力学解读
│       │   ├── dsc.md              # 热学解读
│       │   ├── nmr.md              # 核磁解读
│       │   ├── tem.md              # TEM 解读
│       │   └── summary.md          # 综合档案（RAG 检索核心）
│       └── TEMPLATE_*.md            # 模板文件
│
├── demo/
│   ├── app.py                       # Gradio Web 应用
│   └── data_formatter.py            # 数据格式化工具
│
├── evaluation/
│   ├── test_queries.yaml            # 评估测试集
│   └── report.md                    # 评估报告
│
├── scripts/
│   ├── rag_search.py                # RAG 检索引擎
│   ├── evaluate_rag.py              # RAG 评估脚本
│   ├── generate_summaries.py        # 批量生成 summary.md
│   ├── init_new_sample.py           # 新样本初始化
│   ├── backfill_summary_metrics.py  # 性能指标回填
│   └── utils/                       # 工具函数库
│
├── skills/                          # CodeBuddy AI Skills
│   ├── ssbr-recommender/            # RAG 推荐 Skill
│   ├── ssbr-summary-generator/      # 综合档案生成 Skill
│   ├── ssbr-mechanical-interpretation/
│   ├── ssbr-stress-strain-interpretation/
│   ├── ssbr-payne-interpretation/
│   ├── ssbr-dma-interpretation/
│   ├── ssbr-dsc-interpretation/
│   ├── ssbr-nmr-interpretation/
│   └── ssbr-tem-interpretation/
│
├── specs/                           # 规范文档
│   ├── 001-ssbr-knowledge-recommender/
│   └── 002-rag-data-migration/
│
├── literature/                      # 原始文献 PDF
└── CODEBUDDY.md                     # 项目开发指南
```

## 使用方法

### 1. 查询推荐方案

在 Web 界面输入研究需求，例如：
- "改善白炭黑分散性"
- "降低轮胎滚动阻力"
- "提高湿地抓地力"

系统将返回语义最相关的官能化方案，按匹配度排序。

### 2. 查看方案详情

点击推荐结果可查看：
- 官能团结构和接枝方式
- 关键性能指标（力学、热学、动态性能）
- 文献来源和样本编号

### 3. 添加新样本

```bash
python scripts/init_new_sample.py --sample-id SSBR-018
```

然后按照 `specs/002-rag-data-migration/new-sample-sop.md` 完成数据录入。

## 技术架构

```
用户查询
    ↓
查询预处理 (query_preprocessor.py)
    ↓
Embedding 向量化 (OpenAI text-embedding-3-small)
    ↓
语义相似度计算 (cosine similarity)
    ↓
Top-K 结果排序
    ↓
格式化输出 (data_formatter.py)
```

## 数据来源

| 文献 | 样本范围 | 官能团类型 |
|------|----------|------------|
| Gao_2019 | SSBR-002~004 | 羟基、羧基、硅烷 |
| Qu_2014 | SSBR-006~008 | 羧基（不同含量） |
| Zhang_2018 | SSBR-010~012 | oxa-Michael 改性 |
| Wang_2018 | SSBR-014~017 | 羧基（不同含量） |

> 注：空白对照样本（SSBR-001, 005, 009, 013）已移除，仅保留官能化样本。

## 许可证

本项目仅用于学术研究和毕业设计演示。

---

*SSBR 官能化知识库 · RAG 语义检索系统 · 2026*
