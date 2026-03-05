# SSBR Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-05

## Active Technologies

- **数据格式**: Markdown + YAML front matter
- **脚本语言**: Python 3.x
- **AI Skills**: CodeBuddy IDE Skills
- **Embedding API**: OpenAI text-embedding-3-small (1536 维)
- **数据存储**: Excel (元数据) + Markdown (解读文档)

## Project Structure

```text
dataset/
├── 数据.xlsx                    # 元数据 (A-O 列)
└── interpretations/             # 解读文档库
    ├── SSBR-001/ ~ SSBR-017/   # 17 个样本目录
    │   ├── mechanical.md        # 力学解读
    │   ├── dsc.md              # 热学解读
    │   ├── nmr.md              # 核磁解读
    │   ├── tem.md              # TEM 解读
    │   └── summary.md          # 综合档案 (RAG 检索核心)
    └── TEMPLATE_*.md            # 模板文件

skills/
├── ssbr-recommender/            # RAG 推荐 Skill
├── ssbr-summary-generator/      # 综合档案生成 Skill
├── ssbr-mechanical-interpretation/  # 力学调度 Skill
├── ssbr-stress-strain-interpretation/
├── ssbr-payne-interpretation/
├── ssbr-dma-interpretation/
├── ssbr-dsc-interpretation/
├── ssbr-nmr-interpretation/
└── ssbr-tem-interpretation/

scripts/
├── generate_summaries.py        # 批量生成 summary.md
├── init_new_sample.py           # 新样本初始化
├── update_vector_index.py       # 向量索引更新
├── rag_search.py                # RAG 检索核心
└── utils/                       # 工具函数
    ├── yaml_parser.py
    ├── excel_handler.py
    ├── embedding.py
    ├── similarity.py
    ├── validators.py
    └── query_preprocessor.py

specs/002-rag-data-migration/    # 规范文档
├── spec.md
├── plan.md
├── tasks.md
├── data-model.md
├── quickstart.md
├── new-sample-sop.md
└── contracts/
    ├── yaml-schema.md
    └── search-api.md
```

## Commands

```bash
# 生成所有样本的 summary.md
python scripts/generate_summaries.py

# 初始化新样本
python scripts/init_new_sample.py --sample-id SSBR-018

# 验证数据完整性
python scripts/update_vector_index.py --validate-only

# RAG 检索测试
python scripts/rag_search.py --query "改善白炭黑分散" --top-k 3
```

## Code Style

- Python: PEP 8
- YAML: 2 空格缩进，字符串用双引号
- Markdown: 标准 CommonMark

## Recent Changes

- 002-rag-data-migration (2026-03-05):
  - 实现 RAG 语义检索推荐系统
  - 17 个样本全部生成 4 类解读文档 + summary.md
  - 更新 8 个 Skills 输出格式为 YAML + Markdown
  - 新增 ssbr-summary-generator Skill
  - 新增新样本录入 SOP 和脚本

## Key Concepts

- **RAG 检索**: 基于 summary.md 内容的语义检索
- **解读文档**: YAML front matter (结构化数据) + Markdown 正文 (自然语言)
- **数据来源层级**: L1 (表格) > L2 (图面标注) > L3 (曲线估读)
- **零幻觉原则**: 所有数值必须来自文献，禁止编造

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
