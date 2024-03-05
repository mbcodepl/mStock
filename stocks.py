import yfinance as yf
import pandas as pd
import json
import time
from datetime import datetime

# ANSI escape sequences for colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)
    
def get_currency(symbol, currency_map):
    for key in currency_map:
        if symbol.endswith(key):
            return currency_map[key]
    return "USD"  # Default to USD if not found

def get_stock_prices(symbols):
    prices = []
    for symbol in symbols.split(';'):
        symbol = symbol.strip()
        stock = yf.Ticker(symbol)
        hist = stock.history(period="2d")  # Fetches the last 2 days data
        currency = get_currency(symbol, currency_map)

        try:
            # Fetch the company name
            company_name = stock.info.get('longName', 'N/A')

            if len(hist) > 1:
                last_close = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                price_change = last_close - prev_close
                percent_change = (price_change / prev_close) * 100

                # Determine the price direction compared to the previous market day
                if price_change > 0:
                    trend = f"{GREEN} {price_change:.2f} ({percent_change:.2f}%) ↑{RESET}"
                elif price_change < 0:
                    trend = f"{RED} {price_change:.2f} ({abs(percent_change):.2f}%) ↓{RESET}"
                else:
                    trend = f"{price_change:.2f} ({percent_change:.2f}%)"
            else:
                # Not enough data to determine the trend or price change
                last_close = hist['Close'].iloc[-1] if len(hist) == 1 else "Not available"
                trend = "—"
            
            last_refreshed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_price = f"{last_close:.2f}  {currency}" if isinstance(last_close, float) else last_close
            prices.append([last_refreshed, f"[{symbol}]", f"{company_name} |", formatted_price, trend])
        except IndexError:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            prices.append(["Error", f"[{symbol}]", "N/A", "Not found", current_time, "—"])

    return prices

# Load configuration
config = load_config()

# Default stocks are taken from the config file
default_stocks = config.get('default_stocks', [])
currency_map = config.get('currency_map', {"": "USD"})

# Prompt user for additional stock symbols, if desired
user_input = input("Enter stock symbols separated by semicolon (;), or press Enter to use default stocks: ")
user_symbols = user_input.split(';') if user_input.strip() else []

# Combine default stocks with user-provided stocks, avoiding duplicates
combined_symbols = list(set(default_stocks + user_symbols))
# Now sort the combined symbols alphabetically
sorted_symbols = sorted(combined_symbols)

while True:
    # Get stock prices for combined symbols
    prices = get_stock_prices(";".join(sorted_symbols))

    # Convert data to DataFrame
    df = pd.DataFrame(prices, columns=['Date', 'Symbol', 'Name', 'Price', ''])

    # Clear output before refreshing data (optional, depending on your environment)
    print("\033[H\033[J", end="")  # Clears the screen in many terminal environments
    print(df.to_string(index=False))  # Use to_string to properly display the DataFrame in the console

    time.sleep(config['refresh_rate'])