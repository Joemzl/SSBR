"""
相似度计算工具
用于计算向量之间的余弦相似度

Created: 2026-03-05
"""

from typing import List, Tuple
import numpy as np


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    计算两个向量的余弦相似度
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
        
    Returns:
        余弦相似度，范围 [0, 1]（对于归一化向量）
        
    Raises:
        ValueError: 向量为空或长度不一致时抛出
    """
    if not vec1 or not vec2:
        raise ValueError("向量不能为空")
    
    if len(vec1) != len(vec2):
        raise ValueError(f"向量长度不一致: {len(vec1)} vs {len(vec2)}")
    
    v1 = np.array(vec1, dtype=np.float64)
    v2 = np.array(vec2, dtype=np.float64)
    
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    similarity = float(np.dot(v1, v2) / (norm1 * norm2))
    
    # 由于浮点精度问题，可能略微超出 [-1, 1] 范围
    return max(0.0, min(1.0, similarity))


def batch_cosine_similarity(
    query_vec: List[float], 
    doc_vecs: List[List[float]]
) -> List[float]:
    """
    计算查询向量与多个文档向量的相似度
    
    Args:
        query_vec: 查询向量
        doc_vecs: 文档向量列表
        
    Returns:
        相似度列表，与 doc_vecs 顺序一致
    """
    return [cosine_similarity(query_vec, doc_vec) for doc_vec in doc_vecs]


def rank_by_similarity(
    query_vec: List[float],
    items: List[Tuple[str, List[float]]],
    k: int = 3,
    threshold: float = 0.0
) -> List[Tuple[str, float]]:
    """
    根据相似度排序并返回 Top-K 结果
    
    Args:
        query_vec: 查询向量
        items: (id, vector) 元组列表
        k: 返回数量
        threshold: 最低相似度阈值
        
    Returns:
        (id, similarity) 元组列表，按相似度降序排列
    """
    results = []
    
    for item_id, item_vec in items:
        try:
            sim = cosine_similarity(query_vec, item_vec)
            if sim >= threshold:
                results.append((item_id, sim))
        except ValueError:
            # 跳过无效向量
            continue
    
    # 按相似度降序排序
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results[:k]


def classify_relevance(similarity: float) -> str:
    """
    根据相似度分类相关性
    
    基于 search-api.md 定义的阈值:
    - ≥ 0.7: 高度相关
    - 0.5-0.7: 相关
    - < 0.5: 参考
    
    Args:
        similarity: 相似度值 [0, 1]
        
    Returns:
        相关性标签
    """
    if similarity >= 0.7:
        return "高度相关"
    elif similarity >= 0.5:
        return "相关"
    else:
        return "参考"


def format_search_result(
    sample_id: str,
    similarity: float,
    summary_path: str
) -> dict:
    """
    格式化搜索结果
    
    Args:
        sample_id: 样本 ID
        similarity: 相似度
        summary_path: summary.md 路径
        
    Returns:
        符合 search-api.md 契约的结果字典
    """
    return {
        "sample_id": sample_id,
        "similarity": round(similarity, 2),
        "summary_path": summary_path,
        "relevance": classify_relevance(similarity)
    }


if __name__ == '__main__':
    # 简单测试
    print("相似度计算模块测试")
    print("="*50)
    
    # 测试余弦相似度
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    v3 = [0.0, 1.0, 0.0]
    v4 = [0.707, 0.707, 0.0]
    
    print(f"v1·v2 (相同): {cosine_similarity(v1, v2):.4f}")  # 应为 1.0
    print(f"v1·v3 (正交): {cosine_similarity(v1, v3):.4f}")  # 应为 0.0
    print(f"v1·v4 (45度): {cosine_similarity(v1, v4):.4f}")  # 应约为 0.707
    
    print()
    print("相关性分类:")
    for sim in [0.9, 0.7, 0.6, 0.5, 0.4, 0.2]:
        print(f"  {sim:.1f} → {classify_relevance(sim)}")
