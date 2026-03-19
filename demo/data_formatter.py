"""
数据格式化模块
将内部数据转换为用户友好的展示格式

功能：
- 隐藏样本 ID，使用官能团名称标识
- 转换相似度为匹配度（高/中/低）
- 简化文献来源格式
- 提取核心性能指标
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class FriendlyResult:
    """用户友好的推荐结果"""
    index: int                    # 方案编号 (1, 2, 3...)
    functional_group: str         # 官能团名称 (如 "硅烷官能化")
    reagent: str                  # 官能化试剂
    degree: str                   # 官能化程度
    match_level: str              # 匹配度 (高/中/低)
    summary: str                  # 一句话总结
    key_features: List[str]       # 核心性能特点
    metrics: Dict[str, str]       # 关键指标
    application: List[str]        # 适用场景
    source: str                   # 简化文献来源
    recommendation: str           # 推荐理由
    
    # 内部使用，不对外展示
    _internal_id: str = ""
    _similarity: float = 0.0


def parse_summary_content(content: str) -> Dict[str, Any]:
    """
    解析 summary.md 内容，提取关键信息
    
    Args:
        content: summary.md 的原始内容
        
    Returns:
        提取的结构化数据
    """
    result = {
        "functional_group": "未知官能化",
        "reagent": "未知",
        "degree": "未知",
        "summary": "",
        "key_features": [],
        "metrics": {},
        "application": [],
        "source": "未知来源"
    }
    
    # 提取官能化信息
    # 支持两种格式：
    # 1. **核心官能团**: 羧基 (-COOH)
    # 2. - **核心官能团**: 羧基（-COOH）
    fg_match = re.search(r'[-\s]*\*\*核心官能团\*\*:\s*(.+?)(?:\s*[（(]|$|\n)', content)
    if fg_match:
        fg_name = fg_match.group(1).strip()
        if fg_name and fg_name != '-' and fg_name != '- (-)':
            result["functional_group"] = fg_name + "官能化"
        else:
            result["functional_group"] = "未官能化（空白对照）"
    
    # 官能化试剂
    # 支持 "- **官能化试剂**: ..." 格式
    reagent_match = re.search(r'[-\s]*\*\*官能化试剂\*\*:\s*(.+?)(?:\n|$)', content)
    if reagent_match:
        reagent = reagent_match.group(1).strip()
        if "无" in reagent or "空白" in reagent:
            result["reagent"] = "无（空白对照）"
        else:
            result["reagent"] = reagent
    
    # 官能化程度
    # 支持 "- **官能化程度**: 8.7 wt%" 格式
    degree_match = re.search(r'[-\s]*\*\*官能化程度\*\*:\s*([\d.]+)\s*wt%', content)
    if degree_match:
        result["degree"] = f"{degree_match.group(1)} wt%"
    else:
        result["degree"] = "N/A"
    
    # 一句话总结
    summary_match = re.search(r'## 一句话总结\s*\n+(.+?)(?:\n---|\n##)', content, re.DOTALL)
    if summary_match:
        summary = summary_match.group(1).strip()
        # 移除可能的样本 ID
        summary = re.sub(r'SSBR-\d+', '', summary).strip()
        result["summary"] = summary if summary else "高性能官能化 SSBR 材料"
    
    # 核心性能特点
    features_section = re.search(r'## 核心性能特点\s*\n(.+?)(?:\n---|\n## 适用场景)', content, re.DOTALL)
    if features_section:
        features_text = features_section.group(1)
        # 提取每个特点标题和评价
        feature_matches = re.findall(r'###\s*(.+?)\s*【(.+?)】\s*\n+(.+?)(?=\n###|\n---|\Z)', features_text, re.DOTALL)
        for title, rating, desc in feature_matches:
            desc_clean = desc.strip()
            if desc_clean and "暂无" not in desc_clean:
                result["key_features"].append({
                    "title": title.strip(),
                    "rating": rating.strip(),
                    "description": desc_clean
                })
    
    # 关键性能指标（从表格提取）
    metrics_section = re.search(r'## 关键性能指标\s*\n(.+?)(?:\n---|\n##)', content, re.DOTALL)
    if metrics_section:
        table_text = metrics_section.group(1)
        # 解析表格行
        rows = re.findall(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|', table_text)
        for row in rows:
            if len(row) >= 4:
                category, metric, value, unit = row[0], row[1], row[2], row[3]
                # 跳过表头和无效值
                if metric in ['指标', '---'] or value in ['-', '---', '']:
                    continue
                if value.strip() and value.strip() != '-':
                    result["metrics"][metric.strip()] = f"{value.strip()} {unit.strip()}".strip()
    
    # 适用场景
    app_section = re.search(r'## 适用场景\s*\n(.+?)(?:\n---|\n##)', content, re.DOTALL)
    if app_section:
        app_text = app_section.group(1)
        # 提取 ✅ 开头的场景
        apps = re.findall(r'[✅⚠️]\s*(.+)', app_text)
        result["application"] = [app.strip() for app in apps if app.strip()]
    
    # 文献来源
    # 从 DOI 和引文中提取
    doi_match = re.search(r'\*\*DOI\*\*:\s*(.+?)(?:\n|$)', content)
    cite_match = re.search(r'\*\*引文\*\*:\s*(.+?)(?:\n|$)', content)
    
    if cite_match:
        cite_text = cite_match.group(1).strip()
        # 尝试提取期刊和年份，格式如 "RSC Adv., 2019, 9, 18888-18897"
        journal_year_match = re.search(r'([A-Za-z\s\.]+),\s*(\d{4})', cite_text)
        if journal_year_match:
            journal = journal_year_match.group(1).strip().rstrip(',.')
            year = journal_year_match.group(2)
            result["source"] = f"{journal}, {year}"
        else:
            result["source"] = cite_text[:50]  # 截取前50字符
    elif doi_match:
        result["source"] = f"DOI: {doi_match.group(1).strip()}"
    
    return result


def similarity_to_match_level(similarity: float) -> str:
    """
    将相似度转换为用户友好的匹配度
    
    Args:
        similarity: 相似度分数 (0-1)
        
    Returns:
        匹配度描述 (高/中/低)
    """
    if similarity >= 0.7:
        return "高"
    elif similarity >= 0.5:
        return "中"
    else:
        return "低"


def generate_recommendation(parsed_data: Dict[str, Any], query: str) -> str:
    """
    根据数据和查询生成推荐理由
    
    Args:
        parsed_data: 解析后的数据
        query: 用户查询
        
    Returns:
        推荐理由文本
    """
    fg = parsed_data.get("functional_group", "")
    features = parsed_data.get("key_features", [])
    metrics = parsed_data.get("metrics", {})
    
    reasons = []
    
    # 根据官能团类型给出基础推荐
    if "硅烷" in fg or "硅氧烷" in fg:
        reasons.append("硅烷基团可与白炭黑形成共价键，显著提升界面结合强度")
    elif "羧基" in fg:
        reasons.append("羧基可与白炭黑表面形成强氢键，改善分散性")
    elif "羟基" in fg:
        reasons.append("羟基提供基础的界面相互作用")
    elif "氨基" in fg:
        reasons.append("氨基可提供多种界面相互作用模式")
    elif "空白" in fg or "未官能化" in fg:
        reasons.append("可作为基准对照，评估官能化改性效果")
    
    # 根据性能特点补充
    for feature in features[:2]:  # 最多取2个
        if feature.get("rating") in ["优秀", "良好"]:
            reasons.append(feature.get("description", "")[:50])
    
    return "；".join(reasons[:2]) if reasons else "该方案与您的需求相关"


def format_result_for_display(
    sample_id: str,
    similarity: float,
    summary_content: str,
    index: int,
    query: str = ""
) -> FriendlyResult:
    """
    将原始搜索结果转换为用户友好格式
    
    Args:
        sample_id: 内部样本 ID
        similarity: 相似度分数
        summary_content: summary.md 内容
        index: 方案编号
        query: 用户查询（用于生成推荐理由）
        
    Returns:
        FriendlyResult 对象
    """
    parsed = parse_summary_content(summary_content)
    
    return FriendlyResult(
        index=index,
        functional_group=parsed["functional_group"],
        reagent=parsed["reagent"],
        degree=parsed["degree"],
        match_level=similarity_to_match_level(similarity),
        summary=parsed["summary"],
        key_features=[f.get("description", "") for f in parsed.get("key_features", [])],
        metrics=parsed["metrics"],
        application=parsed["application"],
        source=parsed["source"],
        recommendation=generate_recommendation(parsed, query),
        _internal_id=sample_id,
        _similarity=similarity
    )


def format_results_as_markdown(results: List[FriendlyResult], query: str) -> str:
    """
    将推荐结果格式化为 Markdown 展示
    
    Args:
        results: FriendlyResult 列表
        query: 用户查询
        
    Returns:
        格式化的 Markdown 字符串
    """
    if not results:
        return "### 未找到相关方案\n\n请尝试更换关键词或调整查询条件。"
    
    lines = []
    
    # 检查是否全部为低匹配度
    all_low = all(r.match_level == "低" for r in results)
    if all_low:
        lines.append("> 💡 **提示**: 当前知识库中暂无高度匹配的方案，以下结果供参考\n")
    
    for r in results:
        # 匹配度 emoji
        match_emoji = {"高": "🟢", "中": "🟡", "低": "🔵"}.get(r.match_level, "⚪")
        
        lines.append(f"### 方案 {r.index}: {r.functional_group} {match_emoji}")
        lines.append(f"**匹配度**: {r.match_level}\n")
        
        # 官能化信息
        lines.append("**官能化信息**")
        lines.append(f"- 试剂: {r.reagent}")
        lines.append(f"- 程度: {r.degree}\n")
        
        # 推荐理由
        if r.recommendation:
            lines.append(f"**推荐理由**: {r.recommendation}\n")
        
        lines.append("---\n")
    
    return "\n".join(lines)


def format_detail_as_markdown(result: FriendlyResult) -> str:
    """
    将单个方案格式化为详细展示
    
    Args:
        result: FriendlyResult 对象
        
    Returns:
        格式化的 Markdown 字符串
    """
    lines = []
    
    lines.append(f"# {result.functional_group}")
    lines.append(f"\n{result.summary}\n")
    
    # 官能化信息
    lines.append("## 官能化方案")
    lines.append(f"| 项目 | 内容 |")
    lines.append(f"|------|------|")
    lines.append(f"| 官能化试剂 | {result.reagent} |")
    lines.append(f"| 官能化程度 | {result.degree} |")
    lines.append("")
    
    # 核心性能
    if result.key_features:
        lines.append("## 核心性能特点")
        for i, feature in enumerate(result.key_features, 1):
            if feature:
                lines.append(f"{i}. {feature}")
        lines.append("")
    
    # 关键指标
    if result.metrics:
        lines.append("## 关键性能指标")
        lines.append("| 指标 | 数值 |")
        lines.append("|------|------|")
        for metric, value in result.metrics.items():
            lines.append(f"| {metric} | {value} |")
        lines.append("")
    
    # 适用场景
    if result.application:
        lines.append("## 适用场景")
        for app in result.application:
            lines.append(f"- {app}")
        lines.append("")
    
    # 文献来源
    lines.append("## 数据来源")
    lines.append(f"来源: {result.source}")
    
    return "\n".join(lines)
