from mstocks.config import Config
from mstocks.stocks import StocksManager
from mstocks.crypto import CryptoManager
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/stocks', methods=['GET'])
def api_get_stocks():
    config = Config()
    manager = StocksManager(config)
    stock_symbols = config.get('default_stocks', [])
    stock_prices = manager.get_stock_prices_json(";".join(stock_symbols))
    return jsonify(stock_prices)

@app.route('/api/stocks/<symbols>', methods=['GET'])
def api_get_stocks_by_symbols(symbols):
    config = Config()
    manager = StocksManager(config)
    stock_prices = manager.get_stock_prices_json(symbols)
    return jsonify(stock_prices)

@app.route('/api/crypto', methods=['GET'])
def api_get_crypto():
    config = Config()
    manager = CryptoManager(config)
    crypto_symbols = config.get('default_cryptos', [])
    crypto_prices = manager.get_crypto_prices_json(";".join(crypto_symbols))
    return jsonify(crypto_prices)

@app.route('/api/crypto/<symbols>', methods=['GET'])
def api_get_crypto_by_symbols(symbols):
    config = Config()
    manager = CryptoManager(config)
    crypto_prices = manager.get_crypto_prices_json(symbols)
    return jsonify(crypto_prices)