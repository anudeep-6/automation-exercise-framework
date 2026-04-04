"""This file contains AccountDeletedPage class"""

from src.pages.base_page import BasePage


class AccountDeletedPage(BasePage):
    """Page object for the Account Deleted confirmation page (/delete_account).

    Displayed after successful account deletion. Provides assertion
    for the confirmation heading and navigation via the Continue button.
    """

    PATH = "/delete_account"

    # Locators
    ACCOUNT_DELETED_HEADING = "[data-qa='account-deleted']"
    CONTINUE_BUTTON = "[data-qa='continue-button']"

    def expect_account_deleted_visible(self) -> None:
        self.expect_visible(self.ACCOUNT_DELETED_HEADING)

    def click_continue(self) -> None:
        self.click(self.CONTINUE_BUTTON)
