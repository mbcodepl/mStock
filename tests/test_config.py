import unittest
from unittest.mock import patch, mock_open
import json
from mstocks.config import Config

class TestConfig(unittest.TestCase):

    def setUp(self):
        # Mock configuration data
        self.example_config_data = {
            "default_stocks": ["AAPL", "MSFT"],
            "refresh_rate": 60
        }
        # Mock json.load to return the example_config_data
        self.json_load_patch = patch('json.load', return_value=self.example_config_data)
        self.json_load_mock = self.json_load_patch.start()

    def tearDown(self):
        self.json_load_patch.stop()

    @patch('builtins.open', new_callable=mock_open)
    def test_load_config(self, mock_file):
        # Instantiate Config, which should use the mocked open
        config = Config()
        # Verify the mock was called with the correct filename
        mock_file.assert_called_with('data/config.json', 'r')
        # Verify json.load was called with the mock file handle
        self.json_load_mock.assert_called_once()
        # Verify that the configuration data matches the example
        self.assertEqual(config.config_data, self.example_config_data)

    def test_get_existing_key(self):
        # Instantiate Config and use the example config data
        config = Config()
        # Access a known key
        refresh_rate = config.get('refresh_rate')
        # Check if the known key's value is as expected
        self.assertEqual(refresh_rate, 60)

    def test_get_non_existing_key_with_default(self):
        # Instantiate Config and use the example config data
        config = Config()
        # Access a non-existing key with a default value
        non_existing = config.get('non_existing_key', 'default_value')
        # Check if the default value is returned
        self.assertEqual(non_existing, 'default_value')

    def test_get_non_existing_key_without_default(self):
        # Instantiate Config and use the example config data
        config = Config()
        # Access a non-existing key without a default value
        non_existing = config.get('non_existing_key')
        # Check if None is returned
        self.assertIsNone(non_existing)

if __name__ == '__main__':
    unittest.main()
