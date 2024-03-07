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

    def _format_trend(self, price_change, percent_change, currency):
        if price_change > 0:
            return f"{self.utils.GREEN}+{price_change:.2f} {currency} ({percent_change:.2f}%) ↑{self.utils.RESET}"
        elif price_change < 0:
            return f"{self.utils.RED}{price_change:.2f} {currency} ({abs(percent_change):.2f}%) ↓{self.utils.RESET}"
        else:
            return f"{price_change:.2f} {currency} ({percent_change:.2f}%)"

    def display_stock_prices(self):
        default_stocks = self.config.get('default_stocks', [])
        user_input = input("Enter stock symbols separated by semicolon (;), or press Enter to use default stocks: ")
        user_symbols = user_input.split(';') if user_input.strip() else []

        combined_symbols = list(set(default_stocks + user_symbols))
        sorted_symbols = sorted(combined_symbols)

        while True:
            print("Refreshing...")
            prices = self.get_stock_prices(";".join(sorted_symbols))
            print("\033[H\033[J", end="")  # Clears the screen in many terminal environments
            now = datetime.now().strftime('%Y-%m-%d')
            print("Date: " + now)
            self.utils.print_table_with_fixed_width(prices)
            time.sleep(self.config.get('refresh_rate', 60))  # Default to 60 seconds