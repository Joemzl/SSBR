# NapkinAI 图表生成提示词

本文档包含论文所需 9 张概念/流程图的提示词，中英文两版供选择。
建议优先使用英文提示词，效果通常更好。

---

## 图 1-1: SSBR 官能化知识管理困境示意图

**必要性**: ★★★ (可选)
**用途**: 展示研究者面临的三重困境

### English Prompt

```
Create a clean academic diagram showing three main challenges in SSBR functionalization research knowledge management:

LEFT SECTION: "Literature Explosion" 
- Show multiple scattered document/paper icons (5-6 papers)
- Label: "300+ papers across journals"

CENTER SECTION: "Condition Heterogeneity"
- Show a comparison table with mismatched parameters
- Different units, different test conditions
- Label: "Incomparable experimental conditions"

RIGHT SECTION: "Retrieval Inefficiency"  
- Show a search icon with X mark or hourglass
- Label: "20+ papers to find one answer"

BOTTOM: Arrow pointing down to a frustrated researcher icon

Style: Minimalist icons, blue and gray color scheme, professional academic look, no decorative elements, clean white background
```

### 中文提示词

```
创建一张学术风格的示意图，展示 SSBR 官能化研究中知识管理的三重困境：

左侧区域："文献爆炸"
- 显示多个分散的文献/论文图标（5-6 篇论文）
- 标注："300+ 篇文献分散于各期刊"

中间区域："条件异构"
- 显示一个参数不匹配的对比表格
- 不同单位、不同测试条件
- 标注："实验条件无法直接比对"

右侧区域："检索低效"
- 显示一个带叉号的搜索图标或沙漏
- 标注："回答一个问题需阅读 20+ 篇文献"

底部：箭头指向一个困惑的研究者图标

风格：极简图标风格，蓝灰色调，专业学术外观，无装饰元素，白色背景
```

---

## 图 1-2: RAG 技术解决方案核心思路

**必要性**: ★★★ (可选)
**用途**: 简要展示 RAG 如何解决上述问题（为第二章铺垫）

### English Prompt

```
Create a simple horizontal flowchart showing the RAG solution concept:

FLOW (left to right):
1. USER QUERY (speech bubble icon): "How to improve silica dispersion?"
2. ARROW →
3. KNOWLEDGE BASE (database/document stack icon): "Structured Literature Database"
4. ARROW →
5. AI RETRIEVAL (magnifying glass + brain icon): "Semantic Search + LLM"
6. ARROW →
7. ANSWER (document with checkmark): "Evidence-based answer with citations"

Below the flow, add a tagline: "From scattered literature to instant, traceable answers"

Style: Clean flowchart, rounded rectangles, soft blue gradient, professional academic style, horizontal layout, white background
```

### 中文提示词

```
创建一张简洁的水平流程图，展示 RAG 解决方案的核心思路：

流程（从左到右）：
1. 用户查询（对话气泡图标）："如何改善白炭黑分散性？"
2. 箭头 →
3. 知识库（数据库/文档堆叠图标）："结构化文献数据库"
4. 箭头 →
5. AI 检索（放大镜+大脑图标）："语义搜索 + 大语言模型"
6. 箭头 →
7. 回答（带勾选的文档）："有据可查的回答，附带引用"

流程下方添加标语："从分散文献到即时、可追溯的答案"

风格：简洁流程图，圆角矩形，柔和蓝色渐变，专业学术风格，水平布局，白色背景
```

---

## 图 2-1: RAG 技术原理示意图 ★★★★★

**必要性**: ★★★★★ (必需 - 核心概念图)
**用途**: 完整展示 RAG 工作流程

### English Prompt

```
Create a detailed RAG (Retrieval-Augmented Generation) architecture diagram:

TOP LEFT - User Input:
- User icon with query bubble: "What affects tensile strength?"

MIDDLE LEFT - Retrieval Module:
- Box labeled "Embedding Model"
- Arrow down to "Vector Database" (cylinder icon)
- Show query being converted to vector
- Return "Top-K Relevant Documents" (3 document icons)

MIDDLE RIGHT - Generation Module:
- Box labeled "Large Language Model (GPT)"
- Input: Query + Retrieved Documents
- Processing indicator

BOTTOM RIGHT - Output:
- Generated answer box with citation markers [1], [2], [3]
- Label: "Answer with source citations"

ARROWS: Show clear data flow with labeled arrows:
- "Query embedding" 
- "Similarity search"
- "Context injection"
- "Response generation"

Color scheme: Blue for retrieval components, green for generation components, gray for data flow
Style: Professional technical diagram, clean lines, academic publication quality, white background
```

### 中文提示词

```
创建一张详细的 RAG（检索增强生成）架构图：

左上方 - 用户输入：
- 用户图标带查询气泡："什么因素影响拉伸强度？"

中间左侧 - 检索模块：
- 标注为"嵌入模型"的方框
- 箭头指向"向量数据库"（圆柱体图标）
- 显示查询被转换为向量
- 返回"Top-K 相关文档"（3 个文档图标）

中间右侧 - 生成模块：
- 标注为"大语言模型 (GPT)"的方框
- 输入：查询 + 检索到的文档
- 处理指示器

右下方 - 输出：
- 生成的回答框，带引用标记 [1], [2], [3]
- 标注："带来源引用的回答"

箭头：用带标签的箭头显示清晰的数据流：
- "查询嵌入"
- "相似度搜索"
- "上下文注入"
- "响应生成"

配色：检索组件用蓝色，生成组件用绿色，数据流用灰色
风格：专业技术图表，线条简洁，学术出版质量，白色背景
```

---

## 图 2-2: 向量检索与重排序流程图

**必要性**: ★★★★ (推荐)
**用途**: 展示两阶段检索机制（粗筛 + 精排）

### English Prompt

```
Create a two-stage retrieval pipeline diagram:

STAGE 1 - COARSE RETRIEVAL (Left half, blue theme):
- Input: "User Query"
- Process: "Bi-Encoder" (two parallel boxes encoding query and documents)
- Vector similarity search icon
- Output: "Top-20 Candidates" (shown as a stack of documents)
- Label: "Fast ANN Search (~10ms)"

DIVIDER: Vertical dashed line

STAGE 2 - FINE RE-RANKING (Right half, orange theme):
- Input: Top-20 candidates
- Process: "Cross-Encoder" (single box with query-document pairs)
- Detailed scoring visualization
- Output: "Top-5 Results" (5 highlighted documents with scores: 0.92, 0.87, 0.85...)
- Label: "Precise Relevance Scoring (~200ms)"

BOTTOM: Performance comparison bar
- "Precision: 68% → 85% (+25%)"

Style: Split diagram with clear stage separation, professional colors, clean academic style, horizontal flow, white background
```

### 中文提示词

```
创建一张两阶段检索流程图：

第一阶段 - 粗筛检索（左半部分，蓝色主题）：
- 输入："用户查询"
- 处理："双塔编码器"（两个并行的方框分别编码查询和文档）
- 向量相似度搜索图标
- 输出："Top-20 候选"（显示为一叠文档）
- 标注："快速 ANN 搜索 (~10ms)"

分隔线：垂直虚线

第二阶段 - 精排重排序（右半部分，橙色主题）：
- 输入：Top-20 候选
- 处理："交叉编码器"（单个方框处理查询-文档对）
- 详细评分可视化
- 输出："Top-5 结果"（5 个高亮文档带分数：0.92, 0.87, 0.85...）
- 标注："精确相关性评分 (~200ms)"

底部：性能对比条
- "精度：68% → 85% (+25%)"

风格：分段式图表，阶段分隔清晰，专业配色，简洁学术风格，水平流向，白色背景
```

---

## 图 2-3: SSBR 官能化与白炭黑界面作用示意图 (可选)

**必要性**: ★★★ (可选)
**用途**: 展示不同官能团与白炭黑表面的作用方式

### English Prompt

```
Create a chemistry interface diagram showing SSBR-Silica interactions:

CENTER: Large silica particle (sphere) with Si-OH groups on surface

AROUND THE PARTICLE, show 3 different functional groups interacting:

1. HYDROXYL (-OH) interaction:
- SSBR chain with -OH end group
- Dashed line showing hydrogen bond to Si-OH
- Label: "Hydrogen bonding"

2. AMINO (-NH2) interaction:
- SSBR chain with -NH2 end group
- Dashed lines showing dual hydrogen bonds
- Label: "Strong H-bonding"

3. SILANE (-Si(OR)3) interaction:
- SSBR chain with silane end group
- Solid line showing Si-O-Si covalent bond
- Label: "Covalent bonding (strongest)"

LEGEND at bottom:
- Dashed line = Hydrogen bond
- Solid line = Covalent bond

Style: Simplified molecular diagram, not too detailed, academic chemistry style, blue-white-gray color scheme, clean white background
```

### 中文提示词

```
创建一张化学界面示意图，展示 SSBR 与白炭黑的相互作用：

中心：大的白炭黑颗粒（球体），表面带有 Si-OH 基团

颗粒周围，显示 3 种不同官能团的相互作用：

1. 羟基 (-OH) 相互作用：
- 带 -OH 端基的 SSBR 链
- 虚线显示与 Si-OH 的氢键
- 标注："氢键作用"

2. 氨基 (-NH2) 相互作用：
- 带 -NH2 端基的 SSBR 链
- 虚线显示双氢键
- 标注："强氢键作用"

3. 硅烷 (-Si(OR)3) 相互作用：
- 带硅烷端基的 SSBR 链
- 实线显示 Si-O-Si 共价键
- 标注："共价键（最强）"

底部图例：
- 虚线 = 氢键
- 实线 = 共价键

风格：简化分子示意图，不要太详细，学术化学风格，蓝白灰配色，白色背景
```

---

## 图 3-1: 系统总体架构图 ★★★★★

**必要性**: ★★★★★ (必需 - 最重要的系统图)
**用途**: 展示系统的分层架构和模块组成

### English Prompt

```
Create a layered system architecture diagram with 4 horizontal layers:

LAYER 4 (TOP) - INTERACTION LAYER (Light green):
- "Web Interface" box
- "API Endpoint" box
- "Query Input" and "Answer Output" labels

LAYER 3 - REASONING LAYER (Light orange):
- "Multi-Literature Synthesis" box
- "Trend Analysis" box
- "Extrapolation Control (CEBC)" box
- "Answer Generator" box
- Connected with internal arrows

LAYER 2 - RETRIEVAL LAYER (Light blue):
- "Query Preprocessor" box
- "Vector Search (ChromaDB)" box
- "Cross-Encoder Re-ranker" box
- "Quality Scorer" box
- Show retrieval flow arrows

LAYER 1 (BOTTOM) - DATA LAYER (Light gray):
- "Metadata Database (Excel)" cylinder
- "Interpretation Documents (Markdown)" folder icon
- "Vector Index" cylinder
- Label: "68 samples, 340 documents"

LEFT SIDE: Vertical arrow showing data flow direction (bottom to top)
RIGHT SIDE: Layer labels with brief descriptions

Style: Clean layered architecture, soft pastel colors for each layer, professional technical diagram, clear separation between layers, white background
```

### 中文提示词

```
创建一张四层水平分层的系统架构图：

第四层（顶部）- 交互层（浅绿色）：
- "Web 界面"方框
- "API 接口"方框
- "查询输入"和"回答输出"标签

第三层 - 推理层（浅橙色）：
- "多文献综合"方框
- "趋势分析"方框
- "外推控制 (CEBC)"方框
- "回答生成器"方框
- 用内部箭头连接

第二层 - 检索层（浅蓝色）：
- "查询预处理器"方框
- "向量搜索 (ChromaDB)"方框
- "交叉编码器重排序"方框
- "质量评分器"方框
- 显示检索流程箭头

第一层（底部）- 数据层（浅灰色）：
- "元数据库 (Excel)"圆柱体
- "解读文档 (Markdown)"文件夹图标
- "向量索引"圆柱体
- 标注："68 个样本，340 份文档"

左侧：垂直箭头显示数据流方向（从下到上）
右侧：层级标签及简要描述

风格：简洁分层架构，每层用柔和粉彩色，专业技术图表，层与层之间分隔清晰，白色背景
```

---

## 图 3-2: 知识库数据模型示意图

**必要性**: ★★★★ (推荐)
**用途**: 展示元数据与解读文档分离的数据组织结构

### English Prompt

```
Create a data model diagram showing the knowledge base structure:

LEFT SIDE - METADATA DATABASE:
- Excel spreadsheet icon
- Table preview showing columns:
  | Sample ID | Functional Group | Tg | Tensile Strength | ... |
  | SSBR-001  | Hydroxyl         | -25| 18.5 MPa         | ... |
  | SSBR-002  | Amino            | -28| 21.2 MPa         | ... |
- Label: "24 structured fields per sample"

CENTER - CONNECTION:
- Bidirectional arrows connecting via "Sample ID"
- Label: "Linked by Sample ID"

RIGHT SIDE - INTERPRETATION DOCUMENTS:
- Folder tree structure:
  ```
  interpretations/
  ├── SSBR-001/
  │   ├── mechanical.md
  │   ├── dsc.md
  │   ├── nmr.md
  │   └── summary.md ← (highlighted)
  ├── SSBR-002/
  │   └── ...
  ```
- Label: "5 documents per sample"

BOTTOM - VECTOR INDEX:
- Cylinder icon
- Show documents being embedded into vectors
- Label: "ChromaDB Vector Store"

Style: Clean data architecture diagram, use file/database icons, blue and gray theme, professional technical style, white background
```

### 中文提示词

```
创建一张数据模型图，展示知识库的结构：

左侧 - 元数据库：
- Excel 电子表格图标
- 表格预览显示列：
  | 样本ID | 官能团 | Tg | 拉伸强度 | ... |
  | SSBR-001 | 羟基 | -25 | 18.5 MPa | ... |
  | SSBR-002 | 氨基 | -28 | 21.2 MPa | ... |
- 标注："每个样本 24 个结构化字段"

中间 - 连接：
- 通过"样本 ID"连接的双向箭头
- 标注："通过样本 ID 关联"

右侧 - 解读文档：
- 文件夹树状结构：
  ```
  interpretations/
  ├── SSBR-001/
  │   ├── mechanical.md
  │   ├── dsc.md
  │   ├── nmr.md
  │   └── summary.md ← (高亮)
  ├── SSBR-002/
  │   └── ...
  ```
- 标注："每个样本 5 份文档"

底部 - 向量索引：
- 圆柱体图标
- 显示文档被嵌入为向量
- 标注："ChromaDB 向量存储"

风格：简洁数据架构图，使用文件/数据库图标，蓝灰色主题，专业技术风格，白色背景
```

---

## 图 3-3: 多文献综合推理流程图

**必要性**: ★★★★ (推荐)
**用途**: 展示从检索到综合结论的完整流程

### English Prompt

```
Create a horizontal pipeline flowchart for multi-literature synthesis:

STEP 1: USER QUERY
- Speech bubble: "How does functionalization level affect performance?"

STEP 2: VECTOR RETRIEVAL
- Database icon with search
- Output: "Top-10 relevant samples"

STEP 3: INFORMATION EXTRACTION
- Document with magnifying glass
- Extract: functional group type, content level, performance metrics
- Show structured data cards

STEP 4: SAMPLE AGGREGATION
- Grouping icon
- Group by: "Hydroxyl (5)", "Amino (3)", "Silane (2)"
- Show clustering visualization

STEP 5: TREND ANALYSIS
- Line chart icon
- Show upward trend arrow
- Label: "Identify patterns across samples"

STEP 6: SYNTHESIS & GENERATION
- Brain/AI icon
- Combine evidence from multiple sources
- Citation markers: [1][2][3][4][5]

STEP 7: OUTPUT
- Document with checkmarks
- "Synthesized answer with multi-source citations"

FLOW: Use arrows connecting all steps, highlight the "aggregation" step as the key innovation

Style: Horizontal flowchart, soft blue gradient, rounded rectangles, professional academic style, white background
```

### 中文提示词

```
创建一张多文献综合推理的水平流程图：

步骤 1：用户查询
- 对话气泡："官能化程度如何影响性能？"

步骤 2：向量检索
- 带搜索的数据库图标
- 输出："Top-10 相关样本"

步骤 3：信息抽取
- 带放大镜的文档
- 抽取：官能团类型、含量、性能指标
- 显示结构化数据卡片

步骤 4：样本聚合
- 分组图标
- 按以下分组："羟基 (5)"、"氨基 (3)"、"硅烷 (2)"
- 显示聚类可视化

步骤 5：趋势分析
- 折线图图标
- 显示上升趋势箭头
- 标注："识别跨样本规律"

步骤 6：综合与生成
- 大脑/AI 图标
- 整合多来源证据
- 引用标记：[1][2][3][4][5]

步骤 7：输出
- 带勾选的文档
- "综合回答，附多来源引用"

流程：用箭头连接所有步骤，突出"聚合"步骤作为核心创新

风格：水平流程图，柔和蓝色渐变，圆角矩形，专业学术风格，白色背景
```

---

## 图 4-4: 案例知识溯源路径图

**必要性**: ★★★★ (推荐)
**用途**: 展示多篇文献如何汇聚到一个回答

### English Prompt

```
Create a knowledge tracing diagram showing how multiple sources contribute to one answer:

TOP - USER QUERY:
- Question box: "How to improve silica dispersion in SSBR compounds?"

MIDDLE - SOURCE DOCUMENTS (fan out from query):
Show 5 source cards in a semi-circular arrangement:

Source 1 (SSBR-003):
- "Hydroxyl functionalization"
- Key finding: "20% improvement in dispersion"
- Confidence: 0.89

Source 2 (SSBR-007):
- "Amino end-group modification"  
- Key finding: "Filler-rubber interaction enhanced"
- Confidence: 0.85

Source 3 (SSBR-012):
- "Silane coupling comparison"
- Key finding: "Optimal: 3-5% functionalization"
- Confidence: 0.82

Source 4 (SSBR-015):
- "Processing conditions study"
- Key finding: "Mixing time affects dispersion"
- Confidence: 0.78

Source 5 (SSBR-021):
- "Morphology analysis (TEM)"
- Key finding: "Particle size reduced by 40%"
- Confidence: 0.75

BOTTOM - SYNTHESIZED ANSWER:
- Large answer box with integrated conclusion
- Show citation numbers [1]-[5] linking back to sources
- Highlight key synthesized insights

VISUAL: Use connecting lines with different weights based on confidence scores

Style: Knowledge graph style, sources as cards, connecting lines showing information flow, professional blue-gray theme, white background
```

### 中文提示词

```
创建一张知识溯源图，展示多篇文献如何汇聚成一个回答：

顶部 - 用户查询：
- 问题框："如何改善 SSBR 复合材料中的白炭黑分散性？"

中间 - 来源文档（从查询扇形展开）：
显示 5 个来源卡片，呈半圆形排列：

来源 1 (SSBR-003)：
- "羟基官能化"
- 关键发现："分散性提升 20%"
- 置信度：0.89

来源 2 (SSBR-007)：
- "氨基端基改性"
- 关键发现："填料-橡胶相互作用增强"
- 置信度：0.85

来源 3 (SSBR-012)：
- "硅烷偶联剂对比"
- 关键发现："最佳：3-5% 官能化程度"
- 置信度：0.82

来源 4 (SSBR-015)：
- "加工条件研究"
- 关键发现："混炼时间影响分散性"
- 置信度：0.78

来源 5 (SSBR-021)：
- "形态分析 (TEM)"
- 关键发现："粒径减小 40%"
- 置信度：0.75

底部 - 综合回答：
- 大的回答框，包含整合结论
- 显示引用编号 [1]-[5] 链接回各来源
- 突出关键综合见解

视觉：使用不同粗细的连接线，粗细基于置信度分数

风格：知识图谱风格，来源显示为卡片，连接线显示信息流向，专业蓝灰主题，白色背景
```

---

## 使用建议

### NapkinAI 使用技巧

1. **优先使用英文提示词** - 通常生成效果更好
2. **分段输入** - 如果提示词太长，可以先生成基本结构，再添加细节
3. **迭代优化** - 根据初次生成结果调整提示词
4. **保持简洁** - NapkinAI 擅长简洁的概念图，避免过于复杂的要求

### 图片规格建议

- **分辨率**: 导出时选择高分辨率 (至少 300 DPI)
- **格式**: 优先 PNG（无损）或 PDF（矢量）
- **尺寸**: 宽度建议 1200-1600 像素
- **背景**: 白色背景，便于插入论文

### 优先级排序

| 优先级 | 图号 | 必要性 |
|--------|------|--------|
| 1 | 图 3-1 系统总体架构图 | ★★★★★ |
| 2 | 图 2-1 RAG 技术原理示意图 | ★★★★★ |
| 3 | 图 3-3 多文献综合推理流程图 | ★★★★ |
| 4 | 图 3-2 知识库数据模型示意图 | ★★★★ |
| 5 | 图 2-2 向量检索与重排序流程图 | ★★★★ |
| 6 | 图 4-4 案例知识溯源路径图 | ★★★★ |
| 7 | 图 1-1 知识管理困境示意图 | ★★★ |
| 8 | 图 1-2 RAG 解决方案核心思路 | ★★★ |
| 9 | 图 2-3 SSBR 界面作用示意图 | ★★★ |

---

*生成日期: 2026-04-03*
*用途: 毕业论文图表*
