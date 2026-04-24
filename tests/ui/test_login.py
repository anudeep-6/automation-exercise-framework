"""
Login flow tests for automationexercise.com.

Coverage:
- Valid login with correct credentials; verifies username display and logout
- Invalid login with empty email, invalid format, and wrong credentials
"""

import allure
import pytest

from src.utils.data_reader import DataReader

_reader = DataReader()


def _load_login_data(
    expected_result: str, include_name: bool = False
) -> tuple[list[tuple], list[str]]:
    """Load and shape login rows from login_data.json for parametrization.

    Reads the file once and returns both the parameter tuples and IDs together
    to avoid multiple reads at collection time.

    Args:
        expected_result (str): Filter value for the 'expected_result' key.
        include_name (bool): If True, returns (email, password, name) tuples.
            If False, returns (email, password, validation_type) tuples.

    Returns:
        tuple[list[tuple], list[str]]: Parameter tuples and matching IDs.
    """
    rows = _reader.load_json_rows(
        "login_data.json", filter_by={"expected_result": expected_result}
    )
    ids = [row["description"] for row in rows]
    if include_name:
        params = [(row["email"], row["password"], row["name"]) for row in rows]
    else:
        params = [
            (row["email"], row["password"], row.get("validation_type", ""))
            for row in rows
        ]
    return params, ids


_VALID_PARAMS, _VALID_IDS = _load_login_data("success", include_name=True)
_INVALID_PARAMS, _INVALID_IDS = _load_login_data("failure")


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
    @pytest.mark.parametrize("username, password, name", _VALID_PARAMS, ids=_VALID_IDS)
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
        "username, password, validation_type", _INVALID_PARAMS, ids=_INVALID_IDS
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
