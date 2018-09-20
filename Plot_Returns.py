import matplotlib.pyplot as pl
import seaborn as sns
sns.set()
sns.set_context("talk")
sns.set_style("ticks")

sns.axes_style(rc={'axes.grid': True})


import matplotlib.dates as mdates
import pytz
import numpy as np
import pandas as pd
def Make_ReturnsPlot(SimOrderBooks, ylims):
    fig,ax = pl.subplots()
    ax.set_ylabel("Returns, percent")
    ax.set_xlabel("Time")
    for SimOrderBook in SimOrderBooks:
        Timestamps, Returns_array= SimOrderBook.get_resampled_returns(1., get_timestamps= True, standardize = False)
        Returns_array = Returns_array * 100.
        Returns = pd.DataFrame({"Timestamps": Timestamps[1:], "Returns": Returns_array})
        ax.plot(pd.to_datetime(Returns["Timestamps"], unit= SimOrderBook._time_tick_unit),Returns["Returns"], '.')
    xfmt = mdates.DateFormatter('%H:%M', tz=pytz.timezone("America/New_York"))

    ax.xaxis.set_major_formatter(xfmt)
    ax.yaxis.grid()
    sns.despine(left=True)
    ax.set_ylim(ylims)
    fig.tight_layout()
    fig.show()
    return fig

def Make_ReturnsDistributionPlot(SimOrderBooks, ylims):
    fig,ax = pl.subplots()
    for SimOrderBook in SimOrderBooks:
        Timestamps, Returns_array= SimOrderBook.get_resampled_returns(1.0, get_timestamps= True, standardize = False)
        Returns_array = Returns_array * 100.
        Returns = pd.DataFrame({"Timestamps": Timestamps[1:], "Returns": Returns_array})
        y,x = np.histogram(np.abs(Returns.Returns[Returns["Returns"] > 0].dropna()), bins = 25, normed= False,range= [0.0,0.4])
        BinCenter = x[:-1]+(x[1:]-x[:-1])/2.
        ax.errorbar(x=BinCenter, y=y, yerr=y/np.sqrt(y) , fmt='o',mec= "white", mew = 1.)
        y,x = np.histogram(np.abs(Returns.Returns[Returns["Returns"] < 0].dropna()), bins = 25, normed= False, range= [0.0,0.4])
        BinCenter = x[:-1]+(x[1:]-x[:-1])/2.
        ax.errorbar(x=BinCenter, y=y, yerr=y/np.sqrt(y) , fmt='o', mec= "white", mew = 1.)

    tau = np.logspace(-3,np.log10(0.3))
    ax.plot(tau, 2.5e3*np.exp(-tau**2/(0.001)), "--" )
    ax.plot(tau, 0.0005*tau**(-4.5), "-", label = "Power law with $alpha = -4.5$")
    ax.set_yscale('log')
    ax.set_xlim([0,0.31])

    ax.set_ylabel("Returns dist.")
    ax.set_xlabel("Returns, percent")
    ax.set_ylim(ylims)
    #ax.set_xlim([-0.5,20])
    ax.yaxis.grid()
    sns.despine(offset=10, trim = True)
    fig.tight_layout()
    fig.show()
    return fig