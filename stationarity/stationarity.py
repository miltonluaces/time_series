import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams["figure.figsize"] = (12,6)

def ts_dist(ts, nsplit):
    split = (int)(ts.shape[0]/nsplit)
    start=0
    Ts = []
    for i in range(nsplit):
        end=start+split
        Ts.append(ts[start:end])
        start=end+1
        end=start+split
    for ts in Ts:
        sns.displot(ts, kde=True);
        #sns.distplot(ts);
        
