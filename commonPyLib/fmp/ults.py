
import requests
from urllib.parse import urljoin, urlencode
from commonPyLib.helpers import DateHelper

fmpBaseUrl = "https://financialmodelingprep.com/api"
fmpApiKey = "aCr5aAz9OQAiMwYkGK3mK7ZJdR5AyZgY"


def baseRequest(url, params: dict = {}):
    params = {**params, "apikey": fmpApiKey}
    fullUrl = urljoin(f"{fmpBaseUrl}{url}", "?" + urlencode(params))
    res = requests.get(fullUrl)
    return res.json()

def convertPublishedDateToUnix(inputDate: str = None, informat: str = "%Y-%m-%d %H:%M:%S") -> int:
    if inputDate == None: return None
    return DateHelper.convertToUnix(inputDate, informat) 