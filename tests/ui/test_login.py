"""
Login flow tests for automationexercise.com.

Coverage:
- Valid login with correct credentials; verifies username display and logout
- Invalid login with empty email, invalid format, and wrong credentials
"""

import allure
import pytest

from src.utils.data_reader import DataReader


def load_users(expected_result: str, include_name: bool = False) -> list[tuple]:
    """Load and shape user rows from users_test_data.csv for login parametrization.

    Args:
        expected_result (str): Value to filter the 'expected_result' column by.
            Typically "success" for valid credentials or "failure" for invalid.
        include_name (bool): If True, returns (username, password, name) tuples
            for tests that validate the logged-in username display.
            If False, returns (username, password, validation_type) tuples
            for tests that validate error messages. Defaults to False.

    Returns:
        list[tuple]: List of tuples shaped for login parametrization.
    """
    reader = DataReader()
    rows = reader.load_csv_rows(
        "users_test_data.csv", filter_by={"expected_result": expected_result}
    )

    if include_name:
        return [(row["username"], row["password"], row["name"]) for row in rows]

    return [
        (row["username"], row["password"], row.get("validation_type", ""))
        for row in rows
    ]


@allure.epic("User Management")
@allure.feature("Login")
class TestLogin:
    """Tests covering valid credential login with username verification and
    invalid credential rejection flows."""

    @allure.story("Valid login")
    @allure.title("Valid login - {username}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "username, password, name", load_users("success", include_name=True)
    )
    def test_valid_login(
        self,
        username,
        password,
        name,
        home_page,
        login_page,
    ):
        """Verify that a registered user can log in and is shown the correct username.

        Given a registered user with valid credentials
        When the user navigates to the login page and submits their credentials
        Then they are redirected to the home page, username is displayed in the
             header, and after logout they are returned to the login form
        """
        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to signup/login page and verify login form is visible"):
            home_page.go_to_signup_login()
            login_page.expect_login_form_visible()

        with allure.step(f"Log in as {username}"):
            login_page.login(username, password)

        with allure.step("Verify logged-in state and username display"):
            home_page.expect_logged_in(name)

        with allure.step("Log out and verify login form is visible"):
            home_page.logout()
            login_page.expect_login_form_visible()

    @allure.story("Invalid login")
    @allure.title("Invalid login - {username}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "username, password, validation_type", load_users("failure")
    )
    def test_invalid_login(
        self,
        username,
        password,
        validation_type,
        home_page,
        login_page,
    ):
        """Verify login with invalid credentials shows validation error.

        Given a user with invalid or malformed credentials
        When the user navigates to the login page and submits those credentials
        Then the appropriate validation error is displayed based on the
             validation type
        """
        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to signup/login page and verify login form is visible"):
            home_page.go_to_signup_login()
            login_page.expect_login_form_visible()

        with allure.step(f"Submit invalid credentials for {username}"):
            login_page.login(username, password)

        with allure.step(f"Verify validation error for type: '{validation_type}'"):
            if validation_type == "empty_email":
                login_page.expect_empty_email_validation()
            elif validation_type == "invalid_format":
                login_page.expect_invalid_email_format_validation()
            else:
                login_page.expect_login_error_visible()
