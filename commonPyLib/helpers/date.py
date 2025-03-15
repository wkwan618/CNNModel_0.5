


from datetime import date, datetime, timedelta, timezone
from typing import Literal
from dateutil.relativedelta import relativedelta

DateFormatUnion = Literal["%Y%m%d", "%Y-%m-%d"]

class DateHelper:

    @staticmethod
    def getCurrentUnixTime() -> int:
        return int(datetime.now().timestamp())
    
    @staticmethod
    def convertToUnix(dateStr: str, inFormat: DateFormatUnion = "%Y-%m-%d", offSetGMT: int = None) -> int:
        dateObj = datetime.strptime(dateStr, inFormat)
        if offSetGMT != None:
            dateObj = dateObj - timedelta(hours=offSetGMT)
        return int(dateObj.timestamp())
    
    @staticmethod
    def convertFromUnix(unixTime: int, outFormat: DateFormatUnion = "%Y-%m-%d", offSetGMT: int = None) -> str:
        dateObj = datetime.fromtimestamp(unixTime)
        if offSetGMT != None:
            dateObj = dateObj + timedelta(hours=offSetGMT)
        return dateObj.strftime(outFormat)
    
    @staticmethod
    def getTodayStr(toFormart: DateFormatUnion = "%Y-%m-%d") -> str:
        tzone = timezone(timedelta(hours=8))
        return datetime.now(tzone).strftime(toFormart)
    
    @staticmethod
    def getTodayYear() -> str:
        return DateHelper.getTodayStr("%Y")

    @staticmethod
    def addDay(
        dateString, 
        offsetDays: int, 
        inFormat: DateFormatUnion = "%Y-%m-%d", 
        outFormat: DateFormatUnion= "%Y-%m-%d",
    ) -> str:
        dateObj = datetime.strptime(dateString, inFormat)
        newDateObj = dateObj + timedelta(days=offsetDays)
        return newDateObj.strftime(outFormat)
    
    @staticmethod
    def addYear(
        dateString, 
        offsetYears: int, 
        inFormat: str = "%Y-%m-%d", 
        outFormat: str = "%Y-%m-%d",
    ) -> str:
        dateObj = datetime.strptime(dateString, inFormat)
        newDateObj = dateObj + relativedelta(years=offsetYears)
        return newDateObj.strftime(outFormat)
    
    @staticmethod
    def getDateFromLookbackPeriod(
        lookbackPeriod: str, 
        fromDate: str, 
        inFormat: DateFormatUnion = "%Y-%m-%d", 
        outFormat: DateFormatUnion =  "%Y-%m-%d"
    ) -> str:
        lookbackPeriod = lookbackPeriod.lower()
        multipliers: dict[str, int] = {'y': 365, 'm': 30, 'w': 7, 'd': 1}
        multiplier = multipliers.get(lookbackPeriod[-1], None)
        if multiplier is None: raise ValueError("Invalid lookback period")
        try: value = int(lookbackPeriod[:-1])
        except ValueError: raise ValueError("Invalid lookback period")
        lookbackDay: int = -value * multiplier
        return DateHelper.addDay(fromDate, lookbackDay, inFormat, outFormat)