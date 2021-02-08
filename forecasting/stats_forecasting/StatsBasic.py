import statsmodels as sm


# Ordinary Least Squares
def OLS():
    dat = sm.datasets.get_rdataset("Guerry", "HistData").data
    results = smf.ols('Lottery ~ Literacy + np.log(Pop1831)', data=dat).fit() # using log of one of the regressors
    print(results.summary())

# ARMA Process
def ARMAProcess():
    arparams = np.array([.75, -.25])
    maparams = np.array([.65, .35])
    ar = np.r_[1, -arparams] # add zero-lag and negate
    ma = np.r_[1, maparams]  # add zero-lag
    ap = sm.tsa.ArmaProcess(ar, ma)
    print(ap.isstationary)
    print(ap.isinvertible)
    y = ap.generate_sample(250)
    model = sm.tsa.ARMA(y, (2, 2)).fit(trend='nc', disp=0)
    print(model.params)

# Descomposition
def Descomposition():
    df = pd.read_csv('Data/MilkProd.csv')
    dates = df.iloc[:,0:].values.flatten()
    datess = pd.to_datetime(dates[:168])
    values = df.iloc[:,1:].values.flatten()
    ts = pd.Series(values, datess)
    res = smt.seasonal.seasonal_decompose(ts, freq=12, model='additive')
    print(res.trend)
    print(res.seasonal)
    print(res.resid)
    print(res.observed)

    res.plot()
    plt.show()


import numpy as np
import pandas as pd
import scipy.stats as ss

def OLSFcst(ts, hor):
    hor = 20
    idx = np.arange(0, len(ts))
    res = sp.stats.linregress(idx, ts)
    idx = np.arange(len(ts)+1, len(ts) + hor+1)
    fcst = idx * res.slope + res.intercept
    return(fcst)
