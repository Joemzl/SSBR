"""
RAG 语义检索核心模块
实现基于 summary.md 的语义检索功能

Created: 2026-03-05
Updated: 2026-03-19 - 添加向量缓存支持，大幅提升查询性能
Tasks: T027, T028, T029, T030

性能优化:
- 使用向量缓存，避免每次查询都重新向量化所有文档
- 支持增量更新，只更新变化的文档
- 查询延迟从 25-30秒 降低到 1-2秒
"""

import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.yaml_parser import read_interpretation_file, extract_markdown_body
from utils.embedding import EmbeddingService, EmbeddingError, get_embedding_service
from utils.similarity import cosine_similarity, classify_relevance, format_search_result
from utils.query_preprocessor import preprocess_query, QueryPreprocessor
# 使用 ChromaDB 向量存储（兼容旧接口）
from utils.vector_store import VectorStoreAdapter, get_vector_cache

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
INTERPRETATIONS_DIR = DATASET_DIR / "interpretations"


class SearchResult:
    """搜索结果数据类"""
    
    def __init__(
        self,
        sample_id: str,
        similarity: float,
        summary_path: str,
        relevance: str
    ):
        self.sample_id = sample_id
        self.similarity = similarity
        self.summary_path = summary_path
        self.relevance = relevance
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "similarity": round(self.similarity, 2),
            "summary_path": self.summary_path,
            "relevance": self.relevance
        }
    
    def __repr__(self) -> str:
        return f"SearchResult({self.sample_id}, sim={self.similarity:.2f}, {self.relevance})"


class RAGSearchEngine:
    """
    RAG 语义检索引擎
    
    实现 search-api.md 契约定义的检索接口
    
    性能优化 (2026-03-19):
    - 使用向量缓存预计算文档向量
    - 查询时只需计算查询向量 + 从缓存读取文档向量
    - 查询延迟从 25-30秒 降低到 1-2秒
    """
    
    def __init__(
        self,
        interpretations_dir: Path = INTERPRETATIONS_DIR,
        embedding_service: Optional[EmbeddingService] = None,
        use_cache: bool = True
    ):
        """
        初始化检索引擎
        
        Args:
            interpretations_dir: 解读文档目录
            embedding_service: Embedding 服务实例，默认使用全局实例
            use_cache: 是否使用向量缓存（默认启用）
        """
        self.interpretations_dir = Path(interpretations_dir)
        self.embedding_service = embedding_service or get_embedding_service()
        self.query_preprocessor = QueryPreprocessor()
        self.use_cache = use_cache
        self._vector_cache: Optional[VectorStoreAdapter] = None
        self._cache_initialized = False
    
    def _get_vector_cache(self) -> VectorStoreAdapter:
        """获取或初始化向量缓存"""
        if self._vector_cache is None:
            self._vector_cache = get_vector_cache()
        return self._vector_cache
    
    def ensure_cache(self, force_rebuild: bool = False) -> int:
        """
        确保向量缓存已构建
        
        Args:
            force_rebuild: 是否强制重建缓存
            
        Returns:
            更新的文档数量
        """
        if not self.use_cache:
            return 0
        
        cache = self._get_vector_cache()
        updated = cache.build_cache(self.embedding_service, force_rebuild=force_rebuild)
        self._cache_initialized = True
        return updated
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        if not self.use_cache:
            return {"cache_enabled": False}
        
        cache = self._get_vector_cache()
        stats = cache.get_stats()
        stats["cache_enabled"] = True
        return stats
    
    def _get_all_summaries(self) -> List[Dict[str, Any]]:
        """
        获取所有可检索的 summary.md 文件
        
        Returns:
            summary 信息列表
        """
        summaries = []
        
        if not self.interpretations_dir.exists():
            logger.warning(f"解读文档目录不存在: {self.interpretations_dir}")
            return summaries
        
        for sample_dir in self.interpretations_dir.iterdir():
            # 跳过非目录和模板文件
            if not sample_dir.is_dir():
                continue
            if sample_dir.name.startswith('TEMPLATE'):
                continue
            
            summary_path = sample_dir / "summary.md"
            if not summary_path.exists():
                logger.debug(f"样本 {sample_dir.name} 缺少 summary.md")
                continue
            
            try:
                content = summary_path.read_text(encoding='utf-8')
                # 提取正文用于向量化（去除 YAML front matter）
                body = extract_markdown_body(content)
                
                if len(body) < 50:
                    logger.warning(f"样本 {sample_dir.name} 的 summary.md 内容过短")
                    continue
                
                summaries.append({
                    'sample_id': sample_dir.name,
                    'path': str(summary_path),
                    'content': body
                })
            except Exception as e:
                logger.error(f"读取 {summary_path} 失败: {e}")
        
        return summaries
    
    def search(
        self,
        query: str,
        k: int = 3,
        threshold: float = 0.0
    ) -> List[SearchResult]:
        """
        语义检索主接口
        
        基于用户查询返回相似样本。实现 search-api.md 定义的契约。
        
        Args:
            query: 用户自然语言查询
            k: 返回结果数量，默认 3
            threshold: 最低相似度阈值，默认 0.0
            
        Returns:
            SearchResult 列表，按相似度降序排列
            
        Raises:
            ValueError: 查询无效时抛出
            EmbeddingError: Embedding API 调用失败时抛出
        """
        start_time = time.time()
        
        # 1. 预处理查询
        processed_query, warning = self.query_preprocessor.process(query)
        if warning:
            logger.info(f"查询预处理警告: {warning}")
        
        logger.info(f"执行检索: '{processed_query[:50]}...' (k={k}, threshold={threshold})")
        
        # 2. 获取所有 summary
        summaries = self._get_all_summaries()
        
        if not summaries:
            logger.warning("没有可检索的样本")
            return []
        
        logger.info(f"找到 {len(summaries)} 个可检索样本")
        
        # 3. 获取查询向量
        try:
            query_embedding = self.embedding_service.embed(processed_query)
        except EmbeddingError as e:
            logger.error(f"查询向量化失败: {e}")
            raise
        
        # 4. 计算相似度（使用缓存优化）
        results = []
        
        if self.use_cache:
            # 优化路径：使用向量缓存
            results = self._search_with_cache(summaries, query_embedding, threshold)
        else:
            # 原始路径：实时计算（保留用于兼容）
            results = self._search_realtime(summaries, query_embedding, threshold)
        
        # 5. 排序并返回 Top-K
        results.sort(key=lambda x: x.similarity, reverse=True)
        top_k = results[:k]
        
        # 6. 检查是否所有结果都低于 0.5
        if top_k and all(r.similarity < 0.5 for r in top_k):
            logger.info("所有结果相似度 < 0.5，标记为参考级别")
        
        elapsed = time.time() - start_time
        logger.info(f"返回 {len(top_k)} 个结果，耗时 {elapsed:.2f} 秒")
        return top_k
    
    def _search_with_cache(
        self,
        summaries: List[Dict[str, Any]],
        query_embedding: List[float],
        threshold: float
    ) -> List[SearchResult]:
        """
        使用 ChromaDB 向量存储进行检索（优化路径）
        
        性能: 毫秒级 HNSW 近似最近邻搜索
        """
        cache = self._get_vector_cache()
        
        # 确保缓存已加载
        if not self._cache_initialized:
            cache.load()
            
            # 检查是否需要更新缓存
            cache_summaries = cache.get_all_summaries()
            to_update, _ = cache.check_updates(cache_summaries)
            
            if to_update:
                logger.info(f"检测到 {len(to_update)} 个文档需要更新缓存")
                cache.build_cache(self.embedding_service)
            
            self._cache_initialized = True
        
        # 使用 ChromaDB 原生搜索（返回所有文档，后续再筛选）
        # ChromaDB 内置了 HNSW 索引，比遍历快得多
        search_results = cache.store.search(
            query_embedding=query_embedding,
            top_k=len(summaries)  # 获取所有结果，后续按阈值过滤
        )
        
        results = []
        for doc_id, similarity, content, metadata in search_results:
            # 应用阈值
            if similarity >= threshold:
                # 找到对应的 summary 路径
                summary_path = ""
                for s in summaries:
                    if s['sample_id'] == doc_id:
                        summary_path = s['path']
                        break
                
                result = SearchResult(
                    sample_id=doc_id,
                    similarity=similarity,
                    summary_path=summary_path,
                    relevance=classify_relevance(similarity)
                )
                results.append(result)
                logger.debug(f"  {doc_id}: {similarity:.3f}")
        
        logger.info(f"ChromaDB 搜索返回 {len(search_results)} 个结果，阈值过滤后 {len(results)} 个")
        return results
    
    def _search_realtime(
        self,
        summaries: List[Dict[str, Any]],
        query_embedding: List[float],
        threshold: float
    ) -> List[SearchResult]:
        """
        实时计算向量进行检索（原始路径，保留用于兼容）
        
        性能: O(n) API 调用，较慢
        """
        results = []
        
        for summary in summaries:
            try:
                # 实时计算 summary 向量
                doc_embedding = self.embedding_service.embed(summary['content'])
                
                # 计算余弦相似度
                sim = cosine_similarity(query_embedding, doc_embedding)
                
                # 应用阈值
                if sim >= threshold:
                    result = SearchResult(
                        sample_id=summary['sample_id'],
                        similarity=sim,
                        summary_path=summary['path'],
                        relevance=classify_relevance(sim)
                    )
                    results.append(result)
                    logger.debug(f"  {summary['sample_id']}: {sim:.3f}")
                    
            except EmbeddingError as e:
                logger.warning(f"样本 {summary['sample_id']} 向量化失败: {e}")
                continue
        
        return results
    
    def get_summary_content(self, sample_id: str) -> Optional[str]:
        """
        获取样本的 summary.md 全文内容
        
        Args:
            sample_id: 样本 ID
            
        Returns:
            summary.md 内容，文件不存在返回 None
        """
        summary_path = self.interpretations_dir / sample_id / "summary.md"
        
        if not summary_path.exists():
            return None
        
        try:
            return summary_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"读取 {summary_path} 失败: {e}")
            return None
    
    def is_available(self) -> bool:
        """
        检查检索引擎是否可用
        
        Returns:
            True 如果 Embedding 服务可用且有可检索样本
        """
        if not self.embedding_service.is_available():
            return False
        
        summaries = self._get_all_summaries()
        return len(summaries) > 0


def search(query: str, k: int = 3, threshold: float = 0.0) -> List[Dict[str, Any]]:
    """
    便捷函数：执行语义检索
    
    实现 search-api.md 定义的主接口
    
    Args:
        query: 用户自然语言查询
        k: 返回结果数量
        threshold: 最低相似度阈值
        
    Returns:
        符合契约的结果字典列表
    """
    engine = RAGSearchEngine()
    results = engine.search(query, k, threshold)
    return [r.to_dict() for r in results]


def format_search_results_for_skill(
    results: List[Dict[str, Any]],
    include_content: bool = True
) -> str:
    """
    格式化搜索结果用于 Skill 调用
    
    Args:
        results: 搜索结果列表
        include_content: 是否包含 summary 内容
        
    Returns:
        格式化的 Markdown 字符串
    """
    if not results:
        return "## 检索结果\n\n未找到相关样本。"
    
    # 检查是否全部为参考级别
    all_reference = all(r.get('relevance') == '参考' for r in results)
    
    lines = ["## 检索到的相关案例"]
    
    if all_reference:
        lines.extend([
            "",
            "> ⚠️ **提示**: 知识库中无高度相关案例，以下为参考",
            ""
        ])
    
    lines.append("")
    
    engine = RAGSearchEngine()
    
    for i, result in enumerate(results, 1):
        sample_id = result['sample_id']
        similarity = result['similarity']
        relevance = result['relevance']
        
        lines.extend([
            f"### 案例 {i}: {sample_id} (相似度: {similarity}, {relevance})",
            ""
        ])
        
        if include_content:
            content = engine.get_summary_content(sample_id)
            if content:
                lines.extend([content, "", "---", ""])
    
    return "\n".join(lines)


if __name__ == '__main__':
    # 测试
    print("RAG 检索引擎测试")
    print("=" * 60)
    
    engine = RAGSearchEngine()
    
    print(f"\n解读文档目录: {engine.interpretations_dir}")
    print(f"Embedding 服务可用: {engine.embedding_service.is_available()}")
    print(f"使用向量缓存: {engine.use_cache}")
    
    summaries = engine._get_all_summaries()
    print(f"可检索样本数: {len(summaries)}")
    
    # 显示缓存状态
    cache_stats = engine.get_cache_stats()
    print(f"\n缓存状态:")
    for key, value in cache_stats.items():
        print(f"  {key}: {value}")
    
    if summaries:
        print("\n可检索样本列表 (前 10 个):")
        for s in summaries[:10]:
            print(f"  - {s['sample_id']}: {len(s['content'])} 字符")
        if len(summaries) > 10:
            print(f"  ... 共 {len(summaries)} 个样本")
    
    # 如果 API 可用，执行测试查询
    if engine.embedding_service.is_available():
        print("\n" + "=" * 60)
        print("构建/更新向量缓存...")
        updated = engine.ensure_cache()
        print(f"更新了 {updated} 个文档的向量")
        
        print("\n" + "=" * 60)
        print("执行测试查询: '改善白炭黑分散性'")
        try:
            start = time.time()
            results = engine.search("改善白炭黑分散性", k=3)
            elapsed = time.time() - start
            
            print(f"\n结果 ({len(results)} 个)，耗时 {elapsed:.2f} 秒:")
            for r in results:
                print(f"  {r}")
        except Exception as e:
            print(f"查询失败: {e}")
    else:
        print("\nEmbedding 服务不可用，跳过测试查询")
