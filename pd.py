import pandas as pd
import dicts
import warnings
import os

warnings.filterwarnings("ignore")


def prepare_data(filename: str) -> pd.DataFrame:
    dd = pd.read_csv(f"guru_files/{filename}")
    x = dd['0'].tolist()
    df = pd.read_csv('Data_for_Portfolio.csv')
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
            pass

    # res.dropna(inplace=True)
    res.insert(0, "Company", dd.iloc[3][0])

    return res


def all_data_to_one():

    final_result = pd.DataFrame()

    for filename in os.listdir("guru_files"):
        try:
            print(filename)
            x = prepare_data(filename)
            print(x)
            final_result = pd.concat([final_result, x])
        except TypeError:
            final_result = x

    print(final_result)
    final_result.to_csv("Full_Test_Without_Dropna.csv", index=False)


all_data_to_one()
