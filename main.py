from mstocks.config import Config
from mstocks.stocks import StocksManager

def main():
    # Load configuration
    config = Config()

    # Create a StocksManager instance
    stocks_manager = StocksManager(config)

    # Run the main loop
    stocks_manager.display_stock_prices()

if __name__ == "__main__":
    main()