

from .ults import (
    baseRequest,
    convertPublishedDateToUnix,
    fmpApiKey
)

from .models import (
    UnderlyingProfile,
    HistoricalPriceItem,
    FinancialGrowthItem,
    FmpDcf,
    CompanyRevenueProductSegmentation,
    Quotes,
    QuoteItem,
    PrePostMarketQuotes,
    PrePostMarketQuoteItem
)
from .models.fincStatement import (
    CashFlowStatement,
    BalanceSheet,
    IncomeStatement,
    UnderlyingFincStatement,
)



from commonPyLib.sharedModels.news import NewsItem

from typing import Literal


FincStatementPeriodUnion = Literal["annual", "quarter"]


class FMP:
    
    @staticmethod
    def getCompanyProfile(ticker: str) -> UnderlyingProfile:
        url = f"/v3/profile/{ticker}"
        data = baseRequest(url)
        return UnderlyingProfile(**data[0])
    
    @staticmethod
    def getTickerHistoricalPrices(ticker, start, end) -> list[HistoricalPriceItem]:
        url = f"/v3/historical-price-full/{ticker}"
        d = baseRequest(url, {"from": start, "to": end})
        historical: list[dict] = d.get("historical", [])
        items: list[HistoricalPriceItem] = []
        for i in range(len(historical) - 1, -1, -1):
            row = historical[i]
            item = HistoricalPriceItem(
                date=row.get("date"),
                open=row.get("open"),
                high=row.get("high"),
                low=row.get("low"),
                close=row.get("close"),
                changePercent1D=row.get("changePercent"),
                volume=row.get("volume")
            )
            items.append(item)
        return items
    
    @staticmethod
    def getUnderlyingNews(
        ticker, 
        limit: int = None, 
        page: int = None
    ) -> list[NewsItem]:
        url = f"/v3/stock_news"
        obj = {"tickers": ticker}
        if limit != None: obj["limit"] = limit
        if page != None: obj["page"] = page
        d = baseRequest(url, obj)
        return [NewsItem.initFromFMP(item) for item in d]
    
    @staticmethod
    def getIncomeStatement(symbol: str, limit: int = 8, period: FincStatementPeriodUnion = "quarter") -> list[IncomeStatement]:
        url = f"/v3/income-statement/{symbol}"
        data = baseRequest(url, {"period": period, "limit": limit})
        return [IncomeStatement(**item) for item in data]
    
    @staticmethod
    def getBalanceSheet(symbol: str, limit: int = 8, period: FincStatementPeriodUnion = "quarter") -> list[BalanceSheet]:
        url = f"/v3/balance-sheet-statement/{symbol}"
        data = baseRequest(url, {"period": period, "limit": limit})
        return [BalanceSheet(**item) for item in data]

    
    @staticmethod
    def getCashFlowStatement(symbol: str, limit: int = 8, period: FincStatementPeriodUnion = "quarter") -> list[CashFlowStatement]:
        url = f"/v3/cash-flow-statement/{symbol}"
        data = baseRequest(url, {"period": period, "limit": limit})
        return [CashFlowStatement(**item) for item in data]
    
    @staticmethod
    def getFincStatement(symbol: str, limit: int = 8) -> UnderlyingFincStatement:
        cashflows = FMP.getCashFlowStatement(symbol, limit)
        incomeStatements = FMP.getIncomeStatement(symbol, limit)
        balanceSheets = FMP.getBalanceSheet(symbol, limit)
        return UnderlyingFincStatement(
            cashflows=cashflows, 
            incomeStatements=incomeStatements, 
            balanceSheets=balanceSheets
        )
    
    @staticmethod
    def getFincGrowth(symbol: str) -> list[FinancialGrowthItem]:
        try: 
            url = f"/v3/financial-growth/{symbol}"
            data = baseRequest(url)
            return [FinancialGrowthItem(**item) for item in data]
        except Exception as e: 
            print(e)
            return None

    
    @staticmethod
    def getDiscountedCashFlow(symbol: str) -> FmpDcf:
        try:
            url = f"/v3/discounted-cash-flow/{symbol}"
            data = baseRequest(url)
            return FmpDcf(**data[0])
        except Exception as e:
            print(e)
            return None
        
    @staticmethod
    def getCompanyRevenueProductSegmentation(
        symbol: str, 
        period: FincStatementPeriodUnion = "annual"
    ) -> CompanyRevenueProductSegmentation:
        #########
        url = f"/v4/revenue-product-segmentation"
        data: list[dict[str, dict[str, float]]] = baseRequest(url, {
            "symbol": symbol,
            "structure": "flat",
            "period": period
        })
        return CompanyRevenueProductSegmentation(data=data)
    
    @staticmethod
    def getQuotes(symbol: str | list[str]) -> Quotes:
        if type(symbol) is list:
            symbol = ",".join(symbol)
        url = f"/v3/quote/{symbol}"
        data = baseRequest(url)
        if type(data) is dict:
            print(data)
        return Quotes(items=data)
    
    @staticmethod
    def getPrePostMarketQuotes(symbol: str | list[str]) -> PrePostMarketQuotes:
        if type(symbol) is list:
            symbol = ",".join(symbol)
        url = f"/v4/batch-pre-post-market-trade/{symbol}"
        data = baseRequest(url)
        return PrePostMarketQuotes(items=data)


__all__ = ["FMP", "fmpApiKey"]