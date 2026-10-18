# checks the symbol the user typed

import re

from .errors import InvalidSymbolError

# letters, numbers and - . ^ = (for stuff like BRK-B or ^GSPC)
_TICKER_RE = re.compile(r"^[A-Z0-9.\-^=]{1,15}$")


def normalize_symbol(raw: str) -> str:
    symbol = raw.strip().upper()
    if not symbol:
        raise InvalidSymbolError("Please enter a stock symbol (e.g. ADBE).")
    if not _TICKER_RE.fullmatch(symbol):
        raise InvalidSymbolError(
            f"'{raw.strip()}' is not a valid symbol. Examples: AAPL, BRK-B, ^GSPC."
        )
    return symbol
