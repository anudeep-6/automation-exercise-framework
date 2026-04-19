"""This file contains the OrderConfirmationPage class."""

import os

import allure
from playwright.sync_api import Download

from src.pages.base_page import BasePage


class OrderConfirmationPage(BasePage):
    """Page object for the Order Confirmation page (/payment_done/<order_id>).

    Displayed after successful payment. Provides assertions for the
    order-placed heading, invoice download, and invoice content verification.
    """

    PATH = "/payment_done"

    ORDER_PLACED_HEADING = "[data-qa='order-placed']"
    CONTINUE_BUTTON = "[data-qa='continue-button']"
    DOWNLOAD_INVOICE_BUTTON = "a.check_out"
    EXPECTED_HEADING_TEXT = "Order Placed!"
    EXPECTED_CONFIRMATION_TEXT = "Congratulations! Your order has been confirmed!"
    CONFIRMATION_TEXT_LOCATOR = "section#form p"

    @allure.step("Expect 'Order Placed!' heading is visible")
    def expect_order_placed_visible(self) -> None:
        """Assert the 'Order Placed!' heading is visible on the page."""
        self.expect_visible(self.ORDER_PLACED_HEADING)

    @allure.step("Expect heading text: 'Order Placed!'")
    def expect_order_placed_text(self) -> None:
        """Assert the 'Order Placed!' heading has the correct text."""
        self.expect_text(self.ORDER_PLACED_HEADING, self.EXPECTED_HEADING_TEXT)

    @allure.step("Expect order confirmation message")
    def expect_confirmation_message(self) -> None:
        """Assert the confirmation paragraph text is correct."""
        self.expect_text(
            self.CONFIRMATION_TEXT_LOCATOR, self.EXPECTED_CONFIRMATION_TEXT
        )

    @allure.step("Download invoice and save to disk")
    def download_invoice(self, download_dir: str) -> str:
        """Click 'Download Invoice', wait for the download, and save it.

        Args:
            download_dir (str): Absolute path to the directory where the
                invoice file should be saved.

        Returns:
            str: Absolute path to the saved invoice file.
        """
        with self.page.expect_download() as download_info:
            self.click(self.DOWNLOAD_INVOICE_BUTTON)

        download: Download = download_info.value
        suggested_name = download.suggested_filename or "invoice.txt"
        save_path = os.path.join(download_dir, suggested_name)
        download.save_as(save_path)

        allure.attach.file(
            save_path,
            name="downloaded_invoice",
            attachment_type=allure.attachment_type.TEXT,
        )
        return save_path

    @allure.step("Verify invoice content for user '{username}'")
    def verify_invoice_content(
        self, invoice_path: str, username: str, amount: str
    ) -> None:
        """Read the downloaded invoice (.txt) and assert it contains expected content.

        The invoice format is:
            "Hi <username>, Your total purchase amount is <amount>. Thank you"

        Args:
            invoice_path (str): Absolute path to the downloaded invoice file.
            username (str): The account name expected in the invoice greeting.
            amount (str): Expected purchase amount string (e.g. "Rs. 1500").

        Raises:
            AssertionError: If any expected content is missing from the invoice.
        """

        with open(invoice_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        assert username.replace("_", " ").lower() in content.lower(), (
            f"Expected username '{username}' not found in invoice. "
            f"Actual content: '{content}'"
        )

        amount_value = amount.replace("Rs.", "").strip()
        assert f"purchase amount is {amount_value}".lower() in content.lower(), (
            f"Expected purchase amount '{amount_value}' not found in invoice. "
            f"Actual content: '{content}'"
        )

        assert "thank you" in content.lower(), (
            f"Expected 'Thank you' not found in invoice. "
            f"Actual content: '{content}'"
        )

    @allure.step("Click Continue button")
    def click_continue(self) -> None:
        """Click the Continue button to return to the home page."""
        self.click(self.CONTINUE_BUTTON)
