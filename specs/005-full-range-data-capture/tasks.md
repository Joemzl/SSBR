# 任务清单: 005 - 全范围性能数据捕捉增强

**Date**: 2026-03-31 | **Status**: In Progress

---

## 📋 任务总览

| Phase | 任务数 | 预估工时 | 状态 |
|-------|--------|----------|------|
| Phase 1: YAML Schema 扩展 | 4 | 1 天 | ✅ Done |
| Phase 2: Skill 文件更新 | 4 | 2 天 | ⬜ Ready |
| Phase 3: 试点验证 | 5 | 2 天 | ⬜ Blocked |
| Phase 4: 批量处理（可选） | 4 | 3 天 | ⬜ Future |

**总预估**: 8 天（Phase 1-3 核心功能）

---

## Phase 1: YAML Schema 扩展（1 天）✅ 已完成

### Task 1.1: 更新 yaml-schema.md
- **文件**: `specs/002-rag-data-migration/contracts/yaml-schema.md`
- **内容**: 
  - 新增 `curves` 字段规范
  - 新增 `data_points` 数组格式定义
  - 新增 `curve_features` 字段规范
  - 新增 `validation` 字段规范
- **验收标准**: Schema 文档完整，包含所有新字段的定义和示例
- **状态**: ✅ 已完成 (2026-03-31)

### Task 1.2: 更新 data-model.md
- **文件**: `specs/002-rag-data-migration/data-model.md`
- **内容**:
  - 新增"全范围曲线数据"章节
  - 更新数据层级说明（L1/L2/L3）
  - 新增置信度评分标准
- **验收标准**: 数据模型文档与 Schema 一致
- **状态**: ⏳ 待更新（非阻塞）

### Task 1.3: 创建 curve-data-schema.md
- **文件**: `specs/005-full-range-data-capture/contracts/curve-data-schema.md`
- **内容**:
  - 详细的曲线数据 JSON Schema
  - 各类曲线的专用字段
  - 验证规则定义
- **验收标准**: 可用于自动化验证
- **状态**: ✅ 已完成 (2026-03-31)

### Task 1.4: 创建验证脚本
- **文件**: `scripts/utils/curve_validator.py`
- **内容**:
  - 验证曲线数据格式
  - 检查置信度范围
  - 验证交叉校验结果
- **验收标准**: 能正确验证 YAML 中的曲线数据
- **状态**: ✅ 已完成 (2026-03-31)

---

## Phase 2: Skill 文件更新（2 天）

### Task 2.1: 更新 ssbr-stress-strain-interpretation
- **文件**: `skills/ssbr-stress-strain-interpretation/SKILL.md`
- **参考**: `specs/005-full-range-data-capture/SKILL-stress-strain-v2.md`
- **更新内容**:
  - version 升级到 2.0.0
  - 新增"全范围曲线数据捕捉"章节
  - 更新 YAML 模板
  - 新增估读示例
- **验收标准**: Skill 能指导 AI 提取 15+ 数据点
- **状态**: ⬜ 待开始

### Task 2.2: 更新 ssbr-dma-interpretation
- **文件**: `skills/ssbr-dma-interpretation/SKILL.md`
- **参考**: `specs/005-full-range-data-capture/SKILL-dma-v2.md`
- **更新内容**:
  - version 升级到 2.0.0
  - 新增全范围 tan δ-温度曲线估读
  - 新增轮胎性能关联计算
  - 新增峰特征识别
- **验收标准**: Skill 能指导 AI 提取 15+ 数据点
- **状态**: ⬜ 待开始

### Task 2.3: 更新 ssbr-payne-interpretation
- **文件**: `skills/ssbr-payne-interpretation/SKILL.md`
- **参考**: `specs/005-full-range-data-capture/SKILL-payne-v2.md`
- **更新内容**:
  - version 升级到 2.0.0
  - 新增全范围 G'-应变曲线估读
  - 处理对数坐标
  - 新增多级网络检测
- **验收标准**: Skill 能处理对数坐标并提取 10+ 数据点
- **状态**: ⬜ 待开始

### Task 2.4: 更新 ssbr-dsc-interpretation
- **文件**: `skills/ssbr-dsc-interpretation/SKILL.md`
- **参考**: `specs/005-full-range-data-capture/SKILL-dsc-v2.md`
- **更新内容**:
  - version 升级到 2.0.0
  - 新增全范围热流曲线估读
  - 新增玻璃化转变特征识别
  - 保持 ΔCp 不计算原则
- **验收标准**: Skill 能指导 AI 提取 12+ 数据点
- **状态**: ⬜ 待开始

---

## Phase 3: 试点验证（2 天）

### Task 3.1: 选择试点样本
- **输出**: 试点样本列表
- **选择标准**:
  - 图像质量高（清晰、无重叠）
  - 包含完整的已知数据点（用于交叉验证）
  - 覆盖不同曲线类型
- **数量**: 5 个样本
- **状态**: ⬜ 待开始
- **依赖**: Phase 2 完成

### Task 3.2: 应力-应变曲线验证
- **内容**:
  - 使用更新后的 Skill 解读试点样本
  - 记录估读数据点
  - 与文献已知值交叉验证
  - 计算偏差百分比
- **验收标准**: 平均偏差 < 10%
- **状态**: ⬜ 待开始

### Task 3.3: DMA 曲线验证
- **内容**:
  - 使用更新后的 Skill 解读试点样本
  - 验证 tan δ(0℃)、tan δ(60℃)、Tg
  - 评估置信度与实际精度的关联
- **验收标准**: 关键点偏差 < 15%
- **状态**: ⬜ 待开始

### Task 3.4: Payne 曲线验证
- **内容**:
  - 验证对数坐标处理
  - 验证 G'₀、G'∞、ΔG' 计算
- **验收标准**: 参数偏差 < 15%
- **状态**: ⬜ 待开始

### Task 3.5: 汇总验证报告
- **输出**: `specs/005-full-range-data-capture/validation-report.md`
- **内容**:
  - 各曲线类型的精度统计
  - 问题总结
  - 优化建议
- **状态**: ⬜ 待开始

---

## Phase 4: 批量处理（可选，3 天）

### Task 4.1: 批量解读脚本
- **文件**: `scripts/batch_curve_extraction.py`
- **功能**:
  - 遍历所有样本
  - 调用相应 Skill
  - 存储曲线数据
- **状态**: ⬜ Future

### Task 4.2: 人工审核界面
- **文件**: `demo/curve_review.py`
- **功能**:
  - 显示估读数据 vs 原图
  - 支持人工修正
  - 更新置信度
- **状态**: ⬜ Future

### Task 4.3: 更新 RAG 索引
- **内容**:
  - 将曲线数据纳入向量索引
  - 支持基于曲线特征的检索
- **状态**: ⬜ Future

### Task 4.4: 更新 summary.md 生成
- **文件**: `scripts/generate_summaries.py`
- **内容**:
  - 在 summary.md 中包含曲线特征摘要
- **状态**: ⬜ Future

---

## 📊 关键指标

### 数据丰富度目标

| 曲线类型 | 当前数据点 | 目标数据点 | 提升倍数 |
|----------|------------|------------|----------|
| 应力-应变 | 5 | 15-20 | 3-4x |
| DMA tan δ | 3 | 15-20 | 5-7x |
| Payne G' | 4 参数 | 10-15 | 2.5-4x |
| DSC | 1 | 10-15 | 10-15x |

### 精度目标

| 指标 | 目标 |
|------|------|
| 应力-应变关键点偏差 | < 10% |
| DMA 关键点偏差 | < 15% |
| Payne 参数偏差 | < 15% |
| 置信度-精度相关性 | > 0.7 |

---

## 🔗 文件依赖关系

```
specs/005-full-range-data-capture/
├── spec.md                     # 总体规范 ✅
├── plan.md                     # 实施计划 ✅
├── tasks.md                    # 任务清单（本文件）✅
├── quickstart.md               # 快速入门指南 ✅
├── contracts/
│   └── curve-data-schema.md    # 曲线数据 Schema ✅
├── SKILL-stress-strain-v2.md   # 应力-应变 Skill v2 ✅
├── SKILL-dma-v2.md             # DMA Skill v2 ✅
├── SKILL-payne-v2.md           # Payne Skill v2 ✅
├── SKILL-dsc-v2.md             # DSC Skill v2 ✅
└── validation-report.md        # 验证报告（Phase 3 产出）

scripts/utils/
└── curve_validator.py          # 曲线验证脚本 ✅

specs/002-rag-data-migration/contracts/
└── yaml-schema.md              # 已更新支持 curves 字段 ✅

skills/
├── ssbr-stress-strain-interpretation/
│   └── SKILL.md                # 待更新为 v2.0
├── ssbr-dma-interpretation/
│   └── SKILL.md                # 待更新为 v2.0
├── ssbr-payne-interpretation/
│   └── SKILL.md                # 待更新为 v2.0
└── ssbr-dsc-interpretation/
    └── SKILL.md                # 待更新为 v2.0
```

---

## ✅ 下一步行动

**Phase 1 已完成！** 🎉

**Phase 2 可立即执行的任务**：

1. **Task 2.1**: 将 `SKILL-stress-strain-v2.md` 内容合并到 `skills/ssbr-stress-strain-interpretation/SKILL.md`
2. **Task 2.2**: 将 `SKILL-dma-v2.md` 内容合并到 `skills/ssbr-dma-interpretation/SKILL.md`
3. **Task 2.3**: 将 `SKILL-payne-v2.md` 内容合并到 `skills/ssbr-payne-interpretation/SKILL.md`
4. **Task 2.4**: 将 `SKILL-dsc-v2.md` 内容合并到 `skills/ssbr-dsc-interpretation/SKILL.md`

**需要确认的问题**：

1. 是否立即开始 Phase 2（更新正式 Skill 文件）？
2. 更新方式：完全替换现有 Skill 还是追加新章节？
3. Phase 3 试点验证时是否需要人工参与？

---

**准备好开始 Phase 2 了吗？我可以立即更新正式的 Skill 文件。**
