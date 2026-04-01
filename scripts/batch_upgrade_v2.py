#!/usr/bin/env python3
"""
批量升级工具 - 将解读文件从 v1.0 升级到 v2.0（全范围曲线数据）

功能:
1. 扫描所有解读文件，检测 v1.0/v2.0 状态
2. 按文献 DOI 分组，便于批量处理同一文献的样本
3. 生成升级报告和优先级列表
4. 支持增量升级

用法:
    python scripts/batch_upgrade_v2.py --scan              # 扫描并生成报告
    python scripts/batch_upgrade_v2.py --report            # 查看当前状态报告
    python scripts/batch_upgrade_v2.py --group-by-doi      # 按 DOI 分组显示
    python scripts/batch_upgrade_v2.py --validate          # 验证所有 v2.0 文件
"""

import os
import re
import sys
import io
import yaml
import json
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Windows Unicode 兼容
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
INTERPRETATIONS_DIR = PROJECT_ROOT / "dataset" / "interpretations"
EXCEL_PATH = PROJECT_ROOT / "dataset" / "数据.xlsx"
REPORT_PATH = PROJECT_ROOT / ".cache" / "upgrade_report.json"

# 曲线类型映射
CURVE_TYPES = {
    "mechanical.md": ["stress_strain", "dma_tan_delta", "payne_storage_modulus"],
    "dsc.md": ["dsc_heat_flow"],
    "nmr.md": [],  # NMR 暂无曲线数据定义
    "tem.md": [],  # TEM 暂无曲线数据定义
}

# 最小数据点要求
MIN_POINTS = {
    "stress_strain": 10,
    "dma_tan_delta": 12,
    "payne_storage_modulus": 8,
    "dsc_heat_flow": 10,
}


def extract_yaml_front_matter(file_path: Path) -> dict:
    """从 Markdown 文件中提取 YAML front matter"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = file_path.read_text(encoding="gbk")
    
    # 使用正则提取 YAML front matter
    pattern = r'^---\s*\n(.*?)\n---'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}
    
    yaml_content = match.group(1)
    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return {}


def detect_version(yaml_data: dict) -> str:
    """检测文件版本"""
    # 检查 skill_version 字段
    skill_version = yaml_data.get("skill_version", "")
    if skill_version and skill_version.startswith("2."):
        return "v2.0"
    
    # 检查是否有 curves 字段
    if "curves" in yaml_data:
        return "v2.0"
    
    # 检查 data 中是否有 curves
    data = yaml_data.get("data", {})
    if isinstance(data, dict) and "curves" in data:
        return "v2.0"
    
    return "v1.0"


def count_curve_points(yaml_data: dict) -> dict:
    """统计各曲线类型的数据点数"""
    result = {}
    
    # 检查顶层 curves
    curves = yaml_data.get("curves", {})
    if not curves:
        # 检查 data.curves
        data = yaml_data.get("data", {})
        if isinstance(data, dict):
            curves = data.get("curves", {})
    
    for curve_type, curve_data in curves.items():
        if isinstance(curve_data, dict):
            data_points = curve_data.get("data_points", [])
            result[curve_type] = len(data_points)
    
    return result


def scan_all_files() -> list:
    """扫描所有解读文件"""
    results = []
    
    for sample_dir in sorted(INTERPRETATIONS_DIR.iterdir()):
        if not sample_dir.is_dir():
            continue
        if sample_dir.name.startswith("TEMPLATE"):
            continue
        
        sample_id = sample_dir.name
        
        for file_name in ["mechanical.md", "dsc.md", "nmr.md", "tem.md"]:
            file_path = sample_dir / file_name
            if not file_path.exists():
                continue
            
            yaml_data = extract_yaml_front_matter(file_path)
            version = detect_version(yaml_data)
            curve_points = count_curve_points(yaml_data)
            
            # 提取关键信息
            source_doi = yaml_data.get("source_doi", "")
            source_figure = yaml_data.get("source_figure", "")
            interpretation_type = yaml_data.get("interpretation_type", file_name.replace(".md", ""))
            
            # 确定需要的曲线类型
            expected_curves = CURVE_TYPES.get(file_name, [])
            
            # 计算升级状态
            if version == "v2.0":
                # 检查曲线数据完整性
                missing_curves = []
                for curve_type in expected_curves:
                    if curve_type not in curve_points:
                        missing_curves.append(curve_type)
                    elif curve_points[curve_type] < MIN_POINTS.get(curve_type, 10):
                        missing_curves.append(f"{curve_type}(点数不足)")
                
                if missing_curves:
                    status = "v2.0-incomplete"
                else:
                    status = "v2.0-complete"
            else:
                if expected_curves:
                    status = "v1.0-needs-upgrade"
                else:
                    status = "v1.0-no-curves"  # 如 nmr, tem 暂无曲线要求
            
            results.append({
                "sample_id": sample_id,
                "file_name": file_name,
                "file_path": str(file_path),
                "version": version,
                "status": status,
                "source_doi": source_doi,
                "source_figure": source_figure,
                "interpretation_type": interpretation_type,
                "curve_points": curve_points,
                "expected_curves": expected_curves,
            })
    
    return results


def generate_report(results: list) -> dict:
    """生成升级报告"""
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_files": len(results),
            "v1_needs_upgrade": 0,
            "v1_no_curves": 0,
            "v2_complete": 0,
            "v2_incomplete": 0,
        },
        "by_type": defaultdict(lambda: {"v1": 0, "v2": 0, "total": 0}),
        "by_doi": defaultdict(list),
        "upgrade_queue": [],
        "completed": [],
    }
    
    for item in results:
        status = item["status"]
        file_type = item["file_name"]
        doi = item["source_doi"] or "unknown"
        
        # 更新汇总
        if status == "v1.0-needs-upgrade":
            report["summary"]["v1_needs_upgrade"] += 1
            report["by_type"][file_type]["v1"] += 1
            report["upgrade_queue"].append(item)
        elif status == "v1.0-no-curves":
            report["summary"]["v1_no_curves"] += 1
            report["by_type"][file_type]["v1"] += 1
        elif status == "v2.0-complete":
            report["summary"]["v2_complete"] += 1
            report["by_type"][file_type]["v2"] += 1
            report["completed"].append(item)
        elif status == "v2.0-incomplete":
            report["summary"]["v2_incomplete"] += 1
            report["by_type"][file_type]["v2"] += 1
            report["upgrade_queue"].append(item)
        
        report["by_type"][file_type]["total"] += 1
        
        # 按 DOI 分组
        report["by_doi"][doi].append({
            "sample_id": item["sample_id"],
            "file_name": item["file_name"],
            "status": status,
        })
    
    # 转换 defaultdict 为普通 dict
    report["by_type"] = dict(report["by_type"])
    report["by_doi"] = dict(report["by_doi"])
    
    return report


def print_summary(report: dict):
    """打印汇总报告"""
    print("\n" + "=" * 70)
    print("全范围曲线数据升级状态报告")
    print("=" * 70)
    
    summary = report["summary"]
    print(f"\n📊 总体统计:")
    print(f"   总文件数: {summary['total_files']}")
    print(f"   ✅ v2.0 完整: {summary['v2_complete']}")
    print(f"   ⚠️  v2.0 不完整: {summary['v2_incomplete']}")
    print(f"   🔄 v1.0 待升级: {summary['v1_needs_upgrade']}")
    print(f"   ⏸️  v1.0 无曲线需求: {summary['v1_no_curves']}")
    
    print(f"\n📁 按文件类型:")
    for file_type, counts in report["by_type"].items():
        v2_pct = (counts["v2"] / counts["total"] * 100) if counts["total"] > 0 else 0
        print(f"   {file_type}: v1={counts['v1']}, v2={counts['v2']}, 升级率={v2_pct:.1f}%")
    
    # 打印优先级队列前 10 个
    queue = report["upgrade_queue"]
    if queue:
        print(f"\n🔄 升级队列 (共 {len(queue)} 个, 显示前 10 个):")
        for i, item in enumerate(queue[:10], 1):
            print(f"   {i}. {item['sample_id']}/{item['file_name']} [{item['status']}]")
    
    print("\n" + "=" * 70)


def print_doi_groups(report: dict):
    """按 DOI 分组打印"""
    print("\n" + "=" * 70)
    print("按文献 DOI 分组（便于批量处理同一文献的样本）")
    print("=" * 70)
    
    for doi, samples in sorted(report["by_doi"].items()):
        v1_count = sum(1 for s in samples if s["status"].startswith("v1"))
        v2_count = sum(1 for s in samples if s["status"].startswith("v2"))
        
        print(f"\n📄 DOI: {doi}")
        print(f"   样本数: {len(samples)} (v1: {v1_count}, v2: {v2_count})")
        
        # 按状态分组显示
        needs_upgrade = [s for s in samples if "needs-upgrade" in s["status"] or "incomplete" in s["status"]]
        if needs_upgrade:
            print(f"   待升级:")
            for s in needs_upgrade:
                print(f"      - {s['sample_id']}/{s['file_name']}")


def validate_v2_files(results: list) -> dict:
    """验证所有 v2.0 文件"""
    # 动态导入 curve_validator
    sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "utils"))
    try:
        from curve_validator import validate_file
    except ImportError:
        print("⚠️ 无法导入 curve_validator，跳过验证")
        return {"error": "curve_validator not found"}
    
    validation_results = {
        "passed": [],
        "failed": [],
        "skipped": [],
    }
    
    v2_files = [r for r in results if r["version"] == "v2.0"]
    
    for item in v2_files:
        file_path = Path(item["file_path"])
        try:
            result = validate_file(file_path)
            if result.get("valid", False):
                validation_results["passed"].append(item["sample_id"] + "/" + item["file_name"])
            else:
                validation_results["failed"].append({
                    "file": item["sample_id"] + "/" + item["file_name"],
                    "issues": result.get("issues", []),
                })
        except Exception as e:
            validation_results["skipped"].append({
                "file": item["sample_id"] + "/" + item["file_name"],
                "error": str(e),
            })
    
    return validation_results


def save_report(report: dict):
    """保存报告到缓存"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📝 报告已保存到: {REPORT_PATH}")


def load_report() -> dict:
    """加载缓存的报告"""
    if REPORT_PATH.exists():
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def main():
    parser = argparse.ArgumentParser(description="批量升级工具 - v1.0 到 v2.0")
    parser.add_argument("--scan", action="store_true", help="扫描所有文件并生成报告")
    parser.add_argument("--report", action="store_true", help="查看当前状态报告")
    parser.add_argument("--group-by-doi", action="store_true", help="按 DOI 分组显示")
    parser.add_argument("--validate", action="store_true", help="验证所有 v2.0 文件")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    if args.scan or not any([args.report, args.group_by_doi, args.validate]):
        print("🔍 扫描所有解读文件...")
        results = scan_all_files()
        report = generate_report(results)
        save_report(report)
        
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print_summary(report)
    
    elif args.report:
        report = load_report()
        if report:
            print_summary(report)
        else:
            print("⚠️ 未找到缓存报告，请先运行 --scan")
    
    elif args.group_by_doi:
        report = load_report()
        if report:
            print_doi_groups(report)
        else:
            print("⚠️ 未找到缓存报告，请先运行 --scan")
    
    elif args.validate:
        print("🔍 扫描并验证所有 v2.0 文件...")
        results = scan_all_files()
        validation = validate_v2_files(results)
        
        print(f"\n✅ 通过: {len(validation.get('passed', []))} 个")
        print(f"❌ 失败: {len(validation.get('failed', []))} 个")
        print(f"⏭️ 跳过: {len(validation.get('skipped', []))} 个")
        
        if validation.get("failed"):
            print("\n失败的文件:")
            for item in validation["failed"]:
                print(f"  - {item['file']}: {item.get('issues', [])}")


if __name__ == "__main__":
    main()
