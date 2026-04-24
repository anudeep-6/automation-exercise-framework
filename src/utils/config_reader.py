"""Reads and exposes configuration from environment variables via python-decouple."""

from decouple import UndefinedValueError, config

from src.utils.exceptions import ConfigurationException


class ConfigReader:
    """Exposes environment-driven config values as validated properties."""

    VALID_BROWSERS = {"chromium", "firefox", "webkit"}
    VALID_TRACE_OPTIONS = {"on", "off", "retain-on-failure"}
    VALID_SCREENSHOT_OPTIONS = {"on", "off", "only-on-failure"}

    @property
    def base_url(self) -> str:
        """Returns base UI URL from BASE_URL env var.

        Raises:
            ConfigurationException: If BASE_URL is not set.
        """
        try:
            return config("BASE_URL")
        except UndefinedValueError:
            raise ConfigurationException("BASE_URL is not set in .env or environment")

    @property
    def base_api_url(self) -> str:
        """Returns base API URL from BASE_API_URL env var.

        Raises:
            ConfigurationException: If BASE_API_URL is not set.
        """
        try:
            return config("BASE_API_URL")
        except UndefinedValueError:
            raise ConfigurationException(
                "BASE_API_URL is not set in .env or environment"
            )

    @property
    def browser(self) -> str:
        """Returns browser name from BROWSER env var. Defaults to chromium.

        Raises:
            ConfigurationException: If value is not a supported Playwright browser.
        """
        browser = config("BROWSER", default="chromium")
        if browser not in self.VALID_BROWSERS:
            raise ConfigurationException(
                f"BROWSER — invalid value '{browser}', "
                f"must be one of {self.VALID_BROWSERS}"
            )
        return browser

    @property
    def headless(self) -> bool:
        """Returns headless flag from HEADLESS env var. Defaults to True.

        Raises:
            ConfigurationException: If value cannot be cast to bool.
        """
        try:
            return config("HEADLESS", default=True, cast=bool)
        except ValueError:
            raise ConfigurationException("HEADLESS — expected true or false")

    @property
    def timeout(self) -> int:
        """Returns default timeout in milliseconds from TIMEOUT env var.
        Defaults to 30000.

        Raises:
            ConfigurationException: If value is not a non-negative integer.
        """
        try:
            value = config("TIMEOUT", default=30000, cast=int)
        except ValueError:
            raise ConfigurationException("TIMEOUT — must be a non-negative integer")
        if value < 0:
            raise ConfigurationException(
                f"TIMEOUT — must be non-negative, got '{value}'"
            )
        return value

    @property
    def slow_mo(self) -> int:
        """Returns slow_mo delay in milliseconds from SLOW_MO env var.
        Defaults to 0.

        Raises:
            ConfigurationException: If value is not a non-negative integer.
        """
        try:
            value = config("SLOW_MO", default=0, cast=int)
        except ValueError:
            raise ConfigurationException("SLOW_MO — must be a non-negative integer")
        if value < 0:
            raise ConfigurationException(
                f"SLOW_MO — must be non-negative, got '{value}'"
            )
        return value

    @property
    def viewport(self) -> dict:
        """Returns viewport dict. Hardcoded default — not environment-specific."""
        return {"width": 1280, "height": 720}

    @property
    def trace(self) -> str:
        """Returns Playwright trace setting. Defaults to retain-on-failure."""
        return "retain-on-failure"

    @property
    def screenshot(self) -> str:
        """Returns screenshot setting. Defaults to only-on-failure."""
        return "only-on-failure"

    @property
    def retries(self) -> int:
        """Returns number of test retries from RETRIES env var. Defaults to 0.

        Raises:
            ConfigurationException: If value is not a non-negative integer.
        """
        try:
            value = config("RETRIES", default=0, cast=int)
        except ValueError:
            raise ConfigurationException("RETRIES — must be a non-negative integer")
        if value < 0:
            raise ConfigurationException(
                f"RETRIES — must be non-negative, got '{value}'"
            )
        return value
