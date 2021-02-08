from Forecasting import *


# 1. ARIMA(1,1,1) model on the U.S. Wholesale Price Index (WPI) dataset
def Model():
    # Dataset
    wpi1 = requests.get('http://www.stata-press.com/data/r12/wpi1.dta').content
    data = pd.read_stata(BytesIO(wpi1))['wpi']
   
    # Fit the model
    model = sm.tsa.statespace.SARIMAX(data, trend='c', order=(1,1,1))
    res = model.fit(disp=False)
    print(res.summary())

# EXAMPLE 2

def ModelAndCharts():
    # Dataset
    wpi1 = requests.get('http://www.stata-press.com/data/r12/wpi1.dta').content
    data = pd.read_stata(BytesIO(wpi1))
    data.index = data.t
    data['ln_wpi'] = np.log(data['wpi'])
    data['D.ln_wpi'] = data['ln_wpi'].diff()

    # Graph data
    fig, axes = plt.subplots(1, 2, figsize=(15,4))

    # Levels
    axes[0].plot(data.index._mpl_repr(), data['wpi'], '-')
    axes[0].set(title='US Wholesale Price Index')

    # Log difference
    axes[1].plot(data.index._mpl_repr(), data['D.ln_wpi'], '-')
    axes[1].hlines(0, data.index[0], data.index[-1], 'r')
    axes[1].set(title='US Wholesale Price Index - difference of logs');

    # Graph data
    fig, axes = plt.subplots(1, 2, figsize=(15,4))
    fig = sm.graphics.tsa.plot_acf(data.iloc[1:]['D.ln_wpi'], lags=40, ax=axes[0])
    fig = sm.graphics.tsa.plot_pacf(data.iloc[1:]['D.ln_wpi'], lags=40, ax=axes[1])

    plt.show()

    # Fit the model
    mod = sm.tsa.statespace.SARIMAX(data['ln_wpi'], trend='c', order=(1,1,1))
    res = mod.fit(disp=False)
    print(res.summary())

def Model2():
    # Dataset
    air2 = requests.get('http://www.stata-press.com/data/r12/air2.dta').content
    data = pd.read_stata(BytesIO(air2))
    data.index = pd.date_range(start=datetime(data.time[0], 1, 1), periods=len(data), freq='MS')
    data['lnair'] = np.log(data['air'])

    # Fit the model
    mod = sm.tsa.statespace.SARIMAX(data['lnair'], order=(2,1,0), seasonal_order=(1,1,0,12), simple_differencing=True)
    res = mod.fit(disp=False)
    print(res.summary())

