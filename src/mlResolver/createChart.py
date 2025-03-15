import pandas as pd
import mplfinance as mpf
import os
import shutil
import matplotlib.pyplot as plt

def createOneChart(
        tradingDates: list[str], 
        closes: list[float], 
        volumes: list[float],
        opens: list[float],
        highs: list[float],
        lows: list[float],
        movingAverages: list[float],
        lookbackDays: int, folderPath: str, fileName: str):
    dfChart = pd.DataFrame({
        "tradingDate": tradingDates,
        "close": closes,
        "volume": volumes,
        "open": opens,
        "high": highs,
        "low": lows,
        "movingAverage": movingAverages
    })
    dfChart["tradingDate"] = pd.to_datetime(dfChart["tradingDate"])
    dfChart = dfChart.set_index("tradingDate")
    mavDict = mpf.make_addplot(movingAverages, color = "w", linestyle="-")
    mc = mpf.make_marketcolors(up = "w", down = "w", inherit = True,)
    s = mpf.make_mpf_style(base_mpf_style = "nightclouds", marketcolors = mc)

    fileName = f"{fileName}.png"
    widthConfig = dict(
        line_width = 1.2,
        volume_width = 0.61,  # Reduced from 0.36 to make volume bars thinner
        volume_linewidth = 0,
        ohlc_linewidth = 6.5,
        ohlc_ticksize = 0.1,  # Reduced from 0.5 to make open/close lines shorter
    )
    fig, axlist = mpf.plot(
        dfChart,
        volume = True,
        style = s,
        axisoff = True,
        update_width_config = widthConfig,
        addplot = mavDict,
        figsize=(1.5,3.2),
        returnfig=True,
    )
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    fig.savefig(
        f"{folderPath}/{fileName}",
        dpi=300, 
        bbox_inches="tight", 
        pad_inches=0, 
    )
    plt.close(fig)


def createCharts(graphData: dict, lookbackDays: int, chartsFolderPath: str, isDebug: bool, removeExistingFiles: bool = True, isReCreate: bool = False):

    # Delete all files and folders in the output directory
    if removeExistingFiles:
        if os.path.exists(chartsFolderPath):
            shutil.rmtree(chartsFolderPath)
        os.makedirs(chartsFolderPath)
    #####
    #####
    if isDebug:
        firstKey = next(iter(graphData))
        graphData = {firstKey: graphData[firstKey]}
    for fileName, rowData in graphData.items():
        if isReCreate == False:
            if os.path.exists(f"{chartsFolderPath}/{fileName}.png"):
                continue
        createOneChart(
            tradingDates = rowData["dataObj"]["tradingDate"][0:lookbackDays],
            closes = rowData["dataObj"]["close"][0:lookbackDays],
            volumes = rowData["dataObj"]["volume"][0:lookbackDays],
            opens = rowData["dataObj"]["open"][0:lookbackDays],
            highs = rowData["dataObj"]["high"][0:lookbackDays],
            lows = rowData["dataObj"]["low"][0:lookbackDays],
            movingAverages = rowData["dataObj"]["movingAverage"][0:lookbackDays],
            lookbackDays = lookbackDays,
            folderPath = chartsFolderPath,
            fileName = fileName
        )
