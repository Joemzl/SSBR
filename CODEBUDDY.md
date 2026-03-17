# SSBR Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-14

## Active Technologies

- **数据格式**: Markdown + YAML front matter
- **脚本语言**: Python 3.x
- **AI Skills**: CodeBuddy IDE Skills
- **Embedding API**: OpenAI text-embedding-3-small (1536 维)
- **数据存储**: Excel (元数据 A-W 列) + Markdown (解读文档)
- **文献管理**: Zotero + MCP 集成（literature/ 目录作为 fallback）

## Project Structure

```text
dataset/
├── 数据.xlsx                    # 元数据 (A-W 列，23 列)
└── interpretations/             # 解读文档库
    ├── SSBR-XXX/                # 各样本目录 (动态)
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
├── import_metadata.py           # 元数据导入（从 AI 提取的 Markdown 表格）
├── zotero_bridge.py             # Zotero MCP 桥接工具
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
# 从 AI 提取的数据导入到 Excel（推荐工作流）
python scripts/import_metadata.py --file extracted_data.md --dry-run  # 预览
python scripts/import_metadata.py --file extracted_data.md            # 导入

# 初始化新样本
python scripts/init_new_sample.py --sample-id SSBR-018

# 生成所有样本的 summary.md
python scripts/generate_summaries.py

# 验证数据完整性
python scripts/update_vector_index.py --validate-only

# RAG 检索测试
python scripts/rag_search.py --query "改善白炭黑分散" --top-k 3

# Zotero 文献查询
python scripts/zotero_bridge.py search "10.1039/xxx"
python scripts/zotero_bridge.py list --with-pdf
```

## Code Style

- Python: PEP 8
- YAML: 2 空格缩进，字符串用双引号
- Markdown: 标准 CommonMark

## Recent Changes

- 002-rag-data-migration (2026-03-14):
  - 集成 Zotero MCP 用于文献管理
  - 新增 `import_metadata.py` 元数据导入脚本
  - 新增 `zotero_bridge.py` Zotero 桥接工具
  - Excel 扩展为 23 列新结构（A-W 列）
  - 更新 `excel_handler.py` 支持新列结构
  - DOI 列改为原始格式，DOI_SI 改为存在性标记

- 002-rag-data-migration (2026-03-07):
  - 移除空白对照样本，仅保留官能化样本
  - RAG 评估 Hit Rate@5 = 91.7%

- 002-rag-data-migration (2026-03-05):
  - 实现 RAG 语义检索推荐系统
  - 更新 8 个 Skills 输出格式为 YAML + Markdown
  - 新增 ssbr-summary-generator Skill
  - 新增新样本录入 SOP 和脚本

## Key Concepts

- **RAG 检索**: 基于 summary.md 内容的语义检索
- **解读文档**: YAML front matter (结构化数据) + Markdown 正文 (自然语言)
- **数据来源层级**: L1 (表格) > L2 (图面标注) > L3 (曲线估读)
- **零幻觉原则**: 所有数值必须来自文献，禁止编造
- **样本编号规则**: 样本 ID (如 SSBR-002) 是稀疏非连续的，文档中禁止硬编码样本总数或使用范围描述 (如 SSBR-001~017)
- **文献检索优先级**: Zotero MCP 优先 → literature/ 目录 fallback
- **元数据导入流程**: AI 提取 Markdown 表格 → import_metadata.py 导入 Excel

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
