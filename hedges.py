import random
import time

import gspread as gd
import pandas as pd
from functions import country_checker, bid_checker, asks


gc = gd.service_account('options-349716-50a9f6e13067.json')

worksheet = gc.open('work_table').worksheet('хэджи')

starts = {
    'First': 3,
    'Second': 22
}

amer = []
euro = []
for i in range(starts['Second'], 58):
    c = worksheet.get(f"D{i}")
    if len(c) > 0:
        c = c[0][0]
        t = country_checker(c)
        if t == 'A':
            print(f"Appending {c} to America")
            amer.append(i)
        elif t == 'E':
            print(f"Appending {c} to Europe")
            euro.append(i)
        if i % 40 == 0:
            print('Need to wait 1 min')
            time.sleep(60)
    else:
        print('Finished to sort companies by country, wait 1 min and continue')
        time.sleep(60)
        break

options_e = []
options_a = []

for row in amer:
    x = worksheet.row_values(row)
    date = x[4]
    strike = x[7].replace(',', '.')
    date = date.split('.')
    rd = date[2] + date[1] + date[0]
    ticker = x[1]
    if ticker.find(':') != -1:
        ticker = ticker.split(':')[1]
    options_a.append([ticker, x[2], x[3], strike, x[5], rd, float(x[6])])
    print(options_a[-1])

print('Need to wait 1 min')
time.sleep(60)

for row in euro:
    x = worksheet.row_values(row)
    date = x[4]
    strike = x[7].replace(',', '.')
    date = date.split('.')
    rd = date[2] + date[1] + date[0]
    ticker = x[1]
    if ticker.find(':') != -1:
        ticker = ticker.split(':')[1]
    options_e.append([ticker, x[2], x[3], strike, x[5], rd, float(x[6])])
    print(options_e[-1])

print('America')
print(options_a)
print('Europe')
print(options_e)

ask_closes_a = []
c = 0
for option in options_a:
    try:
        print(option)
        x = bid_checker(option)
        print(f'x : {x}')
        temp = 0
        print(f'temp: {temp}')
        if c != len(asks):
            ask_closes_a.append(asks[-1])
            c = len(asks)
        else:
            print('No new data')
            ask_closes_a.append(None)

        time.sleep(3)
    except:
        print('smth went wrong')
        ask_closes_a.append(None)
        time.sleep(3)
        pass

dda = pd.DataFrame(data=options_a, columns=['Company', 'Currency', 'Exchange', 'Strike', 'Multiplier',
                                            'Expiration Date', 'Number of Contracts'])
dda['Idx'] = amer
dda = dda.set_index('Idx')
print(ask_closes_a)
dda['Ask Close'] = ask_closes_a
dda['Ask Rets'] = dda['Ask Close'] * dda['Number of Contracts']

print('Euro')
print(dda)
print('asks')
print(asks)
dda.to_csv('Test_Hedges_2_Amer.csv')
