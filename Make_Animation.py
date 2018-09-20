import matplotlib.pyplot as pl
from matplotlib.animation import FuncAnimation
import seaborn as sns
#sns.set_context("talk")
sns.set_style("ticks")
sns.axes_style(rc={'axes.grid': True})

pl.style.use("dark_background")



import matplotlib.dates as mdates
import pytz
from collections import deque
import pandas as pd



def plot_order_book(orderbook):

    fig,ax = pl.subplots()
    grouped_orderbook = orderbook.groupby(pd.Grouper(freq = "S"))  # Group order book in chunks of seconds
    for orderbook_second in grouped_orderbook:
        time = pd.to_datetime(orderbook_second[1].Nanos, unit="ns")
        ax.plot(time,orderbook_second[1].Bid1, 'ko')
        ax.plot(time,orderbook_second[1].Bid2, 'k.')
        ax.plot(time, orderbook_second[1].Bid3, 'k.')
        ax.plot(time, orderbook_second[1].Bid4, 'k.')
        ax.plot(time, orderbook_second[1].Bid5, 'k.')
        ax.plot(time, orderbook_second[1].Bid6, 'k.')
        ax.plot(time, orderbook_second[1].Bid7, 'k.')
        ax.plot(time, orderbook_second[1].Bid8, 'k.')
        ax.plot(time, orderbook_second[1].Bid9, 'k.')
        ax.plot(time, orderbook_second[1].Bid10, 'k.')

        ax.plot(time,orderbook_second[1].Ask1, 'ro')
        ax.plot(time,orderbook_second[1].Ask2, 'r.')
        ax.plot(time, orderbook_second[1].Ask3, 'r.')
        ax.plot(time, orderbook_second[1].Ask4, 'r.')
        ax.plot(time, orderbook_second[1].Ask5, 'r.')
        ax.plot(time, orderbook_second[1].Ask6, 'r.')
        ax.plot(time, orderbook_second[1].Ask7, 'r.')
        ax.plot(time, orderbook_second[1].Ask8, 'r.')
        ax.plot(time, orderbook_second[1].Ask9, 'r.')
        ax.plot(time, orderbook_second[1].Ask10, 'r.')


    xfmt = mdates.DateFormatter('%M:%S', tz=pytz.timezone("America/New_York"))
    ax.xaxis.set_major_formatter(xfmt)
    ax.yaxis.grid()
    sns.despine(left=True)
    fig.show()

def update_line(line, line_data):
    line.set_xdata(line_data[0])
    line.set_ydata(line_data[1])
    #return line

def get_line_data(line_deque):
    line_data = [[], []]
    for line_chunk in line_deque:
        for time, price in zip(line_chunk[0],line_chunk[1]):
            #line_data[0].append(pd.to_datetime(time))
            line_data[0].append(time)
            line_data[1].append(price)
    return line_data

def update_plot(orderbook_second, lines,deques, names, axis, t0):
    # update view
    if len(orderbook_second[1]) >= 1:
        midprice = 0.5*(orderbook_second[1]["Ask1"].iloc[-1]+orderbook_second[1]["Bid1"].iloc[-1])
        ylim = axis.set_ylim([midprice-0.15, midprice+0.15])

        #xfmt = mdates.DateFormatter('%H:%M', tz=pytz.timezone("America/New_York"))
        #axis.xaxis.set_major_formatter(xfmt)
        tmin = (orderbook_second[0].value -9*1e9-t0)*1e-9
        if tmin < 0:
            tmin = 0
        tmax = (orderbook_second[0].value+1e9-t0)*1e-9
        xlim = axis.set_xlim([tmin,
                              tmax]
                             )

    # Update lines
    for line, line_deque, name in zip(lines,deques,names):
        time = (orderbook_second[1]["Nanos"]-t0)*1e-9
        price = orderbook_second[1][name]
        line_deque.append([time, price])
        update_line(line, get_line_data(line_deque))

    return lines,

def create_plot(orderbook):
    fig,ax = pl.subplots()
    ax.set_ylim([100.,101.])
    ax.yaxis.grid()
    sns.despine(left=True)
    ax.set_xlabel("Time, sec")
    ax.set_ylabel("Price")

    #sns.set({"axes.facecolor": "#263238","figure.facecolor": "#263238" })
    #pl.rcParams['axes.facecolor'] = ''
    #pl.rcParams['savefig.facecolor'] = '#1C366A'
    #ax.set_xlim([0.0, pd.to_datetime(orderbook["Nanos"].iloc[-1]-)])
    #xfmt = mdates.DateFormatter('%H:%M:%S', tz=pytz.timezone("America/New_York"))
    #ax.xaxis.set_major_formatter(xfmt)
    t0 = orderbook["Nanos"].iloc[0]
    depth = 5
    lines = []
    for i in range(depth):
        line, = ax.plot([0. ], [0.], 's', color = "#FC4E51", markersize = 4, animated=True)  # create empty line
        lines.append(line)
    for i in range(depth):
        line, = ax.plot([0. ], [0.], 's', markersize = 4, color = "#1DABE6", animated=True)  # create empty line
        lines.append(line)
    lines = tuple(lines)

    deques = []
    for i in range(depth):
        deques.append(deque(maxlen=10))

    for i in range(depth):
        deques.append(deque(maxlen=10))
    deques = tuple(deques)

    names = ["Bid1","Bid2","Bid3","Bid4","Bid5",
             "Ask1","Ask2","Ask3","Ask4","Ask5",]

    grouped_orderbook = orderbook.groupby(pd.Grouper(freq="S"))  # Group order book in chunks of seconds

    ani = FuncAnimation(fig, update_plot, frames=grouped_orderbook, fargs=(lines, deques, names, ax, t0), interval=50, blit= False)
    ani.save(filename= "OBani.mp4", savefig_kwargs={'transparent': True, 'facecolor': '#263238'})
    fig.show()






