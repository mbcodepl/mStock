import time
import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
from mstocks.config import Config
from mstocks.run_manager import RunManager

class TestRun(unittest.TestCase):
    @patch('mstocks.run_manager.RunManager._display_loop')
    @patch('mstocks.stocks.Config')
    def test_run_silent(self, mock_config, mock_display_loop):
        mock_config.return_value.get.return_value = []
        stocks_manager = RunManager(mock_config.return_value)
        stocks_manager.run_silent()
        mock_display_loop.assert_called_once_with(sorted([]), sorted([]))
        
    @patch('mstocks.run_manager.RunManager._display_loop')
    @patch('mstocks.stocks.Config')
    def test_run_calls_display_loop(self, mock_config, mock_display_loop):
        mock_config.return_value.get.return_value = []  # Ensure default_stocks and default_cryptos return empty lists
        stocks_manager = RunManager(mock_config.return_value)
        mock_stock_symbols = ['AAPL', 'TSLA']
        mock_crypto_symbols = ['BTC-USD', 'ETH-USD']
        stocks_manager.run(stock_symbols_input=mock_stock_symbols, crypto_symbols_input=mock_crypto_symbols)
        mock_display_loop.assert_called_once_with(sorted(mock_stock_symbols), sorted(mock_crypto_symbols))
    
    @patch('mstocks.run_manager.RunManager._display_loop')
    @patch('mstocks.stocks.Config')
    def test_run_silent(self, mock_config, mock_display_loop):
        mock_config.return_value.get.return_value = []
        stocks_manager = RunManager(mock_config.return_value)
        stocks_manager.run_silent()
        mock_display_loop.assert_called_once_with(sorted([]), sorted([]))
        
    @patch('mstocks.run_manager.RunManager._display_loop')
    @patch('mstocks.stocks.Config')
    def test_run_calls_display_loop(self, mock_config, mock_display_loop):
        mock_config.return_value.get.return_value = []  # Ensure default_stocks and default_cryptos return empty lists
        stocks_manager = RunManager(mock_config.return_value)
        mock_stock_symbols = ['AAPL', 'TSLA']
        mock_crypto_symbols = ['BTC-USD', 'ETH-USD']
        stocks_manager.run(stock_symbols_input=mock_stock_symbols, crypto_symbols_input=mock_crypto_symbols)
        mock_display_loop.assert_called_once_with(sorted(mock_stock_symbols), sorted(mock_crypto_symbols))
                
               
if __name__ == '__main__':
    unittest.main()