# gets the stock data
# made a base class so i can add other apis later

from abc import ABC, abstractmethod

from .connectivity import ensure_reachable
from .errors import ConnectionProblem, RateLimitedError, SymbolNotFoundError
from .models import Quote


class QuoteProvider(ABC):
    @abstractmethod
    def get_quote(self, symbol: str) -> Quote:
        pass  # should return a Quote


# uses yfinance to get data from yahoo
class YahooFinanceProvider(QuoteProvider):
    HOST = "query1.finance.yahoo.com"

    def __init__(self):
        import yfinance  # import here so tests work without yfinance
        self._yf = yfinance

    def get_quote(self, symbol: str) -> Quote:
        ensure_reachable(self.HOST)
        ticker = self._yf.Ticker(symbol)

        info = self._load_info(ticker, symbol)
        price = info.get("regularMarketPrice") or info.get("currentPrice")
        prev = info.get("regularMarketPreviousClose") or info.get("previousClose")

        # if info is missing the price, use history instead
        if price is None or prev is None:
            price, prev = self._from_history(ticker, symbol)

        name = info.get("longName") or info.get("shortName") or symbol
        return Quote(symbol, name, float(price), float(prev))

    @staticmethod
    def _load_info(ticker, symbol: str) -> dict:
        try:
            return ticker.info or {}
        except Exception as exc:
            text = str(exc).lower()
            if "too many requests" in text or "rate limit" in text:
                raise RateLimitedError(
                    "Yahoo Finance is rate-limiting requests. Try again in a minute."
                ) from None
            if "404" in text or "not found" in text:
                raise SymbolNotFoundError(f"No stock found for '{symbol}'.") from None
            return {}  # try history instead

    @staticmethod
    def _from_history(ticker, symbol: str) -> tuple[float, float]:
        try:
            hist = ticker.history(period="5d")
        except Exception as exc:
            raise ConnectionProblem(f"Download failed for '{symbol}': {exc}") from None
        if hist is None or hist.empty:
            raise SymbolNotFoundError(f"No stock found for '{symbol}'.")
        closes = hist["Close"].dropna()
        if closes.empty:
            raise SymbolNotFoundError(f"No price data for '{symbol}'.")
        last = float(closes.iloc[-1])
        prev = float(closes.iloc[-2]) if len(closes) > 1 else last
        return last, prev
