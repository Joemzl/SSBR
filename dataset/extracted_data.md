# Gemini 提取的数据

将 Gemini 输出的 Markdown 表格粘贴到下方，然后运行：
```
python scripts/import_metadata.py --file other/extracted_data.md --dry-run
```

---

<!-- 在此行下方粘贴 Gemini 输出的表格，注意每次粘贴表格时，请把之前的表格删掉 -->
| 样本ID | 是否是SSBR | 是否是链中官能化 | 苯乙烯含量_wt% | 乙烯基含量_mol% | 数均分子量 (Mn) | 应用场景 | 官能化试剂名称 | 试剂整体SMILES | 接枝反应基团 | 核心官能团SMILES | 核心官能团名称 | 核心官能团化学式 | 官能化程度_原始数值 | 官能化程度_原始单位 | 高分子指纹描述符 | 核磁谱图 | 微相分离图片表征 | 核心力学图谱 | DSC谱图 | 引文 | DOI | DOI_SI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| - | 是 | 是 | - | - | - | 绿色轮胎胎面胶 | 3-巯基丙醇（MPL） | OCCS | 巯基 | O | 羟基 | -OH | 3.6 | wt% | OCCS-----巯基-羟基-3.6wt% | 文献 Fig.1(A) ¹H NMR谱图 | 文献 Fig.5(C) TEM图 | 文献 Fig.6(A) G'应变曲线、文献 Fig.6(B) 硫化胶G'应变曲线、文献 Fig.8(A) 应力-应变曲线 | 文献 Fig.2 DSC曲线 | Gao W, Lu J, Song W, et al. Interfacial interaction modes construction of various functional SSBR–silica towards high filler dispersion and excellent composites performances[J]. RSC Advances, 2019, 9(31): 18888-18897. | 10.1039/c9ra02783a | 有 |
| - | 是 | 是 | - | - | - | 绿色轮胎胎面胶 | 11-巯基十一烷酸（MUA） | O=C(O)CCCCCCCCCCS | 巯基 | C(=O)O | 羧基 | -COOH | 8.7 | wt% | O=C(O)CCCCCCCCCCS-----巯基-羧基-8.7wt% | 文献 Fig.1(B) ¹H NMR谱图 | 文献 Fig.5(D) TEM图 | 文献 Fig.6(A) G'应变曲线、文献 Fig.6(B) 硫化胶G'应变曲线、文献 Fig.8(A) 应力-应变曲线 | 文献 Fig.2 DSC曲线 | Gao W, Lu J, Song W, et al. Interfacial interaction modes construction of various functional SSBR–silica towards high filler dispersion and excellent composites performances[J]. RSC Advances, 2019, 9(31): 18888-18897. | 10.1039/c9ra02783a | 有 |
| - | 是 | 是 | - | - | - | 绿色轮胎胎面胶 | 3-巯基丙基三乙氧基硅烷（MPTES） | CCO[Si](OCC)(OCC)CCS | 巯基 | [Si](OCC)(OCC)OCC | 三乙氧基硅烷基 | -Si(OC₂H₅)₃ | 1.7 | wt% | CCO[Si](OCC)(OCC)CCS-----巯基-三乙氧基硅烷基-1.7wt% | 文献 Fig.1(C) ¹H NMR谱图 | - | 文献 Fig.6(A) G'应变曲线、文献 Fig.6(B) 硫化胶G'应变曲线、文献 Fig.8(A) 应力-应变曲线 | - | Gao W, Lu J, Song W, et al. Interfacial interaction modes construction of various functional SSBR–silica towards high filler dispersion and excellent composites performances[J]. RSC Advances, 2019, 9(31): 18888-18897. | 10.1039/c9ra02783a | 有 |
| - | 是 | 是 | - | - | - | 绿色轮胎胎面胶 | 3-巯基丙基三乙氧基硅烷（MPTES） | CCO[Si](OCC)(OCC)CCS | 巯基 | [Si](OCC)(OCC)OCC | 三乙氧基硅烷基 | -Si(OC₂H₅)₃ | 5.8 | wt% | CCO[Si](OCC)(OCC)CCS-----巯基-三乙氧基硅烷基-5.8wt% | 文献 Fig.1(C) ¹H NMR谱图 | - | 文献 Fig.6(A) G'应变曲线、文献 Fig.6(B) 硫化胶G'应变曲线、文献 Fig.8(A) 应力-应变曲线 | - | Gao W, Lu J, Song W, et al. Interfacial interaction modes construction of various functional SSBR–silica towards high filler dispersion and excellent composites performances[J]. RSC Advances, 2019, 9(31): 18888-18897. | 10.1039/c9ra02783a | 有 |
| - | 是 | 是 | - | - | - | 绿色轮胎胎面胶 | 3-巯基丙基三乙氧基硅烷（MPTES） | CCO[Si](OCC)(OCC)CCS | 巯基 | [Si](OCC)(OCC)OCC | 三乙氧基硅烷基 | -Si(OC₂H₅)₃ | 9.5 | wt% | CCO[Si](OCC)(OCC)CCS-----巯基-三乙氧基硅烷基-9.5wt% | 文献 Fig.1(C) ¹H NMR谱图 | 文献 Fig.5(E) TEM图 | 文献 Fig.6(A) G'应变曲线、文献 Fig.6(B) 硫化胶G'应变曲线、文献 Fig.8(A) 应力-应变曲线 | 文献 Fig.2 DSC曲线 | Gao W, Lu J, Song W, et al. Interfacial interaction modes construction of various functional SSBR–silica towards high filler dispersion and excellent composites performances[J]. RSC Advances, 2019, 9(31): 18888-18897. | 10.1039/c9ra02783a | 有 |
