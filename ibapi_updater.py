import datetime
import time

import gspread as gd
import pandas as pd

import functions
from functions import ask_checker


def ibapi_update():

    gc = gd.service_account('options-349716-50a9f6e13067.json')

    worksheet = gc.open('work_table').worksheet('Опционный портфель (short)')

    options = []
    w = []
    print(f'Loading data for companies')
    for i in range(2, 100):
        c = worksheet.get(f"D{i}")
        if len(c) == 0:
            print('Finished to load data, go to get options data')
            break
        w.append(i)
        x = worksheet.row_values(i)
        date = x[21]
        strike = x[9].replace(',', '.')
        date = date.split('.')
        rd = date[2] + date[1] + date[0]
        ticker = x[1]
        options.append([ticker, x[2], x[3], x[7], strike, x[14], rd, float(x[15])])
        print(options[-1])
        if i % 30 == 0:
            print('Need to wait 1 minute')
            time.sleep(60)

    print(options)
    time.sleep(60)
    ask_closes = []
    c = 0
    for option in options:
        try:
            print(option)
            x = ask_checker(option)
            print(f'x : {x}')
            temp = 0
            print(f'temp: {temp}')
            # if c != len(asks):
            #     ask_closes.append(asks[-1])
            #     c = len(asks)
            # else:
            #     print('No new data')
            #     ask_closes.append(None)
            if len(functions.asks) != 0:
                print(f'Asks from f {functions.asks}')
                ask_closes.append(functions.asks[-1])
                functions.asks.clear()
            else:
                print(f'Asks from f {functions.asks}')
                ask_closes.append(None)
            time.sleep(3)
        except:
            print('smth went wrong')
            ask_closes.append(None)
            time.sleep(3)
            pass

    df = pd.DataFrame(data=options, columns=['Company', 'Currency', 'Exchange', 'Right', 'Strike', 'Multiplier',
                                             'Expiration Date', 'Number of Contracts'])
    df['Idx'] = w
    df = df.set_index('Idx')
    print(ask_closes)
    try:
        df['Ask Close'] = ask_closes
        df['Asks Ret'] = df['Number of Contracts'] * df['Ask Close']
    except:
        pass

    print('Result DF')
    print(df)
    df.to_csv('Test_CSV_Amer_09.csv')
    for row_number in w:
        if row_number % 30 == 0:
            print('Need to wait 1 min')
            time.sleep(60)
        if df['Asks Ret'][row_number] > 0:
            print(f"Insert {df['Asks Ret'][row_number]} into {row_number}")
            worksheet.update(f"L{row_number}", df['Asks Ret'][row_number])
        else:
            print(f'Nothing to insert into {row_number}')


print(datetime.datetime.now())
ibapi_update()
print(datetime.datetime.now())
