"""
YAML Front Matter 解析工具
用于解析 Markdown 文件中的 YAML front matter

Created: 2026-03-05
"""

import re
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


def parse_yaml_frontmatter(content: str) -> Dict[str, Any]:
    """
    提取 Markdown 文件的 YAML front matter
    
    Args:
        content: Markdown 文件的完整内容
        
    Returns:
        解析后的 YAML 字典，如果没有 front matter 则返回空字典
        
    Example:
        >>> content = '''---
        ... sample_id: SSBR-001
        ... interpretation_type: mechanical
        ... ---
        ... # Content'''
        >>> parse_yaml_frontmatter(content)
        {'sample_id': 'SSBR-001', 'interpretation_type': 'mechanical'}
    """
    # 匹配 YAML front matter: 以 --- 开头和结尾
    pattern = r'^---\s*\n(.*?)\n---\s*\n?'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        yaml_content = match.group(1)
        try:
            return yaml.safe_load(yaml_content) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"YAML 解析错误: {e}")
    
    return {}


def extract_yaml_data(content: str, keys: list[str]) -> Dict[str, Any]:
    """
    从 YAML front matter 中提取指定字段
    
    Args:
        content: Markdown 文件内容
        keys: 需要提取的字段列表，支持点号分隔的嵌套路径
        
    Returns:
        包含指定字段的字典
        
    Example:
        >>> extract_yaml_data(content, ['sample_id', 'data.stress_100.value'])
        {'sample_id': 'SSBR-001', 'data.stress_100.value': 1.5}
    """
    yaml_data = parse_yaml_frontmatter(content)
    result = {}
    
    for key in keys:
        value = get_nested_value(yaml_data, key)
        result[key] = value
    
    return result


def get_nested_value(data: Dict[str, Any], key_path: str) -> Any:
    """
    获取嵌套字典中的值
    
    Args:
        data: 字典数据
        key_path: 点号分隔的键路径，如 'data.stress_100.value'
        
    Returns:
        对应的值，如果路径不存在则返回 None
    """
    keys = key_path.split('.')
    current = data
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    
    return current


def extract_markdown_body(content: str) -> str:
    """
    提取 Markdown 文件的正文内容（去除 YAML front matter）
    
    Args:
        content: Markdown 文件的完整内容
        
    Returns:
        去除 front matter 后的正文内容
    """
    pattern = r'^---\s*\n.*?\n---\s*\n?'
    return re.sub(pattern, '', content, count=1, flags=re.DOTALL).strip()


def read_interpretation_file(file_path: Path | str) -> Dict[str, Any]:
    """
    读取解读文档文件并解析
    
    Args:
        file_path: 文件路径
        
    Returns:
        包含 'yaml' (解析的 YAML 数据) 和 'body' (Markdown 正文) 的字典
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    
    content = path.read_text(encoding='utf-8')
    
    return {
        'yaml': parse_yaml_frontmatter(content),
        'body': extract_markdown_body(content),
        'path': str(path)
    }


def write_interpretation_file(
    file_path: Path | str,
    yaml_data: Dict[str, Any],
    markdown_body: str
) -> None:
    """
    写入解读文档文件
    
    Args:
        file_path: 文件路径
        yaml_data: YAML front matter 数据
        markdown_body: Markdown 正文内容
    """
    path = Path(file_path)
    
    # 确保父目录存在
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # 构建文件内容
    yaml_str = yaml.dump(yaml_data, allow_unicode=True, default_flow_style=False, sort_keys=False)
    content = f"---\n{yaml_str}---\n\n{markdown_body}"
    
    path.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    # 简单测试
    test_content = """---
sample_id: SSBR-001
interpretation_type: mechanical
data:
  stress_100:
    value: 1.5
    unit: MPa
---

# 力学性能解读

## 核心发现
测试内容
"""
    
    print("解析结果:")
    result = parse_yaml_frontmatter(test_content)
    print(f"  sample_id: {result.get('sample_id')}")
    print(f"  type: {result.get('interpretation_type')}")
    print(f"  stress_100: {result.get('data', {}).get('stress_100', {}).get('value')}")
    
    print("\n正文内容:")
    body = extract_markdown_body(test_content)
    print(f"  {body[:50]}...")
