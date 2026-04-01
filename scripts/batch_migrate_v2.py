#!/usr/bin/env python3
"""
批量迁移工具 - 将解读文件从 v1.0 快速迁移到 v2.0 格式

策略：分级处理
- Phase 1: 快速格式迁移（保留原有数据，添加 v2.0 骨架结构）
- Phase 2: 按需补充曲线数据（后续手动或半自动完成）

用法:
    python scripts/batch_migrate_v2.py --dry-run          # 预览迁移
    python scripts/batch_migrate_v2.py --migrate          # 执行迁移
    python scripts/batch_migrate_v2.py --migrate --doi 10.1039/c9ra02783a  # 按 DOI 迁移
    python scripts/batch_migrate_v2.py --status           # 查看迁移状态
"""

import os
import re
import sys
import io
import yaml
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Windows Unicode 兼容
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
INTERPRETATIONS_DIR = PROJECT_ROOT / "dataset" / "interpretations"
BACKUP_DIR = PROJECT_ROOT / ".cache" / "v1_backup"
LOG_DIR = PROJECT_ROOT / ".cache" / "migration_logs"


def extract_yaml_and_content(file_path: Path) -> Tuple[dict, str]:
    """提取 YAML front matter 和 Markdown 正文"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = file_path.read_text(encoding="gbk")
    
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}, content
    
    yaml_str = match.group(1)
    markdown = match.group(2)
    
    try:
        yaml_data = yaml.safe_load(yaml_str) or {}
    except yaml.YAMLError:
        yaml_data = {}
    
    return yaml_data, markdown


def is_v2(yaml_data: dict) -> bool:
    """检测是否已经是 v2.0 格式"""
    if yaml_data.get("skill_version", "").startswith("2."):
        return True
    if "curves" in yaml_data:
        return True
    return False


def create_empty_curves_skeleton(file_type: str, yaml_data: dict) -> dict:
    """根据文件类型创建空的 curves 骨架结构"""
    curves = {}
    
    if file_type == "mechanical.md":
        # 应力-应变曲线骨架
        curves["stress_strain"] = {
            "x_axis": {"label": "应变", "unit": "%"},
            "y_axis": {"label": "应力", "unit": "MPa"},
            "data_points": [],  # 待填充
            "curve_features": {
                "modulus_100": _extract_feature(yaml_data, ["data", "stress_100", "value"], "MPa"),
                "modulus_300": _extract_feature(yaml_data, ["data", "stress_300", "value"], "MPa"),
                "tensile_strength": _extract_feature(yaml_data, ["data", "tensile_strength", "value"], "MPa"),
                "elongation_at_break": _extract_feature(yaml_data, ["data", "elongation", "value"], "%"),
            },
            "validation": {"known_points": [], "overall_quality": "pending"},
            "metadata": {"point_count": 0, "x_range": [0, 0], "y_range": [0, 0], "avg_confidence": 0}
        }
        
        # DMA 曲线骨架（如果有 DMA 数据）
        if _has_dma_data(yaml_data):
            curves["dma_tan_delta"] = {
                "x_axis": {"label": "温度", "unit": "°C"},
                "y_axis": {"label": "tan δ", "unit": "无量纲"},
                "data_points": [],
                "curve_features": {
                    "tan_delta_0C": _extract_feature(yaml_data, ["data", "tan_delta_0c", "value"], "-"),
                    "tan_delta_60C": _extract_feature(yaml_data, ["data", "tan_delta_60c", "value"], "-"),
                    "tan_delta_max": _extract_feature(yaml_data, ["data", "tan_delta_max", "value"], "-"),
                    "Tg": _extract_tg_feature(yaml_data),
                },
                "validation": {"known_points": [], "overall_quality": "pending"},
                "metadata": {"point_count": 0, "x_range": [-80, 80], "y_range": [0, 1], "avg_confidence": 0}
            }
        
        # Payne 曲线骨架（如果有 Payne 数据）
        if _has_payne_data(yaml_data):
            curves["payne_storage_modulus"] = {
                "x_axis": {"label": "应变", "unit": "%", "scale": "logarithmic"},
                "y_axis": {"label": "储能模量 G'", "unit": "MPa"},
                "data_points": [],
                "curve_features": {
                    "G_prime_0": {"value": None, "unit": "MPa", "strain_at": 0.28, "source": "pending"},
                    "G_prime_inf": {"value": None, "unit": "MPa", "strain_at": 42, "source": "pending"},
                    "delta_G_prime": _extract_feature(yaml_data, ["data", "delta_G_vulcanizates", "value"], "kPa"),
                },
                "validation": {"known_points": [], "overall_quality": "pending"},
                "metadata": {"point_count": 0, "x_range": [0.1, 100], "y_range": [0, 3], "avg_confidence": 0}
            }
    
    elif file_type == "dsc.md":
        # DSC 热流曲线骨架
        tg_value = _get_nested(yaml_data, ["data", "tg", "value"])
        curves["dsc_heat_flow"] = {
            "x_axis": {"label": "温度", "unit": "°C"},
            "y_axis": {"label": "热流", "unit": "mW/mg", "direction": "exo_up"},
            "data_points": [],
            "curve_features": {
                "Tg": {
                    "onset": None,
                    "midpoint": tg_value,
                    "endpoint": None,
                    "unit": "°C",
                    "source": "pending"
                },
                "glass_transition_width": {"value": None, "unit": "°C"},
                "crystallization_peak": {"exists": False},
                "melting_peak": {"exists": False}
            },
            "validation": {"known_points": [], "overall_quality": "pending"},
            "metadata": {"point_count": 0, "x_range": [-80, 100], "y_range": [-1, 1], "avg_confidence": 0}
        }
    
    return curves


def _get_nested(d: dict, keys: list, default=None):
    """安全获取嵌套字典值"""
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d


def _extract_feature(yaml_data: dict, keys: list, unit: str) -> dict:
    """提取特征值"""
    value = _get_nested(yaml_data, keys)
    source_keys = keys[:-1] + ["source"]
    source = _get_nested(yaml_data, source_keys, "v1.0 data")
    return {
        "value": value,
        "unit": unit,
        "source": source if source else "v1.0 data",
        "confidence": 0.95 if value is not None else None
    }


def _extract_tg_feature(yaml_data: dict) -> dict:
    """提取 Tg 特征"""
    tg = _get_nested(yaml_data, ["data", "tg_dma", "value"])
    return {
        "value": tg,
        "unit": "°C",
        "method": "peak",
        "source": _get_nested(yaml_data, ["data", "tg_dma", "source"], "v1.0 data"),
        "confidence": 0.95 if tg is not None else None
    }


def _has_dma_data(yaml_data: dict) -> bool:
    """检查是否有 DMA 数据"""
    data = yaml_data.get("data", {})
    return any(key in data for key in ["tan_delta_0c", "tan_delta_max", "tg_dma"])


def _has_payne_data(yaml_data: dict) -> bool:
    """检查是否有 Payne 数据"""
    data = yaml_data.get("data", {})
    subtypes = yaml_data.get("mechanical_subtypes", [])
    return "payne" in subtypes or any(key in data for key in ["delta_G_compounds", "delta_G_vulcanizates", "payne_effect"])


def migrate_file(file_path: Path, dry_run: bool = True) -> dict:
    """迁移单个文件到 v2.0 格式"""
    result = {
        "file": str(file_path),
        "status": "skipped",
        "message": "",
        "changes": []
    }
    
    if not file_path.exists():
        result["status"] = "error"
        result["message"] = "文件不存在"
        return result
    
    yaml_data, markdown = extract_yaml_and_content(file_path)
    
    if not yaml_data:
        result["status"] = "error"
        result["message"] = "无法解析 YAML front matter"
        return result
    
    # 检查是否已经是 v2.0
    if is_v2(yaml_data):
        result["status"] = "skipped"
        result["message"] = "已是 v2.0 格式"
        return result
    
    file_type = file_path.name
    
    # 跳过不需要曲线的文件类型
    if file_type not in ["mechanical.md", "dsc.md"]:
        result["status"] = "skipped"
        result["message"] = f"{file_type} 暂无曲线数据需求"
        return result
    
    # 创建 v2.0 结构
    yaml_data["skill_version"] = "2.0"
    yaml_data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
    result["changes"].append("添加 skill_version: 2.0")
    result["changes"].append("更新 updated_at")
    
    # 添加 curves 骨架
    curves = create_empty_curves_skeleton(file_type, yaml_data)
    if curves:
        yaml_data["curves"] = curves
        result["changes"].append(f"添加 curves 骨架: {list(curves.keys())}")
    
    # 更新 Markdown 正文（添加 v2.0 说明）
    v2_notice = "\n> **v2.0 升级说明**: 本文档已升级为 v2.0 格式，曲线数据待补充。\n"
    if "v2.0 升级说明" not in markdown and "v2.0 更新" not in markdown:
        # 在第一个 ## 之前插入说明
        if "## " in markdown:
            parts = markdown.split("## ", 1)
            markdown = parts[0] + v2_notice + "\n## " + parts[1]
        else:
            markdown = v2_notice + markdown
        result["changes"].append("添加 v2.0 升级说明")
    
    if dry_run:
        result["status"] = "preview"
        result["message"] = f"预览: {len(result['changes'])} 项变更"
    else:
        # 备份原文件
        backup_path = BACKUP_DIR / file_path.relative_to(INTERPRETATIONS_DIR)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        
        # 写入新文件
        new_content = "---\n" + yaml.dump(yaml_data, allow_unicode=True, sort_keys=False, default_flow_style=False) + "---\n" + markdown
        file_path.write_text(new_content, encoding="utf-8")
        
        result["status"] = "migrated"
        result["message"] = f"已迁移: {len(result['changes'])} 项变更"
    
    return result


def batch_migrate(dry_run: bool = True, doi_filter: str = None) -> dict:
    """批量迁移所有文件"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "dry_run": dry_run,
        "doi_filter": doi_filter,
        "summary": {"total": 0, "migrated": 0, "skipped": 0, "error": 0, "preview": 0},
        "files": []
    }
    
    for sample_dir in sorted(INTERPRETATIONS_DIR.iterdir()):
        if not sample_dir.is_dir() or sample_dir.name.startswith("TEMPLATE"):
            continue
        
        for file_name in ["mechanical.md", "dsc.md"]:
            file_path = sample_dir / file_name
            if not file_path.exists():
                continue
            
            # DOI 过滤
            if doi_filter:
                yaml_data, _ = extract_yaml_and_content(file_path)
                file_doi = yaml_data.get("source_doi", "")
                if doi_filter not in file_doi:
                    continue
            
            result = migrate_file(file_path, dry_run)
            results["files"].append(result)
            results["summary"]["total"] += 1
            results["summary"][result["status"]] += 1
    
    return results


def print_results(results: dict):
    """打印迁移结果"""
    print("\n" + "=" * 70)
    print("批量迁移结果")
    print("=" * 70)
    
    s = results["summary"]
    mode = "预览模式" if results["dry_run"] else "执行模式"
    print(f"\n📊 {mode} 统计:")
    print(f"   总文件数: {s['total']}")
    print(f"   ✅ 已迁移/预览: {s.get('migrated', 0) + s.get('preview', 0)}")
    print(f"   ⏭️  跳过: {s['skipped']}")
    print(f"   ❌ 错误: {s['error']}")
    
    if results.get("doi_filter"):
        print(f"   🔍 DOI 过滤: {results['doi_filter']}")
    
    # 显示详细结果（限制前 20 个）
    migrated = [f for f in results["files"] if f["status"] in ["migrated", "preview"]]
    if migrated:
        print(f"\n📝 变更文件 (显示前 20 个，共 {len(migrated)} 个):")
        for item in migrated[:20]:
            rel_path = Path(item["file"]).relative_to(INTERPRETATIONS_DIR)
            print(f"   • {rel_path}")
            for change in item["changes"][:3]:
                print(f"     - {change}")
    
    print("\n" + "=" * 70)


def save_log(results: dict):
    """保存迁移日志"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode = "dryrun" if results["dry_run"] else "migrate"
    log_file = LOG_DIR / f"migration_{mode}_{timestamp}.json"
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📝 日志已保存: {log_file}")


def main():
    parser = argparse.ArgumentParser(description="批量迁移 v1.0 → v2.0")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际修改文件")
    parser.add_argument("--migrate", action="store_true", help="执行迁移")
    parser.add_argument("--doi", type=str, help="按 DOI 过滤")
    parser.add_argument("--status", action="store_true", help="查看迁移状态")
    parser.add_argument("--file", type=str, help="迁移单个文件")
    
    args = parser.parse_args()
    
    if args.status:
        # 运行扫描
        os.system(f"python {PROJECT_ROOT / 'scripts' / 'batch_upgrade_v2.py'} --scan")
        return
    
    if args.file:
        # 单文件迁移
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = PROJECT_ROOT / args.file
        result = migrate_file(file_path, dry_run=not args.migrate)
        print(f"\n结果: {result}")
        return
    
    # 批量迁移
    dry_run = not args.migrate
    results = batch_migrate(dry_run=dry_run, doi_filter=args.doi)
    print_results(results)
    save_log(results)
    
    if dry_run and results["summary"].get("preview", 0) > 0:
        print("\n💡 提示: 使用 --migrate 参数执行实际迁移")


if __name__ == "__main__":
    main()
