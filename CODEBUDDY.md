# SSBR Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-31

## Active Technologies
- Python 3.10+ (003-rag-qa-enhancement)
- ChromaDB 向量数据库 + Markdown 文档 + Excel 元数据 (003-rag-qa-enhancement)
- Python 3.10+ (与现有系统一致) (004-multi-literature-synthesis)
- ChromaDB 向量数据库 (`.cache/chroma_db/`) (004-multi-literature-synthesis)
- 全范围曲线数据捕捉 (005-full-range-data-capture)

- **数据格式**: Markdown + YAML front matter
- **脚本语言**: Python 3.x
- **AI Skills**: CodeBuddy IDE Skills
- **Embedding API**: OpenAI text-embedding-3-small (1536 维)
- **数据存储**: Excel (元数据 A-X 列) + Markdown (解读文档)
- **向量存储**: ChromaDB 持久化数据库 (`.cache/chroma_db/`)
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

.cache/
└── chroma_db/                   # ChromaDB 向量数据库（不提交 Git，跨设备需重建）

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
├── build_vector_cache.py        # 向量缓存构建脚本
├── build_quality_cache.py       # 质量分数缓存构建脚本
├── update_vector_index.py       # 向量索引更新
├── rag_search.py                # RAG 检索核心
├── qa_engine.py                 # 问答引擎核心（支持综合模式）
├── answer_generator.py          # GPT 回答生成模块
├── reranker.py                  # 交叉编码器重排模块
├── quality_scorer.py            # 样本质量评估模块
├── models.py                    # 数据类定义
├── synthesis/                   # 多文献综合模块 (004-multi-literature-synthesis)
│   ├── __init__.py
│   ├── aggregator.py            # 样本聚合器
│   ├── citation_validator.py    # 引用验证器
│   ├── trend_analyzer.py        # 趋势分析器
│   ├── extrapolator.py          # 外推估计器
│   ├── formula_designer.py      # 配方设计器
│   └── comparison_table.py      # 对比表格生成器
└── utils/                       # 工具函数
    ├── yaml_parser.py
    ├── excel_handler.py
    ├── embedding.py
    ├── similarity.py
    ├── validators.py
    ├── query_preprocessor.py
    ├── vector_store.py          # ChromaDB 向量存储模块
    ├── prompt_templates.py      # Prompt 模板
    ├── exceptions.py            # 异常类定义
    └── curve_validator.py       # 曲线数据验证模块 (005-full-range-data-capture)

specs/002-rag-data-migration/    # 规范文档
├── spec.md
├── plan.md
├── tasks.md
├── data-model.md
├── quickstart.md
├── new-sample-sop.md
└── contracts/
    ├── yaml-schema.md           # 已更新支持 curves 字段
    └── search-api.md

specs/005-full-range-data-capture/  # 全范围数据捕捉规范 (新增)
├── spec.md                      # 总体规范
├── plan.md                      # 实施计划
├── tasks.md                     # 任务清单
├── quickstart.md                # 快速入门指南
├── SKILL-stress-strain-v2.md    # 应力-应变 Skill v2
├── SKILL-dma-v2.md              # DMA Skill v2
├── SKILL-payne-v2.md            # Payne Skill v2
├── SKILL-dsc-v2.md              # DSC Skill v2
└── contracts/
    └── curve-data-schema.md     # 曲线数据 JSON Schema
```

## Commands

```bash
# 向量缓存管理
python scripts/build_vector_cache.py           # 增量更新缓存
python scripts/build_vector_cache.py --force   # 强制重建缓存
python scripts/build_vector_cache.py --stats   # 查看缓存状态

# 质量分数缓存管理
python scripts/build_quality_cache.py          # 构建质量分数缓存
python scripts/build_quality_cache.py --stats  # 查看质量统计

# 问答系统 (003-rag-qa-enhancement)
python scripts/qa_engine.py --query "如何改善白炭黑分散性？"  # 问答测试
python scripts/qa_engine.py --query "提高湿地抓地力" --search-only  # 仅检索
python scripts/qa_engine.py --warmup           # 预热所有组件

# 多文献综合模式 (004-multi-literature-synthesis)
python scripts/qa_engine.py --query "官能化程度如何影响性能？" --synthesize  # 综合问答
python scripts/qa_engine.py --compare "羟基官能化" "氨基官能化"              # 对比分析
python scripts/qa_engine.py --design "高湿地抓地力低滚阻" --target 湿地抓地力=高 滚动阻力=低  # 配方设计
python scripts/qa_engine.py --query "5%官能化的拉伸强度" --no-extrapolation   # 禁用外推

# 重排模块测试
python scripts/reranker.py --warmup            # 加载重排模型
python scripts/reranker.py --test              # 运行重排测试

# 从 AI 提取的数据导入到 Excel（推荐工作流）
python scripts/import_metadata.py --file dataset/extracted_data.md --dry-run  # 预览
python scripts/import_metadata.py --file dataset/extracted_data.md            # 导入

# 初始化新样本
python scripts/init_new_sample.py --sample-id SSBR-018

# 生成所有样本的 summary.md
python scripts/generate_summaries.py

# 验证数据完整性
python scripts/update_vector_index.py --validate-only

# RAG 检索测试
python scripts/rag_search.py --query "改善白炭黑分散" --top-k 3

# Web Demo 启动
python demo/app.py                             # 启动 http://localhost:7861

# RAGAS 评测 (004-multi-literature-synthesis)
python scripts/evaluation/ragas_evaluator.py --mode synthesis  # 评测综合分析
python scripts/evaluation/ragas_evaluator.py --mode single     # 评测单样本问答
python scripts/evaluation/ragas_evaluator.py --mode all        # 全部评测

# Zotero 文献查询
python scripts/zotero_bridge.py search "10.1039/xxx"
python scripts/zotero_bridge.py list --with-pdf

# 曲线数据验证 (005-full-range-data-capture)
python scripts/utils/curve_validator.py --file dataset/interpretations/SSBR-001/mechanical.md  # 单文件验证
python scripts/utils/curve_validator.py --dir dataset/interpretations/  # 批量验证
python scripts/utils/curve_validator.py --dir dataset/interpretations/ --quiet  # 静默模式
```

## Code Style

- Python: PEP 8
- YAML: 2 空格缩进，字符串用双引号
- Markdown: 标准 CommonMark

## Recent Changes

- 005-full-range-data-capture (2026-03-31):
  - **全范围数据捕捉**: 从"离散点提取"升级为"全范围曲线数据捕捉"
  - **曲线数据 Schema**: 定义 stress_strain, dma_tan_delta, payne_storage_modulus, dsc_heat_flow 四种曲线格式
  - **置信度分级**: L1 (表格 0.95) > L2 (标注 0.85) > L3 (估读 0.50-0.75)
  - **交叉验证**: 已知点偏差检查，质量分级 (excellent/good/acceptable/poor)
  - 新增 `specs/005-full-range-data-capture/` 规范目录
  - 新增 `scripts/utils/curve_validator.py` 曲线数据验证模块
  - 新增 v2.0 增强版 Skill 模板 (SKILL-stress-strain-v2.md, SKILL-dma-v2.md, SKILL-payne-v2.md, SKILL-dsc-v2.md)
  - 更新 `specs/002-rag-data-migration/contracts/yaml-schema.md` 支持 curves 字段
  - 数据丰富度目标: 应力-应变 5→15-20 点, DMA 3→15-20 点, Payne 4→10-15 点, DSC 1→10-15 点

- 004-multi-literature-synthesis (2026-03-25):
  - **多文献综合**: 从"单样本检索"升级为"多文献综合推理"
  - **趋势分析**: 从数据中提取规律和趋势
  - **保守外推**: 基于数据趋势进行有限范围的预测（50% 边界）
  - **对比分析**: 多方案结构化对比表格
  - **配方设计**: 根据目标性能生成配方建议
  - 新增 `scripts/synthesis/` 模块（aggregator, citation_validator, trend_analyzer, extrapolator, formula_designer, comparison_table）
  - 扩展 `scripts/models.py` 新增数据类（SynthesisMode, SampleSummary, DataRange, SynthesizedAnswer, TrendAnalysis, ExtrapolationResult, FormulaRecommendation, ComparisonTable）
  - 扩展 `scripts/qa_engine.py` 新增方法（synthesize, design_formula, compare）
  - 更新 `scripts/utils/prompt_templates.py` 新增综合 Prompt 模板
  - 扩展 `scripts/utils/exceptions.py` 新增异常类（InsufficientDataError, ExtrapolationBoundaryError, ConflictingTargetsError）
  - 更新 `demo/app.py` 支持四个 Tab（智能问答、综合分析、对比分析、配方设计）
  - 性能目标: 综合问答响应时间 ≤ 8 秒

- 003-rag-qa-enhancement (2026-03-19):
  - **问答系统**: 实现基于 GPT 的自然语言问答生成
  - **交叉编码器重排**: 集成 bge-reranker-base 提升检索精度
  - **样本质量评估**: 基于字段完整性的降权策略
  - **三级回答类型**: DIRECT (≥0.7) / REFERENCE (0.5-0.7) / GUIDANCE (<0.5)
  - 新增 `scripts/qa_engine.py` 问答引擎
  - 新增 `scripts/answer_generator.py` 回答生成器
  - 新增 `scripts/reranker.py` 重排模块
  - 新增 `scripts/quality_scorer.py` 质量评估模块
  - 新增 `scripts/models.py` 数据类定义
  - 新增 `scripts/utils/prompt_templates.py` Prompt 模板
  - 新增 `scripts/utils/exceptions.py` 异常类
  - 更新 `demo/app.py` 支持问答模式
  - 新增依赖: sentence-transformers>=2.2.0

- 002-rag-data-migration (2026-03-19):
  - **性能优化**: 实现向量缓存机制，查询延迟从 25-30秒 降至 1-2秒
  - 新增 `scripts/utils/vector_cache.py` 向量缓存模块
  - 新增 `scripts/build_vector_cache.py` 缓存构建脚本
  - 更新 `rag_search.py` 支持缓存模式
  - 更新 Web Demo 启动时预加载缓存
  - 可检索样本数增至 68 个

  - 新增「接枝反应基团SMILES」列（K列），Excel 扩展为 24 列
  - 更新高分子指纹描述符格式：使用 SMILES 替代中文名
  - 集成 Zotero MCP 用于文献管理
  - 新增 `import_metadata.py` 元数据导入脚本
  - 新增 `zotero_bridge.py` Zotero 桥接工具
  - 更新 `excel_handler.py` 支持新列结构
  - DOI 列改为原始格式，DOI_SI 改为存在性标记

  - 移除空白对照样本，仅保留官能化样本
  - RAG 评估 Hit Rate@5 = 91.7%

  - 实现 RAG 语义检索推荐系统
  - 更新 8 个 Skills 输出格式为 YAML + Markdown
  - 新增 ssbr-summary-generator Skill
  - 新增新样本录入 SOP 和脚本

## Key Concepts

- **RAG 检索**: 基于 summary.md 内容的语义检索
- **向量存储**: ChromaDB 持久化数据库，支持毫秒级 HNSW 近似最近邻搜索（⚠️ 不通过 Git 同步，跨设备需 `python scripts/build_vector_cache.py --force` 重建）
- **解读文档**: YAML front matter (结构化数据) + Markdown 正文 (自然语言)
- **数据来源层级**: L1 (表格) > L2 (图面标注) > L3 (曲线估读)
- **零幻觉原则**: 所有数值必须来自文献，禁止编造
- **样本编号规则**: 样本 ID (如 SSBR-002) 是稀疏非连续的，文档中禁止硬编码样本总数或使用范围描述 (如 SSBR-001~017)
- **文献检索优先级**: Zotero MCP 优先 → literature/ 目录 fallback
- **元数据导入流程**: AI 提取 Markdown 表格 → import_metadata.py 导入 Excel
- **综合推理模式**: SINGLE (单样本) / SYNTHESIS (多文献综合) / COMPARISON (对比分析) / FORMULA (配方设计)
- **外推边界规则**: 仅允许数据范围外 50% 的外推，外推结果必须标注置信度
- **全范围曲线数据**: 从图像中估读连续数据点（10-20个），存储在 YAML `curves` 字段中，支持 stress_strain、dma_tan_delta、payne_storage_modulus、dsc_heat_flow 四种曲线类型
- **曲线置信度规则**: L1 来源置信度 0.90-0.95，L2 来源 0.85，L3 估读 0.50-0.75；交叉验证偏差 <10% 为 good，<15% 为 acceptable

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
