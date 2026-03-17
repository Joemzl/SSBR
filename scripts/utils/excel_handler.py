"""
Excel 读写工具
用于读取和修改 SSBR 数据 Excel 文件

Created: 2026-03-05
Updated: 2026-03-14 - 扩展为 23 列新结构
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
    
    列定义 (A-X 共 24 列):
    A: 样本ID
    B: 是否是 SSBR
    C: 是否是链中官能化
    D: 苯乙烯含量_wt%
    E: 乙烯基含量_mol%
    F: 数均分子量 (Mn)
    G: 应用场景
    H: 官能化试剂名称
    I: 试剂整体 SMILES
    J: 接枝反应基团
    K: 接枝反应基团 SMILES  ← 新增
    L: 核心官能团 SMILES
    M: 核心官能团名称
    N: 核心官能团化学式
    O: 官能化程度_原始数值
    P: 官能化程度_原始单位
    Q: 高分子指纹描述符
    R: 核磁谱图
    S: 微相分离图片表征
    T: 核心力学图谱
    U: DSC 谱图
    V: 引文
    W: DOI
    X: DOI_SI
    """
    
    # 列名映射（新 24 列结构）
    COLUMN_MAP = {
        'sample_id': 'A',
        'is_ssbr': 'B',
        'is_inchain_functionalization': 'C',
        'styrene_content': 'D',
        'vinyl_content': 'E',
        'mn': 'F',
        'application': 'G',
        'reagent_name': 'H',
        'reagent_smiles': 'I',
        'grafting_group': 'J',
        'grafting_group_smiles': 'K',  # 新增
        'functional_group_smiles': 'L',
        'functional_group_name': 'M',
        'functional_group_formula': 'N',
        'functionalization_degree': 'O',
        'functionalization_unit': 'P',
        'polymer_fingerprint': 'Q',
        'nmr_figure': 'R',
        'tem_figure': 'S',
        'mechanical_figure': 'T',
        'dsc_figure': 'U',
        'citation': 'V',
        'doi': 'W',
        'doi_si': 'X',
    }
    
    # 反向映射
    COLUMN_TO_FIELD = {v: k for k, v in COLUMN_MAP.items()}
    
    # 中文表头映射（用于从 AI 输出导入）
    HEADER_CN_MAP = {
        '样本ID': 'sample_id',
        '是否是SSBR': 'is_ssbr',
        '是否是 SSBR': 'is_ssbr',
        '是否是链中官能化': 'is_inchain_functionalization',
        '苯乙烯含量_wt%': 'styrene_content',
        '乙烯基含量_mol%': 'vinyl_content',
        '数均分子量 (Mn)': 'mn',
        '数均分子量': 'mn',
        'Mn': 'mn',
        '应用场景': 'application',
        '官能化试剂名称': 'reagent_name',
        '试剂整体SMILES': 'reagent_smiles',
        '试剂整体 SMILES': 'reagent_smiles',
        '接枝反应基团': 'grafting_group',
        '接枝反应基团SMILES': 'grafting_group_smiles',  # 新增
        '接枝反应基团 SMILES': 'grafting_group_smiles',  # 新增
        '核心官能团SMILES': 'functional_group_smiles',
        '核心官能团 SMILES': 'functional_group_smiles',
        '核心官能团名称': 'functional_group_name',
        '核心官能团化学式': 'functional_group_formula',
        '官能化程度_原始数值': 'functionalization_degree',
        '官能化程度_原始单位': 'functionalization_unit',
        '高分子指纹描述符': 'polymer_fingerprint',
        '核磁谱图': 'nmr_figure',
        '微相分离图片表征': 'tem_figure',
        '核心力学图谱': 'mechanical_figure',
        'DSC谱图': 'dsc_figure',
        'DSC 谱图': 'dsc_figure',
        '引文': 'citation',
        'DOI': 'doi',
        'DOI_SI': 'doi_si',
    }
    
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
        获取样本的所有元数据字段 (A-W 列)
        
        Args:
            sample_id: 样本 ID
            
        Returns:
            元数据字典
        """
        data = self.get_sample_data(sample_id)
        if not data:
            return {}
        
        return data
    
    def get_next_sample_id(self) -> str:
        """
        获取下一个可用的样本 ID
        
        Returns:
            下一个样本 ID (如 'SSBR-015')
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        
        max_num = 0
        for row in range(2, self.worksheet.max_row + 1):
            sample_id = self.get_cell_value(row, 'A')
            if sample_id and sample_id.startswith('SSBR-'):
                try:
                    num = int(sample_id.split('-')[1])
                    max_num = max(max_num, num)
                except (ValueError, IndexError):
                    pass
        
        return f"SSBR-{max_num + 1:03d}"
    
    def add_sample(self, data: Dict[str, Any], sample_id: Optional[str] = None) -> str:
        """
        添加新样本
        
        Args:
            data: 样本数据字典（字段名或中文表头作为键）
            sample_id: 指定样本 ID，默认自动分配
            
        Returns:
            分配的样本 ID
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        
        # 标准化字段名（将中文表头转换为字段名）
        normalized_data = self._normalize_field_names(data)
        
        # 分配样本 ID
        if sample_id:
            # 检查是否已存在
            if self.find_sample_row(sample_id):
                raise ValueError(f"样本 ID {sample_id} 已存在")
            normalized_data['sample_id'] = sample_id
        else:
            normalized_data['sample_id'] = self.get_next_sample_id()
        
        # 找到下一个空行（从第 2 行开始查找，跳过表头）
        new_row = self._find_next_empty_row()
        
        # 写入数据
        for field, col in self.COLUMN_MAP.items():
            value = normalized_data.get(field)
            if value is not None:
                self.set_cell_value(new_row, col, value)
        
        return normalized_data['sample_id']
    
    def _find_next_empty_row(self) -> int:
        """
        找到下一个空行（A 列为空的行）
        
        Returns:
            空行的行号
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        
        # 从第 2 行开始查找（第 1 行是表头）
        row = 2
        while row <= self.worksheet.max_row + 1:
            cell_value = self.get_cell_value(row, 'A')
            if cell_value is None or str(cell_value).strip() == '':
                return row
            row += 1
        return row
    
    def update_sample(self, sample_id: str, data: Dict[str, Any]) -> bool:
        """
        更新现有样本
        
        Args:
            sample_id: 样本 ID
            data: 要更新的数据字典
            
        Returns:
            是否成功
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        
        row = self.find_sample_row(sample_id)
        if not row:
            return False
        
        # 标准化字段名
        normalized_data = self._normalize_field_names(data)
        
        # 更新数据（跳过 sample_id）
        for field, col in self.COLUMN_MAP.items():
            if field == 'sample_id':
                continue
            if field in normalized_data:
                value = normalized_data[field]
                self.set_cell_value(row, col, value)
        
        return True
    
    def _normalize_field_names(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将数据字典的键标准化为字段名
        
        Args:
            data: 原始数据字典（键可能是中文表头或字段名）
            
        Returns:
            标准化后的数据字典
        """
        normalized = {}
        for key, value in data.items():
            # 如果是中文表头，转换为字段名
            if key in self.HEADER_CN_MAP:
                field = self.HEADER_CN_MAP[key]
            elif key in self.COLUMN_MAP:
                field = key
            else:
                # 尝试直接作为字段名
                field = key
            
            # 处理 "-" 占位符
            if value == '-' or value == '－':
                value = None
            
            normalized[field] = value
        
        return normalized
    
    def find_by_doi(self, doi: str) -> Optional[Dict[str, Any]]:
        """
        通过 DOI 查找样本
        
        Args:
            doi: 文献 DOI
            
        Returns:
            样本数据字典，未找到返回 None
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        
        doi_lower = doi.lower().strip()
        
        for row in range(2, self.worksheet.max_row + 1):
            cell_doi = self.get_cell_value(row, self.COLUMN_MAP['doi'])
            if cell_doi and str(cell_doi).lower().strip() == doi_lower:
                return self.get_row_data(row)
        
        return None
    
    def get_samples_by_doi(self, doi: str) -> List[Dict[str, Any]]:
        """
        获取同一 DOI 下的所有样本（一篇文献可能有多个样本）
        
        Args:
            doi: 文献 DOI
            
        Returns:
            样本数据列表
        """
        if not self.worksheet:
            raise RuntimeError("Excel 文件未打开")
        
        doi_lower = doi.lower().strip()
        samples = []
        
        for row in range(2, self.worksheet.max_row + 1):
            cell_doi = self.get_cell_value(row, self.COLUMN_MAP['doi'])
            if cell_doi and str(cell_doi).lower().strip() == doi_lower:
                samples.append(self.get_row_data(row))
        
        return samples
    
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
    print("\n使用方法:")
    print("  with ExcelHandler('dataset/数据.xlsx') as excel:")
    print("      # 获取样本数据")
    print("      data = excel.get_sample_data('SSBR-001')")
    print("      # 添加新样本")
    print("      new_id = excel.add_sample({'官能化试剂名称': 'MPA', ...})")
    print("      # 通过 DOI 查找")
    print("      samples = excel.get_samples_by_doi('10.1039/xxx')")
    print("      excel.save()")
