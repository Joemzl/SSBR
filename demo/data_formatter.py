"""
数据格式化模块
将内部数据转换为用户友好的展示格式

功能：
- 隐藏样本 ID，使用官能团名称标识
- 转换相似度为匹配度（高/中/低）
- 简化文献来源格式
- 提取核心性能指标

支持的 summary.md 格式：
- 标准格式 v2.0: 统一的 YAML front matter (functionalization 嵌套结构)
- 兼容旧格式：正文中提取或其他 YAML 结构
"""

import re
import yaml
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


def _extract_yaml_front_matter(content: str) -> Optional[Dict[str, Any]]:
    """
    从 Markdown 内容中提取 YAML front matter
    
    Args:
        content: Markdown 原始内容
        
    Returns:
        解析后的 YAML 字典，如果没有 front matter 则返回 None
    """
    # 防御 None 或空字符串输入
    if not content:
        return None
    
    yaml_match = re.match(r'^---\s*\n(.+?)\n---', content, re.DOTALL)
    if yaml_match:
        try:
            return yaml.safe_load(yaml_match.group(1))
        except yaml.YAMLError:
            return None
    return None


def parse_summary_content(content: str) -> Dict[str, Any]:
    """
    解析 summary.md 内容，提取关键信息
    
    支持标准格式 v2.0 (functionalization 嵌套结构) 和旧格式兼容
    
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
    
    # 防御 None 或空字符串输入
    if not content:
        return result
    
    # ========== 第一步：尝试从 YAML front matter 提取 ==========
    yaml_data = _extract_yaml_front_matter(content)
    yaml_extracted = False
    
    if yaml_data:
        # ===== 标准格式 v2.0: functionalization 嵌套结构 =====
        func_info = yaml_data.get("functionalization", {})
        # 放宽检查条件：只要有 functionalization 字典且非空即可
        if isinstance(func_info, dict) and func_info:
            # 检查是否官能化（兼容 is_functionalized 字段或通过 type 判断）
            is_functionalized = func_info.get("is_functionalized", True)  # 默认为 True
            func_type = func_info.get("type", "unknown")
            
            if not is_functionalized or func_type == "none":
                # 未官能化样本
                result["functional_group"] = "未官能化（工业SSBR）"
                result["reagent"] = "无"
                result["degree"] = "N/A"
            elif func_type == "filler_modification":
                # 填料改性
                reagent = func_info.get("reagent") or "填料改性"
                result["functional_group"] = f"填料改性"
                result["reagent"] = reagent
                result["degree"] = "N/A"
            else:
                # 官能化样本 - 优先使用 core_functional_group_name，fallback 到 functional_group
                fg = func_info.get("core_functional_group_name") or func_info.get("functional_group")
                if fg:
                    # 清理官能团名称，确保有 "官能化" 后缀
                    fg_clean = re.sub(r'\s*[（(].+?[）)]', '', fg).strip()
                    if "官能化" not in fg_clean:
                        result["functional_group"] = fg_clean + "官能化"
                    else:
                        result["functional_group"] = fg_clean
                
                reagent = func_info.get("reagent")
                if reagent:
                    result["reagent"] = reagent
                
                degree = func_info.get("degree")
                if degree:
                    result["degree"] = degree
            
            yaml_extracted = True
        
        # ===== 兼容旧格式 =====
        if not yaml_extracted:
            # polymer_type 包含 "未官能化"
            polymer_type = yaml_data.get("polymer_type", "") or ""  # 防御 None
            if polymer_type and "未官能化" in polymer_type:
                result["functional_group"] = "未官能化（工业SSBR）"
                result["reagent"] = "无"
                result["degree"] = "N/A"
                yaml_extracted = True
            
            # functionalizing_agent 格式 (旧)
            func_agent = yaml_data.get("functionalizing_agent", {})
            if isinstance(func_agent, dict) and func_agent:
                core_fg = func_agent.get("core_functional_group", "") or ""  # 防御 None
                if core_fg:
                    result["functional_group"] = core_fg + "官能化"
                    yaml_extracted = True
                
                reagent_name = func_agent.get("name", "") or ""  # 防御 None
                reagent_full = func_agent.get("full_name", "") or ""  # 防御 None
                if reagent_full:
                    result["reagent"] = f"{reagent_name} ({reagent_full})" if reagent_name else reagent_full
                    yaml_extracted = True
                elif reagent_name:
                    result["reagent"] = reagent_name
                    yaml_extracted = True
        
        # DOI 来源
        doi = yaml_data.get("doi") or yaml_data.get("source_doi") or yaml_data.get("literature_doi", "")
        if doi:
            result["source"] = f"DOI: {doi}"
            yaml_extracted = True
    
    # ========== 第二步：从正文提取（作为补充或 fallback）==========
    
    # 提取官能化信息（格式 A）
    # 支持多种格式：
    # 1. - **核心官能团**: 羧基（-COOH）
    # 2. **核心官能团**: 羧基 (-COOH)
    # 3. | 核心官能团 | 羧基 (-COOH) |  (表格格式)
    # 4. 从一句话总结中提取：采用XXX官能化
    if result["functional_group"] == "未知官能化":
        # 尝试 Markdown 格式
        fg_match = re.search(r'[-\s]*\*\*核心官能团\*\*:\s*(.+?)(?:\s*[（(]|$|\n)', content)
        if fg_match:
            fg_name = fg_match.group(1).strip()
            if fg_name and fg_name != '-' and fg_name != '- (-)':
                result["functional_group"] = fg_name + "官能化"
            else:
                result["functional_group"] = "未官能化（空白对照）"
        else:
            # 尝试表格格式: | 核心官能团 | 羧基 (-COOH) |
            fg_table_match = re.search(r'\|\s*核心官能团\s*\|\s*(.+?)\s*\|', content)
            if fg_table_match:
                fg_name = fg_table_match.group(1).strip()
                # 提取括号前的部分作为官能团名称
                fg_clean = re.sub(r'\s*[（(].+?[）)]', '', fg_name).strip()
                if fg_clean and fg_clean != '-':
                    result["functional_group"] = fg_clean + "官能化"
    
    # 从一句话总结中提取官能化信息（新增 fallback）
    if result["functional_group"] == "未知官能化":
        # 提取一句话总结部分
        summary_section = re.search(r'## 一句话总结\s*\n+>?\s*(.+?)(?:\n---|\n##)', content, re.DOTALL)
        if summary_section:
            summary_text = summary_section.group(1).strip()
            # 匹配常见的官能化描述模式：
            # 1. "采用XXX官能化" - 如 "采用羟基官能化"
            # 2. "XXX官能化SSBR" - 如 "氨基官能化"
            # 3. "通过XXX改性" - 如 "通过环氧基改性"
            # 4. "原位环氧化" - 如 "采用原位环氧化制备"
            # 5. "聚多巴胺" - 如 "聚多巴胺和环氧化弹性体协同"
            # 6. "通过XXX界面作用" - 如 "通过羧基双重界面作用"
            # 7. "离子官能化（XXX）" - 如 "离子官能化（吡啶基/羧基）"
            # 8. "XXX 一步法官能化" - 如 "TMPMP 一步法官能化"
            fg_patterns = [
                r'采用\s*[（(]?([^，,）)]+?)[）)]?\s*官能化',  # 采用羟基官能化
                r'([羟羧氨氧胺硅烷巯环氧胍]+基)\s*官能化',  # 直接匹配 XXX基官能化
                r'通过\s*([^，,]+?)\s*(?:官能化|改性)',  # 通过XXX官能化/改性
                r'([a-zA-Z0-9α-ωΑ-Ω,-]+[基团]?)\s*官能化',  # 英文/希腊字母命名的官能团
                r'采用\s*(原位环氧化|原位接枝|原位改性)',  # 采用原位环氧化
                r'采用\s*(聚多巴胺)[和与]',  # 采用聚多巴胺和XXX
                r'通过\s*(环氧基|环氧化)\s*(?:开环反应|反应)?',  # 通过环氧基开环反应
                r'(环氧化弹性体|环氧化SSBR|ESSBR)',  # 环氧化弹性体
                # 新增模式
                r'通过\s*([羟羧氨氧胺硅烷巯环氧胍]+基)\s*(?:双重)?界面',  # 通过羧基双重界面
                r'离子官能化[（(]([^）)]+)[）)]',  # 离子官能化（吡啶基/羧基）
                r'([A-Z0-9a-z]+)\s*(?:一步法)?官能化\s*SSBR',  # TMPMP一步法官能化SSBR
                r'([羟羧氨硅烷环氧胍吡啶]+基)[/和与]',  # 羧基/羟基...
                # 更多模式
                r'采用\s*(胺封端|氨基封端)',  # 采用胺封端
                r'采用\s*(催化环氧化|环氧化工艺)',  # 采用催化环氧化工艺
                r'采用\s*(环氧化天然橡胶|ENR)',  # 采用环氧化天然橡胶
                r'制备\s*(环氧化\s*SSBR)',  # 制备环氧化 SSBR
                r'(TBIR|TBID)\s*改性',  # TBIR 改性
                # 更多复杂模式
                r'引入\s*(脲基嘧啶酮|UPy)\s*基团',  # 引入脲基嘧啶酮 (UPy) 基团
                r'进行\s*(羟基封端)',  # 进行羟基封端
                r'(羟基化)\s*SSBR',  # 羟基化 SSBR
                r'(硅氢加成)',  # 硅氢加成
                r'(rGO-g-SiO2|石墨烯)',  # rGO-g-SiO2
                r'(纳米炭黑|CNT|碳纳米管)',  # 纳米填料
                # 最后一批模式
                r'采用\s*(TGDY|三嗪基石墨炔)',  # 三嗪基石墨炔
                r'采用\s*(APTES)\s*改性',  # APTES改性
                r'采用\s*(VTMS|乙烯基三甲氧基硅烷)',  # VTMS 接枝
                r'(烯烃复分解)',  # 烯烃复分解
                r'(LPB|液体聚丁二烯)',  # 液体聚丁二烯
                r'(烃类树脂|相容性研究)',  # 烃类树脂
                r'与\s*(环氧化\s*SSBR)',  # 与环氧化 SSBR
            ]
            for pattern in fg_patterns:
                fg_summary_match = re.search(pattern, summary_text)
                if fg_summary_match:
                    fg_name = fg_summary_match.group(1).strip()
                    # 移除多余的符号
                    fg_name = re.sub(r'[（(].+?[）)]', '', fg_name).strip()
                    if fg_name and len(fg_name) <= 20:  # 避免匹配过长的文本
                        # 转换特殊名称
                        name_mapping = {
                            "原位环氧化": "环氧基",
                            "原位接枝": "接枝",
                            "原位改性": "改性",
                            "环氧化弹性体": "环氧基",
                            "环氧化SSBR": "环氧基",
                            "ESSBR": "环氧基",
                            "环氧化": "环氧基",
                            "吡啶基/羧基": "离子",
                            "TMPMP": "巯基酯",
                            # 新增映射
                            "胺封端": "胺封端",
                            "氨基封端": "氨基封端",
                            "催化环氧化": "环氧基",
                            "环氧化工艺": "环氧基",
                            "环氧化天然橡胶": "ENR共混",
                            "ENR": "ENR共混",
                            "环氧化 SSBR": "环氧基",
                            "TBIR": "TBIR",
                            "TBID": "TBID",
                            # 更多映射
                            "脲基嘧啶酮": "UPy超分子",
                            "UPy": "UPy超分子",
                            "羟基封端": "羟基封端",
                            "羟基化": "羟基",
                            "硅氢加成": "填料改性",
                            "rGO-g-SiO2": "石墨烯杂化",
                            "石墨烯": "石墨烯杂化",
                            "纳米炭黑": "纳米炭黑",
                            "CNT": "碳纳米管",
                            "碳纳米管": "碳纳米管",
                            # 最后一批映射
                            "TGDY": "TGDY纳米填料",
                            "三嗪基石墨炔": "TGDY纳米填料",
                            "APTES": "APTES偶联",
                            "VTMS": "硅烷接枝",
                            "乙烯基三甲氧基硅烷": "硅烷接枝",
                            "烯烃复分解": "烯烃复分解",
                            "LPB": "LPB增塑",
                            "液体聚丁二烯": "LPB增塑",
                            "烃类树脂": "树脂研究",
                            "相容性研究": "相容性研究",
                        }
                        fg_name = name_mapping.get(fg_name, fg_name)
                        if "官能化" not in fg_name:
                            result["functional_group"] = fg_name + "官能化"
                        else:
                            result["functional_group"] = fg_name
                        break
    
    # 从研究亮点中提取官能化信息（新增 fallback）
    if result["functional_group"] == "未知官能化":
        highlight_section = re.search(r'## 研究亮点\s*\n+(.+?)(?:\n---|\n##)', content, re.DOTALL)
        if highlight_section:
            highlight_text = highlight_section.group(1).strip()
            # 匹配：采用 **XXX官能化** 策略
            highlight_patterns = [
                r'\*\*([^*]+官能化)\*\*',  # **XXX官能化**
                r'采用\s*\*\*([^*]+)\*\*\s*(?:官能化|策略)',  # 采用 **XXX** 官能化/策略
            ]
            for pattern in highlight_patterns:
                hl_match = re.search(pattern, highlight_text)
                if hl_match:
                    fg_name = hl_match.group(1).strip()
                    # 清理名称
                    fg_name = re.sub(r'α,ω-双端\s*', '', fg_name)  # 移除位置描述
                    fg_name = re.sub(r'\s*策略', '', fg_name)
                    if fg_name and len(fg_name) <= 30:
                        if "官能化" not in fg_name:
                            result["functional_group"] = fg_name + "官能化"
                        else:
                            result["functional_group"] = fg_name
                        break
    
    # 从样本概述表格中提取改性方法（新增 fallback）
    if result["functional_group"] == "未知官能化":
        # 匹配表格格式: | **改性方法** | AMMO 硅烷偶联剂改性 |
        method_patterns = [
            r'\|\s*\*\*改性方法\*\*\s*\|\s*(.+?)\s*\|',  # | **改性方法** | XXX |
            r'\|\s*改性方法\s*\|\s*(.+?)\s*\|',  # | 改性方法 | XXX |
            r'\|\s*\*\*材料类型\*\*\s*\|\s*(.+?)\s*\|',  # | **材料类型** | XXX |
        ]
        for pattern in method_patterns:
            method_match = re.search(pattern, content)
            if method_match:
                method_name = method_match.group(1).strip()
                # 从改性方法中提取关键信息
                if "硅烷" in method_name:
                    result["functional_group"] = "硅烷偶联剂改性"
                    break
                elif "改性" in method_name and len(method_name) <= 30:
                    result["functional_group"] = method_name
                    break
    
    # 从核心性能特点中提取（最后的 fallback）
    if result["functional_group"] == "未知官能化":
        # 匹配特定的研究类型
        feature_patterns = [
            r'纳米杂化[材料|策略]',  # 纳米杂化材料
            r'共凝聚法',  # 共凝聚法制备
            r'原位组装',  # 原位组装
            r'加工[性能|工艺]研究',  # 加工性能研究
        ]
        for pattern in feature_patterns:
            if re.search(pattern, content):
                # 尝试从一句话总结中提取更具体的描述
                summary_section = re.search(r'## 一句话总结\s*\n+>?\s*(.+?)(?:\n---|\n##)', content, re.DOTALL)
                if summary_section:
                    summary_text = summary_section.group(1).strip()
                    if "共凝聚法" in summary_text:
                        result["functional_group"] = "共凝聚法改性"
                    elif "原位组装" in summary_text or "纳米杂化" in summary_text:
                        result["functional_group"] = "纳米杂化改性"
                    elif "加工" in summary_text or "润滑" in summary_text:
                        result["functional_group"] = "加工研究"
                    break
    
    # 官能化试剂
    if result["reagent"] == "未知":
        # 尝试 Markdown 格式
        reagent_match = re.search(r'[-\s]*\*\*官能化试剂\*\*:\s*(.+?)(?:\n|$)', content)
        if reagent_match:
            reagent = reagent_match.group(1).strip()
            if "无" in reagent or "空白" in reagent:
                result["reagent"] = "无（空白对照）"
            else:
                result["reagent"] = reagent
        else:
            # 尝试表格格式: | 官能化试剂 | 3-MPA (3-巯基丙酸) |
            reagent_table_match = re.search(r'\|\s*官能化试剂\s*\|\s*(.+?)\s*\|', content)
            if reagent_table_match:
                result["reagent"] = reagent_table_match.group(1).strip()
    
    # 官能化程度
    if result["degree"] == "未知":
        # 尝试 Markdown 格式
        degree_match = re.search(r'[-\s]*\*\*官能化程度\*\*:\s*([\d.]+)\s*wt%', content)
        if degree_match:
            result["degree"] = f"{degree_match.group(1)} wt%"
        else:
            # 尝试表格格式: | 改性剂含量 | 9.6 wt% |
            degree_table_match = re.search(r'\|\s*(?:改性剂含量|官能化程度)\s*\|\s*([\d.]+\s*wt%)\s*\|', content)
            if degree_table_match:
                result["degree"] = degree_table_match.group(1).strip()
            else:
                result["degree"] = "N/A"
    
    # 一句话总结
    if not result["summary"]:
        summary_match = re.search(r'## 一句话总结\s*\n+(.+?)(?:\n---|\n##)', content, re.DOTALL)
        if summary_match:
            summary = summary_match.group(1).strip()
            # 移除可能的 Markdown 加粗标记
            summary = re.sub(r'\*\*(.+?)\*\*', r'\1', summary)
            # 移除可能的样本 ID
            summary = re.sub(r'SSBR-\d+', '', summary).strip()
            result["summary"] = summary if summary else "高性能官能化 SSBR 材料"
    
    # 核心性能特点（仅当 YAML 没有提取到时）
    if not result["key_features"]:
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
    
    # 关键性能指标（从表格提取，补充 YAML 中没有的）
    metrics_section = re.search(r'## 关键性能指标\s*\n(.+?)(?:\n---|\n##)', content, re.DOTALL)
    if metrics_section:
        table_text = metrics_section.group(1)
        # 解析表格行
        rows = re.findall(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|', table_text)
        for row in rows:
            if len(row) >= 4:
                category, metric, value, unit = row[0], row[1], row[2], row[3]
                # 跳过表头和无效值
                if metric in ['指标', '---', '------'] or value in ['-', '---', '------', '']:
                    continue
                if value.strip() and value.strip() != '-':
                    metric_key = metric.strip()
                    if metric_key not in result["metrics"]:
                        result["metrics"][metric_key] = f"{value.strip()} {unit.strip()}".strip()
    
    # 适用场景
    if not result["application"]:
        app_section = re.search(r'## 适用场景\s*\n(.+?)(?:\n---|\n##|\Z)', content, re.DOTALL)
        if app_section:
            app_text = app_section.group(1)
            # 提取 ✅ 或 ⚠️ 开头的场景
            apps = re.findall(r'[✅⚠️]\s*(.+)', app_text)
            if apps:
                result["application"] = [app.strip() for app in apps if app.strip()]
            else:
                # 尝试提取 - 开头的列表项
                apps = re.findall(r'^-\s*(.+)', app_text, re.MULTILINE)
                result["application"] = [app.strip() for app in apps if app.strip()]
    
    # 文献来源（补充）
    if result["source"] == "未知来源":
        # 从正文 DOI 和引文中提取
        doi_match = re.search(r'\*\*DOI\*\*:\s*(.+?)(?:\n|$)', content)
        cite_match = re.search(r'\*\*引文\*\*:\s*(.+?)(?:\n|$)', content)
        
        # 也支持表格格式: | 文献来源 | DOI: xxx |
        doi_table_match = re.search(r'\|\s*文献来源\s*\|\s*DOI:\s*(.+?)\s*\|', content)
        
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
        elif doi_table_match:
            result["source"] = f"DOI: {doi_table_match.group(1).strip()}"
    
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
    fg = parsed_data.get("functional_group", "") or ""  # 防御 None
    features = parsed_data.get("key_features", []) or []
    metrics = parsed_data.get("metrics", {}) or {}
    
    reasons = []
    
    # 根据官能团类型给出基础推荐
    if fg and ("硅烷" in fg or "硅氧烷" in fg):
        reasons.append("硅烷基团可与白炭黑形成共价键，显著提升界面结合强度")
    elif fg and "羧基" in fg:
        reasons.append("羧基可与白炭黑表面形成强氢键，改善分散性")
    elif fg and "羟基" in fg:
        reasons.append("羟基提供基础的界面相互作用")
    elif fg and "氨基" in fg:
        reasons.append("氨基可提供多种界面相互作用模式")
    elif fg and ("空白" in fg or "未官能化" in fg):
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
