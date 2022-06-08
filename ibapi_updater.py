import time

import gspread as gd
import pandas as pd
import numpy as np
from functions import country_checker, ask_checker, asks


def ibapi_update(country: str):

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

    splitted_sheet = {
        'America': amer,
        'Europe': euro,
        'China': china
    }

    w = splitted_sheet[country]

    options = []
    print(f'Loading data for {country}')
    for row in w:
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

    print(options)
    print('Need to wait 1 minute before continuing')
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
    df.to_csv('Test_CSV.csv')
    for row_number in w:
        if df['Asks Ret'][row_number] > 0:
            print(f"Insert {df['Asks Ret'][row_number]} into {row_number}")
            worksheet.update(f"L{row_number}", df['Asks Ret'][row_number])
        else:
            print(f'Nothing to insert into {row_number}')


ibapi_update('Europe')
