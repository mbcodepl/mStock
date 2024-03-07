import json

class Config:
    def __init__(self, filename='data/config.json'):
        self.filename = filename
        self.config_data = self.load_config()

    def load_config(self):
        """Load configuration from the config.json file."""
        with open(self.filename, 'r') as file:
            return json.load(file)

    def get(self, key, default=None):
        """Get a value from the configuration data."""
        return self.config_data.get(key, default)
