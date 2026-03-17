"""
测试为第一个样本（SSBR-001）生成完整解读文档
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).parent))

from utils.excel_handler import ExcelHandler

PROJECT_ROOT = Path(__file__).parent.parent
EXCEL_PATH = PROJECT_ROOT / "dataset" / "数据.xlsx"

def main():
    print("=" * 60)
    print("SSBR-001 样本信息")
    print("=" * 60)
    
    with ExcelHandler(EXCEL_PATH) as excel:
        data = excel.get_sample_data('SSBR-001')
        
        if not data:
            print("未找到 SSBR-001")
            return
        
        # 显示关键字段
        key_fields = [
            ('sample_id', '样本ID'),
            ('styrene_content', '苯乙烯含量_wt%'),
            ('vinyl_content', '乙烯基含量_mol%'),
            ('mn', '数均分子量'),
            ('application', '应用场景'),
            ('reagent_name', '官能化试剂名称'),
            ('functional_group_name', '核心官能团名称'),
            ('functionalization_degree', '官能化程度'),
            ('functionalization_unit', '官能化程度单位'),
            ('mechanical_figure', '核心力学图谱'),
            ('dsc_figure', 'DSC谱图'),
            ('nmr_figure', '核磁谱图'),
            ('tem_figure', 'TEM图片'),
            ('citation', '引文'),
            ('doi', 'DOI'),
            ('doi_si', 'DOI_SI'),
        ]
        
        print("\n关键字段:")
        for field, label in key_fields:
            value = data.get(field)
            if value:
                print(f"  {label}: {value}")
            else:
                print(f"  {label}: [空]")
        
        print("\n" + "=" * 60)
        print("需要生成的解读文档:")
        print("=" * 60)
        
        # 检查需要生成哪些解读文档
        docs = []
        if data.get('mechanical_figure'):
            docs.append(('mechanical.md', f"力学图谱: {data['mechanical_figure']}"))
        if data.get('dsc_figure'):
            docs.append(('dsc.md', f"DSC谱图: {data['dsc_figure']}"))
        if data.get('nmr_figure'):
            docs.append(('nmr.md', f"核磁谱图: {data['nmr_figure']}"))
        if data.get('tem_figure'):
            docs.append(('tem.md', f"TEM图片: {data['tem_figure']}"))
        
        for doc, info in docs:
            print(f"  - {doc}: {info}")
        
        print(f"\n总计: 需要生成 {len(docs)} 个解读文档 + 1 个 summary.md")

if __name__ == '__main__':
    main()
