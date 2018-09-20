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
        SimOrderBook.OrderBook["DateTime"] = pd.to_datetime(SimOrderBook.OrderBook["Nanos"],
                                                            utc=True).dt.tz_convert(
            "America/New_York")  # Make a datetime column and specify that nanos are in utc and convert to localtime ie NY time
        SimOrderBook.OrderBook = SimOrderBook.OrderBook[
            SimOrderBook.OrderBook["DateTime"].dt.weekday < 5]  # Skip Weekends

def Prepare_TradesLogs(TradesLogs):
    for TradeLog in TradesLogs:
        TradeLog["DateTime"] = pd.to_datetime(TradeLog["Nanos"],
                                                            utc=True).dt.tz_convert(
            "America/New_York")  # Make a datetime column and specify that nanos are in utc and convert to localtime ie NY time
        TradeLog = TradeLog[
            TradeLog["DateTime"].dt.weekday < 5]  # Skip Weekends


from multiprocessing import Pool, cpu_count
def GetData(path):
    #if __name__ == "__main__":
    # Class for keeping track of files
    SPYFiles = AnalysisSimulation(instrument="SPY",
                               exchange="NYSE",
                               file_path=path,
                               number_sims=10,
                               offset=0
                               )

    # Generate lists of files for use in analysis
    SPYFiles.SimOBList = SPYFiles.gen_file_list("Matching-OrderBook.csv")
    SPYFiles.AgentLogList = SPYFiles.gen_file_list("Matching-agents.csv")
    # SPYFiles.MMLogList = SPYFiles.gen_file_list("Matching-OpenOrders.csv")

    USDFiles = AnalysisSimulation(instrument="USD",
                               exchange="NYSE",
                               file_path=path,
                               number_sims=10,
                               offset=0
                               )
    USDFiles.InventoryLogList = USDFiles.gen_file_list("Historical-inventory.csv")  # Random trader logs

    TradesFiles = AnalysisSimulation(instrument="SPY",
                                    exchange="NYSE",
                                    file_path=path,
                                    number_sims=10,
                                    offset=0)
    TradesFiles.TradesLogList = TradesFiles.gen_file_list("Matching-MarketOrders.csv")

    with Pool(cpu_count()) as p:
        # Read simulation order book
        SimOrderBooks = p.map(OrderBooks.AmmEngineOrderBook_Wrapper,
                              [{"order_book_file_path": SPYFiles.File_Path + LogName,
                                "order_book_file_type": "Amm engine order book file",
                                "order_book_depth": 10} for LogName in SPYFiles.SimOBList]
                              )
        # Read agent order book
        AgentLogs = p.map(OrderBooks.AgentsLog_Wrapper, [{"log_file_path": SPYFiles.File_Path + AgentLogName,
                                                          "agent_log_file_type": "Amm engine agents log file"} for
                                                         AgentLogName in SPYFiles.AgentLogList]
                          )

        # Read Market Maker order book. commented
        # AgentsOrderBook_ColumnNames =  ["AgentName",
        #                                      "Nanos",
        #                                      "DateTime",
        #                                      "AgentBestBidQty",
        #                                      "AgentBestBid",
        #                                      "AgentBestAsk",
        #                                      "AgentBestAskQty",
        #                                      "scale"]

        # MMLogs = p.map(OrderBooks.AmmEngineAgentOrderBook_Wrapper,
        #                [{"agent_name": "InvMM-%i-0" % (i + SPYFiles.Sim_Numbering_Offset),
        #                  "order_book_file_path": SPYFiles.File_Path + MMLogName,
        #                  "order_book_file_type": "Inventory market maker 2 order book log",
        #                  "order_book_depth": 2,
        #                  "column_names": AgentsOrderBook_ColumnNames} for i, MMLogName in
        #                 enumerate(SPYFiles.MMLogList)]
        #
        #                )

        # Read random trades cash inventory

        InventoryLogList_ColumnNames = ["AgentName",
                                        "Nanos",
                                        "DateTime",
                                        "Cash"]

        # InventoryLogList_ColumnTypes = {"AgentName": str,"Nanos": str, "DateTime": str, "Cash": str}
        RT_CashInventory = p.map(OrderBooks.Read_CSV_Wrapper, [{"filepath_or_buffer": SPYFiles.File_Path + LogName,
                                                                "index_col": False,
                                                                "names": InventoryLogList_ColumnNames,
                                                                "header": 1} for LogName in USDFiles.InventoryLogList]
                                 )
        TradesLogList_ColumnNames = ["Nanos",
                                     "DateTime",
                                     "Agent",
                                     "Action",
                                     "Inst",
                                     "Side",
                                     "OrderQty",
                                     "OrderPrice",
                                     "FilledQty",
                                     "AvgPrice",
                                     "TimeInForce",
                                     "OrderID",
                                     "Method",
                                     "Param"]

        TradesLogs = p.map(OrderBooks.Read_CSV_Wrapper,[{"filepath_or_buffer": TradesFiles.File_Path + LogName,
                                                                "index_col": False,
                                                                "names": TradesLogList_ColumnNames,
                                                                "header": 1} for LogName in TradesFiles.TradesLogList]
                           )
    Prepare_SimOrderBook(SimOrderBooks)
    return SimOrderBooks, AgentLogs, RT_CashInventory, TradesLogs
    if __name__ != "__main__":
        print("Not in __main__")

