import sys
sys.path.append('D:/source/repos')
from utilities.std_imports import *
import datetime
import struct
import time

# Generate time series from array or list. No holidays (continuous)
def gen_ts(start, values, freq='1d'):
    dates = pd.date_range(start=start, periods=len(values), freq=freq)
    ts = pd.Series(values)
    ts.index = dates
    return ts    

# Serialize and deserialize date sequences
def serialize_dates(dts):
    stamps = [time.mktime(dt.timetuple()) for dt in dts]
    bdts = np.array(stamps).tobytes()
    return bdts

def unserialize_dates(bdts):
    stamps = np.frombuffer(bdts, dtype=np.dtype(np.float64))
    dts = [datetime.datetime.fromtimestamp(stamp) for stamp in stamps]
    return dts

if __name__ == "__main__":
    
    #ts = gen_ts('2020-01-06', values)
    #plt.figure(figsize=(14,4))
    #plt.plot(ts);
    
    dt1 = datetime.datetime.strptime('13/05/2020', '%d/%m/%Y')
    dt2 = datetime.datetime.strptime('14/05/2020', '%d/%m/%Y')
    dt3 = datetime.datetime.strptime('15/05/2020', '%d/%m/%Y')
    dts = [dt1, dt2, dt3]
    print(dts)
    
    bdts = serialize_dates(dts)
    print(bdts)
    
    dts_recovered = unserialize_dates(bdts)
    print(dts_recovered)