import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def idx2bin_array(idxs, last=0):
    if(last==0): last = idxs[-1]
    binArray = [ 1 if i in idxs else 0 for i in range(0, last+1) ]
    return(binArray)

def get_bool_array(ts, idxs):
    idxs_bin = idx2bin_array(idxs)
    idxs_bin = pd.Series(idxs_bin)
    idxs_bin_pad = pad(idxs_bin, len(ts)-len(idxs_bin) , left=True)
    return np.array(idxs_bin_pad).astype(np.bool)

def ts2df_idxed(ts):
      idx = np.arange(0, len(ts))
      df = pd.DataFrame(idx,ts)
      df.set_index(idx)
      return df

def pad(ts, n, left=True, fillzeros=True):
    idxs = range(-n, ts.shape[0])
    if left:
        idxs = range(ts.shape[0] + n)
    ts_padded = ts.reindex(idxs)
    if fillzeros:
        pd.Series.fillna(ts_padded, 0, inplace=True)
    return ts_padded

def add_value(ts, val):
    idxs = range(ts.shape[0]+1)
    ts = ts.reindex(idxs) 
    ts[len(ts)-1] = val
    return ts

def gen_ts_fcst(ts_hist, fcst):
    idx = index=range(len(ts_hist), len(ts_hist)+len(fcst))
    return pd.Series(data=fcst, index=idx)

# Time series to Dataframe with column of indexes
def Ts2DfIdxed(ts):
      idx = np.arange(0, len(ts))
      df = pd.DataFrame(idx,ts)
      df.set_index(idx)
      return df

    
if __name__ == "__main__":
    print('test basic_utils\n')

    idxs = [0, 4, 6, 7, 12, 15, 18]
    ba = idx2bin_array(idxs)
    print(ba)

    dt1 = [123, 112, 118, 104, 105, 127, 114, 119, 123, 127, 132, 144]
    ts = pd.Series(data = dt1)
    idxs = [2,5]
    mask = get_bool_array(ts, idxs)
    print(mask)