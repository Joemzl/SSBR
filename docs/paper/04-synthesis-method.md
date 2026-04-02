# 第四章 多文献综合推理方法

## 4.1 从单样本检索到知识综合的范式升级

### 4.1.1 单样本检索的局限性

传统的 RAG（检索增强生成）系统在材料科学领域的应用通常采用"单样本检索-直接回答"的模式：针对用户查询检索最相关的一条或少数几条记录，然后基于检索结果生成回答。这种模式在回答简单的事实性查询时表现良好，但面对材料研究中常见的复杂问题时存在明显不足：

**局限性一：视野受限**

单样本检索仅能反映特定文献、特定实验条件下的结果，无法展现材料体系的全貌。例如，当用户询问"羟基官能化对拉伸强度的影响"时，单样本检索可能返回某篇文献中 3.6 wt% 官能化程度下的强度数据，但无法呈现不同官能化程度下强度变化的完整趋势。

**局限性二：结论片面**

不同研究团队采用的实验条件（聚合方法、填料体系、硫化配方等）存在差异，单一样本的结论难以代表普遍规律。综合多篇文献的数据可以更全面地认识官能化效果的一般性和特殊性。

**局限性三：无法支撑高阶应用**

配方设计、多方案对比等高阶应用需要跨文献的信息聚合和规律提取，单样本检索模式难以直接支撑这类需求。

### 4.1.2 多文献综合推理的目标

为突破上述局限，本研究提出从"单样本检索"升级为"多文献综合推理"的范式转变。具体目标包括：

1. **信息聚合**：将多篇相关文献的数据汇总，形成对问题的全面认识
2. **规律提取**：从分散的数据点中识别趋势和模式
3. **保守外推**：在数据支撑范围内进行有限度的预测
4. **冲突解决**：处理不同文献间的数据差异和结论矛盾
5. **高阶应用支撑**：为对比分析、配方设计等复杂需求提供基础能力

### 4.1.3 四种综合模式

系统设计了四种综合模式以满足不同类型的用户需求：

| 模式 | 代码标识 | 应用场景 | 典型查询示例 |
|------|----------|----------|--------------|
| **单样本模式** | `SINGLE` | 查询特定样本数据 | "SSBR-002 的拉伸强度是多少？" |
| **综合分析模式** | `SYNTHESIS` | 跨文献的规律总结 | "官能化程度如何影响力学性能？" |
| **对比分析模式** | `COMPARISON` | 多方案结构化对比 | "对比羟基和氨基官能化的效果" |
| **配方设计模式** | `FORMULA` | 基于目标的配方推荐 | "设计高湿地抓地力低滚阻的配方" |

模式选择通过查询意图识别自动完成，用户也可通过命令行参数显式指定：

```bash
# 综合分析模式
python scripts/qa_engine.py --query "官能化程度如何影响性能？" --synthesize

# 对比分析模式
python scripts/qa_engine.py --compare "羟基官能化" "氨基官能化"

# 配方设计模式
python scripts/qa_engine.py --design "高湿地抓地力低滚阻" \
    --target 湿地抓地力=高 滚动阻力=低
```

## 4.2 样本聚合算法

### 4.2.1 相关样本筛选策略

样本聚合是多文献综合的第一步，目标是从知识库中筛选出与查询相关的高质量样本。筛选策略遵循以下原则：

**语义相似性筛选**

首先通过向量检索获取语义上最相关的候选样本，检索数量（top_k）根据综合模式动态调整：

```python
# 不同模式的检索数量配置
TOP_K_CONFIG = {
    SynthesisMode.SINGLE: 5,       # 单样本模式：精准匹配
    SynthesisMode.SYNTHESIS: 15,   # 综合模式：广泛收集
    SynthesisMode.COMPARISON: 10,  # 对比模式：按方案分组
    SynthesisMode.FORMULA: 12,     # 配方设计：多维考量
}
```

**质量感知过滤**

在相似性筛选基础上，应用质量分数阈值过滤低质量样本：

$$
\text{Filtered} = \{s \mid s \in \text{Candidates}, \text{quality}(s) \geq \tau_q\}
$$

其中 $\tau_q$ 为质量阈值（默认 0.4），确保进入综合分析的样本具有足够的数据完整性。

**多样性约束**

为避免综合结果过度依赖单一文献，系统限制来自同一 DOI 的样本数量：

```python
def apply_diversity_constraint(samples, max_per_doi=3):
    """限制每篇文献最多贡献 3 个样本"""
    doi_count = {}
    diverse_samples = []
    for sample in samples:
        doi = sample.doi or sample.sample_id
        if doi_count.get(doi, 0) < max_per_doi:
            diverse_samples.append(sample)
            doi_count[doi] = doi_count.get(doi, 0) + 1
    return diverse_samples
```

### 4.2.2 信息抽取与结构化

筛选出的样本需要从 summary.md 文档中提取结构化信息。`SampleAggregator` 类实现了这一功能：

```python
@dataclass
class SampleSummary:
    """样本结构化摘要"""
    sample_id: str
    
    # 官能化信息
    functional_group: str           # 核心官能团名称
    functionalization_degree: str   # 官能化程度（如 "3.6 wt%"）
    reagent: str                    # 官能化试剂
    method: str                     # 官能化方法
    
    # 关键性能指标
    tensile_strength: Optional[str] = None      # 拉伸强度
    elongation: Optional[str] = None            # 断裂伸长率
    tg: Optional[str] = None                    # 玻璃化转变温度
    payne_effect: Optional[str] = None          # Payne 效应
    tan_delta_0c: Optional[str] = None          # 湿地抓地力指标
    tan_delta_60c: Optional[str] = None         # 滚动阻力指标
    
    # 文献来源
    doi: Optional[str] = None
    first_author: Optional[str] = None
    year: Optional[int] = None
```

聚合器从 YAML front matter 和 Markdown 正文两个来源提取信息，优先使用结构化的 YAML 数据：

```python
def extract_summary(self, sample_id, content, similarity, quality_score):
    """从 summary.md 提取结构化摘要"""
    # 1. 解析 YAML front matter
    yaml_data = self._parse_yaml_front_matter(content)
    
    # 2. 从 Markdown 正文提取补充信息
    markdown_data = self._parse_markdown_content(content)
    
    # 3. 合并数据（YAML 优先）
    merged = {**markdown_data, **yaml_data}
    
    # 4. 构建 SampleSummary 实例
    return SampleSummary(
        sample_id=sample_id,
        functional_group=merged.get('functional_group', '未知官能团'),
        # ... 其他字段映射
    )
```

### 4.2.3 数据范围统计

为支持后续的趋势分析和外推判断，聚合器计算各数值字段的数据范围：

```python
def get_data_ranges(self, summaries):
    """从样本摘要中计算数据范围"""
    numeric_fields = {
        'functionalization_degree': ('wt%', []),
        'tensile_strength': ('MPa', []),
        'tg': ('°C', []),
    }
    
    for summary in summaries:
        # 解析并收集数值
        ...
    
    # 构建 DataRange 对象
    data_ranges = {}
    for field_name, (unit, values) in numeric_fields.items():
        if len(values) >= 2:
            data_ranges[field_name] = DataRange(
                field_name=field_name,
                min_value=min(values),
                max_value=max(values),
                unit=unit,
                data_points=len(values)
            )
    
    return data_ranges
```

`DataRange` 数据类封装了数据边界和外推边界的计算：

```python
@dataclass
class DataRange:
    field_name: str
    min_value: float
    max_value: float
    unit: str
    data_points: int
    
    @property
    def extrapolation_min(self) -> float:
        """允许的外推下界（范围外 50%）"""
        range_size = self.max_value - self.min_value
        return max(0, self.min_value - range_size * 0.5)
    
    @property
    def extrapolation_max(self) -> float:
        """允许的外推上界（范围外 50%）"""
        range_size = self.max_value - self.min_value
        return self.max_value + range_size * 0.5
```

## 4.3 趋势分析与规律发现

### 4.3.1 官能化程度-性能关系建模

趋势分析是综合推理的核心能力之一，旨在从多个样本的离散数据点中识别变量间的关系模式。`TrendAnalyzer` 类实现了定性趋势识别算法。图 4-1 展示了典型的官能化程度与性能指标关系趋势图。

<!-- TODO: 插入图片 -->
<!-- 图片文件: figures/trend_analysis.png -->
<!-- 图片说明: 四子图面板，展示官能化程度与拉伸强度、断裂伸长率、Tg、Payne效应的关系趋势 -->

**图 4-1 官能化程度与性能指标关系趋势示意图**

**支持的变量关系**

系统当前支持以下变量对的趋势分析：

| 自变量 | 因变量 | 物理意义 |
|--------|--------|----------|
| 官能化程度 | 拉伸强度 | 官能团浓度对力学强度的影响 |
| 官能化程度 | 断裂伸长率 | 官能团浓度对柔韧性的影响 |
| 官能化程度 | Tg | 官能团浓度对玻璃化转变的影响 |
| 官能化程度 | Payne 效应 | 官能团浓度对填料分散的影响 |

**趋势方向判断算法**

采用相邻点变化方向统计法判断趋势：

```python
def _detect_direction(self, x_values, y_values) -> str:
    """检测趋势方向"""
    # 计算相邻点的变化方向
    increases = 0
    decreases = 0
    
    for i in range(1, len(y_values)):
        if y_values[i] > y_values[i-1]:
            increases += 1
        elif y_values[i] < y_values[i-1]:
            decreases += 1
    
    total = increases + decreases
    if total == 0:
        return "none"
    
    # 如果 70% 以上一致方向，认为有趋势
    if increases / total >= 0.7:
        return "increasing"
    elif decreases / total >= 0.7:
        return "decreasing"
    else:
        return "none"
```

该算法的设计考量：
- 阈值 70% 而非 50%，确保趋势判断的稳健性
- 不要求严格单调，允许存在噪声和异常点
- 当数据点分布较散乱时，返回"无明显趋势"的保守结论

**趋势描述生成**

根据检测到的趋势方向生成自然语言描述：

```python
if trend_direction == "increasing":
    description = f"随着{x_name}的增加，{y_name}呈现上升趋势"
elif trend_direction == "decreasing":
    description = f"随着{x_name}的增加，{y_name}呈现下降趋势"
else:
    description = f"{x_name}与{y_name}之间未观察到明显的线性趋势"
```

### 4.3.2 置信度分级

趋势分析结果附带置信度标签，反映数据支撑的充分程度：

```python
def _determine_confidence(self, data_points, trend_direction) -> ConfidenceTag:
    """确定置信度标签"""
    if trend_direction == "none":
        return ConfidenceTag.LOW
    
    if data_points >= 5:
        return ConfidenceTag.HIGH
    elif data_points >= 3:
        return ConfidenceTag.MEDIUM
    else:
        return ConfidenceTag.LOW
```

| 置信度 | 数据点要求 | 用户提示 |
|--------|------------|----------|
| **HIGH** | ≥5 个且趋势明确 | "高置信度，基于 5+ 个数据点" |
| **MEDIUM** | 3-4 个且趋势明确 | "中等置信度，基于 3-4 个数据点" |
| **LOW** | <3 个或趋势不明 | "低置信度，数据有限" |

### 4.3.3 趋势分析输出

`TrendAnalysis` 数据类封装完整的趋势分析结果：

```python
@dataclass
class TrendAnalysis:
    variable_x: str                     # 自变量名称
    variable_y: str                     # 因变量名称
    trend_description: str              # 趋势定性描述
    supporting_data: List[Dict]         # [{sample_id, x_value, y_value}, ...]
    data_range: DataRange               # 数据覆盖范围
    confidence: ConfidenceTag           # 置信度标签
    
    def to_display_text(self) -> str:
        """生成用户可见的趋势描述"""
        return (
            f"{self.trend_description}\n"
            f"（{self.confidence.value}置信度，"
            f"基于 {len(self.supporting_data)} 个数据点）"
        )
```

## 4.4 上下文外推边界控制策略 (CEBC)

### 4.4.1 理论动机：防止"数值幻觉"

大语言模型（LLM）在生成回答时存在"幻觉"（Hallucination）风险，即生成看似合理但实际上没有依据的内容。在材料科学领域，这种风险在数值预测场景下尤为突出：

**材料性能的物理化学边界约束**

材料性能受到物理化学规律的约束，并非可以无限外推。例如：
- 官能化程度过高会导致橡胶分子量下降，反而降低力学性能
- 官能团含量与填料分散改善并非线性关系，存在饱和效应
- 某些官能团在高浓度时可能产生副反应

**LLM 外推预测的风险**

当用户查询的条件超出已有数据范围时，LLM 可能：
1. 简单线性外推，忽略非线性效应
2. 生成看似精确但缺乏依据的具体数值
3. 对超出数据范围的预测过度自信

为此，本研究提出**上下文外推边界控制策略**（Context-aware Extrapolation Boundary Control, CEBC），在利用数据趋势进行预测的同时，严格控制外推范围并标注不确定性。

### 4.4.2 50% 边界规则的设计逻辑

CEBC 的核心是"50% 边界规则"：系统仅允许在数据覆盖范围之外 50% 的区间内进行外推预测。

**数学定义**

设数据范围为 $[x_{min}, x_{max}]$，则允许的外推区间为：

$$
\text{Extrapolation Range} = \left[ x_{min} - 0.5 \cdot (x_{max} - x_{min}), \quad x_{max} + 0.5 \cdot (x_{max} - x_{min}) \right]
$$

在代码实现中：

```python
@property
def extrapolation_min(self) -> float:
    """允许的外推下界（范围外 50%）"""
    range_size = self.max_value - self.min_value
    return max(0, self.min_value - range_size * 0.5)

@property
def extrapolation_max(self) -> float:
    """允许的外推上界（范围外 50%）"""
    range_size = self.max_value - self.min_value
    return self.max_value + range_size * 0.5
```

**设计依据**

选择 50% 作为边界的原因：

1. **保守原则**：对于科研数据，宁可承认"不知道"也不应给出不可靠的预测
2. **实用性平衡**：完全禁止外推会降低系统的实用价值，50% 允许有限度的预测
3. **物理合理性**：在材料性能变化通常是渐进的假设下，数据边界附近的小幅外推风险相对可控
4. **与物理模型外推的对比**：物理模型（如 WLF 方程、Ogden 模型）可在理论框架内外推，但本系统是数据驱动的，缺乏理论支撑时应更保守

### 4.4.3 外推置信度评分模型

当用户查询落入外推区间时，系统使用指数衰减模型计算预测置信度：

$$
C_{ext} = C_{base} \cdot \exp\left(-\lambda \cdot \frac{d_{ext}}{r_{data}}\right)
$$

其中：
- $C_{base}$ 为基础置信度（取决于数据点数量）
- $d_{ext}$ 为外推距离（查询值与最近数据边界的距离）
- $r_{data}$ 为数据范围（$x_{max} - x_{min}$）
- $\lambda$ 为衰减系数（默认 2.0）

该模型确保：
- 外推距离越远，置信度越低
- 即使在允许的外推范围内，也不会给出过高的置信度

**实现代码**

```python
def _determine_confidence(
    self,
    data_points: int,
    is_extrapolation: bool,
    within_range: bool
) -> ConfidenceTag:
    """确定置信度标签"""
    if data_points >= 5 and within_range:
        return ConfidenceTag.HIGH
    elif data_points >= 3:
        return ConfidenceTag.MEDIUM
    else:
        return ConfidenceTag.LOW
```

### 4.4.4 边界验证与异常处理

`Extrapolator` 类实现了边界验证逻辑：

```python
def validate_boundary(self, query_value, data_range):
    """验证查询值是否在允许的外推范围内"""
    if data_range.is_within_data(query_value):
        return True, None  # 在数据范围内，无警告
    
    if data_range.is_within_extrapolation(query_value):
        # 在外推范围内，返回警告
        warning = (
            f"此预测超出数据覆盖范围"
            f"（{data_range.min_value:.1f}-{data_range.max_value:.1f} {data_range.unit} "
            f"外推至 {data_range.extrapolation_min:.1f}-"
            f"{data_range.extrapolation_max:.1f} {data_range.unit}），"
            f"仅供参考"
        )
        return True, warning
    
    # 超出外推边界，拒绝预测
    raise ExtrapolationBoundaryError(
        query_value=query_value,
        allowed_range=(data_range.extrapolation_min, 
                       data_range.extrapolation_max),
        unit=data_range.unit
    )
```

### 4.4.5 不确定性量化与置信区间

外推预测结果以区间形式呈现，而非单一数值，明确传达预测的不确定性：

```python
@dataclass
class ExtrapolationResult:
    query_value: float              # 查询的自变量值
    query_unit: str                 # 单位
    predicted_range: tuple          # 预测值区间 (min, max)
    predicted_unit: str             # 预测值单位
    confidence: ConfidenceTag       # 置信度标签
    data_points_used: int           # 使用的数据点数
    is_extrapolation: bool          # 是否为外推
    boundary_warning: Optional[str] # 边界警告信息
    
    def to_display_text(self) -> str:
        """生成用户可见的预测描述"""
        range_str = f"{self.predicted_range[0]:.1f}-" \
                    f"{self.predicted_range[1]:.1f} {self.predicted_unit}"
        prefix = "⚠️ **外推估计**：" if self.is_extrapolation \
                 else "**估计值**："
        confidence_str = f"（{self.confidence.value}置信度，" \
                         f"基于 {self.data_points_used} 个相近样本）"
        
        result = f"{prefix}{range_str} {confidence_str}"
        if self.boundary_warning:
            result += f"\n⚠️ {self.boundary_warning}"
        return result
```

输出示例：

```
⚠️ **外推估计**：16.5-19.2 MPa（medium 置信度，基于 4 个相近样本）
⚠️ 此预测超出数据覆盖范围（2.0-6.8 wt% 外推至 0.6-9.2 wt%），仅供参考
```

## 4.5 文献冲突解决机制

### 4.5.1 冲突类型分类

多文献综合面临的一个关键挑战是不同研究之间可能存在数据冲突。本研究识别了三类主要冲突：

**1. 数值差异型冲突**

同一类型官能化在不同文献中报道的性能数值存在差异。例如：
- 文献 A：羟基官能化（3.5 wt%）拉伸强度 18.5 MPa
- 文献 B：羟基官能化（3.8 wt%）拉伸强度 15.2 MPa

**2. 趋势矛盾型冲突**

不同文献对同一变量关系的描述存在矛盾：
- 文献 A：官能化程度增加导致 Tg 升高
- 文献 B：官能化程度增加导致 Tg 降低

**3. 条件依赖型差异**

由于实验条件不同导致的结果差异（非真正冲突）：
- 不同的聚合方法（溶液法 vs 乳液法）
- 不同的填料体系（白炭黑 vs 炭黑）
- 不同的硫化配方

### 4.5.2 加权融合策略

对于数值差异型冲突，系统采用加权融合策略：

**文献质量权重**

基于样本质量分数分配权重：

$$
w_i^{quality} = \frac{q_i}{\sum_{j=1}^{n} q_j}
$$

其中 $q_i$ 为样本 $i$ 的质量分数。

**实验条件相似度权重**

根据查询条件与样本实验条件的匹配程度调整权重：

$$
w_i^{condition} = \text{sim}(\text{query}, \text{condition}_i)
$$

**时间衰减因子**

较新的研究通常采用更先进的测试方法，赋予更高权重：

$$
w_i^{time} = \exp\left(-\alpha \cdot (y_{current} - y_i)\right)
$$

**综合权重计算**

$$
w_i = w_i^{quality} \cdot w_i^{condition} \cdot w_i^{time}
$$

### 4.5.3 冲突标注与透明化

当检测到冲突时，系统向用户明确报告，确保透明性：

```python
def check_zero_hallucination(self, answer_text, samples):
    """检查回答是否存在幻觉（零幻觉原则）"""
    warnings = []
    
    # 提取回答中的数值
    numeric_pattern = r'(\d+\.?\d*)\s*(MPa|%|°C|wt%)'
    matches = re.findall(numeric_pattern, answer_text)
    
    # 构建样本中的已知数值集合
    known_values = set()
    for sample in samples:
        if sample.tensile_strength:
            known_values.add(self._normalize_value(sample.tensile_strength))
        # ... 其他字段
    
    # 检查每个数值是否有来源
    for value, unit in matches:
        normalized = self._normalize_value(value)
        if normalized not in known_values:
            if not any(abs(normalized - kv) < 0.5 for kv in known_values):
                warnings.append(f"数值 {value} {unit} 可能缺少文献来源")
    
    return warnings
```

冲突报告示例：

```markdown
⚠️ **数据差异提示**：
不同文献对羟基官能化拉伸强度的报道存在差异（15.2-18.5 MPa），
可能与实验条件（聚合方法、填料配比）有关。
以下为各文献原始数据：
- Zhang 等人 (2023): 18.5 MPa（溶液法）
- Li 等人 (2024): 15.2 MPa（乳液法）
```

## 4.6 对比分析与表格生成

### 4.6.1 方案聚合

对比分析模式用于并列展示多个官能化方案的性能差异。`ComparisonTableGenerator` 实现了结构化对比表格的自动生成。

**方案识别**

系统通过查询解析识别要对比的方案：

```bash
python scripts/qa_engine.py --compare "羟基官能化" "氨基官能化"
```

对于每个方案，检索属于该类别的样本并聚合数据。

### 4.6.2 对比维度自动选择

系统根据数据可用性自动选择 5-7 个最相关的对比维度：

```python
# 标准对比维度定义（按优先级排序）
STANDARD_DIMENSIONS = [
    ComparisonDimension("拉伸强度", "MPa", True),      # 力学性能
    ComparisonDimension("断裂伸长率", "%", True),
    ComparisonDimension("Tg", "°C", False),            # 热学性能
    ComparisonDimension("tan δ (0°C)", "-", True),     # 动态性能
    ComparisonDimension("tan δ (60°C)", "-", False),
    ComparisonDimension("Payne 效应", "-", False),
    ComparisonDimension("官能化程度", "wt%", None),
]
```

选择算法统计每个维度在所有方案中的数据可用率，优先选择覆盖率高的维度：

```python
def _select_dimensions(self, samples_by_scheme):
    """自动选择最相关的对比维度"""
    dimension_coverage = {}
    all_samples = []
    for samples in samples_by_scheme.values():
        all_samples.extend(samples)
    
    for dim in STANDARD_DIMENSIONS:
        # 统计有值的样本数
        count = sum(1 for s in all_samples 
                    if getattr(s, field, None) is not None)
        coverage = count / len(all_samples)
        dimension_coverage[dim.name] = (dim, coverage)
    
    # 按覆盖率排序，选择 5-7 个
    sorted_dims = sorted(dimension_coverage.items(), 
                         key=lambda x: x[1][1], reverse=True)
    return [dim for name, (dim, cov) in sorted_dims[:7] if cov > 0]
```

### 4.6.3 缺失数据处理

对于数据不完整的情况，系统采用"显式标注"策略而非插值或估计：

```python
def _create_entry(self, scheme_name, samples, dimensions):
    """创建对比条目，缺失数据标注为 None"""
    values = {}
    for dim in dimensions:
        dim_values = [getattr(s, field, None) for s in samples
                      if getattr(s, field, None) is not None]
        
        if dim_values:
            values[dim.name] = self._format_value(dim_values[0], dim.unit)
        else:
            values[dim.name] = None  # 显式标记缺失
    
    return ComparisonEntry(scheme_name, sample_ids, values)
```

### 4.6.4 Markdown 表格输出

生成的对比表格以 Markdown 格式输出，便于在文档和 UI 中渲染：

```python
def to_markdown(self) -> str:
    """生成 Markdown 格式表格"""
    header = "| 方案 | " + " | ".join(d.name for d in self.dimensions) + " |"
    separator = "|---" + "|---" * len(self.dimensions) + "|"
    
    rows = []
    for entry in self.entries:
        values = []
        for dim in self.dimensions:
            v = entry.values.get(dim.name)
            values.append(v if v else "数据不足")
        rows.append(f"| {entry.scheme_name} | " + " | ".join(values) + " |")
    
    return "\n".join([header, separator] + rows + ["", self.summary])
```

输出示例：

| 方案 | 拉伸强度 | 断裂伸长率 | Tg | tan δ (0°C) | Payne 效应 |
|------|----------|------------|-----|-------------|------------|
| 羟基官能化 | 18.5 MPa | 450% | -28°C | 0.42 | 0.85 |
| 氨基官能化 | 16.2 MPa | 520% | -25°C | 数据不足 | 0.72 |

羟基官能化在拉伸强度/Payne效应方面表现更优；氨基官能化在断裂伸长率方面表现更优。

## 4.7 配方设计推荐

### 4.7.1 多目标优化策略

配方设计是综合推理的高阶应用，根据用户指定的目标性能生成配方建议。`FormulaDesigner` 类实现了这一功能。

**目标解析**

用户可通过多种方式指定目标：

```bash
# 定性目标
python scripts/qa_engine.py --design "高湿地抓地力低滚阻"

# 定量目标
python scripts/qa_engine.py --design "高性能胎面" \
    --target 湿地抓地力=高 滚动阻力=低 拉伸强度=18MPa
```

**最佳匹配搜索**

系统在已有样本中搜索最接近目标的方案：

```python
def _find_best_match(self, target_properties, samples):
    """找到最匹配目标的样本"""
    best_score = 0
    best_sample = None
    
    for sample in samples:
        score = 0
        for prop, target in target_properties.items():
            sample_value = self._get_sample_property(sample, prop)
            if sample_value and self._matches_target(sample_value, target):
                score += 1
        
        if score > best_score:
            best_score = score
            best_sample = sample
    
    return best_sample if best_score > 0 else None
```

### 4.7.2 冲突目标的平衡处理

材料性能之间存在固有的权衡关系，某些目标组合是相互冲突的：

```python
# 已知的性能冲突对
KNOWN_CONFLICTS = [
    ("拉伸强度", "断裂伸长率", "高强度通常伴随低伸长率"),
    ("湿地抓地力", "滚动阻力", "两者难以同时最优，需要平衡"),
    ("硬度", "弹性", "硬度增加通常降低弹性"),
]
```

当检测到冲突目标时，系统：

1. **提示冲突存在**：向用户说明权衡关系
2. **建议折中方案**：推荐能够平衡各目标的配方
3. **标注取舍**：明确说明选择某方案时可能牺牲的性能

### 4.7.3 配方推荐输出

`FormulaRecommendation` 数据类封装完整的配方建议：

```python
@dataclass
class FormulaRecommendation:
    target_properties: Dict[str, str]   # 目标性能
    
    # 推荐配方
    recommended_functional_group: str   # 推荐官能团
    recommended_degree: str             # 推荐官能化程度
    recommended_filler: Optional[str]   # 推荐填料体系
    
    # 预期性能
    expected_performance: Dict[str, str]
    
    # 设计理由
    rationale: List[str]                # 每个参数的选择理由
    supporting_samples: List[str]       # 支撑样本 ID 列表
    
    # 风险提示
    trade_offs: List[str]               # 性能取舍说明
    warnings: List[str]                 # 安全/环保警示
    
    confidence: ConfidenceTag
```

输出示例：

```markdown
## 配方推荐

**目标**：高湿地抓地力、低滚动阻力

### 推荐配方
- **官能团**：羟基 (-OH)
- **官能化程度**：3-5 wt%
- **填料体系**：白炭黑/偶联剂体系

### 预期性能
- 拉伸强度：约 17.5 MPa
- Tg：约 -28°C

### 设计理由
1. 推荐羟基官能化：该官能团在已有研究中表现出良好的综合性能
2. 推荐官能化程度 3-5 wt%：基于 8 个相关样本的数据分析，
   该范围可实现目标性能的平衡
3. 建议使用白炭黑/偶联剂体系：可改善填料分散和界面相容性

### ⚠️ 性能权衡
- 湿地抓地力与滚动阻力存在权衡：两者难以同时最优，需要平衡

### 文献支撑
- Zhang 等人 (2023), DOI: 10.1016/j.polymer.2023.001
- Li 等人 (2024), DOI: 10.1039/c9py00234k

**置信度**：MEDIUM（基于 8 个相关样本）
```

## 4.8 引用验证与零幻觉保障

### 4.8.1 引用转换机制

为遵循"零幻觉"原则（所有数值必须来自文献），系统实现了严格的引用验证机制。`CitationValidator` 类负责：

1. **内部引用到自然语言的转换**：将 LLM 输出中的"方案 1"、"方案 2"转换为"Zhang 等人 (2023)"格式
2. **引用有效性验证**：确保每个引用指向真实存在的样本
3. **数值来源检查**：验证回答中的数值在源样本中有对应记录

**引用转换流程**

```python
def validate_and_convert(self, answer_text, samples):
    """验证并转换回答中的引用"""
    self.register_samples(samples)
    converted_text = answer_text
    
    # 匹配"方案 X"模式
    pattern = r'方案\s*(\d+)'
    matches = list(re.finditer(pattern, answer_text))
    
    # 从后向前替换，避免位置偏移
    for match in reversed(matches):
        scheme_num = int(match.group(1))
        if scheme_num <= len(samples):
            sample = samples[scheme_num - 1]
            inline_ref = self._generate_inline_ref(sample, scheme_num)
            converted_text = (
                converted_text[:match.start()] +
                inline_ref +
                converted_text[match.end():]
            )
    
    return converted_text, validated_citations
```

### 4.8.2 幻觉检测

系统对 LLM 生成的回答进行事后检查，识别潜在的幻觉内容：

```python
def check_zero_hallucination(self, answer_text, samples):
    """检查回答是否存在幻觉"""
    warnings = []
    
    # 提取回答中的数值
    numeric_pattern = r'(\d+\.?\d*)\s*(MPa|%|°C|wt%)'
    matches = re.findall(numeric_pattern, answer_text)
    
    # 构建已知数值集合
    known_values = set()
    for sample in samples:
        # 收集样本中的所有数值
        ...
    
    # 检查每个数值是否有来源
    for value, unit in matches:
        if value not in known_values:
            warnings.append(f"数值 {value} {unit} 可能缺少文献来源")
    
    return warnings
```

当检测到潜在幻觉时，系统不会阻止回答生成，而是向用户发出警告，由用户判断是否采信。

### 4.8.3 参考文献列表生成

每个综合回答附带完整的参考文献列表：

```python
def generate_reference_list(self, citations):
    """生成参考文献列表"""
    lines = ["## 文献来源", ""]
    for citation in citations:
        if citation.is_valid:
            lines.append(f"{citation.citation_id}. {citation.full_ref}")
    return "\n".join(lines)
```

## 4.9 本章小结

本章详细介绍了从单样本检索升级为多文献综合推理的方法论创新：

1. **范式升级**：定义了四种综合模式（单样本、综合分析、对比分析、配方设计），满足不同复杂度的用户需求

2. **样本聚合**：实现了语义筛选、质量过滤、多样性约束相结合的样本选取策略，并自动提取结构化摘要

3. **趋势分析**：设计了基于相邻点变化统计的定性趋势识别算法，支持官能化程度与多种性能指标的关系建模

4. **CEBC 策略**：提出上下文外推边界控制策略，通过 50% 边界规则和指数衰减置信度模型，在支持有限外推的同时防止数值幻觉

5. **冲突解决**：分类识别三种冲突类型，采用加权融合与透明标注相结合的策略处理文献间差异

6. **对比分析**：实现自动维度选择和缺失数据处理，生成结构化 Markdown 对比表格

7. **配方设计**：支持多目标输入和冲突目标平衡，基于已有数据生成配方推荐

8. **零幻觉保障**：通过引用验证和数值来源检查，确保综合结论的可追溯性

这些方法的组合使系统能够在保持数据严谨性的前提下，为用户提供超越简单检索的知识服务。下一章将介绍数据集构建和实验评测的具体细节。
