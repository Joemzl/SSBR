import pandas as pd

df = pd.read_excel('dataset/数据.xlsx')
print("=== Excel 数据中的文献信息 ===")
print(df[['样本ID', '引文', 'DOI', 'DOI_SI']].head(10).to_string())
print("\n=== 所有唯一的 DOI ===")
print(df['DOI'].unique())
