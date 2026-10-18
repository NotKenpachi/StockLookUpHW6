# Python Finance Info

Enter a stock symbol, get the current time, company name, price, and change.

```
Please enter a symbol:
ADBE
Mon Oct 10 17:23:48 PDT 2016
Adobe Systems Incorporated (ADBE)
109.24 +0.60 (+0.55%)
```

## Run
```
pip install -r requirements.txt
python main.py
```
Tests (no network needed): `python -m unittest discover -s tests`

## Layout
| File | Responsibility |
|---|---|
| `main.py` | Entry point; wires the Yahoo provider into the CLI |
| `finance_info/cli.py` | Prompt loop; turns every error into a message |
| `finance_info/validator.py` | Cleans and validates ticker input |
| `finance_info/providers.py` | `QuoteProvider` interface + Yahoo Finance implementation |
| `finance_info/connectivity.py` | Fast network reachability check |
| `finance_info/models.py` | `Quote` dataclass; computes change and % change |
| `finance_info/formatter.py` | Builds the 3-line output |
| `finance_info/errors.py` | User-facing exception types |
| `tests/` | Unit tests using a fake provider |

## Error handling
No network, unreachable server, invalid symbol format, unknown symbol,
rate limiting, missing data fields, and Ctrl+C / Ctrl+D all produce a message
instead of a crash.
