from Forecasting import *

# Dataset
def ModelSummary():
    friedman2 = requests.get('http://www.stata-press.com/data/r12/friedman2.dta').content
    data = pd.read_stata(BytesIO(friedman2))
    data.index = data.time

    # Variables
    endog = data.loc['1959':'1981', 'consump']
    exog = sm.add_constant(data.loc['1959':'1981', 'm2'])

    # Fit the model
    mod = sm.tsa.statespace.SARIMAX(endog, exog, order=(1,0,1))
    res = mod.fit(disp=False)
    print(res.summary())


# Dataset
def FcstAndError():
    friedman2 = requests.get('http://www.stata-press.com/data/r12/friedman2.dta').content
    raw = pd.read_stata(BytesIO(friedman2))
    raw.index = raw.time
    data = raw.loc[:'1981']

    # Variables
    endog = data.loc['1959':, 'consump']
    exog = sm.add_constant(data.loc['1959':, 'm2'])
    nobs = endog.shape[0]

    # Fit the model
    mod = sm.tsa.statespace.SARIMAX(endog.loc[:'1978-01-01'], exog=exog.loc[:'1978-01-01'], order=(1,0,1))
    fit_res = mod.fit(disp=False)
    print(fit_res.summary())

    # 11
    mod = sm.tsa.statespace.SARIMAX(endog, exog=exog, order=(1,0,1))
    res = mod.filter(fit_res.params)

    # In-sample one-step-ahead predictions
    predict = res.get_prediction()
    predict_ci = predict.conf_int()

    # Dynamic predictions
    predict_dy = res.get_prediction(dynamic='1978-01-01')
    predict_dy_ci = predict_dy.conf_int()

    # Graph
    fig, ax = plt.subplots(figsize=(9,4))
    npre = 4
    ax.set(title='Personal consumption', xlabel='Date', ylabel='Billions of dollars')

    # Plot data points
    data.loc['1977-07-01':, 'consump'].plot(ax=ax, style='o', label='Observed')

    # Plot predictions
    predict.predicted_mean.loc['1977-07-01':].plot(ax=ax, style='r--', label='One-step-ahead forecast')
    ci = predict_ci.loc['1977-07-01':]
    ax.fill_between(ci.index, ci.iloc[:,0], ci.iloc[:,1], color='r', alpha=0.1)
    predict_dy.predicted_mean.loc['1977-07-01':].plot(ax=ax, style='g', label='Dynamic forecast (1978)')
    ci = predict_dy_ci.loc['1977-07-01':]
    ax.fill_between(ci.index, ci.iloc[:,0], ci.iloc[:,1], color='g', alpha=0.1)

    legend = ax.legend(loc='lower right')

    plt.show()

    # Prediction error

    ## Graph
    fig, ax = plt.subplots(figsize=(9,4))
    npre = 4
    ax.set(title='Forecast error', xlabel='Date', ylabel='Forecast - Actual')

    ## In-sample one-step-ahead predictions and 95% confidence intervals
    predict_error = predict.predicted_mean - endog
    predict_error.loc['1977-10-01':].plot(ax=ax, label='One-step-ahead forecast')
    ci = predict_ci.loc['1977-10-01':].copy()
    ci.iloc[:,0] -= endog.loc['1977-10-01':]
    ci.iloc[:,1] -= endog.loc['1977-10-01':]
    ax.fill_between(ci.index, ci.iloc[:,0], ci.iloc[:,1], alpha=0.1)

    # Dynamic predictions and 95% confidence intervals
    predict_dy_error = predict_dy.predicted_mean - endog
    predict_dy_error.loc['1977-10-01':].plot(ax=ax, style='r', label='Dynamic forecast (1978)')
    ci = predict_dy_ci.loc['1977-10-01':].copy()
    ci.iloc[:,0] -= endog.loc['1977-10-01':]
    ci.iloc[:,1] -= endog.loc['1977-10-01':]
    ax.fill_between(ci.index, ci.iloc[:,0], ci.iloc[:,1], color='r', alpha=0.1)

    legend = ax.legend(loc='lower left');
    legend.get_frame().set_facecolor('w')

    plt.show()