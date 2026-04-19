"""Reads and exposes configuration from config/config.json."""

import json

from src.utils.exceptions import ConfigurationException


class ConfigReader:
    """Loads config.json and exposes values as validated properties."""

    VALID_BROWSERS = {"chromium", "firefox", "webkit"}
    VALID_TRACE_OPTIONS = {"on", "off", "retain-on-failure"}
    VALID_SCREENSHOT_OPTIONS = {"on", "off", "only-on-failure"}

    def __init__(self, config_file: str = "config/config.json") -> None:
        """Initialises ConfigReader and loads the config file.

        Args:
            config_file (str): Path to the JSON config file.
                Defaults to config/config.json.
        """
        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self) -> dict:
        """Loads and returns parsed JSON config.

        Returns:
            dict: Parsed configuration dictionary.

        Raises:
            ConfigurationException: If file is missing or contains invalid JSON.
        """
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            raise ConfigurationException(self.config_file)
        except json.JSONDecodeError as err:
            raise ConfigurationException(f"{self.config_file} — invalid JSON: {err}")

    def get(self, key: str, default=None):
        """Generic accessor for any config key.

        Args:
            key (str): Config key to retrieve.
            default: Value to return if key is absent.

        Returns:
            Value associated with the key, or default if absent.
        """
        return self._config.get(key, default)

    @property
    def base_url(self) -> str:
        """Returns base UI URL.

        Raises:
            ConfigurationException: If base_url is missing or empty.
        """
        url = self._config.get("base_url")
        if not url:
            raise ConfigurationException("base_url is missing or empty in config")
        return url

    @property
    def base_api_url(self) -> str:
        """Returns base API URL.

        Raises:
            ConfigurationException: If base_api_url is missing or empty.
        """
        url = self._config.get("base_api_url")
        if not url:
            raise ConfigurationException("base_api_url is missing or empty in config")
        return url

    @property
    def browser(self) -> str:
        """Returns browser name validated against supported Playwright browsers.

        Raises:
            ConfigurationException: If browser value is not supported.
        """
        browser = self._config.get("browser", "chromium")
        if browser not in self.VALID_BROWSERS:
            raise ConfigurationException(
                f"browser — invalid value '{browser}', "
                f"must be one of {self.VALID_BROWSERS}"
            )
        return browser

    @property
    def headless(self) -> bool:
        """Returns headless flag. Defaults to True.

        Raises:
            ConfigurationException: If value is not a boolean.
        """
        value = self._config.get("headless", True)
        if not isinstance(value, bool):
            raise ConfigurationException(
                f"headless — expected a boolean, got '{value}'"
            )
        return value

    @property
    def timeout(self) -> int:
        """Returns default timeout in milliseconds. Defaults to 30000.

        Raises:
            ConfigurationException: If value is negative.
        """
        value = self._config.get("timeout", 30000)
        if not isinstance(value, int) or value < 0:
            raise ConfigurationException(
                f"timeout — must be a non-negative integer, got '{value}'"
            )
        return value

    @property
    def slow_mo(self) -> int:
        """Returns slow_mo delay in milliseconds. Defaults to 0.

        Raises:
            ConfigurationException: If value is negative.
        """
        value = self._config.get("slow_mo", 0)
        if not isinstance(value, int) or value < 0:
            raise ConfigurationException(
                f"slow_mo — must be a non-negative integer, got '{value}'"
            )
        return value

    @property
    def viewport(self) -> dict:
        """Returns viewport dict with width and height. Defaults to 1280x720."""
        return self._config.get("viewport", {"width": 1280, "height": 720})

    @property
    def trace(self) -> str:
        """Returns Playwright trace setting. Defaults to retain-on-failure.

        Raises:
            ConfigurationException: If value is not a valid trace option.
        """
        trace = self._config.get("trace", "retain-on-failure")
        if trace not in self.VALID_TRACE_OPTIONS:
            raise ConfigurationException(
                f"trace — invalid value '{trace}', "
                f"must be one of {self.VALID_TRACE_OPTIONS}"
            )
        return trace

    @property
    def screenshot(self) -> str:
        """Returns screenshot capture setting. Defaults to only-on-failure.

        Raises:
            ConfigurationException: If value is not a valid screenshot option.
        """
        screenshot = self._config.get("screenshot", "only-on-failure")
        if screenshot not in self.VALID_SCREENSHOT_OPTIONS:
            raise ConfigurationException(
                f"screenshot — invalid value '{screenshot}', "
                f"must be one of {self.VALID_SCREENSHOT_OPTIONS}"
            )
        return screenshot

    @property
    def retries(self) -> int:
        """Returns number of test retries. Defaults to 0.

        Raises:
            ConfigurationException: If value is not a non-negative integer.
        """
        value = self._config.get("retries", 0)
        if not isinstance(value, bool) is False and isinstance(value, bool):
            # bool is a subclass of int in Python — reject True/False explicitly
            raise ConfigurationException(
                f"retries — must be a non-negative integer, got '{value}'"
            )
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ConfigurationException(
                f"retries — must be a non-negative integer, got '{value}'"
            )
        return value
