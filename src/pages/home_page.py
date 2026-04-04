"""This file contains the HomePage class."""

from src.pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the Home page.

    Inherits navigate() and get_title() from BasePage.
    Covers navbar interactions, logged-in state, and logout.
    """

    PATH = "/"

    HOME_LINK = "ul.nav.navbar-nav a[href='/']"
    PRODUCTS_LINK = "a[href='/products']"
    CART_LINK = "a[href='/view_cart']"
    SIGNUP_LOGIN_LINK = "a[href='/login']"
    LOGOUT_LINK = "a:text('Logout')"
    DELETE_ACCOUNT_LINK = "a:text('Delete Account')"
    LOGGED_IN_AS = "a:text('Logged in as')"
    USERNAME = "a:text('Logged in as') b"

    def is_logged_in(self) -> bool:
        """Returns True if 'Logged in as' is visible in the navbar."""
        return self.is_visible(self.LOGGED_IN_AS)

    def get_logged_in_username(self) -> str:
        """Returns the username shown in the navbar after login."""
        return self.get_text(self.USERNAME)

    def expect_logged_in(self):
        """Asserts the logged-in indicator is visible."""
        self.expect_visible(self.LOGGED_IN_AS)

    def expect_home_page_visible(self):
        """Asserts the home page is loaded by checking the Home nav link."""
        self.expect_visible(self.HOME_LINK)

    def go_to_signup_login(self):
        """Clicks the Signup / Login link in the navbar."""
        self.click(self.SIGNUP_LOGIN_LINK)

    def go_to_products(self):
        """Clicks the Products link in the navbar."""
        self.click(self.PRODUCTS_LINK)

    def go_to_cart(self):
        """Clicks the Cart link in the navbar."""
        self.click(self.CART_LINK)

    def logout(self):
        """Clicks the Logout link."""
        self.click(self.LOGOUT_LINK)

    def delete_account(self):
        """Clicks the Delete Account link in the navbar."""
        self.click(self.DELETE_ACCOUNT_LINK)
