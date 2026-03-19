"""测试新增样本是否能被 RAG 检索到"""

import sys
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from rag_search import RAGSearchEngine

def main():
    print("=" * 60)
    print("RAG 新增样本检索测试")
    print("=" * 60)
    
    engine = RAGSearchEngine()
    
    # 测试用例：针对新增样本的特征进行检索
    test_queries = [
        ("环氧化SSBR", "应该检索到 SSBR-088, SSBR-099, SSBR-106 等环氧化样本"),
        ("氮化碳 C3N4 填料", "应该检索到 SSBR-107"),
        ("石墨烯氧化物 rGO", "应该检索到 SSBR-108"),
        ("电池极片压延", "应该检索到 SSBR-113"),
        ("三乙氧基硅烷偶联", "应该检索到 SSBR-111"),
    ]
    
    for query, expected in test_queries:
        print(f"\n查询: '{query}'")
        print(f"期望: {expected}")
        results = engine.search(query, k=5)
        print("结果:")
        for r in results:
            # 标记新增样本 (SSBR-083 及以后)
            sample_num = int(r.sample_id.split('-')[1])
            is_new = " [新增]" if sample_num >= 83 else ""
            print(f"  {r.sample_id}: sim={r.similarity:.3f}{is_new}")
    
    print("\n" + "=" * 60)
    print("测试完成")

if __name__ == "__main__":
    main()
