"""This file reads the config data from json file"""

import json


class ConfigReader:
    """This class loads the json file to get the data
    Args:
        config_file (str): path to the JSON config file
    """

    def __init__(self, config_file="config/config.json"):
        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self):
        """loads and returns data from the config JSON file"""
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"file not found at {self.config_file}")
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON in config file {err}")

    @property
    def base_url(self):
        """Returns base url, raises error if not configured"""
        url = self._config.get("baseUrl")
        if not url:
            raise ValueError("base url is not configured in config file")
        return url

    @property
    def browser(self):
        """Returns browser, raises error if not configured or invalid"""
        browser = self._config.get("browser")
        if not browser:
            raise ValueError("Browser is not configured in the config file")
        if browser not in ["chromium", "firefox", "webkit"]:
            raise ValueError(f"Invalid browser: {browser}")
        return browser

    @property
    def timeout(self):
        """Returns timeout in milliseconds, defaults to 3000 if not set"""
        return self._config.get("timeout", 30000)
