from pydantic import BaseModel
from commonPyLib.helpers import DateHelper
import datetime

class NewsItem(BaseModel):
    providerNewsID: str | None = None
    title: str | None = None
    content: str | None = None
    publisher: str | None = None
    providerPublishTime: int = None
    newsLink: str | None = None
    newsCoverImage: str | None = None
    sentimentScoreByVendor: float = None
    dataSource: str | None = None
    tags: list[str] = []

    def toText(self,) -> str:
        text = f"Title: {self.title}\n"
        text += f"Published On: {DateHelper.convertFromUnix(self.providerPublishTime)}\n"
        text += f"Content: {self.content}\n"
        return text
    
    def getPublishDateDiffFromToday(self) -> int:
        diff = 0
        if self.providerPublishTime != None:
            publishTimeDateObj = datetime.datetime.fromtimestamp(self.providerPublishTime)
            today = datetime.datetime.now()
            diff = today - publishTimeDateObj
            diff = diff.days
        return diff

    @classmethod
    def initFromFMP(cls, data: dict):
        publishTime = DateHelper.convertToUnix(data["publishedDate"], "%Y-%m-%d %H:%M:%S")
        return cls(
            providerNewsID = data.get("url", None),
            title = data.get("title", None),
            content = data.get("text", None),
            publisher = data.get("site", None),
            providerPublishTime =publishTime,
            newsLink = data.get("url", None),
            newsCoverImage = data.get("image", None),
            dataSource = "fmp"
        )