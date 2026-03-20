"""
ChromaDB 向量存储模块
替代原有的 JSON 缓存方案，提供更高效的向量检索

Created: 2026-03-20
优势:
- 持久化存储，无需每次加载完整 JSON
- 内置 HNSW 索引，毫秒级检索
- 支持元数据过滤
- 支持增量更新
"""

import logging
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime

import chromadb
from chromadb.config import Settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
INTERPRETATIONS_DIR = DATASET_DIR / "interpretations"
CACHE_DIR = PROJECT_ROOT / ".cache"
CHROMA_DB_DIR = CACHE_DIR / "chroma_db"

# 集合名称
COLLECTION_NAME = "ssbr_summaries"


class VectorStore:
    """
    基于 ChromaDB 的向量存储
    
    功能:
    - 持久化向量存储（PersistentClient）
    - 余弦相似度检索
    - 支持元数据过滤
    - 增量更新
    """
    
    def __init__(
        self,
        persist_dir: Path = CHROMA_DB_DIR,
        collection_name: str = COLLECTION_NAME
    ):
        """
        初始化向量存储
        
        Args:
            persist_dir: ChromaDB 持久化目录
            collection_name: 集合名称
        """
        self.persist_dir = Path(persist_dir)
        self.collection_name = collection_name
        self._client: Optional[chromadb.PersistentClient] = None
        self._collection = None
        self._initialized = False
    
    def _ensure_dir(self):
        """确保持久化目录存在"""
        self.persist_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_client(self) -> chromadb.PersistentClient:
        """获取或创建 ChromaDB 客户端"""
        if self._client is None:
            self._ensure_dir()
            self._client = chromadb.PersistentClient(
                path=str(self.persist_dir),
                settings=Settings(
                    anonymized_telemetry=False,  # 禁用遥测
                    allow_reset=True
                )
            )
            logger.info(f"ChromaDB 客户端已创建: {self.persist_dir}")
        return self._client
    
    def _get_collection(self):
        """获取或创建集合"""
        if self._collection is None:
            client = self._get_client()
            self._collection = client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
            )
            logger.info(f"集合已加载: {self.collection_name}, 文档数: {self._collection.count()}")
        return self._collection
    
    def add_document(
        self,
        doc_id: str,
        content: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        添加或更新单个文档
        
        Args:
            doc_id: 文档 ID（如 SSBR-001）
            content: 文档内容
            embedding: 向量
            metadata: 元数据（如 hash, mtime 等）
        """
        collection = self._get_collection()
        
        # 准备元数据
        meta = metadata.copy() if metadata else {}
        meta["updated_at"] = datetime.now().isoformat()
        
        # ChromaDB 的 upsert 会自动处理更新
        collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[meta]
        )
        logger.debug(f"文档已添加/更新: {doc_id}")
    
    def add_documents(
        self,
        doc_ids: List[str],
        contents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        批量添加文档
        
        Args:
            doc_ids: 文档 ID 列表
            contents: 文档内容列表
            embeddings: 向量列表
            metadatas: 元数据列表
        """
        if not doc_ids:
            return
        
        collection = self._get_collection()
        
        # 准备元数据
        now = datetime.now().isoformat()
        metas = []
        for i, doc_id in enumerate(doc_ids):
            meta = metadatas[i].copy() if metadatas and i < len(metadatas) else {}
            meta["updated_at"] = now
            metas.append(meta)
        
        collection.upsert(
            ids=doc_ids,
            embeddings=embeddings,
            documents=contents,
            metadatas=metas
        )
        logger.info(f"批量添加/更新 {len(doc_ids)} 个文档")
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict] = None
    ) -> List[Tuple[str, float, str, Dict]]:
        """
        向量相似度搜索
        
        Args:
            query_embedding: 查询向量
            top_k: 返回结果数量
            where: 元数据过滤条件
            
        Returns:
            List of (doc_id, similarity_score, content, metadata)
        """
        collection = self._get_collection()
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        
        # 转换结果格式
        output = []
        if results['ids'] and results['ids'][0]:
            for i, doc_id in enumerate(results['ids'][0]):
                # ChromaDB 返回的是距离 (cosine distance)，转换为相似度
                # cosine_distance = 1 - cosine_similarity
                # 所以 similarity = 1 - distance
                distance = results['distances'][0][i] if results['distances'] else 0
                similarity = 1 - distance
                content = results['documents'][0][i] if results['documents'] else ""
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                output.append((doc_id, similarity, content, metadata))
        
        return output
    
    def get_document(self, doc_id: str) -> Optional[Tuple[str, List[float], Dict]]:
        """
        获取单个文档
        
        Args:
            doc_id: 文档 ID
            
        Returns:
            (content, embedding, metadata) 或 None
        """
        collection = self._get_collection()
        
        result = collection.get(
            ids=[doc_id],
            include=["documents", "embeddings", "metadatas"]
        )
        
        if result['ids']:
            content = result['documents'][0] if result['documents'] else ""
            embedding = result['embeddings'][0] if result['embeddings'] else []
            metadata = result['metadatas'][0] if result['metadatas'] else {}
            return (content, embedding, metadata)
        return None
    
    def get_metadata(self, doc_id: str) -> Optional[Dict]:
        """获取文档元数据"""
        collection = self._get_collection()
        
        result = collection.get(
            ids=[doc_id],
            include=["metadatas"]
        )
        
        if result['ids'] and result['metadatas']:
            return result['metadatas'][0]
        return None
    
    def delete_document(self, doc_id: str) -> None:
        """删除单个文档"""
        collection = self._get_collection()
        collection.delete(ids=[doc_id])
        logger.debug(f"文档已删除: {doc_id}")
    
    def delete_documents(self, doc_ids: List[str]) -> None:
        """批量删除文档"""
        if not doc_ids:
            return
        collection = self._get_collection()
        collection.delete(ids=doc_ids)
        logger.info(f"批量删除 {len(doc_ids)} 个文档")
    
    def get_all_ids(self) -> List[str]:
        """获取所有文档 ID"""
        collection = self._get_collection()
        result = collection.get(include=[])
        return result['ids'] if result['ids'] else []
    
    def get_all_metadatas(self) -> Dict[str, Dict]:
        """获取所有文档的元数据"""
        collection = self._get_collection()
        result = collection.get(include=["metadatas"])
        
        if result['ids'] and result['metadatas']:
            return {
                doc_id: metadata
                for doc_id, metadata in zip(result['ids'], result['metadatas'])
            }
        return {}
    
    def count(self) -> int:
        """获取文档数量"""
        collection = self._get_collection()
        return collection.count()
    
    def clear(self) -> None:
        """清空所有文档"""
        client = self._get_client()
        # 删除并重建集合
        try:
            client.delete_collection(self.collection_name)
        except Exception:
            pass
        self._collection = client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("集合已清空并重建")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_documents": self.count(),
            "persist_dir": str(self.persist_dir),
            "collection_name": self.collection_name,
            "backend": "ChromaDB"
        }


# ============================================================================
# 兼容层：与旧版 VectorCache 接口兼容
# ============================================================================

class VectorStoreAdapter:
    """
    适配器类，提供与旧版 VectorCache 兼容的接口
    
    这样可以最小化对现有代码的修改
    """
    
    def __init__(
        self,
        persist_dir: Path = CHROMA_DB_DIR,
        interpretations_dir: Path = INTERPRETATIONS_DIR
    ):
        self.store = VectorStore(persist_dir=persist_dir)
        self.interpretations_dir = Path(interpretations_dir)
        self._loaded = False
    
    def _get_file_hash(self, file_path: Path) -> str:
        """计算文件内容的 MD5 哈希"""
        content = file_path.read_text(encoding='utf-8')
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _get_file_mtime(self, file_path: Path) -> float:
        """获取文件修改时间"""
        return file_path.stat().st_mtime
    
    def _extract_body(self, content: str) -> str:
        """提取 Markdown 正文（去除 YAML front matter）"""
        import re
        pattern = r'^---\s*\n.*?\n---\s*\n'
        body = re.sub(pattern, '', content, flags=re.DOTALL)
        return body.strip()
    
    def load(self) -> bool:
        """
        加载（兼容旧接口）
        ChromaDB 自动持久化，无需显式加载
        """
        self._loaded = True
        count = self.store.count()
        logger.info(f"ChromaDB 已就绪: {count} 个向量")
        return count > 0
    
    def save(self):
        """
        保存（兼容旧接口）
        ChromaDB 自动持久化，无需显式保存
        """
        pass
    
    def get_all_summaries(self) -> List[Dict]:
        """
        获取所有可检索的 summary.md 文件信息
        """
        summaries = []
        
        if not self.interpretations_dir.exists():
            logger.warning(f"解读文档目录不存在: {self.interpretations_dir}")
            return summaries
        
        for sample_dir in self.interpretations_dir.iterdir():
            if not sample_dir.is_dir():
                continue
            if sample_dir.name.startswith('TEMPLATE'):
                continue
            
            summary_path = sample_dir / "summary.md"
            if not summary_path.exists():
                continue
            
            try:
                content = summary_path.read_text(encoding='utf-8')
                body = self._extract_body(content)
                
                if len(body) < 50:
                    continue
                
                summaries.append({
                    'sample_id': sample_dir.name,
                    'path': str(summary_path),
                    'content': body,
                    'hash': self._get_file_hash(summary_path),
                    'mtime': self._get_file_mtime(summary_path)
                })
            except Exception as e:
                logger.error(f"读取 {summary_path} 失败: {e}")
        
        return summaries
    
    def check_updates(self, summaries: List[Dict]) -> Tuple[List[Dict], List[str]]:
        """
        检查哪些文档需要更新
        """
        to_update = []
        to_delete = []
        
        current_ids = {s['sample_id'] for s in summaries}
        cached_ids = set(self.store.get_all_ids())
        
        # 需要删除的（文件已不存在）
        to_delete = list(cached_ids - current_ids)
        
        # 获取所有已缓存的元数据
        all_metadatas = self.store.get_all_metadatas()
        
        # 检查需要更新的
        for summary in summaries:
            sample_id = summary['sample_id']
            cached_meta = all_metadatas.get(sample_id)
            
            if cached_meta is None:
                # 新文档
                to_update.append(summary)
            elif cached_meta.get("hash") != summary['hash']:
                # 内容变化
                to_update.append(summary)
        
        return to_update, to_delete
    
    def build_cache(self, embedding_service, force_rebuild: bool = False) -> int:
        """
        构建或更新向量缓存
        """
        summaries = self.get_all_summaries()
        logger.info(f"找到 {len(summaries)} 个可检索样本")
        
        if force_rebuild:
            self.store.clear()
            to_update = summaries
            to_delete = []
        else:
            to_update, to_delete = self.check_updates(summaries)
        
        # 处理删除
        if to_delete:
            self.store.delete_documents(to_delete)
            logger.info(f"删除 {len(to_delete)} 个过期文档")
        
        if not to_update:
            logger.info("所有文档已是最新，无需更新")
            return 0
        
        logger.info(f"需要更新 {len(to_update)} 个文档")
        
        # 批量向量化
        try:
            texts = [s['content'] for s in to_update]
            embeddings = embedding_service.embed_batch(texts)
            
            # 准备元数据
            doc_ids = [s['sample_id'] for s in to_update]
            contents = texts
            metadatas = [
                {"hash": s['hash'], "mtime": s['mtime']}
                for s in to_update
            ]
            
            # 批量添加
            self.store.add_documents(doc_ids, contents, embeddings, metadatas)
            
            logger.info(f"缓存更新完成: {len(to_update)} 个文档")
            return len(to_update)
            
        except Exception as e:
            logger.error(f"批量向量化失败: {e}")
            # 降级为逐条处理
            return self._build_cache_sequential(to_update, embedding_service)
    
    def _build_cache_sequential(
        self,
        summaries: List[Dict],
        embedding_service
    ) -> int:
        """逐条向量化（降级方案）"""
        updated = 0
        
        for summary in summaries:
            sample_id = summary['sample_id']
            try:
                embedding = embedding_service.embed(summary['content'])
                
                self.store.add_document(
                    doc_id=sample_id,
                    content=summary['content'],
                    embedding=embedding,
                    metadata={"hash": summary['hash'], "mtime": summary['mtime']}
                )
                updated += 1
                logger.debug(f"更新向量: {sample_id}")
                
            except Exception as e:
                logger.warning(f"向量化失败 {sample_id}: {e}")
        
        return updated
    
    def get_embedding(self, sample_id: str) -> Optional[List[float]]:
        """获取指定样本的向量"""
        doc = self.store.get_document(sample_id)
        if doc:
            return doc[1]  # (content, embedding, metadata)
        return None
    
    def get_all_embeddings(self) -> Dict[str, List[float]]:
        """获取所有已缓存的向量"""
        collection = self.store._get_collection()
        result = collection.get(include=["embeddings"])
        
        if result['ids'] and result['embeddings']:
            return {
                doc_id: embedding
                for doc_id, embedding in zip(result['ids'], result['embeddings'])
            }
        return {}
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        stats = self.store.get_stats()
        stats["cache_exists"] = self.store.count() > 0
        return stats


# ============================================================================
# 全局实例管理
# ============================================================================

_vector_store: Optional[VectorStoreAdapter] = None


def get_vector_store() -> VectorStoreAdapter:
    """获取全局向量存储实例"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStoreAdapter()
    return _vector_store


# 兼容旧接口
def get_vector_cache() -> VectorStoreAdapter:
    """兼容旧接口：获取向量缓存（实际返回 VectorStoreAdapter）"""
    return get_vector_store()


def build_vector_cache(embedding_service, force: bool = False) -> int:
    """便捷函数：构建向量缓存"""
    store = get_vector_store()
    return store.build_cache(embedding_service, force_rebuild=force)


if __name__ == '__main__':
    print("ChromaDB 向量存储模块")
    print("=" * 60)
    
    store = get_vector_store()
    store.load()
    
    stats = store.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    summaries = store.get_all_summaries()
    print(f"\n可检索样本数: {len(summaries)}")
    
    to_update, to_delete = store.check_updates(summaries)
    print(f"需要更新: {len(to_update)}")
    print(f"需要删除: {len(to_delete)}")
