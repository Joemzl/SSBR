# 摘要

**题目**：基于检索增强生成的 SSBR 官能化知识综合与推荐系统研究

---

## 中文摘要

溶聚丁苯橡胶（SSBR）的官能化改性是提升橡胶材料性能的关键技术，广泛应用于高性能轮胎等领域。然而该领域的研究知识高度分散于数百篇学术文献中，研究者面临"文献爆炸、条件异构、检索低效"的三重困境。传统的文献管理方式难以支撑跨文献的知识综合与推理，制约了配方设计效率。

针对上述问题，本文设计并实现了一套基于检索增强生成（RAG）技术的 SSBR 官能化知识综合与推荐系统。系统以"元数据-解读文档分离"架构构建领域知识库，通过向量化语义检索实现自然语言查询；采用多文献综合推理机制，从多个样本中提取共性规律并生成整合性回答；引入保守外推边界控制策略（CEBC），在提供预测性建议的同时严格控制外推范围；设计零幻觉保障机制，确保所有数值可追溯至原始文献。

实验结果表明，系统在 RAGAS 评测框架下取得优异性能：忠实度（Faithfulness）0.827、回答相关性（Answer Relevancy）0.814、上下文精度（Context Precision）0.835、上下文召回率（Context Recall）0.829，所有核心指标均达到优秀水平（≥0.80）。系统平均响应时间 6.06 秒，91.7% 的查询在 8 秒内完成。案例分析证明，系统能够有效综合多篇文献信息，为配方设计提供有数据支撑、可追溯的专业建议。

本研究的主要贡献包括：（1）提出适用于材料科学领域的 RAG 系统架构设计；（2）设计多文献综合推理机制，突破传统单样本检索的局限；（3）建立外推边界控制与零幻觉保障的双重可靠性机制；（4）构建包含 68 个官能化样本的 SSBR 专业知识库。本系统为材料信息学在高分子领域的应用提供了可参考的技术方案。

**关键词**：检索增强生成；溶聚丁苯橡胶；官能化；知识图谱；大语言模型；材料信息学

---

## Abstract

Functionalization of solution-polymerized styrene-butadiene rubber (SSBR) is a key technology for enhancing rubber material performance, with wide applications in high-performance tires and other fields. However, research knowledge in this field is highly dispersed across hundreds of academic papers, and researchers face the triple dilemma of "literature explosion, heterogeneous conditions, and inefficient retrieval." Traditional literature management methods cannot support cross-literature knowledge synthesis and reasoning, limiting formulation design efficiency.

To address these problems, this thesis designs and implements a knowledge synthesis and recommendation system for SSBR functionalization based on Retrieval-Augmented Generation (RAG) technology. The system constructs a domain knowledge base with a "metadata-interpretation document separation" architecture and enables natural language queries through vectorized semantic retrieval. A multi-literature synthesis reasoning mechanism extracts common patterns from multiple samples and generates integrated answers. A Conservative Extrapolation Boundary Control (CEBC) strategy is introduced to provide predictive suggestions while strictly controlling the extrapolation range. A zero-hallucination assurance mechanism ensures all numerical values are traceable to original literature.

Experimental results demonstrate that the system achieves excellent performance under the RAGAS evaluation framework: Faithfulness 0.827, Answer Relevancy 0.814, Context Precision 0.835, and Context Recall 0.829, with all core metrics reaching the excellent level (≥0.80). The system's average response time is 6.06 seconds, with 91.7% of queries completed within 8 seconds. Case studies prove that the system can effectively synthesize information from multiple literature sources and provide data-supported, traceable professional recommendations for formulation design.

The main contributions of this research include: (1) proposing a RAG system architecture suitable for the materials science domain; (2) designing a multi-literature synthesis reasoning mechanism that breaks through the limitations of traditional single-sample retrieval; (3) establishing a dual reliability mechanism with extrapolation boundary control and zero-hallucination assurance; (4) constructing a professional SSBR knowledge base containing 68 functionalized samples. This system provides a referenceable technical solution for the application of materials informatics in the polymer field.

**Keywords**: Retrieval-Augmented Generation; Solution-polymerized Styrene-Butadiene Rubber; Functionalization; Knowledge Graph; Large Language Model; Materials Informatics

---

*字数统计：中文摘要约 520 字，英文摘要约 320 词*
