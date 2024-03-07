import unittest
from unittest.mock import patch
from datetime import datetime, time as datetime_time
import pytz
from mstocks.market import Market
from mstocks.utils import Utils


class TestMarket(unittest.TestCase):
    def setUp(self):
        self.utils = Utils()
        self.market = Market(self.utils)
        
    @patch('mstocks.market.datetime')
    def test_market_open_us(self, mock_datetime):
        # Create a mock datetime object
        mock_now = datetime(2024, 3, 7, 10, 0, 0, tzinfo=pytz.timezone('US/Eastern'))
        mock_datetime.now.return_value = mock_now

        status, _ = self.market.is_market_open("AAPL")  # Use a US market symbol
        self.assertIn(self.utils.GREEN, status)

    @patch('mstocks.market.datetime')
    def test_market_closed_us(self, mock_datetime):
        # Create a mock datetime object
        mock_now = datetime(2024, 3, 7, 5, 0, 0, tzinfo=pytz.timezone('US/Eastern'))
        mock_datetime.now.return_value = mock_now

        status, _ = self.market.is_market_open("AAPL")  # Use a US market symbol
        self.assertIn(self.utils.RED, status)

    @patch('mstocks.market.datetime')
    def test_market_open_warsaw(self, mock_datetime):
        # Create a mock datetime object
        mock_now = datetime(2024, 3, 7, 12, 0, 0, tzinfo=pytz.timezone('Europe/Warsaw'))
        mock_datetime.now.return_value = mock_now

        status, _ = self.market.is_market_open("CDR.WA")  # Use a US market symbol
        self.assertIn(self.utils.GREEN, status)

    @patch('mstocks.market.datetime')
    def test_market_closed_warsaw(self, mock_datetime):
        # Create a mock datetime object
        mock_now = datetime(2024, 3, 7, 18, 0, 0, tzinfo=pytz.timezone('Europe/Warsaw'))
        mock_datetime.now.return_value = mock_now

        status, _ = self.market.is_market_open("CDR.WA")  # Use a US market symbol
        self.assertIn(self.utils.RED, status)

if __name__ == '__main__':
    unittest.main()
