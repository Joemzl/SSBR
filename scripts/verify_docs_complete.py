"""验证所有样本是否都有完整的详细解读文档"""

from pathlib import Path

INTERP_DIR = Path(__file__).parent.parent / "dataset" / "interpretations"
DOCS = ['mechanical.md', 'nmr.md', 'dsc.md', 'tem.md', 'summary.md']


def main():
    missing = []
    complete = 0
    
    for sample_dir in sorted(INTERP_DIR.iterdir()):
        if sample_dir.is_dir() and sample_dir.name.startswith('SSBR-'):
            m = [doc for doc in DOCS if not (sample_dir / doc).exists()]
            if m:
                missing.append((sample_dir.name, m))
            else:
                complete += 1
    
    print("=" * 60)
    print("详细解读文档完整性验证")
    print("=" * 60)
    print(f"\n完整样本数: {complete}")
    print(f"不完整样本数: {len(missing)}")
    
    if missing:
        print(f"\n不完整样本详情 (前 20 个):")
        for sample_id, missing_docs in missing[:20]:
            print(f"  {sample_id}: 缺少 {', '.join(missing_docs)}")
        if len(missing) > 20:
            print(f"  ... 还有 {len(missing) - 20} 个")


if __name__ == "__main__":
    main()
