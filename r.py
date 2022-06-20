import pandas as pd
import dicts


dd = pd.read_csv('GuruFocus_NAS_INTC_Financial_2022-6-20 at 13_49.csv')
x = dd['0'][26:].dropna().tolist()
print(dd)
df = pd.read_csv('Data_for_Portfolio.csv')
y = df.columns[1:-69].tolist()
c = 0
rc = []
for row in x:
    try:
        d = row.strip()
        d = d.replace(" ", "_")
        if d in y:
            # print(f"{d} is in target columns")
            c += 1
            print(d)
            rc.append(d)
        elif dicts.columns__to_replace[d] in y:
            # print(f"{d} is in target columns in dict")
            c += 1
            rc.append(dicts.columns__to_replace[d])
        else:
            print(f"{d} not in target columns")
    except:
        print(f"{row} is invalid")

print(f"Columns in target columns with _ and dict: {c}")
print(f"Target columns: {len(y)}")
print(f"Columns to transform: {len(x)}")

print(x)
print(y)
print("*****************************************")

# for key in dicts.columns__to_replace.keys():
#     if dicts.columns__to_replace[key] in y:
#         print(f"{dicts.columns__to_replace[key]} in target")
#         c += 1
#     else:
#         print('NOt today')
#
# print(c)
nc = []
for col in y:
    if col not in rc:
        print(f"{col}")
        nc.append(col)

print(len(nc))

print('Before')
print(dd)
dd = dd.iloc[26:]
dd = dd.set_index('0')
print(dd)
for row in rc:
    print(dd[row])
