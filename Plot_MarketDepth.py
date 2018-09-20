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


def Make_MarketDepthPlot(SimOrderBooks, time_window = None):
    if time_window == None:
        time_window = [pd.to_datetime("2017-10-02 9:30:00  -4"),
                       pd.to_datetime("2017-10-02 16:00:00 -4")]
    levels = 5
    Bids = [SimOrderBooks[0]._BidPrefix+"%i"%(j+1) for j in range(levels)]
    Asks = [SimOrderBooks[0]._AskPrefix+"%i"%(j+1) for j in range(levels)]
    fig,ax = pl.subplots(2,2, figsize = (10,10))
    for SimOrderBook in SimOrderBooks:
        y,x = np.histogram(SimOrderBook.OrderBook[Bids].count(axis='columns'), range = (-0.5,10.5),bins = 11)
        BinCenter = x[:-1]+(x[1:]-x[:-1])/2.
        ax[1,0].plot(y,BinCenter, 'o')
        y,x = np.histogram(SimOrderBook.OrderBook[Asks].count(axis='columns'), range = (-0.5,10.5),bins = 11)
        BinCenter = x[:-1]+(x[1:]-x[:-1])/2.
        ax[0,0].plot(y,BinCenter, 'o')

        dates = pd.to_datetime(SimOrderBook.OrderBook[SimOrderBook.timestamp_col_name], unit = SimOrderBook._time_tick_unit ,utc = True).dt.tz_convert("America/New_York")
        ax[1,1].plot(dates,  SimOrderBook.OrderBook[Bids].count(axis='columns'), '-', alpha = 1)
        ax[0,1].plot(dates, SimOrderBook.OrderBook[Asks].count(axis='columns'), '-', alpha = 1)

    ax[0,0].set_xlim([1,5e6])
    ax[0,0].set_ylabel("Sell side depth")
    ax[1,0].set_xlim([1,5e6])
    ax[1, 0].set_ylabel("Buy side depth")
    ax[1,0].set_ylim([10,0])

    ax[0,0].set_xscale("log")
    ax[0,0].yaxis.grid()

    ax[1,0].set_xscale("log")
    ax[1,0].yaxis.grid()
    #sns.despine(offset=10, trim = True)
    ax[0,0].xaxis.tick_top()

    xfmt = mdates.DateFormatter('%H:%M', tz = pytz.timezone("America/New_York"))
    ax[0,1].xaxis.set_major_formatter(xfmt)
    ax[0,1].set_xlim(time_window)
    ax[1,1].xaxis.set_major_formatter(xfmt)
    ax[1,1].set_xlabel("Time")
    ax[1,1].set_xlim(time_window)
    ax[1,1].set_ylim([10,0])

    fig.show()
    return fig