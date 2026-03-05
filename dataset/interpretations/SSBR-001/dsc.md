---
sample_id: SSBR-001
interpretation_type: dsc
source_figure: "文献 Fig.2 基础 SSBR 生胶 DSC 谱图"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-dsc-interpretation
created_at: 2026-03-05
updated_at: null

data:
  tg:
    value: -9.0
    range: null
    unit: "℃"
    source: "SI Table S6 (DMTA测得)"
  thermal_source: "Gao et al. RSC Advances, 2019, SI Table S6"
  working_temp_window:
    value: "-9℃以上"
    unit: "℃"
    source: "基于Tg推算"
  other_transitions:
    value: null
    source: "文献未报告其他热转变"
---

# DSC 热分析解读：SSBR-001

> **样本性质**: 空白未官能化 SSBR 生胶，作为本文献中所有官能化样本的热学性能对照组。

## 一、玻璃化转变

### 数值数据

| 指标 | 数值 | 单位 | 来源 |
|------|------|------|------|
| 玻璃化转变温度 (Tg) | -9.0 | ℃ | SI Table S6 (DMTA) |

### 测量条件

根据文献 Experimental Section：
- **测试方法**: DMTA (VA3000)
- **频率**: 10 Hz
- **升温速率**: 3 ℃/min
- **温度范围**: -80 ℃ 至 100 ℃
- **应变振幅**: 0.1%

> 注：文献 Fig.2 为 DSC 测试的生胶（未填充白炭黑），而 SI Table S6 的 Tg 数据来自 DMTA 测试的复合材料。两种测试方法的 Tg 值可能略有差异。

### 核心发现

1. **典型 SSBR Tg**: -9.0℃ 的玻璃化转变温度属于溶聚丁苯橡胶的典型范围，说明该 SSBR 基体具有合适的分子链运动能力。

2. **无官能化影响**: 作为空白对照组，该样本的 Tg 未受到任何官能化改性的影响，反映了 SSBR 基体的本征热学性质。

3. **与绿色轮胎需求匹配**: Tg 在 -10℃ 附近有利于平衡轮胎的滚动阻力和湿地抓地力。

### 与官能化样本对比

| 样本 | Tg (℃) | ΔTg |
|------|--------|-----|
| SSBR-001 (空白) | -9.0 | 基准 |
| SSBR-g-MPL70 | -0.9 | +8.1 ℃ |
| SSBR-g-MUA70 | -2.1 | +6.9 ℃ |
| SSBR-g-MPTES70 | -1.1 | +7.9 ℃ |

### 分析结论

文献 Fig.2 及相关讨论指出：
- 空白 SSBR 的 Tg 值较低（-9.0℃），是因为未引入极性官能团
- 官能化后 Tg 升高的主要原因：
  - **SSBR-g-MPL70**: 羟基(-OH)的极性增强了分子间作用力
  - **SSBR-g-MUA70**: 羧基(-COOH)引入极性，但柔性烷基侧链部分抵消了分子间作用力
  - **SSBR-g-MPTES70**: 硅氧烷基团极性较低，Tg 变化相对较小

---

## 二、其他热转变

文献未报告空白 SSBR 在 DSC 测试中存在其他明显的热转变（如结晶、熔融等），表明该 SSBR 为无定形聚合物，体系均一性良好。

---

## 三、高弹性工作温度窗口

基于 Tg 数据估算材料的有效工作温度范围：

- **下限**: Tg + 10℃ ≈ 1℃
- **推荐工作温度**: 0℃ 以上
- **上限**: 无明显热分解峰报告，通常 SSBR 可在 150℃ 以下长期使用

**应用场景匹配**: 
- Tg = -9.0℃ 适合用于需要在较宽温度范围内保持弹性的应用
- 对于绿色轮胎胎面胶，该 Tg 值有利于低温抓地性能

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **图注引用**: Fig.2 基础 SSBR 生胶 DSC 谱图
- **表格引用**: SI Table S6 (动态力学性能参数)
