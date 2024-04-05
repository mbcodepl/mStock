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


    # This method fetches the stock prices for the given symbols
    # it returns a list of lists containing the stock prices in formatted way to be displayed in table for console
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
                
                earnings, invested, percent_earned, buy_price = self.calculate_earnings(symbol, last_close if isinstance(last_close, float) else 0)
                earnings_str = Utils._format_value(earnings, currency, percent_earned) if earnings is not None else "—"
                invested_str = f"{invested:.2f} {currency} [{buy_price:.2f}]" if invested is not None else "—"

                market_status_symbol, last_refreshed_in_tz = self.market.is_market_open(symbol)
                formatted_price = f"{last_close:.2f} {currency}" if isinstance(last_close, float) else last_close
                
                prices.append([f"{market_status_symbol} ({last_refreshed_in_tz})", f"[{symbol}]", company_name, formatted_price, trend, invested_str, earnings_str])
            except IndexError:
                current_time = datetime.now().strftime('%H:%M:%S')
                prices.append(["Error", f"[{symbol}]", "N/A", "Not found", current_time, "—"])

        return prices
    
    # Thisn method fetches the stock prices for the given symbols
    # it returns a list of lists containing the stock prices in array format
    def get_stock_prices_json(self, symbols):
        prices = []
        for symbol in symbols.split(';'):
            symbol = symbol.strip()
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(period="2d")
                currency = self.utils.get_currency(symbol, self.currency_map)

                company_name = stock.info.get('longName', 'N/A')
                if len(hist) > 1:
                    last_close = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    price_change = float(last_close - prev_close)
                    percent_change = (price_change / prev_close) * 100

                    trend = {
                        "price_change": price_change,
                        "currency": currency,
                        "percent_change": percent_change
                    }
                else:
                    last_close = hist['Close'].iloc[-1] if len(hist) == 1 else "Not available"
                    trend = "—"

                earnings, invested, percent_earned, buy_price = self.calculate_earnings(
                    symbol, last_close if isinstance(last_close, float) else 0
                )
                earnings_info = {
                    "earnings": earnings,
                    "currency": currency,
                    "percent_earned": percent_earned
                } if earnings is not None else "—"
                invested_info = {
                    "invested": f"{invested:.2f}",
                    "currency": currency,
                    "buy_price": f"{buy_price:.2f}"
                } if invested is not None else "—"

                formatted_price = f"{last_close:.2f} {currency}" if isinstance(last_close, float) else last_close

                prices.append({
                    "symbol": symbol,
                    "company_name": company_name,
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

    
    def calculate_earnings(self, symbol, current_price):
        investments = self.config.get('investments', {}).get("stocks", {})
        total_invested = 0.0
        total_earnings = 0.0
        percentage_earned = 0.0
        buy_price = 0.0
        fee = 0.0

        if symbol in investments:
            transactions = investments[symbol]
            for transaction in transactions:
                buy_price = transaction.get('buy_price', 0)
                quantity = transaction.get('quantity', 1)  # Default quantity to 1 if not specified
                fee = transaction.get('fee', 0.0)  # Default fee to 0.0 if not specified
                invested = (buy_price * quantity) + fee
                total_invested += invested
                earnings = (current_price - buy_price) * quantity
                total_earnings += earnings

            # Avoid division by zero
            if total_invested > 0:
                percentage_earned = (total_earnings / total_invested) * 100

        return total_earnings, total_invested, percentage_earned, buy_price

    def _display_stock_prices(self, symbols, now):
        stock_prices = self.get_stock_prices(";".join(symbols))
        print("Stock Prices as of " + now)
        Utils.print_table_with_fixed_width(stock_prices)