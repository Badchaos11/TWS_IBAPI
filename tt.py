import pandas as pd


df1 = pd.read_csv("guru_files/GuruFocus_AMEX_BTG_Financial_2022-6-20 at 17_20.csv")
df2 = pd.read_csv("guru_files/GuruFocus_AMEX_EQX_Financial_2022-6-20 at 17_30.csv")
print("d1")
print(df1)
print('d2')
print(df2)

df3 = pd.DataFrame()

x = pd.concat([df3, df2])
print(x)
