from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, Field
from commonPyLib.sharedModels.getUnderlyingStuff import GetUnderlyingStuffInputBase

from commonPyLib.helpers.date import DateHelper
from commonPyLib.helpers.file import AppFolderPath, FileHelper
from commonPyLib.helpers.number import NumberHelper
from src.mlResolver.createChart import createOneChart
from commonPyLib.fmp import FMP

from fastapi import HTTPException
from fastapi.responses import FileResponse

from src.mlResolver.models.cnn5to5 import Model
import torch
from src.mlResolver.chatTransformer import transformOneImage

app = FastAPI(
    title="Chart Prediction",
    #servers=[{"url": "https://www.thequantengine.com/botTools"}],
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

model = Model()
model.load_state_dict(torch.load(f"{AppFolderPath.mlChart.models}/cnn20250218_5_5_mix.pth", weights_only=True))
model.eval()

###

for folderPath in [
    AppFolderPath.mlChart,
    AppFolderPath.mlChart.devProject,
    AppFolderPath.mlChart.models,
    AppFolderPath.mlChart.rawData
]:
    FileHelper.createFolderIfNotExists(folderPath)

class GetPredictionInput(GetUnderlyingStuffInputBase):
    asOfDate: str = Field(
        default=None, 
        description="The date to get the prediction for. It will use the current date if not provided. Format: YYYY-MM-DD"
    )

class Prediction(BaseModel):
    graphDataImgID: str = Field(
        description="The ID of the graph data image. You can use it to get the Input image from the server."
    )
    dayOfPrediction: int = Field(
        description="The day of the prediction. It will be int. e.g. 1 is the day after the asOfDate and 5 is the fifth day after the asOfDate."
    )
    upProbability: float = Field(
        description="The probability of the stock price going up on the day of the prediction."
    )
    downProbability: float = Field(
        description="The probability of the stock price going down on the day of the prediction."
    )
    inputDateFrom: str = Field(
        description="The start date of the input data."
    )
    inputDateTo: str = Field(
        description="The end date of the input data."
    )
    prediction: str = Field(
        description="The prediction of the stock price. It will be 'Up' or 'Down'."
    )



@app.get("/getPredictionImg/{imgID}", response_class=FileResponse, description="Get the input data chart for prediction, by providing the imgID at the end of the url")
def getPredictionImg(imgID: str):
    try:
        return FileResponse(f"{AppFolderPath.mlChart.prodImgs}/{imgID}", media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=404, detail="No Image Found")


@app.post("/getPrediction", description="Get the prediction for the next N days")
def getFiveDaysPrediction(req: Request, reqBody: GetPredictionInput) -> Prediction:

    ticker = reqBody.getStandardTicker()
    end = DateHelper.getTodayStr() if reqBody.asOfDate is None else reqBody.asOfDate

    start = DateHelper.getDateFromLookbackPeriod("30d", end,)
    prices = FMP.getTickerHistoricalPrices(ticker, start, end)
    if len(prices) > 30:
        prices = prices[-30:]
    ####
    movingAverages = []
    for index, item in enumerate(prices):
        if index < 4: 
            movingAverages.append(None)
            continue
        # Calculate moving average from the slice
        priceWindow = prices[index-4:index+1]
        closePrices = [p.close for p in priceWindow]
        movingAverage = sum(closePrices) / len(closePrices)
        movingAverages.append(movingAverage)
    ####
    prices = prices[-5:]
    inputDateFrom = prices[0].date
    inputDateTo = prices[-1].date
    tradingDates = [p.date for p in prices]
    closes = [p.close for p in prices]
    volumes = [p.volume for p in prices]
    opens = [p.open for p in prices]
    highs = [p.high for p in prices]
    lows = [p.low for p in prices]
    movingAverages = movingAverages[-5:]
    startDate = prices[0].date

    fileName = f"{startDate}_{end}_{ticker}_{NumberHelper.genRandomString(5)}_{NumberHelper.genRandomString(6)}"
    lookbackDays = 5
    createOneChart(
        tradingDates = tradingDates,
        closes = closes,
        volumes = volumes,
        opens = opens,
        highs = highs,
        lows = lows,
        movingAverages = movingAverages,
        lookbackDays = lookbackDays,
        folderPath = AppFolderPath.mlChart.prodImgs,
        fileName = fileName
    )

    vectorImage = transformOneImage(lookbackDays, fileName, AppFolderPath.mlChart.prodImgs)
    vectorImage = vectorImage.unsqueeze(1)
    upProbability = 1
    downProbability = 0
    with torch.no_grad():
        output = model(vectorImage)
        prob = torch.softmax(output, dim=1)
        probList = prob.squeeze(0).tolist()
        upProbability = round(probList[0], 4)
        downProbability = round(probList[1], 4)

    return Prediction(
        graphDataImgID = f"{fileName}.png",
        dayOfPrediction = 5,
        inputDateFrom = inputDateFrom,
        inputDateTo = inputDateTo,
        upProbability = upProbability,
        downProbability = downProbability,
        prediction = "Up" if upProbability >= downProbability else "Down"
    )



if __name__=="__main__":
    print("Starting the Quant Engine Bot Tools")
    uvicorn.run(
        "main:app" ,
        host='0.0.0.0', 
        port=5000, 
        reload = False,
    )

