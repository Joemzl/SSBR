"""
统一 LLM 客户端模块

支持多模型提供商，自动降级策略：
1. Claude 3.5 Sonnet (优先)
2. GPT-4o-mini (降级)

环境变量配置：
- ANTHROPIC_API_KEY: Claude API 密钥 (可选，优先使用)
- OPENAI_API_KEY: OpenAI API 密钥 (必需，用于降级和 Embedding)
- CLAUDE_MODEL: Claude 模型名称 (默认 claude-sonnet-4-20250514)
- OPENAI_MODEL: OpenAI 模型名称 (默认 gpt-4o-mini)
- LLM_ENABLE_FALLBACK: 是否启用降级 (默认 true)
"""

import os
import logging
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """LLM 提供商"""
    CLAUDE = "claude"
    OPENAI = "openai"


@dataclass
class LLMConfig:
    """LLM 配置"""
    # Claude 配置
    claude_model: str = "claude-sonnet-4-20250514"
    claude_api_key: Optional[str] = None
    
    # OpenAI 配置 (降级)
    openai_model: str = "gpt-4o-mini"
    openai_api_key: Optional[str] = None
    
    # 通用配置
    max_tokens: int = 800
    temperature: float = 0.3
    timeout: float = 30.0
    
    # 降级策略
    enable_fallback: bool = True  # 是否启用降级
    
    @classmethod
    def from_env(cls) -> "LLMConfig":
        """从环境变量加载配置"""
        return cls(
            claude_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            claude_model=os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-20250514"),
            openai_model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            max_tokens=int(os.environ.get("QA_MAX_TOKENS", "800")),
            enable_fallback=os.environ.get("LLM_ENABLE_FALLBACK", "true").lower() == "true",
        )


class UnifiedLLMClient:
    """
    统一 LLM 客户端
    
    使用策略:
    1. 如果配置了 ANTHROPIC_API_KEY → 尝试 Claude
    2. Claude 失败 + enable_fallback → 降级到 OpenAI
    3. 没有 Claude Key → 直接使用 OpenAI
    
    Usage:
        client = UnifiedLLMClient()
        response, provider = client.chat(
            system_prompt="你是专家...",
            user_prompt="用户问题..."
        )
        print(f"使用 {provider.value} 生成回答")
    """
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        初始化统一 LLM 客户端
        
        Args:
            config: LLM 配置，默认从环境变量加载
        """
        self.config = config or LLMConfig.from_env()
        self._claude_client = None
        self._openai_client = None
        self._last_provider: Optional[LLMProvider] = None
        self._fallback_used: bool = False
        self._fallback_reason: Optional[str] = None
    
    def _get_claude_client(self):
        """获取 Claude 客户端（延迟初始化）"""
        if self._claude_client is None and self.config.claude_api_key:
            try:
                from anthropic import Anthropic
                self._claude_client = Anthropic(
                    api_key=self.config.claude_api_key,
                    timeout=self.config.timeout
                )
                logger.debug("Claude 客户端初始化成功")
            except ImportError:
                logger.warning("anthropic 包未安装，无法使用 Claude。安装: pip install anthropic>=0.18.0")
                return None
            except Exception as e:
                logger.warning(f"Claude 客户端初始化失败: {e}")
                return None
        return self._claude_client
    
    def _get_openai_client(self):
        """获取 OpenAI 客户端（延迟初始化）"""
        if self._openai_client is None:
            if not self.config.openai_api_key:
                raise RuntimeError("OpenAI 客户端不可用，请设置 OPENAI_API_KEY 环境变量")
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(
                    api_key=self.config.openai_api_key,
                    timeout=self.config.timeout
                )
                logger.debug("OpenAI 客户端初始化成功")
            except ImportError:
                raise ImportError("openai 包未安装。安装: pip install openai>=1.0.0")
        return self._openai_client
    
    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> Tuple[str, LLMProvider]:
        """
        发送聊天请求，自动处理降级
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
        
        Returns:
            tuple[回答文本, 使用的提供商]
        
        Raises:
            RuntimeError: 所有提供商都不可用时抛出
        """
        # 重置降级状态
        self._fallback_used = False
        self._fallback_reason = None
        
        # 策略1: 尝试 Claude (如果配置了)
        if self.config.claude_api_key:
            try:
                response = self._call_claude(system_prompt, user_prompt)
                self._last_provider = LLMProvider.CLAUDE
                logger.info(f"✅ 使用 Claude ({self.config.claude_model}) 生成回答")
                return response, LLMProvider.CLAUDE
            except Exception as e:
                error_msg = str(e)[:200]
                logger.warning(f"⚠️ Claude 调用失败: {error_msg}")
                
                if not self.config.enable_fallback:
                    raise RuntimeError(f"Claude 调用失败且降级已禁用: {error_msg}")
                
                # 记录降级原因（后台日志，用户不可见）
                self._fallback_used = True
                self._fallback_reason = error_msg
                logger.info(f"🔄 触发降级策略: Claude → OpenAI (原因: {error_msg})")
        
        # 策略2: 使用 OpenAI (降级或默认)
        try:
            response = self._call_openai(system_prompt, user_prompt)
            self._last_provider = LLMProvider.OPENAI
            
            if self._fallback_used:
                logger.info(f"✅ 降级成功，使用 OpenAI ({self.config.openai_model}) 生成回答")
            else:
                logger.info(f"✅ 使用 OpenAI ({self.config.openai_model}) 生成回答")
            
            return response, LLMProvider.OPENAI
        except Exception as e:
            error_msg = str(e)[:200]
            logger.error(f"❌ OpenAI 调用也失败: {error_msg}")
            raise RuntimeError(f"所有 LLM 提供商都不可用: {error_msg}")
    
    def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        """
        调用 Claude API
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
        
        Returns:
            生成的回答文本
        """
        client = self._get_claude_client()
        if not client:
            raise RuntimeError("Claude 客户端不可用")
        
        response = client.messages.create(
            model=self.config.claude_model,
            max_tokens=self.config.max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        # 提取文本内容
        if response.content and len(response.content) > 0:
            return response.content[0].text
        else:
            raise RuntimeError("Claude 返回空响应")
    
    def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """
        调用 OpenAI API
        
        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
        
        Returns:
            生成的回答文本
        """
        client = self._get_openai_client()
        
        response = client.chat.completions.create(
            model=self.config.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature
        )
        
        content = response.choices[0].message.content
        if content:
            return content.strip()
        else:
            raise RuntimeError("OpenAI 返回空响应")
    
    @property
    def last_provider(self) -> Optional[LLMProvider]:
        """获取上次使用的提供商"""
        return self._last_provider
    
    @property
    def fallback_used(self) -> bool:
        """是否触发了降级"""
        return self._fallback_used
    
    @property
    def fallback_reason(self) -> Optional[str]:
        """降级原因（仅后台日志用）"""
        return self._fallback_reason
    
    def get_model_name(self) -> str:
        """获取当前使用的模型名称"""
        if self._last_provider == LLMProvider.CLAUDE:
            return self.config.claude_model
        elif self._last_provider == LLMProvider.OPENAI:
            return self.config.openai_model
        else:
            return "unknown"


# =============================================================================
# 单例模式
# =============================================================================

_client_instance: Optional[UnifiedLLMClient] = None


def get_llm_client(config: Optional[LLMConfig] = None) -> UnifiedLLMClient:
    """
    获取单例 LLM 客户端
    
    Args:
        config: 可选配置，仅在首次调用时生效
    
    Returns:
        UnifiedLLMClient 实例
    """
    global _client_instance
    
    if _client_instance is None:
        _client_instance = UnifiedLLMClient(config)
    
    return _client_instance


def reset_llm_client():
    """重置单例客户端（用于测试）"""
    global _client_instance
    _client_instance = None


# =============================================================================
# CLI 测试
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    parser = argparse.ArgumentParser(description="LLM Client 测试工具")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--prompt", type=str, default="你好，请用一句话介绍 SSBR 橡胶",
                        help="测试提示词")
    
    args = parser.parse_args()
    
    if args.test:
        print("=" * 60)
        print("LLM Client Test")
        print("=" * 60)
        
        # 显示配置
        config = LLMConfig.from_env()
        print(f"\n[Config]")
        print(f"   Claude API Key: {'Configured' if config.claude_api_key else 'Not configured'}")
        print(f"   Claude Model: {config.claude_model}")
        print(f"   OpenAI API Key: {'Configured' if config.openai_api_key else 'Not configured'}")
        print(f"   OpenAI Model: {config.openai_model}")
        print(f"   Fallback: {'Enabled' if config.enable_fallback else 'Disabled'}")
        
        # 测试调用
        print(f"\n[Test Prompt] {args.prompt}")
        print("-" * 60)
        
        try:
            client = UnifiedLLMClient(config)
            response, provider = client.chat(
                system_prompt="你是一位高分子材料专家，请简洁回答。",
                user_prompt=args.prompt
            )
            
            print(f"\n[Response] ({provider.value}):")
            print(response)
            print("-" * 60)
            
            if client.fallback_used:
                print(f"\n[Warning] Fallback triggered: {client.fallback_reason}")
            
            print(f"\n[OK] Test completed, model used: {client.get_model_name()}")
            
        except Exception as e:
            print(f"\n[Error] Test failed: {e}")
    else:
        parser.print_help()
