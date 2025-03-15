

from pydantic import BaseModel, Field
from .ults import SymbolIdentifierUnion
from commonPyLib.helpers.symbol import SymbolConvertor

class GetUnderlyingStuffInputBase(BaseModel):
    symbol: str = Field(description="The ticker symbol of the stock.")
    symbolIdentifier: SymbolIdentifierUnion = Field(
        default= "standardTicker", 
        description=(
            "Identifies the type of ticker's symbol. Options include: "
            "1. standardTicker: The raw form of a stock ticker symbol without any additional prefixes, suffixes, e.g. AAPL, TSLA, etc. "
            "2. bbTicker: Bloomberg's unique identifier for a stock, e.g. AAPL US Equity, TSLA US Equity, etc. "
            "3. ric: Reuters Instrument Code, e.g. AAPL.O, TSLA.O, etc. "
            "4. boostedSymbol: The unique identifier for a stock in Boosted Finance's system, e.g. AAPL, TSLA, etc. "
            "5. isin: International Securities Identification Number, e.g. US0378331005, US88160R1014, etc. "
        )
    )

    def getStandardTicker(self) -> str:
        return self.symbol
    
    def getBBTicker(self) -> str:
        return SymbolConvertor.convert(self.symbol, self.symbolIdentifier, "bbTicker")