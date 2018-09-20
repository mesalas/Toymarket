    # # In[149]:

    # # In[150]:
    #
    #
    # from scipy.optimize import curve_fit
    #
    # def autocorr(x, t=1):
    #     return np.corrcoef(np.array([x[0:len(x)-t], x[t:len(x)]]))
    #
    # def get_returns_autocorr(OrderBook, Sampling_interval, absolute_returns = False):
    #     Timestamps, Returns_array= OrderBook.get_resampled_returns(Sampling_interval, get_timestamps= True)
    #     if absolute_returns == True:
    #         x = np.abs(Returns_array)
    #     elif absolute_returns == False:
    #         x = Returns_array
    #     LagTime = [i for i in range(1,200)]
    #     Autocorrelation = []
    #     for i in LagTime:
    #         Autocorrelation.append(autocorr(x, t = i)[0,1])
    #     LagTime = np.array(LagTime, dtype = np.float64)*TimeScale
    #     return LagTime,Autocorrelation
    #
    #
    # TimeScale = 60. # Seconds
    # AutoCorFull = []
    # fig,ax = pl.subplots()
    # ax.set_title("Autocorrelation, %0.2f sec sampling"%TimeScale)
    # ax.set_xlabel("Lag time, sec")
    # Sec_To_Minutes = 1.
    # if TimeScale >= 60.:
    #     Sec_To_Minutes = 60.
    #     ax.set_title("Autocorrelation, %0.2f min sampling"%(TimeScale/Sec_To_Minutes))
    #     ax.set_xlabel("Lag time, min")
    #
    # for SimOrderBook in SimOrderBooks:
    #
    #     LagTime, Autocorrelation = get_returns_autocorr(SimOrderBook, Sampling_interval = TimeScale)
    #     ax.plot(LagTime/Sec_To_Minutes,Autocorrelation, '.')
    #     AutoCorFull.append([LagTime,Autocorrelation])
    # AutoCorFull = np.array(AutoCorFull)
    # ax.set_ylabel("ACF")
    #
    # ax.errorbar(x=AutoCorFull[0,0,:]/Sec_To_Minutes,
    #             y=np.average(AutoCorFull[:,1,:],  axis = 0),
    #             yerr=np.std(AutoCorFull[:,1,:],  axis = 0),
    #             fmt='ko', mec = "white", mew = 1)
    #
    #
    # ax.yaxis.grid()
    # ax.legend()
    # sns.despine(left=True)
    #
    # AutoCorFull = []
    # fig,ax = pl.subplots()
    # ax.set_title("Autocorrelation, %0.2f sec sampling"%TimeScale)
    # ax.set_xlabel("Lag time, sec")
    # Sec_To_Minutes = 1.
    # if TimeScale >= 60.:
    #     Sec_To_Minutes = 60.
    #     ax.set_title("Autocorrelation, %0.2f min sampling"%(TimeScale/Sec_To_Minutes))
    #     ax.set_xlabel("Lag time, min")
    #
    # for SimOrderBook in SimOrderBooks:
    #
    #     LagTime, Autocorrelation = get_returns_autocorr(SimOrderBook, Sampling_interval = TimeScale, absolute_returns= True)
    #     ax.plot(LagTime/Sec_To_Minutes,Autocorrelation, '.')
    #     AutoCorFull.append([LagTime,Autocorrelation])
    # AutoCorFull = np.array(AutoCorFull)
    # ax.set_ylabel("ACF")
    #
    # ax.errorbar(x=AutoCorFull[0,0,:]/Sec_To_Minutes,
    #             y=np.average(AutoCorFull[:,1,:],  axis = 0),
    #             yerr=np.std(AutoCorFull[:,1,:],  axis = 0),
    #             fmt='ko', mec = "white", mew = 1)
    #
    #
    # ax.yaxis.grid()
    # ax.legend()
    # sns.despine(left=True)
    #
    #
    # # In[151]:
    #
    #
    # def GetTimestampList(DataFrame, TimestampName, Timestamps, end_index, start_offset = 0):
    #     MatchedTimestamps = np.zeros(len(Timestamps), dtype = np.int64)
    #     Ob_Timestamps = DataFrame[TimestampName].as_matrix()
    #     LastIndex = 0 + start_offset
    #     iterations = 0
    #     for i,Timestamp in enumerate(Timestamps):
    #         StartIndex = -1
    #
    #         for Ob_Timestamp in Ob_Timestamps[LastIndex:end_index]:
    #             if Ob_Timestamp > Timestamp:
    #                 break
    #
    #             StartIndex += 1
    #             iterations += 1
    #         MatchedTimestamps[i]= StartIndex + LastIndex
    #         LastIndex = StartIndex + LastIndex
    #     #print(iterations)
    #     return MatchedTimestamps
    #
    #
    # # In[157]:
    #
    #
    # SellDiff = []
    # BuyDiff = []
    #
    # Files.MarketOrderLogsList = Files.gen_file_list("Matching-MarketOrders.csv")
    # for i,OrderBook in enumerate(SimOrderBooks):
    #     Trades = pd.read_csv(Files.File_Path+Files.MarketOrderLogsList[i]) #read trades log
    #     Trades = Trades[Trades["Action"]== "COMPLETE"] # Select only completed trades
    #     SellTrades = Trades[Trades["Side"] == "SELL"] # Select sell trades
    #     BuyTrades = Trades[Trades["Side"] == "BUY"] # Select buy trades
    #
    #     SellTimestamps = GetTimestampList(DataFrame = OrderBook.OrderBook, # get the corresponding timestamps in the orderbook
    #                  TimestampName = "Nanos",
    #                  Timestamps = SellTrades["Nanos"].as_matrix() ,
    #                  end_index = len(OrderBook.OrderBook["Ask1"]),
    #                  start_offset = 0)
    #
    #     BuyTimestamps = GetTimestampList(DataFrame = OrderBook.OrderBook,
    #                  TimestampName = "Nanos",
    #                  Timestamps = BuyTrades["Nanos"].as_matrix() ,
    #                  end_index = len(OrderBook.OrderBook["Ask1"]),
    #                  start_offset = 0)
    #
    #     SellMidprice = 0.5*(OrderBook.OrderBook["Ask1"].iloc[SellTimestamps] # get the corresponding midprices
    #                     +OrderBook.OrderBook["Bid1"].iloc[SellTimestamps])
    #     BuyMidprice  = 0.5*(OrderBook.OrderBook["Ask1"].iloc[BuyTimestamps]
    #                     +OrderBook.OrderBook["Bid1"].iloc[BuyTimestamps])
    #     # Recast as numpy arrays
    #     SellTrades = SellTrades["AvgPrice"].as_matrix()
    #     BuyTrades  = BuyTrades["AvgPrice"].as_matrix()
    #     SellMidprice = SellMidprice.as_matrix()
    #     BuyMidprice = BuyMidprice.as_matrix()
    #
    #     SellDiff.append(SellTrades-SellMidprice)
    #     BuyDiff.append(BuyTrades-BuyMidprice)
    #
    #
    # # In[153]:
    #
    #
    #
    #
    #
    # # In[186]:
    #
    #
    # fig,ax = pl.subplots(1,3, figsize = (10,5))
    # for Sell in SellDiff:
    #     ax[0].plot(Sell, 'r.',alpha = 0.05)
    # ax[0].set_ylim([-0.1,0.1])
    #
    # for Buy in BuyDiff:
    #     ax[1].plot(Buy, 'b.',alpha = 0.05)
    # ax[1].set_ylim([-0.1,0.1])
    #
    # for Sell,Buy in zip(SellDiff,BuyDiff):
    #     ax[2].hist(Buy/0.01, bins = 21, range = [-10.5, 10.5],alpha = 0.1, density= True, orientation = "horizontal", color = "blue")
    #     ax[2].hist(Sell/0.01, bins = 21, range = [-10.5, 10.5],alpha = 0.1, density= True, orientation = "horizontal", color = "red")
    # ax[2].set_ylim(-10,10)
    # ax[2].yaxis.set_ticklabels([])
    # ax[1].yaxis.set_ticklabels([])
    #
    # fig.tight_layout()
    # for axis in ax:
    #     axis.yaxis.grid()
    # sns.despine(left=True)
    #
    #
    # # In[178]:
    #
    #
    # fig,ax = pl.subplots()
    # for Sell,Buy in zip(SellDiff,BuyDiff):
    #     ax.hist(Buy/0.01, bins = 21, range = [-10.5, 10.5],alpha = 0.1, density= True)
    #     ax.hist(Sell/0.01, bins = 21, range = [-10.5, 10.5],alpha = 0.1, density= True)
    # ax.set_ylim(0,0.35)
    #
    #
    # # In[10]:
    #
    #
    # for i,AgentLog in enumerate(AgentLogs):
    #     #AgentLog.Log = AgentLog.Log.drop(AgentLog.Log.index[-1]) # drop the last row because of unfinished writing to file
    #
    #     AgentLog.Log["DateTime"] = pd.to_datetime(AgentLog.Log["Nanos"],
    #                                                     utc = True).dt.tz_convert("America/New_York") # Make a datetime column and specify that nanos are in utc and convert to localtime ie NY time
    #     AgentLog.Log = AgentLog.Log[AgentLog.Log["DateTime"].dt.weekday < 5] # Skip Weekends
    #     AgentLog.Log.set_index("DateTime", inplace=True)
    #
    #
    # # In[11]:
    #
    #
    # fig,ax = pl.subplots()
    # ax.set_title("InvMM PL")
    # for i,AgentLog in enumerate(AgentLogs):
    #     ax.plot(AgentLog.get_pl(agent_name = "InvMM-%i-0"%(i+offset)), label = str(i+offset))
    # ax.legend()
    # fig,ax = pl.subplots()
    # ax.set_title("InvMM Pos")
    # for i,AgentLog in enumerate(AgentLogs):
    #     ax.plot(AgentLog.get_pos(agent_name = "InvMM-%i-0"%(i+offset)))
    #
    # fig,ax = pl.subplots()
    # ax.set_title("InvMM Vol")
    # for i,AgentLog in enumerate(AgentLogs):
    #     ax.plot(AgentLog.get_vol(agent_name = "InvMM-%i-0"%(i+offset)))
    #
    #
    # # In[13]:
    #
    #
    # fig,ax = pl.subplots()
    # for MMLog in MMLogs:
    #     ts, BestAsk = MMLog.get_best_ask(get_timestamps=True)
    #     dates = pd.to_datetime(ts)
    #     #Spread = (BestBid- )
    #     #ax.plot(dates, BestBid)
    #     ax.plot(dates,BestAsk-MMLog.get_best_bid(), '-')
    # ax.set_title("InvMM Spread")
    # ax.set_ylim([0,0.5])
    # xfmt = mdates.DateFormatter('%H:%M', tz = pytz.timezone("America/New_York"))
    # ax.xaxis.set_major_formatter(xfmt)
    # fig.autofmt_xdate()
    # ax.yaxis.grid()
    # ax.set_xlabel("Time")
    # ax.legend()
    # ax.set_xlim(TimeWindow)
    # sns.despine(left=True)
    #
    # fig,ax = pl.subplots()
    #
    # color_gen = Generate_BlackOrGrey(100)
    # DayTicks = []
    # offset = 0
    # DayTicks.append(offset)
    # for SimOrderBook in SimOrderBooks:
    #  #, color = color_gen.__next__())
    #
    #     x,ask = SimOrderBook.get_best_ask(get_timestamps=True)
    #     bid = SimOrderBook.get_best_bid(get_timestamps=False)
    #     dates = pd.to_datetime(x)
    #     ax.plot(dates,ask-bid, '-', alpha = 1.)#, label ="Bid")
    #
    # xfmt = mdates.DateFormatter('%H:%M', tz = pytz.timezone("America/New_York"))
    # ax.xaxis.set_major_formatter(xfmt)
    # ax.set_xlim(TimeWindow)
    # fig.autofmt_xdate()
    # ax.yaxis.grid()
    # ax.set_ylim([0,0.5])
    #
    # ax.set_xlabel("Time")
    # ax.legend()
    # sns.despine(left=True)
    #
    #
    # fig,ax = pl.subplots(2)
    # for SimOrderBook in SimOrderBooks:
    #     dates = pd.to_datetime(SimOrderBook.OrderBook["Nanos"])
    #     ax[1].plot(dates,  SimOrderBook.OrderBook[Bids].count(axis='columns'), '-', alpha = 1)
    #     ax[0].plot(dates, SimOrderBook.OrderBook[Asks].count(axis='columns'), '-', alpha = 1)
    # xfmt = mdates.DateFormatter('%H:%M', tz = pytz.timezone("America/New_York"))
    # ax[0].xaxis.set_major_formatter(xfmt)
    # ax[1].xaxis.set_major_formatter(xfmt)
    #
    # fig.autofmt_xdate()
    #
    #
    # # In[161]:
    #
    #
    # TimeWindow = [pd.to_datetime("2017-10-02 9:30:00  -4"),
    #              pd.to_datetime("2017-10-02 16:00:00 -4")]
    #
    # fig,ax = pl.subplots()
    # for MMLog in [MMLogs[0]]:
    #     ts, BestAsk = MMLog.get_best_ask(get_timestamps=True)
    #     dates = pd.to_datetime(ts)
    #     ax.plot(dates,BestAsk, '-', label = "MM Best Ask")
    #
    #     ts, BestBid = MMLog.get_best_bid(get_timestamps=True)
    #     dates = pd.to_datetime(ts)
    #     ax.plot(dates,BestBid, '-', label = "MM Best Bid")
    #
    # for SimOrderBook in [SimOrderBooks[0]]:
    #  #, color = color_gen.__next__())
    #
    #     x,ask = SimOrderBook.get_best_ask(get_timestamps=True)
    #     dates = pd.to_datetime(x)
    #     bid = SimOrderBook.get_best_bid(get_timestamps=False)
    #     ax.plot(dates,ask-bid, '--', label ="Spread")
    #
    #
    # ax.set_ylim([0,1.])
    # xfmt = mdates.DateFormatter('%H:%M', tz = pytz.timezone("America/New_York"))
    # ax.xaxis.set_major_formatter(xfmt)
    # fig.autofmt_xdate()
    # ax.yaxis.grid()
    # ax.set_xlabel("Time")
    # ax.legend()
    # ax.set_xlim(TimeWindow)
    # sns.despine(left=True)
    #
    #
    # # In[160]:
    #
    #
    # fix, ax = pl.subplots()
    # SimOrderBook = SimOrderBooks[0]
    # x,ask = SimOrderBook.get_best_ask(get_timestamps=True)
    # dates = pd.to_datetime(x)
    # bid = SimOrderBook.get_best_bid(get_timestamps=False)
    # spread = (ask-bid)
    # spread = spread[~np.isnan(spread)]/0.01
    # noBins= int((spread.max()-spread.min()))+1
    # y,x = np.histogram(spread, density= True, bins=noBins, range = [-0.5000, float(int(spread.max()))])
    # BinCenter = x[:-1]+(x[1:]-x[:-1])/2.
    # ax.plot(BinCenter, y, 'o')
    # print(sum(y))
    #
    #
    # # In[ ]:
    #
    #
    # noBins
    #
    #
    # # In[ ]:
    #
    #
    # BinCenter[1:]-BinCenter[:-1]
    #
    #
    # # In[ ]:
    #
    #
    # #ReampleTS =  SimOrderBook._sample_interval(60)
    # #ResampledOB = SimOrderBook._resample_order_book(SimOrderBook.OrderBook, ReampleTS)
    # #ResampledOB.reset_index(inplace=True, drop = True)
    #
    # class CustomFormatter(Formatter):
    #     def __init__(self, dates, fmt="%m/%d"):
    #         self.dates = dates
    #         self.fmt = fmt
    #
    #     def __call__(self, x, pos=0):
    #         'Return the label for time x at position pos'
    #         ind = int(round(x))
    #         if ind>=len(self.dates) or ind<0:
    #             return ''
    #
    #         return pd.datetime.strftime(self.dates[ind], format = self.fmt)
    #
    #
    # # In[ ]:
    #
    #
    # ResampledOB.set_index("DateTime", inplace=True)
    # #ResampledOB.reset_index(inplace=True)
    #
    #
    # # In[ ]:
    #
    #
    # pd.datetime.hour(9)
    #
    #
    # # In[ ]:
    #
    #
    # dates
    #
    #
    # # In[ ]:
    #
    #
    # popt
    #
    #
    # # In[ ]:
    #
    #
    # AgentsLog.Log = AgentsLog.Log[AgentsLog.Log["AgentName"] == "InvMM-0"]
    # AgentsLog.Log = AgentsLog.Log.drop(AgentsLog.Log.index[-1]) # drop the last row because of unfinished writing to file
    #
    # AgentsLog.Log["DateTime"] = pd.to_datetime(AgentsLog.Log["Nanos"],
    #                                                     utc = True).dt.tz_convert("America/New_York") # Make a datetime column and specify that nanos are in utc and convert to localtime ie NY time
    # AgentsLog.Log = AgentsLog.Log[AgentsLog.Log["DateTime"].dt.weekday < 5] # Skip Weekends
    # AgentsLog.Log.set_index("DateTime", inplace=True)
    #
    #
    # # In[ ]:
    #
    #
    # fig,ax = pl.subplots()
    #
    # GroupedByDayLog = AgentsLog.Log.groupby(pd.Grouper(freq = "D"))
    # color_gen = Generate_BlackOrGrey(100)
    # DayTicks = []
    # offset = 0
    # for group in GroupedByDayLog:
    #     if len(group[1]) > 0 :
    #         DayTicks.append(offset)
    #         y = group[1].PL.between_time("9:30", "16:00")
    #         lengt = len(y)
    #         xrange = np.arange(start = offset ,stop = lengt+offset)
    #         ax.plot(xrange,y, '-', color = color_gen.__next__())
    #         offset += lengt
    #
    # #DayTicks.append(offset-1)
    # FMT = CustomFormatter(AgentsLog.Log.PL.between_time("9:30", "16:00").index)
    # ax.set_xticks(DayTicks)
    # ax.xaxis.set_major_formatter(FMT)
    # ax.grid()
    # fig.autofmt_xdate()
    # ax.tick_params(labelsize = 20.)
    # ax.set_ylabel("PL, \$", fontsize = 22.)
    # ax.set_xlabel("Date", fontsize = 22.)
    #
    # fig,ax = pl.subplots()
    #
    # color_gen = Generate_BlackOrGrey(100)
    # DayTicks = []
    # offset = 0
    # for group in GroupedByDayLog:
    #     if len(group[1]) > 0 :
    #         DayTicks.append(offset)
    #         y = group[1].Pos.between_time("9:30", "16:00")
    #         lengt = len(y)
    #         xrange = np.arange(start = offset ,stop = lengt+offset)
    #         ax.plot(xrange,y, '-', color = color_gen.__next__())
    #         offset += lengt
    #
    # #DayTicks.append(offset-1)
    # FMT = CustomFormatter(AgentsLog.Log.Pos.between_time("9:30", "16:00").index)
    # ax.set_xticks(DayTicks)
    # ax.xaxis.set_major_formatter(FMT)
    # ax.grid()
    # fig.autofmt_xdate()
    # ax.tick_params(labelsize = 20.)
    # ax.set_ylabel("Position", fontsize = 22.)
    # ax.set_xlabel("Date", fontsize = 22.)
    #
    # fig,ax = pl.subplots()
    #
    # color_gen = Generate_BlackOrGrey(100)
    # DayTicks = []
    # offset = 0
    # for group in GroupedByDayLog:
    #     if len(group[1]) > 0 :
    #         DayTicks.append(offset)
    #         y = group[1].Vol.between_time("9:30", "16:00")
    #         lengt = len(y)
    #         xrange = np.arange(start = offset ,stop = lengt+offset)
    #         ax.plot(xrange,y, '-', color = color_gen.__next__())
    #         offset += lengt
    #
    # #DayTicks.append(offset-1)
    # FMT = CustomFormatter(AgentsLog.Log.Vol.between_time("9:30", "16:00").index)
    # ax.set_xticks(DayTicks)
    # ax.xaxis.set_major_formatter(FMT)
    # ax.grid()
    # fig.autofmt_xdate()
    # ax.tick_params(labelsize = 20.)
    # ax.set_ylabel("Volume", fontsize = 22.)
    # ax.set_xlabel("Date", fontsize = 22.)
    #
    #
    # # In[ ]:
    #
    #
    # AgentsOrderBookName = "SPY_NYSE@1_Matching-OpenOrders.csv"
    # AgentsOrderBook_ColumNames =  ["AgentName",
    #                                              "Nanos",
    #                                              "DateTime",
    #                                              "AgentBestBidQty",
    #                                              "AgentBestBid",
    #                                              "AgentBestAsk",
    #                                              "AgentBestAskQty",
    #                                              "scale"]
    #
    # AgentsOrderBook = OrderBooks.AmmEngineAgentOrderBook(agent_name="InvMM-0",
    #                                                      order_book_file_path=LogPath+AgentsOrderBookName,
    #                                                     order_book_file_type= "Inventory market maker 2 order book log",
    #                                                     order_book_depth= 2,
    #                                                      column_names = AgentsOrderBook_ColumNames
    #                                                     )
    #
    #
    # # In[ ]:
    #
    #
    # fig,ax = pl.subplots(1,2, figsize = (10,5))
    # timestamp, midprice = SimOrderBook.get_midprice(get_timestamps=True)
    # ax[0].plot(1e-3*(timestamp-timestamp[0])/60.,midprice )
    # ax[0].set_ylabel("Midprice")
    # ax[0].set_xlabel("time, min")
    #
    # timestamp, volatility = SimOrderBook.get_volatility(60, 10, get_timestamps= True)
    # average_volatility = np.mean(volatility)**2
    # ax[1].plot(1e-3*(timestamp-timestamp[0])/60.,volatility**2 , label = "10 samples 60 sec interval, average = %f "%average_volatility)
    #
    # timestamp, volatility = SimOrderBook.get_volatility(30, 10, get_timestamps= True)
    # average_volatility = np.mean(volatility)**2
    # ax[1].plot(1e-3*(timestamp-timestamp[0])/60.,volatility**2 ,label = "10 samples 30 sec interval, average = %f "%average_volatility)
    #
    # timestamp, volatility = SimOrderBook.get_volatility(1, 300, get_timestamps= True)
    # average_volatility = np.mean(volatility)**2
    # ax[1].plot(1e-3*(timestamp-timestamp[0])/60.,volatility**2 ,label = "300 samples 1 sec interval, average = %f "%average_volatility)
    #
    #
    # ax[1].legend()
    # ax[1].set_ylabel("Volatility")
    # ax[1].set_xlabel("time, min")
    # fig.tight_layout()
    #
    # fig,ax = pl.subplots()
    # timestamp, midprice = SimOrderBook.get_midprice(get_timestamps=True)
    # ax.plot(1e-3*(timestamp-timestamp[0])/60.,midprice, label = "midprice")
    # ax.set_ylabel("Midprice, $")
    # ax.set_xlabel("time, min")
    #
    # ax2 = ax.twinx()
    # timestamp, volatility = SimOrderBook.get_volatility(60, 10, get_timestamps= True)
    # average_volatility = np.mean(volatility)**2
    # ax2.plot([0.],[0.],label = "midprice" ) # Placeholder
    # ax2.plot(1e-3*(timestamp-timestamp[0])/60.,volatility**2 , label = "10 samples 60 sec interval, average = %f "%average_volatility, color = "red")
    # ax2.set_ylabel(r"Volatility, $\sigma^2$")
    # ax2.legend()
    # fig.tight_layout()
    #
    #
    # # In[ ]:
    #
    #
    # print(pd.to_datetime(1517495400096000001))
    #
    # print(pd.to_datetime(1517495400000000000).tz_localize('UTC').dt.tz_convert("America/New_York"))
    # print(pd.to_datetime(1517518800000000001))
    # print(pd.to_datetime(1517581800000000001))
    # print(pd.to_datetime(1517605200000000001))
    #
    #
    # # In[ ]:
    #
    #
    # #Orderbook midprices
    # fig, ax = pl.subplots()
    # timestamps, midprice = SimOrderBook.get_midprice(get_timestamps=True)
    # ax.plot(pd.to_datetime(timestamps), midprice)
    # xfmt = mdates.DateFormatter('%H:%M')
    # ax.xaxis.set_major_formatter(xfmt)
    #
    # ax.set_ylabel(r"midprice, \$")
    # ax.set_xlabel("time")
    #
    #
    # # In[ ]:
    #
    #
    # fig,ax = pl.subplots(1,2, figsize = (10,5))
    # timestamp, midprice = MarketDataOrderBook1.get_midprice(get_timestamps=True)
    # ax[0].plot(1e-3*(timestamp-timestamp[0])/60.,midprice )
    # ax[0].set_ylabel("Midprice")
    # ax[0].set_xlabel("time, min")
    #
    # timestamp, volatility = MarketDataOrderBook1.get_volatility(60, 10, get_timestamps= True)
    # average_volatility = np.mean(volatility)**2
    # ax[1].plot(1e-3*(timestamp-timestamp[0])/60.,volatility**2 , label = "10 samples 60 sec interval, average = %f "%average_volatility)
    #
    # timestamp, volatility = MarketDataOrderBook1.get_volatility(30, 10, get_timestamps= True)
    # average_volatility = np.mean(volatility)**2
    # ax[1].plot(1e-3*(timestamp-timestamp[0])/60.,volatility**2 ,label = "10 samples 30 sec interval, average = %f "%average_volatility)
    #
    # timestamp, volatility = MarketDataOrderBook1.get_volatility(1, 300, get_timestamps= True)
    # average_volatility = np.mean(volatility)**2
    # ax[1].plot(1e-3*(timestamp-timestamp[0])/60.,volatility**2 ,label = "300 samples 1 sec interval, average = %f "%average_volatility)
    #
    #
    # ax[1].legend()
    # ax[1].set_ylabel("Volatility")
    # ax[1].set_xlabel("time, min")
    # fig.tight_layout()
    #
    #
    # # In[ ]:
    #
    #
    # print("Read Agent log with header:\n")
    # AgentsLog.Log.head()
    #
    #
    # # In[ ]:
    #
    #
    # fig,ax = pl.subplots()
    # ax.set_title("InvMM PL")
    # ax.plot(AgentsLog.get_pl(agent_name = "InvMM-0"))
    #
    # fig,ax = pl.subplots()
    # ax.set_title("InvMM Pos")
    #
    # ax.plot(AgentsLog.get_pos(agent_name = "InvMM-0"))
    #
    # fig,ax = pl.subplots()
    # ax.set_title("InvMM Vol")
    #
    # ax.plot(AgentsLog.get_vol(agent_name = "InvMM-0"))
    #
    #
    # # In[ ]:
    #
    #
    # fig,ax = pl.subplots()
    # timestamp, midprice = SimOrderBook.get_midprice(get_timestamps=True)
    # ax.plot(1e-9*(timestamp-timestamp[0])/60.,midprice, label = "midprice")
    # ax.set_ylabel("Midprice, $")
    # ax.set_xlabel("time, min")
    #
    # #ax2 = ax.twinx()
    # #timestamp, volatility = MarketDataOrderBook1.get_volatility(60, 10, get_timestamps= True)
    # #average_volatility = np.mean(volatility)**2
    # #ax2.plot([0.],[0.],label = "midprice" ) # Placeholder
    # #ax2.plot(1e-3*(timestamp-timestamp[0])/60.,volatility**2 , label = "10 samples 60 sec interval, average = %f "%average_volatility, color = "red")
    # #ax2.set_ylabel(r"Volatility, $\sigma^2$")
    # #ax2.legend()
    # #fig.tight_layout()
    #
    #
    # # In[ ]:
    #
    #
    # fig, ax = pl.subplots()
    # ax.plot(invMM2.get_pl())
    # fig, ax = pl.subplots()
    # ax.plot(invMM2.get_pos())
    #
    #
    # # In[ ]:
    #
    #
    # fig,ax = pl.subplots()
    # ax.plot(invMM2.get_best_ask()-invMM2.get_best_bid())
    #
    #
    # # In[ ]:
    #
    #
    # def AS_reservation_price(midprice, gamma, inventory, volatility):
    #     return midprice-gamma*inventory*volatility**2.
    # def AS_spread(gamma,volatility,workSize):
    #     return workSize*gamma*volatility**2.+0.02 #2.*np.log(1.+gamma/k)/gamma

