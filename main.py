import sys

from finance_info.cli import run
from finance_info.providers import YahooFinanceProvider


def main() -> int:
    try:
        provider = YahooFinanceProvider()
    except ImportError:
        print("Missing dependency 'yfinance'. Run: pip install -r requirements.txt",
              file=sys.stderr)
        return 1
    return run(provider)


if __name__ == "__main__":
    sys.exit(main())
