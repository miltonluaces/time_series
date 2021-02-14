import unittest
from Forecasting import *

class TestML(unittest.TestCase):

    # Data
    series = pd.Series.from_csv('Data/CarSales.csv', header=0)

    def testPlotData(self):
        print(self.series.head(5))
        self.series.plot()
        plt.show()


if __name__ == '__main__':
    unittest.main()

