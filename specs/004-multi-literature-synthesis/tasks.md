# Tasks: 多文献综合推理问答系统

**Input**: Design documents from `/specs/004-multi-literature-synthesis/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests**: Not explicitly requested in specification. Implementation-only tasks.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)

## Path Conventions

- **Scripts**: `scripts/` at repository root
- **Synthesis module**: `scripts/synthesis/` (new)
- **Utils**: `scripts/utils/`
- **Demo**: `demo/`
- Paths based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: New module initialization and basic structure

- [x] T001 Create `scripts/synthesis/` module directory structure
- [x] T002 Create `scripts/synthesis/__init__.py` with module exports
- [x] T003 [P] Add new exception classes to `scripts/utils/exceptions.py` (InsufficientDataError, ExtrapolationBoundaryError, ConflictingTargetsError)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data models and core components that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Data Model Extensions

- [x] T004 [P] Add `SynthesisMode` enum to `scripts/models.py`
- [x] T005 [P] Add `ConfidenceTag` enum to `scripts/models.py`
- [x] T006 [P] Add `ContentType` enum to `scripts/models.py`
- [x] T007 Add `SampleSummary` dataclass to `scripts/models.py`
- [x] T008 Add `DataRange` dataclass with extrapolation boundary methods to `scripts/models.py`
- [x] T009 Add `SynthesizedAnswer` dataclass to `scripts/models.py`
- [x] T010 Add `SynthesisResponse` dataclass to `scripts/models.py`
- [x] T010a [P] Add `Citation` dataclass to `scripts/models.py` (doi, authors, year, title, inline_ref)

### Core Synthesis Infrastructure

- [x] T011 Create `scripts/synthesis/aggregator.py` with `SampleAggregator` class (extract `SampleSummary` from summary.md)
- [x] T012 Create `scripts/synthesis/citation_validator.py` for citation verification and format conversion
- [x] T013 Add synthesis prompt templates to `scripts/utils/prompt_templates.py` (SYNTHESIS_SYSTEM_PROMPT, SYNTHESIS_USER_TEMPLATE)

### QAEngine Base Extensions

- [x] T014 Extend `QAEngineConfig` in `scripts/qa_engine.py` with synthesis config options (synthesis_top_k, min_samples_trend, min_samples_compare, extrapolation_boundary)
- [x] T015 Add mode detection logic to `scripts/qa_engine.py` (classify query intent → SynthesisMode)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - 多文献综合回答 (Priority: P1) 🎯 MVP

**Goal**: 综合分析多篇文献的数据和结论，生成整合性回答（FR-001, FR-002, FR-011, FR-013, FR-014）

**Independent Test**: 输入"如何同时改善白炭黑分散性和湿地抓地力？"，验证回答综合了多个使用不同官能团的样本经验

### Implementation for User Story 1

- [x] T016 [US1] Implement `synthesize()` method in `scripts/qa_engine.py` (pipeline: search → rerank → aggregate → generate → validate)
- [x] T017 [US1] Add synthesis generation logic to `scripts/answer_generator.py` (call LLM with multi-sample context)
- [x] T018 [US1] Implement citation extraction and validation in `scripts/synthesis/citation_validator.py`
- [x] T019 [US1] Implement output formatting (layered structure: summary → details → citations) in `scripts/answer_generator.py`
- [x] T020 [US1] Extend `QAEngine.answer()` with `synthesis_mode` parameter for backward compatibility
- [x] T021 [US1] Add response validation in `SynthesizedAnswer.validate()` method (SC-001, SC-002 checks)

**Checkpoint**: User Story 1 (多文献综合) should be fully functional

---

## Phase 4: User Story 2 - 知识外推与趋势分析 (Priority: P1)

**Goal**: 识别数据规律并进行合理外推预测（FR-003, FR-004, FR-005, FR-012）

**Independent Test**: 询问"官能化程度在 5% 左右时，拉伸强度大概是多少？"，验证系统给出合理的区间估计

### Data Models for User Story 2

- [x] T022 [P] [US2] Add `TrendAnalysis` dataclass to `scripts/models.py`
- [x] T023 [P] [US2] Add `ExtrapolationResult` dataclass to `scripts/models.py`

### Implementation for User Story 2

- [x] T024 [US2] Create `scripts/synthesis/trend_analyzer.py` with `TrendAnalyzer` class
- [x] T025 [US2] Implement trend detection logic (identify variable relationships from samples) in `scripts/synthesis/trend_analyzer.py`
- [x] T026 [US2] Create `scripts/synthesis/extrapolator.py` with `Extrapolator` class
- [x] T027 [US2] Implement boundary validation logic (50% rule) in `scripts/synthesis/extrapolator.py`
- [x] T028 [US2] Implement confidence tag determination (HIGH/MEDIUM/LOW based on data points) in `scripts/synthesis/extrapolator.py`
- [x] T029 [US2] Add trend analysis and extrapolation prompts to `scripts/utils/prompt_templates.py`
- [x] T030 [US2] Integrate trend analyzer and extrapolator into `synthesize()` method in `scripts/qa_engine.py`
- [x] T031 [US2] Add extrapolation warning formatting in `ExtrapolationResult.to_display_text()` method

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - 配方设计建议 (Priority: P2)

**Goal**: 根据用户目标性能需求生成配方设计建议（FR-006, FR-007, FR-008）

**Independent Test**: 输入"设计一个高湿地抓地力、低滚动阻力的配方"，验证系统给出包含官能团、程度、填料参数的建议

### Data Models for User Story 3

- [x] T032 [P] [US3] Add `FormulaRecommendation` dataclass to `scripts/models.py`

### Implementation for User Story 3

- [x] T033 [US3] Create `scripts/synthesis/formula_designer.py` with `FormulaDesigner` class
- [x] T034 [US3] Implement target conflict detection logic in `scripts/synthesis/formula_designer.py`
- [x] T035 [US3] Implement formula generation logic (select functional group, degree, filler) in `scripts/synthesis/formula_designer.py`
- [x] T036 [US3] Add formula design prompt templates to `scripts/utils/prompt_templates.py`
- [x] T037 [US3] Implement `design_formula()` method in `scripts/qa_engine.py`
- [x] T038 [US3] Add trade-off analysis and warning generation in `FormulaRecommendation` formatting

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - 对比分析表格 (Priority: P3)

**Goal**: 生成结构化对比表格，多维度比较不同官能化方案（FR-009, FR-010）

**Independent Test**: 询问"羟基和环氧官能化的区别"，验证系统返回包含力学、热学、分散效果等维度的对比表格

### Data Models for User Story 4

- [x] T039 [P] [US4] Add `ComparisonDimension` dataclass to `scripts/models.py`
- [x] T040 [P] [US4] Add `ComparisonEntry` dataclass to `scripts/models.py`
- [x] T041 [P] [US4] Add `ComparisonTable` dataclass with `to_markdown()` method to `scripts/models.py`

### Implementation for User Story 4

- [x] T042 [US4] Create `scripts/synthesis/comparison_table.py` with `ComparisonTableGenerator` class
- [x] T043 [US4] Implement scheme-based sample retrieval in `scripts/synthesis/comparison_table.py`
- [x] T044 [US4] Implement dimension auto-selection logic (5-7 core dimensions) in `scripts/synthesis/comparison_table.py`
- [x] T045 [US4] Implement missing data handling ("数据不足" marker) in `scripts/synthesis/comparison_table.py`
- [x] T046 [US4] Add comparison prompt templates to `scripts/utils/prompt_templates.py`
- [x] T047 [US4] Implement `compare()` method in `scripts/qa_engine.py`
- [x] T048 [US4] Add Markdown table formatting in `ComparisonTable.to_markdown()` method

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Demo & CLI Integration

**Purpose**: Expose new functionality via CLI and Web Demo

- [x] T049 Add CLI arguments for synthesis mode to `scripts/qa_engine.py` (--synthesize, --compare, --design, --no-extrapolation)
- [x] T050 Update `demo/app.py` to add synthesis mode toggle switch
- [x] T051 Update `demo/app.py` to add comparison analysis tab
- [x] T052 Update `demo/app.py` to add formula design tab
- [x] T053 Add result display formatting for trend analysis and extrapolation in `demo/app.py`

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Validation, optimization, and documentation

- [x] T054 [P] Add input validation for all new API methods in `scripts/qa_engine.py`
- [x] T055 [P] Add performance timing instrumentation (synthesis_time_ms) to `SynthesisResponse`
- [x] T056 Implement timeout handling (8s limit) with graceful degradation in `scripts/qa_engine.py`
- [x] T057 [P] Add logging for synthesis operations in all synthesis/ modules
- [x] T058 Run quickstart.md validation scenarios
- [x] T059 Update `CODEBUDDY.md` with new commands and capabilities
- [x] T060 [P] Add performance benchmark test for 8s SLA (SC-006) in `scripts/qa_engine.py --benchmark`
- [x] T061 [P] Implement zero-hallucination validator: verify all output data points are traceable to citations (FR-011)
- [x] T062 Validate edge cases: single-source warning, out-of-boundary rejection, conflicting data display, safety warnings, table degradation (spec.md Edge Cases)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational (BLOCKS all user stories)
    │
    ├──────────────────────────────────────────────┐
    │                                              │
    ▼                                              ▼
Phase 3: US1 (P1)                            Phase 4: US2 (P1)
多文献综合回答                                知识外推与趋势分析
    │                                              │
    ├──────────────────────────────────────────────┤
    │                                              │
    ▼                                              ▼
Phase 5: US3 (P2)                            Phase 6: US4 (P3)
配方设计建议                                  对比分析表格
    │                                              │
    └──────────────────────────────────────────────┘
                          │
                          ▼
                    Phase 7: Demo & CLI
                          │
                          ▼
                    Phase 8: Polish
```

### User Story Dependencies

| Story | Priority | Depends On | Can Parallel With |
|-------|----------|------------|-------------------|
| US1 (多文献综合) | P1 | Phase 2 | US2 |
| US2 (外推趋势) | P1 | Phase 2 | US1 |
| US3 (配方设计) | P2 | Phase 2, US1 recommended | US4 |
| US4 (对比分析) | P3 | Phase 2 | US3 |

### Within Each User Story

1. Data models first (if any)
2. Core logic modules
3. Prompt templates
4. QAEngine integration
5. Output formatting
6. Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**:
- T001-T003 can run in parallel

**Phase 2 (Foundational)**:
- T004, T005, T006 (enums) can run in parallel
- T007, T008, T009, T010 (dataclasses) sequential
- T011, T012, T013 can run in parallel
- T014, T015 sequential (depends on models)

**Phase 3-6 (User Stories)**:
- US1 and US2 can start in parallel after Phase 2
- US3 and US4 can start in parallel after Phase 2
- Within each story: models [P] → logic → integration

**Phase 7-8 (Demo/Polish)**:
- T049-T053 can run in parallel
- T054, T055, T057 can run in parallel

---

## Parallel Example: User Stories 1 & 2

```bash
# After Phase 2 completes, launch both P1 stories in parallel:

# User Story 1 track:
Task: "Implement synthesize() method in scripts/qa_engine.py"
Task: "Add synthesis generation logic to scripts/answer_generator.py"

# User Story 2 track (parallel):
Task: "Add TrendAnalysis dataclass to scripts/models.py"
Task: "Add ExtrapolationResult dataclass to scripts/models.py"
Task: "Create scripts/synthesis/trend_analyzer.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (~30 min)
2. Complete Phase 2: Foundational (~2 hours)
3. Complete Phase 3: User Story 1 - 多文献综合回答 (~3 hours)
4. **STOP and VALIDATE**: Test with "如何同时改善白炭黑分散性和湿地抓地力？"
5. Deploy/demo if ready - **This is the MVP!**

### Incremental Delivery

| Increment | Content | Business Value |
|-----------|---------|----------------|
| MVP | US1: 多文献综合 | 从"单样本检索"升级为"知识综合" |
| +US2 | 外推趋势分析 | 从"查询"到"分析"的质变 |
| +US3 | 配方设计 | 从"分析已有"到"设计新方案" |
| +US4 | 对比表格 | 结构化对比，便于决策 |
| Polish | Demo + CLI | 完整产品体验 |

### Task Counts

| Phase | Task Count | Parallel Tasks |
|-------|------------|----------------|
| Phase 1: Setup | 3 | 2 |
| Phase 2: Foundational | 12 | 6 |
| Phase 3: US1 | 6 | 0 |
| Phase 4: US2 | 10 | 2 |
| Phase 5: US3 | 7 | 1 |
| Phase 6: US4 | 10 | 3 |
| Phase 7: Demo | 5 | 4 |
| Phase 8: Polish | 9 | 5 |
| **Total** | **63** | **26** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story (US1-US4)
- Each user story should be independently completable and testable
- No tests included (not requested in spec)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All data values must trace to source literature (zero-hallucination principle)
