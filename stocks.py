import yfinance as yf
import pandas as pd
import json
import time
from datetime import datetime, time as datetime_time
import pytz

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
                    trend = f"{GREEN}+{price_change:.2f} ({percent_change:.2f}%) ↑{RESET}"
                elif price_change < 0:
                    trend = f"{RED}{price_change:.2f} ({abs(percent_change):.2f}%) ↓{RESET}"
                else:
                    trend = f"{price_change:.2f} ({percent_change:.2f}%)"
            else:
                # Not enough data to determine the trend or price change
                last_close = hist['Close'].iloc[-1] if len(hist) == 1 else "Not available"
                trend = "—"
            
            # Adjust for the timezone
            market_status_symbol, last_refreshed_in_tz = is_market_open(symbol)  # Now also gets the time

            formatted_price = f"{last_close:.2f}  {currency}" if isinstance(last_close, float) else last_close
            prices.append([market_status_symbol, last_refreshed_in_tz, f"[{symbol}]", f"{company_name}", formatted_price, trend])
        except IndexError:
            current_time = datetime.now().strftime('%H:%M:%S')
            prices.append(["Error", f"[{symbol}]", "N/A", "Not found", current_time, "—"])

    return prices

def is_market_open(symbol):
    # Time zones
    eastern = pytz.timezone('US/Eastern')
    central_european = pytz.timezone('Europe/Warsaw')

    # Define market open and close times
    us_market_open = datetime_time(9, 30, 0)
    us_market_close = datetime_time(16, 0, 0)
    warsaw_market_open = datetime_time(9, 0, 0)
    warsaw_market_close = datetime_time(17, 0, 0)

    # Get current time in appropriate time zone based on symbol
    now = None
    market_open = None
    market_close = None
    if ".WA" in symbol:  # Warsaw market
        now = datetime.now(central_european)
        market_open = warsaw_market_open
        market_close = warsaw_market_close
    else:  # Default to US market
        now = datetime.now(eastern)
        market_open = us_market_open
        market_close = us_market_close

    # Check if current time is within market hours
    is_open = market_open <= now.time() <= market_close and now.weekday() < 5
    # Return symbol indicating market status and current time in the appropriate timezone
    return (f"{GREEN}●{RESET}" if is_open else f"{RED}●{RESET}"), now.strftime('%H:%M:%S')

def print_table_with_fixed_width(prices):
    # Create a list for each column's maximum width
    max_widths = [0] * len(prices[0])
    
    # Determine the maximum width needed for each column
    for row in prices:
        for i, item in enumerate(row):
            # Remove ANSI escape sequences for length calculation
            length = len(str(item).encode().decode('unicode_escape').encode('ascii', 'ignore').decode())
            if length > max_widths[i]:
                max_widths[i] = length

    # Define a format string with the determined widths for each column
    format_str = ' | '.join(f"{{:<{w}}}" for w in max_widths)

    # Print the header
    headers = ['Market status', 'Hour', 'Symbol', 'Name', 'Price', 'Trend']
    print(format_str.format(*headers))

    # Print a separator line
    print('-' * sum(max_widths) + '-----' * (len(max_widths) - 1))

    # Print each row using the format string
    for row in prices:
        print(format_str.format(*row))

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
    print("Refreshing...")
    # Get stock prices for combined symbols
    prices = get_stock_prices(";".join(sorted_symbols))

    print("\033[H\033[J", end="")  # Clears the screen in many terminal environments
    now = datetime.now().strftime('%Y-%m-%d')
    print("Date: " + now)
    print_table_with_fixed_width(prices)

    time.sleep(config['refresh_rate'])
