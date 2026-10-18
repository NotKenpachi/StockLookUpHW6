# custom errors so we can show nice messages


# base error, all the others use this
class QuoteError(Exception):
    pass


# bad input
class InvalidSymbolError(QuoteError):
    pass


# symbol doesnt exist
class SymbolNotFoundError(QuoteError):
    pass


# no internet or cant reach server
class ConnectionProblem(QuoteError):
    pass


# too many requests
class RateLimitedError(QuoteError):
    pass
