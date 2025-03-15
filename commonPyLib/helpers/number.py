

import random
import string

class NumberHelper:
    
    @staticmethod
    def convertNumberToReadableUnit(num: float | int) -> str:
        if isinstance(num, (int, float)) == False: return num
        if abs(num) < 1000: return str(num)
        magnitude = 0
        unit_list = ["", "k", "m", "b", "t"]
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        displayCash = "{:.2f}".format(num).rstrip('0').rstrip('.')
        displayUnit = unit_list[magnitude]
        return f"{displayCash}{displayUnit}"
    
    @staticmethod
    def genRandomString(lengthOfString = 5) -> str:
        randomString = ''.join(random.choices(
            string.ascii_uppercase + string.digits + string.ascii_lowercase, 
            k=lengthOfString
        ))
        return randomString

    @staticmethod
    def genRandomFloat(min: float, max: float) -> float:
        return random.uniform(min, max)
