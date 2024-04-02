import argparse
import sys
from mstocks.config import Config
from mstocks.stocks import StocksManager

def main():
    # Load configuration
    config = Config()

    # Create a StocksManager instance
    stocks_manager = StocksManager(config)

    stocks_manager.display_prices()


if __name__ == "__main__":
    main()