# RunManager.py
import time
from datetime import datetime
from mstocks.stocks import StocksManager
from mstocks.crypto import CryptoManager
from mstocks.utils import Utils

class RunManager:
    def __init__(self, config):
        self.config = config
        crypto_str = self.config.get('crypto', 'False')  # Default to 'False' if not found
        self.crypto_enabled = True if crypto_str == "True" else False
        self.stocks_manager = StocksManager(config)
        self.crypto_manager = CryptoManager(config) 

    def run(self, stock_symbols_input=None, crypto_symbols_input=None):
        default_stocks = self.config.get('default_stocks', [])
        stock_symbols = stock_symbols_input or Utils._collect_symbols("Enter stock symbols separated by semicolon (;), or press Enter to use default stocks: ")
        combined_stock_symbols = list(set(default_stocks + stock_symbols))
        sorted_stock_symbols = sorted(combined_stock_symbols)

        default_cryptos = self.config.get('default_cryptos', [])
        crypto_symbols = crypto_symbols_input if crypto_symbols_input else Utils._collect_symbols("Enter cryptocurrency symbols separated by semicolon (;), or press Enter to use default cryptocurrencies: ") if self.crypto_enabled else []
        combined_crypto_symbols = list(set(default_cryptos + crypto_symbols))
        sorted_crypto_symbols = sorted(combined_crypto_symbols)

        self._display_loop(sorted_stock_symbols, sorted_crypto_symbols)
    
    def run_silent(self):
        default_stocks = self.config.get('default_stocks', [])
        sorted_stock_symbols = sorted(default_stocks)

        default_cryptos = self.config.get('default_cryptos', [])
        sorted_crypto_symbols = sorted(default_cryptos)

        self._display_loop(sorted_stock_symbols, sorted_crypto_symbols)

    def _display_loop(self, sorted_stock_symbols, sorted_crypto_symbols):
        while True:
            print("Refreshing...")
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("\033[H\033[J", end="")  # Clear screen
            if sorted_stock_symbols:
                self.stocks_manager._d(sorted_stock_symbols, now)
            
            if self.crypto_enabled and sorted_crypto_symbols:
                self.crypto_manager._display_crypto_prices(sorted_crypto_symbols, now)

            time.sleep(self.config.get('refresh_rate', 60))  # Refresh rate

    def _collect_stock_symbols(self):
        # Collects stock symbols from the user or uses default ones from config
        stock_input = input("Enter stock symbols separated by semicolon (;), or press Enter to use default stocks: ")
        stock_symbols = stock_input.split(';') if stock_input.strip() else self.config.get('default_stocks', [])
        return stock_symbols

    def _collect_crypto_symbols(self):
        # Collects crypto symbols from the user or uses default ones from config
        if self.crypto_manager:
            crypto_input = input("Enter cryptocurrency symbols separated by semicolon (;), or press Enter to use default cryptocurrencies: ")
            crypto_symbols = crypto_input.split(';') if crypto_input.strip() else self.config.get('default_cryptos', [])
            return crypto_symbols
        return []
