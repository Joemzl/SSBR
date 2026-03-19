# Implementation Plan: RAG 问答系统增强

**Branch**: `003-rag-qa-enhancement` | **Date**: 2026-03-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-rag-qa-enhancement/spec.md`

## Summary

将现有的 SSBR 推荐系统升级为问答系统，核心改进：
1. **回答生成**：使用 OpenAI GPT API 基于检索结果生成 300-500 字的专业回答
2. **重排优化**：集成 bge-reranker-base 交叉编码器提升检索精度
3. **低质量处理**：当最高相似度 < 0.5 时生成引导性回答
4. **质量评估**：基于字段完整性对样本降权而非排除

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: 
- 现有：OpenAI SDK, Gradio, NumPy, PyYAML
- 新增：`sentence-transformers`（bge-reranker-base）
**Storage**: JSON 向量缓存 + Markdown 文档 + Excel 元数据  
**Testing**: pytest（现有但未广泛使用）  
**Target Platform**: Windows 本地运行 / Gradio Web Demo  
**Project Type**: Web 应用（RAG 问答系统）  
**Performance Goals**: 
- 完整回答时间 < 5 秒
- 重排延迟 < 1 秒
- 引用准确率 100%
**Constraints**: 
- 本地优先，降低外部服务依赖
- 兼容现有 82 个 summary.md 文档
- 保持向后兼容（推荐列表模式）
**Scale/Scope**: 82 个文档，单用户本地使用

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| 原则 | 检查项 | 状态 | 说明 |
|------|--------|------|------|
| I. 真实性第一 | 生成回答必须基于文献数据 | ✅ PASS | FR-002 要求标注数据来源，FR-009 禁止编造 |
| I. 真实性第一 | 区分文献数据与一般建议 | ✅ PASS | FR-010 明确要求区分 |
| IV. 推荐严谨可控 | 无确凿不输出 | ✅ PASS | 低质量匹配时生成引导性回答而非虚假推荐 |
| IV. 推荐严谨可控 | 支撑必备 | ✅ PASS | 所有引用可追溯到样本 ID |
| VIII. 轻量化 | 最小依赖 | ✅ PASS | 仅新增 sentence-transformers 一个依赖 |
| VIII. 轻量化 | 本地优先 | ✅ PASS | bge-reranker 本地运行，GPT API 是已有依赖 |

**Gate Result**: ✅ 全部通过，无违规

## Project Structure

### Documentation (this feature)

```text
specs/003-rag-qa-enhancement/
├── plan.md              # 本文件
├── research.md          # Phase 0: 技术研究
├── data-model.md        # Phase 1: 数据模型
├── quickstart.md        # Phase 1: 快速开始指南
├── contracts/           # Phase 1: 接口契约
│   └── qa-api.md        # 问答 API 契约
└── tasks.md             # Phase 2: 任务分解（由 /speckit.tasks 生成）
```

### Source Code (repository root)

```text
scripts/
├── rag_search.py            # 现有：RAG 检索引擎（需扩展）
├── answer_generator.py      # 新增：回答生成模块
├── reranker.py              # 新增：重排模块
├── quality_scorer.py        # 新增：样本质量评估模块
└── utils/
    ├── embedding.py         # 现有：Embedding 服务
    ├── vector_cache.py      # 现有：向量缓存
    ├── similarity.py        # 现有：相似度计算
    └── prompt_templates.py  # 新增：Prompt 模板

demo/
├── app.py                   # 现有：Gradio Web Demo（需扩展）
└── data_formatter.py        # 现有：结果格式化（需扩展）
```

> **Note**: 单元测试（`tests/`）将在后续迭代中添加，本期以手动验证为主。

**Structure Decision**: 扩展现有 scripts/ 和 demo/ 结构，新增模块保持与现有代码风格一致。

## Complexity Tracking

无复杂性违规，本方案遵循轻量化原则。

---

## Constitution Check (Post-Design)

*Re-check after Phase 1 design completion.*

| 原则 | 检查项 | 状态 | 设计验证 |
|------|--------|------|----------|
| I. 真实性第一 | 生成回答基于文献数据 | ✅ PASS | Prompt 模板强制引用样本 ID，后处理验证引用有效性 |
| I. 真实性第一 | 区分文献数据与一般建议 | ✅ PASS | AnswerType 枚举区分 DIRECT/REFERENCE/GUIDANCE |
| IV. 推荐严谨可控 | 无确凿不输出 | ✅ PASS | GUIDANCE 类型回答不包含具体样本推荐 |
| IV. 推荐严谨可控 | 支撑必备 | ✅ PASS | Citation 实体强制关联 sample_id |
| V. 数据解读全面性 | 质量评估覆盖所有表征类型 | ✅ PASS | QualityScore 涵盖力学/热学/动态/官能化/文献5类 |
| VIII. 轻量化 | 最小依赖 | ✅ PASS | 仅新增 sentence-transformers |
| VIII. 轻量化 | 本地优先 | ✅ PASS | 重排模型本地运行，无新增外部服务 |
| VIII. 轻量化 | 结构清晰 | ✅ PASS | 新增模块职责单一，与现有代码风格一致 |

**Post-Design Gate Result**: ✅ 全部通过

---

## Artifacts Generated

| 文件 | 路径 | 说明 |
|------|------|------|
| research.md | `specs/003-rag-qa-enhancement/research.md` | 技术研究与选型 |
| data-model.md | `specs/003-rag-qa-enhancement/data-model.md` | 数据模型定义 |
| qa-api.md | `specs/003-rag-qa-enhancement/contracts/qa-api.md` | API 契约 |
| quickstart.md | `specs/003-rag-qa-enhancement/quickstart.md` | 快速开始指南 |

---

## Next Steps

执行 `/speckit.tasks` 生成任务分解（Phase 2）。
