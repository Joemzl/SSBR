---
sample_id: SSBR-056
doi: 10.1016/j.polymer.2017.08.051
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
  type: superposition
  principles:
    - time-temperature superposition (TTS)
    - strain superposition
    - filler content superposition
application: 轮胎生产
data_completeness:
  mechanical: true (DMA)
  dsc: false
  nmr: false
  tem: false
keywords:
  - 叠加原理
  - 时温等效
  - WLF 方程
  - 动态力学
  - 轮胎材料
  - 主曲线
---

# SSBR-056 综合档案

## 样本概述

SSBR-056 来自 Ivaneiko 等人 (Polymer, 2017) 的理论建模研究，提出增强橡胶动态力学行为的叠加方法，为轮胎材料的性能预测提供计算工具。

## 材料体系

### 基础聚合物
- **SSBR**: Buna VSL 5025-2HM（朗盛）
- **用途**: 模型验证样本
- **应用**: 轮胎生产

### 研究重点
- 动态力学行为的统一描述
- 叠加原理的验证与扩展
- 预测模型的建立

## 核心发现

### 1. 叠加原理框架

| 叠加类型 | 变量 | 应用 |
|----------|------|------|
| 时温叠加 | 温度↔频率 | 主曲线构建 |
| 应变叠加 | 应变幅值 | Payne 效应 |
| 填料叠加 | 填料含量 | 增强预测 |

### 2. 主曲线构建

通过 WLF 方程实现宽频域预测：
- 实验频率: 0.01-100 Hz
- 叠加后: 10⁻⁴-10¹² Hz
- 覆盖所有轮胎使用条件

### 3. 轮胎性能关联

| 频率/温度 | 对应性能 | 预测指标 |
|-----------|----------|----------|
| 60°C/低频 | 滚动阻力 | tan δ @ 60°C |
| 0°C/中频 | 湿抓地力 | tan δ @ 0°C |
| -20°C/高频 | 冰面性能 | G' @ -20°C |

## 技术亮点

| 维度 | 方法 | 优势 |
|------|------|------|
| 预测范围 | 多重叠加 | 覆盖全工况 |
| 计算效率 | 解析模型 | 快速预测 |
| 工程应用 | 轮胎设计 | 实用价值 |

## 应用前景

叠加方法为轮胎材料开发提供：
- 快速性能筛选
- 配方优化指导
- 使用条件预测
- 减少实验成本

## 参考文献

Ivaneiko I, Toshchevikov V, Stöckelhuber K W, et al. Superposition approach to the dynamic-mechanical behaviour of reinforced rubbers[J]. Polymer, 2017, 131: 242-251.
