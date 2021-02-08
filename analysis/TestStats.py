from Utils.Admin.Standard import *
import unittest
from Forecasting import *
import TSAnalysis.StatsForecasting.StatsBasic as sb
import TSAnalysis.StatsForecasting.Misc as ms
import TSAnalysis.StatsForecasting.Arima as ar
import TSAnalysis.StatsForecasting.Sarima as sa
import Visual.TimeSeries.TsPlots.PlotFcst as pf
import TSAnalysis.StatsForecasting.StatsHelpers as sh

def PlotFcstValid(train, test, fcst):
    nH = len(train)
    nF = len(fcst)
    histIdx = np.arange(nH)
    fcstIdx = np.arange(nH, nH+nF)
    plt.figure()
    plt.plot(histIdx, train, label='Train', Color='b', lw=1.)
    plt.plot(fcstIdx, test, label='Test', Color='g', lw=1.)
    plt.plot(fcstIdx, fcst, label='Fcst', Color='r', lw=1.)
    plt.legend(loc='best')
    plt.show()

class TestStats(unittest.TestCase):

    # Data
    df = pd.read_csv(dataPath + 'TrainsTrain.csv')
    print(df.head())
    df = pd.read_csv(dataPath + 'TrainsTrain.csv', nrows = 11856) #subsetting
    train = df[0:10392] 
    test = df[10392:]
    trn = np.asarray(train['Count'])
    tst = np.asarray(test['Count'])
    hor = len(tst)

    # Daily aggregation
    df['Timestamp'] = pd.to_datetime(df.Datetime,format='%d-%m-%Y %H:%M') 
    df.index = df.Timestamp 
    df = df.resample('D').mean()
    train['Timestamp'] = pd.to_datetime(train.Datetime,format='%d-%m-%Y %H:%M') 
    train.index = train.Timestamp 
    train = train.resample('D').mean() 
    test['Timestamp'] = pd.to_datetime(test.Datetime,format='%d-%m-%Y %H:%M') 
    test.index = test.Timestamp 
    test = test.resample('D').mean()

    # Plot
    def test00_Plot(self):
        self.train.Count.plot(figsize=(15,8), title= 'Daily Ridership', fontsize=14)
        self.test.Count.plot(figsize=(15,8), title= 'Daily Ridership', fontsize=14)
        plt.show()

    # 1. StatsBasic
    def test11_OLS(self):
        sb.OLS()
    def test12_ARMAProcess(self):
        sb.ARMAProcess()
    def test13_Descomposition(self):
        sb.Descomposition()

    # 2. Misc
    def test21_Naive(self):
        fcst = ms.Naive(self.trn, self.hor)
        PlotFcstValid(self.trn,self.tst,fcst)

    def test22_SimpleAvg(self):
        fcst = ms.SimpleAvg(self.trn, self.hor)
        PlotFcstValid(self.trn,self.tst,fcst)

    def test23_MovingAvg(self):
        fcst = ms.MovingAvg(ts=self.trn, hor=self.hor, mw=6)
        PlotFcstValid(self.trn,self.tst,fcst)
        
    def test24_ExpSmooth(self):
        fcst = ms.ExpSmooth(ts=self.trn, hor=self.hor, sl=0.6)
        PlotFcstValid(self.trn,self.tst,fcst)
    
    def test25_HoltWintersLin(self):
       fcst = ms.HoltWintersLin(ts=self.trn, hor=self.hor, sl=0.3, ss=0.1)
       PlotFcstValid(self.trn,self.tst,fcst)
   
    def test26_HoltWinters(self):
       fcst = ms.HoltWinters(ts=self.trn, hor=self.hor, sp=7, trd='add', sea='add')
       PlotFcstValid(self.trn,self.tst,fcst)
   
    def test27_Arima(self):
       idx = pd.date_range(pd.to_datetime("2000-01-01"), periods=len(self.trn)).tolist()
       val = self.trn
       data = pd.DataFrame(val)
       data.index = idx
       mod = sm.tsa.statespace.SARIMAX(data, order=(1,0,1))
       ft = mod.fit()
       s = pd.to_datetime("19-02-2000",dayfirst=True)
       e = s + pd.DateOffset(days=self.hor-1)
       fcstSeries = ft.predict(start=s, end=e, dynamic=True)
       fcst = fcstSeries.values
       PlotFcstValid(self.trn,self.tst,fcst)
    

    # 3. Arima
    def test31_Model(self):
        ar.Model()
    def test32_ModelAndCharts(self):
        ar.ModelAndCharts()
    def test33_Model2(self):
        ar.Model2()
   
    # 3. Sarima
    def test41_ModelSummary(self):
        sa.ModelSummary()
    def test42_FcstAndError(self):
       sa.FcstAndError()
    

if __name__ == '__main__':
    unittest.main()

