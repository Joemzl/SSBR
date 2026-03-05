"""
查询预处理器
用于处理 RAG 查询的预处理逻辑

Created: 2026-03-05
Task: T028.1
"""

import re
from typing import Tuple, Optional


# 配置常量
MAX_QUERY_LENGTH = 500  # 最大查询长度（字符）
MIN_QUERY_LENGTH = 2    # 最小查询长度（字符）


def preprocess_query(query: str) -> Tuple[str, Optional[str]]:
    """
    预处理用户查询
    
    处理逻辑:
    1. 空白检测：去除首尾空白，检查是否为空
    2. 长度限制：超过 500 字符时截断
    3. 特殊字符处理：移除控制字符，保留中英文标点
    
    Args:
        query: 原始用户查询
        
    Returns:
        (处理后的查询, 警告消息或 None)
        
    Raises:
        ValueError: 查询为空或过短时抛出
    """
    warning = None
    
    # 1. 空白检测
    if query is None:
        raise ValueError("查询不能为 None")
    
    query = query.strip()
    
    if not query:
        raise ValueError("查询不能为空")
    
    if len(query) < MIN_QUERY_LENGTH:
        raise ValueError(f"查询过短（至少 {MIN_QUERY_LENGTH} 个字符）")
    
    # 2. 特殊字符处理
    # 移除控制字符（保留换行和制表符以支持多行查询）
    query = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', query)
    
    # 规范化空白字符
    query = re.sub(r'\s+', ' ', query)
    query = query.strip()
    
    # 3. 长度限制
    if len(query) > MAX_QUERY_LENGTH:
        query = query[:MAX_QUERY_LENGTH]
        warning = f"查询已截断至 {MAX_QUERY_LENGTH} 字符"
    
    return query, warning


def is_valid_query(query: str) -> Tuple[bool, Optional[str]]:
    """
    检查查询是否有效
    
    Args:
        query: 用户查询
        
    Returns:
        (是否有效, 错误消息或 None)
    """
    try:
        preprocess_query(query)
        return True, None
    except ValueError as e:
        return False, str(e)


def extract_keywords(query: str) -> list[str]:
    """
    从查询中提取关键词
    
    用于辅助分析和日志记录，不影响实际查询处理
    
    Args:
        query: 预处理后的查询
        
    Returns:
        关键词列表
    """
    # 移除常见停用词（简化版）
    stopwords = {
        '的', '是', '在', '和', '有', '我', '你', '他', '她', '它',
        '这', '那', '什么', '怎么', '如何', '需要', '想要', '可以',
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be',
        'to', 'of', 'and', 'in', 'for', 'on', 'with'
    }
    
    # 分词（简单的中英文混合分词）
    # 对于更复杂的需求，可以使用 jieba 等分词库
    words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', query)
    
    # 过滤停用词和单字符
    keywords = [w for w in words if w.lower() not in stopwords and len(w) > 1]
    
    return keywords


def format_query_for_logging(query: str, max_display: int = 100) -> str:
    """
    格式化查询用于日志记录
    
    Args:
        query: 查询内容
        max_display: 最大显示长度
        
    Returns:
        格式化后的查询字符串
    """
    if len(query) <= max_display:
        return query
    return query[:max_display] + f"... (共 {len(query)} 字符)"


class QueryPreprocessor:
    """
    查询预处理器类
    
    提供更灵活的配置和批量处理能力
    """
    
    def __init__(
        self,
        max_length: int = MAX_QUERY_LENGTH,
        min_length: int = MIN_QUERY_LENGTH
    ):
        """
        初始化预处理器
        
        Args:
            max_length: 最大查询长度
            min_length: 最小查询长度
        """
        self.max_length = max_length
        self.min_length = min_length
    
    def process(self, query: str) -> Tuple[str, Optional[str]]:
        """处理查询"""
        warning = None
        
        if query is None:
            raise ValueError("查询不能为 None")
        
        query = query.strip()
        
        if not query:
            raise ValueError("查询不能为空")
        
        if len(query) < self.min_length:
            raise ValueError(f"查询过短（至少 {self.min_length} 个字符）")
        
        # 特殊字符处理
        query = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', query)
        query = re.sub(r'\s+', ' ', query).strip()
        
        # 长度限制
        if len(query) > self.max_length:
            query = query[:self.max_length]
            warning = f"查询已截断至 {self.max_length} 字符"
        
        return query, warning
    
    def is_valid(self, query: str) -> bool:
        """检查查询是否有效"""
        try:
            self.process(query)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    # 测试
    print("查询预处理器测试")
    print("=" * 50)
    
    test_cases = [
        "我需要改善白炭黑分散性",
        "   空白测试   ",
        "",
        "ab",  # 边界长度
        "a" * 600,  # 超长
        "特殊字符\x00测试\x1f结束",
    ]
    
    for query in test_cases:
        print(f"\n输入: {repr(query[:50])}...")
        try:
            result, warning = preprocess_query(query)
            print(f"  输出: {result[:50]}...")
            if warning:
                print(f"  警告: {warning}")
            print(f"  关键词: {extract_keywords(result)}")
        except ValueError as e:
            print(f"  错误: {e}")
