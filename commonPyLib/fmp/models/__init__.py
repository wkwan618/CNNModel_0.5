

from pydantic import BaseModel, Field
from .quote import Quotes, QuoteItem, PrePostMarketQuotes, PrePostMarketQuoteItem

class UnderlyingProfile(BaseModel):
    companyName: str
    industry: str
    sector: str
    country: str
    description: str
    beta: float = None

    def toText(self) -> str:
        text = f"Company Name: {self.companyName}\n"
        text += f"Industry: {self.industry}\n"
        text += f"Sector: {self.sector}\n"
        text += f"Country: {self.country}\n"
        text += f"Description: {self.description}\n"
        return text

class HistoricalPriceItem(BaseModel):
    date: str = None
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    changePercent1D: float = None
    volume: float = None

    def toText(self) -> str:
        return f"{self.date}: {self.close}"



class FmpDcf(BaseModel):
    date: str
    freeCashFlow: float = Field(alias="dcf")
    currentStockPrice: float = Field(alias="Stock Price")

    def toText(self) -> str:
        return f"{self.date}: DCF: {self.freeCashFlow}, Stock Price: {self.currentStockPrice}"
    


class FinancialGrowthItem(BaseModel):
    symbol: str
    date: str
    calendarYear: str
    period: str
    revenueGrowth: float
    grossProfitGrowth: float
    ebitgrowth: float
    operatingIncomeGrowth: float
    netIncomeGrowth: float
    epsgrowth: float
    epsdilutedGrowth: float
    weightedAverageSharesGrowth: float
    weightedAverageSharesDilutedGrowth: float
    dividendsperShareGrowth: float
    operatingCashFlowGrowth: float
    freeCashFlowGrowth: float
    tenYRevenueGrowthPerShare: float
    fiveYRevenueGrowthPerShare: float
    threeYRevenueGrowthPerShare: float
    tenYOperatingCFGrowthPerShare: float
    fiveYOperatingCFGrowthPerShare: float
    threeYOperatingCFGrowthPerShare: float
    tenYNetIncomeGrowthPerShare: float
    fiveYNetIncomeGrowthPerShare: float
    threeYNetIncomeGrowthPerShare: float
    tenYShareholdersEquityGrowthPerShare: float
    fiveYShareholdersEquityGrowthPerShare: float
    threeYShareholdersEquityGrowthPerShare: float
    tenYDividendperShareGrowthPerShare: float
    fiveYDividendperShareGrowthPerShare: float
    threeYDividendperShareGrowthPerShare: float
    receivablesGrowth: float
    inventoryGrowth: float
    assetGrowth: float
    bookValueperShareGrowth: float
    debtGrowth: float
    rdexpenseGrowth: float
    sgaexpensesGrowth: float


class CompanyRevenueProductSegmentation(BaseModel):
    data: list[dict[str, dict[str, float]]]

    def getPeriods(self) -> list[str]:
        periods = []
        for row in self.data:
            for period in row.keys():
                if period not in periods:
                    periods.append(period)
        return periods
        
    def getProductNames(self) -> list[str]:
        names = []
        for index, row in enumerate(self.data):
            if index >= 2: break
            for period, value in row.items():
                for name in value.keys():
                    if name not in names:
                        names.append(name)
        return names

    def getProdcutPeriodRevenue(self, productName: str, period: str) -> float | None:
        periodResult = None
        for row in self.data:
            for rowPeriod, obj in row.items():
                if rowPeriod == period:
                    periodResult = obj
                    break
        if periodResult == None: return None
        return periodResult.get(productName, None)