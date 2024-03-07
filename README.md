# Stock Price Fetcher

This Python script fetches and displays real-time stock prices using `yfinance`. It allows users to specify a list of stock symbols or use a pre-defined list from the configuration file.

## Installation

To run this script, you need Python installed on your system. If you do not have Python, download and install it from [python.org](https://www.python.org/).

Once Python is installed, clone the repository or download the source code to your local machine.

Next, you'll need to install the required Python package `yfinance` and `pandas`. Run the following command to install them:

```bash
pip install yfinance pandas
```

## Configuration

Before using the script, set up the config.json file with your preferred settings. Here's a template for config.json:

```json
{
  "refresh_rate": 10,
  "default_stocks":["AAPL", "MSFT", "CDR.WA", "PKN.WA"],
  "currency_map": {
    ".WA": "PLN",
    "": "USD" // Assuming empty means it's a US stock
    }
}
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

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Contributing

Contributions are welcome. Please open an issue first to discuss what you would like to change or add.