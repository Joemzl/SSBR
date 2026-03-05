# 解读文档模板

本目录用于存储各样本的 Skill 解读结果。

## 目录结构

```
/dataset/interpretations/
├── SSBR-001/
│   ├── nmr.md           # 核磁共振谱图解读
│   ├── tem.md           # TEM 微相分离形貌解读
│   ├── mechanical.md    # 核心力学图谱解读（应力-应变/Payne/DMA）
│   ├── dsc.md           # DSC 热分析解读
│   └── summary.md       # 综合摘要（用于 RAG 检索）
├── SSBR-002/
│   └── ...
└── TEMPLATE.md          # 本模板文件
```

## 文件命名规范

| 文件名 | 对应表征 | 说明 |
|--------|----------|------|
| `nmr.md` | 核磁谱图 (I列) | ¹H NMR 解读 |
| `tem.md` | 微相分离图片表征 (J列) | TEM 形貌解读 |
| `mechanical.md` | 核心力学图谱 (K列) | 可包含多种图谱类型 |
| `dsc.md` | DSC 谱图 (L列) | DSC 热分析解读 |
| `summary.md` | 综合摘要 | 用于向量化检索 |

## YAML Front Matter 规范

每个解读文件必须包含以下元数据：

```yaml
---
sample_id: SSBR-XXX           # 必填：样本 ID
interpretation_type: nmr       # 必填：nmr/tem/mechanical/dsc/summary
source_figure: Figure 2a       # 可选：来源图注
source_doi: 10.1039/xxxxxxx    # 可选：来源 DOI
skill_used: ssbr-nmr-interpretation  # 必填：使用的 Skill
created_at: 2026-03-04         # 必填：创建日期
mechanical_subtypes:           # 仅 mechanical.md 需要
  - stress-strain              # 可选值：stress-strain, payne, dma
  - payne
---
```

## 解读文档模板

### nmr.md / tem.md / dsc.md 模板

```markdown
---
sample_id: SSBR-XXX
interpretation_type: [type]
source_figure: [图注]
source_doi: [DOI]
skill_used: [skill-name]
created_at: [日期]
---

# [表征类型]解读：[样本ID]

## 核心发现

### 1. [发现一]
- **观测结果**：...
- **物理意义**：...

### 2. [发现二]
- **观测结果**：...
- **物理意义**：...

## 关键指标

| 指标 | 数值 | 说明 |
|------|------|------|
| ... | ... | ... |

## 与官能化的关联

[解释该表征结果如何反映/验证官能化效果]
```

### mechanical.md 模板（支持多类型）

```markdown
---
sample_id: SSBR-XXX
interpretation_type: mechanical
source_figure: Figure 4, Figure 5
source_doi: 10.1039/xxxxxxx
skill_used: ssbr-mechanical-interpretation
created_at: 2026-03-04
mechanical_subtypes:
  - stress-strain
  - payne
---

# 力学性能解读：SSBR-XXX

## 包含的图谱类型

- [x] 应力-应变曲线
- [x] Payne 效应曲线
- [ ] DMA 曲线

---

## 一、应力-应变曲线解读

### 核心发现
...

---

## 二、Payne 效应曲线解读

### 核心发现
...
```

### summary.md 模板（关键：用于 RAG 检索）

```markdown
---
sample_id: SSBR-XXX
interpretation_type: summary
created_at: 2026-03-04
---

# 综合摘要：SSBR-XXX

## 一句话总结

[用一句话概括该方案的核心价值和适用场景]

## 官能化信息

- **试剂**：[官能化试剂名称]
- **官能团**：[核心官能团]
- **程度**：[官能化程度] wt%
- **方法**：巯基-烯点击化学

## 核心性能优势

1. **[优势一]**：[具体描述]
2. **[优势二]**：[具体描述]
3. **[优势三]**：[具体描述]

## 适用场景

- [场景一]
- [场景二]

## 关键性能指标

| 类别 | 指标 | 数值 | 评价 |
|------|------|------|------|
| 力学 | 拉伸强度 | XX MPa | ✅ 优秀 |
| 力学 | 断裂伸长率 | XX % | ✅ 良好 |
| 动态 | 60℃ tanδ | X.XX | ✅ 低滚阻 |
| 热学 | Tg | XX ℃ | ✅ 适中 |

## 文献来源

[引文信息]
```
