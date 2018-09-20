# Plot Midprice
import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns
sns.set()
sns.set_context("talk")
sns.set_style("ticks")

sns.axes_style(rc={'axes.grid': True})


import matplotlib.dates as mdates
import pytz

import pandas as pd

def MakeVolatilityPlot(SimOrderBooks, time_window=None):
    if time_window == None:
        time_window = [pd.to_datetime("2017-10-02 9:30:00  -4"),
                       pd.to_datetime("2017-10-02 16:00:00 -4")]

    fig,ax = pl.subplots()

    DayTicks = []
    offset = 0
    DayTicks.append(offset)
    for SimOrderBook in SimOrderBooks:
        x, y = SimOrderBook.get_volatility(interval_sec = 60. , num_intervals = 10, get_timestamps=True)
        dates = pd.to_datetime(x, unit=SimOrderBook._time_tick_unit)
        ax.plot(dates,y, '-', alpha=1.)

    xfmt = mdates.DateFormatter('%H:%M', tz = pytz.timezone("America/New_York"))
    ax.xaxis.set_major_formatter(xfmt)
    ax.set_xlim(time_window)
    fig.autofmt_xdate()
    ax.yaxis.grid()
    ax.set_title("Volatility of %i runs"%(len(SimOrderBooks)))
    ax.set_ylabel("Volatility, \$")
    ax.set_xlabel("Time")
    ax.legend()
    sns.despine(left=True)

    fig.show()
    return fig

def MakeVolatilityDistributionPlot(SimOrderBooks, time_window=None):
    if time_window == None:
        time_window = [pd.to_datetime("2017-10-02 9:30:00  -4"),
                       pd.to_datetime("2017-10-02 16:00:00 -4")]

    fig,ax = pl.subplots()

    DayTicks = []
    offset = 0
    DayTicks.append(offset)
    for SimOrderBook in SimOrderBooks:
        x, y = SimOrderBook.get_volatility(interval_sec = 60. , num_intervals = 10, get_timestamps=True)
        dates = pd.to_datetime(x)
        ax.hist(y[~np.isnan(y)], bins= 50)


    ax.yaxis.grid()
    ax.set_title("Volatility Distribution of %i runs"%(len(SimOrderBooks)))
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Volatility, \$")
    ax.legend()
    sns.despine(left=True)

    fig.show()
    return fig