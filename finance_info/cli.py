# main loop that asks the user for symbols

from .errors import ConnectionProblem, QuoteError
from .formatter import format_quote
from .providers import QuoteProvider
from .validator import normalize_symbol

QUIT_WORDS = {"", "q", "quit", "exit"}


# gets the quote and returns what to print
def lookup(provider: QuoteProvider, raw: str) -> str:
    try:
        symbol = normalize_symbol(raw)
        return format_quote(provider.get_quote(symbol))
    except ConnectionProblem as exc:
        return f"Network error: {exc}"
    except QuoteError as exc:
        return f"Error: {exc}"
    except Exception as exc:  # catch anything else so it doesnt crash
        return f"Unexpected error ({type(exc).__name__}): {exc}"


# keeps asking until the user quits
def run(provider: QuoteProvider, read=input, write=print) -> int:
    write("Stock lookup - press Enter or type 'q' to quit.")
    while True:
        try:
            raw = read("Please enter a symbol:\n")
        except (EOFError, KeyboardInterrupt):  # ctrl+c or ctrl+d
            write("\nGoodbye.")
            return 0
        if raw.strip().lower() in QUIT_WORDS:
            write("Goodbye.")
            return 0
        try:
            write(lookup(provider, raw))
        except KeyboardInterrupt:
            write("\nLookup cancelled.")
        write("")
