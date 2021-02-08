import sys
sys.path.append('D:/source/repos')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import time
import seaborn as sb; sb.set()
import yahoo_fin.stock_info as yfs
import yahoo_finance as yf
import yfinance as yfin
import lstf.Funds

# Real time data
#___________________________________________________________________________________________________________________________________________________________________

def get_rtdata(ticker, ndays=1):
    perStr = str(ndays) + "d"
    data = yfin.download(tickers=ticker, period= perStr, interval="1m");
    return data['High']

# Trend results
#___________________________________________________________________________________________________________________________________________________________________

def TrendRes(ts, now, span, tpVar, slVar, verbose=False):
    per = ts[now+1:now+span+1]
    tpVal = ts[now] * tpVar/100
    slVal = ts[now] * slVar/100
    if(verbose):
        print('Current val\t', ts[now])
        print('Take Profit\t', ts[now] + tpVal)    
        print('Stop Loss\t', ts[now] - slVal)
        print('\nPeriod')
        print(per)
        
    if max(per) >= ts[now] + tpVal : return 1
    if min(per) <= ts[now] - slVal : return -1
    return 0


def TrendResTS(ts, span, tpVar, slVar):
    res = [0] * (len(ts)-span)
    for i in range(len(ts)-span-1):
        res[i] = TrendRes(ts, i, span, tpVar, slVar)
    return res

def CalcLabel(lastHist, tpVar, slVar, fcstPer):
    tpVal = lastHist * tpVar/100
    slVal = lastHist * slVar/100
    label = 0
    if max(fcstPer) >= lastHist + tpVal : label = 1
    if min(fcstPer) <= lastHist - slVal : label = -1
    return label

def GenTrendDs(ts, start, nHist, nFcst, tpVar, slVar, incFcst=False, verbose=False):
    if start < nHist-1: start=nHist-1
    histCols = list(range(1,nHist+1))
    fcstCols = list(range(1,nFcst+1))
    columns = ['H' + str(x) for x in histCols]
    if incFcst : [columns.append('F' + str(x)) for x in fcstCols]
    columns.append('Trend')
    dsarr = []
    for i in range(start, len(ts)-nFcst-1):
        histPer = ts[i-nHist+1:i+1]
        fcstPer = ts[i+1:i+nFcst+1]
        label = CalcLabel(ts[i], tpVar, slVar, fcstPer)
        cols = histPer.values
        if incFcst: cols = np.append(cols, fcstPer.values)
        cols = np.append(cols, label)
        dsarr.append(cols)
    return pd.DataFrame(dsarr, columns=columns)

# TESTING
#____________________________________________________________________________________________________________________________________________________________________

if __name__ == '__main__':
    print('SurfTrading\n')

    ts = st.get_rtdata('ACN')
    plt.figure(figsize=(20, 10));
    ts.plot();
    pd.DataFrame(ts)