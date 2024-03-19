import argparse
from mstocks.config import Config
from mstocks.stocks import StocksManager

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Display stock and cryptocurrency prices.')
    parser.add_argument('--crypto', dest='crypto', action='store', default='true',
                        help='Enable or disable cryptocurrency information (default: enabled)')

    # Parse arguments
    args = parser.parse_args()
    
    # # Convert crypto argument to boolean
    # crypto_enabled = False if args.crypto.lower() == 'false' else True

    # Load configuration
    config = Config()

    # Create a StocksManager instance
    stocks_manager = StocksManager(config)

    # Run the main loop
    stocks_manager.display_prices()

if __name__ == "__main__":
    main()