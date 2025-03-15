

from pydantic import Field
from .getUnderlyingStuff import GetUnderlyingStuffInputBase
from commonPyLib.helpers import DateHelper

class GetUnderlyingHistoricalPriceInput(GetUnderlyingStuffInputBase):
    dateFrom: str | None = Field(
        default=None,
        description=(
            "The start date of the historical data. Input Format: %Y-%m-%d. "
            "If not specified, it will calculate base on the 'lookbackPeriod' field with dataTo value. "
        )
    )
    dateTo: str | None = Field(
        default=None,
        description=(
            "The end date of the historical data. Input Format: %Y-%m-%d. "
            "If not specified, today date will be used as default value."
        )
    )
    lookbackPeriod: str | None = Field(
        default=None,
        description=(
            "If specified, value of dateFrom will be ignored. "
            "Use a number followed by a letter: Y for year, M for month, W for week, and D for day. "
            "For example, 1Y sets dateFrom to one year ago from dateTo; 2d sets it to two days ago"
        )
    )

    def __init__(self, **obj) -> None:
        dateTo = obj.get("dateTo", None)
        dateFrom = obj.get("dateFrom", None)
        lookbackPeriod = obj.get("lookbackPeriod", None)
        ####
        if dateTo == None: dateTo = DateHelper.getTodayStr()
        if dateFrom == None:
            if lookbackPeriod == None: raise ValueError("dateFrom or lookbackPeriod must be specified.")
            else:
                dateFrom = DateHelper.getDateFromLookbackPeriod(lookbackPeriod, dateTo, "%Y-%m-%d", "%Y-%m-%d")
        obj["dateFrom"] = dateFrom
        obj["dateTo"] = dateTo
        obj["lookbackPeriod"] = lookbackPeriod    
        super().__init__(**obj)

    def getDateFromDateTo(self) -> tuple[str, str]:
        return self.dateFrom, self.dateTo
