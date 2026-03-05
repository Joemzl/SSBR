"""
RAG 语义检索核心模块
实现基于 summary.md 的语义检索功能

Created: 2026-03-05
Tasks: T027, T028, T029, T030
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.yaml_parser import read_interpretation_file, extract_markdown_body
from utils.embedding import EmbeddingService, EmbeddingError, get_embedding_service
from utils.similarity import cosine_similarity, classify_relevance, format_search_result
from utils.query_preprocessor import preprocess_query, QueryPreprocessor

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
    """
    
    def __init__(
        self,
        interpretations_dir: Path = INTERPRETATIONS_DIR,
        embedding_service: Optional[EmbeddingService] = None
    ):
        """
        初始化检索引擎
        
        Args:
            interpretations_dir: 解读文档目录
            embedding_service: Embedding 服务实例，默认使用全局实例
        """
        self.interpretations_dir = Path(interpretations_dir)
        self.embedding_service = embedding_service or get_embedding_service()
        self.query_preprocessor = QueryPreprocessor()
    
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
        
        # 4. 计算相似度
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
        
        # 5. 排序并返回 Top-K
        results.sort(key=lambda x: x.similarity, reverse=True)
        top_k = results[:k]
        
        # 6. 检查是否所有结果都低于 0.5
        if top_k and all(r.similarity < 0.5 for r in top_k):
            logger.info("所有结果相似度 < 0.5，标记为参考级别")
        
        logger.info(f"返回 {len(top_k)} 个结果")
        return top_k
    
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
    
    summaries = engine._get_all_summaries()
    print(f"可检索样本数: {len(summaries)}")
    
    if summaries:
        print("\n可检索样本列表:")
        for s in summaries:
            print(f"  - {s['sample_id']}: {len(s['content'])} 字符")
    
    # 如果 API 可用，执行测试查询
    if engine.embedding_service.is_available():
        print("\n执行测试查询: '改善白炭黑分散性'")
        try:
            results = engine.search("改善白炭黑分散性", k=3)
            print(f"\n结果 ({len(results)} 个):")
            for r in results:
                print(f"  {r}")
        except Exception as e:
            print(f"查询失败: {e}")
    else:
        print("\nEmbedding 服务不可用，跳过测试查询")
