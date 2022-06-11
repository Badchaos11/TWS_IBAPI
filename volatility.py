import threading
import time

import gspread as gd
import pandas as pd
from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

imp_opt_vol = []
hist_run = []


class IBapi(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

    def historicalData(self, reqId: int, bar: BarData):
        if reqId == 4002:
            print(f"Implied Vol Data. Bar Data: {bar}")
            imp_opt_vol.append(bar.close)
        if reqId == 4001:
            print(f"Historical Vol Data. Bar Data: {bar}")
            hist_run.append(bar.close)


def run_loop():
    app.run()


gc = gd.service_account('options-349716-50a9f6e13067.json')
worksheet = gc.open('work_table').worksheet('Опционы QQQ')

tickers = []
for i in range(2, 50):
    c = worksheet.get(f'A{i}')
    print(c)
    if len(c) == 0:
        print('Finished')
        break
    c = c[0][0]
    c = c.split(':')
    tickers.append(c[1])

print(tickers)
historical_volatility = []
for ticker in tickers:
    contract = Contract()
    contract.symbol = ticker
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    app = IBapi()
    app.connect('127.0.0.1', 7497, 735861)

    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    time.sleep(2)
    app.reqHistoricalData(4001, contract, '', '1 Y', '1 month', 'HISTORICAL_VOLATILITY', 1, 1, False, [])
    app.reqHistoricalData(4002, contract, '', '1 D', '1 day', 'OPTION_IMPLIED_VOLATILITY', 1, 1, False, [])
    time.sleep(5)
    app.disconnect()
    historical_volatility.append(hist_run[-1])
    hist_run.clear()

df = pd.DataFrame()
df['Companies'] = tickers
df['Implied Volatility'] = imp_opt_vol
df['Implied Volatility'] = df['Implied Volatility'] * 100
df['Historical Volatility'] = historical_volatility
df['Historical Volatility'] = df['Historical Volatility'] * 100

print(df)

df.to_csv('Test_Imp_Vol.csv')
