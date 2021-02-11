# Basic transforms

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Array of indexes to binary (flag) array

def idx2bin_array(idxs, last=0):
    if(last==0): last = idxs[-1]
    binArray = [ 1 if i in idxs else 0 for i in range(0, last+1) ]
    return(binArray)
