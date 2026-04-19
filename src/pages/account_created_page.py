"""This file contains AccountCreatedPage class"""

import allure

from src.pages.base_page import BasePage


class AccountCreatedPage(BasePage):
    """Page object for the Account Created confirmation page (/account_created).

    Displayed after successful user registration. Provides assertion
    for the confirmation heading and navigation via the Continue button.
    """

    PATH = "/account_created"

    ACCOUNT_CREATED_HEADING = "[data-qa='account-created']"
    CONTINUE_BUTTON = "[data-qa='continue-button']"

    @allure.step("Expect account created heading is visible")
    def expect_account_created_visible(self) -> None:
        """Asserts the account created confirmation heading is visible."""
        self.expect_visible(self.ACCOUNT_CREATED_HEADING)

    @allure.step("Click Continue button")
    def click_continue(self) -> None:
        """Clicks the Continue button on the account creation confirmation page."""
        self.click(self.CONTINUE_BUTTON)
