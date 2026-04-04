"""This file contains the LoginPage class."""

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the Login/Signup page.

    Inherits navigate() and get_title() from BasePage.
    Adds login- and signup-specific locators and interactions.
    """

    PATH = "/login"

    # --- Locators ---
    EMAIL_INPUT = "input[data-qa='login-email']"
    PASSWORD_INPUT = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    LOGIN_ERROR = "p:text('Your email or password is incorrect!')"

    SIGNUP_NAME_INPUT = "input[data-qa='signup-name']"
    SIGNUP_EMAIL_INPUT = "input[data-qa='signup-email']"
    SIGNUP_BUTTON = "button[data-qa='signup-button']"
    SIGNUP_ERROR = "p:text('Email Address already exist!')"

    def enter_login_email(self, email: str):
        """Fills the login email input."""
        self.fill(self.EMAIL_INPUT, email)

    def enter_login_password(self, password: str):
        """Fills the login password input."""
        self.fill(self.PASSWORD_INPUT, password)

    def submit_login(self):
        """Clicks the login button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, email: str, password: str):
        """Full login flow: fill email, fill password, submit.

        Args:
            email: User email address.
            password: User password.
        """
        self.enter_login_email(email)
        self.enter_login_password(password)
        self.submit_login()

    def get_login_error(self) -> str:
        """Returns the login error message text."""
        return self.get_text(self.LOGIN_ERROR)

    def expect_login_error_visible(self):
        """Asserts the login error message is visible."""
        self.expect_visible(self.LOGIN_ERROR)

    def enter_signup_name(self, name: str):
        """Fills the signup name input."""
        self.fill(self.SIGNUP_NAME_INPUT, name)

    def enter_signup_email(self, email: str):
        """Fills the signup email input."""
        self.fill(self.SIGNUP_EMAIL_INPUT, email)

    def submit_signup(self):
        """Clicks the signup button."""
        self.click(self.SIGNUP_BUTTON)

    def signup(self, name: str, email: str):
        """Full signup flow: fill name, fill email, submit.

        Args:
            name: New user's display name.
            email: New user's email address.
        """
        self.enter_signup_name(name)
        self.enter_signup_email(email)
        self.submit_signup()

    def get_signup_error(self) -> str:
        """Returns the signup error message text."""
        return self.get_text(self.SIGNUP_ERROR)

    def expect_signup_error_visible(self):
        """Asserts the signup error message is visible."""
        self.expect_visible(self.SIGNUP_ERROR)
