import numpy as np
import pandas as pd

# Transform an asc list of indexes in a binary array
def Idx2BinArray(idxs, last=0):
    if(last==0): last = idxs[-1]
    binArray = [ 1 if i in idxs else 0 for i in range(0, last+1) ]
    return(binArray)
    
# Time series to Dataframe with column of indexes
def Ts2DfIdxed(ts):
      idx = np.arange(0, len(ts))
      df = pd.DataFrame(idx,ts)
      df.set_index(idx)
      return df

