"""This file contains custom exceptions for the automation framework"""


class AutomationException(Exception):
    """Base exception class for all automation exceptions.
    All custom exceptions should inherit from this class.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class PageLoadException(AutomationException):
    """Raised when a page fails to load within the expected time
    Args:
        page_name (str): name of the page that failed to load
        url (str): URL that failed to load
    """

    def __init__(self, page_name, url):
        message = f"Page '{page_name}' falied to load at URL: {url}"
        super().__init__(message)


class ElementNotFoundException(AutomationException):
    """Raised when an expected element is not found on the page.
    Args:
        locator (str): The locator used to find the element
        page_name (str): Name of the page where element was not found
    """

    def __init__(self, locator, page_name):
        message = f"Element '{locator}' not found on {page_name}"
        super().__init__(message)
