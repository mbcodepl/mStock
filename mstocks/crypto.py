import yfinance as yf
import time
from datetime import datetime
from .market import Market
from .config import Config
from .utils import Utils
import requests


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
                    trend = Utils._format_value(price_change, "PLN", percent_change)
                else:
                    last_close = hist['Close'].iloc[-1] if len(hist) == 1 else 0
                    trend = "—"

                # Convert USD price to PLN
                pln_price = self.convert_to_pln(last_close)
                earnings, invested, percent_earned, buy_price, quantity = self.calculate_earnings(symbol, pln_price if isinstance(pln_price, float) else 0)
                earnings_str = Utils._format_value(earnings, "PLN", percent_earned) if earnings is not None else "—"
                invested_str = f"{invested:.2f} PLN" if invested is not None else "—"                

                formatted_price = f"{pln_price:,.4f} PLN".replace(",", " ") if isinstance(pln_price, float) else pln_price
                prices.append([f"[{symbol}]", "Crypto", formatted_price, trend, invested_str, earnings_str])
            except IndexError:
                current_time = datetime.now().strftime('%H:%M:%S')
                prices.append(["Error", f"[{symbol}]", "N/A", "Not found", current_time, "—"])
        return prices
    
    # Thisn method fetches the stock prices for the given symbols
    # it returns a list of lists containing the stock prices in array format
    def get_crypto_prices_json(self, symbols):
        prices = []
        for symbol in symbols.split(';'):
            symbol = symbol.strip()
            try:
                crypto = yf.Ticker(symbol)
                hist = crypto.history(period="2d")
                currency = self.utils.get_currency(symbol, self.currency_map)
                if len(hist) > 1:
                    last_close = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    price_change = last_close - prev_close
                    percent_change = (price_change / prev_close) * 100
                    # Determine the price direction
                    trend = {
                        "price_change": price_change,
                        "percent_change": percent_change
                    }
                else:
                    last_close = hist['Close'].iloc[-1] if len(hist) == 1 else 0
                    trend = "—"

                pln_price = self.convert_to_pln(last_close)
                earnings, invested, percent_earned, buy_price, quantity = self.calculate_earnings(symbol, pln_price if isinstance(pln_price, float) else 0)
                
                earnings_info = {
                    "earnings": earnings,
                    "percent_earned": percent_earned
                } if earnings is not None else "—"
                invested_info = {
                    "invested": f"{invested:.2f}",
                    "quantity": f"{quantity:.2f}",
                    "average_buy_price": f"{buy_price:.2f}"
                } if invested is not None else "—"

                formatted_price = f"{last_close:.2f} {currency}" if isinstance(last_close, float) else last_close

                prices.append({
                    "symbol": symbol,
                    "last_close_price": formatted_price,
                    "trend": trend,
                    "invested": invested_info,
                    "earnings": earnings_info
                })
            except ValueError as e:
                # Handling the case where the symbol is invalid or data could not be fetched.
                prices.append(["Error", f"[{symbol}]", "N/A", "Invalid Symbol or Data Not Found", "—", "—", "—"])
            except Exception as e:
                # General error handling, could be network error, etc.
                prices.append(["Error", f"[{symbol}]", "N/A", "Error Fetching Data", "—", "—", "—"])
                
        return prices

    def convert_to_pln(self, usd_price):
        # Use an API or library to get the exchange rate from USD to PLN
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        exchange_rates = response.json().get('rates')
        pln_rate = exchange_rates.get('PLN')
        pln_price = usd_price * pln_rate
        return pln_price
    
    def calculate_earnings(self, symbol, current_price):
        earnings = 0
        invested = 0
        buy_price = 0
        percentage = 0
        amount = 0
        fee = 0
        investments = self.config.get('investments', {}).get("cryptos", {})

        if symbol in investments:
            for investment in  investments[symbol]:
                buy_price = investment.get('buy_price', 0)
                quantity = investment.get('quantity', 1)
                fee = investment.get('fee', 0)

                invested += (buy_price * quantity) + fee
                earnings += (current_price - buy_price) * quantity
                amount += quantity

        avg_price = invested / amount if amount > 0 else 0

        if invested:
            percentage = (earnings / invested) * 100
        return earnings, invested, percentage, avg_price, amount
    
    def _display_crypto_prices(self, symbols, now):
        crypto_prices = self.get_crypto_prices(";".join(symbols))
        if symbols:
            print("\n" + "-" * 50 + "\n")
        print("Cryptocurrency Prices as of " + now)
        self.utils.print_table_with_fixed_width(crypto_prices, False)