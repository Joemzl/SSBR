"""
Exception Classes for RAG QA System

This module defines custom exceptions for the QA system,
following the error codes defined in contracts/qa-api.md.
"""


class QAError(Exception):
    """Base exception for QA system errors."""
    
    def __init__(self, message: str, code: str = "QA000"):
        self.message = message
        self.code = code
        super().__init__(f"[{code}] {message}")


class EmptyQueryError(QAError):
    """Raised when query is empty or whitespace only."""
    
    def __init__(self, message: str = "查询为空"):
        super().__init__(message, code="QA001")


class QueryTooLongError(QAError):
    """Raised when query exceeds maximum length."""
    
    def __init__(self, length: int, max_length: int = 1000):
        message = f"查询超过 {max_length} 字符（当前: {length}）"
        super().__init__(message, code="QA002")


class EmbeddingError(QAError):
    """Raised when embedding API call fails."""
    
    def __init__(self, message: str = "Embedding API 调用失败", original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message, code="QA003")


class RerankError(QAError):
    """Raised when reranking model fails."""
    
    def __init__(self, message: str = "重排模型加载或推理失败", original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message, code="QA004")


class GenerationError(QAError):
    """Raised when LLM API call fails (Claude or OpenAI)."""
    
    def __init__(self, message: str = "LLM API 调用失败", original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message, code="QA005")


class NoSamplesError(QAError):
    """Raised when no samples are available for search."""
    
    def __init__(self, message: str = "没有可检索的样本"):
        super().__init__(message, code="QA006")


class InvalidSampleError(QAError):
    """Raised when sample data is invalid or corrupted."""
    
    def __init__(self, sample_id: str, reason: str = "数据无效"):
        message = f"样本 {sample_id} {reason}"
        super().__init__(message, code="QA007")


class CacheError(QAError):
    """Raised when cache operations fail."""
    
    def __init__(self, message: str = "缓存操作失败", original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message, code="QA008")


class TimeoutError(QAError):
    """Raised when operation exceeds timeout."""
    
    def __init__(self, operation: str, timeout_seconds: float):
        message = f"{operation} 超时（{timeout_seconds}秒）"
        super().__init__(message, code="QA009")


# =============================================================================
# Synthesis Module Exceptions (004-multi-literature-synthesis)
# =============================================================================

class InsufficientDataError(QAError):
    """
    数据不足错误（FR-005）。
    
    当相关样本数量不满足最小要求时抛出。
    """
    
    def __init__(self, required: int, actual: int, operation: str):
        self.required = required
        self.actual = actual
        self.operation = operation
        message = f"{operation}需要至少 {required} 个相关样本，当前仅找到 {actual} 个"
        super().__init__(message, code="QA010")


class ExtrapolationBoundaryError(QAError):
    """
    外推边界错误（FR-005）。
    
    当查询值超出允许的外推范围时抛出。
    """
    
    def __init__(self, query_value: float, allowed_range: tuple, unit: str):
        self.query_value = query_value
        self.allowed_range = allowed_range
        self.unit = unit
        message = (
            f"查询值 {query_value} {unit} 超出允许的外推范围 "
            f"[{allowed_range[0]:.1f}, {allowed_range[1]:.1f}] {unit}"
        )
        super().__init__(message, code="QA011")


class ConflictingTargetsError(QAError):
    """
    目标冲突错误（FR-008）。
    
    当用户指定的目标性能存在内在矛盾时抛出。
    """
    
    def __init__(self, conflicts: list, suggestion: str):
        self.conflicts = conflicts
        self.suggestion = suggestion
        conflict_str = ", ".join(f"{a} vs {b}" for a, b in conflicts)
        message = f"目标性能存在冲突: {conflict_str}。建议: {suggestion}"
        super().__init__(message, code="QA012")


# =============================================================================
# Error Handling Utilities
# =============================================================================

def handle_generation_error(error: Exception) -> str:
    """
    Generate a fallback message when LLM generation fails.
    
    Args:
        error: The original exception
    
    Returns:
        A user-friendly fallback message
    """
    return """## ⚠️ 生成回答时遇到问题

抱歉，AI 回答生成暂时不可用。请查看下方的推荐样本列表获取相关信息。

**错误信息**: {}

**建议**:
- 稍后重试
- 直接查看推荐样本的详细信息
- 尝试简化您的查询""".format(str(error)[:100])


def is_retriable_error(error: QAError) -> bool:
    """
    Check if the error is potentially retriable.
    
    Args:
        error: The QA error to check
    
    Returns:
        True if the operation could be retried
    """
    retriable_codes = {"QA003", "QA004", "QA005", "QA009"}
    return error.code in retriable_codes
