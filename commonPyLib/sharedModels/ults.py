

from typing import Union, Literal


SymbolIdentifierUnion = Literal[
    "standardTicker",
    "bbTicker",
    "ric",
    "boostedSymbol",
    "isin",
]

DataSourceUnion = Literal[
    "fmp",
    "boosted",
    "bloomberg server",
    "bloomberg desktop",
]