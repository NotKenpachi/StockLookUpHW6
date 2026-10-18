# makes the 3 lines of output

from datetime import datetime

from .models import Quote

TIMESTAMP_FORMAT = "%a %b %d %H:%M:%S %Z %Y"  # like Mon Oct 10 17:23:48 PDT 2016


def format_timestamp(when: datetime | None = None) -> str:
    return (when or datetime.now()).astimezone().strftime(TIMESTAMP_FORMAT)


def format_quote(quote: Quote, when: datetime | None = None) -> str:
    lines = [
        format_timestamp(when),
        f"{quote.company_name} ({quote.symbol})",
        f"{quote.price:.2f} {quote.change:+.2f} ({quote.percent_change:+.2f}%)",
    ]
    return "\n".join(lines)
