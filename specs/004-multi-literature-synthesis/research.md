# Research Document: 多文献综合推理问答系统

**Feature**: 004-multi-literature-synthesis  
**Date**: 2026-03-24

## R1: Multi-sample Synthesis Prompt Design

**Question**: 如何设计 Prompt 让 LLM 有效综合多个样本的信息？

### Research Findings

**Best Practice: Structured Context + Explicit Instructions**

1. **样本呈现格式**：
   - 每个样本独立编号（方案 1、方案 2...）
   - 提取关键字段而非全量内容（减少 token）
   - 包含：官能团类型、官能化程度、关键性能指标

2. **综合指令设计**：
   ```
   你需要：
   1. 识别各方案的共同点和差异点
   2. 对比不同方案在目标性能上的表现
   3. 给出基于多方案的综合建议，而非推荐单一方案
   ```

3. **输出结构约束**：
   - 强制分层输出：结论摘要 → 支撑证据 → 文献来源
   - 每个观点必须标注数据来源

### Decision

采用 **结构化样本摘要 + 分步综合指令** 策略：
- 预处理阶段：从 summary.md 提取结构化字段
- Prompt 阶段：提供 5-8 个样本的摘要
- 后处理阶段：验证引用准确性

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| 全量内容拼接 | Token 限制，5 个 summary.md 约 10K tokens |
| 多轮对话分析 | 延迟增加 3-5 倍，成本增加 |
| 向量聚合后单样本呈现 | 丢失细节，无法对比 |

---

## R2: Extrapolation Control

**Question**: 如何在 Prompt 中精确控制外推边界（数据范围外 50%）？

### Research Findings

**Challenge**: LLM 默认倾向于给出"合理"答案，即使数据不足

**Solution: Explicit Boundary + Post-validation**

1. **Prompt 边界声明**：
   ```
   ## 外推规则
   - 数据覆盖范围：[min, max]（从样本提取）
   - 允许外推范围：[min × 0.5, max × 1.5]
   - 超出范围的查询必须拒绝，并说明数据边界
   ```

2. **后处理验证**：
   - 提取回答中的数值
   - 检查是否超出允许范围
   - 超出则追加警告或重新生成

3. **置信度三级标签**：
   - 高：数据点 ≥5 且在数据范围内
   - 中：数据点 3-4 或在外推区域
   - 低：数据点 <3 或接近边界

### Decision

采用 **Prompt 显式边界 + 后处理校验** 双重保障：
- Prompt 中注入数据范围信息
- 后处理验证数值边界
- 自动添加置信度标签

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| 纯 Prompt 控制 | LLM 可能忽略指令 |
| 数学模型外推 | 需要充足数据点，当前样本量不足 |
| 禁止外推 | 不满足用户需求 |

---

## R3: Trend Analysis Capability

**Question**: LLM 能否从结构化数据中识别定量趋势？

### Research Findings

**测试场景**：官能化程度 vs 力学性能

**结论**：LLM 能识别定性趋势，但定量精度有限

1. **能做到**：
   - "官能化程度增加，拉伸强度呈上升趋势"
   - "羟基官能化比羧基官能化分散效果更好"
   - 识别异常点和离群值

2. **不能做到**：
   - 精确的线性/非线性回归系数
   - 可靠的数值预测（如"5% 官能化对应 15.3 MPa"）

3. **最佳实践**：
   - 趋势描述用定性语言 + 支撑数据点
   - 数值预测给出区间而非点值
   - 明确标注"基于 X 个数据点估计"

### Decision

采用 **定性趋势 + 区间估计** 策略：
- 趋势分析输出定性结论 + 支撑数据
- 数值预测输出区间（如 "12-16 MPa"）
- 所有预测附带数据点数量

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| 线性回归模型 | 数据点太少（通常 3-5 个） |
| 禁止数值预测 | 用户明确需要外推能力 |
| 让 LLM 自由发挥 | 可能产生过于精确的虚假结论 |

---

## R4: Citation Accuracy

**Question**: 综合回答时如何确保引用准确性？

### Research Findings

**当前系统问题**：
- 使用 `[SSBR-XXX]` 格式引用，但用户不可见内部 ID
- 引用后处理会移除 ID，导致无法追溯

**解决方案：双层引用系统**

1. **内部层**：保留 sample_id 用于验证
2. **展示层**：转换为用户友好格式
   - "根据 Zhang 等人的研究[1]"
   - "硅烷官能化方案（文献 DOI: 10.xxx）"

3. **验证流程**：
   - 提取 LLM 回答中的引用
   - 校验引用的 sample_id 是否在输入列表中
   - 丢弃无效引用

### Decision

采用 **内部 ID + 展示转换 + 引用验证** 三层机制：
- LLM 使用内部编号（方案 1、方案 2）
- 后处理转换为文献引用格式
- 验证所有引用指向有效来源

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| 让 LLM 直接生成 DOI | 可能产生幻觉 DOI |
| 仅用描述性引用 | 无法精确追溯 |
| 不做引用验证 | 违反零幻觉原则 |

---

## R5: Response Time Optimization

**Question**: 扩展检索范围后如何保持 ≤8s 响应？

### Research Findings

**当前性能基线**（003 系统）：
- 向量检索（Top-10）：~200ms
- 重排序（Top-10 → Top-3）：~800ms
- LLM 生成：~2-4s
- **总计**：~3-5s

**扩展后预估**（Top-10 → Top-8）：
- 向量检索：~200ms（无变化）
- 重排序（Top-10 → Top-8）：~1s
- LLM 生成（更多 context）：~4-6s
- **总计**：~5-7s（在 8s 内）

**优化策略**：
1. **样本摘要预提取**：缓存结构化字段，避免实时解析
2. **Prompt 精简**：只传递关键字段，非全量 summary.md
3. **并行处理**：质量评分与重排序并行

### Decision

无需额外优化，当前架构可满足 8s 目标：
- 检索扩展到 Top-8（从 Top-3）
- Prompt 传递摘要而非全文
- 保持单次 LLM 调用

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| 流式输出 | 已支持，但不影响总时间 |
| 异步预生成 | 复杂度高，收益有限 |
| 减少检索数量 | 影响综合质量 |

---

## Summary of Decisions

| Research | Decision | Implementation Notes |
|----------|----------|---------------------|
| R1 | 结构化样本摘要 + 分步综合指令 | 新增样本摘要提取器 |
| R2 | Prompt 显式边界 + 后处理校验 | 新增外推验证器 |
| R3 | 定性趋势 + 区间估计 | Prompt 模板约束 |
| R4 | 内部 ID + 展示转换 + 引用验证 | 增强引用处理逻辑 |
| R5 | 无额外优化，当前架构满足 | 检索扩展到 Top-8 |

---

## Open Questions (Resolved in Clarifications)

所有关键问题已在 spec.md 的 Clarifications 章节解决：
- ✅ 外推边界 = 数据范围外 50%
- ✅ 输出结构 = 分层（结论 + 支撑）
- ✅ 数据矛盾 = 展示分歧并分析原因
- ✅ 置信度 = 三级标签 + 数据点数
- ✅ 最小样本数 = 对比≥2，趋势/外推≥3
