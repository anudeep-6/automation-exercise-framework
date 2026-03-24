"""This file contains the LoginPage class"""

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the Login Page
    Inherits from BasePage and implements all the abstract methods
    """

    PATH = "/login"

    def __init__(self, base_url):
        super().__init__(url=f"{base_url}{self.PATH}")

    def navigate(self):
        """Navigate to the login page"""
        pass  # playwright code will be written later

    def get_title(self):
        """Get the login page title"""
        pass  # playwright code will be written later
