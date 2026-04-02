# 基于 RAG 的 SSBR 官能化配方智能推荐系统

## 论文完整目录

**作者**: [作者姓名]  
**导师**: [导师姓名] 教授  
**单位**: [学校/研究机构名称]  
**完成日期**: 2026 年 4 月

---

## 摘要

[待补充 - 建议在全文完成后根据各章内容撰写]

**关键词**: 检索增强生成（RAG）；溶聚丁苯橡胶（SSBR）；官能化；绿色轮胎；材料设计；大语言模型；知识综合；零幻觉；边界约束外推

---

## Abstract

[To be added - Recommended to write after completing all chapters]

**Keywords**: Retrieval-Augmented Generation (RAG); Solution Styrene-Butadiene Rubber (SSBR); Functionalization; Green Tire; Material Design; Large Language Model; Knowledge Synthesis; Zero-Hallucination; Boundary-Constrained Extrapolation

---

## 目录

### 第一章 引言
- 1.1 研究背景
  - 1.1.1 溶聚丁苯橡胶及其官能化技术概述
  - 1.1.2 SSBR 官能化研究现状与知识碎片化问题
  - 1.1.3 材料设计中的知识管理挑战
- 1.2 人工智能在材料科学中的应用
  - 1.2.1 传统数据库检索的局限性
  - 1.2.2 大语言模型与检索增强生成
- 1.3 研究目标与意义
- 1.4 论文组织结构

📄 **文件**: [01-introduction.md](./01-introduction.md)

---

### 第二章 相关工作
- 2.1 SSBR 官能化技术综述
  - 2.1.1 官能化方法分类
  - 2.1.2 常见官能团及其作用机理
  - 2.1.3 白炭黑填充体系与填料分散
- 2.2 材料信息学与知识库构建
  - 2.2.1 材料科学数据库的发展
  - 2.2.2 结构化知识表示方法
  - 2.2.3 高分子材料的数据稀疏性与异构性挑战
- 2.3 检索增强生成（RAG）技术
  - 2.3.1 RAG 基本原理
  - 2.3.2 向量数据库与语义检索
  - 2.3.3 RAG 在科研领域的应用
- 2.4 现有方法的不足与本文贡献

📄 **文件**: [02-related-work.md](./02-related-work.md)

---

### 第三章 系统设计与架构
- 3.1 系统总体架构
- 3.2 知识库构建
  - 3.2.1 文献数据收集与预处理
  - 3.2.2 结构化数据模型设计
  - 3.2.3 元数据与解读文档分离
- 3.3 向量检索模块
  - 3.3.1 文本嵌入方法
  - 3.3.2 ChromaDB 向量数据库设计
  - 3.3.3 HNSW 近似最近邻算法
- 3.4 问答生成模块
  - 3.4.1 Prompt 工程设计
  - 3.4.2 结构化输出格式
  - 3.4.3 引用可追溯性保证
- 3.5 样本质量评估机制
- 3.6 交叉编码器重排序

📄 **文件**: [03-system-design.md](./03-system-design.md)

---

### 第四章 多文献综合方法
- 4.1 综合推理模式设计
- 4.2 样本聚合与趋势分析
- 4.3 保守外推策略
- 4.4 对比分析与配方设计
- 4.5 引用验证机制

📄 **文件**: [04-synthesis-method.md](./04-synthesis-method.md)

---

### 第五章 数据集与实验设置
- 5.1 SSBR 官能化知识库构建
- 5.2 向量数据库设计
- 5.3 样本质量评估体系
- 5.4 测试查询集设计
- 5.5 RAGAS 评测框架
- 5.6 实验环境与硬件配置
- 5.7 实验设计

📄 **文件**: [05-dataset-experiments.md](./05-dataset-experiments.md)

---

### 第六章 实验结果与分析
- 6.1 RAGAS 评测总体结果
- 6.2 检索性能分析
- 6.3 生成质量分析
- 6.4 系统响应效率分析
- 6.5 综合性能仪表盘
- 6.6 分查询详细分析
- 6.7 案例研究
  - 6.7.1 案例 1：白炭黑分散性改善方案
  - 6.7.2 案例 2：高湿地抓地力低滚阻配方设计
  - 6.7.3 案例 3：官能团类型对比分析
- 6.8 统计汇总表

📄 **文件**: [06-results-analysis.md](./06-results-analysis.md)

**包含图片**: 7 张（雷达图、柱状图、热力图、响应时间图、仪表盘、对比图、汇总表）

---

### 第七章 讨论
- 7.1 系统优势总结
  - 7.1.1 知识综合能力
  - 7.1.2 引用可追溯性
  - 7.1.3 响应效率
- 7.2 零幻觉机制对材料科学研究的意义
  - 7.2.1 材料科学对数据准确性的严苛要求
  - 7.2.2 100% 引用可追溯性的价值
  - 7.2.3 与通用 AI 助手的本质区别
- 7.3 当前局限性
  - 7.3.1 忠实度指标的解读与改进空间
  - 7.3.2 知识库规模限制
  - 7.3.3 外推能力的边界
- 7.4 与现有方法的对比
- 7.5 对材料科学研究的启示
- 7.6 未来改进方向

📄 **文件**: [07-discussion.md](./07-discussion.md)

---

### 第八章 结论
- 8.1 主要贡献
- 8.2 研究意义
- 8.3 未来展望

📄 **文件**: [08-conclusion.md](./08-conclusion.md)

---

### 致谢

📄 **文件**: [09-acknowledgements.md](./09-acknowledgements.md)

---

### 参考文献

📄 **文件**: [11-references.md](./11-references.md)

---

### 附录
- 附录 A：系统代码结构
- 附录 B：YAML Schema 定义
- 附录 C：完整测试查询列表
- 附录 D：RAGAS 评测详细数据
- 附录 E：Web 界面功能说明
- 附录 F：系统部署与使用指南

📄 **文件**: [10-appendices.md](./10-appendices.md)

---

## 论文统计

| 章节 | 文件名 | 预估字数 | 预估页数 |
|------|--------|----------|----------|
| 第一章 引言 | 01-introduction.md | ~5,000 | 6-8 |
| 第二章 相关工作 | 02-related-work.md | ~6,000 | 8-10 |
| 第三章 系统设计 | 03-system-design.md | ~7,000 | 10-12 |
| 第四章 综合方法 | 04-synthesis-method.md | ~5,500 | 7-9 |
| 第五章 数据与实验 | 05-dataset-experiments.md | ~6,500 | 8-10 |
| 第六章 结果分析 | 06-results-analysis.md | ~8,000 | 12-15 |
| 第七章 讨论 | 07-discussion.md | ~5,500 | 7-9 |
| 第八章 结论 | 08-conclusion.md | ~2,500 | 3-4 |
| 致谢 | 09-acknowledgements.md | ~500 | 1 |
| 参考文献 | 11-references.md | ~1,500 | 3-4 |
| 附录 | 10-appendices.md | ~4,000 | 8-10 |
| **总计** | **11 个文件** | **~52,000 字** | **75-90 页** |

---

## 图表清单

### 图片列表

| 图号 | 文件路径 | 描述 |
|------|---------|------|
| 图 6-1 | evaluation/figures/ragas_radar.png | RAGAS 评测雷达图 |
| 图 6-2 | evaluation/figures/ragas_bar.png | 各指标柱状图 |
| 图 6-3 | evaluation/figures/ragas_heatmap.png | 评测指标热力图 |
| 图 6-4 | evaluation/figures/ragas_response_time.png | 响应时间分析图 |
| 图 6-5 | evaluation/figures/ragas_dashboard.png | 综合性能仪表盘 |
| 图 6-6 | evaluation/figures/ragas_comparison.png | 各查询性能对比图 |
| 图 6-7 | evaluation/figures/ragas_summary_table.png | 统计汇总表 |

### 表格统计

- 第五章：11 个表格
- 第六章：9 个表格
- 第七章：4 个表格
- 附录：6 个表格
- **总计**：约 30 个表格

---

## 待完善事项

1. [ ] 补充中英文摘要
2. [ ] 根据实际情况修改致谢内容
3. [ ] 确认参考文献格式符合目标期刊/学校要求
4. [ ] 检查所有图片引用路径是否正确
5. [ ] 统一术语翻译（中英对照）
6. [ ] 添加更多第三章和第四章的架构图

---

*论文主体内容已完成，请根据实际需要进行调整和完善。*
