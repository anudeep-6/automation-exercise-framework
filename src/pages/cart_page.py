"""This file contains the CartPage class"""

from src.pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for the Cart Page"""

    PATH = "/view_cart"

    def __init__(self, base_url):
        super().__init__(url=f"{base_url}{self.PATH}")

    def navigate(self):
        """Navigate to the cart page"""
        pass

    def get_title(self):
        """Get the cart page title"""
        pass
