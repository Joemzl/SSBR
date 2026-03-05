"""
Excel 读写工具
用于读取和修改 SSBR 数据 Excel 文件

Created: 2026-03-05
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from openpyxl import load_workbook, Workbook
from openpyxl.worksheet.worksheet import Worksheet
import shutil
from datetime import datetime


class ExcelHandler:
    """
    SSBR 数据 Excel 文件处理器
    
    列定义 (A-O 为元数据，P-W 为待迁移数据):
    A: 样本ID
    B: 应用场景
    C: 官能化试剂名称
    D: 试剂整体 SMILES
    E: 核心官能团 SMILES
    F: 核心官能团名称
    G: 核心官能团化学式
    H: 官能化程度 (wt%)
    I: 核磁谱图
    J: 微相分离图片表征
    K: 核心力学图谱
    L: DSC 谱图
    M: 引文
    N: DOI
    O: DOI_SI
    P: 100%定伸应力（MPa）
    Q: 200%定伸应力（MPa）
    R: 300%定伸应力（MPa）
    S: 拉伸强度（MPa）
    T: 断裂伸长率（%）
    U: 力学数据来源
    V: 玻璃化转变温度Tg（℃）
    W: 热学数据来源
    """
    
    # 列名映射
    COLUMN_MAP = {
        'sample_id': 'A',
        'application': 'B',
        'reagent_name': 'C',
        'reagent_smiles': 'D',
        'functional_group_smiles': 'E',
        'functional_group_name': 'F',
        'functional_group_formula': 'G',
        'functionalization_degree': 'H',
        'nmr_figure': 'I',
        'tem_figure': 'J',
        'mechanical_figure': 'K',
        'dsc_figure': 'L',
        'citation': 'M',
        'doi': 'N',
        'doi_si': 'O',
        # 待迁移的数值列
        'stress_100': 'P',
        'stress_200': 'Q',
        'stress_300': 'R',
        'tensile_strength': 'S',
        'elongation': 'T',
        'mechanical_source': 'U',
        'tg': 'V',
        'thermal_source': 'W',
    }
    
    # 反向映射
    COLUMN_TO_FIELD = {v: k for k, v in COLUMN_MAP.items()}
    
    def __init__(self, excel_path: Path | str):
        """
        初始化 Excel 处理器
        
        Args:
            excel_path: Excel 文件路径
        """
        self.path = Path(excel_path)
        if not self.path.exists():
            raise FileNotFoundError(f"Excel 文件不存在: {self.path}")
        
        self.workbook: Optional[Workbook] = None
        self.worksheet: Optional[Worksheet] = None
    
    def open(self) -> 'ExcelHandler':
        """打开 Excel 文件"""
        self.workbook = load_workbook(self.path)
        self.worksheet = self.workbook.active
        return self
    
    def close(self) -> None:
        """关闭 Excel 文件"""
        if self.workbook:
            self.workbook.close()
            self.workbook = None
            self.worksheet = None
    
    def __enter__(self) -> 'ExcelHandler':
        return self.open()
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
    
    def get_cell_value(self, row: int, column: str) -> Any:
        """
        获取单元格值
        
        Args:
            row: 行号 (从 1 开始，1 为表头)
            column: 列字母 (如 'A', 'P')
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        return self.worksheet[f"{column}{row}"].value
    
    def set_cell_value(self, row: int, column: str, value: Any) -> None:
        """
        设置单元格值
        
        Args:
            row: 行号
            column: 列字母
            value: 值
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        self.worksheet[f"{column}{row}"] = value
    
    def get_row_data(self, row: int) -> Dict[str, Any]:
        """
        获取一行的所有数据
        
        Args:
            row: 行号 (数据从第 2 行开始，第 1 行为表头)
            
        Returns:
            字段名到值的字典
        """
        data = {}
        for field, col in self.COLUMN_MAP.items():
            value = self.get_cell_value(row, col)
            data[field] = value
        return data
    
    def get_sample_data(self, sample_id: str) -> Optional[Dict[str, Any]]:
        """
        根据样本 ID 获取数据
        
        Args:
            sample_id: 样本 ID (如 'SSBR-001')
            
        Returns:
            样本数据字典，未找到返回 None
        """
        row = self.find_sample_row(sample_id)
        if row:
            return self.get_row_data(row)
        return None
    
    def find_sample_row(self, sample_id: str) -> Optional[int]:
        """
        查找样本所在行号
        
        Args:
            sample_id: 样本 ID
            
        Returns:
            行号，未找到返回 None
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        
        for row in range(2, self.worksheet.max_row + 1):
            cell_value = self.get_cell_value(row, 'A')
            if cell_value == sample_id:
                return row
        return None
    
    def get_all_samples(self) -> List[Dict[str, Any]]:
        """
        获取所有样本数据
        
        Returns:
            样本数据列表
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        
        samples = []
        for row in range(2, self.worksheet.max_row + 1):
            sample_id = self.get_cell_value(row, 'A')
            if sample_id:  # 跳过空行
                samples.append(self.get_row_data(row))
        return samples
    
    def get_metadata_fields(self, sample_id: str) -> Dict[str, Any]:
        """
        获取样本的元数据字段 (A-O 列)
        
        Args:
            sample_id: 样本 ID
            
        Returns:
            元数据字典
        """
        data = self.get_sample_data(sample_id)
        if not data:
            return {}
        
        # 只返回 A-O 列的数据
        metadata_fields = [
            'sample_id', 'application', 'reagent_name', 'reagent_smiles',
            'functional_group_smiles', 'functional_group_name', 
            'functional_group_formula', 'functionalization_degree',
            'nmr_figure', 'tem_figure', 'mechanical_figure', 'dsc_figure',
            'citation', 'doi', 'doi_si'
        ]
        return {k: data[k] for k in metadata_fields if k in data}
    
    def get_migration_data(self, sample_id: str) -> Dict[str, Any]:
        """
        获取待迁移的数据字段 (P-W 列)
        
        Args:
            sample_id: 样本 ID
            
        Returns:
            迁移数据字典，分为 mechanical 和 dsc 两部分
        """
        data = self.get_sample_data(sample_id)
        if not data:
            return {}
        
        return {
            'mechanical': {
                'stress_100': data.get('stress_100'),
                'stress_200': data.get('stress_200'),
                'stress_300': data.get('stress_300'),
                'tensile_strength': data.get('tensile_strength'),
                'elongation': data.get('elongation'),
                'mechanical_source': data.get('mechanical_source'),
            },
            'dsc': {
                'tg': data.get('tg'),
                'thermal_source': data.get('thermal_source'),
            }
        }
    
    def delete_columns(self, columns: List[str]) -> None:
        """
        删除指定列
        
        Args:
            columns: 要删除的列字母列表 (如 ['P', 'Q', 'R'])
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        
        # 从后往前删除，避免索引变化
        sorted_cols = sorted(columns, key=lambda x: ord(x), reverse=True)
        for col in sorted_cols:
            col_idx = ord(col) - ord('A') + 1
            self.worksheet.delete_cols(col_idx)
    
    def save(self, path: Optional[Path | str] = None) -> None:
        """
        保存 Excel 文件
        
        Args:
            path: 保存路径，默认为原路径
        """
        if not self.workbook:
            raise RuntimeError("Excel 文件未打开")
        
        save_path = Path(path) if path else self.path
        self.workbook.save(save_path)
    
    @staticmethod
    def backup(excel_path: Path | str, backup_dir: Optional[Path | str] = None) -> Path:
        """
        备份 Excel 文件
        
        Args:
            excel_path: Excel 文件路径
            backup_dir: 备份目录，默认为原目录
            
        Returns:
            备份文件路径
        """
        source = Path(excel_path)
        if not source.exists():
            raise FileNotFoundError(f"文件不存在: {source}")
        
        backup_folder = Path(backup_dir) if backup_dir else source.parent
        backup_folder.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source.stem}_backup_{timestamp}{source.suffix}"
        backup_path = backup_folder / backup_name
        
        shutil.copy2(source, backup_path)
        return backup_path


if __name__ == '__main__':
    # 简单测试
    print("ExcelHandler 模块测试")
    print("使用方法:")
    print("  with ExcelHandler('dataset/数据.xlsx') as excel:")
    print("      data = excel.get_sample_data('SSBR-001')")
