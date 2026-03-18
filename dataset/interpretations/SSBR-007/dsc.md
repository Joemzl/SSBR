---
# SSBR-007 热学性能解读
sample_id: SSBR-007
test_type: dsc
data_source: "10.1002/app.41182"
data_quality: N/A

# DSC 数据状态
dsc_data:
  available: false
  reason: "文献未提供 DSC 测试数据"

# 已知热学相关信息
thermal_info:
  processing_temperature:
    mixing: "160°C"
    compression_molding: "160°C"
    extrusion_die: "160°C"
  S_EB_S_properties:
    melt_flow_index: "22 g/10min (230°C/5kg)"
    density: "0.90 g/cc"
    polystyrene_content: "13%"
  S_SBR_properties:
    polystyrene_content: "23.5%"
    source: "Dycon Chemicals, India"
---

## 热学性能解读

### 数据可用性

本文献（DOI: 10.1002/app.41182）未提供 DSC 热分析测试数据。研究主要聚焦于 TPV 的流变性能、动态粘弹性和形态学表征。

### 相关热学信息

虽然没有 DSC 数据，文献提供了以下热学相关信息：

#### 加工温度

- **内部混合器温度**: 160°C
- **压模温度**: 160°C，5 MPa，4 min
- **挤出机模头温度**: 160°C
- **进料区温度**: 130°C
- **其他区域温度**: 150°C

#### 原材料热学特性

**S-EB-S (Kraton G1657)**:
- 熔融指数: 22 g/10min (230°C/5kg)
- 密度: 0.90 g/cc
- 为氢化苯乙烯类三嵌段共聚物

**S-SBR**:
- 苯乙烯含量: 23.5 wt%
- Tg 未提供

### DMA 温度扫描数据

虽然不是传统 DSC，文献 Fig. 11 提供了储能模量（E'）随温度变化的 DMA 数据，可用于判断玻璃化转变区域。在 25°C 时的 E' 值见 mechanical.md 文档。

### 建议

如需完整的 Tg 和结晶/熔融行为数据，建议：
1. 查阅 S-SBR 和 S-EB-S 的产品技术数据表
2. 参考相关 TPV 体系的 DSC 研究文献
