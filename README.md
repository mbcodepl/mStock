# Stock Price Fetcher

This Python script fetches and displays real-time stock prices using `yfinance`. It allows users to specify a list of stock symbols or use a pre-defined list from the configuration file.

## Installation

To run this script, you need Python installed on your system. If you do not have Python, download and install it from [python.org](https://www.python.org/).

Once Python is installed, clone the repository or download the source code to your local machine.

Next, you'll need to install the required Python package `yfinance` and `pandas`. Run the following command to install them:

```bash
pip install -r requiremnts.txt
```

## Configuration

The application uses a JSON configuration file. Here is a sample configuration:

```json
{
  "refresh_rate": 10,  // The rate at which the stock prices are refreshed
  "crypto": "False",  // Set to "True" if you want to fetch crypto prices
  "default_stocks": [  // The default stocks to fetch if no input is provided by the user
    "AAPL",
    "MSFT",
  ],
  "default_cryptos": [ // The default cryptos to fetch if no input is provided by the user
    "BTC-USD",
    "ETH-USD"
  ],
  "currency_map": { // Mapping of currency symbols to their full names
    ".WA": "PLN",
    "": "USD"
  },
  "investments": { // Your investments in different stocks
    "MSFT": [
      {
        "buy_price": 285.77,
        "buy_date": "2023-04-21",
        "quantity": 0.01959617,
        "fee": 0.95
      }
    ],
    "AAPL": [
      {
        "buy_price": 167.51,
        "buy_date": "2023-04-19",
        "quantity": 0.59697928,
        "fee": 0
      },
      {
        "buy_price": 165.13,
        "buy_date": "2023-04-21",
        "quantity": 0.40302072,
        "fee": 0.95
      },
    ]
  }
}
```
## Running Tests

To run the tests for this project, you can use the `unittest` module in Python. We also use `coverage` to measure the code coverage of our tests. You can run the tests with the following command:

```bash
coverage run -m unittest discover -s tests
```

## Usage

To run the script, navigate to the project directory in your terminal or command prompt and execute the script with Python:

```bash
python main.py
```

Upon running the script, you will be prompted to enter stock symbols separated by a semicolon (;). If you simply press Enter, the script will use the default stocks specified in config.json.

The script will then fetch the stock prices and display them, refreshing every few seconds based on the refresh_rate defined in the config.json file.

To stop the script, use the keyboard interrupt command, usually Ctrl+C or Ctrl+Z.

## License

This project is licensed under the MIT License. See the LICENSE.md file for details.

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change or add.