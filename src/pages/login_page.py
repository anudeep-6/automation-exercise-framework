"""This file contains the LoginPage class."""

import allure

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the Login/Signup page.

    Inherits navigate() and get_title() from BasePage.
    Adds login- and signup-specific locators and interactions.
    """

    PATH = "/login"

    LOGIN_FORM_HEADING = "h2:has-text('Login to your account')"
    EMAIL_INPUT = "input[data-qa='login-email']"
    PASSWORD_INPUT = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    LOGIN_ERROR = "p:has-text('Your email or password is incorrect!')"

    SIGNUP_NAME_INPUT = "input[data-qa='signup-name']"
    SIGNUP_EMAIL_INPUT = "input[data-qa='signup-email']"
    SIGNUP_BUTTON = "button[data-qa='signup-button']"
    SIGNUP_ERROR = "p:has-text('Email Address already exist!')"

    @allure.step("Expect login form visible")
    def expect_login_form_visible(self):
        """Asserts 'Login to your account' heading is visible."""
        self.expect_visible(self.LOGIN_FORM_HEADING)

    @allure.step("Enter login email: {email}")
    def enter_login_email(self, email: str):
        """Fills the login email input."""
        self.fill(self.EMAIL_INPUT, email)

    @allure.step("Enter login password")
    def enter_login_password(self, password: str):
        """Fills the login password input."""
        self.fill(self.PASSWORD_INPUT, password)

    @allure.step("Submit login form")
    def submit_login(self):
        """Clicks the login button."""
        self.click(self.LOGIN_BUTTON)

    @allure.step("Login with email {email}")
    def login(self, email: str, password: str):
        """Full login flow: fill email, fill password, submit.

        Args:
            email: User email address.
            password: User password.
        """
        self.enter_login_email(email)
        self.enter_login_password(password)
        self.submit_login()

    @allure.step("Get login error message")
    def get_login_error(self) -> str:
        """Returns the login error message text."""
        return self.get_text(self.LOGIN_ERROR)

    @allure.step("Expect login error visible")
    def expect_login_error_visible(self):
        """Asserts the login error message is visible."""
        self.expect_visible(self.LOGIN_ERROR)

    @allure.step("Get email field validation message")
    def get_email_validation_message(self) -> str:
        """Gets the HTML5 validation message for the email input field.

        Returns:
            str: The validation message from the email input element.
        """
        return self.page.locator(self.EMAIL_INPUT).evaluate(
            "el => el.validationMessage"
        )

    @allure.step("Expect empty email validation message")
    def expect_empty_email_validation(self):
        """Asserts that the email field shows a 'required' validation message."""
        message = self.get_email_validation_message()
        assert (
            "fill out" in message.lower() or "please" in message.lower()
        ), f"Expected empty field validation, got: '{message}'"

    @allure.step("Expect invalid email format validation message")
    def expect_invalid_email_format_validation(self):
        """Asserts that the email field shows a format validation message."""
        message = self.get_email_validation_message()
        assert (
            "@" in message or "email" in message.lower()
        ), f"Expected format validation, got: '{message}'"

    @allure.step("Enter signup name: {name}")
    def enter_signup_name(self, name: str):
        """Fills the signup name input."""
        self.fill(self.SIGNUP_NAME_INPUT, name)

    @allure.step("Enter signup email: {email}")
    def enter_signup_email(self, email: str):
        """Fills the signup email input."""
        self.fill(self.SIGNUP_EMAIL_INPUT, email)

    @allure.step("Submit signup form")
    def submit_signup(self):
        """Clicks the signup button."""
        self.click(self.SIGNUP_BUTTON)

    @allure.step("Signup with name {name} and email {email}")
    def signup(self, name: str, email: str):
        """Full signup flow: fill name, fill email, submit.

        Args:
            name: New user's display name.
            email: New user's email address.
        """
        self.enter_signup_name(name)
        self.enter_signup_email(email)
        self.submit_signup()

    @allure.step("Get signup error message")
    def get_signup_error(self) -> str:
        """Returns the signup error message text."""
        return self.get_text(self.SIGNUP_ERROR)

    @allure.step("Expect signup error visible")
    def expect_signup_error_visible(self):
        """Asserts the signup error message is visible."""
        self.expect_visible(self.SIGNUP_ERROR)
