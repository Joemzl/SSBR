"""
向量缓存构建脚本
用于预计算所有 summary.md 的向量并保存到缓存文件

Usage:
    python scripts/build_vector_cache.py           # 增量更新
    python scripts/build_vector_cache.py --force   # 强制重建
    python scripts/build_vector_cache.py --stats   # 仅显示统计

Created: 2026-03-19
"""

import sys
import argparse
import time
import io
from pathlib import Path

# 修复 Windows 控制台 Unicode 编码问题
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.vector_cache import VectorCache, get_vector_cache
from utils.embedding import get_embedding_service


def main():
    parser = argparse.ArgumentParser(description='向量缓存构建工具')
    parser.add_argument('--force', action='store_true', help='强制重建全部缓存')
    parser.add_argument('--stats', action='store_true', help='仅显示缓存统计')
    args = parser.parse_args()
    
    print("=" * 60)
    print("SSBR 向量缓存构建工具")
    print("=" * 60)
    print()
    
    cache = get_vector_cache()
    
    if args.stats:
        # 仅显示统计
        cache.load()
        stats = cache.get_stats()
        print("缓存统计:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        return
    
    # 检查 Embedding 服务
    embedding_service = get_embedding_service()
    if not embedding_service.is_available():
        print("❌ Embedding 服务不可用，请检查 API Key 配置")
        print("   设置环境变量 OPENAI_API_KEY 或在项目根目录创建 .env 文件")
        sys.exit(1)
    
    print("✅ Embedding 服务可用")
    print()
    
    # 显示当前状态
    cache.load()
    summaries = cache.get_all_summaries()
    print(f"发现 {len(summaries)} 个可检索样本")
    
    if not args.force:
        to_update, to_delete = cache.check_updates(summaries)
        print(f"需要更新: {len(to_update)} 个")
        print(f"需要删除: {len(to_delete)} 个")
        
        if not to_update and not to_delete:
            print("\n✅ 缓存已是最新，无需更新")
            stats = cache.get_stats()
            print(f"   已缓存: {stats.get('total_documents', 0)} 个文档")
            return
    else:
        print("强制重建模式：将重新向量化所有文档")
    
    print()
    print("开始构建缓存...")
    start_time = time.time()
    
    updated = cache.build_cache(embedding_service, force_rebuild=args.force)
    
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print(f"✅ 缓存构建完成!")
    print(f"   更新文档: {updated} 个")
    print(f"   耗时: {elapsed:.1f} 秒")
    print()
    
    # 显示最终统计
    stats = cache.get_stats()
    print("最终状态:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == '__main__':
    main()
