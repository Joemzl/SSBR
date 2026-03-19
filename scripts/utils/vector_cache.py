"""
向量缓存模块
实现文档向量的预计算、持久化存储和增量更新

Created: 2026-03-19
优化目标: 将查询延迟从 25-30秒 降低到 1-2秒

设计原则:
1. 启动时加载缓存，首次使用时构建
2. 基于文件 mtime 检测变更，只更新需要的文档
3. 缓存存储为 JSON 文件，便于调试和版本控制
"""

import json
import os
import time
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
INTERPRETATIONS_DIR = DATASET_DIR / "interpretations"
CACHE_DIR = PROJECT_ROOT / ".cache"
VECTOR_CACHE_FILE = CACHE_DIR / "vector_cache.json"


class VectorCache:
    """
    向量缓存管理器
    
    功能:
    - 预计算所有 summary.md 的向量
    - 持久化存储到本地文件
    - 增量更新变化的文档
    - 批量向量化 API 调用
    """
    
    def __init__(
        self,
        cache_file: Path = VECTOR_CACHE_FILE,
        interpretations_dir: Path = INTERPRETATIONS_DIR
    ):
        self.cache_file = Path(cache_file)
        self.interpretations_dir = Path(interpretations_dir)
        self._cache: Dict = {}
        self._embeddings: Dict[str, List[float]] = {}
        self._loaded = False
    
    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _get_file_hash(self, file_path: Path) -> str:
        """计算文件内容的 MD5 哈希"""
        content = file_path.read_text(encoding='utf-8')
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def _get_file_mtime(self, file_path: Path) -> float:
        """获取文件修改时间"""
        return file_path.stat().st_mtime
    
    def load(self) -> bool:
        """
        加载缓存文件
        
        Returns:
            True 如果缓存加载成功，False 如果缓存不存在或损坏
        """
        if self._loaded:
            return True
        
        if not self.cache_file.exists():
            logger.info("缓存文件不存在，将创建新缓存")
            self._cache = {"version": "1.0", "documents": {}}
            self._embeddings = {}
            return False
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self._cache = json.load(f)
            
            # 提取向量
            self._embeddings = {
                sample_id: doc["embedding"]
                for sample_id, doc in self._cache.get("documents", {}).items()
                if "embedding" in doc
            }
            
            self._loaded = True
            logger.info(f"加载缓存成功: {len(self._embeddings)} 个向量")
            return True
            
        except Exception as e:
            logger.error(f"加载缓存失败: {e}")
            self._cache = {"version": "1.0", "documents": {}}
            self._embeddings = {}
            return False
    
    def save(self):
        """保存缓存到文件"""
        self._ensure_cache_dir()
        
        self._cache["updated_at"] = datetime.now().isoformat()
        
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
            logger.info(f"保存缓存成功: {len(self._embeddings)} 个向量")
        except Exception as e:
            logger.error(f"保存缓存失败: {e}")
    
    def get_all_summaries(self) -> List[Dict]:
        """
        获取所有可检索的 summary.md 文件信息
        
        Returns:
            包含 sample_id, path, content, hash 的字典列表
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
                
                # 提取正文（去除 YAML front matter）
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
    
    def _extract_body(self, content: str) -> str:
        """提取 Markdown 正文（去除 YAML front matter）"""
        import re
        pattern = r'^---\s*\n.*?\n---\s*\n'
        body = re.sub(pattern, '', content, flags=re.DOTALL)
        return body.strip()
    
    def check_updates(self, summaries: List[Dict]) -> Tuple[List[Dict], List[str]]:
        """
        检查哪些文档需要更新
        
        Args:
            summaries: 当前文件系统中的 summary 列表
            
        Returns:
            (需要更新的文档列表, 需要删除的 sample_id 列表)
        """
        to_update = []
        to_delete = []
        
        current_ids = {s['sample_id'] for s in summaries}
        cached_ids = set(self._cache.get("documents", {}).keys())
        
        # 检查需要删除的（文件已不存在）
        to_delete = list(cached_ids - current_ids)
        
        # 检查需要更新的
        for summary in summaries:
            sample_id = summary['sample_id']
            cached_doc = self._cache.get("documents", {}).get(sample_id)
            
            if cached_doc is None:
                # 新文档
                to_update.append(summary)
            elif cached_doc.get("hash") != summary['hash']:
                # 内容变化
                to_update.append(summary)
        
        return to_update, to_delete
    
    def build_cache(self, embedding_service, force_rebuild: bool = False) -> int:
        """
        构建或更新向量缓存
        
        Args:
            embedding_service: EmbeddingService 实例
            force_rebuild: 是否强制重建全部缓存
            
        Returns:
            更新的文档数量
        """
        self.load()
        
        summaries = self.get_all_summaries()
        logger.info(f"找到 {len(summaries)} 个可检索样本")
        
        if force_rebuild:
            to_update = summaries
            to_delete = []
        else:
            to_update, to_delete = self.check_updates(summaries)
        
        # 处理删除
        for sample_id in to_delete:
            if sample_id in self._cache.get("documents", {}):
                del self._cache["documents"][sample_id]
            if sample_id in self._embeddings:
                del self._embeddings[sample_id]
            logger.info(f"删除缓存: {sample_id}")
        
        if not to_update:
            logger.info("所有文档已是最新，无需更新")
            return 0
        
        logger.info(f"需要更新 {len(to_update)} 个文档")
        
        # 批量向量化
        try:
            texts = [s['content'] for s in to_update]
            embeddings = embedding_service.embed_batch(texts)
            
            # 更新缓存
            if "documents" not in self._cache:
                self._cache["documents"] = {}
            
            for i, summary in enumerate(to_update):
                sample_id = summary['sample_id']
                self._cache["documents"][sample_id] = {
                    "hash": summary['hash'],
                    "mtime": summary['mtime'],
                    "embedding": embeddings[i],
                    "updated_at": datetime.now().isoformat()
                }
                self._embeddings[sample_id] = embeddings[i]
                logger.debug(f"更新向量: {sample_id}")
            
            # 保存缓存
            self.save()
            
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
        
        if "documents" not in self._cache:
            self._cache["documents"] = {}
        
        for summary in summaries:
            sample_id = summary['sample_id']
            try:
                embedding = embedding_service.embed(summary['content'])
                
                self._cache["documents"][sample_id] = {
                    "hash": summary['hash'],
                    "mtime": summary['mtime'],
                    "embedding": embedding,
                    "updated_at": datetime.now().isoformat()
                }
                self._embeddings[sample_id] = embedding
                updated += 1
                logger.debug(f"更新向量: {sample_id}")
                
            except Exception as e:
                logger.warning(f"向量化失败 {sample_id}: {e}")
        
        self.save()
        return updated
    
    def get_embedding(self, sample_id: str) -> Optional[List[float]]:
        """获取指定样本的向量"""
        if not self._loaded:
            self.load()
        return self._embeddings.get(sample_id)
    
    def get_all_embeddings(self) -> Dict[str, List[float]]:
        """获取所有已缓存的向量"""
        if not self._loaded:
            self.load()
        return self._embeddings.copy()
    
    def get_stats(self) -> Dict:
        """获取缓存统计信息"""
        if not self._loaded:
            self.load()
        
        return {
            "total_documents": len(self._embeddings),
            "cache_file": str(self.cache_file),
            "cache_exists": self.cache_file.exists(),
            "cache_size_kb": self.cache_file.stat().st_size / 1024 if self.cache_file.exists() else 0,
            "updated_at": self._cache.get("updated_at", "未知")
        }


# 全局缓存实例
_vector_cache: Optional[VectorCache] = None


def get_vector_cache() -> VectorCache:
    """获取全局向量缓存实例"""
    global _vector_cache
    if _vector_cache is None:
        _vector_cache = VectorCache()
    return _vector_cache


def build_vector_cache(embedding_service, force: bool = False) -> int:
    """便捷函数：构建向量缓存"""
    cache = get_vector_cache()
    return cache.build_cache(embedding_service, force_rebuild=force)


if __name__ == '__main__':
    print("向量缓存模块")
    print("=" * 60)
    
    cache = get_vector_cache()
    cache.load()
    
    stats = cache.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    summaries = cache.get_all_summaries()
    print(f"\n可检索样本数: {len(summaries)}")
    
    to_update, to_delete = cache.check_updates(summaries)
    print(f"需要更新: {len(to_update)}")
    print(f"需要删除: {len(to_delete)}")
