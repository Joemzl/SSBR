"""
向量索引增量更新脚本
支持单样本实时更新，避免全量重计算

Created: 2026-03-05
Task: T050
FR-022: 支持单样本实时更新

MVP 版本说明：
- 当前为纯文件实时计算模式，不持久化向量
- 本脚本主要用于验证 summary.md 可读性和预热缓存
- 未来升级到 Chroma 时，本脚本将负责向量持久化
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.yaml_parser import read_interpretation_file
from utils.embedding import embed_text, EmbeddingError

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
INTERPRETATIONS_DIR = PROJECT_ROOT / "dataset" / "interpretations"


def get_all_sample_ids() -> List[str]:
    """
    获取所有样本 ID
    
    Returns:
        样本 ID 列表
    """
    samples = []
    for d in INTERPRETATIONS_DIR.iterdir():
        if d.is_dir() and d.name.startswith('SSBR-'):
            samples.append(d.name)
    return sorted(samples)


def validate_summary(sample_id: str) -> Dict[str, Any]:
    """
    验证 summary.md 的有效性
    
    Args:
        sample_id: 样本 ID
        
    Returns:
        验证结果
    """
    result = {
        'sample_id': sample_id,
        'valid': False,
        'file_exists': False,
        'yaml_valid': False,
        'body_length': 0,
        'errors': []
    }
    
    summary_path = INTERPRETATIONS_DIR / sample_id / "summary.md"
    
    # 检查文件存在
    if not summary_path.exists():
        result['errors'].append("summary.md does not exist")
        return result
    
    result['file_exists'] = True
    
    # 解析文件
    try:
        doc = read_interpretation_file(summary_path)
        result['yaml_valid'] = True
        result['body_length'] = len(doc['body'])
        
        # 验证最小内容长度
        if result['body_length'] < 200:
            result['errors'].append(f"Body too short: {result['body_length']} chars (min: 200)")
        else:
            result['valid'] = True
            
    except Exception as e:
        result['errors'].append(f"Parse error: {e}")
    
    return result


def update_single_sample(sample_id: str, dry_run: bool = False) -> Dict[str, Any]:
    """
    更新单个样本的向量索引
    
    Args:
        sample_id: 样本 ID
        dry_run: 是否为预览模式
        
    Returns:
        更新结果
    """
    result = {
        'sample_id': sample_id,
        'success': False,
        'embedding_computed': False,
        'embedding_dim': 0,
        'errors': []
    }
    
    # 验证 summary
    validation = validate_summary(sample_id)
    if not validation['valid']:
        result['errors'] = validation['errors']
        return result
    
    # 读取 summary 内容
    summary_path = INTERPRETATIONS_DIR / sample_id / "summary.md"
    
    try:
        doc = read_interpretation_file(summary_path)
        content = doc['body']
        
        if dry_run:
            print(f"  [DRY RUN] Would compute embedding for {len(content)} chars")
            result['success'] = True
            return result
        
        # 计算 embedding
        embedding = get_embedding(content)
        
        if embedding is not None and len(embedding) > 0:
            result['embedding_computed'] = True
            result['embedding_dim'] = len(embedding)
            result['success'] = True
            print(f"  [OK] Embedding computed: {len(embedding)} dimensions")
        else:
            result['errors'].append("Embedding computation failed")
            
    except Exception as e:
        result['errors'].append(f"Error: {e}")
    
    return result


def update_all_samples(dry_run: bool = False) -> Dict[str, Any]:
    """
    更新所有样本的向量索引
    
    Args:
        dry_run: 是否为预览模式
        
    Returns:
        更新统计
    """
    stats = {
        'total': 0,
        'valid': 0,
        'updated': 0,
        'failed': 0,
        'errors': []
    }
    
    sample_ids = get_all_sample_ids()
    stats['total'] = len(sample_ids)
    
    print(f"\nProcessing {len(sample_ids)} samples...")
    
    for sample_id in sample_ids:
        print(f"\n{sample_id}:")
        
        # 验证
        validation = validate_summary(sample_id)
        if validation['valid']:
            stats['valid'] += 1
        else:
            print(f"  [SKIP] Invalid: {validation['errors']}")
            continue
        
        # 更新
        result = update_single_sample(sample_id, dry_run)
        if result['success']:
            stats['updated'] += 1
        else:
            stats['failed'] += 1
            stats['errors'].append(f"{sample_id}: {result['errors']}")
    
    return stats


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='SSBR Vector Index Update Tool',
        epilog='MVP Note: Current version uses real-time computation without persistence.'
    )
    parser.add_argument(
        '--sample', '-s',
        type=str,
        help='Update specific sample (e.g., SSBR-001)'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Update all samples'
    )
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Preview mode, do not compute embeddings'
    )
    parser.add_argument(
        '--validate-only', '-v',
        action='store_true',
        help='Only validate summary files, do not compute embeddings'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("SSBR Vector Index Update Tool")
    print("=" * 60)
    
    if args.dry_run:
        print("\n[DRY RUN MODE] No embeddings will be computed\n")
    
    # 仅验证模式
    if args.validate_only:
        print("\n[VALIDATION MODE]\n")
        sample_ids = [args.sample] if args.sample else get_all_sample_ids()
        
        valid_count = 0
        for sample_id in sample_ids:
            result = validate_summary(sample_id)
            status = "[OK]" if result['valid'] else "[FAIL]"
            print(f"  {sample_id}: {status}")
            if result['valid']:
                valid_count += 1
            elif result['errors']:
                for err in result['errors']:
                    print(f"    - {err}")
        
        print(f"\nValidation complete: {valid_count}/{len(sample_ids)} valid")
        return 0 if valid_count == len(sample_ids) else 1
    
    # 单样本更新
    if args.sample:
        print(f"\nUpdating sample: {args.sample}")
        result = update_single_sample(args.sample, args.dry_run)
        
        if result['success']:
            print(f"\n[OK] {args.sample} updated successfully")
            if result['embedding_computed']:
                print(f"  Embedding dimensions: {result['embedding_dim']}")
            return 0
        else:
            print(f"\n[FAIL] Update failed: {result['errors']}")
            return 1
    
    # 全量更新
    if args.all:
        stats = update_all_samples(args.dry_run)
        
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"  Total samples: {stats['total']}")
        print(f"  Valid summaries: {stats['valid']}")
        print(f"  Successfully updated: {stats['updated']}")
        print(f"  Failed: {stats['failed']}")
        
        if stats['errors']:
            print("\nErrors:")
            for err in stats['errors']:
                print(f"  - {err}")
        
        return 0 if stats['failed'] == 0 else 1
    
    # 无参数，显示帮助
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
