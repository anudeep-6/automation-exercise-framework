"""This file contains the BasePage class for all the page objects"""

from abc import ABC, abstractmethod


class BasePage(ABC):
    """Base class for the page objects

    All page classes must inherit from this and implement the abstract methods

    Args:
        url(str): The URL of the page
    """

    def __init__(self, url):
        self.url = url

    @abstractmethod
    def navigate(self):
        """Navigates to the page URL"""
        pass

    @abstractmethod
    def get_title(self):
        """Gets the title of the page"""
        pass

    def __str__(self):
        """Readable string for humans"""
        return f"{self.__class__.__name__}(url={self.url})"

    def __repr__(self):
        """Detailed string for debugging"""
        return f"{self.__class__.__name__}(url='{self.url}')"
