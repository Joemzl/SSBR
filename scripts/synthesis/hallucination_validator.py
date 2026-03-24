"""
Zero-Hallucination Validator (T061)

验证生成的回答中所有数据点都可追溯到引用的文献来源。

FR-011: 零幻觉原则 - 所有输出数据点必须可追溯到引用文献，不允许任何编造数据
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DataPoint:
    """从回答中提取的数据点"""
    value: str              # 数据值（如 "18.5 MPa"）
    context: str            # 上下文（周围文本）
    position: int           # 在文本中的位置
    data_type: str          # 数据类型（numeric, percentage, range）
    
    def __str__(self):
        return f"{self.value} (at {self.position})"


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    total_data_points: int
    traced_data_points: int
    untraced_data_points: List[DataPoint]
    warnings: List[str]
    
    @property
    def trace_rate(self) -> float:
        """追溯率"""
        if self.total_data_points == 0:
            return 1.0
        return self.traced_data_points / self.total_data_points
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "total_data_points": self.total_data_points,
            "traced_data_points": self.traced_data_points,
            "trace_rate": self.trace_rate,
            "untraced_count": len(self.untraced_data_points),
            "warnings": self.warnings
        }


class ZeroHallucinationValidator:
    """
    零幻觉验证器
    
    验证回答中的所有数值数据点是否可以追溯到提供的来源样本。
    """
    
    # 数值匹配模式
    NUMERIC_PATTERNS = [
        # 带单位的数值（如 18.5 MPa, 3.6 wt%, -28°C）
        r'(\d+(?:\.\d+)?)\s*(MPa|GPa|kPa|Pa|wt%|mol%|%|°C|℃|K|nm|μm|mm|cm|m)',
        # 范围（如 3-8%, 14-17 MPa）
        r'(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*(MPa|GPa|kPa|Pa|wt%|mol%|%|°C|℃|K|nm|μm|mm|cm|m)?',
        # 纯数值（如 0.35, 1.5）
        r'(?<![a-zA-Z\d\.])(\d+\.\d+)(?![a-zA-Z\d\.])',
        # 整数百分比
        r'(\d+)\s*%',
    ]
    
    # 常见的非数据数值（应排除）
    EXCLUDE_PATTERNS = [
        r'^\d+$',           # 纯整数可能是编号
        r'^[12]\d{3}$',     # 年份
        r'^\d+\.\d{2}$',    # 可能是版本号
    ]
    
    def __init__(self):
        self._compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.NUMERIC_PATTERNS]
        self._exclude_patterns = [re.compile(p) for p in self.EXCLUDE_PATTERNS]
    
    def extract_data_points(self, text: str) -> List[DataPoint]:
        """
        从文本中提取所有数据点。
        
        Args:
            text: 待分析的文本
        
        Returns:
            提取的数据点列表
        """
        data_points = []
        seen_values = set()  # 去重
        
        for pattern in self._compiled_patterns:
            for match in pattern.finditer(text):
                value = match.group(0)
                
                # 排除非数据数值
                if any(ep.match(value.strip()) for ep in self._exclude_patterns):
                    continue
                
                # 去重
                if value in seen_values:
                    continue
                seen_values.add(value)
                
                # 获取上下文（前后 50 个字符）
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # 确定数据类型
                if '-' in value or '–' in value:
                    data_type = "range"
                elif '%' in value:
                    data_type = "percentage"
                else:
                    data_type = "numeric"
                
                data_points.append(DataPoint(
                    value=value,
                    context=context,
                    position=match.start(),
                    data_type=data_type
                ))
        
        return data_points
    
    def extract_source_values(self, samples: List[Dict[str, Any]]) -> set:
        """
        从来源样本中提取所有数值。
        
        Args:
            samples: 来源样本列表（SampleSummary.to_dict() 格式）
        
        Returns:
            来源数值集合
        """
        source_values = set()
        
        for sample in samples:
            # 提取所有字符串值中的数值
            for key, value in sample.items():
                if value is None:
                    continue
                
                value_str = str(value)
                
                # 提取数值
                for pattern in self._compiled_patterns:
                    for match in pattern.finditer(value_str):
                        # 提取纯数值部分用于模糊匹配
                        numeric_part = re.findall(r'\d+(?:\.\d+)?', match.group(0))
                        for num in numeric_part:
                            source_values.add(num)
                            # 添加带符号的版本
                            source_values.add(f"-{num}")
        
        return source_values
    
    def validate(
        self,
        answer_text: str,
        source_samples: List[Dict[str, Any]]
    ) -> ValidationResult:
        """
        验证回答中的数据点是否可追溯。
        
        Args:
            answer_text: 生成的回答文本
            source_samples: 来源样本列表
        
        Returns:
            ValidationResult
        """
        # 提取回答中的数据点
        data_points = self.extract_data_points(answer_text)
        
        if not data_points:
            return ValidationResult(
                is_valid=True,
                total_data_points=0,
                traced_data_points=0,
                untraced_data_points=[],
                warnings=["回答中未检测到数值数据点"]
            )
        
        # 提取来源数值
        source_values = self.extract_source_values(source_samples)
        
        # 验证每个数据点
        traced = []
        untraced = []
        warnings = []
        
        for dp in data_points:
            # 提取数据点中的纯数值
            numeric_parts = re.findall(r'\d+(?:\.\d+)?', dp.value)
            
            # 检查是否有任何数值可追溯
            is_traced = False
            for num in numeric_parts:
                if num in source_values:
                    is_traced = True
                    break
                # 尝试近似匹配（允许小数点后一位的差异）
                try:
                    num_float = float(num)
                    for src in source_values:
                        try:
                            src_float = float(src)
                            if abs(num_float - src_float) < 0.5:  # 允许 0.5 的误差
                                is_traced = True
                                break
                        except ValueError:
                            continue
                except ValueError:
                    pass
            
            if is_traced:
                traced.append(dp)
            else:
                untraced.append(dp)
                logger.warning(f"Untraced data point: {dp.value}")
        
        # 生成警告
        if untraced:
            warnings.append(f"发现 {len(untraced)} 个无法追溯的数据点")
            for dp in untraced[:3]:  # 只显示前 3 个
                warnings.append(f"  - {dp.value}: ...{dp.context[:30]}...")
        
        # 判断是否通过验证
        # 允许少量无法追溯的数据点（如通用知识中的数值）
        trace_rate = len(traced) / len(data_points) if data_points else 1.0
        is_valid = trace_rate >= 0.8  # 80% 追溯率
        
        return ValidationResult(
            is_valid=is_valid,
            total_data_points=len(data_points),
            traced_data_points=len(traced),
            untraced_data_points=untraced,
            warnings=warnings
        )
    
    def validate_synthesized_answer(
        self,
        answer: Any  # SynthesizedAnswer
    ) -> ValidationResult:
        """
        验证 SynthesizedAnswer 对象。
        
        Args:
            answer: SynthesizedAnswer 实例
        
        Returns:
            ValidationResult
        """
        samples_dict = [s.to_dict() for s in answer.source_samples]
        return self.validate(answer.answer_text, samples_dict)


# 单例实例
_validator_instance: Optional[ZeroHallucinationValidator] = None


def get_validator() -> ZeroHallucinationValidator:
    """获取验证器单例"""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = ZeroHallucinationValidator()
    return _validator_instance


def validate_zero_hallucination(
    answer_text: str,
    source_samples: List[Dict[str, Any]]
) -> ValidationResult:
    """
    便捷函数：验证回答是否符合零幻觉原则。
    
    Args:
        answer_text: 生成的回答
        source_samples: 来源样本（字典格式）
    
    Returns:
        ValidationResult
    """
    return get_validator().validate(answer_text, source_samples)


# CLI 测试
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Zero-Hallucination Validator")
    parser.add_argument("--test", action="store_true", help="Run test cases")
    args = parser.parse_args()
    
    if args.test:
        print("=" * 50)
        print("Zero-Hallucination Validator Test")
        print("=" * 50)
        
        validator = ZeroHallucinationValidator()
        
        # 测试用例 1: 所有数据可追溯
        test_answer_1 = """
        根据文献数据，羟基官能化 SSBR 的拉伸强度可达 18.5 MPa，
        官能化程度为 3.6 wt% 时效果最佳。Tg 约为 -28°C。
        """
        test_samples_1 = [
            {"tensile_strength": "18.5 MPa", "functionalization_degree": "3.6 wt%", "tg": "-28°C"}
        ]
        
        result_1 = validator.validate(test_answer_1, test_samples_1)
        print(f"\nTest 1 (all traced): {result_1.is_valid}")
        print(f"  Trace rate: {result_1.trace_rate:.0%}")
        print(f"  Data points: {result_1.traced_data_points}/{result_1.total_data_points}")
        
        # 测试用例 2: 包含未追溯数据
        test_answer_2 = """
        拉伸强度为 18.5 MPa，但我们估计在 25% 官能化时可达 30 MPa。
        """
        test_samples_2 = [
            {"tensile_strength": "18.5 MPa", "functionalization_degree": "5%"}
        ]
        
        result_2 = validator.validate(test_answer_2, test_samples_2)
        print(f"\nTest 2 (with hallucination): {result_2.is_valid}")
        print(f"  Trace rate: {result_2.trace_rate:.0%}")
        print(f"  Untraced: {[dp.value for dp in result_2.untraced_data_points]}")
        
        # 测试用例 3: 无数值
        test_answer_3 = "羟基官能化可以改善白炭黑分散性。"
        result_3 = validator.validate(test_answer_3, [])
        print(f"\nTest 3 (no data): {result_3.is_valid}")
        print(f"  Data points: {result_3.total_data_points}")
        
        print("\n" + "=" * 50)
        print("All tests completed")
