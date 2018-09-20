import importlib.machinery

#%
import RandomTradersStats as RTStats
from Plot_MidPrice import MakeMidPricePlot
from Plot_MarketDepth import Make_MarketDepthPlot
from Plot_Returns import Make_ReturnsPlot, Make_ReturnsDistributionPlot
from Plot_Autocorrelation import MakeAutocorrelationPlot
from Inv_MarketMaker import Plot_LOHitTime, PlotWaitingTimes
from Plot_Volatility import MakeVolatilityPlot, MakeVolatilityDistributionPlot

loader = importlib.machinery.SourceFileLoader('LoadRandomTradersToymarketData', 'LoadRandomTradersToymarketData.py')
LoadRandomTradersToymarketData = loader.load_module()

figurePrefix = "figures/ToyMarket1_"

default_file_path= "../../../git/amm.engine/amm.engine/amm.testing/bin/Debug/netcoreapp2.0/datalogs/" # sim default output


if __name__ == "__main__":  # Multithreaded functions
    SimOrderBooks, AgentLogs, RT_CashInventory, TradesLogs = LoadRandomTradersToymarketData.GetData("data/")
    AgentNames = LoadRandomTradersToymarketData.GenerateAgentNames(10,100, "RT")


# Make plot of the mid price

    MidPriceFigure = MakeMidPricePlot(SimOrderBooks)
    MidPriceFigure.savefig(figurePrefix+"Midprice.png")

# Make plot of volatility and volatility distribution

    VolatilityFigure = MakeVolatilityPlot(SimOrderBooks)
    VolatilityFigure.savefig(figurePrefix+"Volatility.png")

# Make plot of the agents final PL distribution

    FinalPLFigure = RTStats.Plot_FinalPlDist(AgentLogs, AgentNames)
    FinalPLFigure.savefig(figurePrefix+"FinalPL.png")

# Make plot of market depth

    MarketDepthFigure = Make_MarketDepthPlot(SimOrderBooks)
    MarketDepthFigure.savefig(figurePrefix+"MarketDepth.png")

# Make plot of returns
    ReturnsFigure = Make_ReturnsPlot(SimOrderBooks, ylims= [-.3,0.3])
    ReturnsFigure.savefig(figurePrefix+"Returns.png")
    ReturnsDistFigure = Make_ReturnsDistributionPlot(SimOrderBooks, ylims = [8e-1,4e3])
    ReturnsDistFigure.savefig(figurePrefix+"ReturnsDist.png")

# make 60sec autocorrelation plots
    AbsAutocorrelation60secFigure = MakeAutocorrelationPlot(SimOrderBooks, TimeScale=60., AbsoluteCorrelation=True)
    AbsAutocorrelation60secFigure.savefig(figurePrefix+"Abs60secAutocorr.png")
    Autocorrelation60secFigure = MakeAutocorrelationPlot(SimOrderBooks, TimeScale=60., AbsoluteCorrelation=False)
    Autocorrelation60secFigure.savefig(figurePrefix+"60secAutocorr.png")

# make 1sec autocorrelation plots
    AbsAutocorrelation1secFigure = MakeAutocorrelationPlot(SimOrderBooks, TimeScale=1., AbsoluteCorrelation=True)
    AbsAutocorrelation1secFigure.savefig(figurePrefix+"Abs1secAutocorr.png")
    Autocorrelation1secFigure = MakeAutocorrelationPlot(SimOrderBooks, TimeScale=1., AbsoluteCorrelation=False)
    Autocorrelation1secFigure.savefig(figurePrefix+"1secAutocorr.png")

# make market order intensity plot
    MO_Intensity_Figure = Plot_LOHitTime(TradesLogs, SimOrderBooks, 10.)
    MO_Intensity_Figure.savefig(figurePrefix+"MO_Intensity.png")

    PlotWaitingTimes(SimOrderBooks, 10.)



# Plot Price extremes
    MarketDepthFigure_extremes = Make_MarketDepthPlot([SimOrderBooks[2], SimOrderBooks[9]])
    MarketDepthFigure_extremes.savefig(figurePrefix+"MarketDepth_ex.png")
    MidPriceFigure_extremes = MakeMidPricePlot([SimOrderBooks[2], SimOrderBooks[9]])
    MidPriceFigure_extremes.savefig(figurePrefix+"Midprice_ex.png")
