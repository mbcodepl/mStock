import argparse
import sys
from mstocks.endpoints import app
from mstocks.config import Config
from mstocks.run_manager import RunManager
from mstocks.stocks import StocksManager

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Manage stocks and crypto.')
    parser.add_argument('--silent', dest='silent', action='store_true', help='Enable silent mode to run in docker env (default: disabled)')
    parser.add_argument('--serve', dest='serve', action='store_true', help='Start the web server for API (default: disabled)')
    args = parser.parse_args()

    config = Config()
    runner = RunManager(config)

    if args.serve:
        # If --serve is specified, start the Flask web server
        app.run(debug=True, port=5000)  # You can change the port if needed
    elif args.silent:
        runner.run_silent()
    else:
        runner.run()

if __name__ == "__main__":
    main()
