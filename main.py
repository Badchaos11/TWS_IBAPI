import datetime
import threading
import time

import gspread as gd
import pandas as pd
from ibapi.client import EClient
from ibapi.common import SetOfString, SetOfFloat, TickerId, BarData
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

imp_opt_vol = []
hist_run = []

class IBapi(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

    def securityDefinitionOptionParameter(self, reqId: int, exchange: str, underlyingConId: int, tradingClass: str,
                                          multiplier: str, expirations: SetOfString, strikes: SetOfFloat):
        print(f"SecurityDefinitionOptionParameter.\n"
              f"ReqId: {reqId}, Exchange: {exchange}, Underlying conId: {underlyingConId};\n"
              f"Trading Class: {tradingClass}, Multiplier: {multiplier};\n"
              f"Expirations: {expirations};\n"
              f" Strikes: {strikes}\n")

    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        print(
            f"Position.\n"
            f"Account {account}, Symbol: {contract.symbol}, SecType: {contract.secType};\n"
            f"Currency: {contract.currency}, Position: {position}, Avg Cost: {avgCost}\n")

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        print(f"Account Summary.\n"
              f"ReqId {reqId}, Account: {account}, Tag: {tag};\n"
              f"Currency: {currency}, Value: {value}\n")

    def realtimeBar(self, reqId: TickerId, time: int, open_: float, high: float, low: float, close: float,
                    volume: int, wap: float, count: int):
        if reqId == 220603:
            print(f"Realtime Bar (now for Bid).\n"
                  f"Req ID: {reqId}, Date: {time};\n"
                  f"Open: {open_}, Hihg: {high}, Low: {low}, Close: {close};\n"
                  f"Volume: {volume}, WAP: {wap}, Count: {count}")
        elif reqId == 220604:
            print(f"Realtime Bar (now for Ask).\n"
                  f"Req ID: {reqId}, Date: {time};\n"
                  f"Open: {open_}, Hihg: {high}, Low: {low}, Close: {close};\n"
                  f"Volume: {volume}, WAP: {wap}, Count: {count}")
        print(datetime.datetime.now())
        print(50 * '*')

    def historicalData(self, reqId: int, bar: BarData):
        if reqId == 4002:
            print(f"Implied Vol Data. Bar Data: {bar}")
            imp_opt_vol.append(bar.close)
        if reqId == 4001:
            print(f"Historical Vol Data. Bar Data: {bar}")
            hist_run.append(bar.close)


def run_loop():
    app.run()


# app = IBapi()
# app.connect('127.0.0.1', 7497, 735861)
#
# api_thread = threading.Thread(target=run_loop, daemon=True)
# api_thread.start()
#
# time.sleep(2)

# app.reqPositions()
# app.reqSecDefOptParams(0, "IBM", "", "STK", 8314)
# app.reqAccountSummary(9001, "All", 'Cushion')

# contract = Contract()
# contract.symbol = "9988"
# contract.secType = "OPT"
# contract.exchange = "SEHK"
# contract.currency = "HKD"
# contract.multiplier = '500'
# contract.right = 'C'
# contract.strike = 105
# contract.lastTradeDateOrContractMonth = '20220629'
# contract.primaryExchange = 'SEHK'

# contract = Contract()
# contract.symbol = "ADBE"
# contract.secType = "STK"
# contract.exchange = "SMART"
# contract.currency = "USD"
# contract.multiplier = '500'
# contract.right = 'C'
# contract.strike = 56
# contract.lastTradeDateOrContractMonth = '20220624'
# contract.tradingClass = 'TOT4'

# contract = Contract()
# contract.symbol = "UBI"
# contract.secType = "OPT"
# contract.exchange = "SMART"
# contract.currency = "USD"
# contract.multiplier = '100'
# contract.right = 'C'
# contract.strike = 54
# contract.lastTradeDateOrContractMonth = '20220617'

# app.reqRealTimeBars(220603, contract, whatToShow='BID', useRTH=True, barSize=5, realTimeBarsOptions=[])
# app.reqRealTimeBars(220604, contract, whatToShow='ASK', useRTH=True, barSize=5, realTimeBarsOptions=[])
# app.reqHistoricalData(4001, contract, '', '1 Y', '1 month', 'HISTORICAL_VOLATILITY', 1, 1, False, [])
# app.reqHistoricalData(4002, contract, '', '1 D', '1 day', 'OPTION_IMPLIED_VOLATILITY', 1, 1, False, [])
# time.sleep(5)
# app.disconnect()

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
