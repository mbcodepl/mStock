import yfinance as yf
import time
from datetime import datetime
from .market import Market
from .config import Config
from .utils import Utils

class StocksManager:
    def __init__(self, config):
        self.config = config
        self.utils = Utils()
        self.market = Market(self.utils)
        self.currency_map = config.get('currency_map', {"": "USD"})
        crypto_str = self.config.get('crypto', 'False')  # Default to 'False' if not found
        self.crypto_enabled = True if crypto_str == "True" else False

    def get_stock_prices(self, symbols):
        prices = []
        for symbol in symbols.split(';'):
            symbol = symbol.strip()
            stock = yf.Ticker(symbol)
            hist = stock.history(period="2d")  # Fetches the last 2 days data
            currency = self.utils.get_currency(symbol, self.currency_map)

            try:
                # Fetch the company name
                company_name = stock.info.get('longName', 'N/A')

                if len(hist) > 1:
                    last_close = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    price_change = last_close - prev_close
                    percent_change = (price_change / prev_close) * 100

                    # Determine the price direction
                    trend = self._format_trend(price_change, percent_change, currency)
                else:
                    last_close = hist['Close'].iloc[-1] if len(hist) == 1 else "Not available"
                    trend = "—"

                market_status_symbol, last_refreshed_in_tz = self.market.is_market_open(symbol)
                formatted_price = f"{last_close:.2f}  {currency}" if isinstance(last_close, float) else last_close
                prices.append([market_status_symbol, last_refreshed_in_tz, f"[{symbol}]", f"{company_name}", formatted_price, trend])
            except IndexError:
                current_time = datetime.now().strftime('%H:%M:%S')
                prices.append(["Error", f"[{symbol}]", "N/A", "Not found", current_time, "—"])

        return prices
    
    def get_crypto_prices(self, symbols):
        prices = []
        for symbol in symbols.split(';'):
            symbol = symbol.strip()
            crypto = yf.Ticker(symbol)
            hist = crypto.history(period="2d")  # Fetches the last 2 days data

            try:
                if len(hist) > 1:
                    last_close = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    price_change = last_close - prev_close
                    percent_change = (price_change / prev_close) * 100

                    # Determine the price direction
                    trend = self._format_trend(price_change, percent_change, "USD")
                else:
                    last_close = hist['Close'].iloc[-1] if len(hist) == 1 else "Not available"
                    trend = "—"

                market_status_symbol, last_refreshed_in_tz = self.market.is_market_open(symbol)
                formatted_price = f"{last_close:.2f} USD" if isinstance(last_close, float) else last_close
                prices.append([market_status_symbol, last_refreshed_in_tz, f"[{symbol}]", "Crypto", formatted_price, trend])
            except IndexError:
                current_time = datetime.now().strftime('%H:%M:%S')
                prices.append(["Error", f"[{symbol}]", "N/A", "Not found", current_time, "—"])

        return prices


    def _format_trend(self, price_change, percent_change, currency):
        if price_change > 0:
            return f"{self.utils.GREEN}+{price_change:.2f} {currency} ({percent_change:.2f}%) ↑{self.utils.RESET}"
        elif price_change < 0:
            return f"{self.utils.RED}{price_change:.2f} {currency} ({abs(percent_change):.2f}%) ↓{self.utils.RESET}"
        else:
            return f"{price_change:.2f} {currency} ({percent_change:.2f}%)"
        
    def collect_symbols(self, text):
        inpt = input(text)
        return inpt.split(';') if inpt.strip() else []
    
    def display_prices(self, stock_symbols_input=None, crypto_symbols_input=None):
        default_stocks = self.config.get('default_stocks', [])
        stock_symbols = stock_symbols_input if stock_symbols_input is not None else self.collect_symbols("Enter stock symbols separated by semicolon (;), or press Enter to use default stocks: ")
        combined_stock_symbols = list(set(default_stocks + stock_symbols))
        sorted_stock_symbols = sorted(combined_stock_symbols)

        default_cryptos = self.config.get('default_cryptos', [])
        crypto_symbols = crypto_symbols_input if crypto_symbols_input is not None else self.collect_symbols("Enter cryptocurrency symbols separated by semicolon (;), or press Enter to use default cryptocurrencies: ") if self.crypto_enabled else []
        combined_crypto_symbols = list(set(default_cryptos + crypto_symbols))
        sorted_crypto_symbols = sorted(combined_crypto_symbols)

        self._display_loop(sorted_stock_symbols, sorted_crypto_symbols)

    def _display_stock_prices(self, symbols, now):
        stock_prices = self.get_stock_prices(";".join(symbols))
        print("\033[H\033[J", end="")  # Clear screen
        print("Stock Prices as of " + now)
        self.utils.print_table_with_fixed_width(stock_prices)

    def _display_crypto_prices(self, symbols, now):
        crypto_prices = self.get_crypto_prices(";".join(symbols))
        if symbols:
            print("\n" + "-" * 50 + "\n")
        print("Cryptocurrency Prices as of " + now)
        self.utils.print_table_with_fixed_width(crypto_prices, False)

    def _display_loop(self, sorted_stock_symbols, sorted_crypto_symbols):
        while True:
            print("Refreshing...")
            now = datetime.now().strftime('%Y-%m-%d')
            
            if sorted_stock_symbols:
                self._display_stock_prices(sorted_stock_symbols, now)
            
            if self.crypto_enabled and sorted_crypto_symbols:
                self._display_crypto_prices(sorted_crypto_symbols, now)

            time.sleep(self.config.get('refresh_rate', 60))  # Refresh rate
