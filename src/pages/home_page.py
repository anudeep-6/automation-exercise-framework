"""This file contains the HomePage class"""

from src.pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the Home Page
    Inherits from BasePage and implements all the abstract methods
    """

    PATH = "/home"

    def __init__(self, base_url):
        super().__init__(url=f"{base_url}{self.PATH}")

    def navigate(self):
        """Navigate to the home page"""
        pass  # playwright code will be written later

    def get_title(self):
        """Get the home page title"""
        pass  # playwright code will be written later
