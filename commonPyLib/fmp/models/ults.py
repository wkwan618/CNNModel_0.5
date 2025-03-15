


from typing import Literal

ExchangeCodeUnion = Literal[
    "NASDAQ", 
    "NYSE", 
    "SHZ", # Start with 3 or 0 & SZ
    "SHH", # Start with 6 & SS
    "others",
    "HKSE",
]
