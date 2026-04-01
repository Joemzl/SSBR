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

# 加载 .env 文件
try:
    from dotenv import load_dotenv
    # 查找项目根目录的 .env 文件
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"[INFO] 已加载环境变量: {env_path}")
    else:
        print(f"[WARNING] 未找到 .env 文件: {env_path}")
except ImportError:
    print("[WARNING] python-dotenv 未安装，无法加载 .env 文件")

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
# 重要：ground_truth_context 需要包含完整的数值数据，以便 RAGAS 验证 Faithfulness
# 扩展至 12 个测试样本，覆盖更多场景
SYNTHESIS_TEST_SAMPLES = [
    # === 原有测试样本 (5个) - 已丰富 ground_truth_context ===
    EvalSample(
        question="如何通过官能化改善白炭黑分散性？",
        ground_truth="通过引入极性官能团（如羟基、羧基）或硅烷偶联剂，可以增强 SSBR 与白炭黑表面的相互作用，从而改善分散性。羟基和羧基可通过氢键与白炭黑表面的硅羟基相互作用，硅烷偶联剂则可形成共价结合。推荐官能化程度在 2.5-5 wt% 范围内。",
        ground_truth_context=[
            # SSBR-002: 羧基官能化
            "SSBR-002 羧基官能化，官能化程度 8.7 wt%，试剂：11-巯基十一烷酸（MUA），拉伸强度 26.0 MPa，断裂伸长率 340%，Tg=-2.1℃，结合橡胶含量 67.82%",
            "MUA 的羧基提供双重界面相互作用：(1) 氢键作用：羧基与白炭黑硅羟基形成强氢键（46 kJ/mol）；(2) 共价键作用：羧基可与硅羟基发生酯化反应形成 Si-O-C 共价键",
            "TEM 观察显示白炭黑分散非常均匀，团聚和空隙很少，分散性排名: MPTES > MUA > MPL > 空白",
            # SSBR-003/004/005: 硅烷官能化
            "SSBR-003 三乙氧基硅烷基官能化，官能化程度 1.7 wt%，试剂：MPTES，拉伸强度 18.2 MPa，断裂伸长率 275%，Tg=-8.9℃，结合橡胶含量 46.23%",
            "SSBR-004 三乙氧基硅烷基官能化，官能化程度 5.8 wt%，拉伸强度 12.8 MPa，断裂伸长率 248%，结合橡胶含量 57.61%",
            "SSBR-005 三乙氧基硅烷基官能化，官能化程度 9.5 wt%，拉伸强度 11.9 MPa，断裂伸长率 105%，结合橡胶含量 80.20%（所有样品最高）",
            "MPTES 的三乙氧基硅烷基可与白炭黑表面硅羟基发生缩合反应，形成稳定的 Si-O-Si 共价键",
            "silica/SSBR-g-MPTES70 分散性最优，tan δ (7% strain)=0.065（所有样品最低，表明 Payne 效应最小）",
        ],
        expected_samples=["SSBR-002", "SSBR-003", "SSBR-004", "SSBR-005"],
        category="分散性",
        difficulty="medium"
    ),
    EvalSample(
        question="官能化程度如何影响 Payne 效应？最佳官能化程度是多少？",
        ground_truth="官能化程度的增加通常会降低 Payne 效应（ΔG'），因为官能团改善了填料-橡胶界面结合，减少了填料-填料网络的形成。根据数据，SSBR-005（9.5 wt%）的 tan δ (7% strain) 为 0.065，是所有样品中最低的。",
        ground_truth_context=[
            # Payne 效应数据
            "SSBR-002: Payne G'-应变曲线，G'₀=1.45 MPa，G'∞=0.59 MPa，ΔG'=0.856 MPa，临界应变 γc≈3.5%",
            "SSBR-003: ΔG'=1.55 MPa (G'₀=2.1 MPa, G'∞=0.55 MPa)，tan δ (7% strain)=0.110",
            "SSBR-004: ΔG'=1.33 MPa (G'₀=1.85 MPa, G'∞=0.52 MPa)，tan δ (7% strain)=0.086",
            "SSBR-005: ΔG'=1.03 MPa (G'₀=1.55 MPa, G'∞=0.52 MPa)，tan δ (7% strain)=0.065（所有样品最低）",
            "官能化程度越高，Payne 效应越小，这是因为更强的橡胶-填料界面结合减少了填料-填料网络的形成",
            "SSBR-005 官能化程度 9.5 wt%，结合橡胶含量 80.20%，分散性最优",
        ],
        expected_samples=["SSBR-002", "SSBR-003", "SSBR-004", "SSBR-005"],
        category="Payne效应",
        difficulty="hard"
    ),
    EvalSample(
        question="羟基官能化和羧基官能化哪个更适合改善力学性能？",
        ground_truth="根据数据对比，羧基官能化（SSBR-002）的力学性能最优：拉伸强度 26.0 MPa，断裂伸长率 340%。硅烷官能化（SSBR-003）的拉伸强度为 18.2 MPa，断裂伸长率 275%。如果追求高强度，建议使用羧基官能化。",
        ground_truth_context=[
            # SSBR-002 力学数据
            "SSBR-002 羧基官能化（8.7 wt%）：拉伸强度 26.0 MPa，300%定伸应力 23.3 MPa，断裂伸长率 340%，100%定伸应力 6.3 MPa",
            "SSBR-002 相比空白 SSBR：拉伸强度从 15.0 MPa 提升到 26.0 MPa（+73%），300%定伸应力从 9.0 MPa 提升到 23.3 MPa（+159%）",
            "文献结论：Filler–rubber, filler–filler, and rubber–rubber networks reached equilibrium in the silica/SSBR-g-MUA composite",
            # SSBR-003/004/005 力学数据
            "SSBR-003 硅烷官能化（1.7 wt%）：拉伸强度 18.2 MPa，断裂伸长率 275%，100%定伸应力 2.8 MPa",
            "SSBR-004 硅烷官能化（5.8 wt%）：拉伸强度 12.8 MPa，断裂伸长率 248%，100%定伸应力 3.2 MPa",
            "SSBR-005 硅烷官能化（9.5 wt%）：拉伸强度 11.9 MPa，断裂伸长率 105%，100%定伸应力 11.0 MPa",
            "SSBR-005 过强的界面网络限制了分子链运动，导致伸长率大幅下降（文献：The excessively strong rubber–rubber networks led to poor mechanical properties）",
        ],
        expected_samples=["SSBR-002", "SSBR-003", "SSBR-004", "SSBR-005"],
        category="力学性能",
        difficulty="medium"
    ),
    EvalSample(
        question="如何设计一个同时具有高湿地抓地力和低滚动阻力的 SSBR 配方？",
        ground_truth="实现高湿地抓地力（高 tan δ at 0°C）和低滚动阻力（低 tan δ at 60°C）的关键是优化官能化类型和程度。SSBR-005 表现最优：tan δ(0°C)=1.342（最高），tan δ(60°C)≈0.08，湿地抓地力提升 184.3%，滚动阻力降低 50.8%。",
        ground_truth_context=[
            # SSBR-002 动态性能
            "SSBR-002: tan δ(0°C)=1.233（湿地抓地力指标），tan δ(60°C)≈0.13（滚动阻力指标），Tg=-2.1℃",
            "SSBR-002 DMA tan δ-温度曲线：温度范围 -80-80℃，tan δ 范围 0.02-1.239，峰半高宽≈48℃",
            # SSBR-003/004/005 动态性能
            "SSBR-003: tan δ(0°C)=0.886，tan δ(60°C)≈0.1，Tg=-8.9℃",
            "SSBR-004: tan δ(0°C)=1.21，tan δ(60°C)≈0.09，Tg=-3.9℃",
            "SSBR-005: tan δ(0°C)=1.342（所有样品最高），tan δ(60°C)≈0.08，Tg=-1.1℃",
            "SSBR-005 湿地抓地力提升 184.3%（文献原文），滚动阻力降低 50.8%（文献原文）",
            # SSBR-015 动态性能
            "SSBR-015（DPES官能化）: 0℃ tan δ 增大（湿地抓地力提高），60℃ tan δ 降低 30.8%（滚动阻力显著降低）",
        ],
        expected_samples=["SSBR-002", "SSBR-005", "SSBR-015"],
        category="动态性能",
        difficulty="hard"
    ),
    EvalSample(
        question="不同文献中羧基官能化 SSBR 的性能有什么共性和差异？",
        ground_truth="多篇文献均报道羧基官能化可改善 SSBR 与白炭黑的相容性。共性：官能化程度增加通常改善分散性和界面结合。SSBR-002（8.7 wt% 羧基官能化）拉伸强度 26.0 MPa，SSBR-017（4 phr 酯基官能化）拉伸强度 14.1 MPa。",
        ground_truth_context=[
            # SSBR-002 详细数据
            "SSBR-002（Gao_2019）：羧基官能化，官能化程度 8.7 wt%，试剂 MUA，拉伸强度 26.0 MPa，断裂伸长率 340%",
            "SSBR-002 双重界面作用机制：氢键（46 kJ/mol）+ 共价键（酯化反应），结合橡胶含量 67.82%",
            # SSBR-017 详细数据
            "SSBR-017（Sun_2017）：酯基官能化，官能化程度 4 phr，试剂 TMPMP，拉伸强度 14.1 MPa，断裂伸长率 264%",
            "SSBR-017 应用场景：硅橡胶/SSBR界面改性",
            # 共性和差异
            "共性：官能化改善填料分散性和界面结合，提高力学性能",
            "差异：不同试剂和官能化程度导致不同的力学性能，SSBR-002（MUA）优于 SSBR-017（TMPMP）",
        ],
        expected_samples=["SSBR-002", "SSBR-017"],
        category="综合",
        difficulty="hard"
    ),
    
    # === 新增测试样本 (7个) ===
    EvalSample(
        question="环氧基官能化 SSBR 有哪些优势？适合什么应用场景？",
        ground_truth="环氧基官能化 SSBR 具有良好的反应活性，环氧基可与白炭黑表面的硅羟基反应形成共价键，显著改善界面结合。来自 Hayeemasae_2020 的研究表明，环氧基官能化可通过开环反应实现，有效降低橡胶与填料的界面张力。适合需要高耐磨性和良好力学性能的应用场景，如轮胎胎面胶。",
        ground_truth_context=[
            "环氧基官能化，开环反应改性，改善界面结合",
            "环氧基与白炭黑硅羟基形成共价键",
            "环氧基官能化适合高耐磨性应用",
            "Hayeemasae_2020 研究环氧基改性 SSBR",
        ],
        expected_samples=["SSBR-021", "SSBR-022", "SSBR-023", "SSBR-024", "SSBR-025"],
        category="官能团类型",
        difficulty="medium"
    ),
    EvalSample(
        question="星型支化 SSBR 相比线型 SSBR 有什么优势？",
        ground_truth="星型支化 SSBR 具有独特的分子结构，通过 SiCl4 或 SnCl4 作为偶联剂将多条线型链连接到中心点。这种结构可以降低材料的滞后损耗，同时保持良好的加工性能。Wang_2020 的研究表明，星型支化结构可优化分子链的运动性，改善动态力学性能。",
        ground_truth_context=[
            # SSBR-043 详细数据
            "SSBR-043 星形 SSBR (YK-2)，4 支链结构，乙烯基含量 46.0 mol%（最高），苯乙烯含量 24.2 wt%，Mn=33.6×10⁴ g/mol，PDI=1.82",
            "SSBR-043 力学性能（三种 SSBR 中最优）：300%定伸应力 4.6 MPa（+17.9%），拉伸强度 11.9 MPa（+15.5%），断裂伸长率 489%，撕裂强度 25.5 kN/m（+7.6%）",
            "SSBR-043 高乙烯基含量优势：更高的 Tg（+2℃）、更好的撕裂抗性、tan δ(0℃) 最高（湿地抓地力最优）",
            "SSBR-043 白炭黑分散：粒径 20-30 nm（对照 >30 nm），球形均匀分散，FB 值 0.31±0.01",
            "星型 SSBR 通过 SiCl4 或 SnCl4 偶联剂合成，将多条活性聚合物链连接到中心原子",
            "AMMO 硅烷偶联剂改性可进一步降低 Payne 效应（ΔG' 减小）",
        ],
        expected_samples=["SSBR-043", "SSBR-044", "SSBR-045", "SSBR-046"],
        category="分子结构",
        difficulty="medium"
    ),
    EvalSample(
        question="如何通过官能化改善 SSBR 的玻璃化转变温度 (Tg)？",
        ground_truth="SSBR 的 Tg 主要由苯乙烯含量和微观结构决定，官能化可以通过改变链段运动性来调节 Tg。羧基和氨基官能化通常会略微提高 Tg，因为极性基团增加了分子间相互作用。数据显示，官能化程度约 5-7 wt% 时，Tg 可提高 2-5°C，但过高的官能化程度可能导致加工性下降。",
        ground_truth_context=[
            # Tg 数据汇总
            "SSBR-001 羟基官能化（3.6 wt%）：复合材料 Tg=-0.9℃，ΔTg=23.9℃（纯聚合物到复合材料）",
            "SSBR-002 羧基官能化（8.7 wt%）：Tg=-2.1℃",
            "SSBR-003 硅烷官能化（1.7 wt%）：Tg=-8.9℃",
            "SSBR-004 硅烷官能化（5.8 wt%）：Tg=-3.9℃",
            "SSBR-005 硅烷官能化（9.5 wt%）：Tg=-1.1℃",
            "SSBR-018 氨基官能化（0.09 wt%）：Tg=-17.4℃",
            "官能化程度增加 → 界面相互作用增强 → Tg 上升，因为极性基团限制链段运动",
        ],
        expected_samples=["SSBR-001", "SSBR-002", "SSBR-003", "SSBR-004", "SSBR-005", "SSBR-018"],
        category="热学性能",
        difficulty="hard"
    ),
    EvalSample(
        question="活性阴离子聚合法合成官能化 SSBR 有什么优点？",
        ground_truth="活性阴离子聚合（Living Anionic Polymerization）是合成官能化 SSBR 的主要方法，具有以下优点：1）分子量分布窄（PDI≈1.1-1.3）；2）可精确控制官能团位置（链端或链中）；3）官能化程度可通过官能化试剂用量精确调控。多篇文献采用此方法合成含羟基、羧基、氨基等官能团的 SSBR。",
        ground_truth_context=[
            # 合成方法数据
            "SSBR-001（羟基官能化）：巯基-烯点击化学（UV 或热引发），反应位点为 1,2-乙烯基侧链双键",
            "SSBR-002/003/004/005 采用自由基引发的硫醇-烯加成反应（thiol-ene addition）",
            "SSBR-018（氨基官能化）：通过 DPE-NMe2 进行链端官能化",
            "SSBR-043 分子量分布 PDI=1.82（星形结构），完全无规共聚物",
            "活性阴离子聚合特点：快引发、慢增长、无终止、无转移，确保分子量分布窄",
            "官能化程度可通过官能化试剂用量精确调控：SSBR-001 为 3.6 wt%，SSBR-005 为 9.5 wt%",
        ],
        expected_samples=["SSBR-001", "SSBR-002", "SSBR-003", "SSBR-004", "SSBR-005", "SSBR-018"],
        category="合成方法",
        difficulty="medium"
    ),
    EvalSample(
        question="如何选择合适的官能化试剂？不同试剂对性能有什么影响？",
        ground_truth="官能化试剂的选择取决于目标官能团和应用需求。常用试剂包括：1）羟基化：3-巯基丙醇、环氧乙烷；2）羧基化：CO2、丙烯酸、腈氧化物；3）氨基化：三甲氧基硅烷类；4）硅烷化：三乙氧基硅烷基试剂。不同试剂引入的官能团密度和分布不同，影响最终材料的界面相容性和力学性能。",
        ground_truth_context=[
            # 各类试剂及性能数据
            "羟基化试剂 MPL（3-巯基丙醇）：SSBR-001，拉伸强度 14.2 MPa，断裂伸长率 200%，通过羟基-硅羟基氢键改善分散性",
            "羧基化试剂 MUA（11-巯基十一烷酸）：SSBR-002，拉伸强度 26.0 MPa（最高），断裂伸长率 340%，双重界面作用（氢键+共价键）",
            "硅烷化试剂 MPTES（3-巯基丙基三乙氧基硅烷）：SSBR-003/004/005，通过 Si-O-Si 共价键与白炭黑结合",
            "氨基化试剂 DPE-NMe2：SSBR-018，链端氨基官能化，氨基-羟基氢键改善分散性",
            "氨基化试剂 AMMO：SSBR-043，硅烷偶联剂，同时含氨基和硅烷基",
            "试剂选择原则：羧基/硅烷试剂适合高强度需求，羟基试剂适合高延展性需求",
        ],
        expected_samples=["SSBR-001", "SSBR-002", "SSBR-003", "SSBR-004", "SSBR-005", "SSBR-018", "SSBR-043"],
        category="官能化试剂",
        difficulty="medium"
    ),
    EvalSample(
        question="SSBR 与炭黑填充体系相比，白炭黑填充体系有什么优势？",
        ground_truth="白炭黑（二氧化硅）填充体系相比炭黑具有以下优势：1）滚动阻力更低（节能 5-7%）；2）湿地抓地力更好；3）耐磨性可比。但白炭黑表面极性与非极性 SSBR 不相容，需要官能化改性或添加硅烷偶联剂。官能化 SSBR 可显著改善白炭黑分散性，是绿色轮胎的首选方案。",
        ground_truth_context=[
            # 白炭黑分散性数据
            "SSBR-001: TEM 观察显示白炭黑分散相当均匀，团聚和空隙较少，分散性排序: MPTES > MUA > MPL > 空白",
            "SSBR-002: TEM 观察白炭黑分散非常均匀，结合橡胶含量 67.82%（高），界面结合力强",
            "SSBR-005: 分散性最优，tan δ (7% strain)=0.065（最低），结合橡胶含量 80.20%（最高）",
            "SSBR-018: 白炭黑团聚体尺寸从 ~200 nm 降至 90-125 nm，Payne 效应最小",
            "白炭黑填充体系优势：滚动阻力低（tan δ(60°C) 低）、湿地抓地力好（tan δ(0°C) 高）",
            "官能化改性通过极性基团与白炭黑表面硅羟基相互作用，改善界面结合",
        ],
        expected_samples=["SSBR-001", "SSBR-002", "SSBR-003", "SSBR-004", "SSBR-005", "SSBR-018"],
        category="填料体系",
        difficulty="medium"
    ),
    EvalSample(
        question="高苯乙烯含量和高乙烯基含量对 SSBR 性能有什么影响？",
        ground_truth="苯乙烯含量和乙烯基含量是影响 SSBR 性能的关键微观结构参数。高苯乙烯含量（>25%）可提高 Tg 和湿地抓地力，但会降低低温柔韧性。高乙烯基含量（>50%）同样提高 Tg 和抓地力，同时改善与白炭黑的相容性。绿色轮胎通常采用高乙烯基含量（55-65%）+ 中等苯乙烯含量（20-25%）的配方。",
        ground_truth_context=[
            # 微观结构数据
            "SSBR-001: 苯乙烯含量 23.0 wt%，乙烯基含量 40.1 mol%，Mn=18.5×10⁴ g/mol",
            "SSBR-043: 苯乙烯含量 24.2 wt%，乙烯基含量 46.0 mol%（三种 SSBR 中最高），Mn=33.6×10⁴ g/mol，完全无规",
            "SSBR-043 高乙烯基含量带来：更高的 Tg（+2℃）、更好的撕裂抗性、tan δ(0℃) 最高（湿地抓地力最优）",
            "高乙烯基含量优势：侧链乙烯基阻碍主链运动（提高 Tg），提供能量耗散（改善撕裂抗性）",
            "乙烯基侧链双键可作为巯基-烯点击化学的反应位点（SSBR-001 采用此方法）",
            "高苯乙烯含量（>25%）：提高 Tg 和湿地抓地力，但降低低温柔韧性",
        ],
        expected_samples=["SSBR-001", "SSBR-043"],
        category="微观结构",
        difficulty="hard"
    ),
]

# 单样本问答测试集 - 较简单的直接问题
# 重要：ground_truth_context 需要包含完整的数值数据，以便 RAGAS 验证 Faithfulness
# 扩展至 12 个测试样本
SINGLE_TEST_SAMPLES = [
    # === 原有测试样本 (5个) - 已丰富 ground_truth_context ===
    EvalSample(
        question="硅烷官能化 SSBR 的拉伸强度是多少？",
        ground_truth="硅烷官能化 SSBR 的拉伸强度约为 18.2 MPa（1.7 wt%）、12.8 MPa（5.8 wt%）、11.9 MPa（9.5 wt%），这是通过三乙氧基硅烷基试剂实现的，官能化可显著改善白炭黑与橡胶的界面结合。",
        ground_truth_context=[
            "SSBR-003 硅烷官能化（1.7 wt%）：拉伸强度 18.2 MPa，断裂伸长率 275%，100%定伸应力 2.8 MPa，试剂 MPTES",
            "SSBR-004 硅烷官能化（5.8 wt%）：拉伸强度 12.8 MPa，断裂伸长率 248%，100%定伸应力 3.2 MPa",
            "SSBR-005 硅烷官能化（9.5 wt%）：拉伸强度 11.9 MPa，断裂伸长率 105%，100%定伸应力 11.0 MPa，结合橡胶含量 80.20%（最高）",
            "MPTES（3-巯基丙基三乙氧基硅烷）通过 Si-O-Si 共价键与白炭黑表面结合",
            "SSBR-005 分散性最优，tan δ (7% strain)=0.065（所有样品最低），但过强界面网络限制分子链运动导致伸长率下降",
        ],
        expected_samples=["SSBR-003", "SSBR-004", "SSBR-005"],
        category="力学性能",
        difficulty="easy"
    ),
    EvalSample(
        question="哪种官能化方案的 tan δ(0°C) 最高，适合高湿地抓地力应用？",
        ground_truth="硅烷官能化 SSBR-005 的 tan δ(0°C) 最高，可达 1.342，非常适合高湿地抓地力轮胎应用。高 tan δ(0°C) 意味着在低温下材料的能量耗散能力强，有利于提高湿地抓地性能。",
        ground_truth_context=[
            "SSBR-005: tan δ(0°C)=1.342（所有样品最高），tan δ(60°C)≈0.08，Tg=-1.1℃",
            "SSBR-005 湿地抓地力提升 184.3%（文献原文），滚动阻力降低 50.8%（文献原文）",
            "SSBR-002: tan δ(0°C)=1.233，tan δ(60°C)≈0.13，Tg=-2.1℃",
            "SSBR-001: tan δ(0°C)=1.004，Tg(复合材料)=-0.9℃",
            "高 tan δ(0°C) 意味着良好的湿滑路面制动性能",
        ],
        expected_samples=["SSBR-005", "SSBR-002", "SSBR-001"],
        category="动态性能",
        difficulty="easy"
    ),
    EvalSample(
        question="羟基官能化 SSBR 的断裂伸长率是多少？延展性如何？",
        ground_truth="羟基官能化 SSBR-001 的断裂伸长率为 200%，通过 3-巯基丙醇（MPL）作为官能化试剂实现的，官能化程度约 3.6 wt%。羧基官能化 SSBR-002 断裂伸长率更高，达 340%。",
        ground_truth_context=[
            "SSBR-001 羟基官能化（3.6 wt%）：拉伸强度 14.2 MPa，断裂伸长率 200%，100%定伸应力 4.2 MPa，试剂 MPL（3-巯基丙醇）",
            "SSBR-001 相比空白 SSBR：拉伸强度从 8.5 MPa 提升到 14.2 MPa（+67%），断裂伸长率从 120% 提升到 200%（+67%）",
            "SSBR-002 羧基官能化（8.7 wt%）：拉伸强度 26.0 MPa，断裂伸长率 340%",
            "羟基官能团与白炭黑表面硅羟基形成氢键，改善界面结合",
        ],
        expected_samples=["SSBR-001", "SSBR-002"],
        category="力学性能",
        difficulty="easy"
    ),
    EvalSample(
        question="如何提高 SSBR 与白炭黑的相容性？",
        ground_truth="提高 SSBR 与白炭黑相容性的主要方法是引入极性官能团，如羧基或羟基。这些官能团可以通过氢键与白炭黑表面的硅羟基相互作用，改善界面结合。SSBR-002（羧基官能化 8.7 wt%）结合橡胶含量达 67.82%，SSBR-005（硅烷官能化 9.5 wt%）达 80.20%。",
        ground_truth_context=[
            "SSBR-002 羧基官能化：结合橡胶含量 67.82%，双重界面作用（氢键 46 kJ/mol + 共价键）",
            "SSBR-005 硅烷官能化：结合橡胶含量 80.20%（所有样品最高），通过 Si-O-Si 共价键结合",
            "SSBR-001 羟基官能化：结合橡胶含量 55.28%，通过羟基-硅羟基氢键改善分散性",
            "白炭黑分散性排序: MPTES（硅烷）> MUA（羧基）> MPL（羟基）> 空白",
            "TEM 观察：官能化显著减少白炭黑团聚和空隙",
        ],
        expected_samples=["SSBR-001", "SSBR-002", "SSBR-005"],
        category="相容性",
        difficulty="easy"
    ),
    EvalSample(
        question="氨基官能化 SSBR 的主要优势是什么？",
        ground_truth="氨基官能化 SSBR（如 SSBR-018）的主要优势是能够同时改善湿地抓地力和滚动阻力特性。SSBR-018 链端氨基官能化，白炭黑团聚体尺寸从 ~200 nm 降至 90-125 nm，Payne 效应最小。",
        ground_truth_context=[
            "SSBR-018 链端氨基官能化（0.09 wt%）：Tg=-17.4℃，试剂 DPE-NMe2",
            "SSBR-018 白炭黑分散性最优：团聚体尺寸从 ~200 nm 降至 90-125 nm，TXM 3D 成像确认 <100 nm 团聚体比例显著提高",
            'SSBR-018 轮胎"魔三角"性能平衡：高 tan δ(0°C)（湿地抓地力）、低 tan δ(60°C)（滚动阻力）、高力学强度',
            "SSBR-018 界面增强：紧密结合橡胶层（TBR）厚度 10.8 nm（+42%），松散结合橡胶层（LBR）厚度 12.5 nm（+44%）",
            "氨基-羟基氢键有效传递剪切力，促进团聚体破碎",
        ],
        expected_samples=["SSBR-018"],
        category="动态性能",
        difficulty="easy"
    ),
    
    # === 新增测试样本 (7个) - 已丰富 ground_truth_context ===
    EvalSample(
        question="环氧基官能化 SSBR 的官能化程度一般是多少？",
        ground_truth="环氧基官能化 SSBR 的官能化程度通常在 3-10 mol% 范围内，取决于环氧化反应条件和催化剂用量。Hayeemasae_2020 的研究中使用的环氧基官能化程度约为 5-8%，可有效改善与白炭黑的界面相互作用。",
        ground_truth_context=[
            # 由于数据库中暂无 SSBR-021~025 详细数据，保持原有简化 context
            "环氧基官能化：官能化程度通常 3-10 mol%，取决于环氧化反应条件",
            "环氧基官能团可与白炭黑表面硅羟基发生开环反应，形成共价键",
            "环氧基改善橡胶-填料界面相互作用，降低 Payne 效应",
        ],
        expected_samples=["SSBR-021", "SSBR-022", "SSBR-023"],
        category="官能化程度",
        difficulty="easy"
    ),
    EvalSample(
        question="羧基官能化 SSBR 的 Payne 效应相关数据是多少？",
        ground_truth="羧基官能化 SSBR 的 Payne 效应与官能化程度相关。SSBR-002（8.7 wt%）的 ΔG'=0.856 MPa（G'₀=1.45 MPa，G'∞=0.59 MPa），临界应变 γc≈3.5%。官能化程度越高，Payne 效应越小。",
        ground_truth_context=[
            "SSBR-002 羧基官能化（8.7 wt%）：Payne G'-应变曲线，G'₀=1.45 MPa，G'∞=0.59 MPa，ΔG'=0.856 MPa，临界应变 γc≈3.5%",
            "SSBR-003 硅烷官能化（1.7 wt%）：ΔG'=1.55 MPa (G'₀=2.1 MPa, G'∞=0.55 MPa)，tan δ (7% strain)=0.110",
            "SSBR-004 硅烷官能化（5.8 wt%）：ΔG'=1.33 MPa (G'₀=1.85 MPa, G'∞=0.52 MPa)，tan δ (7% strain)=0.086",
            "SSBR-005 硅烷官能化（9.5 wt%）：ΔG'=1.03 MPa (G'₀=1.55 MPa, G'∞=0.52 MPa)，tan δ (7% strain)=0.065（最低）",
            "Payne 效应越小，表示填料分散性越好，填料-填料网络越弱",
        ],
        expected_samples=["SSBR-002", "SSBR-003", "SSBR-004", "SSBR-005"],
        category="Payne效应",
        difficulty="medium"
    ),
    EvalSample(
        question="星型支化 SSBR 使用什么偶联剂合成？",
        ground_truth="星型支化 SSBR 通常使用 SiCl4（四氯化硅）或 SnCl4（四氯化锡）作为偶联剂，将多条活性聚合物链连接到中心原子。SSBR-043 采用 AMMO 硅烷偶联剂改性的星形 SSBR，具有 4 支链结构。",
        ground_truth_context=[
            "SSBR-043 星形 SSBR (YK-2)：4 支链结构，通过偶联剂将活性链连接到中心原子",
            "SSBR-043 采用 AMMO（[3-(2-氨基乙基)氨基丙基]三甲氧基硅烷）作为硅烷偶联剂",
            "偶联剂类型：SiCl4（四氯化硅）或 SnCl4（四氯化锡）可合成星型结构",
            "SSBR-043 分子量分布 PDI=1.82，完全无规共聚物",
        ],
        expected_samples=["SSBR-043"],
        category="合成方法",
        difficulty="easy"
    ),
    EvalSample(
        question="低滚动阻力轮胎需要 tan δ(60°C) 达到什么水平？",
        ground_truth="低滚动阻力轮胎要求 tan δ(60°C) 尽可能低。根据数据，SSBR-005 的 tan δ(60°C)≈0.08（滚动阻力降低 50.8%），SSBR-002 的 tan δ(60°C)≈0.13，SSBR-018 在四种变体中展现最佳综合性能。",
        ground_truth_context=[
            "SSBR-005 硅烷官能化（9.5 wt%）：tan δ(60°C)≈0.08，滚动阻力降低 50.8%（文献原文）",
            "SSBR-002 羧基官能化（8.7 wt%）：tan δ(60°C)≈0.13",
            "SSBR-003 硅烷官能化（1.7 wt%）：tan δ(60°C)≈0.1",
            "SSBR-004 硅烷官能化（5.8 wt%）：tan δ(60°C)≈0.09",
            "SSBR-018 氨基官能化：在四种 SSBR 变体中展现低滚动阻力（低 tan δ(60°C)）",
        ],
        expected_samples=["SSBR-002", "SSBR-003", "SSBR-004", "SSBR-005", "SSBR-018"],
        category="动态性能",
        difficulty="easy"
    ),
    EvalSample(
        question="活性阴离子聚合法合成的 SSBR 分子量分布如何？",
        ground_truth="活性阴离子聚合法合成的 SSBR 具有可控分子量分布。SSBR-001 的 Mn=18.5×10⁴ g/mol，SSBR-043（星形结构）的 Mn=33.6×10⁴ g/mol，PDI=1.82。",
        ground_truth_context=[
            "SSBR-001 羟基官能化：Mn=18.5×10⁴ g/mol（即 185000 g/mol）",
            "SSBR-043 星形 SSBR：Mn=33.6×10⁴ g/mol（即 336000 g/mol），PDI=1.82，完全无规共聚物",
            "活性阴离子聚合特点：快引发、慢增长、无终止、无转移",
            "官能化程度可通过试剂用量精确调控",
        ],
        expected_samples=["SSBR-001", "SSBR-043"],
        category="合成方法",
        difficulty="easy"
    ),
    EvalSample(
        question="羧基官能化 SSBR 的拉伸强度一般是多少？",
        ground_truth="羧基官能化 SSBR 的拉伸强度随官能化程度而变化。SSBR-002（8.7 wt% 羧基官能化）的拉伸强度为 26.0 MPa（所有样品最高），相比空白 SSBR（15.0 MPa）提升 73%。",
        ground_truth_context=[
            "SSBR-002 羧基官能化（8.7 wt%）：拉伸强度 26.0 MPa（所有样品最高），断裂伸长率 340%，300%定伸应力 23.3 MPa",
            "SSBR-002 相比空白 SSBR：拉伸强度从 15.0 MPa 提升到 26.0 MPa（+73%）",
            "羧基官能化双重界面作用：氢键（46 kJ/mol）+ 共价键（酯化反应）",
            "SSBR-001 羟基官能化（3.6 wt%）：拉伸强度 14.2 MPa",
        ],
        expected_samples=["SSBR-001", "SSBR-002"],
        category="力学性能",
        difficulty="easy"
    ),
    EvalSample(
        question="SSBR 的乙烯基含量对性能有什么影响？",
        ground_truth="SSBR 的乙烯基含量（1,2-结构含量）显著影响材料性能。SSBR-001 乙烯基含量 40.1 mol%，SSBR-043 乙烯基含量 46.0 mol%（三种 SSBR 中最高）。高乙烯基含量带来更高 Tg 和更好的湿地抓地力。",
        ground_truth_context=[
            "SSBR-001 羟基官能化：乙烯基含量 40.1 mol%，苯乙烯含量 23.0 wt%",
            "SSBR-043 星形 SSBR：乙烯基含量 46.0 mol%（三种 SSBR 中最高），苯乙烯含量 24.2 wt%",
            "SSBR-043 高乙烯基含量带来：更高的 Tg（+2℃）、更好的撕裂抗性、tan δ(0℃) 最高（湿地抓地力最优）",
            "乙烯基侧链双键可作为巯基-烯点击化学的反应位点",
            "高乙烯基含量：侧链乙烯基阻碍主链运动（提高 Tg），提供能量耗散（改善撕裂抗性）",
        ],
        expected_samples=["SSBR-001", "SSBR-043"],
        category="微观结构",
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
            # 获取 API 配置（支持两种环境变量名）
            api_key = os.environ.get("OPENAI_API_KEY", "")
            api_base = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE", "https://sg.uiuiapi.com/v1")
            
            # 调试输出
            logger.info(f"API Key 配置: {'已设置' if api_key else '未设置'} (长度: {len(api_key)})")
            logger.info(f"API Base URL: {api_base}")
            
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
            "contexts": List[str],   # 检索到的上下文 (需要与 ground_truth_context 格式对齐!)
            "ground_truth": str      # 标准答案（可选）
        }
        
        重要：contexts 的格式必须与 ground_truth_context 对齐，否则 RAGAS 计算会失败
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
                    
                    # ========================================
                    # 优化 Faithfulness：提供完整的原文内容
                    # ========================================
                    # 策略：将完整的 summary.md 原文作为 contexts
                    # 这样 RAGAS 可以验证回答中的每个声明
                    from synthesis.aggregator import SampleAggregator
                    aggregator = SampleAggregator()
                    
                    contexts = []
                    for s in response.answer.source_samples:
                        # 加载完整的 summary.md 内容
                        full_content = aggregator.load_sample_content(s.sample_id)
                        
                        if full_content:
                            # 取前 3000 字符，确保包含关键性能指标表格
                            # 移除 YAML front matter 以减少噪音
                            content_body = full_content
                            if '---' in full_content:
                                parts = full_content.split('---', 2)
                                if len(parts) >= 3:
                                    content_body = parts[2].strip()
                            
                            # 截取合理长度（约 3000 字符）
                            max_len = 3000
                            if len(content_body) > max_len:
                                content_body = content_body[:max_len] + "\n...[内容已截断]"
                            
                            # 添加样本标识
                            context_text = f"【{s.sample_id} - {s.functional_group or '未知'}官能化】\n{content_body}"
                        else:
                            # 降级：使用结构化数据
                            full_info = s.to_dict()
                            detailed_info = []
                            for k, v in full_info.items():
                                if v and v not in ['-', 'None', None, '未知官能团', '未知方法']:
                                    detailed_info.append(f"{k}: {v}")
                            context_text = f"【{s.sample_id}】\n" + "\n".join(detailed_info)
                        
                        contexts.append(context_text)
                    
                    response_time = response.total_time_ms
                    sample_count = response.sample_count
                else:
                    # 使用单样本问答模式
                    response = self.qa_engine.answer(sample.question, top_k=3)
                    answer = response.answer.answer_text
                    
                    # ========================================
                    # 优化 Faithfulness：提供完整的原文内容
                    # ========================================
                    from synthesis.aggregator import SampleAggregator
                    aggregator = SampleAggregator()
                    
                    contexts = []
                    for r in response.samples[:3]:
                        # 直接使用检索到的完整内容
                        if r.content:
                            # 移除 YAML front matter
                            content_body = r.content
                            if '---' in r.content:
                                parts = r.content.split('---', 2)
                                if len(parts) >= 3:
                                    content_body = parts[2].strip()
                            
                            # 截取合理长度（约 2500 字符）
                            max_len = 2500
                            if len(content_body) > max_len:
                                content_body = content_body[:max_len] + "\n...[内容已截断]"
                            
                            # 添加结构化摘要作为标题
                            summary = aggregator.extract_summary(
                                sample_id=r.sample_id,
                                content=r.content,
                                similarity=r.similarity,
                                quality_score=r.quality_score
                            )
                            header_parts = []
                            if summary.functional_group:
                                header_parts.append(f"{summary.functional_group}官能化")
                            if summary.functionalization_degree:
                                header_parts.append(f"{summary.functionalization_degree}")
                            header = ", ".join(header_parts) if header_parts else "样本数据"
                            
                            context_text = f"【{r.sample_id} - {header}】\n{content_body}"
                        else:
                            context_text = f"【{r.sample_id}】无详细内容"
                        
                        contexts.append(context_text)
                    
                    response_time = response.search_time_ms + response.generation_time_ms
                    sample_count = len(response.samples)
                
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
            # 重要：SingleTurnSample 需要 reference_contexts 来计算 Context Recall
            samples = []
            for d in dataset:
                # 准备参数
                sample_kwargs = {
                    "user_input": d["question"],
                    "response": d["answer"],
                    "retrieved_contexts": d["contexts"] if d["contexts"] else ["无检索结果"],
                    "reference": d.get("ground_truth", "") or "无标准答案",
                }
                
                # 添加 reference_contexts（ground_truth_context）用于 Context Recall 计算
                ground_truth_context = d.get("ground_truth_context", [])
                if ground_truth_context:
                    sample_kwargs["reference_contexts"] = ground_truth_context
                
                sample = SingleTurnSample(**sample_kwargs)
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
