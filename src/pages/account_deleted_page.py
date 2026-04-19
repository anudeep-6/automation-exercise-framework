"""This file contains AccountDeletedPage class"""

import allure

from src.pages.base_page import BasePage


class AccountDeletedPage(BasePage):
    """Page object for the Account Deleted confirmation page (/delete_account).

    Displayed after successful account deletion. Provides assertion
    for the confirmation heading and navigation via the Continue button.
    """

    PATH = "/delete_account"

    ACCOUNT_DELETED_HEADING = "[data-qa='account-deleted']"
    CONTINUE_BUTTON = "[data-qa='continue-button']"

    @allure.step("Expect account deleted heading is visible")
    def expect_account_deleted_visible(self) -> None:
        """Asserts the account deleted confirmation heading is visible."""
        self.expect_visible(self.ACCOUNT_DELETED_HEADING)

    @allure.step("Click Continue button")
    def click_continue(self) -> None:
        """Clicks the Continue button on the account deletion confirmation page."""
        self.click(self.CONTINUE_BUTTON)
