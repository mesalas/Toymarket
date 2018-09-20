# Plot Midprice
import numpy as np
import matplotlib.pyplot as pl
import seaborn as sns
sns.set()
sns.set_context("talk")
sns.set_style("ticks")

sns.axes_style(rc={'axes.grid': True})
from multiprocessing import Pool, cpu_count


import matplotlib.dates as mdates
import pytz

import pandas as pd

def Plot_CashDistribution(RT_CashInventory : pd.DataFrame ,RT_Names : list):
    fig,ax = pl.subplots()
    ax.set_title("Agent Cash Histogram")
    for agent_name in RT_Names:
        current_agent_dataframe = RT_CashInventory[RT_CashInventory["AgentName"] == agent_name]
        ax.hist(current_agent_dataframe["Cash"])
    fig.show()
    return fig

def Plot_Cash(RT_CashInventory : pd.DataFrame ,RT_Names : list):
    fig,ax = pl.subplots()
    ax.set_title("Agent Cash")
    for agent_name in RT_Names:
        current_agent_dataframe = RT_CashInventory[RT_CashInventory["AgentName"] == agent_name]
        ax.plot(current_agent_dataframe["Cash"])
    fig.show()
    return fig


def Plot_Inventory(AgentsLog,RT_Names : list):
    fig, ax = pl.subplots()
    ax.set_title("Random Trader Position")
    for agent_name in RT_Names:
        ax.plot(AgentsLog.get_pos(agent_name))
    fig.show()

def Plot_Pl(AgentsLog,RT_Names : list):
    fig, ax = pl.subplots()
    ax.set_title("Random Trader Position")
    for agent_name in RT_Names:
        ax.plot(AgentsLog.get_pl(agent_name))
    fig.show()

def Plot_FinalPlDist(AgentsLogs : list,RT_Names : list):
    fig, ax = pl.subplots()
    ax.set_title("Random Trader Final PL Distribution")

    with Pool(cpu_count()) as p:
        finalPL = p.map(get_agent_final_PL, [[AgentName,AgentsLog] for AgentName,AgentsLog in zip(RT_Names, AgentsLogs)])
    finalPL = np.ravel(np.array(finalPL)) # convert to np array and ravel

    ax.hist(finalPL, bins= 50)
    ax.yaxis.grid()
    sns.despine(left=True)

    fig.show()
    return fig

def get_agent_final_PL(names_and_log  : list):
    RT_Names = names_and_log[0]
    AgentsLog = names_and_log[1]

    finalPL = []
    for agent_name in RT_Names:
        finalPL.append(AgentsLog.get_pl(agent_name).iloc[-1])
    return finalPL


def Plot_CashEarningDistribution(RT_CashInventory : pd.DataFrame ,RT_Names : list):
    fig,ax = pl.subplots()
    ax.set_title("Agent Cash Earning Histogram")
    earnings = []
    for agent_name in RT_Names:
        current_agent_dataframe = RT_CashInventory[RT_CashInventory["AgentName"] == agent_name]
        earnings.append(current_agent_dataframe.iloc[-1]["Cash"]-current_agent_dataframe.iloc[0]["Cash"])
    ax.plot(earnings)
    fig.show()
    return fig

