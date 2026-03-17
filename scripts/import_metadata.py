#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSBR 元数据导入脚本

从 AI 提取的 Markdown 表格导入元数据到 Excel 文件。

工作流程：
1. 用户使用豆包/Gemini 等 AI 解析 PDF 文献
2. AI 按照提示词输出 Markdown 表格
3. 本脚本解析表格并导入到 dataset/数据.xlsx

Date: 2026-03-14
Branch: 002-rag-data-migration
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.excel_handler import ExcelHandler

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
EXCEL_PATH = DATASET_DIR / "数据.xlsx"


def parse_markdown_table(content: str) -> List[Dict[str, str]]:
    """
    解析 Markdown 表格
    
    支持格式：
    | 列1 | 列2 | 列3 |
    |-----|-----|-----|
    | 值1 | 值2 | 值3 |
    
    Args:
        content: Markdown 文本内容
        
    Returns:
        字典列表，每个字典代表一行数据
    """
    lines = content.strip().split('\n')
    
    # 找到表格行
    table_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            table_lines.append(line)
    
    if len(table_lines) < 3:
        raise ValueError("未找到有效的 Markdown 表格（至少需要表头、分隔符和一行数据）")
    
    # 解析表头
    header_line = table_lines[0]
    headers = [h.strip() for h in header_line.strip('|').split('|')]
    
    # 跳过分隔符行（第二行）
    # 解析数据行
    rows = []
    for line in table_lines[2:]:
        values = [v.strip() for v in line.strip('|').split('|')]
        if len(values) == len(headers):
            row_data = dict(zip(headers, values))
            rows.append(row_data)
        else:
            print(f"警告: 跳过列数不匹配的行: {line[:50]}...")
    
    return rows


def validate_row(row: Dict[str, str]) -> Dict[str, Any]:
    """
    验证并清洗一行数据
    
    Args:
        row: 原始行数据
        
    Returns:
        验证后的数据字典
    """
    result = {}
    errors = []
    
    # 必填字段检查
    required_fields = ['是否是SSBR', '是否是链中官能化', '官能化试剂名称']
    for field in required_fields:
        if field not in row or not row[field] or row[field] == '-':
            errors.append(f"缺少必填字段: {field}")
    
    # 检查是否为有效样本（必须是 SSBR 且是链中官能化）
    is_ssbr = row.get('是否是SSBR', '').strip()
    is_inchain = row.get('是否是链中官能化', '').strip()
    
    if is_ssbr != '是':
        errors.append(f"非 SSBR 样本 (是否是SSBR={is_ssbr})")
    if is_inchain != '是':
        errors.append(f"非链中官能化样本 (是否是链中官能化={is_inchain})")
    
    if errors:
        return {'valid': False, 'errors': errors, 'data': row}
    
    # 清洗数据
    for key, value in row.items():
        # 处理占位符
        if value == '-' or value == '－' or value == '':
            result[key] = None
        else:
            result[key] = value.strip()
    
    return {'valid': True, 'errors': [], 'data': result}


def import_from_file(
    input_path: Path,
    excel_handler: ExcelHandler,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    从 Markdown 文件导入数据
    
    Args:
        input_path: Markdown 文件路径
        excel_handler: Excel 处理器
        dry_run: 是否为试运行模式
        
    Returns:
        导入统计
    """
    stats = {
        'total_rows': 0,
        'imported': 0,
        'skipped_invalid': 0,
        'errors': [],
        'imported_samples': []
    }
    
    # 读取文件
    content = input_path.read_text(encoding='utf-8')
    
    # 解析表格
    try:
        rows = parse_markdown_table(content)
    except ValueError as e:
        stats['errors'].append(str(e))
        return stats
    
    stats['total_rows'] = len(rows)
    print(f"解析到 {len(rows)} 行数据")
    
    # 逐行处理
    for i, row in enumerate(rows, 1):
        print(f"\n处理第 {i} 行...")
        
        # 验证数据
        validation = validate_row(row)
        if not validation['valid']:
            print(f"  [SKIP] 无效: {', '.join(validation['errors'])}")
            stats['skipped_invalid'] += 1
            stats['errors'].append({
                'row': i,
                'errors': validation['errors'],
                'data': row
            })
            continue
        
        data = validation['data']
        doi = data.get('DOI')
        
        # 导入数据
        if dry_run:
            next_id = excel_handler.get_next_sample_id()
            print(f"  [DRY RUN] 将创建样本: {next_id}")
            print(f"    试剂: {data.get('官能化试剂名称')}")
            print(f"    DOI: {doi}")
            stats['imported'] += 1
            stats['imported_samples'].append({
                'sample_id': next_id,
                'reagent': data.get('官能化试剂名称'),
                'doi': doi
            })
        else:
            try:
                sample_id = excel_handler.add_sample(data)
                # 每次添加后立即保存，确保数据写入
                excel_handler.save()
                print(f"  [OK] 已创建样本: {sample_id}")
                stats['imported'] += 1
                stats['imported_samples'].append({
                    'sample_id': sample_id,
                    'reagent': data.get('官能化试剂名称'),
                    'doi': doi
                })
            except Exception as e:
                print(f"  [FAIL] 导入失败: {e}")
                stats['errors'].append({
                    'row': i,
                    'errors': [str(e)],
                    'data': row
                })
    
    return stats


def import_from_clipboard(
    excel_handler: ExcelHandler,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    从剪贴板导入数据
    
    Args:
        excel_handler: Excel 处理器
        dry_run: 是否为试运行模式
        
    Returns:
        导入统计
    """
    try:
        import pyperclip
        content = pyperclip.paste()
    except ImportError:
        print("错误: 需要安装 pyperclip 模块")
        print("  pip install pyperclip")
        return {'errors': ['pyperclip 未安装']}
    except Exception as e:
        print(f"错误: 无法读取剪贴板 - {e}")
        return {'errors': [str(e)]}
    
    if not content or '|' not in content:
        print("错误: 剪贴板中没有有效的 Markdown 表格")
        return {'errors': ['剪贴板内容无效']}
    
    # 创建临时文件
    temp_path = PROJECT_ROOT / ".temp_import.md"
    temp_path.write_text(content, encoding='utf-8')
    
    try:
        result = import_from_file(temp_path, excel_handler, dry_run)
    finally:
        temp_path.unlink(missing_ok=True)
    
    return result


def interactive_import(excel_handler: ExcelHandler):
    """
    交互式导入模式
    
    Args:
        excel_handler: Excel 处理器
    """
    print("\n" + "=" * 60)
    print("SSBR 元数据交互式导入")
    print("=" * 60)
    print("\n请粘贴 Markdown 表格内容，输入空行结束:")
    print("（提示：表格应包含表头、分隔符和数据行）\n")
    
    lines = []
    empty_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == '':
                empty_count += 1
                if empty_count >= 2:
                    break
                lines.append(line)
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break
    
    content = '\n'.join(lines)
    
    if not content.strip():
        print("未输入任何内容")
        return
    
    # 保存到临时文件
    temp_path = PROJECT_ROOT / ".temp_import.md"
    temp_path.write_text(content, encoding='utf-8')
    
    try:
        # 先试运行
        print("\n" + "-" * 40)
        print("预览模式（不实际导入）:")
        print("-" * 40)
        
        stats = import_from_file(temp_path, excel_handler, dry_run=True)
        
        if stats['imported'] == 0:
            print("\n没有可导入的数据")
            return
        
        # 确认导入
        print(f"\n共 {stats['imported']} 条数据可导入")
        confirm = input("是否确认导入？(y/N): ").strip().lower()
        
        if confirm == 'y':
            print("\n" + "-" * 40)
            print("正在导入...")
            print("-" * 40)
            stats = import_from_file(temp_path, excel_handler, dry_run=False)
            excel_handler.save()
            print(f"\n✓ 已导入 {stats['imported']} 条数据")
        else:
            print("已取消导入")
    finally:
        temp_path.unlink(missing_ok=True)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='SSBR 元数据导入工具 - 从 Markdown 表格导入到 Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从文件导入（试运行）
  python import_metadata.py --file data.md --dry-run
  
  # 从文件导入
  python import_metadata.py --file data.md
  
  # 从剪贴板导入
  python import_metadata.py --clipboard
  
  # 交互式导入
  python import_metadata.py --interactive
        """
    )
    
    parser.add_argument('--file', '-f', type=Path, help='Markdown 文件路径')
    parser.add_argument('--clipboard', '-c', action='store_true', help='从剪贴板导入')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互式导入模式')
    parser.add_argument('--dry-run', action='store_true', help='试运行模式（不实际写入）')
    parser.add_argument('--excel', type=Path, default=EXCEL_PATH, help='Excel 文件路径')
    
    args = parser.parse_args()
    
    # 检查参数
    if not (args.file or args.clipboard or args.interactive):
        parser.print_help()
        print("\n错误: 请指定 --file、--clipboard 或 --interactive")
        return 1
    
    # 打开 Excel
    with ExcelHandler(args.excel) as excel:
        print(f"已打开 Excel: {args.excel}")
        print(f"当前样本数: {len(excel.get_all_samples())}")
        
        if args.interactive:
            interactive_import(excel)
        elif args.file:
            if not args.file.exists():
                print(f"错误: 文件不存在 - {args.file}")
                return 1
            
            print(f"\n从文件导入: {args.file}")
            stats = import_from_file(
                args.file, 
                excel,
                dry_run=args.dry_run
            )
            
            print_stats(stats, args.dry_run)
            
        elif args.clipboard:
            print("\n从剪贴板导入...")
            stats = import_from_clipboard(
                excel,
                dry_run=args.dry_run
            )
            
            print_stats(stats, args.dry_run)
    
    return 0


def print_stats(stats: Dict[str, Any], dry_run: bool = False):
    """打印导入统计"""
    print("\n" + "=" * 60)
    print("导入统计" + (" [DRY RUN]" if dry_run else ""))
    print("=" * 60)
    print(f"  总行数: {stats.get('total_rows', 0)}")
    print(f"  已导入: {stats.get('imported', 0)}")
    print(f"  跳过（无效）: {stats.get('skipped_invalid', 0)}")
    
    if stats.get('imported_samples'):
        print("\n导入的样本:")
        for sample in stats['imported_samples']:
            print(f"  - {sample['sample_id']}: {sample.get('reagent', 'N/A')}")
    
    if stats.get('errors'):
        print(f"\n错误 ({len(stats['errors'])} 条):")
        for err in stats['errors'][:5]:  # 只显示前 5 条
            if isinstance(err, dict):
                print(f"  - 第 {err.get('row')} 行: {', '.join(err.get('errors', []))}")
            else:
                print(f"  - {err}")


if __name__ == '__main__':
    sys.exit(main())
