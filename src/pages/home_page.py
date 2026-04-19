"""This file contains the HomePage class."""

import allure

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
    CONTACT_US_LINK = "a[href='/contact_us']"

    def is_logged_in(self) -> bool:
        """Returns True if 'Logged in as' is visible in the navbar."""
        return self.is_visible(self.LOGGED_IN_AS)

    def get_logged_in_username(self) -> str:
        """Returns the username shown in the navbar after login."""
        return self.get_text(self.USERNAME)

    @allure.step("Expect user is logged in as: {name}")
    def expect_logged_in(self, name: str) -> None:
        """Asserts the logged-in indicator is visible and shows the correct name.

        Args:
            username (str): The username expected to appear in the navbar.
        """
        self.expect_visible(self.LOGGED_IN_AS)
        self.expect_text(self.USERNAME, name)

    @allure.step("Expect home page is visible")
    def expect_home_page_visible(self) -> None:
        """Asserts the home page is loaded by checking the Home nav link."""
        self.expect_visible(self.HOME_LINK)

    @allure.step("Navigate to Signup / Login")
    def go_to_signup_login(self) -> None:
        """Clicks the Signup / Login link in the navbar."""
        self.click(self.SIGNUP_LOGIN_LINK)

    @allure.step("Navigate to Products")
    def go_to_products(self) -> None:
        """Clicks the Products link in the navbar."""
        self.click(self.PRODUCTS_LINK)

    @allure.step("Navigate to Cart")
    def go_to_cart(self) -> None:
        """Clicks the Cart link in the navbar."""
        self.click(self.CART_LINK)

    @allure.step("Logout")
    def logout(self) -> None:
        """Clicks the Logout link."""
        self.click(self.LOGOUT_LINK)

    @allure.step("Delete account")
    def delete_account(self) -> None:
        """Clicks the Delete Account link in the navbar."""
        self.click(self.DELETE_ACCOUNT_LINK)

    @allure.step("Navigate to Contact Us")
    def go_to_contact_us(self) -> None:
        """Clicks the Contact Us link in the navbar."""
        self.click(self.CONTACT_US_LINK)
