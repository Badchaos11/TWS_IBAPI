import random
import time

import gspread as gd
import pandas as pd
from functions import country_checker, ask_checker, asks


gc = gd.service_account('options-349716-50a9f6e13067.json')

worksheet = gc.open('work_table').worksheet('Опционный портфель (short)')

amer = []
china = []
euro = []

for i in range(2, 100):
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
        else:
            print(f"Appending {c} to China")
            china.append(i)
        if i % 40 == 0:
            print('Need to wait 1 min')
            time.sleep(60)
    else:
        print('Finished to sort companies by country, wait 1 min and continue')
        time.sleep(60)
        break


options = []
print('America')
for row in amer:
    x = worksheet.row_values(row)
    date = x[21]
    strike = x[9].replace(',', '.')
    date = date.split('.')
    rd = date[2] + date[1] + date[0]
    ticker = x[0]
    if ticker.find(':') != -1:
        ticker = ticker.split(':')[1]
    options.append([ticker, x[2], x[3], x[7], strike, x[14], rd, float(x[15])])
    print(options[-1])

print('sleep 1 min')
time.sleep(60)

print('Euro')
options_euro = []
for row in euro:
    x = worksheet.row_values(row)
    date = x[21]
    strike = x[9].replace(',', '.')
    date = date.split('.')
    rd = date[2] + date[1] + date[0]
    ticker = x[0][4:]
    options_euro.append([ticker, x[2], x[3], x[7], strike, x[14], rd, float(x[15])])
    print(options_euro[-1])

print('sleep 1 min')
time.sleep(60)

print('China')
options_sehk = []
for row in china:
    x = worksheet.row_values(row)
    date = x[21]
    strike = x[9].replace(',', '.')
    date = date.split('.')
    rd = date[2] + date[1] + date[0]
    ticker = x[0][4:]
    if ticker[0] == '0':
        ticker = ticker[1:]
    options_sehk.append([ticker, x[2], x[3], x[7], strike, x[14], rd, float(x[15])])
    print(options_sehk[-1])

print('America options')
print(options)
print('Euro options')
print(options_euro)
print('China options')
print(options_sehk)

ask_closes_a = []
c = 0
for option in options:
    try:
        print(option)
        x = ask_checker(option)
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

# Европа

# ask_closes_e = []
# c = 0
# for option in options_euro:
#     try:
#         print(option)
#         x = ask_checker(option)
#         print(f'x : {x}')
#         temp = 0
#         print(f'temp: {temp}')
#         if c != len(asks):
#             ask_closes_e.append(asks[-1])
#             c = len(asks)
#         else:
#             print('No new data')
#             ask_closes_e.append(None)
#
#         time.sleep(3)
#     except:
#         print('smth went wrong')
#         ask_closes_e.append(None)
#         time.sleep(3)
#         pass

# Китай

# ask_closes_c = []
# c = 0
# for option in options_sehk:
#     try:
#         print(option)
#         x = ask_checker(option)
#         print(f'x : {x}')
#         temp = 0
#         print(f'temp: {temp}')
#         if c != len(asks):
#             ask_closes_c.append(asks[-1])
#             c = len(asks)
#         else:
#             print('No new data')
#             ask_closes_c.append(None)
#         time.sleep(3)
#     except:
#         print('smth went wrong')
#         ask_closes_c.append(None)
#         time.sleep(3)
#         pass

# Америка
#
dda = pd.DataFrame(data=options, columns=['Company', 'Currency', 'Exchange', 'Right', 'Strike', 'Multiplier',
                                          'Expiration Date', 'Number of Contracts'])
dda['Idx'] = amer
dda = dda.set_index('Idx')
print(ask_closes_a)
try:
    dda['Ask Close'] = ask_closes_a
    dda['Asks Ret'] = dda['Number of Contracts'] * dda['Ask Close']
except:
    pass
#
# Европа
#
# dde = pd.DataFrame(data=options_euro, columns=['Company', 'Currency', 'Exchange', 'Right', 'Strike', 'Multiplier',
#                                                'Expiration Date', 'Number of Contracts'])
# dde['Idx'] = euro
# dde = dde.set_index('Idx')
# print(ask_closes_e)
# try:
#     dde['Ask Close'] = ask_closes_e
#     dde['Ask Rets'] = dde['Ask Close'] * dde['Number of Contracts']
# except:
#     pass

#
# Китай
#
# ddc = pd.DataFrame(data=options_sehk, columns=['Company', 'Currency', 'Exchange', 'Right', 'Strike', 'Multiplier',
#                                                'Expiration Date'])
# ddc['Idx'] = china
# ddc = ddc.set_index('Idx')
# try:
#     ddc['Ask Close'] = ask_closes_c
# except:
#     pass

# print('Amer')
# print(dda)
#
# print('Euro')
# print(dde)

# print('China')
# print(ddc)
# print('asks')
# print(asks)
# ddc.to_csv('China_Asks_220606.csv')

print('America')
print(dda)
print('asks')
print(asks)
dda.to_csv('Test_Amer_With_Contracts_220607_2.csv')

# print(amer)
# print('Result of asks for contracts contracts')
# print(dd)
# print('askes')
# print(asks)
# print('Saving result to CSV')
# dd.to_csv('Test_Run_IB_America.csv')

for number in china:
    print(f"insert {random.randrange(2, 100, 1)} into L{number}")
    # worksheet.update(f"L{number}", dd['Ask Close'][number])
