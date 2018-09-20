import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns
from scipy.optimize import curve_fit
sns.set()
sns.set_context("talk")
sns.set_style("ticks")

sns.axes_style(rc={'axes.grid': True})


import matplotlib.dates as mdates
import pytz

def get_SellWatingTimesdIndexes(start_index,end_index,dPrice, MidPrice):
    '''
    Fuction to find the relative distance (in indexes relative to the start index) until the midprice at the start index has moved dP

    Parameters:

        start_index : int specifies the starting index in the midprice array. Is between 0 and len(MidPrice)
        dPrice : list of the price changes relative to the midprice at start_index to calculate the index distance to
        MidPrice: numpy array of midprices

    Returns:
        dIndex : numpy array of the distance in index where the midprice hits dP. it has the dimension of dPrice
    '''
    dIndex = np.array([np.argmax(MidPrice[start_index:end_index] > MidPrice[start_index] + dP) for dP in dPrice])
    return dIndex

def get_BuyWatingTimesdIndexes(start_index,end_index, dPrice, MidPrice):
    dIndex = np.array([np.argmax(MidPrice[start_index:end_index] < MidPrice[start_index] + dP) for dP in dPrice])
    return dIndex

def get_WaitingTimes(dIndex,TimeStamps,start_index, reference_timestamps, reference_start_index, time_stamp_scale = 1e-9):
    dTime = []
    for i in dIndex:
        if i < 0:
            dTime.append(np.nan)
        else:
            dTime.append(time_stamp_scale * (TimeStamps[i + start_index] - reference_timestamps[reference_start_index]))

    return dTime

def ShowWaitingTimes(SimOrderBook, start_index):
    TimeStamps, MidPrice= SimOrderBook.get_midprice(get_timestamps=True)
    dPrice = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]  # Distance from mid price
    dIndex = get_SellWatingTimesdIndexes(start_index, dPrice, MidPrice)
    fig,ax = pl.subplots()
    end_index = start_index+dIndex[-1]
    ax.plot(TimeStamps[start_index:end_index+1], MidPrice[start_index:end_index+1])
    for dI,dP in zip(dIndex,dPrice):
        ax.plot([TimeStamps[start_index],TimeStamps[start_index+dI]], [ MidPrice[start_index] + dP, MidPrice[start_index] + dP])

    dPrice = [0.0, -0.01, -0.02, -0.03, -0.04, -0.05]  # Distance from mid price
    dIndex = get_BuyWatingTimesdIndexes(start_index, dPrice, MidPrice)
    end_index = start_index+dIndex[-1]
    ax.plot(TimeStamps[start_index:end_index+1], MidPrice[start_index:end_index+1])
    for dI,dP in zip(dIndex,dPrice):
        ax.plot([TimeStamps[start_index],TimeStamps[start_index+dI]], [ MidPrice[start_index] + dP, MidPrice[start_index] + dP])

    fig.show()
def exponential_model(t, a, gamma):
    return a*np.exp(-1.*np.abs(t)*gamma)

def PlotWaitingTimes(SimOrderBooks, SamplingTime = 60.):
    fig,ax = pl.subplots()

    for SimOrderBook in SimOrderBooks:
        TimeStamps, MidPrice = SimOrderBook.get_midprice(get_timestamps=True)
        sample_indexes = SimOrderBook._sample_interval(TimeStamps,SamplingTime, return_index = True)
        EndTimestamps = np.zeros(len(sample_indexes), dtype=np.int64)

        for i,sample_index in enumerate(sample_indexes):
            EndTimestamps[i] = TimeStamps[sample_index] + np.long(60.*2.*1./SimOrderBook._time_tick_sec) # Offset original timestamp by 10 min in nano seconds
            if EndTimestamps[i] >= TimeStamps[-1]:
                EndTimestamps[i] = TimeStamps[-1]


        sample_end_indexes,x = SimOrderBook._sample_at_time(TimeStamps,EndTimestamps)


        dPrice = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]  # Distance from mid price
        WaitingTimes = []
        for start_index,end_index in zip(sample_indexes,sample_end_indexes):
            if start_index < end_index:
                dIndex = get_sell_lo_waiting_times_dindices(start_index, end_index, MidPrice, dPrice, start_index, MidPrice)
                #dIndex = get_SellWatingTimesdIndexes(start_index,end_index, dPrice, MidPrice)
                dTime = get_WaitingTimes(dIndex, TimeStamps, start_index, TimeStamps, start_index, time_stamp_scale=SimOrderBook._time_tick_sec)
                WaitingTimes.append(dTime)

        WaitingTimes = np.array(WaitingTimes)
        MeanIntensity = np.nanmean(WaitingTimes,axis = 0)
        ax.plot(dPrice, 1./MeanIntensity, 'o')
        popt, pcov = curve_fit(exponential_model, xdata=dPrice, ydata=1./MeanIntensity)
        ax.plot(dPrice,exponential_model(dPrice, popt[0], popt[1]), '--', label = r"A %0.2e , $\gamma = $ %0.2e"%(popt[0], popt[1]))

        dPrice = [-0.0, -0.01, -0.02, -0.03, -0.04, -0.05]  # Distance from mid price
        WaitingTimes = []
        for start_index,end_index in zip(sample_indexes,sample_end_indexes):
            if start_index < end_index:
                dIndex = get_buy_lo_waiting_times_dindices(start_index, end_index, MidPrice, dPrice, start_index, MidPrice)
                #dIndex = get_BuyWatingTimesdIndexes(start_index,end_index, dPriceSell, MidPrice)
                dTime = get_WaitingTimes(dIndex, TimeStamps, start_index, TimeStamps, start_index, time_stamp_scale=SimOrderBook._time_tick_sec)
                WaitingTimes.append(dTime)

        WaitingTimes = np.array(WaitingTimes)
        MeanIntensity = np.nanmean(WaitingTimes,axis = 0)

        ax.plot(dPrice, 1./MeanIntensity, 'o')
        popt, pcov = curve_fit(exponential_model, xdata=dPrice, ydata=1./MeanIntensity)

        ax.plot(dPrice,exponential_model(dPrice, popt[0], popt[1]), '--', label = r"A %0.2e , $\gamma = $ %0.2e"%(popt[0], popt[1]))
        #for i in range(len(dPriceSell)):
        #    ax.hist( WaitingTimes[:,i], bins=50)
        #ax.set_yscale("log")
    ax.legend()
    fig.show()


def get_buy_lo_waiting_times_dindices(start_index, end_index, price, dPrice, mid_price_start_index, mid_price):
    '''
    Fuction to find the relative distance (in indexes relative to the start index) until the midprice at the start index has moved dP

    Parameters:

        start_index : int specifies the starting index in the midprice array. Is between 0 and len(MidPrice)
        dPrice : list of the price changes relative to the midprice at start_index to calculate the index distance to
        MidPrice: numpy array of midprices

    Returns:
        dIndex : numpy array of the distance in index where the midprice hits dP. it has the dimension of dPrice
    '''
    dIndex = np.zeros(len(dPrice), dtype = np.int)
    for i,dP in enumerate(dPrice):
        dIndex[i] = np.argmax(price[start_index:end_index] < mid_price[mid_price_start_index] + dP)
        if not np.any(price[start_index:end_index] < mid_price[mid_price_start_index] + dP):
            dIndex[i] = -1
    return dIndex

def get_sell_lo_waiting_times_dindices(start_index, end_index, price, dPrice, mid_price_start_index, mid_price):
    '''
    Fuction to find the relative distance (in indexes relative to the start index) until the midprice at the start index has moved dP

    Parameters:

        start_index : int specifies the starting index in the midprice array. Is between 0 and len(MidPrice)
        dPrice : list of the price changes relative to the midprice at start_index to calculate the index distance to
        MidPrice: numpy array of midprices

    Returns:
        dIndex : numpy array of the distance in index where the midprice hits dP. it has the dimension of dPrice
    '''
    dIndex = np.zeros(len(dPrice), dtype = np.int)
    for i,dP in enumerate(dPrice):
        dIndex[i] = np.argmax(price[start_index:end_index] > mid_price[mid_price_start_index] + dP)
        if not np.any(price[start_index:end_index] > mid_price[mid_price_start_index] + dP):
            dIndex[i] = -1
    return dIndex

def Get_Simulation_MOs(MarketOrders, side):
    market_orders = MarketOrders[(MarketOrders["Action"] == "COMPLETE") & (MarketOrders["Side"] == side)] # Grab completed orders of the desired side (eihter "sell" or "buy")
    market_orders_timestamps = SellMOsTimestamps = market_orders["Nanos"].as_matrix() # Grab the timestamps
    market_orders_prices = market_orders["AvgPrice"].as_matrix() # Grab the market order avg price
    return market_orders_timestamps,market_orders_prices

def Plot_LOHitTime(MarketOrdersLog, SimOrderBooks, SamplingTime):
    ''''
    Function for plotting the  waiting time before an LO is hit by an MO. It uses the order book to calculate
     the mid-price and the trades log to get the limit order trade prices
    Parameters:
        MarketOrders : Pandas DataFrame, Market order log
        SimOrderBook : Pandas DataFrame, Order book log
        SamplingTime : double. Time between each sampling

    Returns:
        fig : Matplotlib figure
    '''
    fig, ax = pl.subplots()
    for MarketOrders, SimOrderBook in zip(MarketOrdersLog,SimOrderBooks):
        # Grab and prepare market order data
        SellMOsTimestamps, SellMOsAvgPrice = Get_Simulation_MOs(MarketOrders, side="SELL")
        BuyMOsTimestamps, BuyMOsAvgPrice= Get_Simulation_MOs(MarketOrders, side="BUY")

        # Grab and prepare mid-price
        TimeStamps, MidPrice = SimOrderBook.get_midprice(get_timestamps=True)

        # Get indices of t0 times where we want to sample
        LO_sample_indices = SimOrderBook._sample_interval(TimeStamps, SamplingTime, return_index=True)


        # Find the indices in the MO data that corresponds to the samples in the mid price
        MO_sample_indices = np.asarray([np.argmax(SellMOsTimestamps >= TimeStamps[i]) for i in LO_sample_indices])

        mo_sample_end_time_stamps = np.zeros(len(MO_sample_indices))
        for i,sample_index in enumerate(MO_sample_indices):
            mo_sample_end_time_stamps[i] = SellMOsTimestamps[sample_index] + np.long(60*5*1e9) # Offset original timestamp by 10 min in nano seconds
            if mo_sample_end_time_stamps[i] >= TimeStamps[-1]:
                mo_sample_end_time_stamps[i] = TimeStamps[-1]

        mo_sample_end_indices, x = SimOrderBook._sample_at_time(SellMOsTimestamps, mo_sample_end_time_stamps)

        dPriceBuy = [0.0, -0.01, -0.02, -0.03, -0.04, -0.05]  # Distance from mid price

        WaitingTimes = []
        for start_index, stop_index, lo_start_index in zip(MO_sample_indices,mo_sample_end_indices,LO_sample_indices):
            if start_index < stop_index:

                dIndex = get_buy_lo_waiting_times_dindices(start_index,stop_index,SellMOsAvgPrice,dPriceBuy, lo_start_index,MidPrice)

                dTime = get_WaitingTimes(dIndex, SellMOsTimestamps, start_index, TimeStamps, lo_start_index)
                WaitingTimes.append(dTime)
        WaitingTimes = np.array(WaitingTimes)

        ax.plot(dPriceBuy, 1./np.nanmean(WaitingTimes, axis = 0), 'o-', color = "orange")
        popt, pcov = curve_fit(exponential_model, xdata=dPriceBuy, ydata=1. / np.nanmean(WaitingTimes, axis=0))

        ax.plot(dPriceBuy, exponential_model(dPriceBuy, popt[0], popt[1]), '--',
                label=r"A %0.2e , $\gamma = $ %0.2e" % (popt[0], popt[1]))

        # Make buy orders plot
        MO_sample_indices = np.asarray([np.argmax(BuyMOsTimestamps >= TimeStamps[i]) for i in LO_sample_indices])

        mo_sample_end_time_stamps = np.zeros(len(MO_sample_indices))
        for i, sample_index in enumerate(MO_sample_indices):
            mo_sample_end_time_stamps[i] = BuyMOsTimestamps[sample_index] + np.long(
                60 * 5 * 1e9)  # Offset original timestamp by 10 min in nano seconds
            if mo_sample_end_time_stamps[i] >= TimeStamps[-1]:
                mo_sample_end_time_stamps[i] = TimeStamps[-1]

        mo_sample_end_indices, x = SimOrderBook._sample_at_time(BuyMOsTimestamps, mo_sample_end_time_stamps)

        dPriceBuy = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]  # Distance from mid price

        WaitingTimes = []
        for start_index, stop_index, lo_start_index in zip(MO_sample_indices, mo_sample_end_indices, LO_sample_indices):
            if start_index < stop_index:
                dIndex = get_sell_lo_waiting_times_dindices(start_index, stop_index, BuyMOsAvgPrice, dPriceBuy,
                                                           lo_start_index, MidPrice)

                dTime = get_WaitingTimes(dIndex, BuyMOsTimestamps, start_index, TimeStamps, lo_start_index)
                WaitingTimes.append(dTime)
        WaitingTimes = np.array(WaitingTimes)

        ax.plot(dPriceBuy, 1. / np.nanmean(WaitingTimes, axis=0), 'o-', color = "steelblue")
        popt, pcov = curve_fit(exponential_model, xdata=dPriceBuy, ydata=1. / np.nanmean(WaitingTimes, axis=0))

        ax.plot(dPriceBuy, exponential_model(dPriceBuy, popt[0], popt[1]), '--',
                label=r"A %0.2e , $\gamma = $ %0.2e" % (popt[0], popt[1]))
    ax.yaxis.grid()
    ax.set_ylabel("Market order intensity, orders/sec")
    ax.set_xlabel("Distance from mid-price, $")
    sns.despine(left=True)
    fig.tight_layout()
    fig.show()
    return fig

