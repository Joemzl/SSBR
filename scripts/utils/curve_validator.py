"""
曲线数据验证模块

用于验证 YAML front matter 中的全范围曲线数据格式和完整性。

Version: 1.0.0
Date: 2026-03-31
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import yaml
import re
from pathlib import Path


class DataSource(Enum):
    """数据来源层级"""
    L1 = "L1"  # 文献表格/正文数值
    L2 = "L2"  # 图面标注数字
    L3 = "L3"  # 曲线视觉估读


class QualityLevel(Enum):
    """数据质量等级"""
    EXCELLENT = "excellent"  # < 5% 偏差
    GOOD = "good"            # 5-10% 偏差
    ACCEPTABLE = "acceptable"  # 10-15% 偏差
    POOR = "poor"            # > 15% 偏差


@dataclass
class ValidationIssue:
    """验证问题"""
    severity: str  # "error" / "warning" / "info"
    field: str
    message: str


@dataclass
class ValidationResult:
    """验证结果"""
    valid: bool
    issues: List[ValidationIssue]
    avg_confidence: float
    point_count: int
    quality: QualityLevel


# 各曲线类型的最小数据点要求
MIN_POINTS = {
    "stress_strain": 10,
    "dma_tan_delta": 12,
    "payne_storage_modulus": 8,
    "dsc_heat_flow": 10,
}

# 各曲线类型的必填特征
REQUIRED_FEATURES = {
    "stress_strain": ["modulus_100", "tensile_strength", "elongation_at_break"],
    "dma_tan_delta": ["tan_delta_0C", "tan_delta_60C", "Tg"],
    "payne_storage_modulus": ["G_prime_0", "G_prime_inf", "delta_G_prime"],
    "dsc_heat_flow": ["Tg"],
}


def validate_data_point(point: Dict[str, Any]) -> Tuple[bool, List[ValidationIssue]]:
    """
    验证单个数据点
    
    Args:
        point: 数据点字典 {x, y, confidence, source}
    
    Returns:
        (valid, issues) 元组
    """
    issues = []
    required_fields = ['x', 'y', 'confidence', 'source']
    
    # 检查必填字段
    for field in required_fields:
        if field not in point:
            issues.append(ValidationIssue(
                severity="error",
                field=f"data_point.{field}",
                message=f"缺少必填字段: {field}"
            ))
    
    if issues:
        return False, issues
    
    # 验证置信度范围
    confidence = point.get('confidence', 0)
    if not (0 <= confidence <= 1):
        issues.append(ValidationIssue(
            severity="error",
            field="data_point.confidence",
            message=f"置信度超出范围 [0, 1]: {confidence}"
        ))
    
    # 验证数据来源
    source = point.get('source', '')
    valid_sources = [s.value for s in DataSource]
    if source not in valid_sources:
        issues.append(ValidationIssue(
            severity="error",
            field="data_point.source",
            message=f"无效的数据来源: {source}，应为 {valid_sources}"
        ))
    
    # 验证数值类型
    for field in ['x', 'y']:
        value = point.get(field)
        if not isinstance(value, (int, float)):
            issues.append(ValidationIssue(
                severity="error",
                field=f"data_point.{field}",
                message=f"{field} 必须是数值类型，实际: {type(value).__name__}"
            ))
    
    return len(issues) == 0, issues


def validate_curve(curve: Dict[str, Any], curve_type: str) -> ValidationResult:
    """
    验证曲线数据完整性
    
    Args:
        curve: 曲线数据字典
        curve_type: 曲线类型标识符
    
    Returns:
        ValidationResult 对象
    """
    issues = []
    
    # 1. 检查必填顶级字段
    required_top_fields = ['x_axis', 'y_axis', 'data_points']
    for field in required_top_fields:
        if field not in curve:
            issues.append(ValidationIssue(
                severity="error",
                field=field,
                message=f"缺少必填字段: {field}"
            ))
    
    # 2. 检查数据点数量
    data_points = curve.get('data_points', [])
    min_points = MIN_POINTS.get(curve_type, 10)
    
    if len(data_points) < min_points:
        issues.append(ValidationIssue(
            severity="error",
            field="data_points",
            message=f"数据点不足，需要 {min_points}，实际 {len(data_points)}"
        ))
    
    # 3. 验证每个数据点
    confidences = []
    x_values = []
    
    for i, point in enumerate(data_points):
        valid, point_issues = validate_data_point(point)
        for issue in point_issues:
            issue.field = f"data_points[{i}].{issue.field.split('.')[-1]}"
            issues.append(issue)
        
        if valid:
            confidences.append(point['confidence'])
            x_values.append(point['x'])
    
    # 4. 检查 X 单调性
    if x_values and x_values != sorted(x_values):
        issues.append(ValidationIssue(
            severity="warning",
            field="data_points",
            message="X 值不单调递增，可能导致曲线插值问题"
        ))
    
    # 5. 检查必填曲线特征
    curve_features = curve.get('curve_features', {})
    required_features = REQUIRED_FEATURES.get(curve_type, [])
    
    for feature in required_features:
        if feature not in curve_features:
            issues.append(ValidationIssue(
                severity="error",
                field=f"curve_features.{feature}",
                message=f"缺少必填曲线特征: {feature}"
            ))
    
    # 6. 计算平均置信度
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    # 7. 交叉验证
    validation_data = curve.get('validation', {})
    known_points = validation_data.get('known_points', [])
    
    deviations = []
    for kp in known_points:
        dev = kp.get('deviation_percent', 0)
        deviations.append(abs(dev))
    
    avg_deviation = sum(deviations) / len(deviations) if deviations else 0
    
    # 8. 确定质量等级
    if avg_deviation < 5:
        quality = QualityLevel.EXCELLENT
    elif avg_deviation < 10:
        quality = QualityLevel.GOOD
    elif avg_deviation < 15:
        quality = QualityLevel.ACCEPTABLE
    else:
        quality = QualityLevel.POOR
        issues.append(ValidationIssue(
            severity="warning",
            field="validation",
            message=f"交叉验证偏差较大: {avg_deviation:.1f}%"
        ))
    
    # 构建结果
    has_errors = any(i.severity == "error" for i in issues)
    
    return ValidationResult(
        valid=not has_errors,
        issues=issues,
        avg_confidence=avg_confidence,
        point_count=len(data_points),
        quality=quality
    )


def validate_yaml_curves(yaml_content: str) -> Dict[str, ValidationResult]:
    """
    验证 YAML 文件中的所有曲线数据
    
    Args:
        yaml_content: YAML 文件内容
    
    Returns:
        {曲线类型: ValidationResult} 字典
    """
    results = {}
    
    # 解析 YAML front matter (使用正则表达式更可靠)
    if yaml_content.startswith('---'):
        # 使用正则表达式匹配 front matter: ---\n...\n---
        match = re.match(r'^---\n(.*?)\n---', yaml_content, re.DOTALL)
        if match:
            yaml_section = match.group(1)
        else:
            # 回退到 split 方法
            parts = yaml_content.split('---', 2)
            yaml_section = parts[1] if len(parts) >= 2 else yaml_content
    else:
        yaml_section = yaml_content
    
    try:
        data = yaml.safe_load(yaml_section)
    except yaml.YAMLError as e:
        return {"_parse_error": ValidationResult(
            valid=False,
            issues=[ValidationIssue(
                severity="error",
                field="_yaml",
                message=f"YAML 解析失败: {str(e)}"
            )],
            avg_confidence=0,
            point_count=0,
            quality=QualityLevel.POOR
        )}
    
    if not data:
        return {}
    
    # 验证 curves 部分
    curves = data.get('curves', {})
    
    # 处理 curves 为 None 的情况
    if curves is None:
        curves = {}
    
    for curve_type, curve_data in curves.items():
        if isinstance(curve_data, dict):
            results[curve_type] = validate_curve(curve_data, curve_type)
    
    return results


def validate_file(file_path: str) -> Dict[str, ValidationResult]:
    """
    验证文件中的曲线数据
    
    Args:
        file_path: 文件路径
    
    Returns:
        验证结果字典
    """
    path = Path(file_path)
    
    if not path.exists():
        return {"_file_error": ValidationResult(
            valid=False,
            issues=[ValidationIssue(
                severity="error",
                field="_file",
                message=f"文件不存在: {file_path}"
            )],
            avg_confidence=0,
            point_count=0,
            quality=QualityLevel.POOR
        )}
    
    content = path.read_text(encoding='utf-8')
    return validate_yaml_curves(content)


def print_validation_report(results: Dict[str, ValidationResult]) -> None:
    """打印验证报告"""
    print("\n" + "=" * 60)
    print("曲线数据验证报告")
    print("=" * 60)
    
    for curve_type, result in results.items():
        print(f"\n[CURVE] {curve_type}")
        print(f"   状态: {'[PASS] 通过' if result.valid else '[FAIL] 失败'}")
        print(f"   数据点: {result.point_count}")
        print(f"   平均置信度: {result.avg_confidence:.2f}")
        print(f"   质量等级: {result.quality.value}")
        
        if result.issues:
            print("   问题:")
            for issue in result.issues:
                icon = "[ERROR]" if issue.severity == "error" else "[WARN]" if issue.severity == "warning" else "[INFO]"
                print(f"      {icon} [{issue.severity}] {issue.field}: {issue.message}")
    
    print("\n" + "=" * 60)


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="验证曲线数据格式")
    parser.add_argument("--file", "-f", help="要验证的 Markdown 文件路径")
    parser.add_argument("--dir", "-d", help="要验证的目录（递归）")
    parser.add_argument("--quiet", "-q", action="store_true", help="只输出错误")
    
    args = parser.parse_args()
    
    if args.file:
        results = validate_file(args.file)
        print_validation_report(results)
        
        # 退出码
        has_errors = any(not r.valid for r in results.values())
        sys.exit(1 if has_errors else 0)
    
    elif args.dir:
        from pathlib import Path
        
        dir_path = Path(args.dir)
        all_valid = True
        
        for md_file in dir_path.rglob("*.md"):
            results = validate_file(str(md_file))
            
            # 检查是否有曲线数据
            has_curves = any(k not in ['_parse_error', '_file_error'] for k in results.keys())
            
            if has_curves:
                print(f"\n📄 {md_file.relative_to(dir_path)}")
                
                for curve_type, result in results.items():
                    if curve_type.startswith('_'):
                        continue
                    
                    status = '✅' if result.valid else '❌'
                    print(f"   {status} {curve_type}: {result.point_count} 点, 置信度 {result.avg_confidence:.2f}")
                    
                    if not result.valid:
                        all_valid = False
                        if not args.quiet:
                            for issue in result.issues:
                                if issue.severity == "error":
                                    print(f"      ❌ {issue.message}")
        
        sys.exit(0 if all_valid else 1)
    
    else:
        # 演示模式
        demo_yaml = """---
sample_id: "SSBR-TEST"
curves:
  stress_strain:
    x_axis:
      label: "应变"
      unit: "%"
    y_axis:
      label: "应力"
      unit: "MPa"
    data_points:
      - {x: 0, y: 0, confidence: 1.0, source: "L1"}
      - {x: 50, y: 1.2, confidence: 0.70, source: "L3"}
      - {x: 100, y: 2.5, confidence: 0.95, source: "L1"}
      - {x: 150, y: 4.1, confidence: 0.70, source: "L3"}
      - {x: 200, y: 5.8, confidence: 0.70, source: "L3"}
      - {x: 250, y: 7.0, confidence: 0.70, source: "L3"}
      - {x: 300, y: 8.2, confidence: 0.95, source: "L1"}
      - {x: 350, y: 10.5, confidence: 0.65, source: "L3"}
      - {x: 400, y: 14.2, confidence: 0.65, source: "L3"}
      - {x: 420, y: 16.8, confidence: 0.95, source: "L1"}
    curve_features:
      modulus_100:
        value: 2.5
        unit: "MPa"
        source: "L1"
      tensile_strength:
        value: 16.8
        unit: "MPa"
        source: "L1"
      elongation_at_break:
        value: 420
        unit: "%"
        source: "L1"
    validation:
      known_points:
        - {strain: 100, stress_expected: 2.5, stress_measured: 2.5, deviation_percent: 0}
      overall_quality: "good"
---
"""
        print("演示模式 - 验证示例 YAML:")
        results = validate_yaml_curves(demo_yaml)
        print_validation_report(results)
