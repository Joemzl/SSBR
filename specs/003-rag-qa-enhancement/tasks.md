# Tasks: RAG 问答系统增强

**Input**: Design documents from `/specs/003-rag-qa-enhancement/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/qa-api.md ✓

**Tests**: 不包含测试任务（规范中未要求 TDD）

**Organization**: 任务按用户故事组织，支持独立实现和测试。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行执行（不同文件，无依赖）
- **[Story]**: 所属用户故事（US1, US2, US3, US4）
- 描述中包含精确文件路径

## Path Conventions

基于 plan.md 的项目结构：
- **脚本模块**: `scripts/`
- **工具函数**: `scripts/utils/`
- **Web Demo**: `demo/`
- **缓存文件**: `.cache/`

---

## Phase 1: Setup（共享基础设施）

**Purpose**: 项目初始化和依赖配置

- [x] T001 更新 requirements.txt 添加 sentence-transformers>=2.2.0 依赖 in `requirements.txt`
- [x] T002 创建 Prompt 模板模块基础结构 in `scripts/utils/prompt_templates.py`
- [x] T003 [P] 创建 QA 系统异常类定义 in `scripts/utils/exceptions.py`

---

## Phase 2: Foundational（阻塞性前置条件）

**Purpose**: 所有用户故事依赖的核心基础设施

**⚠️ CRITICAL**: 用户故事工作必须在此阶段完成后才能开始

- [x] T004 实现数据类定义（Query, Candidate, RankedResult, Citation, GeneratedAnswer, QualityScore）in `scripts/models.py`
- [x] T005 [P] 实现 QualityScorer 质量评估模块 in `scripts/quality_scorer.py`
- [x] T006 [P] 实现 Reranker 重排模块（加载 bge-reranker-base）in `scripts/reranker.py`
- [x] T007 实现 AnswerGenerator 回答生成模块 in `scripts/answer_generator.py`
- [x] T008 构建质量分数缓存（预计算 82 个样本的 QualityScore）in `.cache/quality_scores.json`

**Checkpoint**: 基础模块就绪 - 用户故事实现可以开始

---

## Phase 3: User Story 1 - 自然语言问答 (Priority: P1) 🎯 MVP

**Goal**: 用户输入问题后，系统基于检索样本生成 300-500 字的专业回答，包含引用

**Independent Test**: 输入"如何改善白炭黑分散性？"验证返回包含具体建议、数据支撑和文献引用的自然语言回答

### Implementation for User Story 1

- [x] T009 [US1] 创建 QAEngine 主类框架 in `scripts/qa_engine.py`
- [x] T010 [US1] 实现 QAEngine.answer() 主方法（检索→质量评估→重排→生成）in `scripts/qa_engine.py`
- [x] T011 [US1] 实现 AnswerType 判定逻辑（DIRECT/REFERENCE/GUIDANCE 基于相似度阈值 0.5/0.7）in `scripts/qa_engine.py`
- [x] T012 [US1] 实现生成回答的 Prompt 模板（System Prompt + User Prompt）in `scripts/utils/prompt_templates.py`
- [x] T013 [US1] 实现引用提取和验证逻辑（确保所有引用可追溯到样本 ID）in `scripts/answer_generator.py`
- [x] T014 [US1] 实现回答后处理（长度检查、引用格式化、置信度标注）in `scripts/answer_generator.py`

**Checkpoint**: User Story 1 完成 - 可独立测试自然语言问答功能

---

## Phase 4: User Story 2 - 重排优化检索精度 (Priority: P2)

**Goal**: 对 Top-10 候选结果进行交叉编码器重排，将最相关样本提升到前列

**Independent Test**: 对比有/无重排时的检索结果排序，验证重排后更相关样本排名更靠前

### Implementation for User Story 2

- [x] T015 [US2] 优化 Reranker 模块支持批量重排（Top-10 → Top-3）in `scripts/reranker.py`
- [x] T016 [US2] 实现重排分数与原始相似度的融合策略 in `scripts/reranker.py`
- [x] T017 [US2] 添加重排模型懒加载和预热机制 in `scripts/reranker.py`
- [x] T018 [US2] 集成重排到 QAEngine 流程（插入在向量检索和生成之间）in `scripts/qa_engine.py`
- [x] T019 [US2] 添加重排性能监控（rerank_time_ms 指标）in `scripts/qa_engine.py`

**Checkpoint**: User Story 2 完成 - 重排功能可独立验证

---

## Phase 5: User Story 3 - 低质量匹配的优雅处理 (Priority: P2)

**Goal**: 当所有结果相似度 < 0.5 时，生成引导性回答而非"未找到"

**Independent Test**: 输入与现有样本无关的查询，验证返回有帮助的引导性回答

### Implementation for User Story 3

- [x] T020 [US3] 实现 GUIDANCE 类型回答的 Prompt 模板 in `scripts/utils/prompt_templates.py`
- [x] T021 [US3] 实现引导性回答生成逻辑（问题分析 + 通用建议 + 查询优化提示）in `scripts/answer_generator.py`
- [x] T022 [US3] 添加相似度阈值检测和回答类型自动切换 in `scripts/qa_engine.py`
- [x] T023 [US3] 实现 REFERENCE 类型回答（0.5-0.7 相似度）的"仅供参考"声明 in `scripts/answer_generator.py`
- [x] T024 [US3] 处理边缘情况：检索结果为空、非技术性查询、生成异常 in `scripts/qa_engine.py`

**Checkpoint**: User Story 3 完成 - 低质量匹配场景可独立验证

---

## Phase 6: User Story 4 - 保留原有推荐列表功能 (Priority: P3)

**Goal**: 同时展示生成回答和样本列表，支持模式切换

**Independent Test**: 同一查询验证系统同时返回生成回答和样本列表两部分内容

### Implementation for User Story 4

- [x] T025 [US4] 扩展 demo/app.py 添加问答 UI 组件（AI 回答区域）in `demo/app.py`
- [x] T026 [US4] 实现 search_and_answer() 函数（返回回答 + 样本列表）in `demo/app.py`
- [x] T027 [US4] 添加"检索并生成回答"和"仅检索推荐"两个按钮 in `demo/app.py`
- [x] T028 [US4] 实现显示模式切换（只看回答/只看列表/两者都看）in `demo/app.py`
- [x] T029 [US4] 添加性能统计展示（检索耗时、重排耗时、生成耗时、总耗时）in `demo/app.py`
- [x] T030 [US4] 保持原有 search_samples() 接口向后兼容 in `demo/app.py`

**Checkpoint**: User Story 4 完成 - Web UI 可独立验证

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 跨用户故事的改进和优化

- [x] T031 [P] 添加 QAEngine 启动时重排模型预加载（减少首次查询延迟）in `demo/app.py`
- [x] T032 [P] 优化错误处理：GPT API 失败时回退到纯推荐模式 in `scripts/qa_engine.py`
- [x] T033 [P] 添加配置管理（环境变量：QA_MODEL, QA_MAX_TOKENS, RERANK_TOP_K）in `scripts/qa_engine.py`
- [x] T034 运行 quickstart.md 验证流程确认所有功能正常 in `specs/003-rag-qa-enhancement/quickstart.md`
- [x] T035 [FR-011] 网页界面隐藏数据库内部信息（样本ID、分数），转换为用户友好描述 in `demo/app.py`, `scripts/utils/prompt_templates.py`, `scripts/answer_generator.py`

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ← BLOCKS all user stories
    │
    ├──────────────────────────────────┐
    ▼                                  ▼
Phase 3 (US1: P1) 🎯 MVP         可并行开始其他故事
    │                                  │
    ▼                                  ▼
Phase 4 (US2: P2)              Phase 5 (US3: P2)
    │                                  │
    └──────────────┬───────────────────┘
                   ▼
             Phase 6 (US4: P3) ← 依赖 US1 完成
                   │
                   ▼
             Phase 7 (Polish)
```

### User Story Dependencies

| User Story | 优先级 | 依赖 | 可并行 |
|------------|--------|------|--------|
| US1 自然语言问答 | P1 | Phase 2 | ✅ MVP |
| US2 重排优化 | P2 | Phase 2, 可与 US1 并行 | ✅ |
| US3 低质量处理 | P2 | Phase 2, 可与 US1 并行 | ✅ |
| US4 UI 扩展 | P3 | US1 完成 | 需要 US1 |

### Within Each User Story

- 数据类定义 → 服务实现 → 引擎集成 → UI 展示
- 核心实现 → 边缘情况处理

### Parallel Opportunities

**Phase 2 内部可并行**:
```bash
# 同时启动（不同文件，无依赖）:
Task T005: "实现 QualityScorer 质量评估模块 in scripts/quality_scorer.py"
Task T006: "实现 Reranker 重排模块 in scripts/reranker.py"
```

**User Story 2 和 3 可并行**:
```bash
# US2 和 US3 优先级相同，可同时开发:
Developer A: Phase 4 (US2 重排优化)
Developer B: Phase 5 (US3 低质量处理)
```

---

## Parallel Example: Phase 2

```bash
# 数据类定义完成后，可并行启动:
Task T005: "实现 QualityScorer 质量评估模块 in scripts/quality_scorer.py"
Task T006: "实现 Reranker 重排模块 in scripts/reranker.py"

# T007 依赖 T005 的 QualityScore，需等待
```

## Parallel Example: User Story 1

```bash
# T009 完成后，以下可并行:
Task T012: "实现生成回答的 Prompt 模板 in scripts/utils/prompt_templates.py"
Task T013: "实现引用提取和验证逻辑 in scripts/answer_generator.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup（~15 分钟）
2. Complete Phase 2: Foundational（~2 小时）
3. Complete Phase 3: User Story 1（~2 小时）
4. **STOP and VALIDATE**: 测试自然语言问答功能
5. 可选：部署/演示 MVP

### Incremental Delivery

1. Setup + Foundational → 基础就绪
2. Add User Story 1 → 测试 → **MVP 交付!**
3. Add User Story 2 + 3（并行）→ 测试 → 增强版交付
4. Add User Story 4 → 测试 → 完整版交付
5. 每个故事独立增加价值，不破坏已有功能

### Suggested MVP Scope

**MVP = Phase 1 + Phase 2 + Phase 3 (User Story 1)**

- 核心问答功能可用
- 可演示自然语言回答生成
- 预估工时：4-5 小时

---

## Summary

| 项目 | 数值 |
|------|------|
| **总任务数** | 34 |
| **Phase 1 (Setup)** | 3 任务 |
| **Phase 2 (Foundational)** | 5 任务 |
| **US1 自然语言问答 (P1)** | 6 任务 |
| **US2 重排优化 (P2)** | 5 任务 |
| **US3 低质量处理 (P2)** | 5 任务 |
| **US4 UI 扩展 (P3)** | 6 任务 |
| **Phase 7 (Polish)** | 4 任务 |
| **可并行任务** | 12 任务（标记 [P]） |
| **MVP 范围** | Phase 1-3, 14 任务 |

---

## Notes

- [P] 任务 = 不同文件，无依赖，可并行
- [Story] 标签将任务映射到特定用户故事，便于追溯
- 每个用户故事应可独立完成和测试
- 每个任务或逻辑组完成后提交代码
- 可在任何检查点停止以独立验证故事
- 避免：模糊任务、同文件冲突、破坏独立性的跨故事依赖
