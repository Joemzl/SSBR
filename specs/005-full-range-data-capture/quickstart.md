# 快速入门：全范围性能数据捕捉

**Version**: 1.0.0 | **Date**: 2026-03-31

---

## 📋 概述

本指南帮助你快速上手使用增强版 Skills 从文献图像中捕捉全范围性能数据。

---

## 🚀 5 分钟快速开始

### Step 1: 准备文献图像

确保你有以下类型的图像之一：
- 应力-应变曲线 (Stress-Strain Curve)
- DMA tan δ-温度曲线 (Dynamic Mechanical Analysis)
- Payne 效应曲线 (Storage Modulus vs Strain)
- DSC 热流曲线 (Differential Scanning Calorimetry)

### Step 2: 使用增强版 Skill

以 DMA 曲线为例，在 CodeBuddy 中输入：

```
使用 ssbr-dma-interpretation skill 解读以下 DMA tan δ-温度曲线图像。

[粘贴或上传图像]

请提取全范围数据，包括：
1. 从 -60°C 到 80°C 的完整曲线数据点
2. 关键特征值（tan δ(0°C)、tan δ(60°C)、Tg）
3. 曲线形态特征
```

### Step 3: 检查输出格式

AI 将输出包含 `curves` 部分的 YAML：

```yaml
curves:
  dma_tan_delta:
    data_points:
      - {x: -60, y: 0.05, confidence: 0.70, source: "L3"}
      - {x: -40, y: 0.45, confidence: 0.70, source: "L3"}
      # ... 更多数据点
    curve_features:
      tan_delta_0C:
        value: 0.35
        source: "L1"
```

### Step 4: 验证数据

运行验证脚本：

```bash
python scripts/utils/curve_validator.py --file dataset/interpretations/SSBR-XXX/mechanical.md
```

---

## 📊 各曲线类型使用指南

### 1. 应力-应变曲线

**触发 Skill**: `ssbr-stress-strain-interpretation`

**推荐提示词**:
```
请使用 ssbr-stress-strain-interpretation skill 解读这张应力-应变曲线。

要求：
1. 提取从 0% 到断裂点的全范围应力数据
2. 建议采样点：0, 50, 100, 150, 200, 250, 300%...直到断裂
3. 识别 100%、200%、300% 定伸应力和拉伸强度
4. 检测是否有屈服现象
```

**关键输出字段**:
- `curves.stress_strain.data_points` - 至少 10-15 个点
- `curves.stress_strain.curve_features.modulus_100` - 100% 定伸应力
- `curves.stress_strain.curve_features.tensile_strength` - 拉伸强度

---

### 2. DMA tan δ-温度曲线

**触发 Skill**: `ssbr-dma-interpretation`

**推荐提示词**:
```
请使用 ssbr-dma-interpretation skill 解读这张 DMA tan δ-温度曲线。

要求：
1. 提取从 -80°C 到 80°C 的全范围 tan δ 数据
2. 重点关注：-40°C ~ 0°C（转变区）需要更密集采样
3. 识别 tan δ(0°C)、tan δ(60°C)、Tg 和峰值
4. 评估峰宽度（半高宽）
```

**关键输出字段**:
- `curves.dma_tan_delta.data_points` - 至少 12-17 个点
- `curves.dma_tan_delta.curve_features.tan_delta_0C` - 湿地抓地力指标
- `curves.dma_tan_delta.curve_features.tan_delta_60C` - 滚动阻力指标
- `curves.dma_tan_delta.curve_features.Tg` - 玻璃化转变温度

---

### 3. Payne 效应曲线

**触发 Skill**: `ssbr-payne-interpretation`

**推荐提示词**:
```
请使用 ssbr-payne-interpretation skill 解读这张 Payne 效应 G'-应变曲线。

注意：X 轴通常是对数坐标！

要求：
1. 按对数间隔采样：0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100%
2. 识别 G'₀（低应变模量）和 G'∞（高应变模量）
3. 计算 ΔG' 和填料网络强度
4. 检测是否存在多级网络结构
```

**关键输出字段**:
- `curves.payne_storage_modulus.data_points` - 至少 8-12 个点（对数间隔）
- `curves.payne_storage_modulus.x_axis.scale` = "logarithmic"
- `curves.payne_storage_modulus.curve_features.delta_G_prime` - Payne 效应幅度

---

### 4. DSC 热流曲线

**触发 Skill**: `ssbr-dsc-interpretation`

**推荐提示词**:
```
请使用 ssbr-dsc-interpretation skill 解读这张 DSC 热流曲线。

要求：
1. 提取从 -80°C 到 50°C 的全范围热流数据
2. 在玻璃化转变区（Tg 附近 ±20°C）密集采样
3. 识别 Tg 的 onset、midpoint、endpoint
4. 检查是否有冷结晶或熔融峰
```

**关键输出字段**:
- `curves.dsc_heat_flow.data_points` - 至少 10-14 个点
- `curves.dsc_heat_flow.curve_features.Tg.midpoint` - 玻璃化转变温度
- `curves.dsc_heat_flow.curve_features.glass_transition_width` - 转变宽度

---

## 🎯 数据质量保证

### 置信度等级说明

| 数据来源 | 代码 | 建议置信度 | 说明 |
|----------|------|-----------|------|
| 文献表格数值 | L1 | 0.95 | 最可靠 |
| 图面标注数字 | L2 | 0.85 | 可靠 |
| 清晰曲线估读 | L3 | 0.70-0.75 | 可接受 |
| 一般曲线估读 | L3 | 0.60-0.70 | 需谨慎 |
| 模糊曲线估读 | L3 | 0.50-0.60 | 仅供参考 |

### 交叉验证

每次估读后，检查已知点偏差：

```yaml
validation:
  known_points:
    - strain: 100
      stress_expected: 2.5    # 文献给出的值
      stress_measured: 2.6    # 估读值
      deviation_percent: 4.0  # 偏差 4%，可接受
```

**质量标准**:
- Excellent: 偏差 < 5%
- Good: 偏差 5-10%
- Acceptable: 偏差 10-15%
- Poor: 偏差 > 15%（需要人工复核）

---

## 📁 文件存储位置

全范围曲线数据存储在解读文档的 YAML front matter 中：

```
dataset/interpretations/
├── SSBR-001/
│   ├── mechanical.md    ← 包含 stress_strain, payne 曲线
│   ├── dsc.md           ← 包含 dsc_heat_flow 曲线
│   └── summary.md
```

---

## ⚠️ 常见问题

### Q1: 图像分辨率低怎么办？

降低置信度，使用区间估读：
```yaml
data_points:
  - x: 100
    y: 2.5
    confidence: 0.55   # 低置信度
    source: "L3"
```

### Q2: 多条曲线重叠怎么办？

1. 优先读取目标曲线（通常是官能化样本）
2. 标注在 metadata 中：
```yaml
metadata:
  notes: "多曲线重叠，仅读取 SSBR-f 曲线"
```

### Q3: X 轴是对数坐标怎么处理？

在 `x_axis` 中标注：
```yaml
x_axis:
  label: "应变"
  unit: "%"
  scale: "logarithmic"
```

### Q4: 曲线超出图边界怎么办？

只记录可见部分，在 metadata 中说明：
```yaml
metadata:
  notes: "曲线在 400% 应变处超出图边界，实际断裂点未知"
```

---

## 🔧 验证工具使用

### 单文件验证

```bash
python scripts/utils/curve_validator.py --file dataset/interpretations/SSBR-001/mechanical.md
```

### 目录批量验证

```bash
python scripts/utils/curve_validator.py --dir dataset/interpretations/
```

### 静默模式（仅输出错误）

```bash
python scripts/utils/curve_validator.py --dir dataset/interpretations/ --quiet
```

---

## 📚 相关文档

- [完整规范](./spec.md) - 设计目标和技术方案
- [实施计划](./plan.md) - Phase 划分和时间线
- [任务清单](./tasks.md) - 详细任务和状态
- [曲线数据 Schema](./contracts/curve-data-schema.md) - 完整字段定义
- [YAML Schema](../002-rag-data-migration/contracts/yaml-schema.md) - 通用格式规范

---

**准备好了吗？选择一个曲线类型开始吧！** 🚀
