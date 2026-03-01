# Implementation Plan: SSBR官能化知识库与智能推荐系统

**Branch**: `001-ssbr-knowledge-recommender` | **Date**: 2026-02-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ssbr-knowledge-recommender/spec.md`

## Summary

构建一个 SSBR 官能化体系专属知识库与智能推荐系统，以 AI 对话助手技能（Skill）形式运行。系统包含四套标准化表征解读技能（¹H核磁、TEM、应力-应变、DSC），可从本地 Excel 数据集和 PDF 文献库自动检索、定位、解读表征图片，并基于结构化知识库实现官能化方案智能推荐——用户输入目标性能指标后，系统返回带文献支撑的推荐结果。

## Technical Context

**Language/Version**: N/A（纯 Skill 配置，无编程语言依赖）  
**Primary Dependencies**: 
- AI 对话助手平台（CodeBuddy/Claude 等）
- PDF 阅读与图片定位能力（依赖 AI 平台内置能力）
- Excel 读取能力（依赖 AI 平台内置能力）

**Storage**: 
- `/dataset/数据.xlsx` - 主数据存储（唯一数据源）
- `/literature/` - 本地 PDF 文献库（按 `DOI_第一作者_年份.pdf` 命名）

**Testing**: 手动验收测试（基于 spec.md 中定义的 Acceptance Scenarios）  
**Target Platform**: AI 对话助手平台（本地运行）  
**Project Type**: AI Skill 集合（知识库 + 推荐系统）  
**Performance Goals**: 推荐查询响应 ≤30秒（知识库≤500条）  
**Constraints**: 
- 零幻觉：所有输出必须有文献支撑
- 本地优先：支持完全本地运行
- 轻量化：无需额外数据库部署

**Scale/Scope**: 
- 初期：数十至数百条样本数据
- 扩展目标：≤500条数据时保持性能

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Check (Phase 0 前)

| Principle | Status | Compliance Notes |
|-----------|--------|------------------|
| I. 真实性第一 | ✅ PASS | Skills 已定义「显式数据优先、零编造、零幻觉」规则，所有输出标注数据来源层级 |
| II. 全流程自动化 | ✅ PASS | Skills 已定义固定路径检索流程，无需手动上传 |
| III. 格式标准化 | ✅ PASS | Skills 输出格式与 Excel 列一一对应 |
| IV. 推荐严谨可控 | ✅ PASS | 推荐系统规则明确：场景优先、无确凿不输出 |
| V. 数据解读全面性 | ✅ PASS | 应力-应变 Skill 明确多点提取（100%/200%/300%定伸应力） |
| VI. 兼容可扩展 | ✅ PASS | Excel 存储兼容未来数据库迁移设计 |
| VII. 合规使用 | ✅ PASS | Skills 明确仅限学术研究用途 |
| VIII. 轻量化与可维护性 | ✅ PASS | 纯 Skill 配置，零编程依赖，本地 Excel + PDF |

**Pre-Design Gate Result**: ✅ ALL PASS - 进入 Phase 0

### Post-Design Check (Phase 1 后)

| Principle | Status | Compliance Notes |
|-----------|--------|------------------|
| I. 真实性第一 | ✅ PASS | data-model.md 定义了数据来源层级（L1-L4），contracts 明确错误响应规范 |
| II. 全流程自动化 | ✅ PASS | contracts 定义了完整的自动检索-解读-输出流程 |
| III. 格式标准化 | ✅ PASS | data-model.md 规范了字段格式（单位、精度），quickstart 提供录入指南 |
| IV. 推荐严谨可控 | ✅ PASS | contracts 明确了匹配规则、排序机制、错误响应 |
| V. 数据解读全面性 | ✅ PASS | data-model.md 包含力学/热学全部字段，支持多维度匹配 |
| VI. 兼容可扩展 | ✅ PASS | data-model.md 提供了 SQL 迁移模板 |
| VII. 合规使用 | ✅ PASS | quickstart 强调数据质量红线 |
| VIII. 轻量化与可维护性 | ✅ PASS | 纯 Skill 架构，无编程依赖，文档完整 |

**Post-Design Gate Result**: ✅ ALL PASS - 可进入 Phase 2

## Project Structure

### Documentation (this feature)

```text
specs/001-ssbr-knowledge-recommender/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (Skill 接口契约)
└── tasks.md             # Phase 2 output (NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
skills/
├── ssbr-dsc-interpretation/
│   └── SKILL.md                       # DSC 谱图解读技能 (已存在)
├── ssbr-nmr-interpretation/
│   └── SKILL.md                       # ¹H 核磁解读技能 (已存在)
├── ssbr-stress-strain-interpretation/
│   └── SKILL.md                       # 应力-应变解读技能 (已存在)
├── ssbr-tem-interpretation/
│   └── SKILL.md                       # TEM 形貌解读技能 (已存在)
└── ssbr-recommender/
    └── SKILL.md                       # 智能推荐技能 (已存在)

dataset/
└── 数据.xlsx                          # 知识库主数据源 (已存在)

literature/
└── *.pdf                              # 本地 PDF 文献库 (按命名规范存放)
```

**Structure Decision**: 采用 CodeBuddy 标准 Skill 文件夹架构（每个 Skill 为独立文件夹，包含 SKILL.md），无需编程代码。所有功能通过 AI 对话助手技能配置实现，数据存储使用现有 Excel 文件。

## Complexity Tracking

> 无违规项需要追踪，所有宪法原则均已满足。

---

## Phase Completion Status

| Phase | Status | Output |
|-------|--------|--------|
| Phase 0: Research | ✅ Complete | [research.md](./research.md) |
| Phase 1: Design | ✅ Complete | [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md) |
| Phase 2: Tasks | ✅ Complete | [tasks.md](./tasks.md) |
| Phase 3: Implementation | ✅ Complete | Skills 完善、数据迁移指南、备份建议 |

---

## Generated Artifacts Summary

| Artifact | Path | Description |
|----------|------|-------------|
| research.md | `specs/001-ssbr-knowledge-recommender/research.md` | 5 项研究决策：Skill 组织、数据结构、匹配算法、排序机制、错误处理 |
| data-model.md | `specs/001-ssbr-knowledge-recommender/data-model.md` | 数据模型定义，含字段规范、验证规则、迁移模板 |
| skill-interfaces.md | `specs/001-ssbr-knowledge-recommender/contracts/skill-interfaces.md` | 5 套 Skill 接口契约，含输入/输出格式、错误响应 |
| quickstart.md | `specs/001-ssbr-knowledge-recommender/quickstart.md` | 快速入门指南，含使用示例和常见问题 |
