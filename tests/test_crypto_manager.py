import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
from mstocks.config import Config
from mstocks.crypto import CryptoManager

class TestCryptoManager(unittest.TestCase):
    @patch('mstocks.stocks.yf.Ticker')
    def test_empty_symbol_string_for_crypto(self, mock_ticker):
        # Assuming your StocksManager is initialized here
        stocks_manager = CryptoManager(Config())
        result = stocks_manager.get_crypto_prices('')
        expected_result = [['\x1b[91m●\x1b[0m', any, '[]', 'Crypto', 'Not available', '—']]
        self.assertEqual(len(result), len(expected_result))

    @patch('mstocks.stocks.Config')
    def test_initialization_and_config_checks(self, mock_config):
        mock_config_instance = mock_config.return_value
        mock_config_instance.get.side_effect = lambda key, default: {"crypto": "True", "currency_map": {"BTC": "USD"}}[key] if key in ["crypto", "currency_map"] else default
        stocks_manager = CryptoManager(mock_config_instance)

        self.assertTrue(stocks_manager.crypto_enabled)
        self.assertEqual(stocks_manager.currency_map, {"BTC": "USD"})

    @patch('mstocks.stocks.yf.Ticker')
    def test_get_crypto_prices(self, mock_ticker):
        # Setup a mock DataFrame response
        data = {
            'Close': [50000, 51000],
        }
        mock_hist = pd.DataFrame(data)

        # Mock the history method to return our mock DataFrame
        mock_ticker.return_value.history.return_value = mock_hist

        # Assuming your StocksManager initialization is properly set up
        config = {"currency_map": {"BTC-USD": "USD"}, 'default_stocks': [], 'refresh_rate': 60}
        manager = CryptoManager(config)

        result = manager.get_crypto_prices("BTC-USD")
        # Adjust your assertions as necessary. The following is a placeholder.
        # For example, check if "BTC-USD" or "51000.00 USD" appears in any of the strings in the result list.
        self.assertTrue(any("BTC-USD" in item for item in result[0]), "BTC-USD should be in the results")