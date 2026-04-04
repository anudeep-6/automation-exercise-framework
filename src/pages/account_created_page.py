"""This file contains AccountCreatedPage class"""

from src.pages.base_page import BasePage


class AccountCreatedPage(BasePage):
    """Page object for the Account Created confirmation page (/account_created).

    Displayed after successful user registration. Provides assertion
    for the confirmation heading and navigation via the Continue button.
    """

    PATH = "/account_created"

    # Locators
    ACCOUNT_CREATED_HEADING = "[data-qa='account-created']"
    CONTINUE_BUTTON = "[data-qa='continue-button']"

    def expect_account_created_visible(self) -> None:
        self.expect_visible(self.ACCOUNT_CREATED_HEADING)

    def click_continue(self) -> None:
        self.click(self.CONTINUE_BUTTON)
