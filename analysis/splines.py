import numpy as np
import pandas as pd

# Determine inflection points 
def GetInflectionPointIdxs(ts):
    ip = np.zeros(len(ts))
    for i in (range(1,len(ts)-1)):
        if(ts[i] > ts[i-1] and ts[i] > ts[i+1]):
           ip[i] = 1
        elif(ts[i] < ts[i-1] and ts[i] < ts[i+1]): 
            ip[i] = -1
    return(ip)

# Get the ts formed by only the inflection points
def GetIPSeries(ts, ip, interpolate=True):
    ips = np.zeros(len(ts))
    for i in range(len(ts)):
        if(ip[i] != 0): ips[i]=ts[i]
        else: ips[i] = np.nan
    ips[0] = ts[0]
    ips[-1] = ts[-1]
    nPs = len(ips[~np.isnan(ips)])
    if(interpolate): 
        df = pd.DataFrame(ips)
        interp = df.interpolate(method='linear')
        ips = np.asarray(interp[0])
    return ips, nPs
