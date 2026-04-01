# Spec: 005 - 全范围性能数据捕捉增强

**Date**: 2026-03-31 | **Status**: Draft  
**Author**: AI Assistant | **Reviewer**: [待定]

---

## 一、背景与动机

### 1.1 当前问题

现有的数据提取 Skills 存在一个核心缺陷：**只提取离散点数据，丢失全范围曲线信息**。

| Skill | 当前提取 | 丢失数据 |
|-------|----------|----------|
| stress-strain | 5 个点（100%/200%/300% 定伸、拉伸强度、断裂伸长率） | 完整应力-应变曲线（数百个数据点） |
| DMA | 3 个点（tan δ @ 0℃/60℃、Tg） | -80℃ ~ 80℃ 完整温度扫描曲线 |
| Payne | 4 个参数（G'₀、G'∞、ΔG'、γc） | 0.1% ~ 100% 应变范围的完整曲线 |
| DSC | 1 个点（Tg） | 完整热流-温度曲线 |
| NMR | 离散化学位移峰 | 完整谱图数据（ppm vs intensity） |

### 1.2 用户核心需求

> "文献文字中只阐述某个点的性能数据，但图片中会有全范围的性能数据，这是我最关注的。"

用户需要的是：
1. **趋势分析**：不同官能化程度下，性能曲线形态的变化规律
2. **外推预测**：基于已有数据点，预测未测量区间的性能
3. **配方设计**：根据完整的性能包络，推荐最优配方

### 1.3 改进目标

| 指标 | 当前 | 目标 |
|------|------|------|
| 应力-应变数据点 | 5 点/样本 | 20-50 点/样本 |
| DMA 温度点 | 3 点/样本 | 20-30 点/样本 |
| Payne 应变点 | 4 参数/样本 | 15-25 点/样本 |
| DSC 温度点 | 1 点/样本 | 10-20 点/样本 |
| 曲线数字化成功率 | 0% | ≥80% |

---

## 二、技术方案

### 2.1 方案概览

采用**三层数据提取策略**：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         全范围数据提取策略                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Layer 1: 文献原始数据（最高优先级）                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • SI 中的原始数据表格（CSV/Excel）                                   │   │
│  │  • 文献正文中的完整数据表格                                           │   │
│  │  • 数据来源标记: "L1-原始数据"                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓ Fallback                                    │
│  Layer 2: 曲线数字化（中等优先级）                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • 使用 AI 视觉 + WebPlotDigitizer 算法                              │   │
│  │  • 从图像中自动提取曲线数据点                                         │   │
│  │  • 数据来源标记: "L2-曲线数字化"                                      │   │
│  │  • 置信度评估 + 不确定性区间                                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓ Fallback                                    │
│  Layer 3: AI 估读（最低优先级）                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • AI 模型直接从图像估读关键点                                        │   │
│  │  • 输出不确定性区间而非精确值                                         │   │
│  │  • 数据来源标记: "L3-AI估读"                                          │   │
│  │  • 仅在 Layer 1/2 均失败时使用                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 新增数据结构

#### 2.2.1 全范围曲线数据 Schema

```yaml
# 新增到 mechanical.md YAML front matter

data:
  # ... 现有离散点数据保持不变 ...

  # ===== 新增：全范围曲线数据 =====
  curves:
    stress_strain:                    # 应力-应变曲线
      source_type: "L2-digitized"     # L1-原始数据 | L2-digitized | L3-AI估读
      source_detail: "Figure 4a"      # 数据来源详情
      digitization_tool: "curve_digitizer_v1"  # 数字化工具版本
      confidence: 0.85                # 置信度 (0-1)
      x_label: "strain"               # X 轴标签
      x_unit: "%"                     # X 轴单位
      y_label: "stress"               # Y 轴标签
      y_unit: "MPa"                   # Y 轴单位
      data_points:                    # 数据点数组
        - [0, 0]                      # [应变%, 应力MPa]
        - [10, 0.3]
        - [20, 0.5]
        - [50, 0.8]
        - [100, 1.5]
        - [150, 2.8]
        - [200, 4.5]
        - [250, 6.8]
        - [300, 9.0]
        - [350, 11.5]
        - [400, 13.8]
        - [452, 15.0]                 # 断裂点
      uncertainty:                    # 不确定性估计
        x_error: 2                    # X 轴误差 ±2%
        y_error: 0.3                  # Y 轴误差 ±0.3 MPa
      
    dma_tan_delta:                    # DMA tan δ-温度曲线
      source_type: "L2-digitized"
      source_detail: "Figure 6"
      confidence: 0.82
      x_label: "temperature"
      x_unit: "℃"
      y_label: "tan_delta"
      y_unit: "-"
      data_points:
        - [-80, 0.02]
        - [-60, 0.05]
        - [-40, 0.15]
        - [-30, 0.45]                 # 接近 Tg
        - [-25, 0.68]                 # Tg 附近
        - [-20, 0.52]
        - [0, 0.25]                   # 湿地抓地力参考温度
        - [20, 0.15]
        - [40, 0.10]
        - [60, 0.08]                  # 滚动阻力参考温度
        - [80, 0.06]
      uncertainty:
        x_error: 2
        y_error: 0.02

    payne_effect:                     # Payne 效应曲线
      source_type: "L2-digitized"
      source_detail: "Figure 5b"
      confidence: 0.88
      x_label: "strain"
      x_unit: "%"
      y_label: "storage_modulus"
      y_unit: "kPa"
      x_scale: "log"                  # X 轴对数坐标
      data_points:
        - [0.1, 2500]                 # G'₀
        - [0.2, 2450]
        - [0.5, 2350]
        - [1.0, 2100]
        - [2.0, 1800]
        - [5.0, 1450]
        - [10.0, 1200]
        - [20.0, 1050]
        - [50.0, 950]
        - [100.0, 900]                # G'∞
      uncertainty:
        x_error: 0.05                 # 对数坐标下的误差
        y_error: 50

  # 曲线特征参数（从全范围数据计算）
  curve_features:
    stress_strain:
      initial_modulus:                # 初始模量 (0-10% 斜率)
        value: 0.03
        unit: "MPa/%"
        source: "calculated"
      yield_strain:                   # 屈服应变（如果存在）
        value: null
        unit: "%"
        source: "not observed"
      hardening_index:                # 硬化指数
        value: 1.8
        unit: "-"
        source: "calculated"
        
    dma_tan_delta:
      peak_width:                     # tan δ 峰宽度
        value: 25
        unit: "℃"
        source: "calculated"
      peak_height:                    # tan δ 峰高
        value: 0.68
        unit: "-"
        source: "calculated"
      secondary_transitions:          # 次级转变
        value: null
        source: "not observed"
```

#### 2.2.2 DSC 全范围数据 Schema

```yaml
# dsc.md 新增字段

data:
  tg:                                 # 保持不变
    value: -25.5
    unit: "℃"
    source: "Table 2"

  # ===== 新增：全范围曲线数据 =====
  curves:
    heat_flow:                        # 热流曲线
      source_type: "L2-digitized"
      source_detail: "Figure 7"
      confidence: 0.75
      x_label: "temperature"
      x_unit: "℃"
      y_label: "heat_flow"
      y_unit: "mW/mg"
      scan_rate: 10                   # 升温速率 ℃/min
      data_points:
        - [-100, -0.5]
        - [-80, -0.48]
        - [-60, -0.45]
        - [-40, -0.43]
        - [-30, -0.55]                # Tg onset
        - [-25, -0.70]                # Tg midpoint
        - [-20, -0.60]                # Tg end
        - [0, -0.40]
        - [50, -0.35]
        - [100, -0.30]
      uncertainty:
        x_error: 1
        y_error: 0.05

  curve_features:
    tg_onset:                         # Tg 起始温度
      value: -30
      unit: "℃"
      source: "calculated"
    tg_endpoint:                      # Tg 终止温度
      value: -20
      unit: "℃"
      source: "calculated"
    delta_cp:                         # 热容变化（从曲线计算）
      value: 0.15
      unit: "J/(g·℃)"
      source: "calculated"
      confidence: 0.6                 # 较低置信度
```

#### 2.2.3 NMR 全范围数据 Schema

```yaml
# nmr.md 新增字段

data:
  functionalization_degree:           # 保持不变
    value: 2.5
    unit: "wt%"
    source: "calculated"

  # ===== 新增：全范围谱图数据 =====
  curves:
    spectrum:                         # ¹H NMR 谱图
      source_type: "L2-digitized"
      source_detail: "Figure 2"
      confidence: 0.70                # NMR 谱图数字化较难
      x_label: "chemical_shift"
      x_unit: "ppm"
      y_label: "intensity"
      y_unit: "a.u."
      frequency: 400                  # 仪器频率 MHz
      solvent: "CDCl3"                # 溶剂
      
      # 简化的谱图数据（关键区域）
      regions:                        # 分区域存储
        - name: "aromatic"            # 芳香区
          range: [6.5, 7.5]
          peaks:                      # 峰列表
            - [7.2, 100, "苯乙烯苯环"]  # [ppm, 相对强度, 归属]
            
        - name: "vinyl"               # 乙烯基区
          range: [4.8, 5.8]
          peaks:
            - [5.0, 45, "1,2-乙烯基 =CH₂"]
            - [5.4, 30, "1,4-乙烯基 =CH-"]
            
        - name: "functional_group"    # 官能团区
          range: [2.5, 4.5]
          peaks:
            - [3.6, 15, "官能化基团 -CH₂-O-"]
            
        - name: "backbone"            # 主链区
          range: [0.5, 2.5]
          peaks:
            - [1.3, 200, "主链 -CH₂-"]
            - [2.0, 80, "主链 -CH-"]

  curve_features:
    vinyl_content:                    # 乙烯基含量
      value: 63
      unit: "mol%"
      source: "calculated from spectrum"
    styrene_content:                  # 苯乙烯含量
      value: 25
      unit: "wt%"
      source: "calculated from spectrum"
```

---

## 三、曲线数字化模块设计

### 3.1 模块架构

```
scripts/
├── curve_digitizer/                  # 曲线数字化模块
│   ├── __init__.py
│   ├── digitizer.py                  # 核心数字化器
│   ├── axis_detector.py              # 坐标轴检测
│   ├── curve_extractor.py            # 曲线提取
│   ├── data_validator.py             # 数据验证
│   └── models/                       # 预训练模型
│       └── axis_detection.onnx       # 坐标轴检测模型
│
├── utils/
│   └── image_processor.py            # 图像预处理
```

### 3.2 数字化流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         曲线数字化流水线                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Step 1: 图像预处理                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • 从 PDF 提取指定 Figure 区域                                        │   │
│  │  • 去噪、二值化、透视校正                                              │   │
│  │  • 识别图像类型（曲线图/条形图/散点图）                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                             │
│  Step 2: 坐标轴检测                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • 检测 X/Y 轴位置和范围                                              │   │
│  │  • OCR 识别刻度标签和单位                                             │   │
│  │  • 检测对数/线性坐标                                                  │   │
│  │  • 输出: axis_bounds, scale_type, unit                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                             │
│  Step 3: 曲线追踪                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • 颜色分割：分离不同颜色的曲线                                        │   │
│  │  • 边缘检测：提取曲线骨架                                             │   │
│  │  • 点采样：沿曲线均匀采样数据点                                        │   │
│  │  • 坐标转换：像素坐标 → 物理坐标                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                             │
│  Step 4: 数据验证与后处理                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • 物理合理性检验（单调性、范围）                                       │   │
│  │  • 噪声过滤与平滑                                                     │   │
│  │  • 不确定性估计                                                       │   │
│  │  • 与文献离散点交叉验证                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ↓                                             │
│  Step 5: 输出                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  • 生成标准化 YAML 数据结构                                           │   │
│  │  • 输出置信度评分                                                     │   │
│  │  • 生成可视化校验图                                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 核心算法

#### 3.3.1 坐标轴检测

```python
class AxisDetector:
    """检测图像中的坐标轴"""
    
    def detect(self, image: np.ndarray) -> AxisInfo:
        """
        输入: 图像
        输出: 坐标轴信息
        """
        # 1. Hough 线变换检测轴线
        # 2. OCR 识别刻度标签
        # 3. 推断坐标系参数
        return AxisInfo(
            x_range=(0, 500),       # X 轴范围
            y_range=(0, 20),        # Y 轴范围
            x_unit="%",             # X 单位
            y_unit="MPa",           # Y 单位
            x_scale="linear",       # 线性/对数
            y_scale="linear",
            origin_pixel=(100, 400) # 原点像素坐标
        )
```

#### 3.3.2 曲线提取

```python
class CurveExtractor:
    """从图像中提取曲线数据点"""
    
    def extract(
        self, 
        image: np.ndarray, 
        axis_info: AxisInfo,
        target_color: Optional[Tuple[int, int, int]] = None
    ) -> CurveData:
        """
        输入: 图像、坐标轴信息、目标曲线颜色
        输出: 曲线数据点
        """
        # 1. 颜色分割
        if target_color:
            mask = self._color_segment(image, target_color)
        else:
            mask = self._auto_detect_curve(image)
        
        # 2. 骨架提取
        skeleton = morphology.skeletonize(mask)
        
        # 3. 有序点采样
        points_pixel = self._trace_skeleton(skeleton)
        
        # 4. 坐标转换
        points_physical = self._pixel_to_physical(
            points_pixel, axis_info
        )
        
        return CurveData(
            points=points_physical,
            confidence=self._estimate_confidence(points_pixel),
            uncertainty=self._estimate_uncertainty(axis_info)
        )
```

### 3.4 不同曲线类型的处理策略

| 曲线类型 | 特殊处理 | 预期精度 |
|----------|----------|----------|
| 应力-应变曲线 | 检测断裂点、屈服点 | ±2% 应变, ±5% 应力 |
| DMA tan δ 曲线 | 检测峰位、峰宽 | ±2℃, ±0.02 tan δ |
| Payne 效应曲线 | 对数 X 轴处理 | ±10% 应变, ±5% G' |
| DSC 曲线 | 基线校正、Tg 检测 | ±2℃, ±10% 热流 |
| NMR 谱图 | 峰分离、积分计算 | ±0.02 ppm, ±10% 积分 |

---

## 四、Skill 改进计划

### 4.1 修改策略

采用**增量式改进**，保持现有功能的同时增加全范围数据提取能力。

### 4.2 各 Skill 改进点

#### 4.2.1 ssbr-stress-strain-interpretation

**新增提取项**：

```diff
+ ## 新增：全范围曲线数据提取
+ 
+ ### 步骤 X：应力-应变曲线数字化
+ 
+ **触发条件**：文献包含应力-应变曲线图
+ 
+ **执行流程**：
+ 1. 识别图中目标样本对应的曲线（通过图例匹配）
+ 2. 调用曲线数字化模块提取数据点
+ 3. 验证数据点与已知离散值的一致性（100%/200%/300% 定伸）
+ 4. 计算曲线特征参数（初始模量、硬化指数）
+ 
+ **输出格式**：
+ ```yaml
+ curves:
+   stress_strain:
+     source_type: "L2-digitized"
+     data_points: [[0, 0], [10, 0.3], ...]
+     confidence: 0.85
+ ```
+ 
+ **交叉验证规则**：
+ - 数字化 stress(100%) 与文献值偏差 ≤ 10%
+ - 数字化 stress(300%) 与文献值偏差 ≤ 10%
+ - 断裂点与文献伸长率偏差 ≤ 5%
```

#### 4.2.2 ssbr-dma-interpretation

**新增提取项**：

```diff
+ ## 新增：全范围 DMA 曲线提取
+ 
+ ### 步骤 X：tan δ-温度曲线数字化
+ 
+ **数据点采样策略**：
+ - 低温区（-80℃ ~ Tg-10℃）：每 10℃ 一个点
+ - Tg 区域（Tg±15℃）：每 5℃ 一个点（高密度采样）
+ - 高温区（Tg+10℃ ~ 80℃）：每 10℃ 一个点
+ 
+ **峰检测**：
+ - 主峰位置 → Tg
+ - 峰高 → tan δ max
+ - 半高宽 → 表征分子链运动分布
+ - 次级峰 → 可能的相分离或 β 转变
+ 
+ **轮胎性能关联**：
+ | 温度区间 | 性能关联 | 提取要求 |
+ |----------|----------|----------|
+ | -30℃ ~ 0℃ | 冰地抓地力 | 密集采样 |
+ | 0℃ ~ 30℃ | 湿地抓地力 | 密集采样 |
+ | 50℃ ~ 80℃ | 滚动阻力 | 标准采样 |
```

#### 4.2.3 ssbr-payne-interpretation

**新增提取项**：

```diff
+ ## 新增：全范围 Payne 效应曲线提取
+ 
+ ### 步骤 X：G'-应变曲线数字化
+ 
+ **对数坐标处理**：
+ - X 轴通常为对数坐标，需检测并正确转换
+ - 采样点分布：0.1%, 0.2%, 0.5%, 1%, 2%, 5%, 10%, 20%, 50%, 100%
+ 
+ **关键参数提取**：
+ - G'₀：低应变平台区（γ < 0.5%）的平均值
+ - G'∞：高应变平台区（γ > 50%）的平均值
+ - γc：G' 下降 50% 时的临界应变
+ - dG'/dγ 曲线：从 G' 数据计算斜率
+ 
+ **多级网络检测**：
+ - 如果 G'-γ 曲线存在多个下降阶段，分别标注
+ - 可能指示：填料-填料网络 + 填料-橡胶网络
```

#### 4.2.4 ssbr-dsc-interpretation

**新增提取项**：

```diff
+ ## 新增：全范围 DSC 曲线提取
+ 
+ ### 步骤 X：热流曲线数字化
+ 
+ **基线校正**：
+ - 自动检测玻璃化转变前后的基线
+ - 计算校正后的热流信号
+ 
+ **特征提取**：
+ - Tg onset：切线法确定起始温度
+ - Tg midpoint：拐点温度
+ - Tg endpoint：切线法确定终止温度
+ - ΔTg：玻璃化转变宽度
+ - ΔCp：热容变化（如果基线质量足够）
+ 
+ **注意事项**：
+ - ΔCp 置信度较低，需标注 confidence < 0.6
+ - 多峰情况需分别标注
```

### 4.3 新增 Skill: curve-digitizer-core

创建一个核心 Skill 供其他 Skills 调用：

```yaml
name: curve-digitizer-core
description: 曲线数字化核心模块
version: 1.0.0

capabilities:
  - axis_detection          # 坐标轴检测
  - curve_extraction        # 曲线提取
  - data_validation         # 数据验证
  - uncertainty_estimation  # 不确定性估计

supported_curve_types:
  - stress_strain           # 应力-应变曲线
  - dma_tan_delta           # DMA tan δ 曲线
  - payne_effect            # Payne 效应曲线
  - dsc_heat_flow           # DSC 热流曲线
  - nmr_spectrum            # NMR 谱图

output_format: yaml         # 输出 YAML 格式数据
```

---

## 五、实现路线图

### Phase 1: 基础设施（Week 1-2）

| 任务 | 描述 | 优先级 |
|------|------|--------|
| 5.1.1 | 扩展 YAML Schema 支持全范围曲线数据 | P0 |
| 5.1.2 | 创建 `scripts/curve_digitizer/` 模块框架 | P0 |
| 5.1.3 | 实现基础图像预处理功能 | P0 |
| 5.1.4 | 实现坐标轴检测算法（线性坐标） | P0 |

### Phase 2: 核心数字化能力（Week 3-4）

| 任务 | 描述 | 优先级 |
|------|------|--------|
| 5.2.1 | 实现曲线追踪与提取算法 | P0 |
| 5.2.2 | 支持对数坐标轴 | P1 |
| 5.2.3 | 实现不确定性估计 | P1 |
| 5.2.4 | 实现数据验证与交叉校验 | P0 |

### Phase 3: Skill 集成（Week 5-6）

| 任务 | 描述 | 优先级 |
|------|------|--------|
| 5.3.1 | 更新 ssbr-stress-strain-interpretation | P0 |
| 5.3.2 | 更新 ssbr-dma-interpretation | P0 |
| 5.3.3 | 更新 ssbr-payne-interpretation | P1 |
| 5.3.4 | 更新 ssbr-dsc-interpretation | P1 |

### Phase 4: 验证与优化（Week 7-8）

| 任务 | 描述 | 优先级 |
|------|------|--------|
| 5.4.1 | 对 10 个样本进行全流程测试 | P0 |
| 5.4.2 | 精度评估与参数调优 | P0 |
| 5.4.3 | 更新 RAG 系统支持曲线数据检索 | P1 |
| 5.4.4 | 文档与培训 | P2 |

---

## 六、依赖与风险

### 6.1 技术依赖

| 依赖 | 用途 | 备选方案 |
|------|------|----------|
| OpenCV | 图像处理 | scikit-image |
| pytesseract | OCR 识别刻度 | EasyOCR |
| scikit-image | 形态学处理 | - |
| scipy | 曲线拟合 | numpy |

### 6.2 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 低质量图像导致数字化失败 | 中 | 高 | 提供人工校验入口 |
| OCR 刻度识别错误 | 中 | 高 | 交叉验证 + 物理约束检查 |
| 多曲线分离困难 | 中 | 中 | 用户指定目标曲线颜色 |
| 不同文献图表风格差异大 | 高 | 中 | 预训练多种图表类型 |

### 6.3 性能预期

| 指标 | 目标值 |
|------|--------|
| 单张图像处理时间 | ≤ 5 秒 |
| 坐标轴检测成功率 | ≥ 90% |
| 曲线数字化成功率 | ≥ 80% |
| 数值精度（与原始数据对比） | ±10% |

---

## 七、验收标准

### 7.1 功能验收

- [ ] 能够从应力-应变曲线图提取 ≥20 个数据点
- [ ] 能够从 DMA 曲线图提取 -80℃ 到 80℃ 范围的数据
- [ ] 能够处理对数坐标的 Payne 效应曲线
- [ ] 数字化数据与文献离散点偏差 ≤ 10%
- [ ] 输出标准 YAML 格式，可直接写入解读文档

### 7.2 质量验收

- [ ] 每个数据点附带不确定性估计
- [ ] 提供置信度评分（0-1）
- [ ] 低置信度（<0.7）时自动标记需人工校验
- [ ] 生成可视化校验图便于人工审核

### 7.3 集成验收

- [ ] 更新后的 Skills 能正常调用曲线数字化模块
- [ ] 全范围数据可被 RAG 系统索引和检索
- [ ] 向量搜索支持基于曲线形态的相似性匹配

---

## 八、附录

### 8.1 曲线数据示例

完整的应力-应变曲线数据示例：

```yaml
curves:
  stress_strain:
    source_type: "L2-digitized"
    source_detail: "Figure 4a, 红色曲线"
    digitization_tool: "curve_digitizer_v1.0"
    digitization_date: "2026-03-31"
    confidence: 0.87
    x_label: "strain"
    x_unit: "%"
    y_label: "stress"
    y_unit: "MPa"
    data_points:
      - [0, 0]
      - [5, 0.15]
      - [10, 0.28]
      - [15, 0.40]
      - [20, 0.52]
      - [30, 0.72]
      - [40, 0.90]
      - [50, 1.08]
      - [60, 1.22]
      - [70, 1.38]
      - [80, 1.52]
      - [90, 1.65]
      - [100, 1.80]          # 验证点 vs 文献值 1.75
      - [120, 2.15]
      - [140, 2.55]
      - [160, 3.00]
      - [180, 3.50]
      - [200, 4.10]          # 验证点 vs 文献值 4.05
      - [220, 4.75]
      - [240, 5.50]
      - [260, 6.35]
      - [280, 7.30]
      - [300, 8.40]          # 验证点 vs 文献值 8.35
      - [320, 9.60]
      - [340, 10.95]
      - [360, 12.40]
      - [380, 13.90]
      - [400, 15.45]
      - [420, 16.80]
      - [440, 17.90]
      - [455, 18.50]         # 断裂点
    uncertainty:
      x_error: 2             # ±2% 应变
      y_error_percent: 5     # ±5% 相对误差
    validation:
      stress_100_literature: 1.75
      stress_100_digitized: 1.80
      deviation_100: 2.9%    # 偏差 2.9%，通过
      stress_200_literature: 4.05
      stress_200_digitized: 4.10
      deviation_200: 1.2%    # 偏差 1.2%，通过
      stress_300_literature: 8.35
      stress_300_digitized: 8.40
      deviation_300: 0.6%    # 偏差 0.6%，通过
      overall_status: "PASS"
```

### 8.2 相关文档

- `specs/002-rag-data-migration/data-model.md` - 数据模型定义
- `specs/002-rag-data-migration/contracts/yaml-schema.md` - YAML 格式规范
- `skills/*/SKILL.md` - 各 Skill 定义文件
