import numpy as np
import scipy as sp
import pandas as pd
import TrendFcst.TrendMethods as tm


# Optimize TrendBreaks for var parameter
# ts : the time series (array of reals)
# var : percentage of variation
# Returns : breaks (for each var), best var and best breaks
def OptimTrBreaks(ts, maxVar):
    breaks = []
    var = 0.1
    bestVar = 0
    bestBreaks = 0
    while var <= maxVar:
        tf, totBrk, totPft = tm.TrendProfit(ts, var)
        breaks.append(totBrk)
        if totBrk > bestBreaks : bestBreaks = totBrk; bestVar = var
        var += 0.1
    return breaks, bestVar, bestBreaks


# Optimize TrendProfit for var parameter
# ts : the time series (array of reals)
# var : percentage of variation
# Returns : profits (for each var), best var and best profit
def OptimTrProfit(ts, maxVar):
    profs = []
    var = 0.1
    bestVar = 0
    bestProf = 0
    while var <= maxVar:
        tf, totBrk, totPft = tm.TrendProfit(ts, var)
        profs.append(totPft)
        if totPft > bestProf : bestProf = totPft; bestVar = var
        var += 0.1
    return profs, bestVar, bestProf


