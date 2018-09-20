import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns
sns.set()
sns.set_context("talk")
sns.set_style("ticks")

sns.axes_style(rc={'axes.grid': True})

from multiprocessing import Pool, cpu_count

def autocorr(x, t=1):
        return np.corrcoef(np.array([x[0:len(x)-t], x[t:len(x)]]))

def get_returns_autocorr(OrderBook, Sampling_interval, absolute_returns = False):
    Timestamps, Returns_array= OrderBook.get_resampled_returns(Sampling_interval, get_timestamps= True)
    if absolute_returns == True:
        x = np.abs(Returns_array)
    elif absolute_returns == False:
        x = Returns_array
    LagTime = [i for i in range(1,200)]
    Autocorrelation = []
    for i in LagTime:
        Autocorrelation.append(autocorr(x, t = i)[0,1])
    LagTime = np.array(LagTime, dtype = np.float64)*Sampling_interval
    return LagTime,Autocorrelation

def get_returns_autocorr_Wrapper(parameters):
    SimOrderBook = parameters[0]
    TimeScale = parameters[1]
    AbsoluteCorrelation = parameters[2]

    LagTime, Autocorrelation = get_returns_autocorr(SimOrderBook, Sampling_interval=TimeScale,
                                                    absolute_returns=AbsoluteCorrelation)
    return [LagTime, Autocorrelation]


def MakeAutocorrelationPlot(SimOrderBooks, TimeScale = 60., AbsoluteCorrelation = False):
    fig,ax = pl.subplots()
    ax.set_title("Autocorrelation, %0.2f sec sampling"%TimeScale)
    ax.set_xlabel("Lag time, sec")
    Sec_To_Minutes = 1.
    if TimeScale >= 60.:
        Sec_To_Minutes = 60.
        ax.set_title("Autocorrelation, %0.2f min sampling"%(TimeScale/Sec_To_Minutes))
        ax.set_xlabel("Lag time, min")
    with Pool(cpu_count()) as p:
        Autocorrelations = p.map(get_returns_autocorr_Wrapper, [[SimOrderBook, TimeScale, AbsoluteCorrelation] for SimOrderBook in SimOrderBooks])

    Autocorrelations = np.array(Autocorrelations)
    for Autocorrelation in Autocorrelations:
        ax.plot(Autocorrelation[0] / Sec_To_Minutes, Autocorrelation[1], '.')

    ax.set_ylabel("ACF")
    if AbsoluteCorrelation == True:
        ax.set_ylabel("Absolute ACF")

    ax.errorbar(x=Autocorrelations[0,0]/Sec_To_Minutes,
                y=np.average(Autocorrelations[:,1], axis= 0),
                yerr=np.std(Autocorrelations[:,1],  axis = 0),
                fmt='ko', mec = "white", mew = 1)


    ax.yaxis.grid()
    ax.legend()
    sns.despine(left=True)
    fig.tight_layout()
    fig.show()
    return fig