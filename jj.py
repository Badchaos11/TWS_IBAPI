import pandas as pd
import numpy as np


df = pd.read_csv('Test_CSV.csv')
print(df)
df = df.set_index('Idx')
print(df['Asks Ret'][62])
print(type(df['Asks Ret'][62]))
