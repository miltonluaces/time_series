import numpy as np
import scipy as sp
import pandas as pd
import Forecasting.UniFcst as uf

# TrendRes : calculate the trend result
# ts : the time series (array of reals)
# idx : current index
# span : period lenght (from idx+1)
# var : percentage of variation
# Returns : -1 if lower limit is reached, 1 if upper limit is reached, 0 otherwise
def TrendRes(ts, idx, span, var):
    per = ts[idx+1:idx+span+1]
    spVal = per[0] * var/100
    if min(per) <= ts[idx] - spVal : return -1
    if max(per) >= ts[idx] + spVal : return 1
    return 0

# TrendRes : calculate the trend result with moving window for whole time series (except the last span)
# ts : the time series (array of reals)
# span : period lenght (from idx+1)
# var : percentage of variation
# Returns : -1 if lower limit is reached, 1 if upper limit is reached, 0 otherwise
def TrendResTS(ts, span, var):
    res = [0] * (len(ts)-span)
    for i in range(len(ts)-span-1):
        res[i] = TrendRes(ts, i, span, var)
    return res

# Deriv : relative rate change of a time series
# ts : the time series
# Returns : time series of relative changes (len-1)
def Deriv(ts):
    n = len(ts)
    return (ts[1:n]-ts[0:(n-1)])/ts[1:n]

def PlotDerivVar(ts, var):
    der = Deriv(ts)
    plt.plot(der)
    plt.axhline(y=var/100, color='r', linestyle='--')
    plt.axhline(y=-var/100, color='r', linestyle='--')
    plt.show()

# Fixed and simmetric stop loss (sl) and take profit (tf), until one fires.
# ts : the time series (array of reals)
# var : percentage of variation
# Returns : total profit
def TrendProfit(ts, var):
    tf = pd.DataFrame(columns=['Idx','Brk','Pft'])
    profit=0
    state=1
    for i in range(len(ts)-1):
        if(state!=0):
            diff = ts[i] * var/100
            sl = ts[i] - diff
            tp = ts[i] + diff
            state=0
        
        if ts[i] < sl : profit-= diff; tf.loc[tf.shape[0]] = i,-1, -diff; n=+1; state=1
        if ts[i] > tp : profit+= diff; tf.loc[tf.shape[0]] = i, 1, diff; n=+1; state=1
        totBrk = sum(tf['Brk'])
        totPft = sum(tf['Pft'])
    return tf, totBrk, totPft  

# Fixed and simmetric stop loss (sl) and take profit (tf) within moving window (for fcst validation at each point)
# ts : the time series (array of reals)
# var : percentage of variation
# mw : moving window
# Returns : total profit
def TrendBreaksMw(ts, var, mw):
    tf = pd.DataFrame(columns=['Idx','Brk','Pft'])
    breaks = []
    for i in range(len(ts)-1):
        if(i<mw or i>(len(ts)-mw-1)): breaks.append(0); continue
        diff = ts[i] * var/100
        sl = ts[i] - diff
        tp = ts[i] + diff
        per = ts[(i+1):(i+mw)]
        if min(per) < sl : breaks.append(-1)
        elif max(per) > tp : breaks.append(1)
        else : breaks.append(0)
    return breaks

# Fcst
def TrendBreaksMwFcst(ts, var, mw, fMethod):
    tf = pd.DataFrame(columns=['Idx','Brk','Pft'])
    breaks = []
    for i in range(len(ts)-1):
        if(i<mw or i>(len(ts)-mw-1)): breaks.append(0); continue
        diff = ts[i] * var/100
        sl = ts[i] - diff
        tp = ts[i] + diff
        fcst = uf.Forecast(ts[:i], hor=mw, method=fMethod)
        if min(fcst) < sl : breaks.append(-1)
        elif max(fcst) > tp : breaks.append(1)
        else : breaks.append(0)
    return breaks


# Determine the correct var based on forecast accuracy
# Determine investment needed for a certain return given other parameters
# In PlotDerivVar determine the right spread to optimize profit (consider original ts)


def ValidateTrendFcst(ts, var, mw, fMethod):
    tbReal = TrendBreaksMw(ts, var, mw)
    tbFcst = TrendBreaksMwFcst(ts, var, mw, fMethod)
    diff = abs(np.array(tbReal) - np.array(tbFcst))
    mae = sum(diff)/len(tbReal)
    return(diff, mae)
 