import argparse
import sys
from mstocks.config import Config
from mstocks.stocks import StocksManager

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Silent run.')
    # Change here: using store_true action for --silent
    parser.add_argument('--silent', dest='silent', action='store_true',
                         help='Enable silent mode to run in docker env (default: disabled)')

    # Parse arguments
    args = parser.parse_args()

    # Load configuration
    config = Config()

    # Create a StocksManager instance
    stocks_manager = StocksManager(config)

    # Decide which method to call based on silent_mode
    if args.silent:  # Directly using args.silent as it's already a boolean
        stocks_manager.run_silent()
    else:
        stocks_manager.run()

if __name__ == "__main__":
    main()
