"""Quote data sources.

QuoteProvider is an interface so another API (Alpha Vantage, Finnhub, ...)
can be added later without touching the CLI.
"""

from abc import ABC, abstractmethod

from .connectivity import ensure_reachable
from .errors import ConnectionProblem, RateLimitedError, SymbolNotFoundError
from .models import Quote


class QuoteProvider(ABC):
    @abstractmethod
    def get_quote(self, symbol: str) -> Quote:
        """Return a Quote for the symbol or raise a QuoteError."""


class YahooFinanceProvider(QuoteProvider):
    HOST = "query1.finance.yahoo.com"

    def __init__(self):
        import logging
        import yfinance  # imported here so tests can run without it
        # yfinance logs its own "HTTP Error 404 / possibly delisted" lines;
        # hide them so the user only sees this program's error message.
        logging.getLogger("yfinance").setLevel(logging.CRITICAL)
        self._yf = yfinance

    def get_quote(self, symbol: str) -> Quote:
        ensure_reachable(self.HOST)
        ticker = self._yf.Ticker(symbol)

        info = self._load_info(ticker, symbol)
        price = info.get("regularMarketPrice") or info.get("currentPrice")
        prev = info.get("regularMarketPreviousClose") or info.get("previousClose")

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
            return {}  # fall back to price history

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