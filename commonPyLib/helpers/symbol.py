
from commonPyLib.sharedModels.ults import SymbolIdentifierUnion
from commonPyLib.sharedModels.countryCode import BoostedCountryCodeUnion, CountryCodeUnion

def destructBBTicker(bbTicker: str) -> tuple[str, str, str, str, str, float]:
    splitedTicker = bbTicker.split(" ")
    splitedLength = len(splitedTicker)
    symbol = ""
    exCode = ""
    assetClass = ""
    expiryDate = ""
    strike = 0
    callPut = ""
    if "Index" in bbTicker and splitedLength == 2:
        symbol = splitedTicker[0]
        assetClass = "Index"
    if "Equity" in bbTicker:
        if splitedLength == 3:
            symbol = splitedTicker[0]
            exCode = splitedTicker[1]
            assetClass = "Equity"
        if splitedLength == 5:
            callPutStrike = splitedTicker[3]
            callPut = "Call" if callPutStrike[0] == "C" else "Put"
            strike = float(callPutStrike[1:])
            ####
            symbol = splitedTicker[0]
            exCode = splitedTicker[1]
            assetClass = "Option"
            expiryDate = splitedTicker[2]
    return symbol, exCode, assetClass, expiryDate, callPut, strike



class SymbolConvertor:

    @staticmethod
    def ricExCodeToBBExCode(exCode: str = None) -> str:
        bbExCode = "US"
        if exCode == "HK": return "HK"
        if exCode == "TW": bbExCode = "TT"
        if exCode == "SS" or exCode == "SZ": bbExCode = "CH"
        if exCode == "ZK": bbExCode = "C2"
        if exCode == "SH": bbExCode = "C1"
        return bbExCode

    @staticmethod
    def symbolToChinaReutersCode(symbol: str) -> str:
        symbol = symbol.zfill(6)
        excode = "SS"
        excode = "SZ" if symbol[0] == "3" or symbol[0] == "0" else "SS"
        return f"{symbol}.{excode}"
    
    @staticmethod
    def symbolToHKReutersCode(symbol: str) -> str:
        symbol = symbol.zfill(4)
        return f"{symbol}.HK"

    @staticmethod
    def bbTickerToStandardTicker(bbTicker: str) -> str:
        splitedTicker = destructBBTicker(bbTicker)
        sym = splitedTicker[0]
        exCode = splitedTicker[1]
        if exCode == "HK": return SymbolConvertor.symbolToHKReutersCode(sym)
        if exCode == "TT": return f"{sym}.TW"
        if exCode == "CH" or exCode == "C1" or exCode == "C2": 
            return SymbolConvertor.symbolToChinaReutersCode(sym)
        return sym
    
    @staticmethod
    def bbTickerToRic(bbTicker: str) -> str:
        splitedTicker = destructBBTicker(bbTicker)
        sym = splitedTicker[0]
        exCode = splitedTicker[1]
        if exCode == "HK": return SymbolConvertor.symbolToHKReutersCode(sym)
        if exCode == "TT": return f"{sym}.TW"
        if exCode == "CH" or exCode == "C1" or exCode == "C2" or exCode == "CJ": 
            return SymbolConvertor.symbolToChinaReutersCode(sym)
        return f"{sym}.OQ"
    
    @staticmethod
    def bbTickerToBoostedSym(bbTicker: str) -> tuple[str, BoostedCountryCodeUnion]:
        splitedTicker = destructBBTicker(bbTicker)
        sym = splitedTicker[0]
        exCode = splitedTicker[1]
        countryCode: BoostedCountryCodeUnion = "USA"
        if exCode == "HK": countryCode = "HKG"
        if exCode == "TT": countryCode = "TWN"
        if exCode == "CH" or exCode == "C1" or exCode == "C2": countryCode = "CHN"
        return sym, countryCode
    
    @staticmethod
    def standardToBBTicker(ticker: str) -> str:
        sName = ticker.split(".")
        symbol = sName[0]
        exCode = sName[1] if len(sName) > 1 else None
        bbExCode = SymbolConvertor.ricExCodeToBBExCode(exCode)
        if exCode == "HK": 
            symbol = symbol.lstrip('0')
        return f"{symbol} {bbExCode} Equity"
    
    @staticmethod
    def standardToBoostedSymbol(yahooTicker: str) -> tuple[str, BoostedCountryCodeUnion]:
        sName = yahooTicker.split(" ")
        if len(sName) == 1: return sName[0], "USA"
        symbol = sName[0]
        ricExCode = sName[1]
        if ricExCode == "HK": return symbol, "HKG"
        if ricExCode == "TW": return symbol, "TWN"
        if ricExCode in ["SS", "SZ", "ZK", "SH"]: return symbol, "CHN"
        return symbol, "USA"


    @staticmethod
    def convert(symbol: str, inFormat: SymbolIdentifierUnion, outFormat: SymbolIdentifierUnion):
        if inFormat == outFormat: return symbol
        if inFormat == "bbTicker":
            if outFormat == "standardTicker": return SymbolConvertor.bbTickerToStandardTicker(symbol)
            if outFormat == "ric": return SymbolConvertor.bbTickerToRic(symbol)
            if outFormat == "boostedSymbol": SymbolConvertor.bbTickerToBoostedSym(symbol)
        if inFormat == "standardTicker":
           if outFormat == "bbTicker": return SymbolConvertor.standardToBBTicker(symbol)
           if outFormat == "boostedSymbol": return SymbolConvertor.standardToBoostedSymbol(symbol)
        
        raise Exception(f"Unable to convert {symbol} to {outFormat}")

