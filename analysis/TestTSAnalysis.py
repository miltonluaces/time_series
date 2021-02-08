from Helpers.testing import *
import scipy as sp
import TSAnalysis.Splines as ts
import TSAnalysis.TsIntegrals as ti
import Helpers.TSMethods as ht
import Plotting.TsPlots as pp
import Parallelization.MThreadingWorkers as mw
from scipy import integrate
import time
import scipy as sp

class TestTsAnalysis(unittest.TestCase):

    # Data
    df = pd.read_csv(dataPath + 'sp500.csv')
    date = pd.to_datetime(df.iloc[:,0].values, dayfirst=True)
    price = df.iloc[:,2].values

    dfToy = pd.read_csv(dataPath + 'toy.csv')
    ts1 = dfToy.iloc[:,1].values


    # Tests
    def test00_DataLoading(self):
        plt.plot(self.date, self.price)
        plt.show()
        plt.plot(self.ts1)
        plt.show()

    def test10_GetInflectionPoints(self):
        points = ts.GetInflectionPointIdxs(self.ts1)
        print(self.ts1)
        print(points)
        values = self.ts1
        vp.PlotTsPoints2(values, points)

    def test11_GetInflectionPointsSeries(self):
        points = ts.GetInflectionPointIdxs(self.ts1)
        ips, nPs = ts.GetIPSeries(self.ts1, points)
        df = pd.DataFrame({'col1':self.ts1, 'col2':ips})
        print(df)
        print(ips)
        plt.plot(self.ts1)
        plt.plot(ips)
        plt.show()

        integTs, integErr, relErr = ti.TsIntegError(self.ts1, ips)
        print('Ts origin = ','{0:.2f}'.format(integTs))
        print('Ts interp = ','{0:.2f}'.format(integErr))
        print('Rel Err = ','{0:.2f}'.format(relErr))

    def test21_IntegralsDiff(self):
        points = ts.GetInflectionPointIdxs(self.ts1)
        irpe1, irpe2 = ti.TsIntegRelPointError(self.ts1, points)
        print('irpe1 = ', '{0:.2f}'.format(irpe1))
        print('irpe2 = ', '{0:.2f}'.format(irpe2))

    def test22_IntegralsDiffOptim(self):
        points = ti.OptimIrpe(ts=self.ts1, decRate=0.999, trace=True)
        vp.PlotTsPoints2(self.ts1, points)
        vp.PlotTsPoints2Interp(self.ts1, points)
        
        idx = np.array(np.where(points != 0)).flatten()
        val = np.array(self.ts1[np.where(points != 0)])
        df = pd.DataFrame({'col1':idx, 'col2':val})
        print(df)
        
    def test23_IntegralsDiffOptim2(self):
        points = ti.OptimIrpe(ts=self.ts1, decRate=0.999, trace=True)
        pp.PlotTsPoints2(self.ts1, points)
        pp.PlotTsPoints2Interp(self.ts1, points)

    def test31_IDiffMultiThreading(self):
        TimesSeq = []
        TimesMTh = []
        t1=time.time()
        for n in range(20):
            for t in range(n):
                points1 = ti.OptimIrpe(ts=self.ts1, decRate=0.999, trace=False)
                #points2 = ti.OptimIrpe(ts=self.price, decRate=0.999, trace=False)
            t2=time.time()
            delta = t2-t1
            print("Sequential : ", '{0:.2f}'.format(delta))
            TimesSeq.append(delta)

        #pp.PlotTsPoints2Interp(self.ts1, points1)
        #pp.PlotTsPoints2Interp(self.price, points2)

            t1=time.time()
            Jobs = []
            for t in range(n):
                Jobs.append(mw.MThOptimIrpe(ts=self.ts1, decRate=0.999, trace=False))
                #Jobs.append(mw.MThOptimIrpe(ts=self.price, decRate=0.999, trace=False))
            for i in range(len(Jobs)-1): Jobs[i].start()
            for i in range(len(Jobs)-1): Jobs[i].join()
            t2=time.time()
            delta = t2-t1
            print("Multithreading : ", '{0:.2f}'.format(delta))
            TimesMTh.append(delta)
       
        #pp.PlotTsPoints2Interp(self.ts1, Jobs[0].output)
        #pp.PlotTsPoints2Interp(self.price, Jobs[1].output)

        plt.plot(TimesSeq)
        plt.plot(TimesMTh)
        plt.show()



    def test10_TSMethods_Idx2BinArray(self):
        idxs = [0, 1, 3, 6]
        binArr1 = ht.Idx2BinArray(idxs)
        print(binArr1)
        binArr2 = ht.Idx2BinArray(idxs,9)
        print(binArr2)

if __name__ == '__main__':
    unittest.main()
       

# Once we have the trends, consider:
# 1. number of periods the trend is ongoing (current spline)
# 2. slope of the spline
# Regression: if there will be an inflection point or not
# Meassure the predictibility of a time series or a period of a ts (cross validated k-folded).

# Also use the spline to forecast trend (extrapolate the last one)
    
    
        
       
        
