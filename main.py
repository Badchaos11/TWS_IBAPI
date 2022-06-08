import datetime
import threading
import time

from ibapi.client import EClient
from ibapi.common import SetOfString, SetOfFloat, TickerId
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


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


def run_loop():
    app.run()


app = IBapi()
app.connect('127.0.0.1', 7497, 735861)

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1)

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

contract = Contract()
contract.symbol = "OVS"
contract.secType = "OPT"
contract.exchange = "IDEM"
contract.currency = "EUR"
contract.multiplier = '500'
contract.right = 'P'
contract.strike = 1.7
contract.lastTradeDateOrContractMonth = '20220915'
contract.tradingClass = 'OVS'

# contract = Contract()
# contract.symbol = "UBI"
# contract.secType = "OPT"
# contract.exchange = "SMART"
# contract.currency = "USD"
# contract.multiplier = '100'
# contract.right = 'C'
# contract.strike = 54
# contract.lastTradeDateOrContractMonth = '20220617'

app.reqRealTimeBars(220603, contract, whatToShow='BID', useRTH=True, barSize=5, realTimeBarsOptions=[])
app.reqRealTimeBars(220604, contract, whatToShow='ASK', useRTH=True, barSize=5, realTimeBarsOptions=[])

time.sleep(2)
app.disconnect()
