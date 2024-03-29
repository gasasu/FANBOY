# region imports
from AlgorithmImports import *
# endregion

class Macd_adx_v1(QCAlgorithm):

    def Initialize(self):
      # start and end dates for backtesting
        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2024, 1, 1)
      # total cash for portfolio
        self.SetCash(10000)
      # adding equities to portfolio. Make sure to follow this format.
        self.AddEquity("NVDA", Resolution.Daily)
        self.AddEquity("TSLA", Resolution.Daily)
        self.AddEquity("AAPL", Resolution.Daily)
        self.AddEquity("AMZN", Resolution.Daily)
        self.AddEquity("MSFT", Resolution.Daily)
        self.AddEquity("META", Resolution.Daily)
        self.AddEquity("GOOG", Resolution.Daily)
      # do not modify anything here. 
        self.SetBenchmark("SPY")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Cash)
        self.macd = {}
        self.adx = {}
        for security in self.Securities.Values:
            self.macd[security.Symbol] = self.MACD(security.Symbol, 12, 26, 9, MovingAverageType.Exponential, resolution=Resolution.Daily)
            self.adx[security.Symbol] = self.ADX(security.Symbol, 14, resolution=Resolution.Daily)


    def OnData(self, data: Slice):
      # do not modify anything here.
        for security in self.Securities.Values:
            if security.Symbol not in data.Bars:
                continue
            price = data.Bars[security.Symbol].Close
            macd = self.macd[security.Symbol]
            adx = self.adx[security.Symbol]
            if macd.IsReady and adx.IsReady:

                if self.Portfolio[security.Symbol].Invested:
                  # modify the selling parameters
                    if macd.Current.Value < macd.Signal.Current.Value and \
                        adx.PositiveDirectionalIndex.Current.Value < adx.NegativeDirectionalIndex.Current.Value:
                        self.Liquidate(security.Symbol)
                        self.Log(f"SELL {security.Symbol.Value} @ {price}")

                else:
                  # modify the buying parameters
                    if macd.Current.Value > macd.Signal.Current.Value and \
                    (adx.PositiveDirectionalIndex.Current.Value > abs(adx.NegativeDirectionalIndex.Current.Value)  
                    and adx.Current.Value > 25):
                      # you can change portfolio concentration and sizing.
                        self.SetHoldings(security.Symbol, .14)
                        self.Log(f"BUY {security.Symbol.Value} @ {price}")
