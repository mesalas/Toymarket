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

def make_volume_volatility_scatter_plot(trades_logs,SimOrderBooks, sampling_time, time_window = None):
    # TODO: Axis text
    # TODO: make sure it works for both market data nad simulated data. Timestamps are in ns or ms and lables are different
    if time_window == None:
        time_window = [pd.to_datetime("2017-10-02 9:30:00  -4"),
                       pd.to_datetime("2017-10-02 16:00:00 -4")]

    fig,ax = pl.subplots()

    DayTicks = []
    offset = 0
    DayTicks.append(offset)
    for trades_log,SimOrderBook in zip(trades_logs, SimOrderBooks):

        x, y = SimOrderBook.get_volatility(interval_sec = sampling_time , num_intervals = 10, get_timestamps=True)
        dates = pd.to_datetime(x, unit=SimOrderBook._time_tick_unit)
       # ax2 = ax.twinx()
        # ax2.plot(dates[:],y, '-', alpha=1., color = "orange")

        #trades_log = trades_log[(trades_log["Action"] == "COMPLETE")]  # Grab completed orders. needed for simulation trades
        trades_sample_indecies = SimOrderBook._sample_interval(trades_log["TIMESTAMP"].as_matrix(), sampling_time, return_index=True)
        trades_volume_per_sample = [trades_log["SIZE"].iloc[trades_sample_indecies[i]:trades_sample_indecies[i+1]].sum() for i in range(len(trades_sample_indecies)-1)]
        #trades_volume_per_sample = trades_log["SIZE"].iloc[trades_sample_indecies]
        timestamps = trades_log["TIMESTAMP"].iloc[trades_sample_indecies]
        # dates = pd.to_datetime(timestamps, unit = SimOrderBook._time_tick_unit)
        # traded_vol_mean = pd.Series(trades_volume_per_sample) #.rolling(window=10, center=False).mean()
         # y = y**0.5
        #trades_volume_per_sample = np.array(trades_volume_per_sample)**0.5
        ax.plot(y, trades_volume_per_sample, '.')



   # xfmt = mdates.DateFormatter('%H:%M' , tz = pytz.timezone("America/New_York"))
  #  ax.xaxis.set_major_formatter(xfmt)
  #  fig.autofmt_xdate()
    ax.yaxis.grid()
   # ax.set_xlim(time_window)

#    ax.set_title("Volatility of %i runs"%(len(SimOrderBooks)))
    ax.set_ylabel("Volume")
    ax.set_xlabel("Time")
    ax.legend()
    sns.despine(left=True)

    fig.show()
    return fig
