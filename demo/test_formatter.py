"""测试 data_formatter 的解析功能 - 覆盖所有 YAML 格式"""
import pathlib
import sys
sys.stdout.reconfigure(encoding='utf-8')

from data_formatter import parse_summary_content

def test_sample(sample_id: str, expected_type: str):
    """测试单个样本的解析"""
    path = pathlib.Path(f"../dataset/interpretations/{sample_id}/summary.md")
    if not path.exists():
        print(f"  [X] 文件不存在: {path}")
        return False
    
    content = path.read_text(encoding='utf-8')
    result = parse_summary_content(content)
    
    fg = result['functional_group']
    reagent = result['reagent']
    source = result['source']
    
    # 检查是否还是默认值
    is_unknown = fg == '未知官能化' or reagent == '未知' or source == '未知来源'
    status = "[!] FAIL" if is_unknown else "[OK]"
    
    print(f"{status} {sample_id} ({expected_type})")
    print(f"      官能团: {fg}")
    print(f"      试剂: {reagent}")
    print(f"      来源: {source[:50]}..." if len(source) > 50 else f"      来源: {source}")
    
    return not is_unknown


def test_all_samples():
    """测试所有样本"""
    import os
    
    base_dir = pathlib.Path("../dataset/interpretations")
    all_dirs = sorted([d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith("SSBR-")])
    
    success_count = 0
    fail_count = 0
    failed_samples = []
    
    for sample_dir in all_dirs:
        summary_path = sample_dir / "summary.md"
        if not summary_path.exists():
            continue
        
        content = summary_path.read_text(encoding='utf-8')
        result = parse_summary_content(content)
        
        fg = result['functional_group']
        reagent = result['reagent']
        source = result['source']
        
        # 检查是否还是默认值
        has_issues = []
        # 只有来源是必须的
        if source == '未知来源':
            has_issues.append("来源")
        
        # 官能团和试剂是可选的（数据源可能没有）
        # 但如果两者都是未知，则标记为需要检查
        if fg == '未知官能化' and reagent == '未知':
            has_issues.append("官能团+试剂")
        
        if has_issues:
            fail_count += 1
            failed_samples.append((sample_dir.name, has_issues, fg, reagent, source[:30]))
        else:
            success_count += 1
    
    return success_count, fail_count, failed_samples


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # 测试所有样本
        print("=" * 60)
        print("测试所有样本")
        print("=" * 60)
        
        success, fail, failed = test_all_samples()
        print(f"\n总计: {success + fail} 个样本")
        print(f"成功: {success} 个")
        print(f"失败: {fail} 个")
        
        if failed:
            print(f"\n失败样本详情:")
            for sample_id, issues, fg, reagent, source in failed[:20]:  # 只显示前20个
                print(f"  {sample_id}: 缺少 {', '.join(issues)}")
                print(f"    官能团={fg}, 试剂={reagent}, 来源={source}")
            if len(failed) > 20:
                print(f"  ... 还有 {len(failed) - 20} 个")
    else:
        # 默认测试
        print("=" * 60)
        print("测试 data_formatter.py - 覆盖所有 YAML 格式")
        print("=" * 60)
        
        success_count = 0
        total_count = 0
        
        # 测试不同格式
        test_cases = [
            # 格式 A: 正文 Markdown (SSBR-001, SSBR-002)
            ("SSBR-001", "格式A - 正文Markdown"),
            ("SSBR-002", "格式A - 正文Markdown"),
            
            # 格式 B: YAML functionalizing_agent (SSBR-030)
            ("SSBR-030", "格式B - YAML functionalizing_agent"),
            
            # 格式 C: YAML polymer_type 未官能化 (SSBR-070)
            ("SSBR-070", "格式C - polymer_type 未官能化"),
            
            # 格式 D: YAML functionalization: 无 (SSBR-009, SSBR-010)
            ("SSBR-009", "格式D - functionalization: 无"),
            ("SSBR-010", "格式D - functionalization: 无"),
            
            # 格式 E: YAML 顶层 functional_group (SSBR-021)
            ("SSBR-021", "格式E - 顶层 functional_group"),
            ("SSBR-015", "格式E - 顶层 functional_group"),
            
            # 格式 F: YAML polymer 嵌套 (SSBR-050)
            ("SSBR-050", "格式F - polymer 嵌套"),
            
            # 格式 G: 填料改性 (SSBR-040)
            ("SSBR-040", "格式G - 填料改性"),
        ]
        
        for sample_id, expected_type in test_cases:
            total_count += 1
            if test_sample(sample_id, expected_type):
                success_count += 1
            print()
        
        print("=" * 60)
        print(f"测试结果: {success_count}/{total_count} 通过")
        if success_count == total_count:
            print("[OK] 所有测试通过!")
        else:
            print(f"[!] {total_count - success_count} 个测试失败")
        
        print("\n提示: 使用 'python test_formatter.py --all' 测试所有样本")
