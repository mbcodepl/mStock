import unittest
from unittest.mock import patch, MagicMock
from mstocks.config import Config
from mstocks.stocks import StocksManager

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

    def test_format_trend_positive(self):
        stocks_manager = StocksManager(Config())
        trend = stocks_manager._format_trend(5, 10, "USD")
        self.assertIn("+5.00 USD (10.00%) ↑", trend)

    def test_format_trend_negative(self):
        config = Config()  # Mock this if needed
        stocks_manager = StocksManager(config)
        trend = stocks_manager._format_trend(-5, -10, "USD")
        self.assertIn("-5.00 USD (10.00%) ↓", trend)

    def test_format_trend_no_change(self):
        config = Config()  # Mock this if needed
        stocks_manager = StocksManager(config)
        trend = stocks_manager._format_trend(0, 0, "USD")
        self.assertIn("0.00 USD (0.00%)", trend)

if __name__ == '__main__':
    unittest.main()
