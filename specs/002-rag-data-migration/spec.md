# Feature Specification: RAG 推荐系统数据架构重构

**Feature Branch**: `002-rag-data-migration`  
**Created**: 2026-03-05  
**Status**: Clarified  
**Input**: User description: "将项目数据保存形式从 Excel 列存储改为元数据+解读文档分离架构，支持 RAG 语义检索推荐"

## 背景与动机

当前 SSBR 官能化知识库的推荐系统存在以下问题：

1. **无法理解用户意图**：用户使用自然语言描述需求时，系统无法进行语义匹配
2. **数据稀疏**：17 条样本数据难以通过精确匹配找到完全符合的案例
3. **扩展性差**：每次新增性能指标都需要修改 Excel 表结构（增加列）
4. **语义缺失**：纯数值数据缺乏上下文，LLM 无法理解其物理意义

本次重构旨在将数据架构从「Excel 存储所有数值」改为「元数据 + 解读文档」分离架构，支持 RAG 语义检索推荐。

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 自然语言推荐查询 (Priority: P1)

作为 SSBR 配方研究人员，我希望用自然语言描述我的需求（如"我需要改善白炭黑分散性并降低滚动阻力"），系统能够基于知识库中的历史案例，推荐最合适的官能化方案。

**Why this priority**: 这是推荐系统的核心价值，直接解决用户无法用精确参数描述需求的痛点。

**Independent Test**: 可通过输入一段自然语言需求描述，验证系统返回相关案例和推荐方案。

**Acceptance Scenarios**:

1. **Given** 知识库中有 17 个样本的 summary.md 已生成，**When** 用户输入"我需要改善白炭黑分散性"，**Then** 系统返回与分散性改善相关的 Top-3 样本及推荐理由
2. **Given** 知识库正常运行，**When** 用户输入"降低滚动阻力同时保持抓地力"，**Then** 系统返回 DMA 性能优异的样本，并解释推荐原因
3. **Given** 知识库正常运行，**When** 用户输入与知识库无关的需求（如"提高耐油性"），**Then** 系统明确告知"知识库中无高度相关案例"

---

### User Story 2 - 数据迁移与 Excel 瘦身 (Priority: P1)

作为系统维护者，我需要将现有 Excel P-W 列的力学/热学数值数据迁移到 Markdown 解读文档中，并删除 Excel 中的冗余列，使 Excel 只保留元数据。

**Why this priority**: 这是实现新架构的基础，不完成迁移就无法使用新的推荐流程。

**Independent Test**: 可通过检查迁移后的文件结构和数据完整性来验证。

**Acceptance Scenarios**:

1. **Given** 当前 Excel 有 A-W 列数据，**When** 执行数据迁移脚本，**Then** P-W 列数据被写入对应样本的 mechanical.md 和 dsc.md 文件的 YAML 部分
2. **Given** 数据迁移完成，**When** 查看 Excel 文件，**Then** 只保留 A-O 列，P-W 列已删除
3. **Given** 迁移完成，**When** 对比迁移前后的数据，**Then** 所有数值完全一致，无丢失

---

### User Story 3 - 综合档案生成 (Priority: P1)

作为系统维护者，我需要为每个样本生成 summary.md 综合档案，该档案以自然语言描述样本的核心特性，供 RAG 检索使用。

**Why this priority**: summary.md 是 RAG 检索的核心，没有它语义检索无法工作。

**Independent Test**: 可通过检查生成的 summary.md 内容是否符合规范来验证。

**Acceptance Scenarios**:

1. **Given** 样本 SSBR-001 有完整的 Excel 元数据和解读文档，**When** 调用 summary-generator Skill，**Then** 生成的 summary.md 包含官能化信息、核心性能特点、适用场景和文献来源
2. **Given** 某样本缺少部分解读文档，**When** 生成 summary.md，**Then** summary 中只包含已有解读内容，并标注缺失项
3. **Given** summary.md 已生成，**When** 阅读其内容，**Then** 内容为自然语言描述，非纯数值罗列

---

### User Story 4 - Skills 输出格式调整 (Priority: P2)

作为系统维护者，我需要更新现有解读 Skills 的输出格式，使其输出 YAML front matter + Markdown 正文，并自动保存到 interpretations 目录。

**Why this priority**: Skills 格式调整是数据流转的关键环节，但可以在完成数据迁移后逐步进行。

**Independent Test**: 可通过调用单个 Skill 并检查输出文件格式来验证。

**Acceptance Scenarios**:

1. **Given** 用户提供应力-应变曲线图片，**When** 调用 ssbr-stress-strain-interpretation Skill，**Then** 输出包含 YAML 数值和 Markdown 解读的 mechanical.md 文件
2. **Given** 输出文件已生成，**When** 解析 YAML front matter，**Then** 能正确提取所有结构化数值字段

---

### User Story 5 - 新样本录入 (Priority: P2)

作为研究人员，当我发现新的文献案例时，我希望按照标准流程录入新样本，包括填写 Excel 元数据、生成解读文档、生成综合档案。

**Why this priority**: 知识库的持续扩充是长期价值，但不影响当前系统的基本功能。

**Independent Test**: 可通过完整录入一个新样本并验证推荐系统能检索到它来验证。

**Acceptance Scenarios**:

1. **Given** 用户有一篇新文献，**When** 按工作流录入新样本 SSBR-018，**Then** Excel 新增一行元数据，interpretations/SSBR-018/ 目录包含所有解读文档和 summary.md
2. **Given** 新样本录入完成，**When** 用户查询与该样本相关的需求，**Then** 推荐系统能检索到该新样本

---

### Edge Cases

- **空查询处理**：用户输入空白或无意义字符时，系统应提示用户提供有效的需求描述
- **超长查询处理**：用户输入过长的描述时，系统应能正常处理或适当截断
- **YAML 解析失败**：某个解读文档 YAML 格式错误时，系统应能识别并报告具体问题，不影响其他样本
- **文件缺失处理**：当某个样本缺少 summary.md 时，推荐检索应跳过该样本并记录警告
- **并发访问**：多人同时录入数据时，不应产生文件冲突

---

## Requirements *(mandatory)*

### Functional Requirements

#### 数据架构

- **FR-001**: 系统 MUST 将 Excel 数据结构简化为只保留 A-O 列（元数据），移除 P-W 列（性能数值）
- **FR-002**: 系统 MUST 在 `/dataset/interpretations/` 目录下为每个样本建立独立文件夹
- **FR-003**: 系统 MUST 支持以 YAML front matter + Markdown 正文的格式存储解读文档
- **FR-004**: 每个样本 MUST 有一个 summary.md 综合档案文件

#### 数据迁移

- **FR-005**: 系统 MUST 在迁移前自动备份原始 Excel 文件
- **FR-006**: 系统 MUST 将 P-U 列数据（力学性能）迁移到 mechanical.md 的 YAML 部分
- **FR-007**: 系统 MUST 将 V-W 列数据（热学性能）迁移到 dsc.md 的 YAML 部分
- **FR-008**: 迁移过程 MUST 保证数据完整性，所有数值精确保留

#### 解读文档格式

- **FR-009**: 解读文档 MUST 包含 sample_id、type、created_at 等元信息字段
- **FR-010**: 解读文档的 data 部分 MUST 支持嵌套结构，记录数值、单位和数据来源
- **FR-011**: summary.md MUST 为自然语言描述，包含官能化信息、核心性能特点、适用场景

#### RAG 检索

- **FR-012**: 系统 MUST 能够对 summary.md 内容进行向量化处理
- **FR-013**: 系统 MUST 支持基于用户自然语言查询进行语义相似度检索
- **FR-014**: 系统 MUST 返回相似度最高的 Top-K（默认 K=3）样本
- **FR-015**: 推荐输出 MUST 包含推荐方案、参考案例、预期效果、文献来源

#### Skills 调整

- **FR-016**: 所有解读 Skills MUST 更新输出格式为 YAML+Markdown
- **FR-017**: 系统 MUST 新增 ssbr-summary-generator Skill 用于生成综合档案
- **FR-018**: 解读 Skills MUST 支持自动保存输出到 interpretations 目录

#### 边界处理

- **FR-019**: 当用户需求模糊时，系统 MUST 引导用户明确应用场景或关注指标
- **FR-020**: 当无相似案例（相似度 < 0.5）时，系统 MUST 提示"知识库中无高度相关案例"并给出最接近的参考
- **FR-021**: 推荐结果 MUST 标注数据来源，禁止编造知识库中不存在的数据

### Key Entities

- **样本（Sample）**: 一条 SSBR 官能化案例记录，由 Excel 元数据行和 interpretations 目录下的文档集合组成，唯一标识符为样本ID（如 SSBR-001）
- **解读文档（Interpretation Document）**: 存储特定类型表征解读结果的 Markdown 文件，包含 YAML 结构化数值和自然语言描述，类型包括 nmr.md、tem.md、mechanical.md、dsc.md
- **综合档案（Summary）**: 每个样本必须有的 summary.md 文件，汇总所有解读内容为自然语言描述，是 RAG 检索的核心文档
- **元数据（Metadata）**: Excel 中 A-O 列存储的固定信息，包括样本ID、官能化信息、图注引用、文献来源

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 数据迁移后 Excel 只保留 15 列（A-O），17 个样本的迁移数据与原数据 100% 一致
- **SC-002**: 17 个样本全部生成符合规范的 summary.md，每个文件包含至少 4 个必需章节（官能化信息、核心性能特点、适用场景、文献来源）
- **SC-003**: 用户输入自然语言查询后，系统在 30 秒内返回推荐结果
- **SC-004**: 对于"改善白炭黑分散性"、"降低滚动阻力"等典型查询，系统返回的 Top-3 结果中至少有 2 个与查询意图高度相关
- **SC-005**: 新样本录入流程可在 30 分钟内完成（从获取文献到推荐系统可检索）
- **SC-006**: 新增一种性能指标类型时，无需修改 Excel 表结构，只需在对应解读文档中添加 YAML 字段

---

## Assumptions

- 当前 Excel P-W 列的数据已经通过 Skills 解读填充完毕，数据质量可靠
- 向量化技术选型暂定使用 OpenAI text-embedding-3-small，后续可调整
- 17 条样本数据量较小，MVP 阶段采用纯文件 + 实时 Embedding 计算方案
- 用户具备基本的 Markdown 文件编辑能力

---

## Clarifications *(resolved 2026-03-05)*

### CLR-001: 向量索引更新策略

**Question**: 当新增或修改样本的 summary.md 后，向量索引应如何更新？

**Decision**: **实时更新** - 每次保存 summary.md 后立即重新向量化。

**Rationale**: 17 条数据量小，实时计算成本可忽略，且能保证用户始终查询到最新数据，更符合知识库的使用场景。

**Impact**: 
- FR-012 细化：系统 MUST 在 summary.md 保存后自动触发向量化更新
- 新增 FR-022：向量索引 SHOULD 支持增量更新（只更新变化的文档），避免全量重计算

---

### CLR-002: Embedding API 失败处理策略

**Question**: 当调用 Embedding API 失败时（网络超时、配额用尽、服务不可用），系统应如何处理？

**Decision**: **静默降级** - 记录失败日志，通知用户，允许继续其他操作。

**Rationale**: 查询功能不应因向量化失败而完全阻塞，用户可以继续使用其他功能（如数据录入、文档查看），同时被告知需要稍后重试向量检索。

**Impact**:
- 新增 FR-023：Embedding API 调用失败时，系统 MUST 记录详细错误日志（时间、错误类型、请求参数）
- 新增 FR-024：Embedding API 调用失败时，系统 MUST 向用户显示友好提示，说明功能临时不可用
- 新增 FR-025：系统 SHOULD 在 API 恢复后自动重试失败的向量化任务

---

## Vector Storage Evolution Guide *(2026-03-05)*

### 架构设计原则

当前架构采用**数据层与向量层解耦**设计，确保未来向量存储迁移的平滑性：

```
┌─────────────────────────────────────────────────────────────┐
│  数据层（稳定，不随存储方案变化）                              │
│  /dataset/interpretations/*/summary.md                     │
│  • 向量化的唯一数据源                                        │
│  • Markdown 纯文本格式，兼容任何 Embedding 模型              │
└─────────────────────────────────────────────────────────────┘
                              ↓ 向量化
┌─────────────────────────────────────────────────────────────┐
│  向量存储层（可替换）                                         │
│  • MVP: 纯文件 + 实时 Embedding 计算                        │
│  • 中期: Chroma 本地向量数据库                               │
│  • 长期: SQLite-vec / Milvus / Pinecone                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  检索接口层（抽象，接口稳定）                                  │
│  search(query: str) → list[sample_id]                      │
│  • 输入：用户自然语言查询                                    │
│  • 输出：相似度 Top-K 的样本 ID 列表                         │
│  • 内部实现可随时替换，不影响上层调用                          │
└─────────────────────────────────────────────────────────────┘
```

### 演进路线

| 阶段 | 数据规模 | 存储方案 | 特点 | 迁移触发条件 |
|------|----------|----------|------|--------------|
| **Phase 1 (MVP)** | 17-50 条 | 纯文件 + 实时计算 | 零部署成本，验证 RAG 效果 | 当前阶段 |
| **Phase 2** | 50-200 条 | Chroma 本地 | `pip install`，检索提速 | 查询延迟 > 30s |
| **Phase 3** | 200-1000 条 | SQLite-vec | 持久化，与现有结构兼容 | 需要复杂查询/持久化 |
| **Phase 4** | 1000+ 条 | Milvus / Pinecone | 分布式，高并发 | 多用户/生产环境 |

### 迁移工作量评估

| 改动范围 | 工作量 | 说明 |
|----------|--------|------|
| summary.md 文档 | ✅ 零改动 | 向量化的源数据不变 |
| Excel 元数据 | ✅ 零改动 | 与向量存储无关 |
| 解读文档格式 | ✅ 零改动 | YAML + Markdown 格式兼容所有方案 |
| Skills 输出 | ✅ 零改动 | 只管输出文档，不管向量存储 |
| 向量化逻辑 | ⚠️ 小改动 | 将向量写入数据库而非实时计算 |
| 检索逻辑 | ⚠️ 小改动 | 从「遍历计算」改为「数据库查询」|

### 各阶段迁移指南

#### MVP → Chroma（预计 1-2 天）

**前置条件**：查询延迟超过 30 秒，或样本量超过 50 条

**步骤**：
1. 安装依赖：`pip install chromadb`
2. 编写初始化脚本：遍历所有 summary.md，写入 Chroma collection
3. 修改检索函数：约 10-20 行代码改动
4. 验证：对比迁移前后的检索结果一致性

**代码示例**：
```python
# 初始化
import chromadb
client = chromadb.PersistentClient(path="./vector_db")
collection = client.get_or_create_collection("summaries")

# 导入数据
for sample_id in all_samples:
    content = read_summary(sample_id)
    collection.add(documents=[content], ids=[sample_id])

# 检索
def search(query: str, k: int = 3) -> list[str]:
    results = collection.query(query_texts=[query], n_results=k)
    return results['ids'][0]
```

#### Chroma → SQLite-vec（预计 2-3 天）

**前置条件**：需要 SQL 查询能力，或需要与现有 SQLite 数据整合

**步骤**：
1. 编译安装 sqlite-vec 扩展
2. 设计向量表结构
3. 编写数据迁移脚本
4. 修改检索逻辑为 SQL 查询

**表结构示例**：
```sql
CREATE VIRTUAL TABLE summary_vectors USING vec0(
    sample_id TEXT PRIMARY KEY,
    embedding float[1536]
);
```

### 迁移兼容性保证

为确保平滑迁移，系统设计遵循以下原则：

1. **单一数据源**：summary.md 是向量化的唯一输入，向量索引可随时从源文件重建
2. **统一主键**：sample_id 贯穿所有层，向量检索结果可直接关联详情数据
3. **接口抽象**：检索接口 `search(query) → sample_ids` 保持稳定，实现可替换
4. **无状态设计**：向量索引可删除重建，不影响原始数据完整性
