from utilities.std_imports import *
import time_series.utilities.basic_utils as bu

# Plot history and forecast in the same plot
def PlotFcst(hist, fcst):
    tot = list(hist) + list(fcst)
    plt.plot(tot, color='r')
    plt.plot(hist, color='b')
    plt.show()

def plot_fcst(ts_hist, ts_fcst):
    tot = list(ts_hist) + list(ts_fcst)
    plt.plot(tot, color='r')
    plt.plot(ts_hist, color='b')
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
    
def plot_fcst_valid(train, test, fcst):
    train_plus = bu.add_value(train, test[0])
    nH = len(train_plus)
    nF = len(fcst)
    histIdx = range(len(train_plus))
    fcstIdx = range(len(train), len(train)+len(fcst))
    plt.figure()
    plt.plot(histIdx, train_plus, label='Train', color='b', lw=1.)
    plt.plot(fcstIdx, test, label='Test', color='g', lw=1.)
    plt.plot(fcstIdx, fcst, label='Fcst', color='r', lw=1.)
    plt.legend(loc='best')
    plt.show()


def plot_high(ts, points):
    mask = bu.get_bool_array(ts, points)
    xs = np.arange(len(ts))
    plt.plot(xs, ts, linestyle='-', color='blue')
    plt.plot(xs[mask], ts[mask], ':', color='red', linewidth=0, marker='o')
    plt.show()

def plot_high_mask(ts, mask):
    xs = np.arange(len(ts))
    plt.plot(xs, ts, linestyle='-', color='blue')
    plt.plot(xs[mask], ts[mask], ':', color='red', linewidth=0, marker='o')
    plt.show()
    
def plot_compare(ts1, ts2):
    fig, ax1 = plt.subplots(1,1,figsize=(22,6), dpi= 80)
    ax1.plot(ts1, color='tab:blue', linewidth=2)

    ax2 = ax1.twinx() 
    ax2.plot(ts2, color='tab:red', linewidth=0.5)

    ax1.set_xlabel('time', fontsize=12)
    ax1.set_ylabel('units', fontsize=12)

    ax1.tick_params(axis='x', rotation=0, labelsize=12)
    ax1.tick_params(axis='y', rotation=0, labelsize=12)

    ax1.grid(alpha=.4);
    
