# 必须添加图片的设计说明与制作提示词

本文档包含论文中6张"必须添加"优先级图片的详细设计说明和制作提示词，供 Nano Banana 或其他图像生成工具使用。

---

## 图片 1：系统整体架构图

**位置**：第三章 3.1.2 节

**图号**：图 3-1

**图片标题**：SSBR 官能化知识库系统整体架构图

### 详细内容说明

这是整个系统设计章节的核心图，需要展示系统的三层架构和数据流向：

1. **数据采集层**（底层）
   - 文献 PDF 输入
   - AI 辅助数据提取（豆包/Gemini/Claude）
   - Zotero 文献管理集成

2. **数据处理层**（中层）
   - Excel 元数据存储（24 列）
   - Markdown 解读文档（5 种类型）
   - YAML Schema 格式规范
   - 数据质量分级（L1/L2/L3）

3. **RAG 检索层**（顶层）
   - ChromaDB 向量数据库
   - 文本嵌入（text-embedding-3-small, 1536 维）
   - HNSW 近似最近邻搜索
   - 交叉编码器重排序（bge-reranker-base）
   - GPT 问答生成

4. **数据流箭头**
   - PDF → AI 提取 → 结构化数据 → 向量化 → ChromaDB → 检索 → 问答生成

5. **用户界面入口**（右侧或顶部）
   - Web Demo（Gradio）
   - 命令行界面
   - CodeBuddy IDE 集成

### 制作提示词

```
Create a professional technical system architecture diagram for an academic paper. The diagram should show a three-layer architecture for an "SSBR Functionalization Knowledge Base System":

LAYER 1 - DATA ACQUISITION (bottom):
- PDF Literature icon
- AI Extraction module (connecting to cloud icons for Doubao/Gemini/Claude)
- Zotero integration icon
- Arrow showing data flow upward

LAYER 2 - DATA PROCESSING (middle):
- Excel icon labeled "Metadata (24 columns)"
- Markdown files icon labeled "Interpretation Documents"
- YAML schema icon
- Data quality badge showing "L1/L2/L3 levels"
- All connected with bidirectional arrows

LAYER 3 - RAG RETRIEVAL (top):
- ChromaDB vector database cylinder
- Embedding module (1536-dim vectors visualization)
- HNSW index graph structure
- Cross-encoder reranker box
- GPT answer generator
- Flow arrows showing: Query → Vector Search → Rerank → Generate

USER INTERFACES (right side):
- Web Demo (Gradio) browser icon
- CLI terminal icon
- IDE integration icon

Style requirements:
- Clean, modern flat design with subtle shadows
- Blue and teal color scheme for professional academic look
- White background
- Chinese labels for layer names: "数据采集层", "数据处理层", "RAG 检索层"
- English labels for technical components
- Clear directional arrows showing data flow
- Consistent icon style throughout
- Size: 1920x1080 pixels, landscape orientation

Reference content from paper:
"系统采用分层架构，从底层数据采集到上层智能问答形成完整的数据处理管道。"
"数据流经的完整路径为：PDF 文献 → AI 提取 → 结构化数据 → 向量化 → ChromaDB → 检索 → 问答生成"
```

---

## 图片 2：Web Demo 界面截图

**位置**：第三章 3.6.1 节

**图号**：图 3-2

**图片标题**：SSBR 官能化知识库 Web Demo 界面

### 详细内容说明

这是展示系统实际运行形态的关键截图，需要展示 Gradio 界面的四个功能标签页：

1. **智能问答标签页**（默认显示）
   - 输入框：用户问题
   - 输出区域：推荐方案卡片 + 自然语言回答 + 文献引用
   - 示例问题按钮

2. **综合分析标签页**
   - 输入框：综合问题
   - 趋势分析结果展示
   - 置信度标签

3. **对比分析标签页**
   - 两个输入框：方案 A、方案 B
   - Markdown 对比表格输出
   - 优劣势总结

4. **配方设计标签页**
   - 目标性能输入
   - 配方推荐卡片
   - 设计理由和文献支撑

### 制作提示词

```
Create a realistic mockup of a Web Demo interface for an academic knowledge base system. The interface is built with Gradio framework and has a clean, modern design.

MAIN LAYOUT:
- Header: "SSBR 官能化知识库" (SSBR Functionalization Knowledge Base)
- Four tabs in a row: "智能问答" (active, highlighted), "综合分析", "对比分析", "配方设计"

ACTIVE TAB CONTENT (智能问答 - Q&A):
Left panel:
- Input text box with placeholder "请输入您的问题..."
- Example buttons: "如何改善白炭黑分散性？", "羟基官能化的优势？"
- Submit button (blue)

Right panel (output area):
- Recommendation card with title "🎯 推荐方案":
  | 参数 | 推荐值 | 置信度 |
  |------|--------|--------|
  | 推荐官能团 | 羟基 (-OH) | 高 |
  | 推荐试剂 | 3-巯基丙醇 | 高 |
  | 推荐程度 | 2.5-4.0 wt% | 中 |

- Natural language answer section (300-400 Chinese characters, blurred/placeholder)
- References section: "📚 数据来源: [1] Zhang et al., 2024..."

FOOTER:
- "Powered by ChromaDB + GPT-4" badge
- Response time indicator: "响应时间: 4.2s"

Style requirements:
- Gradio default styling with blue accent color
- Light gray background (#f5f5f5)
- White content cards with subtle shadows
- Chinese text throughout
- Size: 1920x1080 pixels
- Show it as a browser window with URL "localhost:7861"

Reference content from paper:
"基于 Gradio 框架的 Web 界面，包含四个功能标签页：智能问答、综合分析、对比分析、配方设计"
"启动命令：python demo/app.py  # 默认端口 7861"
```

---

## 图片 3：官能化程度-性能趋势图

**位置**：第四章 4.3.1 节

**图号**：图 4-1

**图片标题**：官能化程度与性能指标关系趋势示意图

### 详细内容说明

这是趋势分析模块的核心可视化图，展示官能化程度与多种性能指标的关系：

1. **图表类型**：多子图面板（2×2 或 1×4 布局）

2. **子图内容**：
   - **子图 A**：官能化程度 vs 拉伸强度
     - X 轴：官能化程度 (0-10 wt%)
     - Y 轴：拉伸强度 (10-30 MPa)
     - 散点 + 趋势线（上升趋势）
     - 数据点标注样本来源
   
   - **子图 B**：官能化程度 vs 断裂伸长率
     - X 轴：官能化程度 (0-10 wt%)
     - Y 轴：断裂伸长率 (200-600%)
     - 散点 + 趋势线（下降趋势）
   
   - **子图 C**：官能化程度 vs Tg
     - X 轴：官能化程度 (0-10 wt%)
     - Y 轴：Tg (-40 to 0°C)
     - 散点 + 趋势线（上升趋势）
   
   - **子图 D**：官能化程度 vs Payne 效应
     - X 轴：官能化程度 (0-10 wt%)
     - Y 轴：Payne 效应指数 (0-2)
     - 散点 + 趋势线（下降趋势）

3. **置信度标注**：
   - 高置信度趋势线：实线
   - 中等置信度：虚线
   - 低置信度：点线

4. **数据范围阴影**：
   - 数据覆盖区域：浅色填充
   - 外推区域：不填充或极浅色

### 制作提示词

```
Create a scientific figure with four subplots showing the relationship between functionalization degree and various performance metrics for SSBR rubber. This is for an academic paper on materials science.

LAYOUT: 2×2 grid of subplots (A, B, C, D)

SUBPLOT A (top-left): "官能化程度 vs 拉伸强度"
- X-axis: "官能化程度 (wt%)" range 0-10
- Y-axis: "拉伸强度 (MPa)" range 10-30
- 6-8 scatter points showing INCREASING trend
- Solid blue trend line with confidence band
- Points labeled with sample sources (small text)
- Trend arrow pointing up with "↑ 上升趋势"

SUBPLOT B (top-right): "官能化程度 vs 断裂伸长率"
- X-axis: "官能化程度 (wt%)" range 0-10
- Y-axis: "断裂伸长率 (%)" range 200-600
- 6-8 scatter points showing DECREASING trend
- Dashed orange trend line
- Trend arrow pointing down with "↓ 下降趋势"

SUBPLOT C (bottom-left): "官能化程度 vs Tg"
- X-axis: "官能化程度 (wt%)" range 0-10
- Y-axis: "Tg (°C)" range -40 to 0
- 5-7 scatter points showing INCREASING trend
- Solid green trend line
- "↑ 上升趋势"

SUBPLOT D (bottom-right): "官能化程度 vs Payne 效应"
- X-axis: "官能化程度 (wt%)" range 0-10
- Y-axis: "Payne 效应 (ΔG')" range 0-2
- 5-7 scatter points showing DECREASING trend
- Solid red trend line
- "↓ 下降趋势 (改善)"

COMMON ELEMENTS:
- Light gray shaded area indicating "数据覆盖范围" (data range)
- Legend showing: "● 样本数据点", "— 高置信度趋势", "-- 中等置信度"
- Scientific plot style with gridlines
- Chinese axis labels and subplot titles
- Size: 1600x1200 pixels

Reference from paper:
"系统当前支持以下变量对的趋势分析：官能化程度 vs 拉伸强度、断裂伸长率、Tg、Payne 效应"
"采用相邻点变化方向统计法判断趋势，阈值 70% 确保趋势判断的稳健性"
```

---

## 图片 4：50% 边界规则示意图

**位置**：第四章 4.4.2 节

**图号**：图 4-2

**图片标题**：上下文外推边界控制策略 (CEBC) 示意图

### 详细内容说明

这是 CEBC 策略的核心图，展示数据范围和外推边界的关系：

1. **主体内容**：一维数轴展示
   - 数据范围：[x_min, x_max]
   - 外推边界：[-50%, +50%] 范围
   - 禁止区域：超出外推边界的部分

2. **视觉元素**：
   - **绿色区域**：数据覆盖范围（高置信度）
   - **黄色区域**：允许外推范围（中等置信度）
   - **红色区域**：禁止预测区域

3. **标注**：
   - 数学公式展示边界计算
   - 置信度衰减曲线（可选）
   - 示例数值（如 2.0-6.8 wt% 外推至 0.6-9.2 wt%）

4. **右侧/下方**：
   - 置信度衰减曲线图
   - 指数衰减公式

### 制作提示词

```
Create a technical diagram illustrating the "Context-aware Extrapolation Boundary Control (CEBC)" strategy for an academic paper. This diagram explains the 50% boundary rule for data extrapolation.

MAIN VISUALIZATION (horizontal number line):

Left section (RED, striped pattern):
- Label: "禁止预测区域"
- Range indicator: "< 0.6 wt%"
- Icon: ⛔ or X mark

Left-middle section (YELLOW/ORANGE gradient):
- Label: "外推区域 (-50%)"
- Range: "0.6 - 2.0 wt%"
- Badge: "⚠️ 中等置信度"
- Confidence indicator decreasing leftward

CENTER section (GREEN, solid fill):
- Label: "数据覆盖范围"
- Range: "2.0 - 6.8 wt%"
- Badge: "✓ 高置信度"
- Scatter points representing actual data

Right-middle section (YELLOW/ORANGE gradient):
- Label: "外推区域 (+50%)"
- Range: "6.8 - 9.2 wt%"
- Badge: "⚠️ 中等置信度"
- Confidence indicator decreasing rightward

Right section (RED, striped pattern):
- Label: "禁止预测区域"
- Range indicator: "> 9.2 wt%"
- Icon: ⛔ or X mark

MATHEMATICAL FORMULAS (below the number line):
- Left formula: "x_ext_min = x_min - 0.5 × (x_max - x_min)"
- Right formula: "x_ext_max = x_max + 0.5 × (x_max - x_min)"

CONFIDENCE DECAY CURVE (bottom right inset):
- Small line graph showing exponential decay
- X-axis: "外推距离"
- Y-axis: "置信度"
- Formula: "C = C_base × exp(-λ × d_ext / r_data)"

ANNOTATIONS:
- Bracket showing "数据范围 r = 4.8 wt%"
- Arrows indicating the 50% extension on each side

Style requirements:
- Clean infographic style
- Color scheme: Green (#2ecc71), Yellow (#f1c40f), Red (#e74c3c)
- White background
- Chinese labels with English technical terms
- Size: 1600x900 pixels, landscape

Reference from paper:
"系统仅允许在数据覆盖范围之外 50% 的区间内进行外推预测"
"在材料性能变化通常是渐进的假设下，数据边界附近的小幅外推风险相对可控"
"当用户查询落入外推区间时，系统使用指数衰减模型计算预测置信度"
```

---

## 图片 5：官能团类型分布图

**位置**：第五章 5.1.2 节

**图号**：图 5-1

**图片标题**：SSBR 官能化知识库官能团类型分布

### 详细内容说明

这是数据集概览的关键可视化，展示 68 个样本的官能团类型分布：

1. **图表类型**：饼图 + 柱状图组合（或二选一）

2. **数据内容**：
   | 官能团类型 | 样本数 | 占比 |
   |-----------|--------|------|
   | 硅烷基 (Silane) | 15 | 22.1% |
   | 羧基 (Carboxyl) | 12 | 17.6% |
   | 羟基 (Hydroxyl) | 11 | 16.2% |
   | 氨基 (Amino) | 9 | 13.2% |
   | 环氧基 (Epoxy) | 7 | 10.3% |
   | 酯基 (Ester) | 5 | 7.4% |
   | 锡基 (Tin) | 4 | 5.9% |
   | 其他 | 5 | 7.4% |

3. **设计要求**：
   - 配色方案应区分度高
   - 每个扇区/柱子标注数量和百分比
   - 总计样本数：68 个
   - 文献来源数：23 篇

### 制作提示词

```
Create a professional data visualization showing the distribution of functional group types in the SSBR functionalization knowledge base. This is for an academic paper on materials science.

MAIN CHART: Donut/Pie Chart (left side, 60% of width)
- Total: 68 samples
- Segments with labels and percentages:
  1. 硅烷基 (Silane): 15 samples, 22.1% - Deep Blue (#3498db)
  2. 羧基 (Carboxyl): 12 samples, 17.6% - Red (#e74c3c)
  3. 羟基 (Hydroxyl): 11 samples, 16.2% - Green (#2ecc71)
  4. 氨基 (Amino): 9 samples, 13.2% - Orange (#f39c12)
  5. 环氧基 (Epoxy): 7 samples, 10.3% - Purple (#9b59b6)
  6. 酯基 (Ester): 5 samples, 7.4% - Cyan (#1abc9c)
  7. 锡基 (Tin): 4 samples, 5.9% - Pink (#e91e63)
  8. 其他 (Others): 5 samples, 7.4% - Gray (#95a5a6)

CENTER OF DONUT:
- Large number "68"
- Text below: "总样本数"

SECONDARY CHART: Horizontal Bar Chart (right side, 35% of width)
- Same data as bars, sorted by count descending
- Each bar labeled with count and percentage
- Provides alternative view for exact comparison

HEADER:
- Title: "SSBR 官能化知识库样本分布"
- Subtitle: "68 个样本 | 23 篇文献 | 12 种官能团"

LEGEND (bottom):
- Horizontal layout with color swatches and both Chinese and English names
- Format: "色块 中文名 (English) - N个 (XX%)"

Style requirements:
- Clean, modern infographic style
- White background with subtle grid
- Professional color palette (distinct but harmonious)
- Chinese labels as primary, English in parentheses
- Size: 1600x1000 pixels

Reference from paper:
"知识库包含：总样本数 68 个，文献来源数 23 篇，官能团类型 12 种"
"官能团类型分布：硅烷基 15(22.1%), 羧基 12(17.6%), 羟基 11(16.2%)..."
```

---

## 图片 6：RAGAS 评估流程图

**位置**：第五章 5.5.4 节

**图号**：图 5-2

**图片标题**：RAGAS 评测框架流程图

### 详细内容说明

这是评测方法章节的核心图，展示 RAGAS 评估的完整流程：

1. **输入层**：
   - 测试查询集（24 个问题）
   - Ground Truth（标准答案）

2. **系统处理流程**：
   - Query → Retriever → Contexts
   - Contexts → Generator → Answer

3. **评估指标计算**：
   - Faithfulness（忠实度）
   - Answer Relevancy（回答相关性）
   - Context Precision（上下文精度）
   - Context Recall（上下文召回率）

4. **自定义指标**：
   - Citation Accuracy（引用准确性）
   - Recommendation Completeness（推荐完整性）

5. **输出层**：
   - 评估报告
   - 分数汇总
   - 可视化图表

### 制作提示词

```
Create a flowchart diagram illustrating the RAGAS (Retrieval-Augmented Generation Assessment) evaluation framework for an academic paper. The diagram should show the complete evaluation pipeline.

LAYOUT: Top-to-bottom flow with parallel evaluation branches

INPUT SECTION (top):
- Box: "测试查询集" (Test Query Set)
  - Sub-label: "24 个问题 (综合12 + 单样本12)"
- Box: "Ground Truth"
  - Sub-label: "标准答案 + 支持上下文"
- Arrow pointing down

SYSTEM PIPELINE (middle, horizontal flow):
1. Box: "Query (问题)" - Blue
   Arrow →
2. Box: "Retriever (检索器)" - Blue
   - Sub-label: "ChromaDB + HNSW"
   Arrow →
3. Box: "Contexts (检索上下文)" - Blue
   - Sub-label: "Top-5 相关样本"
   Arrow →
4. Box: "Generator (生成器)" - Blue
   - Sub-label: "GPT-4"
   Arrow →
5. Box: "Answer (回答)" - Blue

EVALUATION BRANCHES (bottom, 4 parallel paths from Answer/Contexts):

Branch 1 (from Answer + Contexts):
- Diamond: "Faithfulness Eval"
- Output box: "忠实度 (Faithfulness)"
- Formula hint: "支持声明 / 总声明"

Branch 2 (from Answer + Query):
- Diamond: "Relevancy Eval"
- Output box: "回答相关性 (Answer Relevancy)"
- Formula hint: "反向问题相似度"

Branch 3 (from Contexts + Ground Truth):
- Diamond: "Precision Eval"
- Output box: "上下文精度 (Context Precision)"
- Formula hint: "加权 Precision@K"

Branch 4 (from Contexts + Ground Truth):
- Diamond: "Recall Eval"
- Output box: "上下文召回率 (Context Recall)"
- Formula hint: "信息覆盖率"

CUSTOM METRICS (additional row, highlighted differently):
- Box: "引用准确性 (Citation Accuracy)" - Orange
- Box: "推荐完整性 (Recommendation Completeness)" - Orange
- Label: "自定义评估指标"

OUTPUT SECTION (bottom):
- All arrows converge to:
- Large box: "评估报告 & 可视化"
  - Icons for: 雷达图, 柱状图, 热力图

Style requirements:
- Professional flowchart style
- Blue color scheme for system components
- Orange for custom metrics
- Gray for Ground Truth
- White background
- Chinese primary labels with English in parentheses
- Clear directional arrows
- Size: 1600x1200 pixels

Reference from paper:
"RAGAS 是由 Explodinggradients 团队开发的开源 RAG 系统评估框架"
"核心指标包括：Faithfulness、Answer Relevancy、Context Precision、Context Recall"
"针对本系统设计了两个自定义指标：引用准确性、推荐完整性"
```

---

## 使用说明

### 如何使用这些提示词

1. **选择工具**：将提示词复制到 Nano Banana、Midjourney、DALL-E 或其他图像生成工具

2. **调整参数**：
   - 尺寸：根据论文排版需求调整（建议保持 16:9 或 4:3 比例）
   - 语言：如需纯英文版本，可要求翻译所有标签

3. **迭代优化**：
   - 生成初版后，可根据实际效果进行微调
   - 关注技术细节的准确性

4. **后处理**：
   - 使用 Photoshop/Figma 进行最终调整
   - 确保字体清晰、颜色一致

### 文件命名建议

| 图号 | 建议文件名 | 位置 |
|------|-----------|------|
| 图 3-1 | `system_architecture.png` | 第三章 |
| 图 3-2 | `web_demo_interface.png` | 第三章 |
| 图 4-1 | `trend_analysis.png` | 第四章 |
| 图 4-2 | `cebc_boundary_rule.png` | 第四章 |
| 图 5-1 | `functional_group_distribution.png` | 第五章 |
| 图 5-2 | `ragas_evaluation_flow.png` | 第五章 |

### 注意事项

- 所有图片应保存为 300 DPI 以上的高分辨率
- 建议同时准备 PNG（带透明背景）和 PDF 格式
- 确保图中文字在打印时清晰可读（最小字号 8pt）
