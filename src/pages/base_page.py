"""Base class for all Page Object Model classes."""

import logging

import allure
from playwright.sync_api import Page, expect

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

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.url = f"{self.base_url}{self.PATH}"

    def navigate(self):
        """Navigates to this page's full URL."""
        with allure.step(f"Navigate to {self.url}"):
            logger.info(f"Navigating to: {self.url}")
            self.page.goto(self.url)

    def get_title(self):
        """Returns the current page title."""
        return self.page.title()

    def get_current_url(self):
        """Returns the current browser URL."""
        return self.page.url

    def click(self, locator: str):
        """Clicks an element identified by the given locator.

        Args:
            locator (str): Playwright locator string
        """
        with allure.step(f"Click: {locator}"):
            logger.debug(f"Clicking locator: {locator}")
            self.page.locator(locator).click()

    def fill(self, locator: str, value: str):
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

        Args:
            locator (str): Playwright locator string.
        """
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator: str) -> bool:
        """Returns True if element is visible on the page.

        Args:
            locator (str): Playwright locator string.
        """
        return self.page.locator(locator).is_visible()

    def expect_url_contains(self, fragment: str):
        """Asserts current URL contains the given fragment.

        Args:
            fragment (str): URL substring to check for.
        """
        with allure.step(f"Expect URL to contain: '{fragment}'"):
            expect(self.page).to_have_url(f".*{fragment}.*")

    def expect_visible(self, locator: str):
        """Asserts element is visible. Retries until timeout.

        Args:
            locator (str): Playwright locator string.
        """
        with allure.step(f"Expect visible: {locator}"):
            logger.debug(f"Asserting visibility of: {locator}")
            expect(self.page.locator(locator)).to_be_visible()

    def expect_text(self, locator: str, text: str):
        """Asserts element contains the expected text. Retries until timeout.

        Args:
            locator (str): Playwright locator string.
            text (str): Expected text content.
        """
        with allure.step(f"Expect text '{text}' in: {locator}"):
            logger.debug(f"Expected text '{text}' in: {locator}")
            expect(self.page.locator(locator)).to_have_text(text)

    def __str__(self):
        """Readable string for humans"""
        return f"{self.__class__.__name__}(url={self.url})"

    def __repr__(self):
        """Detailed string for debugging"""
        return f"{self.__class__.__name__}(url='{self.url}')"
