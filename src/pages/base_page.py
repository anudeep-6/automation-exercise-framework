"""Base class for all Page Object Model classes."""

import logging
import os
import re

import allure
from playwright.sync_api import Locator, Page, expect

from src.utils.config_reader import ConfigReader

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects.

    Provides common Playwright interactions and Allure step wrappers.
    All page classes inherit from this and define their own PATH constant.

    Args:
        page (Page): Playwright Page object injected via pytest fixture.
        base_url (str): Base URL from ConfigReader, injected via pytest fixture.
    """

    PATH = ""

    timeout: int

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.url = f"{self.base_url}{self.PATH}"
        self.timeout = ConfigReader().get("default_timeout", 30000)

    def navigate(self) -> None:
        """Navigates to this page's full URL."""
        with allure.step(f"Navigate to {self.url}"):
            logger.info(f"Navigating to: {self.url}")
            self.page.goto(self.url)

    def get_title(self) -> str:
        """Returns the current page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Returns the current browser URL."""
        return self.page.url

    def click(self, locator: str) -> None:
        """Clicks an element identified by the given locator.

        Args:
            locator (str): Playwright locator string.
        """
        with allure.step(f"Click: {locator}"):
            logger.debug(f"Clicking locator: {locator}")
            self.page.locator(locator).click()

    def fill(self, locator: str, value: str) -> None:
        """Clears and fills an input field.

        Args:
            locator (str): Playwright locator string.
            value (str): Text to enter.
        """
        with allure.step(f"Fill '{locator}' with '{value}'"):
            logger.debug(f"Filling '{locator}' with value (length={len(value)})")
            self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:
        """Returns visible text content of an element.

        Uses inner_text() which respects CSS visibility — hidden elements
        (e.g. display:none) are excluded from the result.

        Args:
            locator (str): Playwright locator string.
        """
        return self.page.locator(locator).inner_text()

    def get_text_content(self, locator: str) -> str:
        """Returns raw text content of an element including hidden text.

        Uses text_content() which does NOT respect CSS visibility — text inside
        elements with display:none is included. Prefer get_text() for visible
        text assertions; use this only when hidden text must be read.

        Args:
            locator (str): Playwright locator string.
        """
        return self.page.locator(locator).text_content()

    def get_all_text_contents(self, locator: str) -> list[str]:
        """Returns text content of all matching elements.

        Waits for the first matching element to be visible before collecting.

        Args:
            locator (str): Playwright locator string.
        """
        self.page.locator(locator).first.wait_for(state="visible")
        return self.page.locator(locator).all_text_contents()

    def is_visible(self, locator: str) -> bool:
        """Returns True if element is visible on the page.

        Args:
            locator (str): Playwright locator string.
        """
        return self.page.locator(locator).is_visible()

    def expect_url_contains(self, fragment: str) -> None:
        """Asserts current URL contains the given fragment.

        Args:
            fragment (str): URL substring to check for.
        """
        with allure.step(f"Expect URL to contain: '{fragment}'"):
            expect(self.page).to_have_url(re.compile(f".*{fragment}.*"))

    def expect_visible(self, locator: str) -> None:
        """Asserts element is visible. Retries until timeout.

        Args:
            locator (str): Playwright locator string.
        """
        with allure.step(f"Expect visible: {locator}"):
            logger.debug(f"Asserting visibility of: {locator}")
            expect(self.page.locator(locator)).to_be_visible()

    def expect_locator_visible(self, locator: Locator) -> None:
        """Asserts a pre-built Locator is visible. Retries until timeout.

        Use this when you already hold a Locator object (e.g. a chained locator).
        For plain selector strings, prefer :meth:`expect_visible` instead.

        Args:
            locator (Locator): Playwright Locator object to assert visibility on.
        """
        with allure.step(f"Expect visible: {locator}"):
            logger.debug(f"Asserting visibility of locator: {locator}")
            expect(locator).to_be_visible()

    def expect_text(self, locator: str, text: str) -> None:
        """Asserts element has exactly the expected text. Retries until timeout.

        Args:
            locator (str): Playwright locator string.
            text (str): Expected text content.
        """
        with allure.step(f"Expect text '{text}' in: {locator}"):
            logger.debug(f"Expected text '{text}' in: {locator}")
            expect(self.page.locator(locator)).to_have_text(text)

    def expect_contains_text(self, locator: str, text: str) -> None:
        """Asserts element contains the expected text (partial match).

        Retries until timeout.

        Args:
            locator (str): Playwright locator string.
            text (str): Expected partial text content.
        """
        with allure.step(f"Expect '{locator}' to contain text: '{text}'"):
            logger.debug(f"Asserting '{locator}' contains text: '{text}'")
            expect(self.page.locator(locator)).to_contain_text(text)

    def upload_file(self, selector: str, file_path: str) -> None:
        """Upload a file using a file input element.

        The file must exist at the given path before this method is called.

        Args:
            selector (str): Playwright locator pointing to the file input element.
            file_path (str): Absolute or relative path to the file to upload.

        Raises:
            FileNotFoundError: If the file does not exist at the given path.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Upload file not found at path: {file_path}")
        self.page.locator(selector).set_input_files(file_path)

    def accept_dialog(self) -> list[str]:
        """Registers a one-time accept handler for the next browser dialog.

        Returns a mutable list that will be populated with the dialog message
        AFTER the action that triggers the dialog is called. The handler must
        be registered before the triggering action — Playwright auto-dismisses
        dialogs that have no handler at the time they appear.

        Returns:
            list[str]: A list that will contain the dialog message text once
                the dialog is triggered and accepted. Read index [0] after
                the triggering action.
        """
        dialog_message: list[str] = []

        def handler(dialog):
            dialog_message.append(dialog.message)
            dialog.accept()

        self.page.once("dialog", handler)
        return dialog_message

    def hover(self, locator: str) -> None:
        """Hover over an element identified by the given locator.

        Args:
            locator (str): Playwright locator string.
        """
        with allure.step(f"Hover: {locator}"):
            logger.debug(f"Hovering over locator: {locator}")
            self.page.locator(locator).hover()

    def select_option(self, locator: str, value: str) -> None:
        """Selects an option from a <select> dropdown by value.

        Args:
            locator (str): Playwright locator string pointing to the <select> element.
            value (str): The option value to select (matches the 'value' attribute).
        """
        with allure.step(f"Select option '{value}' in: {locator}"):
            logger.debug(f"Selecting option '{value}' in: {locator}")
            self.page.locator(locator).select_option(value)

    def is_checked(self, locator: str) -> bool:
        """Returns True if a checkbox or radio input is currently checked.

        Args:
            locator (str): Playwright locator string pointing to the input element.
        """
        return self.page.locator(locator).is_checked()

    def __str__(self) -> str:
        """Readable string for humans."""
        return f"{self.__class__.__name__}(url={self.url})"

    def __repr__(self) -> str:
        """Detailed string for debugging."""
        return f"{self.__class__.__name__}(url='{self.url}')"
