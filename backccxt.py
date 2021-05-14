from backtrader.order import BuyOrder, SellOrder
import ccxt
import numpy as np
from numpy.core.numeric import False_

import pandas as pd
import config 
import backtrader as bt
import matplotlib
import os.path
import sys 
import datetime
import time
import backtrader.feeds as btfeeds
from config import COIN_TARGET

    ##################################################################################
    #               API CREDENTIALS FROM FONFIG FILE
    ##################################################################################
    

exchange = ccxt.binanceus({
    "apiKey": config.BINANCE_API_KEY,
    "secret": config.BINANCE_SECRET_KEY
})

    ##################################################################################
    #               FETCH DATA FROM BINANCE AND ADD COLUMNS AND CREATE CSV FILE
    ##################################################################################
    
l = 100
bars = exchange.fetch_ohlcv('ETH/USD', timeframe='4h', limit=l)
df = pd.DataFrame(bars[:-1], columns=['timestamp','open', 'high', 'low', 'close', 'volume'])
df = pd.DataFrame(bars[:-1], columns=['timestamp','open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

df['previous_close'] = df['close'].shift(1)
df['difference'] = df['close'] - df['previous_close']
df.to_csv (r'C:\python\projects\csv\ethusdt.csv', index = False, header=True)


    ##################################################################################
    #               DEFINE STRATEGY
    ##################################################################################
    

class MyStrategy(bt.Strategy):
        
        def __init__(self):
            
            df.difference = df.close - df.previous_close
            self.signal = ''
            self.entrybuy = 0
            self.entrysell = 0
            self.order = None
            
            
            for i in range(3,95):
                
                if df.difference[i]>0 and df.difference[i+1]>0 and df.difference[i+2]<0 and df.difference[i+3]<0: 
                    self.signal = 'sell'
                    self.entrysell = df.close[i+3] 
                    print('SELL',self.entrysell)
                     
                    
                if df.difference[i]<0 and df.difference[i+1]<0 and df.difference[i+2]>0 and df.difference[i+3]>0:
                    self.signal = 'buy'
                    self.entrybuy = df.close[i+3] 
                    print('BUY',self.entrybuy) 
                    
                    
        def next(self):
            
                if self.order:
                    return
            
                if  self.signal == 'buy': 
                    self.order = self.buy(size=0.1, price=self.entrybuy)
                    print(self.order)
                    
                    
                if  self.signal == 'sell': 
                    self.order = self.sell(size=0.1, price=self.entrysell)
                    print(self.order)
                
                    
    ##################################################################################
    #               LOAD DATA FROM CSV
    ##################################################################################    
  
data = bt.feeds.GenericCSVData(
            name=COIN_TARGET,
            dataname="C:\python\projects\csv\ethusdt.csv",
            timeframe=bt.TimeFrame.Minutes,
            nullvalue=0.0
        )
  
  
cerebro = bt.Cerebro()  
cerebro.adddata(data)
cerebro.addstrategy(MyStrategy)

   
    # Set our desired cash start
cerebro.broker.setcash(10000.0)

    # Set the commission
cerebro.broker.setcommission(commission=0.01)

    # Run over everything
cerebro.run(maxcpus=1)

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style='candlestick')







