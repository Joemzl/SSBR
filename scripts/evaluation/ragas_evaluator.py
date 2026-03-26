"""
RAGAS Evaluator for SSBR QA System

使用 RAGAS 框架评估问答系统性能，重点评估：
1. Faithfulness（忠实度）：回答是否忠实于检索到的上下文
2. Answer Relevancy（相关性）：回答与问题的相关性
3. Context Precision（上下文精度）：检索结果的排序质量
4. Context Recall（上下文召回）：检索覆盖度
5. Answer Correctness（正确性）：需要 ground truth

针对综合分析模块的额外指标：
6. Citation Accuracy（引用准确性）：引用是否可追溯
7. Recommendation Quality（推荐质量）：推荐卡片的完整性和合理性

Usage:
    python scripts/evaluation/ragas_evaluator.py --mode single    # 评测单样本问答
    python scripts/evaluation/ragas_evaluator.py --mode synthesis  # 评测综合分析
    python scripts/evaluation/ragas_evaluator.py --mode all        # 全部评测
    python scripts/evaluation/ragas_evaluator.py --export csv      # 导出结果
    python scripts/evaluation/ragas_evaluator.py --quick-test      # 快速测试（1个样本）
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class EvalSample:
    """评测样本数据结构"""
    question: str                          # 测试问题
    ground_truth: Optional[str] = None     # 标准答案（可选）
    ground_truth_context: List[str] = field(default_factory=list)  # 标准上下文
    expected_samples: List[str] = field(default_factory=list)      # 期望检索到的样本
    category: str = ""                     # 问题类别
    difficulty: str = "medium"             # 难度：easy/medium/hard


@dataclass 
class EvalResult:
    """单个样本的评测结果"""
    question: str
    answer: str
    contexts: List[str]
    
    # RAGAS 核心指标
    faithfulness: Optional[float] = None
    answer_relevancy: Optional[float] = None
    context_precision: Optional[float] = None
    context_recall: Optional[float] = None
    answer_correctness: Optional[float] = None
    
    # 自定义指标（综合分析专用）
    citation_accuracy: Optional[float] = None
    recommendation_completeness: Optional[float] = None
    
    # 元数据
    response_time_ms: int = 0
    sample_count: int = 0
    mode: str = "single"


@dataclass
class EvalReport:
    """评测报告"""
    timestamp: str
    mode: str
    total_samples: int
    results: List[EvalResult]
    
    # 聚合指标
    avg_faithfulness: float = 0.0
    avg_answer_relevancy: float = 0.0
    avg_context_precision: float = 0.0
    avg_context_recall: float = 0.0
    avg_answer_correctness: float = 0.0
    avg_citation_accuracy: float = 0.0
    avg_recommendation_completeness: float = 0.0
    avg_response_time_ms: float = 0.0


# =============================================================================
# Test Dataset
# =============================================================================

# 综合分析测试集 - 需要更复杂的问题和多样本答案
SYNTHESIS_TEST_SAMPLES = [
    EvalSample(
        question="如何通过官能化改善白炭黑分散性？",
        ground_truth="通过引入极性官能团（如羟基、羧基）或硅烷偶联剂，可以增强 SSBR 与白炭黑表面的相互作用，从而改善分散性。羟基和羧基可通过氢键与白炭黑表面的硅羟基相互作用，硅烷偶联剂则可形成共价结合。推荐官能化程度在 2.5-5 wt% 范围内。",
        ground_truth_context=[
            "羟基官能化 SSBR 与白炭黑形成氢键相互作用",
            "羧基官能化可改善填料分散性",
            "硅烷偶联剂实现橡胶-填料共价结合"
        ],
        expected_samples=["SSBR-002", "SSBR-003", "SSBR-004", "SSBR-008"],
        category="分散性",
        difficulty="medium"
    ),
    EvalSample(
        question="官能化程度如何影响 Payne 效应？最佳官能化程度是多少？",
        ground_truth="官能化程度的增加通常会降低 Payne 效应（ΔG'），因为官能团改善了填料-橡胶界面结合，减少了填料-填料网络的形成。但过高的官能化程度可能导致交联密度过高。根据数据，4-5 wt% 的羧基官能化程度是最佳范围，可实现 Payne 效应活化能 14-18 kJ/mol。",
        ground_truth_context=[
            "SSBR-008 (9.6% 羧基) Payne 活化能 17.7 kJ/mol",
            "SSBR-007 (4.2% 羧基) Payne 活化能 14.2 kJ/mol",
            "SSBR-006 (2.4% 羧基) Payne 活化能 12.8 kJ/mol"
        ],
        expected_samples=["SSBR-006", "SSBR-007", "SSBR-008"],
        category="Payne效应",
        difficulty="hard"
    ),
    EvalSample(
        question="羟基官能化和羧基官能化哪个更适合改善力学性能？",
        ground_truth="根据数据对比，硅烷偶联改性的力学性能最优（拉伸强度 21.5 MPa），其次是羧基官能化（约 19 MPa），羟基官能化的拉伸强度相对较低（17.5 MPa），但断裂伸长率最高（475%）。如果追求高强度，建议使用硅烷偶联或羧基官能化；如果追求延展性，建议羟基官能化。",
        expected_samples=["SSBR-002", "SSBR-003", "SSBR-004"],
        category="力学性能",
        difficulty="medium"
    ),
    EvalSample(
        question="如何设计一个同时具有高湿地抓地力和低滚动阻力的 SSBR 配方？",
        ground_truth="实现高湿地抓地力（高 tan δ at 0°C）和低滚动阻力（低 tan δ at 60°C）的关键是优化官能化类型和程度。推荐使用羧基官能化，程度在 4-5 wt%。SSBR-016（4.29% 羧基）表现最优：tan δ(0°C)=0.9059, tan δ(60°C)=0.0734。",
        expected_samples=["SSBR-015", "SSBR-016", "SSBR-017"],
        category="动态性能",
        difficulty="hard"
    ),
    EvalSample(
        question="不同文献中羧基官能化 SSBR 的性能有什么共性和差异？",
        ground_truth="多篇文献均报道羧基官能化可改善 SSBR 与白炭黑的相容性。共性：官能化程度增加通常改善分散性和界面结合。差异：不同文献使用的官能化方法（活性阴离子聚合 vs 后改性）和测试条件不同，导致绝对数值有差异。Qu_2014 系列样本侧重 Payne 效应，Wang_2018 系列侧重动态力学性能。",
        expected_samples=["SSBR-003", "SSBR-006", "SSBR-007", "SSBR-008", "SSBR-014", "SSBR-015", "SSBR-016", "SSBR-017"],
        category="综合",
        difficulty="hard"
    ),
]

# 单样本问答测试集 - 较简单的直接问题
SINGLE_TEST_SAMPLES = [
    EvalSample(
        question="SSBR-004 的拉伸强度是多少？",
        ground_truth="SSBR-004 的拉伸强度为 21.5 MPa。",
        expected_samples=["SSBR-004"],
        category="力学性能",
        difficulty="easy"
    ),
    EvalSample(
        question="哪个样本的 tan δ(0°C) 最高？",
        ground_truth="SSBR-016 的 tan δ(0°C) 最高，为 0.9059。",
        expected_samples=["SSBR-016"],
        category="动态性能",
        difficulty="easy"
    ),
    EvalSample(
        question="羟基官能化 SSBR 的断裂伸长率是多少？",
        ground_truth="SSBR-002（羟基官能化）的断裂伸长率为 475%。",
        expected_samples=["SSBR-002"],
        category="力学性能",
        difficulty="easy"
    ),
]


# =============================================================================
# RAGAS Integration
# =============================================================================

class RAGASEvaluator:
    """
    RAGAS 评测器
    
    集成 RAGAS 框架评估 SSBR 问答系统
    """
    
    def __init__(self, use_local_llm: bool = False):
        """
        初始化评测器
        
        Args:
            use_local_llm: 是否使用本地 LLM（否则使用 OpenAI）
        """
        self.use_local_llm = use_local_llm
        self._qa_engine = None
        self._ragas_llm = None
        self._ragas_embeddings = None
        self._ragas_available = self._check_ragas()
        if self._ragas_available:
            self._setup_ragas_llm()
        
    def _check_ragas(self) -> bool:
        """检查 RAGAS 是否已安装"""
        try:
            import ragas
            logger.info(f"RAGAS version: {ragas.__version__}")
            return True
        except ImportError:
            logger.warning("RAGAS 未安装，请运行: pip install ragas")
            return False
    
    def _setup_ragas_llm(self):
        """配置 RAGAS 使用的 LLM 和 Embedding"""
        try:
            # 获取 API 配置
            api_key = os.environ.get("OPENAI_API_KEY", "")
            api_base = os.environ.get("OPENAI_API_BASE", "https://sg.uiuiapi.com/v1")
            
            # 如果没有 API Key，使用备用评估
            if not api_key:
                logger.warning("OPENAI_API_KEY 未设置，将使用规则评估方法（不需要 API）")
                self._ragas_available = False  # 强制使用备用方法
                return False
            
            from ragas.llms import LangchainLLMWrapper
            from ragas.embeddings import LangchainEmbeddingsWrapper
            from langchain_openai import ChatOpenAI, OpenAIEmbeddings
            
            # 配置 LLM
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=api_key,
                base_url=api_base,
                temperature=0
            )
            
            # 配置 Embedding
            embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=api_key,
                base_url=api_base
            )
            
            self._ragas_llm = LangchainLLMWrapper(llm)
            self._ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)
            logger.info("RAGAS LLM/Embedding 配置完成")
            return True
            
        except ImportError as e:
            logger.warning(f"无法配置 RAGAS LLM: {e}")
            logger.warning("尝试使用默认配置...")
            self._ragas_llm = None
            self._ragas_embeddings = None
            return False
        except Exception as e:
            logger.error(f"RAGAS LLM 配置失败: {e}")
            self._ragas_llm = None
            self._ragas_embeddings = None
            return False
    
    @property
    def qa_engine(self):
        """延迟加载 QA Engine（禁用 reranker 以避免网络问题）"""
        if self._qa_engine is None:
            from qa_engine import QAEngine, QAEngineConfig
            # 禁用 reranker，避免 HuggingFace 网络问题
            config = QAEngineConfig(enable_rerank=False)
            self._qa_engine = QAEngine(config=config)
            logger.info("QAEngine 已加载（reranker 已禁用）")
        return self._qa_engine
    
    def prepare_ragas_dataset(
        self, 
        test_samples: List[EvalSample],
        mode: str = "synthesis"
    ) -> List[Dict[str, Any]]:
        """
        将测试样本转换为 RAGAS 数据集格式
        
        RAGAS 数据集格式:
        {
            "question": str,
            "answer": str,           # 系统生成的答案
            "contexts": List[str],   # 检索到的上下文
            "ground_truth": str      # 标准答案（可选）
        }
        """
        dataset = []
        
        for sample in test_samples:
            logger.info(f"处理测试样本: {sample.question[:50]}...")
            
            try:
                if mode == "synthesis":
                    # 使用综合分析模式
                    response = self.qa_engine.synthesize(
                        query=sample.question,
                        top_k=5,
                        min_samples=3,
                        enable_trend=True,
                        enable_extrapolation=False  # 评测时关闭外推
                    )
                    answer = response.answer.answer_text
                    # SampleSummary 没有 key_findings，使用 to_dict() 转为字符串
                    contexts = [
                        f"样本 {s.sample_id}: {s.functional_group} 官能化 ({s.functionalization_degree}), "
                        f"拉伸强度={s.tensile_strength}, Payne效应={s.payne_effect}"
                        for s in response.answer.source_samples
                    ]
                    response_time = response.total_time_ms
                    sample_count = response.sample_count
                else:
                    # 使用单样本问答模式
                    response = self.qa_engine.answer(sample.question, top_k=3)
                    answer = response.answer.answer_text
                    contexts = [r.content[:500] for r in response.search_results[:3]]
                    response_time = response.retrieval_time_ms + response.generation_time_ms
                    sample_count = len(response.search_results)
                
                dataset.append({
                    "question": sample.question,
                    "answer": answer,
                    "contexts": contexts,
                    "ground_truth": sample.ground_truth,
                    "ground_truth_context": sample.ground_truth_context,
                    "expected_samples": sample.expected_samples,
                    "category": sample.category,
                    "response_time_ms": response_time,
                    "sample_count": sample_count,
                    "mode": mode
                })
                
            except Exception as e:
                logger.error(f"处理样本失败: {e}")
                dataset.append({
                    "question": sample.question,
                    "answer": f"Error: {str(e)}",
                    "contexts": [],
                    "ground_truth": sample.ground_truth,
                    "error": str(e)
                })
        
        return dataset
    
    async def evaluate_with_ragas(
        self, 
        dataset: List[Dict[str, Any]]
    ) -> List[EvalResult]:
        """
        使用 RAGAS 评估数据集
        
        Returns:
            评测结果列表
        """
        if not self._ragas_available:
            logger.warning("RAGAS 不可用，使用备用评估方法")
            return self._fallback_evaluate(dataset)
        
        try:
            from ragas import evaluate
            # RAGAS 0.4.x 使用新的导入路径
            try:
                from ragas.metrics._faithfulness import Faithfulness
                from ragas.metrics._answer_relevance import ResponseRelevancy
                from ragas.metrics._context_precision import ContextPrecision
                from ragas.metrics._context_recall import ContextRecall
                
                metrics = [
                    Faithfulness(),
                    ResponseRelevancy(),
                    ContextPrecision(),
                ]
                # 如果有 ground_truth，添加 context_recall
                if any(d.get("ground_truth") for d in dataset):
                    metrics.append(ContextRecall())
                    
            except ImportError:
                # 尝试旧版导入
                from ragas.metrics import (
                    faithfulness,
                    answer_relevancy,
                    context_precision,
                    context_recall,
                )
                metrics = [faithfulness, answer_relevancy, context_precision]
                if any(d.get("ground_truth") for d in dataset):
                    metrics.append(context_recall)
            
            from ragas import EvaluationDataset, SingleTurnSample
            
            # RAGAS 0.4.x 使用 EvaluationDataset
            samples = []
            for d in dataset:
                sample = SingleTurnSample(
                    user_input=d["question"],
                    response=d["answer"],
                    retrieved_contexts=d["contexts"] if d["contexts"] else ["无检索结果"],
                    reference=d.get("ground_truth", "") or "无标准答案"
                )
                samples.append(sample)
            
            eval_dataset = EvaluationDataset(samples=samples)
            
            # 运行评估 - 传入配置的 LLM 和 Embedding
            logger.info(f"开始 RAGAS 评估，共 {len(dataset)} 个样本...")
            
            eval_kwargs = {"dataset": eval_dataset, "metrics": metrics}
            if self._ragas_llm:
                eval_kwargs["llm"] = self._ragas_llm
            if self._ragas_embeddings:
                eval_kwargs["embeddings"] = self._ragas_embeddings
            
            result = evaluate(**eval_kwargs)
            
            # 转换结果
            eval_results = []
            result_df = result.to_pandas()
            
            for i, d in enumerate(dataset):
                row = result_df.iloc[i] if i < len(result_df) else {}
                
                eval_result = EvalResult(
                    question=d["question"],
                    answer=d["answer"],
                    contexts=d["contexts"],
                    faithfulness=row.get("faithfulness") if "faithfulness" in row else None,
                    answer_relevancy=row.get("response_relevancy") or row.get("answer_relevancy"),
                    context_precision=row.get("context_precision"),
                    context_recall=row.get("context_recall"),
                    response_time_ms=d.get("response_time_ms", 0),
                    sample_count=d.get("sample_count", 0),
                    mode=d.get("mode", "single")
                )
                
                # 添加自定义指标
                eval_result.citation_accuracy = self._evaluate_citation_accuracy(d)
                eval_result.recommendation_completeness = self._evaluate_recommendation(d)
                
                eval_results.append(eval_result)
            
            return eval_results
            
        except Exception as e:
            logger.error(f"RAGAS 评估失败: {e}")
            import traceback
            traceback.print_exc()
            return self._fallback_evaluate(dataset)
    
    def _fallback_evaluate(self, dataset: List[Dict[str, Any]]) -> List[EvalResult]:
        """
        备用评估方法（当 RAGAS 不可用时）
        
        使用简单的规则评估
        """
        logger.info("使用备用评估方法...")
        results = []
        
        for d in dataset:
            # 简单的相关性评分：检查答案是否包含问题中的关键词
            question_keywords = set(d["question"].replace("？", "").replace("?", "").split())
            answer_lower = d["answer"].lower()
            
            keyword_hits = sum(1 for kw in question_keywords if kw in answer_lower)
            answer_relevancy = min(keyword_hits / max(len(question_keywords), 1), 1.0)
            
            # 上下文精度：检查上下文是否非空
            context_precision = 1.0 if d["contexts"] else 0.0
            
            # 忠实度：简化为检查答案长度合理性
            answer_len = len(d["answer"])
            faithfulness = 1.0 if 100 < answer_len < 2000 else 0.5
            
            results.append(EvalResult(
                question=d["question"],
                answer=d["answer"],
                contexts=d["contexts"],
                faithfulness=faithfulness,
                answer_relevancy=answer_relevancy,
                context_precision=context_precision,
                citation_accuracy=self._evaluate_citation_accuracy(d),
                recommendation_completeness=self._evaluate_recommendation(d),
                response_time_ms=d.get("response_time_ms", 0),
                sample_count=d.get("sample_count", 0),
                mode=d.get("mode", "single")
            ))
        
        return results
    
    def _evaluate_citation_accuracy(self, data: Dict[str, Any]) -> float:
        """
        评估引用准确性（自定义指标）
        
        检查答案中的引用是否可追溯到上下文
        """
        import re
        
        answer = data.get("answer", "")
        contexts = data.get("contexts", [])
        
        # 提取引用模式：方案 X、SSBR-XXX 等
        citation_patterns = [
            r"方案\s*\d+",
            r"SSBR-\d+",
            r"\[\d+\]",
        ]
        
        citations = []
        for pattern in citation_patterns:
            citations.extend(re.findall(pattern, answer))
        
        if not citations:
            return 1.0  # 无引用不扣分
        
        # 简化检查：引用数量合理性
        expected_samples = data.get("expected_samples", [])
        if expected_samples:
            # 检查是否引用了期望的样本
            hit_count = sum(1 for s in expected_samples if s in answer or f"方案" in answer)
            return min(hit_count / len(expected_samples), 1.0)
        
        return 0.8  # 默认给予较高分数
    
    def _evaluate_recommendation(self, data: Dict[str, Any]) -> float:
        """
        评估推荐卡片完整性（综合分析专用指标）
        
        检查推荐卡片是否包含所有必填字段
        """
        answer = data.get("answer", "")
        
        # 推荐卡片必填字段关键词
        required_fields = [
            ("官能团", ["推荐官能团", "官能团"]),
            ("试剂", ["推荐试剂", "官能化试剂"]),
            ("程度", ["官能化程度", "推荐官能化程度", "wt%"]),
            ("效果", ["预期改善效果", "预期效果", "改善"]),
        ]
        
        score = 0.0
        for field_name, keywords in required_fields:
            if any(kw in answer for kw in keywords):
                score += 0.25
        
        return score
    
    def generate_report(
        self, 
        results: List[EvalResult], 
        mode: str
    ) -> EvalReport:
        """生成评测报告"""
        
        def safe_avg(values):
            valid = [v for v in values if v is not None]
            return sum(valid) / len(valid) if valid else 0.0
        
        report = EvalReport(
            timestamp=datetime.now().isoformat(),
            mode=mode,
            total_samples=len(results),
            results=results,
            avg_faithfulness=safe_avg([r.faithfulness for r in results]),
            avg_answer_relevancy=safe_avg([r.answer_relevancy for r in results]),
            avg_context_precision=safe_avg([r.context_precision for r in results]),
            avg_context_recall=safe_avg([r.context_recall for r in results]),
            avg_answer_correctness=safe_avg([r.answer_correctness for r in results]),
            avg_citation_accuracy=safe_avg([r.citation_accuracy for r in results]),
            avg_recommendation_completeness=safe_avg([r.recommendation_completeness for r in results]),
            avg_response_time_ms=safe_avg([r.response_time_ms for r in results]),
        )
        
        return report
    
    def export_report_markdown(self, report: EvalReport, output_path: str):
        """导出 Markdown 格式报告"""
        
        content = f"""# RAGAS 评测报告

**生成时间**: {report.timestamp}  
**评测模式**: {report.mode}  
**样本数量**: {report.total_samples}

---

## 1. 总体指标

| 指标 | 数值 | 说明 |
|------|------|------|
| **Faithfulness（忠实度）** | {report.avg_faithfulness:.3f} | 回答是否忠实于上下文 |
| **Answer Relevancy（相关性）** | {report.avg_answer_relevancy:.3f} | 回答与问题的相关性 |
| **Context Precision（上下文精度）** | {report.avg_context_precision:.3f} | 检索结果排序质量 |
| **Context Recall（上下文召回）** | {report.avg_context_recall:.3f} | 检索覆盖度 |
| **Citation Accuracy（引用准确性）** | {report.avg_citation_accuracy:.3f} | 引用可追溯性 |
| **Recommendation Completeness** | {report.avg_recommendation_completeness:.3f} | 推荐卡片完整性 |
| **平均响应时间** | {report.avg_response_time_ms:.0f} ms | 系统响应速度 |

---

## 2. 详细结果

"""
        for i, r in enumerate(report.results, 1):
            question_preview = r.question[:50] if len(r.question) > 50 else r.question
            faithfulness_str = f"{r.faithfulness:.3f}" if r.faithfulness else "N/A"
            relevancy_str = f"{r.answer_relevancy:.3f}" if r.answer_relevancy else "N/A"
            precision_str = f"{r.context_precision:.3f}" if r.context_precision else "N/A"
            citation_str = f"{r.citation_accuracy:.3f}" if r.citation_accuracy else "N/A"
            recommendation_str = f"{r.recommendation_completeness:.3f}" if r.recommendation_completeness else "N/A"
            answer_preview = r.answer[:200] if len(r.answer) > 200 else r.answer
            
            content += f"""### 样本 {i}: {question_preview}...

- **模式**: {r.mode}
- **检索样本数**: {r.sample_count}
- **响应时间**: {r.response_time_ms} ms
- **Faithfulness**: {faithfulness_str}
- **Answer Relevancy**: {relevancy_str}
- **Context Precision**: {precision_str}
- **Citation Accuracy**: {citation_str}
- **Recommendation**: {recommendation_str}

**回答摘要**: {answer_preview}...

---

"""
        
        content += """
## 3. 评估说明

### 3.1 RAGAS 指标说明

- **Faithfulness**: 衡量回答是否基于检索到的上下文生成，值域 [0,1]
- **Answer Relevancy**: 衡量回答是否直接回答了用户问题，值域 [0,1]
- **Context Precision**: 衡量检索结果中相关文档的排序质量，值域 [0,1]
- **Context Recall**: 衡量检索到的上下文覆盖了多少真实答案所需信息，值域 [0,1]

### 3.2 自定义指标说明

- **Citation Accuracy**: 检查答案中的引用（方案 X、SSBR-XXX）是否可追溯
- **Recommendation Completeness**: 检查推荐卡片是否包含官能团、试剂、程度、效果四个必填字段

---

*本报告由 RAGAS Evaluator 自动生成*
"""
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"报告已导出: {output_path}")
    
    def export_report_csv(self, report: EvalReport, output_path: str):
        """导出 CSV 格式报告"""
        import csv
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            
            # 写入表头
            writer.writerow([
                "question", "mode", "sample_count", "response_time_ms",
                "faithfulness", "answer_relevancy", "context_precision",
                "context_recall", "citation_accuracy", "recommendation_completeness",
                "answer_preview"
            ])
            
            # 写入数据
            for r in report.results:
                writer.writerow([
                    r.question,
                    r.mode,
                    r.sample_count,
                    r.response_time_ms,
                    f"{r.faithfulness:.3f}" if r.faithfulness else "",
                    f"{r.answer_relevancy:.3f}" if r.answer_relevancy else "",
                    f"{r.context_precision:.3f}" if r.context_precision else "",
                    f"{r.context_recall:.3f}" if r.context_recall else "",
                    f"{r.citation_accuracy:.3f}" if r.citation_accuracy else "",
                    f"{r.recommendation_completeness:.3f}" if r.recommendation_completeness else "",
                    r.answer[:100]
                ])
        
        logger.info(f"CSV 已导出: {output_path}")


# =============================================================================
# Main Entry
# =============================================================================

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="RAGAS 评测 SSBR 问答系统")
    parser.add_argument(
        "--mode", 
        choices=["single", "synthesis", "all"], 
        default="synthesis",
        help="评测模式"
    )
    parser.add_argument(
        "--export", 
        choices=["md", "csv", "both"], 
        default="both",
        help="导出格式"
    )
    parser.add_argument(
        "--output-dir",
        default="evaluation/ragas_reports",
        help="输出目录"
    )
    parser.add_argument(
        "--quick-test",
        action="store_true",
        help="快速测试模式（仅运行1个样本，验证系统是否正常）"
    )
    
    args = parser.parse_args()
    
    evaluator = RAGASEvaluator()
    
    # 快速测试模式
    if args.quick_test:
        logger.info("=" * 50)
        logger.info("[Quick Test] 快速测试模式")
        logger.info("=" * 50)
        
        # 只用一个简单的测试样本
        quick_test_sample = [
            EvalSample(
                question="如何改善白炭黑分散性？",
                ground_truth="通过引入极性官能团（羟基、羧基）或硅烷偶联剂可以改善分散性。",
                expected_samples=["SSBR-002", "SSBR-004"],
                category="分散性",
                difficulty="medium"
            )
        ]
        
        print("\n[Test] 测试问题: 如何改善白炭黑分散性?")
        print("-" * 50)
        
        # 准备数据
        print("[1/3] 正在调用问答系统...")
        dataset = evaluator.prepare_ragas_dataset(quick_test_sample, mode="synthesis")
        
        if dataset and dataset[0].get("answer"):
            print(f"[OK] 问答系统响应成功")
            print(f"     - 回答长度: {len(dataset[0]['answer'])} 字符")
            print(f"     - 检索样本数: {dataset[0].get('sample_count', 'N/A')}")
            print(f"     - 响应时间: {dataset[0].get('response_time_ms', 'N/A')} ms")
            
            print("\n[2/3] 正在运行 RAGAS 评估...")
            results = await evaluator.evaluate_with_ragas(dataset)
            
            if results:
                r = results[0]
                print("\n" + "=" * 50)
                print("[3/3] 评测结果")
                print("=" * 50)
                print(f"  Faithfulness (忠实度):     {r.faithfulness:.3f}" if r.faithfulness else "  Faithfulness: N/A")
                print(f"  Answer Relevancy (相关性): {r.answer_relevancy:.3f}" if r.answer_relevancy else "  Answer Relevancy: N/A")
                print(f"  Context Precision (精度):  {r.context_precision:.3f}" if r.context_precision else "  Context Precision: N/A")
                print(f"  Citation Accuracy (引用):  {r.citation_accuracy:.3f}" if r.citation_accuracy else "  Citation Accuracy: N/A")
                print(f"  Recommendation (推荐):     {r.recommendation_completeness:.3f}" if r.recommendation_completeness else "  Recommendation: N/A")
                
                print("\n[Preview] 回答预览:")
                print("-" * 50)
                # 安全打印，避免编码问题
                try:
                    preview = r.answer[:500] + "..." if len(r.answer) > 500 else r.answer
                    print(preview)
                except UnicodeEncodeError:
                    print("[Unable to display - encoding issue]")
                print("\n[Done] 快速测试完成!")
            else:
                print("[Error] 评测返回空结果")
        else:
            print("[Error] 问答系统未能生成回答")
        
        return
    
    all_results = []
    
    if args.mode in ["synthesis", "all"]:
        logger.info("=" * 50)
        logger.info("评测综合分析模块")
        logger.info("=" * 50)
        
        dataset = evaluator.prepare_ragas_dataset(SYNTHESIS_TEST_SAMPLES, mode="synthesis")
        results = await evaluator.evaluate_with_ragas(dataset)
        all_results.extend(results)
        
        report = evaluator.generate_report(results, mode="synthesis")
        
        if args.export in ["md", "both"]:
            evaluator.export_report_markdown(
                report, 
                f"{args.output_dir}/synthesis_report.md"
            )
        if args.export in ["csv", "both"]:
            evaluator.export_report_csv(
                report,
                f"{args.output_dir}/synthesis_report.csv"
            )
    
    if args.mode in ["single", "all"]:
        logger.info("=" * 50)
        logger.info("评测单样本问答模块")
        logger.info("=" * 50)
        
        dataset = evaluator.prepare_ragas_dataset(SINGLE_TEST_SAMPLES, mode="single")
        results = await evaluator.evaluate_with_ragas(dataset)
        all_results.extend(results)
        
        report = evaluator.generate_report(results, mode="single")
        
        if args.export in ["md", "both"]:
            evaluator.export_report_markdown(
                report,
                f"{args.output_dir}/single_report.md"
            )
        if args.export in ["csv", "both"]:
            evaluator.export_report_csv(
                report,
                f"{args.output_dir}/single_report.csv"
            )
    
    # 输出总结
    print("\n" + "=" * 50)
    print("评测完成！")
    print("=" * 50)
    
    if all_results:
        avg_faithfulness = sum(r.faithfulness or 0 for r in all_results) / len(all_results)
        avg_relevancy = sum(r.answer_relevancy or 0 for r in all_results) / len(all_results)
        avg_citation = sum(r.citation_accuracy or 0 for r in all_results) / len(all_results)
        
        print(f"\n总体指标 ({len(all_results)} 个样本):")
        print(f"  Faithfulness:      {avg_faithfulness:.3f}")
        print(f"  Answer Relevancy:  {avg_relevancy:.3f}")
        print(f"  Citation Accuracy: {avg_citation:.3f}")


if __name__ == "__main__":
    asyncio.run(main())
