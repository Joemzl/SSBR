# Tasks: RAG 推荐系统数据架构重构

**Input**: Design documents from `/specs/002-rag-data-migration/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests**: 未在规范中明确要求，本任务列表不包含测试任务。如需测试，可后续补充。

**Organization**: 任务按用户故事分组，支持独立实现和验证。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行执行（不同文件，无依赖）
- **[Story]**: 所属用户故事 (US1, US2, US3, US4, US5)
- 描述中包含精确文件路径

## Path Conventions

- **数据目录**: `dataset/`
- **解读文档**: `dataset/interpretations/`
- **Skills 目录**: `skills/`
- **迁移脚本**: `scripts/`
- **规范文档**: `specs/002-rag-data-migration/`

---

## Phase 1: Setup (基础设施)

**Purpose**: 项目初始化，创建必要的目录结构和脚本框架

- [x] T001 创建 scripts 目录结构 `scripts/`
- [x] T002 [P] 创建 Python 依赖文件 `scripts/requirements.txt`（含 openpyxl, pyyaml, openai, numpy）
- [x] T003 [P] 创建 17 个样本的解读文档目录 `dataset/interpretations/SSBR-001/` 至 `SSBR-017/`

---

## Phase 2: Foundational (阻塞性基础工作)

**Purpose**: 必须在所有用户故事之前完成的核心基础设施

**⚠️ CRITICAL**: 用户故事工作必须等此阶段完成后才能开始

- [x] T004 创建 YAML 解析工具函数 `scripts/utils/yaml_parser.py`
- [x] T005 [P] 创建 Excel 读写工具函数 `scripts/utils/excel_handler.py`
- [x] T006 [P] 创建 Embedding API 封装 `scripts/utils/embedding.py`（含错误处理和降级逻辑）
- [x] T007 [P] 创建余弦相似度计算工具 `scripts/utils/similarity.py`
- [x] T008 创建样本 ID 验证工具 `scripts/utils/validators.py`

**Checkpoint**: 基础工具库就绪，用户故事实现可以开始

---

## Phase 3: User Story 2 - 解读文档生成 (Priority: P1) 🎯 MVP

**Goal**: 为所有样本生成完整的 4 类解读文档（mechanical.md、dsc.md、nmr.md、tem.md）

**Independent Test**: 检查每个样本目录包含 nmr.md、tem.md、mechanical.md、dsc.md，内容符合模板规范

**Why First**: 这是实现新架构的基础，不完成解读文档其他故事无法进行

> **背景说明**: Excel 已经是瘦身状态（只有 A-O 列元数据），力学/热学数值数据需要通过调用解读 Skills 从文献图谱中提取

### Implementation for User Story 2

#### 2.1 模板与基础设施

- [x] T010 [US2] 创建批量解读调度脚本框架 `scripts/batch_interpret.py`
- [x] T011 [P] [US2] 创建 mechanical.md 模板文件 `dataset/interpretations/TEMPLATE_mechanical.md`
- [x] T012 [P] [US2] 创建 dsc.md 模板文件 `dataset/interpretations/TEMPLATE_dsc.md`
- [x] T012.1 [P] [US2] 创建 nmr.md 模板文件 `dataset/interpretations/TEMPLATE_nmr.md`
- [x] T012.2 [P] [US2] 创建 tem.md 模板文件 `dataset/interpretations/TEMPLATE_tem.md`

#### 2.2 解读文档生成（调用 Skills 从文献提取数据）

> **说明**: 以下任务需要手动调用对应的解读 Skills，AI 将从文献 PDF 中提取数据并生成标准化解读文档

- [x] T013 [US2] 为 17 个样本生成 mechanical.md（调用 ssbr-mechanical-interpretation Skill 解读力学图谱）
- [x] T014 [US2] 为 17 个样本生成 dsc.md（调用 ssbr-dsc-interpretation Skill 解读 DSC 谱图）
- [x] T015 [US2] 为 17 个样本生成 nmr.md（调用 ssbr-nmr-interpretation Skill 解读核磁谱图）
- [x] T016 [US2] 为 17 个样本生成 tem.md（调用 ssbr-tem-interpretation Skill 解读 TEM 图片）

> **注意**: 
> - 解读任务需要逐个样本手动调用 Skills，AI 会自动读取 Excel 和 PDF 文献
> - 缺失数据的样本，AI 会在解读文档中标注"暂无此项数据"
> - Excel 备份和瘦身任务由用户手动完成，不在自动化任务范围内

**Checkpoint**: 17 个样本各有 4 个解读文档（nmr.md、tem.md、mechanical.md、dsc.md），内容符合模板规范

---

## Phase 4: User Story 3 - 综合档案生成 (Priority: P1)

**Goal**: 为每个样本生成 summary.md 综合档案，供 RAG 检索使用

**Independent Test**: 检查生成的 summary.md 是否包含 4 个必需章节（官能化信息、核心性能特点、适用场景、文献来源）

**Depends on**: User Story 2（需要 mechanical.md 和 dsc.md 数据）

### Implementation for User Story 3

- [x] T019 [US3] 创建 summary.md 模板 `dataset/interpretations/TEMPLATE_summary.md`
- [x] T020 [US3] 创建 summary 生成脚本 `scripts/generate_summaries.py`
- [x] T021 [US3] 实现从 Excel 读取元数据（A-O 列：官能化信息、文献来源）
- [x] T022 [US3] 实现从 mechanical.md 提取力学数据和核心发现
- [x] T023 [US3] 实现从 dsc.md 提取热学数据和核心发现
- [x] T024 [US3] 实现 summary.md YAML front matter 生成（含 interpretations_included/missing）
- [x] T025 [US3] 实现 summary.md Markdown 正文生成（自然语言描述）
- [x] T026 [US3] 批量为 17 个样本生成 summary.md

**Checkpoint**: 17 个样本全部生成符合规范的 summary.md，每个文件包含至少 4 个必需章节

---

## Phase 5: User Story 1 - 自然语言推荐查询 (Priority: P1)

**Goal**: 实现基于语义的 RAG 推荐系统，用户可用自然语言描述需求获取推荐

**Independent Test**: 输入"改善白炭黑分散性"，验证系统返回相关 Top-3 样本及推荐理由

**Depends on**: User Story 3（需要 summary.md 作为检索数据源）

### Implementation for User Story 1

- [x] T027 [US1] 创建 RAG 检索核心模块 `scripts/rag_search.py`（实现 search-api.md 契约）
- [x] T028 [US1] 实现 search(query, k=3) 主接口（遍历 summary.md + 实时 Embedding）
- [x] T028.1 [US1] 实现查询预处理 `scripts/utils/query_preprocessor.py`（空白检测、长度限制 500 字符、特殊字符处理）
- [x] T029 [US1] 实现相似度分类逻辑（≥0.7 高度相关, 0.5-0.7 相关, <0.5 参考）
- [x] T030 [US1] 实现相关性分类和低相似度处理（< 0.5 标记为"参考"级别，仍返回 Top-K 并提示"知识库中无高度相关案例，以下为参考"）
- [x] T031 [US1] 更新 ssbr-recommender Skill `skills/ssbr-recommender/SKILL.md`
- [x] T032 [US1] 实现 Skill 调用 RAG 检索获取 Top-K 样本
- [x] T033 [US1] 实现 Skill 读取检索到的 summary.md 全文
- [x] T034 [US1] 实现 Skill 读取 Excel 元数据构建推荐上下文
- [x] T035 [US1] 实现 Skill LLM 生成推荐输出（含推荐方案、参考案例、预期效果、文献来源）
- [x] T036 [US1] 实现 Embedding API 失败时的降级处理（记录日志，通知用户）

**Checkpoint**: 自然语言推荐功能可用，用户输入查询可获得相关案例推荐

---

## Phase 6: User Story 4 - Skills 输出格式调整 (Priority: P2)

**Goal**: 更新解读 Skills 输出格式为 YAML front matter + Markdown 正文

**Independent Test**: 调用单个 Skill，检查输出文件是否符合 yaml-schema.md 规范

### Implementation for User Story 4

- [x] T037 [P] [US4] 更新 ssbr-stress-strain-interpretation Skill 输出格式 `skills/ssbr-stress-strain-interpretation/SKILL.md`
- [x] T038 [P] [US4] 更新 ssbr-payne-interpretation Skill 输出格式 `skills/ssbr-payne-interpretation/SKILL.md`
- [x] T039 [P] [US4] 更新 ssbr-dma-interpretation Skill 输出格式 `skills/ssbr-dma-interpretation/SKILL.md`
- [x] T040 [P] [US4] 更新 ssbr-dsc-interpretation Skill 输出格式 `skills/ssbr-dsc-interpretation/SKILL.md`
- [x] T041 [P] [US4] 更新 ssbr-nmr-interpretation Skill 输出格式 `skills/ssbr-nmr-interpretation/SKILL.md`
- [x] T042 [P] [US4] 更新 ssbr-tem-interpretation Skill 输出格式 `skills/ssbr-tem-interpretation/SKILL.md`
- [x] T043 [US4] 更新 ssbr-mechanical-interpretation 调度层 `skills/ssbr-mechanical-interpretation/SKILL.md`
- [x] T044 [US4] 创建新 Skill: ssbr-summary-generator `skills/ssbr-summary-generator/SKILL.md`
- [x] T045 [US4] 实现 Skills 自动保存输出到 interpretations 目录的逻辑

**Checkpoint**: 所有 7 个解读 Skills 和 1 个新 Skill 输出格式符合 YAML+Markdown 规范

---

## Phase 7: User Story 5 - 新样本录入 (Priority: P2)

**Goal**: 建立新样本录入标准流程

**Independent Test**: 录入新样本 SSBR-018，验证推荐系统能检索到该新样本

**Depends on**: User Story 1, 3, 4（需要完整的推荐系统和 Skills 格式）

### Implementation for User Story 5

- [x] T046 [US5] 编写新样本录入 SOP 文档 `specs/002-rag-data-migration/new-sample-sop.md`（含 MVP 单用户模式声明，明确不支持并发录入）
- [x] T047 [US5] 创建新样本目录初始化脚本 `scripts/init_new_sample.py`
- [x] T048 [US5] 实现新样本 Excel 行添加逻辑（元数据 A-O 列）
- [x] T049 [US5] 实现新样本 summary.md 自动生成触发（调用 ssbr-summary-generator）
- [x] T050 [US5] 实现向量索引增量更新 `scripts/update_vector_index.py`（支持单样本实时更新，避免全量重计算；覆盖 FR-022）

**Checkpoint**: 新样本录入流程完整可用，录入后推荐系统可立即检索到新样本

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: 跨用户故事的优化和完善工作

- [x] T051 [P] 更新 quickstart.md 添加实际使用示例 `specs/002-rag-data-migration/quickstart.md`
- [x] T052 [P] 更新 CODEBUDDY.md 项目上下文 `CODEBUDDY.md`
- [x] T053 代码清理和重构（移除调试代码，优化性能）
- [x] T054 [P] 创建边界情况处理文档（空查询、超长查询、YAML 解析失败、文件缺失）
- [x] T055 运行 quickstart.md 验证所有功能正常

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational) ← 阻塞所有用户故事
    │
    ▼
Phase 3 (US2: 数据迁移) ← MVP 第一步
    │
    ▼
Phase 4 (US3: Summary 生成) ← 依赖迁移完成
    │
    ▼
Phase 5 (US1: RAG 推荐) ← 依赖 Summary
    │
    ├─→ Phase 6 (US4: Skills 格式) ← 可并行
    │
    ▼
Phase 7 (US5: 新样本录入) ← 依赖完整系统
    │
    ▼
Phase 8 (Polish)
```

### User Story Dependencies

| User Story | 依赖 | 可并行 |
|------------|------|--------|
| US2 (数据迁移) | Phase 2 Foundational | 无 |
| US3 (Summary) | US2 | 无 |
| US1 (RAG 推荐) | US3 | 无 |
| US4 (Skills 格式) | Phase 2 | 可与 US2/US3/US1 并行 |
| US5 (新样本录入) | US1, US3, US4 | 无 |

### Within Each User Story

- 工具函数优先于业务脚本
- 数据处理优先于 Skill 更新
- 核心功能优先于边界处理
- 每个 checkpoint 后可验证该故事独立功能

### Parallel Opportunities

**Phase 1-2 并行任务**:
```
T002 (requirements.txt) ─┬─ 并行
T003 (创建目录)         ─┘

T005 (excel_handler.py) ─┬─ 并行
T006 (embedding.py)      │
T007 (similarity.py)    ─┘
```

**Phase 3 (US2) 并行任务**:
```
T011 (TEMPLATE_mechanical.md) ─┬─ 并行
T012 (TEMPLATE_dsc.md)        ─┘
```

**Phase 6 (US4) 并行任务**:
```
T037 (stress-strain) ─┬─ 所有 Skills
T038 (payne)         │  更新可完全
T039 (dma)           │  并行执行
T040 (dsc)           │
T041 (nmr)           │
T042 (tem)          ─┘
```

---

## Parallel Example: User Story 2 (数据迁移)

```bash
# Step 1: 创建模板文件（并行）
Task: "创建 mechanical.md 模板 dataset/interpretations/TEMPLATE_mechanical.md"
Task: "创建 dsc.md 模板 dataset/interpretations/TEMPLATE_dsc.md"

# Step 2: 按顺序执行迁移
Task: "创建 Excel 备份脚本 scripts/backup_excel.py"
Task: "创建数据迁移主脚本 scripts/migrate_excel_data.py"
Task: "实现 P-U 列数据写入..."
Task: "实现 V-W 列数据写入..."

# Step 3: 验证和清理
Task: "创建数据验证脚本 scripts/validate_migration.py"
Task: "执行数据迁移..."
```

---

## Implementation Strategy

### MVP First (最小可用产品)

1. ✅ Complete Phase 1: Setup
2. ✅ Complete Phase 2: Foundational
3. ✅ Complete Phase 3: US2 (数据迁移) - **基础数据就绪**
4. ✅ Complete Phase 4: US3 (Summary 生成) - **RAG 数据源就绪**
5. ✅ Complete Phase 5: US1 (RAG 推荐) - **核心功能可用**
6. **STOP and VALIDATE**: 测试自然语言推荐功能
7. 可选：继续 Phase 6-7 扩展功能

### Suggested MVP Scope

**MVP 范围**: User Story 2 + User Story 3 + User Story 1

**MVP 验收标准**:
- 17 个样本数据迁移完成，Excel 只保留 A-O 列
- 17 个样本各有 4 个解读文档（nmr.md、tem.md、mechanical.md、dsc.md）
- 17 个样本全部生成 summary.md
- 用户可用自然语言查询获取推荐

**MVP 预计任务数**: 42 个任务 (Phase 1-5 全部任务)

### Incremental Delivery

| 阶段 | 交付物 | 用户价值 |
|------|--------|----------|
| Phase 3 完成 | 数据迁移 | 数据架构现代化 |
| Phase 4 完成 | Summary 生成 | RAG 数据源就绪 |
| Phase 5 完成 | RAG 推荐 | 核心功能可用 ✨ |
| Phase 6 完成 | Skills 更新 | 新数据可自动入库 |
| Phase 7 完成 | 新样本流程 | 知识库可持续扩充 |

---

## Task Summary

| 类别 | 任务数 |
|------|--------|
| **总任务数** | 61 |
| **Phase 1 (Setup)** | 3 |
| **Phase 2 (Foundational)** | 5 |
| **Phase 3 (US2 数据迁移)** | 15 |
| **Phase 4 (US3 Summary)** | 8 |
| **Phase 5 (US1 RAG推荐)** | 11 |
| **Phase 6 (US4 Skills)** | 9 |
| **Phase 7 (US5 新样本)** | 5 |
| **Phase 8 (Polish)** | 5 |

| 并行机会 | 数量 |
|----------|------|
| **可并行任务 [P]** | 19 |
| **最大并行度** | 6 (Phase 6 Skills 更新) |

---

## Notes

- [P] 任务 = 不同文件，无依赖，可并行执行
- [Story] 标签 = 任务所属用户故事，便于追溯
- 每个用户故事应独立完成和可测试
- 每个 checkpoint 后提交代码
- MVP 范围：Phase 1-5（共 42 个任务）
- 避免：模糊任务、同文件冲突、跨故事依赖
