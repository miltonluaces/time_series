import matplotlib.pyplot as plt

# Plot history and forecast in the same plot
def PlotFcst(hist, fcst):
    tot = list(hist) + list(fcst)
    plt.plot(tot, color='r')
    plt.plot(hist, color='b')
    plt.show()

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

