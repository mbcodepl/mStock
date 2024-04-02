import unittest
from unittest.mock import patch
from io import StringIO
from mstocks.utils import Utils

class TestUtils(unittest.TestCase):
    
    def test_get_currency_known_symbol(self):
        currency_map = {
            ".US": "USD",
            ".UK": "GBP",
            ".EU": "EUR"
        }
        symbol = "AAPL.US"
        currency = Utils.get_currency(symbol, currency_map)
        self.assertEqual(currency, "USD")

    def test_get_currency_unknown_symbol(self):
        currency_map = {
            ".US": "USD",
            ".UK": "GBP",
            ".EU": "EUR"
        }
        symbol = "TSLA"
        currency = Utils.get_currency(symbol, currency_map)
        self.assertEqual(currency, "USD")

    def test_get_currency_new_extension(self):
        currency_map = {
            ".US": "USD",
            ".UK": "GBP",
            ".EU": "EUR",
            ".JP": "JPY"
        }
        symbol = "SONY.JP"
        currency = Utils.get_currency(symbol, currency_map)
        self.assertEqual(currency, "JPY")

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_table_with_fixed_width(self, mock_stdout):
        prices_with_market_status = [
            ["Open", "10:00", "AAPL", "Apple Inc.", "150.00 USD", Utils.OKGREEN + "+1.00 USD (0.67%) ↑" + Utils.ENDC, "100.00 USD", "1.00%", "1.00 USD"],
            ["Closed", "16:00", "MSFT", "Microsoft Corp.", "250.00 USD", Utils.FAIL + "-2.00 USD (0.80%) ↓" + Utils.ENDC, "200.00 USD", "-1.00%", "-2.00 USD"]
        ]

        # Your prices_with_market_status data as defined above.
        Utils.print_table_with_fixed_width(prices_with_market_status) 
        output = Utils.strip_ansi_codes(mock_stdout.getvalue())
        self.assertIn("Market status", output)
        # Check for the presence of an ANSI-escaped string in output
        self.assertIn(Utils.strip_ansi_codes("+1.00 USD (0.67%) ↑"), Utils.strip_ansi_codes(output))
        self.assertIn("100.00 USD", output)  # Check for invested amount
        self.assertIn("1.00%", output)  # Check for earned percentage

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_table_without_market_status(self, mock_stdout):
        prices_without_market_status = [
            ["10:00", "AAPL", "Apple Inc.", "150.00 USD", Utils.OKGREEN + "+1.00 USD (0.67%) ↑" + Utils.ENDC, "100.00 USD", "1.00%", "1.00 USD"],
            ["16:00", "MSFT", "Microsoft Corp.", "250.00 USD", Utils.FAIL + "-2.00 USD (0.80%) ↓" + Utils.ENDC, "200.00 USD", "-1.00%", "-2.00 USD"]
        ]
        # Your prices_without_market_status data as defined above.
        Utils.print_table_with_fixed_width(prices_without_market_status, include_market_status=False)
        output = mock_stdout.getvalue()
        self.assertNotIn("Market status", output)
        # Check for the presence of an ANSI-escaped string in output
        self.assertIn(Utils.strip_ansi_codes("+1.00 USD (0.67%) ↑"), Utils.strip_ansi_codes(output))
        self.assertIn("100.00 USD", output)  # Check for invested amount
        self.assertIn("1.00%", output)  # Check for earned percentage


if __name__ == '__main__':
    unittest.main()
