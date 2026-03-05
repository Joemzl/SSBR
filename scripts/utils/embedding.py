"""
Embedding API 封装
用于文本向量化，支持错误处理和降级逻辑

Created: 2026-03-05

支持的环境变量:
- OPENAI_API_KEY: API 密钥 (必需)
- OPENAI_BASE_URL: API 代理地址 (可选，如 https://api.uiuiapi.com/v1)

配置方式:
1. 环境变量: export OPENAI_API_KEY=xxx
2. .env 文件: 在项目根目录创建 .env 文件
"""

import os
import time
from typing import List, Optional
import logging
from pathlib import Path

# 尝试加载 .env 文件
def _load_dotenv():
    """从项目根目录加载 .env 文件"""
    try:
        # 查找项目根目录 (包含 dataset 目录的父目录)
        current = Path(__file__).resolve()
        for parent in [current] + list(current.parents):
            env_file = parent / '.env'
            if env_file.exists():
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key and value and key not in os.environ:
                                os.environ[key] = value
                return True
    except Exception:
        pass
    return False

_load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    OpenAI Embedding API 封装
    
    使用 text-embedding-3-small 模型 (1536 维)
    """
    
    MODEL = "text-embedding-3-small"
    DIMENSION = 1536
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # 秒
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化 Embedding 服务
        
        Args:
            api_key: OpenAI API Key，默认从环境变量 OPENAI_API_KEY 获取
            base_url: API Base URL，默认从环境变量 OPENAI_BASE_URL 获取
                     支持代理 API 如 UiUiAPI: https://api.uiuiapi.com/v1
        """
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.base_url = base_url or os.environ.get('OPENAI_BASE_URL')
        
        if not self.api_key:
            logger.warning("未设置 OPENAI_API_KEY，Embedding 功能将不可用")
        
        if self.base_url:
            logger.info(f"使用代理 API: {self.base_url}")
        
        self._client = None
    
    @property
    def client(self):
        """延迟初始化 OpenAI 客户端"""
        if self._client is None:
            try:
                from openai import OpenAI
                # 支持代理 API (如 UiUiAPI)
                client_kwargs = {"api_key": self.api_key}
                if self.base_url:
                    client_kwargs["base_url"] = self.base_url
                self._client = OpenAI(**client_kwargs)
            except ImportError:
                raise ImportError("请安装 openai 库: pip install openai")
        return self._client
    
    def embed(self, text: str) -> List[float]:
        """
        将文本转换为向量
        
        Args:
            text: 待向量化的文本
            
        Returns:
            1536 维浮点数向量
            
        Raises:
            EmbeddingError: API 调用失败时抛出
        """
        if not self.api_key:
            raise EmbeddingError("未配置 API Key")
        
        if not text or not text.strip():
            raise ValueError("文本不能为空")
        
        # 截断过长文本 (OpenAI 限制约 8191 tokens)
        text = text[:30000]  # 粗略截断
        
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.client.embeddings.create(
                    model=self.MODEL,
                    input=text
                )
                return response.data[0].embedding
            
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                # 判断错误类型
                if 'rate limit' in error_msg:
                    logger.warning(f"API 配额限制，等待 {self.RETRY_DELAY * (attempt + 1)} 秒后重试...")
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                    continue
                
                elif 'timeout' in error_msg or 'connection' in error_msg:
                    logger.warning(f"网络错误，等待 {self.RETRY_DELAY} 秒后重试...")
                    time.sleep(self.RETRY_DELAY)
                    continue
                
                else:
                    # 其他错误直接抛出
                    raise EmbeddingError(f"Embedding API 错误: {e}")
        
        raise EmbeddingError(f"重试 {self.MAX_RETRIES} 次后仍然失败: {last_error}")
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        批量向量化
        
        Args:
            texts: 文本列表
            
        Returns:
            向量列表
        """
        if not self.api_key:
            raise EmbeddingError("未配置 API Key")
        
        if not texts:
            return []
        
        # 过滤空文本
        valid_texts = [t[:30000] for t in texts if t and t.strip()]
        
        if not valid_texts:
            return []
        
        try:
            response = self.client.embeddings.create(
                model=self.MODEL,
                input=valid_texts
            )
            return [item.embedding for item in response.data]
        
        except Exception as e:
            raise EmbeddingError(f"批量 Embedding 错误: {e}")
    
    def is_available(self) -> bool:
        """
        检查 Embedding 服务是否可用
        
        Returns:
            True 如果服务可用
        """
        if not self.api_key:
            return False
        
        try:
            # 用最短文本测试
            self.embed("test")
            return True
        except Exception:
            return False


class EmbeddingError(Exception):
    """Embedding 服务错误"""
    pass


def get_embedding_service(api_key: Optional[str] = None) -> EmbeddingService:
    """
    获取 Embedding 服务实例
    
    Args:
        api_key: 可选的 API Key
        
    Returns:
        EmbeddingService 实例
    """
    return EmbeddingService(api_key)


# 便捷函数
def embed_text(text: str, api_key: Optional[str] = None) -> List[float]:
    """
    便捷函数：向量化单个文本
    
    Args:
        text: 文本
        api_key: 可选的 API Key
        
    Returns:
        向量
    """
    service = get_embedding_service(api_key)
    return service.embed(text)


if __name__ == '__main__':
    print("EmbeddingService 模块")
    print("="*50)
    print(f"模型: {EmbeddingService.MODEL}")
    print(f"向量维度: {EmbeddingService.DIMENSION}")
    print(f"最大重试次数: {EmbeddingService.MAX_RETRIES}")
    print()
    print("使用方法:")
    print("  service = EmbeddingService()")
    print("  vector = service.embed('文本内容')")
    print()
    print("或使用便捷函数:")
    print("  vector = embed_text('文本内容')")
