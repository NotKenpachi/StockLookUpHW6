# tests, run with: python -m unittest discover tests

import unittest
from datetime import datetime, timezone

from finance_info.cli import lookup, run
from finance_info.errors import (ConnectionProblem, InvalidSymbolError,
                                 SymbolNotFoundError)
from finance_info.formatter import format_quote
from finance_info.models import Quote
from finance_info.providers import QuoteProvider
from finance_info.validator import normalize_symbol


# fake provider so tests dont need internet
class FakeProvider(QuoteProvider):
    def __init__(self, result):
        self.result = result

    def get_quote(self, symbol):
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


ADBE = Quote("ADBE", "Adobe Inc.", 109.24, 108.64)


class ValidatorTests(unittest.TestCase):
    def test_normalizes_case_and_spaces(self):
        self.assertEqual(normalize_symbol("  adbe "), "ADBE")

    def test_accepts_special_tickers(self):
        for s in ("BRK-B", "^GSPC", "RY.TO", "EURUSD=X"):
            self.assertEqual(normalize_symbol(s), s)

    def test_rejects_bad_input(self):
        for s in ("", "   ", "$$bad!", "A" * 16):
            with self.assertRaises(InvalidSymbolError):
                normalize_symbol(s)


class QuoteTests(unittest.TestCase):
    def test_change_and_percent(self):
        self.assertAlmostEqual(ADBE.change, 0.60, places=2)
        self.assertAlmostEqual(ADBE.percent_change, 0.55, places=2)

    def test_zero_previous_close(self):
        self.assertEqual(Quote("X", "X", 5.0, 0.0).percent_change, 0.0)


class FormatterTests(unittest.TestCase):
    def test_matches_assignment_format(self):
        when = datetime(2016, 10, 10, 17, 23, 48, tzinfo=timezone.utc)
        lines = format_quote(ADBE, when).splitlines()
        self.assertTrue(lines[0].startswith("Mon Oct 10"))
        self.assertEqual(lines[1], "Adobe Inc. (ADBE)")
        self.assertEqual(lines[2], "109.24 +0.60 (+0.55%)")

    def test_negative_change_sign(self):
        q = Quote("TSLA", "Tesla, Inc.", 220.10, 223.50)
        self.assertEqual(format_quote(q).splitlines()[2], "220.10 -3.40 (-1.52%)")


class CliTests(unittest.TestCase):
    def test_success(self):
        self.assertIn("Adobe Inc. (ADBE)", lookup(FakeProvider(ADBE), "adbe"))

    def test_network_error(self):
        out = lookup(FakeProvider(ConnectionProblem("offline")), "ADBE")
        self.assertTrue(out.startswith("Network error"))

    def test_unknown_symbol(self):
        out = lookup(FakeProvider(SymbolNotFoundError("nope")), "ZZZZ")
        self.assertTrue(out.startswith("Error"))

    def test_unexpected_exception_does_not_crash(self):
        out = lookup(FakeProvider(RuntimeError("boom")), "ADBE")
        self.assertIn("Unexpected error", out)

    def test_loop_quits_and_handles_eof(self):
        inputs = iter(["adbe", "q"])
        out = []
        self.assertEqual(run(FakeProvider(ADBE), lambda _: next(inputs), out.append), 0)
        self.assertIn("Goodbye.", out)

        def eof(_):
            raise EOFError
        self.assertEqual(run(FakeProvider(ADBE), eof, lambda *_: None), 0)


if __name__ == "__main__":
    unittest.main()
