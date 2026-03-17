---
sample_id: SSBR-001
interpretation_type: tem
source_figure: "Fig. 5(C)"
source_doi: "10.1039/c9ra02783a"
skill_used: ssbr-tem-interpretation
created_at: 2026-03-17
updated_at: null

data:
  domain_size:
    value: null
    range: null
    unit: nm
    source: "未明确给出具体尺寸"
  dispersion_quality: "良"
  morphology: "白炭黑分散相当均匀，团聚和空隙较少"
  scale_bar: "200 nm"
---

# TEM 透射电镜形貌解读：SSBR-001

## 一、微相分离形貌

### 观察参数

| 参数 | 数值 |
|------|------|
| 放大倍数 | 未标注 |
| 标尺 | 200 nm |
| 染色方法 | 未说明（推测为重金属染色或无需染色的明场TEM） |

### 形貌描述

Fig. 5(C) 展示了 silica/SSBR-g-MPL70 复合材料的 TEM 图像。图中深色区域为白炭黑填料颗粒，浅色区域为橡胶基体。

观察到的特征：
- 白炭黑颗粒在橡胶基体中分布较为均匀
- 相比空白样品，团聚现象明显减少
- 橡胶-填料界面较为清晰，空隙较少
- 填料颗粒呈现出较好的分散状态

---

## 二、填料分散状态

### 分散质量评价

- **整体评价**: 良
- **团聚情况**: 较少团聚，相比未官能化样品显著改善

### 相区尺寸

| 特征 | 尺寸 (nm) | 备注 |
|------|-----------|------|
| 平均相区尺寸 | - | 文献未给出定量数据 |
| 尺寸分布 | - | 需要图像分析定量 |
| 标尺参考 | 200 | 可用于估算相对尺寸 |

### 核心发现

文献原文描述：
> "The dispersions of silica in the silica/F-SSBR composites were quite uniform with fewer aggregates and voids compared with silica/SSBR."

关键发现：
1. **MPL 官能化改善分散**: 巯基丙醇(MPL)接枝到 SSBR 主链后，末端羟基(-OH)能够与白炭黑表面的硅羟基形成氢键，增强界面相互作用
2. **界面空隙减少**: 改善的界面粘附导致填料-橡胶界面处的空隙明显减少
3. **团聚抑制**: 更好的界面相互作用有助于抑制白炭黑的团聚倾向

---

## 三、与对照组对比

文献给出了不同官能化样品的分散性排序：
> "In terms of silica dispersions in vulcanizates, it was found that silica/SSBR-g-MPTES70 > silica/SSBR-g-MUA70 > silica/SSBR-g-MPL70, which was attributed to the gradually improving interfacial interactions."

| 特征 | SSBR-g-MPL70 (本样本) | 空白 SSBR | 改善程度 |
|------|----------------------|-----------|----------|
| 分散质量 | 良（较均匀） | 差（大量团聚） | 显著改善 |
| 团聚数量 | 较少 | 大量 | 明显减少 |
| 界面空隙 | 较少 | 大量 | 明显减少 |

### 与其他官能化样品对比

| 样本 | 接枝基团 | 界面作用机制 | 分散性排名 |
|------|----------|--------------|------------|
| SSBR-g-MPTES70 | 三乙氧基硅烷 | 共价键 + 氢键 | 第 1 名（最优） |
| SSBR-g-MUA70 | 十一烯酸（羧基） | 双氢键（羧基） | 第 2 名 |
| **SSBR-g-MPL70** | **巯基丙醇（羟基）** | **单氢键（羟基）** | **第 3 名** |
| 空白 SSBR | 无 | 无 | 最差 |

**分散性差异原因分析**：
- MPTES 含三乙氧基硅烷基团，可与白炭黑表面形成 Si-O-Si 共价键，界面结合最强
- MUA 的羧基可形成双氢键，界面作用次之
- MPL 的羟基仅能形成单氢键，界面作用相对较弱，但仍显著优于未官能化样品

---

## 四、结构-性能关联

### 分散性与力学性能的关系

TEM 观察到的良好分散性与力学测试结果相呼应：

1. **拉伸强度提升**: 分散均匀的填料能够更有效地传递应力，提高复合材料的拉伸强度（22.9 MPa vs 16.7 MPa）

2. **断裂伸长率改善**: 减少的团聚和空隙降低了应力集中点，允许更大的形变（543% vs 503%）

3. **撕裂强度增强**: 改善的界面粘附和均匀分散提高了抗撕裂能力（51.9 kN/m vs 35.6 kN/m）

### 分散性与动态性能的关系

1. **Payne 效应减弱**: 更好的分散减少了填料-填料网络，降低了 Payne 效应（ΔG' = 0.94 MPa vs 1.77 MPa）

2. **滞后损失降低**: 均匀分散减少了填料团聚导致的能量耗散

### 界面作用机理示意

```
白炭黑表面        接枝链            SSBR 主链
   |                |                  |
 Si-OH ····· HO-CH₂-CH₂-CH₂-S-CH₂-CH= (聚合物链)
   ↑          ↑               ↑
  硅羟基    羟基氢键        巯基-烯加成点
```

---

## 文献来源

- **DOI**: 10.1039/c9ra02783a
- **图注引用**: Fig. 5. TEM photographs of (A) silica/SSBR, (B) silica/SSBR-g-MUA70, (C) silica/SSBR-g-MPL70 and (D) silica/SSBR-g-MPTES70 vulcanizates.
- **数据来源层级**: L2（图面标注 + 文字描述）
