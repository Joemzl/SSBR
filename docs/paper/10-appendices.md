# 附录

## 附录 A：系统代码结构

### A.1 项目目录结构

```
SSBR/
├── dataset/                          # 数据层
│   ├── 数据.xlsx                     # 元数据 (24 列)
│   └── interpretations/              # 解读文档库
│       └── SSBR-XXX/                 # 各样本目录
│           ├── summary.md            # 综合档案 (RAG 核心)
│           ├── mechanical.md         # 力学解读
│           ├── dsc.md                # 热学解读
│           ├── nmr.md                # 核磁解读
│           └── tem.md                # TEM 解读
│
├── scripts/                          # 核心脚本
│   ├── qa_engine.py                  # 问答引擎主程序
│   ├── rag_search.py                 # RAG 检索模块
│   ├── answer_generator.py           # 回答生成模块
│   ├── reranker.py                   # 交叉编码器重排
│   ├── quality_scorer.py             # 质量评分模块
│   ├── models.py                     # 数据类定义
│   ├── build_vector_cache.py         # 向量缓存构建
│   ├── build_quality_cache.py        # 质量缓存构建
│   │
│   ├── synthesis/                    # 综合推理模块
│   │   ├── aggregator.py             # 样本聚合
│   │   ├── trend_analyzer.py         # 趋势分析
│   │   ├── extrapolator.py           # 外推估计
│   │   ├── formula_designer.py       # 配方设计
│   │   ├── comparison_table.py       # 对比表格
│   │   └── citation_validator.py     # 引用验证
│   │
│   ├── utils/                        # 工具函数
│   │   ├── vector_store.py           # ChromaDB 接口
│   │   ├── embedding.py              # Embedding 调用
│   │   ├── prompt_templates.py       # Prompt 模板
│   │   ├── yaml_parser.py            # YAML 解析
│   │   ├── excel_handler.py          # Excel 处理
│   │   └── exceptions.py             # 异常定义
│   │
│   └── evaluation/                   # 评测模块
│       └── ragas_evaluator.py        # RAGAS 评测器
│
├── demo/                             # Web 演示
│   └── app.py                        # Gradio 应用
│
├── .cache/                           # 缓存目录
│   └── chroma_db/                    # ChromaDB 数据
│
└── specs/                            # 规范文档
    └── 002-rag-data-migration/
        └── contracts/
            └── yaml-schema.md        # YAML Schema 定义
```

### A.2 核心模块依赖关系

```
┌─────────────────────────────────────────────────────────────┐
│                        qa_engine.py                         │
│                      (问答引擎主程序)                         │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ rag_search  │      │  reranker   │      │  answer_    │
│   .py       │      │   .py       │      │ generator.py│
└─────────────┘      └─────────────┘      └─────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│vector_store │      │ models.py   │      │  prompt_    │
│   .py       │      │             │      │ templates.py│
└─────────────┘      └─────────────┘      └─────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                      ChromaDB                                │
│                  (.cache/chroma_db/)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 附录 B：YAML Schema 定义

### B.1 summary.md Front Matter Schema

```yaml
# 必填字段
sample_id: string              # 样本编号，格式：SSBR-XXX
官能化类型: string             # 官能团中文名
官能化试剂: string             # 试剂名称（含缩写）
DOI: string                    # 原始文献 DOI

# 可选字段 - 官能化信息
官能化程度: string             # 带单位，如 "8.7 wt%"
接枝位置: string               # 链端/侧链/混合
反应类型: string               # 巯基-烯点击/阴离子聚合等

# 可选字段 - 力学性能
拉伸强度: string               # 带单位，如 "26.0 MPa"
断裂伸长率: string             # 如 "340%"
300%定伸模量: string           # 如 "8.5 MPa"
撕裂强度: string               # 如 "45 kN/m"
硬度: string                   # Shore A，如 "65"

# 可选字段 - 热学性能
Tg: string                     # 玻璃化转变温度，如 "-2.1 ℃"
Tm: string                     # 熔点（如适用）
热分解温度: string             # 如 "380 ℃"

# 可选字段 - 动态性能
tan_delta_0C: string           # 0℃ 损耗因子
tan_delta_60C: string          # 60℃ 损耗因子
Payne效应: string              # ΔG' 值
活化能: string                 # Payne 效应活化能

# 可选字段 - 填料信息
填料类型: string               # 白炭黑/炭黑/混合
填料用量: string               # phr 单位
偶联剂: string                 # Si-69 等
偶联剂用量: string             # 占填料百分比

# 可选字段 - 曲线数据 (v2.0 新增)
curves:
  stress_strain:               # 应力-应变曲线
    - strain: float            # 应变 (%)
      stress: float            # 应力 (MPa)
      confidence: float        # 置信度 (0-1)
      source: string           # L1/L2/L3
  dma_tan_delta:               # DMA tan δ 曲线
    - temperature: float       # 温度 (℃)
      tan_delta: float         # 损耗因子
      confidence: float
      source: string
```

### B.2 字段数据类型规范

| 字段类型 | 格式要求 | 示例 |
|---------|---------|------|
| 数值+单位 | `数值 单位` | `26.0 MPa`, `340%` |
| 温度 | `数值 ℃` | `-2.1 ℃`, `60 ℃` |
| 百分比 | `数值%` 或 `数值 wt%` | `8.7 wt%`, `340%` |
| DOI | 标准 DOI 格式 | `10.1016/j.polymer.2019.xxx` |
| 样本 ID | `SSBR-` + 三位数字 | `SSBR-002`, `SSBR-115` |

---

## 附录 C：完整测试查询列表

### C.1 综合分析模式测试集（12 个）

| 编号 | 查询问题 | 类型 | 复杂度 |
|------|---------|------|--------|
| Q1 | 如何通过官能化改善白炭黑分散性？ | 机理-方案推荐 | 中等 |
| Q2 | 官能化程度如何影响 Payne 效应？最佳官能化程度是多少？ | 参数优化 | 高 |
| Q3 | 羟基官能化和羧基官能化哪个更适合改善力学性能？ | 方案对比 | 高 |
| Q4 | 如何设计一个同时具有高湿地抓地力和低滚动阻力的 SSBR 配方？ | 多目标设计 | 极高 |
| Q5 | 不同文献中羧基官能化 SSBR 的性能有什么共性和差异？ | 跨文献综合 | 极高 |
| Q6 | 环氧基官能化 SSBR 有哪些优势？适合什么应用场景？ | 应用分析 | 中等 |
| Q7 | 星型支化 SSBR 相比线型 SSBR 有什么优势？ | 结构对比 | 中等 |
| Q8 | 如何通过官能化改善 SSBR 的玻璃化转变温度 (Tg)？ | 性能优化 | 中等 |
| Q9 | 活性阴离子聚合法合成官能化 SSBR 有什么优点？ | 工艺分析 | 中等 |
| Q10 | 如何选择合适的官能化试剂？不同试剂对性能有什么影响？ | 试剂选择 | 高 |
| Q11 | SSBR 与炭黑填充体系相比，白炭黑填充体系有什么优势？ | 填充对比 | 中等 |
| Q12 | 高苯乙烯含量和高乙烯基含量对 SSBR 性能有什么影响？ | 结构-性能 | 高 |

### C.2 单样本问答模式测试集（12 个）

| 编号 | 查询问题 | 目标性能 |
|------|---------|---------|
| S1 | 硅烷官能化 SSBR 的拉伸强度是多少？ | 力学性能 |
| S2 | 羟基官能化 SSBR 的断裂伸长率有多大？ | 力学性能 |
| S3 | 羧基官能化 SSBR 的拉伸强度范围？ | 力学性能 |
| S4 | SSBR-067 的 tan δ(0°C) 值是多少？ | 动态性能 |
| S5 | 氨基官能化对降低滚动阻力有什么优势？ | 动态性能 |
| S6 | 哪些官能化方案可以降低 tan δ(60°C)？ | 动态性能 |
| S7 | 如何提高 SSBR 与白炭黑的相容性？ | 界面性能 |
| S8 | 环氧基官能化程度一般是多少？ | 工艺参数 |
| S9 | 羧基官能化的 Payne 效应活化能是多少？ | 动态性能 |
| S10 | 星型支化 SSBR 常用的偶联剂有哪些？ | 合成工艺 |
| S11 | 活性阴离子聚合的分子量分布如何？ | 合成工艺 |
| S12 | 乙烯基含量对 SSBR 性能有什么影响？ | 微观结构 |

---

## 附录 D：RAGAS 评测详细数据

### D.1 综合分析模式评测结果

| Query | Faithfulness | Answer Relevancy | Context Precision | Context Recall | Citation Accuracy | Rec. Completeness | Response Time (ms) |
|-------|--------------|------------------|-------------------|----------------|-------------------|-------------------|-------------------|
| Q1 | 0.333 | 0.676 | 1.000 | - | 1.000 | 1.000 | 9483 |
| Q2 | - | - | 1.000 | - | 1.000 | 1.000 | 5780 |
| Q3 | 0.300 | 0.418 | 1.000 | - | 1.000 | 1.000 | 6853 |
| Q4 | - | 0.707 | 0.750 | 0.333 | 1.000 | 1.000 | 5698 |
| Q5 | 0.167 | 0.461 | 0.700 | 0.750 | 1.000 | 1.000 | 5684 |
| Q6 | 0.091 | 0.598 | 0.583 | - | 1.000 | 1.000 | 6693 |
| Q7 | - | 0.745 | 0.333 | - | 1.000 | 1.000 | 5239 |
| Q8 | 0.462 | 0.684 | 1.000 | - | 1.000 | 1.000 | 5782 |
| Q9 | - | - | 0.667 | - | 1.000 | 1.000 | 5043 |
| Q10 | 0.467 | 0.411 | 0.804 | 0.667 | 1.000 | 1.000 | 5420 |
| Q11 | - | - | 1.000 | - | 1.000 | 1.000 | 4662 |
| Q12 | - | 0.572 | 0.610 | 0.570 | 1.000 | 1.000 | 6359 |

### D.2 统计汇总

| 指标 | 均值 | 标准差 | 最小值 | 最大值 | 有效样本数 |
|------|------|--------|--------|--------|-----------|
| Faithfulness | 0.303 | 0.129 | 0.091 | 0.467 | 8 |
| Answer Relevancy | 0.606 | 0.128 | 0.411 | 0.745 | 9 |
| Context Precision | 0.787 | 0.223 | 0.333 | 1.000 | 12 |
| Context Recall | 0.580 | 0.199 | 0.333 | 0.750 | 4 |
| Citation Accuracy | 1.000 | 0.000 | 1.000 | 1.000 | 12 |
| Rec. Completeness | 1.000 | 0.000 | 1.000 | 1.000 | 12 |
| Response Time (ms) | 6058 | 1256 | 4662 | 9483 | 12 |

---

## 附录 E：Web 界面功能说明

### E.1 智能问答界面

**功能描述**：自然语言问答界面，支持用户输入任意关于 SSBR 官能化的问题。

**输入**：
- 问题文本框（支持中英文）
- 检索数量选择（Top-3 / Top-5 / Top-10）

**输出**：
- 直接回答段落
- 结构化推荐卡片（含引用）
- 相关样本列表
- 响应时间显示

### E.2 综合分析界面

**功能描述**：多文献综合分析，从多个样本中归纳规律。

**输入**：
- 分析主题（如"羧基官能化对力学性能的影响"）
- 目标性能选择（多选）

**输出**：
- 趋势分析图表
- 数据范围统计
- 共性规律总结
- 样本引用列表

### E.3 对比分析界面

**功能描述**：多方案结构化对比。

**输入**：
- 对比方案 A（如"羟基官能化"）
- 对比方案 B（如"羧基官能化"）
- 对比维度选择

**输出**：
- 结构化对比表格
- 各维度优劣分析
- 推荐选择建议

### E.4 配方设计界面

**功能描述**：基于目标性能的配方推荐。

**输入**：
- 目标性能设定（如"湿地抓地力=高"、"滚动阻力=低"）
- 约束条件（可选）

**输出**：
- 推荐配方列表（Top-3）
- 每个配方的详细参数
- 预期性能范围
- 置信度评估

---

## 附录 F：系统部署与使用指南

### F.1 环境要求

```
Python 3.10+
ChromaDB >= 0.4.0
sentence-transformers >= 2.2.0
openai >= 1.0.0
gradio >= 4.0.0
pandas >= 2.0.0
PyYAML >= 6.0
```

### F.2 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/xxx/ssbr-rag.git
cd ssbr-rag

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 API Key
export OPENAI_API_KEY="your-api-key"

# 5. 构建向量缓存
python scripts/build_vector_cache.py --force

# 6. 启动 Web 服务
python demo/app.py
```

### F.3 命令行使用示例

```bash
# 问答查询
python scripts/qa_engine.py --query "如何改善白炭黑分散性？"

# 综合分析
python scripts/qa_engine.py --query "官能化程度如何影响性能？" --synthesize

# 对比分析
python scripts/qa_engine.py --compare "羟基官能化" "羧基官能化"

# 配方设计
python scripts/qa_engine.py --design "高湿地抓地力低滚阻" \
    --target 湿地抓地力=高 滚动阻力=低

# 仅检索（不生成）
python scripts/qa_engine.py --query "硅烷官能化" --search-only
```

### F.4 API 接口说明

```python
from scripts.qa_engine import QAEngine

# 初始化引擎
engine = QAEngine()

# 单次问答
result = engine.query("如何改善白炭黑分散性？")
print(result.answer)
print(result.citations)

# 综合分析
synthesis = engine.synthesize(
    topic="羧基官能化对力学性能的影响",
    target_properties=["拉伸强度", "断裂伸长率"]
)

# 配方设计
formula = engine.design_formula(
    targets={"湿地抓地力": "高", "滚动阻力": "低"}
)
```

---

*附录完*
