


import pandas as pd

def processDataToGraphData(ticker: str, dataPath: str, lookbackDays: int, futureDays: int, isDebug: bool = False) -> dict:
    
    df = pd.read_csv(dataPath)
    df['movingAverage'] = df['close'].rolling(window = lookbackDays).mean()
    dataFrameLength = len(df)
    stopAt = dataFrameLength - (1 + futureDays)
    graphData = {}

    for i in range(lookbackDays * 2, dataFrameLength):
        if i > stopAt: break
        ###

        stackStartingIndex = i - lookbackDays
        stackEndingIndex = i + futureDays
        stack = df[stackStartingIndex:stackEndingIndex]
        stack.reset_index(drop = True, inplace = True)


        initialDate = stack.loc[0, 'tradingDate']
        asOfDate = stack.loc[lookbackDays - 1, 'tradingDate']
        asOfDateClose = stack.loc[lookbackDays - 1, 'close']
        predictionRowIndex = i + futureDays - 1
        predictionDate = df.loc[predictionRowIndex, 'tradingDate']
        predictionClose = df.loc[predictionRowIndex, 'close']
        change = (predictionClose - asOfDateClose) / asOfDateClose
        ### convert to dictionary
        dataObj = stack.to_dict(orient='list')
        fileName = f"{ticker}_{initialDate}_{asOfDate}_{predictionDate}"
        graphData[fileName] = {
            'initialDate': initialDate,
            'asOfDate': asOfDate,
            'predictionDate': predictionDate,
            'asOfDateClose': asOfDateClose,
            'predictionClose': predictionClose,
            'change': change,
            'dataObj': dataObj,
        }

        if isDebug:
            print(stack)
            print("")
            print(graphData[fileName])
            break

    return graphData