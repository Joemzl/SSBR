# -*- coding: utf-8 -*-
"""
分析 5 个样本的官能化程度信息

样本列表：
- SSBR-025: Sirisinha et al., 2019 (10.1002/app.48696)
- SSBR-033: Qin et al., 2018 (10.3389/fchem.2018.00240)
- SSBR-045: Sun et al., 2009 (10.1002/app.29646)
- SSBR-050: Qin et al., 2018 (10.1016/j.nanoen.2018.03.038)
- SSBR-114: Liu et al., 2023 (10.1007/s10965-023-03446-7)
"""

# ==================== 文献分析结果 ====================

analysis = """
## SSBR-025 (Sirisinha et al., 2019)
文献原文 Table I:
"The amount of functional groups in F-SSBR is still not disclosed."
("F-SSBR 中官能团的含量尚未公开")

结论：确认为"未公开"，无法获取具体数值。

---

## SSBR-033 (Qin et al., 2018 - Frontiers in Chemistry)
这篇文献研究的是 HTSSBR-PU（羟基封端SSBR基聚氨酯），使用 NDI（1,5-萘二异氰酸酯）作为硬段。

文献中给出的关键数值：
- 苯乙烯含量: 23.75%
- 1,2-丁二烯含量: 61.56%
- 1,4-丁二烯含量: 14.69%
- 分子量: ~3000

但关于 NDI 的"官能化程度"，文献描述的是软段/硬段比例（如 100:25, 100:30 等），
而不是传统意义上的接枝率。

结论：确认为"未公开"——这是聚氨酯材料设计，不是接枝改性。

---

## SSBR-045 (Sun et al., 2009)
文献研究的是白炭黑填充 SSBR 的非线性应力松弛行为。
使用的是 3-辛酰硫基-1-丙基三乙氧基硅烷 (3-octanoylthio-1-propyltriethoxyl silane) 作为偶联剂。

关键信息（Table I）：
- 白炭黑填充量: 0, 10, 30, 50 phr
- 偶联剂用量: "Corresponds to the SiO2 loading"（对应于白炭黑用量）

文献没有给出具体的偶联剂用量数值（phr 或 wt%）。

结论：确认为"未公开"——偶联剂用量与白炭黑用量相关，但未给出具体数值。

---

## SSBR-050 (Qin et al., 2018 - Nano Energy)
这篇文献同样研究 HTSSBR-PU（羟基封端SSBR基聚氨酯）。

文献中给出的关键数值：
- 苯乙烯含量: 23.65%
- 1,2-丁二烯含量: 61.57%
- 1,4-丁二烯含量: 14.78%
- 软段/硬段比例可调

同样，这是聚氨酯材料设计，不是接枝改性，没有传统的官能化程度数值。

结论：确认为"未公开"——这是聚氨酯材料设计。

---

## SSBR-114 (Liu et al., 2023)
文献使用乙烯基三甲氧基硅烷 (VTMS/VTMO) 通过烯烃复分解反应改性 SSBR。

关键原文 (Modification of SSBR 部分):
"add a certain volume of VTMO (nVTMO=n-CH=CH2 of SSBR)"

这意味着 VTMO 的用量与 SSBR 上的乙烯基双键**等摩尔**。
文献确实没有给出具体的百分比数值。

结论：确认为"等摩尔 (vs 双键)"——这是正确的描述。
"""

print(analysis)

print("\n" + "="*60)
print("最终结论")
print("="*60)

conclusions = """
| 样本ID | 官能化程度_原始数值 | 官能化程度_原始单位 | 是否需要更新 | 原因 |
|--------|---------------------|---------------------|--------------|------|
| SSBR-025 | 未公开 | - | 否 | 文献明确写道 "still not disclosed" |
| SSBR-033 | 未公开 | - | 否 | 聚氨酯材料设计，非接枝改性 |
| SSBR-045 | 未公开 | - | 否 | 偶联剂用量未给出具体数值 |
| SSBR-050 | 未公开 | - | 否 | 聚氨酯材料设计，非接枝改性 |
| SSBR-114 | 等摩尔 | (vs 双键) | 否 | 文献原文 nVTMO=n-CH=CH2 |
"""

print(conclusions)
