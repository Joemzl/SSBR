---
# SSBR-007 形貌解读
sample_id: SSBR-007
test_type: morphology
data_source: "10.1002/app.41182"
data_quality: L2

# 表征方法
characterization_methods:
  SEM:
    available: true
    equipment: "ZEISS EVO 60"
    sample_prep: "低温断裂 + 甲苯萃取 S-EB-S 相 (25°C, 72h)"
    figures: ["Fig. 3a,b", "Fig. 3c,d", "Fig. 4a,b"]
  AFM:
    available: true
    equipment: "Agilent 5500 Scanning Probe Microscope"
    mode: "间歇接触模式 (ACAFM)"
    tip_frequency: "146-236 kHz"
    force_constant: "48 N/m"
    figures: ["Fig. 5a,b", "Fig. 6a,b"]
  TEM:
    available: false
    reason: "文献未使用 TEM 表征"

# 形态学观察
morphology_observations:
  initial_TPV:
    SEV_system:
      type: "共连续形态 + 拉长的橡胶粒子"
      description: "Fig. 3b 可见拉长的橡胶粒子"
      rubber_phase: "交联的 S-SBR"
      matrix_phase: "S-EB-S"
    EV_system:
      type: "共连续形态"
      description: "Fig. 3d 未见拉长粒子"
      rubber_phase: "交联的 S-SBR"
      matrix_phase: "S-EB-S"
  after_reprocessing:
    SEV_system:
      type: "共连续 + 分散液滴形态"
      description: "再加工后形成部分液滴状形态"
      particle_size: "微米级"
      figure: "Fig. 4a, Fig. 6a"
    EV_system:
      type: "共连续形态 (无显著变化)"
      description: "再加工后形态基本不变"
      figure: "Fig. 4b, Fig. 6b"
---

## 形貌解读

### 概述

本文献使用 SEM 和 AFM 对 S-EB-S/S-SBR TPV 的形态进行了详细表征。由于是共混物体系而非纳米填料体系，未使用 TEM。形态学研究揭示了不同硫化体系（SEV vs EV）和再加工对 TPV 微观结构的影响。

### 样品制备方法

**SEM 样品**:
1. 低温断裂（液氮冷冻）
2. 甲苯溶剂萃取 S-EB-S 相（25°C，72h）
3. 60°C 干燥 24h
4. 金属镀层后观察

**AFM 样品**:
1. 压模制备薄膜（160°C，5 MPa，4 min）
2. 清洁干燥后直接观察

### 初始 TPV 形态

#### SEV 硫化体系（SST 1）

| 特征 | 描述 | 图像来源 |
|------|------|----------|
| 形态类型 | 共连续形态 | Fig. 3a (500×), Fig. 5a |
| 橡胶相 | 拉长的橡胶粒子可见 | Fig. 3b (3000×) |
| 萃取后 | 保持自支撑结构 | 证实共连续形态 |

形成拉长粒子的原因：
- SEV 体系形成二硫键和多硫键（键能较低）
- 弹性网络的弹性较低
- 混合剪切力可使橡胶相产生一定变形

#### EV 硫化体系（SST 2）

| 特征 | 描述 | 图像来源 |
|------|------|----------|
| 形态类型 | 共连续形态 | Fig. 3c (500×), Fig. 5b |
| 橡胶相 | 无拉长粒子 | Fig. 3d (3000×) |
| 萃取后 | 保持自支撑结构 | 证实共连续形态 |

无拉长粒子的原因：
- EV 体系形成单硫键（键能较高）
- 弹性网络的弹性更高
- 混合剪切力不足以使高弹性橡胶相变形

### 再加工后形态变化

#### SEV 体系（SST 1R）

再加工后观察到显著的形态变化：
- **部分液滴形态形成**: 拉长的橡胶粒子被剪切成球形微液滴
- **双重形态**: 共连续结构与分散液滴共存
- **性能影响**: 液滴作为增强填料，提高力学性能

这解释了为什么 SEV 体系再加工后拉伸强度从 4.9 MPa 提高到 6.3 MPa。

#### EV 体系（SST 2R）

再加工后形态基本无变化：
- **保持共连续形态**: 高弹性橡胶相抵抗剪切变形
- **临界应力未达到**: 混合剪切力不足以破坏高弹性网络
- **性能影响**: 力学性能略有下降（可能由于轻微降解）

### AFM 相图分析

AFM 相图中：
- **浅黄色区域**: 交联橡胶粒子（较硬）
- **棕色区域**: S-EB-S 相（TPE 基体）

两种体系的 AFM 相图均清晰显示共连续形态，与 SEM 观察结果一致。

### 形态-性能关联

| 体系 | 形态特征 | 断裂伸长率 | 再加工后变化 |
|------|----------|-----------|--------------|
| SEV (SST 1) | 共连续 + 拉长粒子 | 672% | 强度↑, 伸长率不变 |
| EV (SST 2) | 纯共连续 | 533% | 强度↓, 伸长率↓ |

拉长粒子的存在有利于提高断裂伸长率，这与 SST 1 比 SST 2 伸长率高 26% 的结果一致。

### 关键发现

1. **共连续形态**: 两种体系均形成共连续形态，证实了 TPV 的成功制备
2. **硫化体系影响**: SEV 体系的弹性网络弹性较低，更易在剪切下变形
3. **再加工效应**: SEV 体系可通过再加工优化形态，改善性能
4. **临界剪切应力**: EV 体系的高弹性网络需要更高剪切力才能发生形态重排

### 数据来源

- Fig. 3: 初始 TPV 的 SEM 图像
- Fig. 4: 再加工后 TPV 的 SEM 图像
- Fig. 5: 初始 TPV 的 AFM 相图
- Fig. 6: 再加工后 TPV 的 AFM 相图
