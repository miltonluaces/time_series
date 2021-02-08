import numpy as np

def MA(ts, mw):
    cs = np.cumsum(ts, dtype=float)
    cs[mw:] = cs[mw:] - cs[:-mw]
    return cs[mw-1:]/mw

