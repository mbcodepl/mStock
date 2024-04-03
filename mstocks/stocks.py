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
            hist = stock.history(period="2d")
            currency = self.utils.get_currency(symbol, self.currency_map)

            try:
                company_name = stock.info.get('longName', 'N/A')
                if len(hist) > 1:
                    last_close = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    price_change = float(last_close - prev_close)
                    percent_change = (price_change / prev_close) * 100

                    trend = Utils._format_value(price_change, currency, percent_change)
                else:
                    last_close = hist['Close'].iloc[-1] if len(hist) == 1 else "Not available"
                    trend = "—"
                
                earnings, invested, _ = self.calculate_earnings(symbol, last_close if isinstance(last_close, float) else 0)
                earnings_str = Utils._format_value(earnings, currency) if earnings is not None else "—"
                invested_str = f"{invested:.2f} {currency}" if invested is not None else "—"

                market_status_symbol, last_refreshed_in_tz = self.market.is_market_open(symbol)
                formatted_price = f"{last_close:.2f} {currency}" if isinstance(last_close, float) else last_close
                
                prices.append([market_status_symbol, last_refreshed_in_tz, f"[{symbol}]", company_name, formatted_price, trend, invested_str, earnings_str])
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
                    trend = Utils._format_value(price_change, "USD", percent_change)
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
    
    def calculate_earnings(self, symbol, current_price):
        investments = self.config.get('investments', {})
        total_invested = 0.0
        total_earnings = 0.0
        percentage_earned = 0.0

        if symbol in investments:
            transactions = investments[symbol]
            for transaction in transactions:
                buy_price = transaction.get('buy_price')
                quantity = transaction.get('quantity', 1)  # Default quantity to 1 if not specified
                invested = buy_price * quantity
                total_invested += invested
                earnings = (current_price - buy_price) * quantity
                total_earnings += earnings

            # Avoid division by zero
            if total_invested > 0:
                percentage_earned = (total_earnings / total_invested) * 100

        return total_earnings, total_invested, percentage_earned
        
    def collect_symbols(self, text):
        inpt = input(text)
        return inpt.split(';') if inpt.strip() else []
    
    def run(self, stock_symbols_input=None, crypto_symbols_input=None):
        default_stocks = self.config.get('default_stocks', [])
        stock_symbols = stock_symbols_input if stock_symbols_input is not None else self.collect_symbols("Enter stock symbols separated by semicolon (;), or press Enter to use default stocks: ")
        combined_stock_symbols = list(set(default_stocks + stock_symbols))
        sorted_stock_symbols = sorted(combined_stock_symbols)

        default_cryptos = self.config.get('default_cryptos', [])
        crypto_symbols = crypto_symbols_input if crypto_symbols_input is not None else self.collect_symbols("Enter cryptocurrency symbols separated by semicolon (;), or press Enter to use default cryptocurrencies: ") if self.crypto_enabled else []
        combined_crypto_symbols = list(set(default_cryptos + crypto_symbols))
        sorted_crypto_symbols = sorted(combined_crypto_symbols)

        self._display_loop(sorted_stock_symbols, sorted_crypto_symbols)
    
    def run_silent(self):
        default_stocks = self.config.get('default_stocks', [])
        sorted_stock_symbols = sorted(default_stocks)

        default_cryptos = self.config.get('default_cryptos', [])
        sorted_crypto_symbols = sorted(default_cryptos)

        self._display_loop(sorted_stock_symbols, sorted_crypto_symbols)

    def _display_stock_prices(self, symbols, now):
        stock_prices = self.get_stock_prices(";".join(symbols))
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
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("\033[H\033[J", end="")  # Clear screen
            if sorted_stock_symbols:
                self._display_stock_prices(sorted_stock_symbols, now)
            
            if self.crypto_enabled and sorted_crypto_symbols:
                self._display_crypto_prices(sorted_crypto_symbols, now)

            time.sleep(self.config.get('refresh_rate', 60))  # Refresh rate
