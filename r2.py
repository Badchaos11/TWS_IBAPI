import pandas as pd
import dicts
import warnings

warnings.filterwarnings("ignore")


dd = pd.read_csv('GuruFocus_NAS_INTC_Financial_2022-6-20 at 13_49.csv')
x = dd['0'].tolist()
print(dd.iloc[3][0])
print(dd)
df = pd.read_csv('Data_for_Portfolio.csv')
print(df)
y = df.columns[1:-69].tolist()

res = pd.DataFrame()

for i, row in enumerate(x):
    try:
        d = row.strip()
        d = d.replace(" ", "_")
        if d in y:
            res[d] = dd.iloc[i][1:]
        elif dicts.columns__to_replace[d] in y:
            res[dicts.columns__to_replace[d]] = dd.iloc[i][1:]
    except:
        print('Nothing else')

print(res)


res.dropna(inplace=True)
print(res)
comp = ["INTC"] * len(res)
print(comp)

res.insert(0, "Company", "INTC")
print(res)
# res.to_csv("Test_3.csv", index=False)
print(len(res.iloc[31]))
print(len(res.iloc[35]))
