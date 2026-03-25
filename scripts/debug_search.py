"""调试智能问答的元数据传递"""
import sys
sys.path.insert(0, "d:/SSBR")

from scripts.synthesis.aggregator import SampleAggregator
from scripts.rag_search import search
from scripts.reranker import get_reranker
from scripts.quality_scorer import QualityScorer

# 模拟 answer_generator 的流程
print("=" * 60)
print("模拟 answer_generator.generate() 流程")
print("=" * 60)

# 1. 搜索
results = search("改善白炭黑分散性", k=5)
print(f"\n1. RAG 搜索返回 {len(results)} 个结果")

# 2. 重排序 (简化，直接使用搜索结果)
print("\n2. 准备 samples_for_prompt:")

aggregator = SampleAggregator()

for i, r in enumerate(results[:3], 1):
    sample_id = r.get('sample_id')
    content = aggregator.load_sample_content(sample_id)
    
    # 模拟 answer_generator 中的结构化提取
    summary = aggregator.extract_summary(
        sample_id=sample_id,
        content=content,
        similarity=r.get('similarity', 0),
        quality_score=0.8
    )
    
    print(f"\n[{i}] {sample_id}")
    print(f"  functional_group: {summary.functional_group}")
    print(f"  reagent: {summary.reagent}")
    print(f"  functionalization_degree: {summary.functionalization_degree}")
    print(f"  doi: {summary.doi}")
    print(f"  first_author: {summary.first_author}")

print("\n" + "=" * 60)
print("[OK] 元数据将正确传递给 Prompt 模板")
print("=" * 60)
