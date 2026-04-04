"""Reads and exposes configuration from config/config.json"""

import json

from src.utils.exceptions import ConfigurationException


class ConfigReader:
    """Loads config.json and exposes values as validated properties.

    Args:
        config_file (str): Path to the JSON config file.
    """

    VALID_BROWSERS = {"chromium", "firefox", "webkit"}
    VALID_TRACE_OPTIONS = {"on", "off", "retain-on-failure"}
    VALID_SCREENSHOT_OPTIONS = {"on", "off", "only-on-failure"}

    def __init__(self, config_file="config/config.json"):
        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self):
        """Loads and returns parsed JSON config."""
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise ConfigurationException(self.config_file)
        except json.JSONDecodeError as err:
            raise ConfigurationException(f"{self.config_file} — invalid JSON: {err}")

    def get(self, key, default=None):
        """Generic accessor for any config key.

        Args:
            key (str): Config key to retrieve.
            default: Value to return if key is absent.
        """
        return self._config.get(key, default)

    @property
    def base_url(self):
        """Returns base UI URL. Raises if not configured."""
        url = self._config.get("base_url")
        if not url:
            raise ConfigurationException("base_url")
        return url

    @property
    def base_api_url(self):
        """Returns base API URL. Raises if not configured."""
        url = self._config.get("base_api_url")
        if not url:
            raise ConfigurationException("base_api_url")
        return url

    @property
    def browser(self):
        """Returns browser name. Validates against supported Playwright browsers."""
        browser = self._config.get("browser", "chromium")
        if browser not in self.VALID_BROWSERS:
            raise ConfigurationException(
                f"browser — invalid value '{browser}', "
                f"must be one of {self.VALID_BROWSERS}"
            )
        return browser

    @property
    def headless(self):
        """Returns headless flag. Defaults to True."""
        return self._config.get("headless", True)

    @property
    def timeout(self):
        """Returns default timeout in milliseconds. Defaults to 30000."""
        return self._config.get("timeout", 30000)

    @property
    def slow_mo(self):
        """Returns slow_mo delay in milliseconds. Defaults to 0."""
        return self._config.get("slow_mo", 0)

    @property
    def viewport(self):
        """Returns viewport dict with width and height. Defaults to 1280x720."""
        return self._config.get("viewport", {"width": 1280, "height": 720})

    @property
    def trace(self):
        """Returns Playwright trace setting. Defaults to retain-on-failure."""
        trace = self._config.get("trace", "retain-on-failure")
        if trace not in self.VALID_TRACE_OPTIONS:
            raise ConfigurationException(
                f"trace — invalid value '{trace}', "
                f"must be one of {self.VALID_TRACE_OPTIONS}"
            )
        return trace

    @property
    def screenshot(self):
        """Returns screenshot capture setting. Defaults to only-on-failure."""
        screenshot = self._config.get("screenshot", "only-on-failure")
        if screenshot not in self.VALID_SCREENSHOT_OPTIONS:
            raise ConfigurationException(
                f"screenshot — invalid value '{screenshot}', "
                f"must be one of {self.VALID_SCREENSHOT_OPTIONS}"
            )
        return screenshot

    @property
    def retries(self):
        """Returns number of test retries. Defaults to 1."""
        return self._config.get("retries", 1)
