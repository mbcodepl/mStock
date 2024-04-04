import yfinance as yf
import time
from datetime import datetime
from .market import Market
from .config import Config
from .utils import Utils


class CryptoManager:
    def __init__(self, config):
        self.config = config
        self.utils = Utils()
        self.market = Market(self.utils)
        self.currency_map = config.get('currency_map', {"": "USD"})
        crypto_str = self.config.get('crypto', 'False')  # Default to 'False' if not found
        self.crypto_enabled = True if crypto_str == "True" else False
    
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
    
    def _display_crypto_prices(self, symbols, now):
        crypto_prices = self.get_crypto_prices(";".join(symbols))
        if symbols:
            print("\n" + "-" * 50 + "\n")
        print("Cryptocurrency Prices as of " + now)
        self.utils.print_table_with_fixed_width(crypto_prices, False)