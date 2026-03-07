#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RAG 检索系统评估脚本

用于量化评估 SSBR 推荐系统的检索准确性。
该脚本独立于主系统，仅用于学术评估目的。

评估指标：
- Hit@K: Top-K 结果中是否包含至少一个 relevant 样本
- Precision@K: Top-K 结果中 relevant + acceptable 的比例
- MRR (Mean Reciprocal Rank): 第一个 relevant 样本的排名倒数

Usage:
    python scripts/evaluate_rag.py
    python scripts/evaluate_rag.py --top-k 5 --output evaluation/report.md
"""

import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import argparse
import yaml
from datetime import datetime
from dataclasses import dataclass

from rag_search import RAGSearchEngine


@dataclass
class EvaluationResult:
    """单个测试用例的评估结果"""
    query_id: str
    query: str
    category: str
    top_k_results: list[str]  # 检索返回的 sample_id 列表
    relevant: list[str]       # 标注的 relevant 样本
    acceptable: list[str]     # 标注的 acceptable 样本
    hit: bool                 # 是否命中 relevant
    precision: float          # 精确率
    reciprocal_rank: float    # 倒数排名
    first_relevant_rank: int  # 第一个 relevant 的排名（0 表示未命中）


def load_test_cases(yaml_path: Path) -> list[dict]:
    """加载测试用例"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('test_cases', [])


def evaluate_single_query(
    engine: RAGSearchEngine,
    test_case: dict,
    top_k: int
) -> EvaluationResult:
    """评估单个查询"""
    query = test_case['query']
    relevant = set(test_case.get('relevant', []))
    acceptable = set(test_case.get('acceptable', []))
    
    # 执行检索
    results = engine.search(query, k=top_k)
    top_k_results = [r.sample_id for r in results]
    
    # 计算 Hit@K
    hit = bool(relevant & set(top_k_results))
    
    # 计算 Precision@K
    relevant_or_acceptable = relevant | acceptable
    correct_count = sum(1 for r in top_k_results if r in relevant_or_acceptable)
    precision = correct_count / len(top_k_results) if top_k_results else 0.0
    
    # 计算 Reciprocal Rank
    first_relevant_rank = 0
    for i, sample_id in enumerate(top_k_results, 1):
        if sample_id in relevant:
            first_relevant_rank = i
            break
    reciprocal_rank = 1.0 / first_relevant_rank if first_relevant_rank > 0 else 0.0
    
    return EvaluationResult(
        query_id=test_case['id'],
        query=query,
        category=test_case.get('category', '未分类'),
        top_k_results=top_k_results,
        relevant=list(relevant),
        acceptable=list(acceptable),
        hit=hit,
        precision=precision,
        reciprocal_rank=reciprocal_rank,
        first_relevant_rank=first_relevant_rank
    )


def run_evaluation(
    engine: RAGSearchEngine,
    test_cases: list[dict],
    top_k: int
) -> list[EvaluationResult]:
    """运行完整评估"""
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"  [{i}/{len(test_cases)}] 评估: {test_case['query'][:20]}...")
        result = evaluate_single_query(engine, test_case, top_k)
        results.append(result)
    return results


def calculate_metrics(results: list[EvaluationResult]) -> dict:
    """计算汇总指标"""
    n = len(results)
    if n == 0:
        return {}
    
    hit_count = sum(1 for r in results if r.hit)
    avg_precision = sum(r.precision for r in results) / n
    mrr = sum(r.reciprocal_rank for r in results) / n
    
    # 按类别统计
    categories = {}
    for r in results:
        cat = r.category
        if cat not in categories:
            categories[cat] = {'hit': 0, 'total': 0, 'precision_sum': 0}
        categories[cat]['total'] += 1
        categories[cat]['hit'] += int(r.hit)
        categories[cat]['precision_sum'] += r.precision
    
    category_metrics = {}
    for cat, data in categories.items():
        category_metrics[cat] = {
            'hit_rate': data['hit'] / data['total'],
            'avg_precision': data['precision_sum'] / data['total'],
            'count': data['total']
        }
    
    return {
        'total_queries': n,
        'hit_rate': hit_count / n,
        'avg_precision': avg_precision,
        'mrr': mrr,
        'hit_count': hit_count,
        'by_category': category_metrics
    }


def generate_report(
    results: list[EvaluationResult],
    metrics: dict,
    top_k: int,
    output_path: Path
) -> str:
    """生成 Markdown 评估报告"""
    
    report = f"""# RAG 检索系统评估报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**评估参数**: Top-K = {top_k}  
**测试用例数**: {metrics['total_queries']}

---

## 1. 总体指标

| 指标 | 数值 | 说明 |
|------|------|------|
| **Hit Rate@{top_k}** | {metrics['hit_rate']:.1%} ({metrics['hit_count']}/{metrics['total_queries']}) | Top-{top_k} 结果中包含 relevant 样本的查询比例 |
| **Avg Precision@{top_k}** | {metrics['avg_precision']:.1%} | Top-{top_k} 结果中相关样本的平均比例 |
| **MRR** | {metrics['mrr']:.3f} | Mean Reciprocal Rank，第一个正确结果的平均排名倒数 |

---

## 2. 分类别指标

| 类别 | 查询数 | Hit Rate | Avg Precision |
|------|--------|----------|---------------|
"""
    
    for cat, data in sorted(metrics['by_category'].items()):
        report += f"| {cat} | {data['count']} | {data['hit_rate']:.1%} | {data['avg_precision']:.1%} |\n"
    
    report += """
---

## 3. 详细结果

"""
    
    for r in results:
        hit_mark = "✅" if r.hit else "❌"
        report += f"""### {r.query_id}: {r.query}

- **类别**: {r.category}
- **命中**: {hit_mark} (首个 relevant 排名: {r.first_relevant_rank if r.first_relevant_rank > 0 else 'N/A'})
- **Precision@{top_k}**: {r.precision:.1%}
- **标注 relevant**: {', '.join(r.relevant)}
- **检索结果**: {', '.join(r.top_k_results)}

"""
    
    report += """---

## 4. 评估方法说明

### 4.1 指标定义

- **Hit Rate@K**: 衡量系统是否能在 Top-K 结果中返回至少一个正确答案
- **Precision@K**: 衡量 Top-K 结果中正确答案的比例（包括 relevant 和 acceptable）
- **MRR (Mean Reciprocal Rank)**: 衡量第一个正确答案出现的位置，排名越靠前得分越高

### 4.2 标注说明

- **relevant**: 与查询直接相关的样本，必须出现才算命中
- **acceptable**: 可接受的相关样本，出现可提高 Precision，不影响 Hit

### 4.3 局限性

- 测试集规模较小（12 个查询），统计意义有限
- 标注带有主观性，不同标注者可能有不同判断
- 小规模知识库（13 样本）限制了检索难度

---

*本报告由 `scripts/evaluate_rag.py` 自动生成，用于学术评估目的。*
"""
    
    # 写入文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report


def main():
    parser = argparse.ArgumentParser(description='RAG 检索系统评估')
    parser.add_argument('--top-k', type=int, default=5, help='Top-K 参数 (默认: 5)')
    parser.add_argument('--test-file', type=str, 
                        default='evaluation/test_queries.yaml',
                        help='测试用例文件路径')
    parser.add_argument('--output', type=str,
                        default='evaluation/report.md',
                        help='评估报告输出路径')
    args = parser.parse_args()
    
    print("=" * 60)
    print("RAG 检索系统评估")
    print("=" * 60)
    print()
    
    # 初始化检索引擎
    print("[1/4] 初始化检索引擎...")
    engine = RAGSearchEngine()
    
    if not engine.embedding_service.is_available():
        print("❌ Embedding 服务不可用，无法进行评估")
        sys.exit(1)
    
    print(f"  可检索样本数: {len(engine._get_all_summaries())}")
    
    # 加载测试用例
    print("[2/4] 加载测试用例...")
    test_file = PROJECT_ROOT / args.test_file
    if not test_file.exists():
        print(f"❌ 测试文件不存在: {test_file}")
        sys.exit(1)
    
    test_cases = load_test_cases(test_file)
    print(f"  测试用例数: {len(test_cases)}")
    
    # 运行评估
    print(f"[3/4] 运行评估 (Top-K = {args.top_k})...")
    results = run_evaluation(engine, test_cases, args.top_k)
    
    # 计算指标
    metrics = calculate_metrics(results)
    
    # 生成报告
    print("[4/4] 生成评估报告...")
    output_path = PROJECT_ROOT / args.output
    report = generate_report(results, metrics, args.top_k, output_path)
    
    print()
    print("=" * 60)
    print("评估完成")
    print("=" * 60)
    print()
    print(f"总体指标:")
    print(f"   Hit Rate@{args.top_k}: {metrics['hit_rate']:.1%} ({metrics['hit_count']}/{metrics['total_queries']})")
    print(f"   Avg Precision@{args.top_k}: {metrics['avg_precision']:.1%}")
    print(f"   MRR: {metrics['mrr']:.3f}")
    print()
    print(f"报告已保存: {output_path}")


if __name__ == "__main__":
    main()
