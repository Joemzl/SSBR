#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero Bridge - Zotero MCP 桥接模块

通过 Zotero MCP 服务查询文献信息和 PDF 路径。
替代原有的基于 DOI 文件名匹配 literature/ 目录的方式。

Date: 2026-03-14
Branch: 002-rag-data-migration
"""

import json
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


@dataclass
class PDFAttachment:
    """PDF 附件信息"""
    key: str
    filename: str
    path: str
    content_type: str
    has_fulltext: bool
    is_si: bool = False  # 是否为 SI 补充材料


@dataclass
class ZoteroItem:
    """Zotero 条目信息"""
    key: str
    title: str
    doi: Optional[str]
    creators: List[str]
    year: Optional[int]
    publication: Optional[str]
    abstract: Optional[str]
    pdf_attachments: List[PDFAttachment]
    
    @property
    def main_pdf(self) -> Optional[PDFAttachment]:
        """获取主 PDF（非 SI）"""
        for att in self.pdf_attachments:
            if not att.is_si:
                return att
        return self.pdf_attachments[0] if self.pdf_attachments else None
    
    @property
    def si_pdf(self) -> Optional[PDFAttachment]:
        """获取 SI 补充材料 PDF"""
        for att in self.pdf_attachments:
            if att.is_si:
                return att
        return None
    
    @property
    def has_si(self) -> bool:
        """是否有 SI 补充材料"""
        return self.si_pdf is not None


class ZoteroBridge:
    """Zotero MCP 桥接类"""
    
    # SSBR 目录的 Collection Key（可配置）
    SSBR_COLLECTION_KEY = "M3PDJABT"
    
    def __init__(self, collection_key: Optional[str] = None):
        """
        初始化 Zotero 桥接
        
        Args:
            collection_key: Zotero 目录 key，默认使用 SSBR 目录
        """
        self.collection_key = collection_key or self.SSBR_COLLECTION_KEY
        self._cache: Dict[str, ZoteroItem] = {}
    
    def search_by_doi(self, doi: str) -> Optional[ZoteroItem]:
        """
        通过 DOI 搜索 Zotero 条目
        
        Args:
            doi: 文献 DOI（原始格式，如 10.1039/c4ra09492a）
        
        Returns:
            ZoteroItem 或 None
        """
        # 检查缓存
        cache_key = f"doi:{doi}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # 使用 search_library 搜索
        result = self._call_mcp("search_library", {
            "q": doi,
            "limit": 5
        })
        
        if not result:
            return None
        
        # 获取搜索结果（可能是 results 或 items）
        items_data = result.get("results", []) or result.get("items", [])
        
        if not items_data:
            return None
        
        # 返回第一个匹配的条目（搜索结果已按相关性排序）
        item_data = items_data[0]
        item = self._parse_item(item_data)
        self._cache[cache_key] = item
        self._cache[f"key:{item.key}"] = item
        return item
    
    def get_by_key(self, item_key: str) -> Optional[ZoteroItem]:
        """
        通过 Zotero item key 获取条目详情
        
        Args:
            item_key: Zotero 条目 key（如 ALCQDLD4）
        
        Returns:
            ZoteroItem 或 None
        """
        # 检查缓存
        cache_key = f"key:{item_key}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # 使用 get_item_details 获取详情
        result = self._call_mcp("get_item_details", {
            "itemKey": item_key,
            "mode": "complete"
        })
        
        if not result:
            return None
        
        item = self._parse_item(result)
        self._cache[cache_key] = item
        if item.doi:
            self._cache[f"doi:{item.doi}"] = item
        
        return item
    
    def get_pdf_path(self, doi: str = None, item_key: str = None) -> Optional[str]:
        """
        获取 PDF 文件的本地路径
        
        Args:
            doi: 文献 DOI
            item_key: Zotero 条目 key
        
        Returns:
            PDF 文件路径或 None
        """
        item = None
        if item_key:
            item = self.get_by_key(item_key)
        elif doi:
            item = self.search_by_doi(doi)
        
        if item and item.main_pdf:
            return item.main_pdf.path
        
        return None
    
    def get_pdf_paths(self, doi: str = None, item_key: str = None) -> Dict[str, Optional[str]]:
        """
        获取主 PDF 和 SI PDF 的本地路径
        
        Args:
            doi: 文献 DOI
            item_key: Zotero 条目 key
        
        Returns:
            {"main": 主PDF路径, "si": SI PDF路径}
        """
        item = None
        if item_key:
            item = self.get_by_key(item_key)
        elif doi:
            item = self.search_by_doi(doi)
        
        result = {"main": None, "si": None}
        if item:
            if item.main_pdf:
                result["main"] = item.main_pdf.path
            if item.si_pdf:
                result["si"] = item.si_pdf.path
        
        return result
    
    def list_collection_items(self, limit: int = 100, offset: int = 0) -> List[ZoteroItem]:
        """
        列出 SSBR 目录下的所有条目
        
        Args:
            limit: 返回数量限制
            offset: 分页偏移
        
        Returns:
            ZoteroItem 列表
        """
        result = self._call_mcp("get_collection_items", {
            "collectionKey": self.collection_key,
            "limit": limit,
            "offset": offset
        })
        
        if not result:
            return []
        
        # 获取条目列表（可能是列表本身，或 dict 中的 items/results）
        if isinstance(result, list):
            items_data = result
        else:
            items_data = result.get("items", []) or result.get("results", [])
        
        items = []
        for item_data in items_data:
            item = self._parse_item(item_data)
            items.append(item)
            # 更新缓存
            self._cache[f"key:{item.key}"] = item
            if item.doi:
                self._cache[f"doi:{item.doi}"] = item
        
        return items
    
    def _parse_item(self, data: Dict[str, Any]) -> ZoteroItem:
        """解析 Zotero 条目数据"""
        # 解析创作者
        creators = []
        creators_data = data.get("creators", [])
        if isinstance(creators_data, str):
            # 如果是字符串（如 "Liangliang Qu, Lijing Wang"），按逗号分割
            creators = [c.strip() for c in creators_data.split(",")]
        else:
            for creator in creators_data:
                if isinstance(creator, dict):
                    name = creator.get("lastName", "") or creator.get("name", "")
                    if name:
                        creators.append(name)
                elif isinstance(creator, str):
                    creators.append(creator)
        
        # 解析 PDF 附件
        pdf_attachments = []
        for att in data.get("attachments", []):
            content_type = att.get("contentType", "")
            if content_type == "application/pdf":
                filename = att.get("filename", "")
                # 判断是否为 SI（文件名必须明确包含 SI 相关关键词）
                filename_lower = filename.lower()
                is_si = any([
                    "_si." in filename_lower,
                    "_si_" in filename_lower,
                    " si." in filename_lower,
                    " si " in filename_lower,
                    "supporting" in filename_lower,
                    "supplementary" in filename_lower,
                    "supplement" in filename_lower and "info" in filename_lower,
                ])
                
                # 路径字段可能是 filePath 或 path
                file_path = att.get("filePath", "") or att.get("path", "")
                
                pdf_attachments.append(PDFAttachment(
                    key=att.get("key", ""),
                    filename=filename,
                    path=file_path,
                    content_type="application/pdf",
                    has_fulltext=att.get("hasFulltext", False),
                    is_si=is_si
                ))
        
        # 解析年份
        year = None
        date_str = data.get("date", "") or data.get("year", "")
        if date_str:
            try:
                # 尝试提取年份
                import re
                year_match = re.search(r'(\d{4})', str(date_str))
                if year_match:
                    year = int(year_match.group(1))
            except:
                pass
        
        return ZoteroItem(
            key=data.get("key", ""),
            title=data.get("title", ""),
            doi=data.get("DOI", "") or data.get("doi", "") or None,
            creators=creators,
            year=year,
            publication=data.get("publicationTitle", "") or data.get("journalAbbreviation", ""),
            abstract=data.get("abstractNote", "") or None,
            pdf_attachments=pdf_attachments
        )
    
    def _call_mcp(self, tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        调用 Zotero MCP 工具
        
        注意：此方法在脚本独立运行时使用 HTTP 直接调用 MCP 服务。
        在 CodeBuddy IDE 中，应使用 IDE 提供的 MCP 调用机制。
        
        Args:
            tool_name: 工具名称
            args: 工具参数
        
        Returns:
            工具返回结果或 None
        """
        import urllib.request
        import urllib.error
        
        # Zotero MCP 服务端点
        url = "http://127.0.0.1:23120/mcp"
        
        # 构造 JSON-RPC 2.0 请求
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": args
            }
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # 解析 JSON-RPC 响应
                if "error" in result:
                    print(f"[ZoteroBridge] MCP 错误: {result['error']}", file=sys.stderr)
                    return None
                
                if "result" in result:
                    content = result["result"].get("content", [])
                    if content and isinstance(content, list):
                        for item in content:
                            if item.get("type") == "text":
                                try:
                                    parsed = json.loads(item.get("text", "{}"))
                                    # 处理嵌套的 data 结构
                                    if "data" in parsed:
                                        return parsed["data"]
                                    return parsed
                                except json.JSONDecodeError:
                                    return {"text": item.get("text", "")}
                
                return result.get("result")
                
        except urllib.error.URLError as e:
            print(f"[ZoteroBridge] MCP 连接失败: {e}", file=sys.stderr)
            print(f"[ZoteroBridge] 请确保 Zotero 已启动且 MCP 服务正在运行", file=sys.stderr)
            return None
        except Exception as e:
            print(f"[ZoteroBridge] MCP 调用错误: {e}", file=sys.stderr)
            return None


# === Fallback: 本地 literature/ 目录查找 ===

def find_pdf_in_literature(doi: str, is_si: bool = False) -> Optional[str]:
    """
    在本地 literature/ 或 literature_SI/ 目录中按 DOI 查找 PDF
    
    这是 Zotero 不可用时的 fallback 方案。
    
    Args:
        doi: 文献 DOI（原始格式或路径安全格式）
        is_si: 是否查找 SI 补充材料
    
    Returns:
        PDF 文件路径或 None
    """
    # 将 DOI 转换为可能的文件名模式
    doi_pattern = doi.replace("/", "_").lower()
    
    # 确定搜索目录
    search_dir = PROJECT_ROOT / ("literature_SI" if is_si else "literature")
    
    if not search_dir.exists():
        return None
    
    # 搜索匹配的 PDF 文件
    for pdf_file in search_dir.glob("*.pdf"):
        if doi_pattern in pdf_file.name.lower():
            return str(pdf_file)
    
    return None


def get_literature_path(doi: str, zotero_key: str = None, is_si: bool = False) -> Optional[str]:
    """
    获取文献 PDF 路径（统一入口）
    
    优先使用 Zotero MCP，失败时 fallback 到本地目录。
    
    Args:
        doi: 文献 DOI
        zotero_key: Zotero 条目 key（可选，优先使用）
        is_si: 是否获取 SI 补充材料
    
    Returns:
        PDF 文件路径或 None
    """
    # 1. 尝试 Zotero MCP
    try:
        bridge = ZoteroBridge()
        paths = bridge.get_pdf_paths(doi=doi, item_key=zotero_key)
        target_path = paths["si"] if is_si else paths["main"]
        if target_path:
            return target_path
    except Exception as e:
        print(f"[get_literature_path] Zotero 查询失败: {e}", file=sys.stderr)
    
    # 2. Fallback: 本地 literature/ 目录
    local_path = find_pdf_in_literature(doi, is_si=is_si)
    if local_path:
        print(f"[get_literature_path] 使用本地文件: {local_path}", file=sys.stderr)
        return local_path
    
    return None


# === CLI 入口 ===

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Zotero MCP 桥接工具 - 查询文献信息和 PDF 路径"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="按 DOI 搜索文献")
    search_parser.add_argument("doi", help="文献 DOI")
    
    # get 命令
    get_parser = subparsers.add_parser("get", help="获取条目详情")
    get_parser.add_argument("key", help="Zotero item key")
    
    # path 命令
    path_parser = subparsers.add_parser("path", help="获取 PDF 路径")
    path_parser.add_argument("--doi", help="文献 DOI")
    path_parser.add_argument("--key", help="Zotero item key")
    path_parser.add_argument("--si", action="store_true", help="获取 SI 路径")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出 SSBR 目录下的文献")
    list_parser.add_argument("--limit", type=int, default=20, help="返回数量")
    list_parser.add_argument("--offset", type=int, default=0, help="偏移量")
    list_parser.add_argument("--with-pdf", action="store_true", help="仅显示有 PDF 的条目")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    bridge = ZoteroBridge()
    
    if args.command == "search":
        item = bridge.search_by_doi(args.doi)
        if item:
            print(f"找到文献: {item.title}")
            print(f"  Key: {item.key}")
            print(f"  DOI: {item.doi}")
            print(f"  年份: {item.year}")
            print(f"  PDF 数量: {len(item.pdf_attachments)}")
            if item.main_pdf:
                print(f"  主 PDF: {item.main_pdf.path}")
            if item.si_pdf:
                print(f"  SI PDF: {item.si_pdf.path}")
        else:
            print(f"未找到 DOI 为 {args.doi} 的文献")
            sys.exit(1)
    
    elif args.command == "get":
        item = bridge.get_by_key(args.key)
        if item:
            print(f"标题: {item.title}")
            print(f"DOI: {item.doi}")
            print(f"作者: {', '.join(item.creators)}")
            print(f"年份: {item.year}")
            print(f"期刊: {item.publication}")
            print(f"PDF 附件: {len(item.pdf_attachments)} 个")
            for i, att in enumerate(item.pdf_attachments):
                si_mark = " [SI]" if att.is_si else ""
                print(f"  [{i+1}]{si_mark} {att.filename}")
                print(f"      路径: {att.path}")
        else:
            print(f"未找到 key 为 {args.key} 的条目")
            sys.exit(1)
    
    elif args.command == "path":
        if not args.doi and not args.key:
            print("错误: 必须提供 --doi 或 --key")
            sys.exit(1)
        
        path = get_literature_path(
            doi=args.doi or "",
            zotero_key=args.key,
            is_si=args.si
        )
        
        if path:
            print(path)
        else:
            target = "SI" if args.si else "主"
            print(f"未找到{target} PDF")
            sys.exit(1)
    
    elif args.command == "list":
        items = bridge.list_collection_items(limit=args.limit, offset=args.offset)
        
        if args.with_pdf:
            items = [item for item in items if item.pdf_attachments]
        
        print(f"共 {len(items)} 条记录:\n")
        for i, item in enumerate(items):
            pdf_count = len(item.pdf_attachments)
            si_mark = " [有SI]" if item.has_si else ""
            print(f"{i+1}. [{item.key}] {item.title[:50]}...")
            print(f"   DOI: {item.doi or '-'} | PDF: {pdf_count}个{si_mark}")


if __name__ == "__main__":
    main()
