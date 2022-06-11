import time

import gspread as gd
import pandas as pd
from functions import bid_checker, asks

gc = gd.service_account('options-349716-50a9f6e13067.json')

worksheet = gc.open('work_table').worksheet('хэджи')

starts = {
    'First': 3,
    'Second': 22
}

f = []
s = []
for i in range(starts['First'], 20):
    t = worksheet.get(f'B{i}')
    print(f"Get {t}")
    if len(t) != 0:
        f.append(i)
    else:
        print('Finished 1 part, wait 1 min')
        break

time.sleep(60)

for i in range(starts['Second'], 100):
    t = worksheet.get(f'B{i}')
    print(f"Get {t}")
    if len(t) != 0:
        s.append(i)
    else:
        print('Finished 2 part, wait 1 min')
        break

time.sleep(60)
fs = f + s
print(fs)

options = []
for row in fs:
    x = worksheet.row_values(row)
    if len(x[1]) == 0:
        print('Finished to load data')
        break
    print(x)
    date = x[5]
    strike = x[8].replace(',', '.')
    date = date.split('.')
    rd = date[2] + date[1] + date[0]
    ticker = x[1]
    if ticker.find(':') != -1:
        ticker = ticker.split(':')[1]
    tc = x[2]
    options.append([ticker, x[3], x[4], strike, x[6], rd, float(x[7]), tc])
    print(options[-1])
    if row % 40 == 0:
        print('Need to wait 1 minute')
        time.sleep(60)

print(options)

ask_closes = []
c = 0
for option in options:
    try:
        print(option)
        x = bid_checker(option)
        print(f'x : {x}')
        temp = 0
        print(f'temp: {temp}')
        if c != len(asks):
            ask_closes.append(asks[-1])
            c = len(asks)
        else:
            print('No new data')
            ask_closes.append(None)
        time.sleep(3)
    except:
        print('smth went wrong')
        ask_closes.append(None)
        time.sleep(3)
        pass

df = pd.DataFrame(data=options, columns=['Company', 'Currency', 'Exchange', 'Strike', 'Multiplier',
                                         'Expiration Date', 'Number of Contracts', 'Trade Class'])
df['Idx'] = fs
df = df.set_index('Idx')
print(ask_closes)
df['Ask Close'] = ask_closes
df['Asks Ret'] = df['Ask Close'] * df['Number of Contracts']

print('Result')
print(df)

df.to_csv('Test_Hedges_2_Amer_08.csv')

for row_number in fs:
    if row_number % 30 == 0:
        print('Need to wait 1 min')
        time.sleep(60)
    if df['Asks Ret'][row_number] > 0:
        print(f"Insert {df['Asks Ret'][row_number]} into M{row_number}")
        worksheet.update(f"M{row_number}", df['Asks Ret'][row_number])
    else:
        print(f'Nothing to insert into M{row_number}')
