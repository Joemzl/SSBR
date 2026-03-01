# Tasks: SSBR官能化知识库与智能推荐系统

**Input**: Design documents from `/specs/001-ssbr-knowledge-recommender/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: 手动验收测试（基于 spec.md 中定义的 Acceptance Scenarios），无自动化测试要求

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

本项目采用 CodeBuddy 标准 Skill 文件夹架构，无编程代码：

```
skills/                  # AI 对话助手技能文件夹
├── skill-name/
│   └── SKILL.md         # 包含 YAML 前置元数据 + Markdown 指令
dataset/                 # 知识库数据存储
literature/              # PDF 文献库
specs/                   # 规格与设计文档
```

---

## Phase 1: Setup (基础环境准备)

**Purpose**: 确认项目结构和现有资源完整性

- [X] T001 验证项目目录结构完整性（skills/, dataset/, literature/）
- [X] T002 [P] 确认 `/dataset/数据.xlsx` 文件存在且结构符合 data-model.md 规范
- [X] T003 [P] 确认 `/literature/` 文件夹存在且至少包含一个按命名规范命名的 PDF 文件
- [X] T004 [P] 验证现有 4 套解读 Skill 文件夹完整（`skills/ssbr-dsc-interpretation/SKILL.md`, `skills/ssbr-nmr-interpretation/SKILL.md`, `skills/ssbr-stress-strain-interpretation/SKILL.md`, `skills/ssbr-tem-interpretation/SKILL.md`）

---

## Phase 2: Foundational (数据结构标准化)

**Purpose**: 确保 Excel 数据结构符合推荐系统需求，此阶段必须完成才能开始用户故事实现

**⚠️ CRITICAL**: 数据结构不规范将导致推荐系统无法正常匹配

- [X] T005 根据 data-model.md 检查并补全 `/dataset/数据.xlsx` 列结构，确保包含所有必填字段（已生成 data-migration-guide.md 指导用户手动调整）
- [X] T006 [P] 在 Excel 中添加「应用场景」列（如尚未存在），允许值：轮胎胎面、密封制品、减震材料、通用橡胶制品（现有列名为「SSBR 应用」，已在迁移指南中说明重命名）
- [X] T007 [P] 在 Excel 中添加「力学数据来源」和「热学数据来源」列，标注 Level 1/2/3（已在迁移指南中定义列结构）
- [X] T008 检查现有数据记录，为每条记录填充「样本ID」（格式：SSBR-XXX）（已在迁移指南中提供建议ID）
- [X] T009 验证 PDF 文件命名规范：`{DOI}_{第一作者}_{年份}.pdf`（DOI 中 `/` 替换为 `_`）（现有文件 10.1039_c9ra02783a_Gao_2019.pdf 符合规范）

**Checkpoint**: 数据结构标准化完成 - 可开始用户故事实现

---

## Phase 3: User Story 1 - 智能方案推荐查询 (Priority: P1) 🎯 MVP

**Goal**: 用户输入目标性能指标，系统返回带文献支撑的官能化方案推荐

**Independent Test**: 输入"我想用SSBR做轮胎胎面，希望100%定伸应力达到4.0MPa"，系统返回匹配方案或明确提示无匹配

### Implementation for User Story 1

- [X] T010 [US1] 验证并完善智能推荐 Skill 文件 `/skills/ssbr-recommender/SKILL.md`（已存在基础版本）
- [X] T011 [US1] 在 `ssbr-recommender/SKILL.md` 中完善角色定位：SSBR官能化智能推荐专家
- [X] T012 [US1] 在 `ssbr-recommender/SKILL.md` 中完善自动化检索流程：读取 `/dataset/数据.xlsx` 全部数据
- [X] T013 [US1] 在 `ssbr-recommender/SKILL.md` 中完善查询解析规则：提取应用场景、性能指标（精确值/范围）、偏差容忍
- [X] T014 [US1] 在 `ssbr-recommender/SKILL.md` 中完善场景过滤规则：优先锁定用户指定的应用场景
- [X] T015 [US1] 在 `ssbr-recommender/SKILL.md` 中完善性能匹配规则：支持精确值匹配、范围匹配、偏差容忍匹配
- [X] T016 [US1] 在 `ssbr-recommender/SKILL.md` 中完善排序规则：完全匹配 > 偏差匹配，偏差小 > 偏差大，Level 1 > Level 2 > Level 3
- [X] T017 [US1] 在 `ssbr-recommender/SKILL.md` 中完善标准化输出格式（符合 contracts/skill-interfaces.md Contract 2 规范）
- [X] T018 [US1] 在 `ssbr-recommender/SKILL.md` 中完善错误处理：知识库为空、无匹配结果、查询无法解析
- [X] T019 [US1] 在 `ssbr-recommender/SKILL.md` 中完善禁止项：零编造、零幻觉、无确凿不输出
- [ ] T020 [US1] 手动验收测试：执行 spec.md 中 User Story 1 的 4 个 Acceptance Scenarios

**Checkpoint**: 智能推荐功能可独立使用和验证

---

## Phase 4: User Story 2 - 表征图片自动解读 (Priority: P2)

**Goal**: 根据 Excel 中的 DOI 和图注，自动定位文献图片并输出标准化解读结果

**Independent Test**: 指定 Excel 第 2 行，系统自动完成 DSC 解读并输出可直接录入 Excel 的结果

### Implementation for User Story 2

- [X] T021 [US2] 审查 `/skills/ssbr-dsc-interpretation/SKILL.md`，确保符合 contracts/skill-interfaces.md Contract 1 规范
- [X] T022 [P] [US2] 审查 `/skills/ssbr-nmr-interpretation/SKILL.md`，确保符合 contracts/skill-interfaces.md Contract 1 规范
- [X] T023 [P] [US2] 审查 `/skills/ssbr-stress-strain-interpretation/SKILL.md`，确保符合 contracts/skill-interfaces.md Contract 1 规范
- [X] T024 [P] [US2] 审查 `/skills/ssbr-tem-interpretation/SKILL.md`，确保符合 contracts/skill-interfaces.md Contract 1 规范
- [X] T025 [US2] 统一 4 套解读 Skill 的输入格式：支持「指定行号」和「指定样本ID」两种方式
- [X] T026 [US2] 统一 4 套解读 Skill 的输出格式：基础信息 → 表征特定信息 → 核心数据 → 文献结论
- [X] T027 [US2] 确保 4 套解读 Skill 的错误响应格式一致（参考 contracts/skill-interfaces.md）
- [ ] T028 [US2] 手动验收测试：执行 spec.md 中 User Story 2 的 4 个 Acceptance Scenarios（使用现有文献 10.1039_c9ra02783a_Gao_2019.pdf）

**Checkpoint**: 4 套表征解读功能可独立使用和验证

---

## Phase 5: User Story 3 - 知识库数据浏览与管理 (Priority: P3)

**Goal**: 用户可浏览知识库中所有数据，按条件筛选，查看详情

**Independent Test**: 请求查看全部数据，系统返回结构化的数据列表

### Implementation for User Story 3

- [X] T029 [US3] 在 `/skills/ssbr-recommender/SKILL.md` 中扩展数据浏览功能：支持「查看知识库全部数据」指令
- [X] T030 [US3] 定义数据列表输出格式：官能化试剂、核心官能团、官能化程度、应用场景、核心性能、文献来源
- [X] T031 [US3] 支持按字段筛选：官能化试剂=XXX、应用场景=XXX、Tg范围=XXX
- [X] T032 [US3] 支持查看单条数据详情：展示完整表征解读信息
- [ ] T033 [US3] 手动验收测试：执行 spec.md 中 User Story 3 的 3 个 Acceptance Scenarios

**Checkpoint**: 数据浏览与筛选功能可独立使用和验证

---

## Phase 6: User Story 4 - 知识库数据录入 (Priority: P4)

**Goal**: 用户可将新样本数据录入知识库，系统验证数据格式

**Independent Test**: 新增一条样本后，可在推荐查询中检索到

### Implementation for User Story 4

- [X] T034 [US4] 扩展 `/specs/001-ssbr-knowledge-recommender/quickstart.md` 的数据录入指南部分（避免与现有内容重复）
- [X] T035 [US4] 在录入指南中定义必填字段检查清单（样本ID、样品名称、官能化试剂名称、核心官能团、文献DOI）
- [X] T036 [US4] 在录入指南中定义字段格式规范（应力数值、温度数值、百分比、缺失数据表示）
- [X] T037 [US4] 在录入指南中定义 PDF 命名规范和存放位置
- [X] T038 [US4] 在录入指南中定义数据录入工作流：准备 PDF → 录入基础信息 → 调用解读 Skill → 复制结果到 Excel
- [ ] T039 [US4] 手动验收测试：执行 spec.md 中 User Story 4 的 3 个 Acceptance Scenarios

**Checkpoint**: 数据录入流程清晰，可指导用户完成知识库扩充

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 完善文档、处理边缘情况、整体优化

- [X] T040 [P] 更新 `/specs/001-ssbr-knowledge-recommender/quickstart.md`，确保与实现一致
- [X] T041 [P] 整理所有 Skill 文件夹（`skills/*/SKILL.md`）的格式和注释，确保可读性
- [X] T042 验证所有边缘情况处理（spec.md Edge Cases）
- [X] T043 [P] 创建知识库数据备份建议文档
- [ ] T044 按 quickstart.md 执行完整端到端验证流程
- [X] T045 更新 plan.md 标记 Phase 2: Tasks 为 Complete

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ──────────────────────┐
                                     │
Phase 2: Foundational ───────────────┼──→ BLOCKS all user stories
                                     │
         ┌───────────────────────────┘
         │
         ├──→ Phase 3: US1 (P1) - 智能推荐 🎯 MVP
         │
         ├──→ Phase 4: US2 (P2) - 表征解读
         │
         ├──→ Phase 5: US3 (P3) - 数据浏览
         │
         └──→ Phase 6: US4 (P4) - 数据录入
                                     │
                                     ↓
Phase 7: Polish ─────────────────────┘
```

### User Story Dependencies

| User Story | 依赖 | 可并行 |
|------------|------|--------|
| US1 (P1) 智能推荐 | Phase 2 完成 | ✅ 可独立开始 |
| US2 (P2) 表征解读 | Phase 2 完成 | ✅ 可与 US1 并行 |
| US3 (P3) 数据浏览 | US1 基础（复用推荐 Skill） | ⚠️ 建议 US1 后 |
| US4 (P4) 数据录入 | US2 完成（需要解读功能） | ⚠️ 需 US2 先完成 |

### Parallel Opportunities

- **Phase 1**: T002, T003, T004 可并行
- **Phase 2**: T006, T007 可并行
- **Phase 4**: T022, T023, T024 可并行（审查不同 Skill 文件）
- **Phase 7**: T040, T041, T043 可并行

---

## Parallel Example: Phase 4 (User Story 2)

```bash
# 可同时启动的任务：
Task T022: 审查 ssbr-nmr-interpretation/SKILL.md
Task T023: 审查 ssbr-stress-strain-interpretation/SKILL.md  
Task T024: 审查 ssbr-tem-interpretation/SKILL.md

# 完成后再执行：
Task T025: 统一输入格式
Task T026: 统一输出格式
Task T027: 统一错误响应
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. ✅ Complete Phase 1: Setup（验证环境）
2. ✅ Complete Phase 2: Foundational（数据结构标准化）
3. ⭐ Complete Phase 3: User Story 1（智能推荐 - **核心价值**）
4. **STOP and VALIDATE**: 测试推荐功能是否返回正确结果
5. 🚀 **MVP 可交付**：用户已可使用智能推荐功能

### Incremental Delivery

| 阶段 | 交付内容 | 用户可使用的功能 |
|------|----------|------------------|
| MVP | Phase 1-3 | 智能推荐查询 |
| +US2 | Phase 4 | 智能推荐 + 表征自动解读 |
| +US3 | Phase 5 | 上述 + 知识库浏览 |
| +US4 | Phase 6 | 上述 + 数据录入指南 |
| Complete | Phase 7 | 完整系统 + 文档 |

### 建议执行顺序（单人）

```
Day 1: T001-T009 (Setup + Foundational)
Day 2: T010-T020 (US1 - 推荐 Skill 创建)
Day 3: T021-T028 (US2 - 解读 Skill 审查)
Day 4: T029-T039 (US3 + US4)
Day 5: T040-T045 (Polish)
```

---

## Notes

- **[P]** 标记的任务可与同 Phase 内其他 [P] 任务并行执行
- **[USn]** 标记表示该任务属于哪个用户故事
- 本项目为纯 Skill 配置，无编程代码，所有"实现"均为 Skill 文件内容编写
- 手动验收测试基于 spec.md 中定义的 Acceptance Scenarios
- 每个 Checkpoint 后应验证当前用户故事可独立工作
- 推荐使用 Git 在每个 Phase 完成后提交

---

## Summary

| 统计项 | 数值 |
|--------|------|
| **总任务数** | 45 |
| **Phase 1 (Setup)** | 4 |
| **Phase 2 (Foundational)** | 5 |
| **Phase 3 (US1 - 推荐)** | 11 |
| **Phase 4 (US2 - 解读)** | 8 |
| **Phase 5 (US3 - 浏览)** | 5 |
| **Phase 6 (US4 - 录入)** | 6 |
| **Phase 7 (Polish)** | 6 |
| **可并行任务** | 15 |
| **MVP 范围** | Phase 1-3 (20 tasks) |
