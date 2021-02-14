import sys
sys.path.append('D:/source/repos')
from utilities.std_imports import *
from scipy import integrate
import time_series.analysis.integrals as ig
import time_series.trend_analysis.splines as sp

# Integral of Ts, integral of the abs error and rel abs error 
def TsIntegError(ts1, ts2):
    err = abs(ts1 - ts2)
    integTs = integrate.simps(ts1)
    integErr = integrate.simps(err)
    relErr = integErr/integTs
    return(integTs, integErr, relErr)

# Relative integral error : i.e./ n points for ts and interpolation
def TsIntegRelPointError(ts, points):
    ips, nPs = sp.GetIPSeries(ts, points)
    integTs, integErr, relErr = TsIntegError(ts, ips)
    integIps = integTs - integErr
    irpeTs = integTs
    #irpeIps = integIps * nPs/len(ts)
    irpeIps = integIps
    return(irpeTs, irpeIps)
    
def OptimIrpe(ts, decRate=0.999, trace=False):
    points = sp.GetInflectionPointIdxs(ts)
    irpe1, irpe2 = TsIntegRelPointError(ts, points)
    #if(trace):
        #print('irpe1 = ', '{0:.2f}'.format(irpe1))
        #print('irpe2 = ', '{0:.2f}'.format(irpe2))
    bestIrpe = irpe2
    bestIdx = 0
    end=False
    while(not end):
        prevBestIrpe = bestIrpe
        end=True
        for i in range(len(points)):
            val = points[i]
            if(val!=0):
                points[i]=0
                irpe1, irpe2 = TsIntegRelPointError(ts, points)
                if(irpe2 > bestIrpe * decRate): 
                    bestIrpe = irpe2
                    bestIdx = i
                    end=False
                points[i]=val
            
        if(trace):
            print("BestIdx  : ", bestIdx)
            print("BestIrpe : ", '{0:.2f}'.format(bestIrpe))
        points[bestIdx]=0
    return(points)           



