from Forecasting import *
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
   
# Naive Forecast
def Naive(ts, hor):
    fcst = np.full(shape=hor, fill_value=ts[len(ts)-1])
    return fcst

# Simple Average
def SimpleAvg(ts, hor):
    mean = ts.mean()
    fcst = np.full(shape=hor, fill_value=mean)
    return fcst

# Moving Average
def MovingAvg(ts, hor, mw):
    mean = ts[-mw:].mean()
    fcst = np.full(shape=hor, fill_value=mean)
    return fcst
 
# Exponential Smoothing
def ExpSmooth(ts, hor, sl):
    fit = SimpleExpSmoothing(ts).fit(smoothing_level=sl, optimized=False)
    fcst = fit.forecast(hor)
    return fcst

# Holt-Winters Linear
def HoltWintersLin(ts, hor, sl, ss):
    fit = Holt(ts).fit(smoothing_level = sl,smoothing_slope = ss)
    fcst = fit.forecast(hor)
    return fcst

# Holt-Winters 
def HoltWinters(ts, hor, sp, trd, sea):
    fit = ExponentialSmoothing(ts ,seasonal_periods=sp ,trend=trd, seasonal=sea,).fit()
    fcst = fit.forecast(hor)
    return fcst
  
# ARIMA
def Arima(ts, hor):
    fit = sm.tsa.statespace.SARIMAX(train.Count, order=(2, 1, 4),seasonal_order=(0,1,1,7)).fit()
    fcst = fit.predict(start="2013-11-1", end="2013-12-31", dynamic=True)
    return fcst