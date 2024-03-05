# Stock Price Fetcher

This Python script fetches and displays real-time stock prices using `yfinance`. It allows users to specify a list of stock symbols or use a pre-defined list from the configuration file.

## Installation

To run this script, you need Python installed on your system. If you do not have Python, download and install it from [python.org](https://www.python.org/).

Once Python is installed, clone the repository or download the source code to your local machine.

Next, you'll need to install the required Python package `yfinance` and `pandas`. Run the following command to install them:

```bash
pip install yfinance pandas
```

Configuration

Before using the script, set up the config.json file with your preferred settings. Here's a template for config.json:

```json
Copy code
{
  "alpha_vantage": {
    "api_key": "your_api_key_here"
  },
  "refresh_rate": 10,
  "default_stocks":
["AAPL", "MSFT", "CDR.WA", "PKN.WA"],
"currency_map": {
".WA": "PLN",
"": "USD" // Assuming empty means it's a US stock
}
}
```

Replace `your_api_key_here` with your actual API key for Alpha Vantage if needed, though this script primarily uses `yfinance`, which does not require an API key.

## Usage

To run the script, navigate to the project directory in your terminal or command prompt and execute the script with Python:

```bash
python stock_prices.py