# RAG 检索系统评估报告

**生成时间**: 2026-03-07 21:30:29  
**评估参数**: Top-K = 5  
**测试用例数**: 12

---

## 1. 总体指标

| 指标 | 数值 | 说明 |
|------|------|------|
| **Hit Rate@5** | 91.7% (11/12) | Top-5 结果中包含 relevant 样本的查询比例 |
| **Avg Precision@5** | 55.0% | Top-5 结果中相关样本的平均比例 |
| **MRR** | 0.600 | Mean Reciprocal Rank，第一个正确结果的平均排名倒数 |

---

## 2. 分类别指标

| 类别 | 查询数 | Hit Rate | Avg Precision |
|------|--------|----------|---------------|
| Payne效应 | 1 | 100.0% | 40.0% |
| 分散性 | 2 | 100.0% | 60.0% |
| 力学性能 | 2 | 100.0% | 60.0% |
| 动态性能 | 3 | 100.0% | 53.3% |
| 热学性能 | 2 | 50.0% | 50.0% |
| 综合 | 2 | 100.0% | 60.0% |

---

## 3. 详细结果

### Q01: 改善白炭黑分散性

- **类别**: 分散性
- **命中**: ✅ (首个 relevant 排名: 2)
- **Precision@5**: 60.0%
- **标注 relevant**: SSBR-004, SSBR-008
- **检索结果**: SSBR-002, SSBR-004, SSBR-003, SSBR-016, SSBR-015

### Q02: 提高填料-橡胶界面结合强度

- **类别**: 分散性
- **命中**: ✅ (首个 relevant 排名: 1)
- **Precision@5**: 60.0%
- **标注 relevant**: SSBR-004, SSBR-008, SSBR-003
- **检索结果**: SSBR-004, SSBR-002, SSBR-003, SSBR-016, SSBR-015

### Q03: 降低轮胎滚动阻力

- **类别**: 动态性能
- **命中**: ✅ (首个 relevant 排名: 4)
- **Precision@5**: 20.0%
- **标注 relevant**: SSBR-015, SSBR-017, SSBR-016
- **检索结果**: SSBR-011, SSBR-012, SSBR-010, SSBR-015, SSBR-002

### Q04: 提高湿地抓地力

- **类别**: 动态性能
- **命中**: ✅ (首个 relevant 排名: 1)
- **Precision@5**: 80.0%
- **标注 relevant**: SSBR-015, SSBR-016
- **检索结果**: SSBR-016, SSBR-017, SSBR-015, SSBR-014, SSBR-004

### Q05: 同时提高抓地力和降低滚阻

- **类别**: 动态性能
- **命中**: ✅ (首个 relevant 排名: 2)
- **Precision@5**: 60.0%
- **标注 relevant**: SSBR-015, SSBR-016
- **检索结果**: SSBR-002, SSBR-016, SSBR-015, SSBR-003, SSBR-017

### Q06: 提高拉伸强度

- **类别**: 力学性能
- **命中**: ✅ (首个 relevant 排名: 1)
- **Precision@5**: 60.0%
- **标注 relevant**: SSBR-004, SSBR-003
- **检索结果**: SSBR-003, SSBR-002, SSBR-004, SSBR-006, SSBR-008

### Q07: 提高断裂伸长率和延展性

- **类别**: 力学性能
- **命中**: ✅ (首个 relevant 排名: 1)
- **Precision@5**: 60.0%
- **标注 relevant**: SSBR-002, SSBR-003
- **检索结果**: SSBR-002, SSBR-004, SSBR-003, SSBR-016, SSBR-015

### Q08: 改善低温性能

- **类别**: 热学性能
- **命中**: ❌ (首个 relevant 排名: N/A)
- **Precision@5**: 40.0%
- **标注 relevant**: SSBR-006, SSBR-007
- **检索结果**: SSBR-011, SSBR-010, SSBR-012, SSBR-004, SSBR-015

### Q09: 提高玻璃化转变温度

- **类别**: 热学性能
- **命中**: ✅ (首个 relevant 排名: 1)
- **Precision@5**: 60.0%
- **标注 relevant**: SSBR-004, SSBR-017, SSBR-003
- **检索结果**: SSBR-004, SSBR-002, SSBR-003, SSBR-006, SSBR-015

### Q10: 稳定填料网络结构

- **类别**: Payne效应
- **命中**: ✅ (首个 relevant 排名: 5)
- **Precision@5**: 40.0%
- **标注 relevant**: SSBR-007, SSBR-008
- **检索结果**: SSBR-002, SSBR-003, SSBR-006, SSBR-004, SSBR-008

### Q11: 绿色轮胎胎面胶配方

- **类别**: 综合
- **命中**: ✅ (首个 relevant 排名: 2)
- **Precision@5**: 80.0%
- **标注 relevant**: SSBR-015, SSBR-004, SSBR-016
- **检索结果**: SSBR-014, SSBR-016, SSBR-017, SSBR-015, SSBR-004

### Q12: 羧基官能化改性方案

- **类别**: 综合
- **命中**: ✅ (首个 relevant 排名: 4)
- **Precision@5**: 40.0%
- **标注 relevant**: SSBR-006, SSBR-015, SSBR-007, SSBR-016, SSBR-014, SSBR-017, SSBR-008, SSBR-003
- **检索结果**: SSBR-011, SSBR-010, SSBR-012, SSBR-007, SSBR-003

---

## 4. 评估方法说明

### 4.1 指标定义

- **Hit Rate@K**: 衡量系统是否能在 Top-K 结果中返回至少一个正确答案
- **Precision@K**: 衡量 Top-K 结果中正确答案的比例（包括 relevant 和 acceptable）
- **MRR (Mean Reciprocal Rank)**: 衡量第一个正确答案出现的位置，排名越靠前得分越高

### 4.2 标注说明

- **relevant**: 与查询直接相关的样本，必须出现才算命中
- **acceptable**: 可接受的相关样本，出现可提高 Precision，不影响 Hit

### 4.3 局限性

- 测试集规模较小（12 个查询），统计意义有限
- 标注带有主观性，不同标注者可能有不同判断
- 小规模知识库限制了检索难度

---

*本报告由 `scripts/evaluate_rag.py` 自动生成，用于学术评估目的。*
