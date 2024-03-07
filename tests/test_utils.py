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

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_table_with_fixed_width(self, mock_stdout):
        prices = [
            ["Open", "10:00", "AAPL", "Apple Inc.", "$150.00", "+1.00 (0.67%) ↑"],
            ["Closed", "16:00", "MSFT", "Microsoft Corp.", "$250.00", "-2.00 (0.80%) ↓"]
        ]
        Utils.print_table_with_fixed_width(prices)
        output = mock_stdout.getvalue()
        self.assertIn("Apple Inc.", output)
        self.assertIn("Microsoft Corp.", output)
        self.assertIn("+1.00 (0.67%) ↑", output)
        self.assertIn("-2.00 (0.80%) ↓", output)

if __name__ == '__main__':
    unittest.main()
