"""分析待生成样本，并检查 Zotero PDF 可用性"""
import pandas as pd
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

# 读取 Excel
df = pd.read_excel('dataset/数据.xlsx')

# 获取已完成的样本
interp_dir = 'dataset/interpretations'
done_samples = []
for folder in os.listdir(interp_dir):
    folder_path = os.path.join(interp_dir, folder)
    if os.path.isdir(folder_path) and folder.startswith('SSBR-'):
        files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
        if len(files) >= 5:
            done_samples.append(folder)

done_set = set(done_samples)

# 筛选未完成的样本
pending_df = df[~df['样本ID'].isin(done_set)].copy()

# Zotero 中的 DOI 到 PDF 路径映射（从 MCP 查询结果提取）
zotero_pdfs = {
    "10.1002/app.28621": "D:\\zotero\\library\\storage\\FZHUPV9E\\app.28621.pdf.pdf",
    "10.1021/acs.iecr.6b02259": "D:\\zotero\\library\\storage\\8WRVT7UP\\acs.iecr.6b02259.pdf.pdf",
    "10.1039/c8ra00572a": "D:\\zotero\\library\\storage\\ZRAEA8LE\\C8RA00572A.pdf.pdf",
    "10.1002/app.41182": "D:\\zotero\\library\\storage\\4NTLNXKS\\app.41182.pdf.pdf",
    "10.1002/app.44923": "D:\\zotero\\library\\storage\\HBDDW85I\\app.44923.pdf.pdf",
    "10.1002/app.45749": "D:\\zotero\\library\\storage\\UDTF4WSK\\app.45749.pdf.pdf",
    "10.1002/app.45975": "D:\\zotero\\library\\storage\\4847RUGM\\app.45975.pdf.pdf",
    "10.1002/masy.201650001": "D:\\zotero\\library\\storage\\QIZNLCHW\\masy.201650001.pdf.pdf",
    "10.1002/pen.25110": "D:\\zotero\\library\\storage\\QU52ZRIY\\pen.25110.pdf.pdf",
    "10.1002/pen.25650": "D:\\zotero\\library\\storage\\K47YJXD3\\pen.25650.pdf.pdf",
    "10.1007/s10853-008-3223-8": "D:\\zotero\\library\\storage\\DNFLTNS7\\s10853-008-3223-8.pdf.pdf",
    "10.1016/j.compositesb.2015.07.001": "D:\\zotero\\library\\storage\\E5H6EHAM\\j.compositesb.2015.07.001.pdf.pdf",
    "10.1016/j.compositesb.2019.107027": "D:\\zotero\\library\\storage\\FDN6MXEL\\j.compositesb.2019.107027.pdf.pdf",
    "10.1016/j.compositesb.2020.108301": "D:\\zotero\\library\\storage\\7LXZVSX7\\j.compositesb.2020.108301.pdf.pdf",
    "10.1016/j.compscitech.2018.04.008": "D:\\zotero\\library\\storage\\HNHXABRZ\\j.compscitech.2018.04.008.pdf.pdf",
    "10.1016/j.nanoen.2018.03.038": "D:\\zotero\\library\\storage\\ARCC6JTT\\j.nanoen.2018.03.038.pdf.pdf",
    "10.1016/j.polymer.2010.03.006": "D:\\zotero\\library\\storage\\CEKUMW8H\\j.polymer.2010.03.006.pdf.pdf",
    "10.1016/j.polymer.2015.07.015": "D:\\zotero\\library\\storage\\TC9A74KE\\j.polymer.2015.07.015.pdf.pdf",
    "10.1016/j.polymer.2015.11.039": "D:\\zotero\\library\\storage\\7WRXJFPQ\\j.polymer.2015.11.039.pdf.pdf",
    "10.1016/j.polymer.2017.08.051": "D:\\zotero\\library\\storage\\J4QV2C8V\\j.polymer.2017.08.051.pdf.pdf",
    "10.1016/j.polymer.2018.02.057": "D:\\zotero\\library\\storage\\AE4IBFXD\\j.polymer.2018.02.057.pdf.pdf",
    "10.1016/j.polymertesting.2017.01.007": "D:\\zotero\\library\\storage\\4T67JQC7\\j.polymertesting.2017.01.007.pdf.pdf",
    "10.1016/j.polymertesting.2020.106558": "D:\\zotero\\library\\storage\\KPADCDYV\\j.polymertesting.2020.106558.pdf.pdf",
    "10.1039/C6RA08417F": None,  # 需要检查
    "10.1039/c3ra47050d": "D:\\zotero\\library\\storage\\N477VFC7\\C3RA47050D.pdf.pdf",
    "10.1039/c4ra04722b": "D:\\zotero\\library\\storage\\9DIBM9JZ\\c4ra04722b.pdf.pdf",
    "10.1142/S0256767908003503": "D:\\zotero\\library\\storage\\7TNA95XY\\S0256767908003503.pdf.pdf",
    "10.3389/fchem.2018.00240": "D:\\zotero\\library\\storage\\YTJ78IQU\\fchem.2018.00240.pdf.pdf",
    "10.3390/polym12010209": "D:\\zotero\\library\\storage\\8T8H66NG\\polym12010209.pdf.pdf",
    "10.3390/polym13101626": "D:\\zotero\\library\\storage\\EQP8EZED\\polym13101626.pdf.pdf",
    "10.4028/www.scientific.net/AMR.11-12.657": "D:\\zotero\\library\\storage\\DPRR47NA\\www.scientific.net%252Famr.11-12.657.pdf.pdf",
    "10.5254/rct.15.84881": "D:\\zotero\\library\\storage\\9LFZ7PNI\\rct.15.84881.pdf.pdf",
    "10.5254/rct.17.83724": "D:\\zotero\\library\\storage\\WS3YBLYX\\rct.17.83724.pdf.pdf",
    "10.5254/rct.19.80439": "D:\\zotero\\library\\storage\\F9BMUDY6\\rct.19.80439.pdf.pdf",
    "10.1002/app.43342": "D:\\zotero\\library\\storage\\M7NQJTFD\\app.43342.pdf.pdf",
    "10.1002/app.32372": "D:\\zotero\\library\\storage\\CE9E26B4\\app.32372.pdf.pdf",
    "10.1007/s13726-020-00843-3": "D:\\zotero\\library\\storage\\Q87C4WBQ\\s13726-020-00843-3.pdf.pdf",
}

# 按 DOI 分组分析
print("=" * 100)
print("📊 待生成样本详细分析报告")
print("=" * 100)

doi_groups = []
for doi, group in pending_df.groupby('DOI'):
    samples = group['样本ID'].tolist()
    reagents = [r for r in group['官能化试剂名称'].unique() if pd.notna(r)]
    is_chain = group['是否是链中官能化'].unique().tolist()
    
    # 检查 PDF 是否可用
    pdf_path = zotero_pdfs.get(doi)
    pdf_available = pdf_path is not None and os.path.exists(pdf_path) if pdf_path else False
    
    doi_groups.append({
        'DOI': doi,
        '样本数': len(samples),
        '样本列表': samples,
        '官能化试剂': reagents if reagents else ['未指定'],
        '是否链中官能化': is_chain,
        'PDF路径': pdf_path,
        'PDF可用': pdf_available
    })

# 按样本数排序
doi_groups.sort(key=lambda x: x['样本数'], reverse=True)

# 分类统计
pdf_available_count = sum(1 for g in doi_groups if g['PDF可用'])
pdf_missing_count = len(doi_groups) - pdf_available_count

print(f"\n📈 总体统计:")
print(f"  - 待生成样本总数: {len(pending_df)} 个")
print(f"  - 涉及文献数: {len(doi_groups)} 篇")
print(f"  - PDF 可用: {pdf_available_count} 篇 ✅")
print(f"  - PDF 缺失: {pdf_missing_count} 篇 ❌")

# 按 PDF 可用性分组输出
print("\n" + "=" * 100)
print("✅ PDF 可用的文献 (可直接生成)")
print("=" * 100)

batch_num = 1
samples_with_pdf = 0
for g in doi_groups:
    if g['PDF可用']:
        samples_with_pdf += g['样本数']
        print(f"\n【批次 {batch_num}】DOI: {g['DOI']}")
        print(f"    样本数: {g['样本数']} 个 → {g['样本列表']}")
        print(f"    官能化试剂: {g['官能化试剂']}")
        print(f"    PDF: {g['PDF路径']}")
        batch_num += 1

print(f"\n  小计: {samples_with_pdf} 个样本可直接生成")

print("\n" + "=" * 100)
print("❌ PDF 缺失的文献 (需要先获取 PDF)")
print("=" * 100)

samples_without_pdf = 0
for g in doi_groups:
    if not g['PDF可用']:
        samples_without_pdf += g['样本数']
        print(f"\n  DOI: {g['DOI']}")
        print(f"    样本: {g['样本列表']}")
        print(f"    官能化试剂: {g['官能化试剂']}")

print(f"\n  小计: {samples_without_pdf} 个样本需要先获取 PDF")

# 输出建议的批次计划
print("\n" + "=" * 100)
print("📋 建议的生成批次计划")
print("=" * 100)

batch_plan = []
current_batch = []
current_samples = 0

for g in doi_groups:
    if g['PDF可用']:
        if current_samples + g['样本数'] <= 10:  # 每批次最多 10 个样本
            current_batch.append(g)
            current_samples += g['样本数']
        else:
            if current_batch:
                batch_plan.append(current_batch)
            current_batch = [g]
            current_samples = g['样本数']

if current_batch:
    batch_plan.append(current_batch)

for i, batch in enumerate(batch_plan, 1):
    total_samples = sum(g['样本数'] for g in batch)
    dois = [g['DOI'] for g in batch]
    samples = []
    for g in batch:
        samples.extend(g['样本列表'])
    print(f"\n批次 {i}: {total_samples} 个样本, {len(batch)} 篇文献")
    print(f"  样本: {samples}")
    print(f"  DOIs: {dois}")
