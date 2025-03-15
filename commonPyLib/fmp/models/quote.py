

from pydantic import BaseModel
from commonPyLib.fmp.models.ults import ExchangeCodeUnion
from commonPyLib.helpers import SymbolConvertor

class QuoteItem(BaseModel):
    symbol: str
    ###
    bbTicker: str
    ric: str
    ###
    name: str
    price: float
    changesPercentage: float
    change: float
    dayLow: float
    dayHigh: float
    yearHigh: float
    yearLow: float
    marketCap: float
    priceAvg50: float
    priceAvg200: float
    exchange: ExchangeCodeUnion
    volume: int
    avgVolume: int
    open: float
    previousClose: float
    eps: float
    pe: float
    earningsAnnouncement: str
    sharesOutstanding: int
    timestamp: int

    def __init__(self, **kwargs):
        exchange: ExchangeCodeUnion = kwargs.get("exchange", "others")
        symbol: str = kwargs["symbol"]
        kwargs["bbTicker"] = SymbolConvertor.standardToBBTicker(symbol)
        kwargs["ric"] = symbol
        if exchange == "NYSE":
            kwargs["ric"] = SymbolConvertor.bbTickerToRic(f"{symbol}.N")
        if exchange == "NASDAQ":
            kwargs["ric"] = SymbolConvertor.bbTickerToRic(f"{symbol}.OQ")
        super().__init__(**kwargs)


class Quotes(BaseModel):
    items: list[QuoteItem] = []

    def findByBBTicker(self, bbTicker: str) -> QuoteItem | None:
        for quote in self.items:
            if quote.bbTicker == bbTicker: return quote
        return None
    
    def findByRic(self, ric: str) -> QuoteItem | None:
        for quote in self.items:
            if quote.ric == ric: return quote
        return None



class PrePostMarketQuoteItem(BaseModel):
    symbol: str
    bbTicker: str
    price: float
    size: int
    timestamp: int

    def __init__(self, **kwargs):
        kwargs["bbTicker"] = SymbolConvertor.standardToBBTicker(kwargs["symbol"])
        super().__init__(**kwargs)


class PrePostMarketQuotes(BaseModel):
    items: list[PrePostMarketQuoteItem] = []

    def findByBBTicker(self, bbTicker: str) -> PrePostMarketQuoteItem | None:
        for item in self.items:
            if item.bbTicker == bbTicker: return item
        return None
