import sys
sys.path.append('D:/source/repos')
from utilities.std_imports import *


# Ts split univariate
# Parameteres: ts (time series, hist: last n historical periods to consider, fhor: forecasting horizon)
# Return: list of training time series and testing time series

def split_uni(ts, hist, fhor):
    trains = []
    tests = []
    for i in range(hist, ts.shape[0]-fhor+1):
        trains.append(ts[i-hist:i])
        tests.append(ts[i:i+fhor])
    return trains, tests


# Ts split multivariate
# Parameters: tss: list of time series (first: observable, others: exogenous), hist: last n historical periods to consider, fhor: forecasting horizon)
# Return: list of lists of training time series and list of lists of testing time series 
def split_multi(tss, hist, fhor):
    trainss = []
    testss = []
    for ts in tss:
        trains, tests = split_uni(ts=ts, hist=hist, fhor=fhor)
        trainss.append(trains)
        testss.append(tests)
    return trainss, testss