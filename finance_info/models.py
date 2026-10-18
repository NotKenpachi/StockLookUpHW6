# holds the stock info

from dataclasses import dataclass


@dataclass(frozen=True)
class Quote:
    symbol: str
    company_name: str
    price: float
    previous_close: float

    @property
    def change(self) -> float:
        return self.price - self.previous_close

    @property
    def percent_change(self) -> float:
        if not self.previous_close:  # dont divide by 0
            return 0.0
        return self.change / self.previous_close * 100
