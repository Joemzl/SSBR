---
sample_id: SSBR-054
doi: 10.1016/j.polymer.2015.11.039
polymer:
  type: SSBR
  grade: Buna VSL 5025-2HM
  manufacturer: Lanxess
  is_functionalized: false
  functionalization_type: null
  styrene_content: 25.0 wt%
  vinyl_content: 50.0 mol%
  Mn: null
research_type: theoretical_modeling
model:
  type: multiscale
  scales:
    - microscale (molecular)
    - mesoscale (aggregate)
    - macroscale (continuum)
application: 增强弹性体动力学建模
data_completeness:
  mechanical: true
  dsc: false
  nmr: false
  tem: false
keywords:
  - 多尺度建模
  - 动态力学
  - 本构模型
  - Payne 效应
  - 时温等效
  - 计算材料学
---

# SSBR-054 综合档案

## 样本概述

SSBR-054 来自 Ivaneiko 等人 (Polymer, 2016) 的理论建模研究，使用多尺度方法模拟增强弹性体的动态力学行为，以 SSBR/SiO₂ 体系作为模型验证案例。

## 材料体系

### 基础聚合物
- **SSBR**: Buna VSL 5025-2HM（朗盛）
- **用途**: 模型验证样本
- **结构**: 高乙烯基、中等苯乙烯

### 填料体系
- **填料**: SiO₂（模型体系）
- **填充量**: 多个水平（用于模型验证）

## 核心发现

### 1. 多尺度建模框架

| 尺度 | 描述 | 方法 |
|------|------|------|
| 微观 | 分子链动力学 | 统计力学 |
| 介观 | 填料团聚体 | 有效介质 |
| 宏观 | 本构响应 | 连续介质 |

### 2. 模型预测能力

| 行为 | 预测精度 | 应用 |
|------|----------|------|
| 应力-应变 | ~5% | 配方优化 |
| Payne 效应 | 定性 | 填料分散 |
| 温度依赖 | ~10% | 使用条件 |

### 3. 关键机制

模型揭示的增强机制：
- 应变放大效应
- 界面层贡献
- 填料网络作用
- 动态解缠/缠结

## 技术亮点

| 维度 | 贡献 | 意义 |
|------|------|------|
| 理论 | 多尺度框架 | 机理理解 |
| 预测 | 本构模型 | 材料设计 |
| 验证 | 实验对比 | 可靠性 |

## 科学意义

本研究建立了增强弹性体的计算预测平台：
- 减少实验试错
- 指导配方设计
- 理解构效关系
- 加速材料开发

## 参考文献

Ivaneiko I, Toshchevikov V, Saphiannikova M, et al. Modeling of dynamic-mechanical behavior of reinforced elastomers using a multiscale approach[J]. Polymer, 2016, 82: 356-365.
