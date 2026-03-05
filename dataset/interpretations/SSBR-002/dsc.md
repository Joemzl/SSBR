# SSBR-002 DSC 热分析解读

```yaml
sample_id: SSBR-002
interpretation_type: dsc
data_version: "1.0"
created_at: 2026-03-05
source_doi: "10.1039/c9ra02783a"
source_figure: "SI Table S6"

thermal_properties:
  tg:
    value: -8.5
    unit: "℃"
    confidence: high
    method: DSC
  
  thermal_stability:
    decomposition_onset:
      value: null
      unit: "℃"
      confidence: null
    max_decomposition_rate:
      value: null
      unit: "℃"
      confidence: null
```

## 样本基本信息

- **样本编号**: SSBR-002
- **官能团类型**: 3-巯基丙醇（MPL）官能化 SSBR
- **功能基团**: -OH（羟基）
- **填料体系**: 白炭黑 (60 phr)
- **文献来源**: Gao et al., RSC Advances, 2019

## 热学性能数据

### 玻璃化转变温度 (Tg)

| 指标 | 数值 | 单位 | 测试方法 | 置信度 |
|------|------|------|----------|--------|
| Tg | -8.5 | ℃ | DSC | 高 |

### 热稳定性

暂无此项数据。

## 性能解读

### Tg 变化分析

SSBR-002（羟基官能化）的 Tg 为 -8.5℃，与空白 SSBR-001（Tg = -9.0℃）相比略有升高（+0.5℃）。

**Tg 升高原因分析**：
1. **界面约束效应**: 羟基与白炭黑表面形成氢键，增加了橡胶分子链的界面约束
2. **分子链运动受限**: 更强的填料-橡胶界面作用限制了分子链段运动
3. **交联网络影响**: 官能化可能影响硫化网络结构

### 对轮胎性能的影响

Tg 的轻微升高（0.5℃）对轮胎性能的影响：
- **滚动阻力**: 影响较小，Tg 仍远低于使用温度
- **湿抓地力**: Tg 略升高有利于湿抓地力
- **低温性能**: 轻微升高不影响低温柔韧性

## 数据来源与置信度说明

- Tg 数据来自文献 SI Table S6
- 测试方法为 DSC（差示扫描量热法）
- 置信度"高"表示数据直接从文献表格读取
