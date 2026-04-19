"""
Tests for user registration flows on automationexercise.com.

Coverage:
- Successful new user registration with full profile and account deletion
- Attempt to register with an already-existing email address (error validation)
"""

import allure
import pytest

from tests.ui.conftest import load_existing_users


@allure.epic("User Management")
@allure.feature("Registration")
class TestRegisterUser:
    """Covers registration, deletion, and duplicate-email error handling."""

    @allure.story("Register new user and delete account")
    @allure.title("Register new user and delete account")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_register_new_user(
        self,
        home_page,
        login_page,
        registration_page,
        account_created_page,
        account_deleted_page,
        register_user_data,
    ):
        """
        Given a valid set of registration details that do not yet exist in the system
        When the user completes the signup and account info forms and submits
        Then the account is created, the user is logged in, and the account can
             be deleted
        """
        user = register_user_data

        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to signup / login page"):
            home_page.go_to_signup_login()

        with allure.step("Enter name and email to initiate signup"):
            login_page.signup(user["name"], user["email"])

        with allure.step("Verify account info form is visible"):
            registration_page.expect_account_info_form_visible()

        with allure.step("Fill in account info (title, password, date of birth)"):
            registration_page.fill_account_info(
                title=user["title"],
                password=user["password"],
                day=user["dob_day"],
                month=user["dob_month"],
                year=user["dob_year"],
            )

        with allure.step("Fill in address and personal details"):
            registration_page.fill_address_info(
                first_name=user["first_name"],
                last_name=user["last_name"],
                address=user["address"],
                country=user["country"],
                state=user["state"],
                city=user["city"],
                zipcode=user["zipcode"],
                mobile=user["mobile"],
                company=user["company"],
                address2=user["address2"],
            )

        with allure.step("Submit account creation form"):
            registration_page.submit_create_account()

        with allure.step("Verify account created confirmation is visible"):
            account_created_page.expect_account_created_visible()

        with allure.step("Click Continue and verify home page shows logged-in state"):
            account_created_page.click_continue()
            home_page.expect_logged_in(user["name"])

        with allure.step("Delete the account"):
            home_page.delete_account()

        with allure.step("Verify account deleted confirmation and click Continue"):
            account_deleted_page.expect_account_deleted_visible()
            account_deleted_page.click_continue()

    @allure.story("Register with existing email")
    @allure.title("Register user with existing email shows error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("user_credentials", load_existing_users())
    def test_register_user_with_existing_mail(
        self,
        home_page,
        login_page,
        user_credentials,
    ):
        """
        Given a set of credentials that already exist in the system
        When the user attempts to register with that email address
        Then an error message is displayed indicating the email is already in use
        """
        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to signup / login page"):
            home_page.go_to_signup_login()

        with allure.step("Enter existing name and email to initiate signup"):
            login_page.signup(user_credentials["name"], user_credentials["username"])

        with allure.step("Verify signup error is displayed for duplicate email"):
            login_page.expect_signup_error_visible()
