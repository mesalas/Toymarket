# Script for reading data from random traders

# Import libs
# Import `AmmEnginePyTools` from custom dir
import importlib.machinery

loader = importlib.machinery.SourceFileLoader('OrderBooks', '../../../AmmEnginePyTools/OrderBooks.py')
OrderBooks = loader.load_module()

import pandas as pd


# Define Classs
class AnalysisSimulation():

    def __init__(self, instrument, exchange, file_path, number_sims=1, offset=0):
        self.Instrument = instrument
        self.Exchange = exchange
        self.Number_Of_Simulations = number_sims
        self.Sim_Numbering_Offset = offset
        self.File_Path = file_path

    def gen_file_list(self, name):
        return [self.Instrument + "_" + self.Exchange + "@%i_" % i + name for i in
                range(self.Sim_Numbering_Offset, self.Number_Of_Simulations)]


def GenerateAgentNames(number_of_markets: int, number_of_agents: int, agent_name_prefix: str) -> list:
    ''' Function for generateing a list of agent names based on an agent name prefix string and the number of sims and
     the number of agents in each sim'''
    AgentNames: list = []  # %Make List of agent names
    for i in range(number_of_markets):
        AgentNames.append([agent_name_prefix + "-%i-%i" % (i, j) for j in range(1, number_of_agents)])
    return AgentNames


def Prepare_SimOrderBook(SimOrderBooks):
    for SimOrderBook in SimOrderBooks:
        SimOrderBook.OrderBook["DateTime"] = pd.to_datetime(SimOrderBook.OrderBook[SimOrderBook.timestamp_col_name],
                                                            utc=True, unit="ms").dt.tz_convert(
            "America/New_York")  # Make a datetime column and specify that nanos are in utc and convert to localtime ie NY time
        SimOrderBook.OrderBook = SimOrderBook.OrderBook[
            SimOrderBook.OrderBook["DateTime"].dt.weekday < 5]  # Skip Weekends
        SimOrderBook.OrderBook.index = SimOrderBook.OrderBook["DateTime"]
        SimOrderBook.OrderBook = SimOrderBook.OrderBook.between_time("9:30", "16:00")


from multiprocessing import Pool, cpu_count
def GetData(path):
    #if __name__ == "__main__":
    # Class for keeping track of files
    SPYFiles = AnalysisSimulation(instrument="SPY",
                               exchange="NYSE",
                               file_path=path,
                               number_sims=1,
                               offset=0
                               )

    # Generate lists of files for use in analysis
    SPYFiles.SimOBList = ["SPY_OTC_BOOK10_20180206.csv.gz"]#SPYFiles.gen_file_list("Matching-OrderBook.csv")

    with Pool(cpu_count()) as p:
        # Read simulation order book
        SimOrderBooks = p.map(OrderBooks.MarketDataOrderBook_Wrapper,
                              [{"order_book_file_path": SPYFiles.File_Path + LogName,
                                "order_book_file_type": "Market data order book file",
                                "order_book_depth": 10} for LogName in SPYFiles.SimOBList]
                              )

    Prepare_SimOrderBook(SimOrderBooks)
    return SimOrderBooks #, AgentLogs, RT_CashInventory, TradesLogs
    if __name__ != "__main__":
        print("Not in __main__")

