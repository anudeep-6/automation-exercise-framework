"""Custom exception hierarchy for the automation framework.

Exceptions:
    AutomationException     — base class for all framework exceptions
    PageLoadException       — page did not reach expected state
    ConfigurationException  — config key missing or value invalid
    TestDataException       — test data file missing or malformed
    DialogException         — expected browser dialog did not appeared
"""


class AutomationException(Exception):
    """Base class for all automation framework exceptions.

    All custom exceptions should inherit from this class to allow
    callers to catch any framework error with a single except clause.

    Args:
        message (str): Human-readable description of the error.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"


class PageLoadException(AutomationException):
    """Raised when a page fails to reach its expected loaded state.

    Args:
        page_name (str): Name of the page that failed to load.
        url (str): URL that was being loaded.
    """

    def __init__(self, page_name: str, url: str) -> None:
        message = f"Page '{page_name}' failed to load at URL: {url}"
        super().__init__(message)


class ConfigurationException(AutomationException):
    """Raised when a required config key is missing or its value is invalid.

    Args:
        key (str): The config key that was missing or invalid.
    """

    def __init__(self, key: str) -> None:
        message = f"Configuration error: missing or invalid key '{key}'"
        super().__init__(message)


class TestDataException(AutomationException):
    """Raised when test data is missing, malformed, or unreadable.

    Args:
        source (str): File path or data source that caused the error.
        detail (str): Specific description of what went wrong.
    """

    def __init__(self, source: str, detail: str) -> None:
        message = f"Test data error in '{source}': {detail}"
        super().__init__(message)


class DialogException(AutomationException):
    """Raised when an expected browser dialog did not appear.

    Args:
        action (str): Description of the action that should have triggered the dialog.
    """

    def __init__(self, action: str) -> None:
        message = f"Expected a browser dialog after '{action}', but none was triggered."
        super().__init__(message)
