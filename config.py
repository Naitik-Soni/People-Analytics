"""
Config module for loading every config used in the application
"""

import json
from pathlib import Path

from logger import logger

class Config:
    "Config class for getting config file"
    def __init__(self):
        path = Path(__file__).parent.parent / "config.json"

        logger.debug("Config loaded...")
        with open(path, "r", encoding="utf-8") as f:
            self._config = json.load(f)


    # Returns value containing keys passed
    def get(self, *keys, default=None):
        value = self._config
        for key in keys:
            value = value.get(key)
            if value is None:
                return default
        logger.debug(f"Getting config for {key}={value}")
        return value

config = Config()