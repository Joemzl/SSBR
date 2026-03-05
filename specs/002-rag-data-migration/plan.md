# Implementation Plan: RAG 推荐系统数据架构重构

**Branch**: `002-rag-data-migration` | **Date**: 2026-03-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-rag-data-migration/spec.md`

## Summary

将 SSBR 官能化知识库从「Excel 存储所有数值」架构重构为「元数据 + 解读文档」分离架构，实现 RAG 语义检索推荐。核心工作包括：Excel 瘦身（保留 A-O 列）、数据迁移到 Markdown 解读文档、summary.md 综合档案生成、实时向量化检索实现。

## Technical Context

**Language/Version**: Markdown + YAML (数据格式), Python 3.x (迁移脚本)  
**Primary Dependencies**: AI Skills (CodeBuddy IDE), OpenAI Embedding API (text-embedding-3-small)  
**Storage**: 文件系统 (Markdown 文档) + Excel (元数据), MVP 阶段无向量数据库  
**Testing**: 手动验证 + 数据完整性校验脚本  
**Target Platform**: CodeBuddy IDE 本地环境  
**Project Type**: 知识库 + AI Skills 系统  
**Performance Goals**: 单次推荐查询 < 30 秒，全量向量化 < 5 分钟  
**Constraints**: 17 条样本数据，本地优先，轻量化部署，零幻觉  
**Scale/Scope**: 17 个样本，4 类解读文档/样本，7 个 Skills 更新

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| 原则 | 状态 | 说明 |
|------|------|------|
| I. 真实性第一 | ✅ PASS | 数据迁移保持原始数据完整性，summary.md 基于已有解读生成 |
| II. 全流程自动化 | ✅ PASS | Skills 自动保存到 interpretations 目录，自动触发向量化 |
| III. 格式标准化 | ✅ PASS | YAML front matter + Markdown 正文格式统一规范 |
| IV. 推荐严谨可控 | ✅ PASS | RAG 检索基于真实 summary.md，推荐输出包含文献来源 |
| V. 数据解读全面性 | ✅ PASS | 解读文档继承现有字段结构，支持多点提取 |
| VI. 兼容可扩展 | ✅ PASS | 新增指标无需修改 Excel，只需扩展解读文档 YAML |
| VII. 合规使用 | ✅ PASS | 仅限学术研究，保留完整引用信息 |
| VIII. 轻量化与可维护性 | ✅ PASS | 纯文件 + 实时 Embedding，零数据库依赖 |

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-data-migration/
├── spec.md              # 功能规范 (已完成)
├── plan.md              # 本文件
├── research.md          # Phase 0 研究输出
├── data-model.md        # Phase 1 数据模型
├── quickstart.md        # Phase 1 快速开始指南
├── contracts/           # Phase 1 接口契约
│   ├── yaml-schema.md   # YAML front matter 结构定义
│   └── search-api.md    # 检索接口契约
└── tasks.md             # Phase 2 任务分解 (speckit.tasks 生成)
```

### Source Code (repository root)

```text
dataset/
├── 数据.xlsx                    # 元数据存储（瘦身后 A-O 列）
├── 数据_backup_YYYYMMDD.xlsx    # 迁移前备份
└── interpretations/             # 解读文档库
    ├── TEMPLATE.md              # 模板文件（已存在）
    ├── SSBR-001/
    │   ├── nmr.md               # 核磁解读
    │   ├── tem.md               # TEM 解读
    │   ├── mechanical.md        # 力学解读（含应力-应变/Payne/DMA）
    │   ├── dsc.md               # DSC 解读
    │   └── summary.md           # 综合档案（RAG 检索核心）
    ├── SSBR-002/
    │   └── ...
    └── SSBR-017/
        └── ...

skills/
├── ssbr-recommender/            # 推荐 Skill（需更新为 RAG 模式）
├── ssbr-summary-generator/      # 新增：综合档案生成 Skill
├── ssbr-stress-strain-interpretation/  # 更新输出格式
├── ssbr-payne-interpretation/   # 更新输出格式
├── ssbr-dma-interpretation/     # 更新输出格式
├── ssbr-dsc-interpretation/     # 更新输出格式
├── ssbr-nmr-interpretation/     # 更新输出格式
├── ssbr-tem-interpretation/     # 更新输出格式
└── ssbr-mechanical-interpretation/  # 调度层更新

scripts/                         # 新增：迁移和工具脚本
├── migrate_excel_data.py        # Excel 数据迁移脚本
├── generate_summaries.py        # 批量生成 summary.md
└── validate_migration.py        # 迁移数据校验脚本
```

**Structure Decision**: 采用纯文件系统方案，解读文档存储于 `/dataset/interpretations/`，Skills 定义存储于 `/skills/`。MVP 阶段不引入额外数据库依赖。

## Complexity Tracking

> 无违规项需要记录。设计符合宪法所有原则。

---

## Constitution Check (Post-Design Re-evaluation)

*Phase 1 设计完成后重新评估*

| 原则 | 状态 | 验证点 |
|------|------|--------|
| I. 真实性第一 | ✅ PASS | data-model.md 定义数据来源层级，summary.md 必须基于已有解读生成 |
| II. 全流程自动化 | ✅ PASS | search-api.md 定义自动化检索流程，Skills 自动保存到 interpretations |
| III. 格式标准化 | ✅ PASS | yaml-schema.md 定义统一的 YAML front matter 结构 |
| IV. 推荐严谨可控 | ✅ PASS | search-api.md 定义相似度阈值和相关性分类，推荐必须标注来源 |
| V. 数据解读全面性 | ✅ PASS | yaml-schema.md 定义完整的数值字段，支持多点提取和区间表达 |
| VI. 兼容可扩展 | ✅ PASS | data-model.md 支持新增解读类型，spec.md 定义向量存储演进路线 |
| VII. 合规使用 | ✅ PASS | summary.md 必须包含文献来源章节，推荐输出保留引用信息 |
| VIII. 轻量化与可维护性 | ✅ PASS | MVP 采用纯文件方案，零数据库依赖，quickstart.md 提供快速上手指南 |

**结论**: Phase 1 设计通过所有宪法原则检查，可进入 Phase 2 任务分解阶段。

---

## Phase Outputs Summary

| Phase | 输出文件 | 状态 |
|-------|----------|------|
| Phase 0 | research.md | ✅ 完成 |
| Phase 1 | data-model.md | ✅ 完成 |
| Phase 1 | contracts/yaml-schema.md | ✅ 完成 |
| Phase 1 | contracts/search-api.md | ✅ 完成 |
| Phase 1 | quickstart.md | ✅ 完成 |
| Phase 1 | CODEBUDDY.md (agent context) | ✅ 完成 |
| Phase 2 | tasks.md | ✅ 完成 |
