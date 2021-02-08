import unittest
from Stats.forecasting import *
from ML.forecasting import *
from Stats import Basic, Arima, Sarima
import os 
import logging
from ML import Lstm
class Test_Stats(unittest.TestCase):

    # 1. Basic
    def test11_OLS(self):
        Basic.OLS()
    def test12_ARMAProcess(self):
        Basic.ARMAProcess()
    def test13_Descomposition(self):
        Basic.Descomposition()

    # 2. Arima
    def test21_Model(self):
        Arima.Model()
    def test22_ModelAndCharts(self):
        Arima.ModelAndCharts()
    def test23_Model2(self):
        Arima.Model2()
   
    # 3. Sarima
    def test31_ModelSummary(self):
        Sarima.ModelSummary()
    def test32_FcstAndError(self):
        Sarima.FcstAndError()
    
    
    # 4. ML Models
    def test41_LSTM_Sequence(self):
        Lstm.LSTM_sequence()

if __name__ == '__main__':
    
    path = os.path.abspath(os.getcwd()) + '\\Logs'
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename = path + '\\full.log', 
    					level = logging.INFO,
    					format = LOG_FORMAT)
    
    logger = logging.getLogger()
        
    
    unittest.main()

\
