---
sample_id: SSBR-003
doi: 10.1039/c9ra02783a
polymer_type: null
data_completeness:
  mechanical: true
  dsc: true
  nmr: true
  tem: true
created_at: '2026-03-21'
updated_at: '2026-03-24'
functionalization:
  type: in_chain
  reagent: 3-巯基丙基三乙氧基硅烷（MPTES）
  grafting_group: 巯基
  grafting_group_smiles: S
  core_functional_group_smiles: '[Si](OCC)(OCC)OCC'
  core_functional_group_name: 三乙氧基硅烷基
  degree: 1.7 wt%
polymer_fingerprint: --186000.0-18.4-47.8-S---1.7wt%
---

# SSBR-003 综合档案

## 一句话总结

低接枝量硅烷偶联SSBR：MPTES官能化程度最低（1.7 wt%，约13个接枝分子），通过共价键与白炭黑结合，力学性能中等，适用于需要温和界面改性的应用。

---

## 核心性能特点

### 【共价键界面作用】评价：良好

MPTES 的三乙氧基硅烷基可与白炭黑表面硅羟基发生缩合反应，形成稳定的 Si-O-Si 共价键：

```
白炭黑表面        接枝链              SSBR 主链
   |               |                    |
 Si-O-Si-(CH₂)₃-S-CH₂-CH= (聚合物链)
   ↑         ↑              ↑
 Si-O-Si   硅烷偶联     巯基-烯加成
 共价键
```

### 【力学性能】评价：良好

| 指标 | SSBR-g-MPTES13 | 空白 SSBR | 提升幅度 |
|------|----------------|-----------|----------|
| 100%定伸应力 | 2.8 MPa | 1.5 MPa | +87% |
| 拉伸强度 | 18.2 MPa | 15.0 MPa | +21% |
| 断裂伸长率 | 275% | 452% | -39% |

### 【分散性改善】评价：良好

- **结合橡胶含量**: 46.23%（空白: 20.56%）
- **tan δ (7% strain)**: 0.110（空白: 0.132）
- TEM 显示分散性显著改善

---

---

## 适用场景

- ✅ 绿色轮胎胎面胶

---

## 关键性能指标

| 类别 | 指标 | 数值 | 单位 | 评价 |
|------|------|------|------|------|
| 力学性能 | 100%定伸应力 | 2.8 | MPa | - |
| 力学性能 | 300%定伸应力 | - | MPa | - |
| 力学性能 | 拉伸强度 | 18.2 | MPa | - |
| 力学性能 | 断裂伸长率 | 275 | % | - |
| 热学性能 | Tg | -8.9 | ℃ | - |
| 界面性能 | 结合橡胶含量 | 46.23 | % | - |

---

## 解读文档完整性

| 文档类型 | 状态 | 备注 |
|----------|------|------|
| mechanical.md | ✓ | 已生成 |
| dsc.md | ✓ | 已生成 |
| nmr.md | ✓ | 已生成 |
| tem.md | ✓ | 已生成 |

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **引文**: Gao W, Lu J, Song W, et al. Interfacial interaction modes construction of various functional SSBR–silica towards high filler dispersion and excellent composites performances[J]. RSC Advances, 2019, 9(31): 18888-18897.

---


## 曲线数据概览 (v2.0)

本样本已完成全范围曲线数据提取，支持高精度分析和趋势外推。

### 应力-应变曲线
- **数据点数**: 12
- **应变范围**: 0-275%
- **应力范围**: 0-18.2 MPa
- **平均置信度**: 0.74
- **交叉验证**: good
- **拉伸强度**: 18.2 MPa
- **断裂伸长率**: 275%

### DMA tan δ-温度曲线
- **数据点数**: 17
- **温度范围**: -80-80℃
- **tan δ 范围**: 0.02-0.9
- **平均置信度**: 0.70
- **交叉验证**: good
- **关键特征值**:
  - Tg (tan δ 峰值): -8.9℃
  - tan δ (0℃): 0.886（湿地抓地力指标）
  - tan δ (60℃): ~0.1（滚动阻力指标）

### Payne G'-应变曲线
- **数据点数**: 12
- **应变范围**: 0.28-42% (对数间隔)
- **G' 范围**: 0.55-2.1 MPa
- **平均置信度**: 0.70
- **交叉验证**: acceptable
- **关键特征值**:
  - G'₀: 2.1 MPa
  - G'∞: 0.55 MPa
  - ΔG': 1.55 MPa

### DSC 热流曲线
- **数据点数**: 12
- **温度范围**: -80-60℃
- **平均置信度**: 0.67
- **交叉验证**: acceptable
- **玻璃化转变**:
  - Tg onset: -30℃
  - Tg midpoint: -24.5℃
  - Tg endpoint: -15℃
  - 转变宽度: ~15℃
---

*本综合档案由 `ssbr-summary-generator` 脚本合并生成，保留了人工撰写的解读内容，用于 RAG 语义检索。*