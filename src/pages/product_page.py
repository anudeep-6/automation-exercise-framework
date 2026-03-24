"""This file contains the ProductPage class"""

from src.pages.base_page import BasePage


class ProductPage(BasePage):
    """Page object for the Products Page"""

    PATH = "/products"

    def __init__(self, base_url):
        super().__init__(url=f"{base_url}{self.PATH}")

    def navigate(self):
        """Navigate to the products page"""
        pass

    def get_title(self):
        """Get the products page title"""
        pass
