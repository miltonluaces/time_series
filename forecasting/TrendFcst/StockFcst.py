import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime as dt
import yahoo_fin.stock_info as si
import plotly.graph_objects as go
import plotly.express as px
import statsmodels.tsa.statespace.sarimax as sms


def Sarimax(ts, order, seasonal_order):
    fit = sms.SARIMAX(ts, order=order,seasonal_order=seasonal_order).fit()
    fcst = fit.predict(start=121, end=127, dynamic=True)
    return fcst

def GetFirstNotNa(ts):
    for i in range(len(ts)):
        if not pd.isna(ts[i]):
            return i
        
def GetLastNotNa(ts):
    for i in reversed(range(len(ts))):
       if not pd.isna(ts[i]):
            return i
        
def PadMA(ts):
    tsp = ts
    idx = GetFirstNotNa(ts)
    diff = ts[idx+2] - ts[idx+1]
    for i in reversed(range(idx)):
        tsp[i] = ts[i+1] - diff
    
    idx = GetLastNotNa(ts)
    diff = ts[idx-1] - ts[idx-2]
    for i in range(idx, len(ts)):
        tsp[i] = ts[i-1] + diff
    return tsp

def GetMA(df, ticker, mw):
    rolling = df[ticker].rolling(window=mw, center=True)
    ma = rolling.mean()
    return PadMA(ma)

def PlotStockMA(df, ticker, mw1, mw2):
    ma1 = GetMA(df, ticker, mw1)
    ma2 = GetMA(df, ticker, mw2)
   
    plt.figure(figsize=(20, 10))
    plt.plot(df[ticker])
    plt.plot(ma1)
    plt.plot(ma2)
    plt.title(ticker)
    plt.show()

# Calculate Moving Average and get the difference from now to n days before
def GetMADiff(df, ticker, mw, nDays):
    ma = GetMA(df, ticker, mw)
    n = len(ma)
    diff = ((ma[n-1] - ma[n-nDays-1]) / ma[n-nDays-1]) * 100
    return round(diff, 2)


if __name__ == '__main__':
    print('StockFcst\n')