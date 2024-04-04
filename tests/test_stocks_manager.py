import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
from mstocks.config import Config
from mstocks.stocks import StocksManager
from mstocks.utils import Utils

class TestStocksManager(unittest.TestCase):

    @patch('mstocks.stocks.Config')
    @patch('mstocks.stocks.yf.Ticker')
    def test_get_stock_prices(self, mock_ticker, mock_config):
        # Setup mock config and mock ticker
        mock_config_instance = mock_config.return_value
        mock_config_instance.get.return_value = {"": "USD"}

        mock_stock_instance = mock_ticker.return_value
        mock_stock_instance.history.return_value = MagicMock(
            Close={'2022-03-08': 150, '2022-03-09': 155}
        )
        mock_stock_instance.info.return_value = {'longName': 'Test Company'}

        # Instance of StocksManager with mock
        stocks_manager = StocksManager(mock_config_instance)

        # Call get_stock_prices
        result = stocks_manager.get_stock_prices('AAPL;TSLA')

        # Check if the result contains the correct entries
        self.assertIsInstance(result, list)

    @patch('mstocks.stocks.yf.Ticker')
    def test_empty_symbol_string_for_stocks(self, mock_ticker):
        # Assuming your StocksManager is initialized here
        stocks_manager = StocksManager(Config())
        result = stocks_manager.get_stock_prices('')
        expected_result = [['\x1b[91m●\x1b[0m', any, '[]', 'N/A', 'Not available', '—']]
        self.assertEqual(len(result), len(expected_result))

    @patch('mstocks.stocks.yf.Ticker')
    def test_ticker_returns_empty_dataframe_for_stocks(self, mock_ticker):
        mock_ticker.return_value.history.return_value = MagicMock(empty=True)
        stocks_manager = StocksManager(Config())
        result = stocks_manager.get_stock_prices('AAPL')
        self.assertTrue(any("Not available" in item for item in result))

    @patch('builtins.input', side_effect=['AAPL;TSLA', ''])
    def test_collect_symbols_with_input(self, mock_input):
        stocks_manager = StocksManager(Config())
        symbols = Utils._collect_symbols("Enter stock symbols: ")
        self.assertEqual(symbols, ['AAPL', 'TSLA'])

    @patch('builtins.input', return_value='')
    def test_collect_symbols_no_input(self, mock_input):
        stocks_manager = StocksManager(Config())
        symbols = Utils._collect_symbols("Enter stock symbols: ")
        self.assertEqual(symbols, [])

    def setUp(self):
        # Mock configuration
        self.config = {
            'investments': {
                'AAPL': [
                    {'buy_price': 100, 'quantity': 0.5},
                    {'buy_price': 105, 'quantity': 0.3},
                ],
                'MSFT': [
                    {'buy_price': 200, 'quantity': 1},
                ],
            }
        }
        # Create instance of StocksManager
        self.stocks_manager = StocksManager(self.config)

    def test_calculate_earnings_positive(self):
        symbol = 'AAPL'
        current_price = 150
        # Call the method
        earnings, invested, percentage, buy_price = self.stocks_manager.calculate_earnings(symbol, current_price)
        # Check the results
        self.assertEqual(earnings, ((150 - 100) * 0.5) + ((150 - 105) * 0.3))
        self.assertEqual(invested, (100 * 0.5) + (105 * 0.3))
        self.assertTrue(percentage > 0)  # Earnings should be positive
        self.assertEqual(buy_price, 105)

    def test_calculate_earnings_negative(self):
        symbol = 'MSFT'
        current_price = 190
        # Call the method
        earnings, invested, percentage, buy_price = self.stocks_manager.calculate_earnings(symbol, current_price)
        # Check the results
        self.assertEqual(earnings, (190 - 200) * 1)
        self.assertEqual(invested, 200 * 1)
        self.assertTrue(percentage < 0)  # Earnings should be negative
        self.assertEqual(buy_price, 200)

    def test_calculate_earnings_no_investment(self):
        symbol = 'GOOG'  # Assuming GOOG is not in the investments
        current_price = 1000
        # Call the method
        earnings, invested, percentage, buy_price = self.stocks_manager.calculate_earnings(symbol, current_price)
        # Check the results
        self.assertEqual(earnings, 0)
        self.assertEqual(invested, 0)
        self.assertEqual(percentage, 0)
        self.assertEqual(buy_price, 0)

    def test_calculate_earnings_zero_invested(self):
        symbol = 'GOOG'  # Assuming GOOG is not in the investments
        current_price = 1000
        # Call the method
        earnings, invested, percentage, buy_price = self.stocks_manager.calculate_earnings(symbol, current_price)
        # Check the results
        self.assertEqual(earnings, 0)
        self.assertEqual(invested, 0)
        self.assertEqual(percentage, 0)
        self.assertEqual(buy_price, 0)

if __name__ == '__main__':
    unittest.main()
