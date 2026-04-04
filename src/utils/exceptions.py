"""This file contains custom exceptions for the automation framework."""


class AutomationException(Exception):
    """Base exception class for all automation exceptions.

    All custom exceptions should inherit from this class.

    Args:
        message (str): Human-readable description of the error.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class PageLoadException(AutomationException):
    """Raised when a page fails to load within the expected time.

    Args:
        page_name (str): Name of the page that failed to load.
        url (str): URL that failed to load.
    """

    def __init__(self, page_name: str, url: str):
        message = f"Page '{page_name}' failed to load at URL: {url}"
        super().__init__(message)


class ElementNotFoundException(AutomationException):
    """Raised when an expected element is not found on the page.

    Args:
        locator (str): The locator used to find the element.
        page_name (str): Name of the page where element was not found.
    """

    def __init__(self, locator: str, page_name: str):
        message = f"Element '{locator}' not found on {page_name}"
        super().__init__(message)


class ConfigurationException(AutomationException):
    """Raised when a required config key is missing or the config file is invalid.

    Args:
        key (str): The config key that was missing or invalid.
    """

    def __init__(self, key: str):
        message = f"Configuration error: missing or invalid key '{key}'"
        super().__init__(message)


class TestDataException(AutomationException):
    """Raised when test data is missing, malformed, or unreadable.

    Args:
        source (str): File path or data source that caused the error.
        detail (str): Specific description of what went wrong.
    """

    def __init__(self, source: str, detail: str):
        message = f"Test data error in '{source}': {detail}"
        super().__init__(message)
