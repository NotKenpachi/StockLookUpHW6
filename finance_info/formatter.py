"""Turns a Quote into the three-line output the assignment requires."""

from datetime import datetime

from .models import Quote

TIMESTAMP_FORMAT = "%a %b %d %H:%M:%S %Z %Y"  # Mon Oct 10 17:23:48 PDT 2016


def _short_tz(name: str) -> str:
    """Windows reports 'Pacific Daylight Time'; shorten it to 'PDT'."""
    return "".join(word[0] for word in name.split()) if " " in name else name


def format_timestamp(when: datetime | None = None) -> str:
    now = (when or datetime.now()).astimezone()
    tz = _short_tz(now.tzname() or "")
    return now.strftime(TIMESTAMP_FORMAT.replace("%Z", tz))


def format_quote(quote: Quote, when: datetime | None = None) -> str:
    lines = [
        format_timestamp(when),
        f"{quote.company_name} ({quote.symbol})",
        f"{quote.price:.2f} {quote.change:+.2f} ({quote.percent_change:+.2f}%)",
    ]
    return "\n".join(lines)