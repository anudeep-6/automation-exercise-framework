"""
Verification tests for Authentication State Management.

Confirms that the auth_page fixture delivers a pre-authenticated session —
tests navigate directly to protected areas without executing any login steps.
"""

import re

import allure
import pytest
from playwright.sync_api import Page, expect


@allure.epic("Authentication")
@allure.feature("Storage State")
class TestAuthState:
    """Verifies that saved storage state bypasses the login flow."""

    @allure.story("Reuse saved auth state")
    @allure.title("auth_page fixture starts session in logged-in state")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_auth_page_is_logged_in(self, auth_page: Page, base_url: str) -> None:
        """
        GIVEN  auth/state.json contains a valid session
        WHEN   a new page is opened using the auth_page fixture
        THEN   navigating to the home page shows the logout nav link
        AND    the 'Logged in as' label is visible — confirming no redirect to login
        """
        with allure.step("Navigate to home page using pre-authenticated context"):
            auth_page.goto(f"{base_url}/")

        with allure.step("Assert logout link is visible in nav bar"):
            expect(auth_page.locator("a[href='/logout']")).to_be_visible(timeout=10_000)

        with allure.step("Assert 'Logged in as <username>' label is visible in nav"):
            # Use a pattern to confirm a username is actually appended after the label.
            expect(
                auth_page.locator(
                    "ul.nav li a", has_text=re.compile(r"Logged in as .+")
                )
            ).to_be_visible(timeout=10_000)

    @allure.story("Reuse saved auth state")
    @allure.title("auth_page fixture never visits the login page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_page_not_visited(self, auth_page: Page, base_url: str) -> None:
        """
        GIVEN  auth/state.json contains a valid session
        WHEN   the home page is opened using the auth_page fixture
        THEN   the login form is not present on the page,
               confirming the session loaded directly without a login redirect.
        """
        with allure.step("Navigate to home page using pre-authenticated context"):
            auth_page.goto(f"{base_url}/")

        with allure.step("Assert login email input is not visible on the page"):
            expect(auth_page.locator("input[data-qa='login-email']")).not_to_be_visible(
                timeout=10_000
            )
