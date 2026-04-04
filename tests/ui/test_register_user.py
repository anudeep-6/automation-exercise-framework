"""This file contains TestRegisterUser class"""

import allure


@allure.epic("User Management")
@allure.feature("Registration")
@allure.story("Register new user and delete account")
@allure.severity(allure.severity_level.CRITICAL)
class TestRegisterUser:
    """Test suite for user registration flow."""

    def test_register_new_user(
        self,
        home_page,
        login_page,
        registration_page,
        account_created_page,
        account_deleted_page,
        register_user_data,
    ):
        """Test Case 1: Register a new user and delete the account."""
        user = register_user_data

        home_page.navigate()
        home_page.expect_home_page_visible()
        home_page.go_to_signup_login()

        login_page.enter_signup_name(user["name"])
        login_page.enter_signup_email(user["email"])
        login_page.submit_signup()

        registration_page.expect_account_info_form_visible()

        registration_page.fill_account_info(
            title=user["title"],
            password=user["password"],
            day=user["dob_day"],
            month=user["dob_month"],
            year=user["dob_year"],
        )

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

        registration_page.submit_create_account()

        account_created_page.expect_account_created_visible()
        account_created_page.click_continue()

        home_page.expect_logged_in()
        assert home_page.get_logged_in_username() == user["name"]
        home_page.delete_account()

        account_deleted_page.expect_account_deleted_visible()
        account_deleted_page.click_continue()
