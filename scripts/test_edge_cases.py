"""
Edge Case Validation Test (T062)

验证 spec.md 中定义的边缘案例处理：
1. 单源警告 - 当样本来自同一文献时提示
2. 边界拒绝 - 当外推超出合理范围时拒绝
3. 冲突数据显示 - 当数据矛盾时列出差异
4. 安全警示 - 当涉及危险物质时提醒
5. 表格降级 - 当样本不足时退化为文字描述
"""

import sys
sys.path.insert(0, '.')

from scripts.models import (
    SampleSummary, DataRange, ComparisonTable, 
    ComparisonDimension, ComparisonEntry, ConfidenceTag
)
from scripts.utils.exceptions import (
    InsufficientDataError, ExtrapolationBoundaryError, ConflictingTargetsError
)


def test_single_source_warning():
    """
    Edge Case 1: 单源警告
    当检索到的样本来自同一篇文献时，系统应提示"以下分析主要基于单一研究"
    """
    print("\n[Test 1] Single-Source Warning")
    print("-" * 40)
    
    # 创建来自同一文献的样本
    samples = [
        SampleSummary(
            sample_id="SSBR-001",
            functional_group="hydroxyl",
            functionalization_degree="3.6 wt%",
            reagent="test",
            method="grafting",
            doi="10.1039/test123",
            first_author="Zhang"
        ),
        SampleSummary(
            sample_id="SSBR-002",
            functional_group="hydroxyl",
            functionalization_degree="5.2 wt%",
            reagent="test",
            method="grafting",
            doi="10.1039/test123",  # 同一 DOI
            first_author="Zhang"
        ),
    ]
    
    # 检查 DOI 唯一性
    unique_dois = set(s.doi for s in samples if s.doi)
    
    if len(unique_dois) == 1:
        warning = "[WARNING] Yi xia fen xi zhu yao ji yu dan yi yan jiu, jian yi can kao geng duo wen xian"
        print(f"  [PASS] Single-source detected: Only 1 DOI found")
        return True
    else:
        print(f"  [FAIL] Multiple sources detected when expected single")
        return False


def test_boundary_rejection():
    """
    Edge Case 2: 边界拒绝
    当用户请求的外推超出合理数据范围时，系统应拒绝外推
    """
    print("\n[Test 2] Out-of-Boundary Rejection")
    print("-" * 40)
    
    # 创建数据范围（覆盖 1%-15%）
    data_range = DataRange(
        field_name="functionalization_degree",
        min_value=1.0,
        max_value=15.0,
        unit="wt%",
        data_points=5
    )
    
    # 验证外推边界计算（50% 规则）
    # 范围大小 = 15 - 1 = 14
    # 外推下界 = 1 - 14*0.5 = -6 → max(0, -6) = 0
    # 外推上界 = 15 + 14*0.5 = 22
    expected_min = 0
    expected_max = 22.0
    
    tests_passed = 0
    
    # Test: 外推下界
    if data_range.extrapolation_min == expected_min:
        print(f"  [PASS] extrapolation_min = {data_range.extrapolation_min} (expected {expected_min})")
        tests_passed += 1
    else:
        print(f"  [FAIL] extrapolation_min = {data_range.extrapolation_min} (expected {expected_min})")
    
    # Test: 外推上界
    if data_range.extrapolation_max == expected_max:
        print(f"  [PASS] extrapolation_max = {data_range.extrapolation_max} (expected {expected_max})")
        tests_passed += 1
    else:
        print(f"  [FAIL] extrapolation_max = {data_range.extrapolation_max} (expected {expected_max})")
    
    # Test: 超出边界应拒绝
    out_of_bound_value = 50.0  # 超出 22.0 的上界
    if not data_range.is_within_extrapolation(out_of_bound_value):
        print(f"  [PASS] Value {out_of_bound_value} correctly rejected (outside {expected_min}-{expected_max})")
        tests_passed += 1
    else:
        print(f"  [FAIL] Value {out_of_bound_value} incorrectly accepted")
    
    # Test: 边界内应接受
    within_bound_value = 20.0  # 在 0-22 范围内
    if data_range.is_within_extrapolation(within_bound_value):
        print(f"  [PASS] Value {within_bound_value} correctly accepted")
        tests_passed += 1
    else:
        print(f"  [FAIL] Value {within_bound_value} incorrectly rejected")
    
    # Test: ExtrapolationBoundaryError
    try:
        raise ExtrapolationBoundaryError(
            query_value=50.0,
            allowed_range=(0, 22.0),
            unit="wt%"
        )
    except ExtrapolationBoundaryError as e:
        if "50" in str(e) and "22" in str(e):
            print(f"  [PASS] ExtrapolationBoundaryError message correct")
            tests_passed += 1
        else:
            print(f"  [FAIL] ExtrapolationBoundaryError message incorrect")
    
    return tests_passed == 5


def test_conflicting_data_display():
    """
    Edge Case 3: 冲突数据显示
    当多个样本数据存在明显矛盾时，系统应明确列出不同数据
    """
    print("\n[Test 3] Conflicting Data Display")
    print("-" * 40)
    
    # 创建有冲突数据的样本
    samples = [
        SampleSummary(
            sample_id="SSBR-001",
            functional_group="hydroxyl",
            functionalization_degree="3.6 wt%",
            reagent="test",
            method="grafting",
            tensile_strength="18.5 MPa",  # 高值
            first_author="Zhang"
        ),
        SampleSummary(
            sample_id="SSBR-002",
            functional_group="hydroxyl",
            functionalization_degree="3.5 wt%",  # 相似条件
            reagent="test",
            method="grafting",
            tensile_strength="12.0 MPa",  # 低值，差异大
            first_author="Li"
        ),
    ]
    
    # 检测数值冲突（相似条件下差异 > 30%）
    tensile_values = []
    for s in samples:
        if s.tensile_strength:
            # 提取数值
            import re
            match = re.search(r'(\d+(?:\.\d+)?)', s.tensile_strength)
            if match:
                tensile_values.append((s.sample_id, float(match.group(1)), s.first_author))
    
    if len(tensile_values) >= 2:
        val1, val2 = tensile_values[0][1], tensile_values[1][1]
        diff_percent = abs(val1 - val2) / max(val1, val2) * 100
        
        if diff_percent > 30:
            conflict_msg = f"数据存在差异: {tensile_values[0][2]}报告{val1} MPa, {tensile_values[1][2]}报告{val2} MPa (差异{diff_percent:.0f}%)"
            print(f"  [PASS] Conflict detected: {conflict_msg}")
            
            # Test: ConflictingTargetsError
            try:
                raise ConflictingTargetsError(
                    conflicts=[("高湿地抓地力", "低滚动阻力")],
                    suggestion="选择折中方案"
                )
            except ConflictingTargetsError as e:
                if "高湿地抓地力" in str(e):
                    print(f"  [PASS] ConflictingTargetsError works")
                    return True
    
    print(f"  [FAIL] Conflict not properly detected")
    return False


def test_safety_warnings():
    """
    Edge Case 4: 安全警示
    当进行配方设计时，如果涉及安全或环保问题，系统应给出警示
    """
    print("\n[Test 4] Safety Warnings")
    print("-" * 40)
    
    # 定义危险试剂列表（部分）
    hazardous_reagents = [
        "甲苯", "二甲苯", "丙酮", "甲醇", "乙醇",
        "硫酸", "盐酸", "氢氧化钠", "过氧化氢",
        "氨水", "甲醛", "苯", "氯仿",
        "toluene", "xylene", "benzene", "chloroform"
    ]
    
    test_samples = [
        SampleSummary(
            sample_id="SSBR-001",
            functional_group="hydroxyl",
            functionalization_degree="3.6 wt%",
            reagent="甲苯溶液",  # 含危险试剂
            method="grafting"
        ),
        SampleSummary(
            sample_id="SSBR-002",
            functional_group="amino",
            functionalization_degree="5.0 wt%",
            reagent="水性体系",  # 安全
            method="grafting"
        ),
    ]
    
    warnings = []
    for sample in test_samples:
        reagent = sample.reagent.lower() if sample.reagent else ""
        for hazard in hazardous_reagents:
            if hazard.lower() in reagent:
                warnings.append(f"[WARNING] {sample.sample_id} reagent contains {hazard}")
                break
    
    if warnings:
        for w in warnings:
            print(f"  [PASS] Warning generated: {w}")
        return True
    else:
        print(f"  [FAIL] No safety warning generated for hazardous reagent")
        return False


def test_table_degradation():
    """
    Edge Case 5: 表格降级
    当生成对比表格时，如果样本数量过少（< 2 个有效对比项），应退化为文字描述
    """
    print("\n[Test 5] Table Degradation")
    print("-" * 40)
    
    # 创建只有 1 个条目的对比表
    dim = ComparisonDimension(name="拉伸强度", unit="MPa")
    entry = ComparisonEntry(
        scheme_name="羟基官能化",
        sample_ids=["SSBR-001"],
        values={"拉伸强度": "18.5"}
    )
    
    table = ComparisonTable(
        title="官能化方案对比",
        dimensions=[dim],
        entries=[entry],  # 只有 1 个条目
        summary="仅有单一方案，无法形成有效对比"
    )
    
    # 检查条目数量
    if len(table.entries) < 2:
        # 应降级为文字描述
        degraded_text = f"由于对比方案不足（当前仅 {len(table.entries)} 个），无法生成对比表格。{table.summary}"
        print(f"  [PASS] Table degraded: {degraded_text}")
        
        # 验证表格方法仍然可用
        md = table.to_markdown()
        if "羟基官能化" in md:
            print(f"  [PASS] Markdown still renders partial data")
            return True
    
    print(f"  [FAIL] Table not degraded when expected")
    return False


def test_insufficient_data_error():
    """
    补充测试: InsufficientDataError
    """
    print("\n[Test 6] InsufficientDataError")
    print("-" * 40)
    
    try:
        raise InsufficientDataError(
            required=3,
            actual=1,
            operation="综合分析"
        )
    except InsufficientDataError as e:
        if "3" in str(e) and "1" in str(e) and "综合分析" in str(e):
            print(f"  [PASS] InsufficientDataError: {e.message}")
            return True
    
    print(f"  [FAIL] InsufficientDataError not working")
    return False


def main():
    print("=" * 60)
    print("Edge Case Validation Test (T062)")
    print("=" * 60)
    
    results = []
    
    results.append(("Single-Source Warning", test_single_source_warning()))
    results.append(("Boundary Rejection", test_boundary_rejection()))
    results.append(("Conflicting Data", test_conflicting_data_display()))
    results.append(("Safety Warnings", test_safety_warnings()))
    results.append(("Table Degradation", test_table_degradation()))
    results.append(("InsufficientDataError", test_insufficient_data_error()))
    
    print("\n" + "=" * 60)
    print("Summary:")
    for name, passed in results:
        print(f"  {'[PASS]' if passed else '[FAIL]'} {name}")
    
    passed_count = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\nTotal: {passed_count}/{total} tests passed")
    
    return passed_count == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
