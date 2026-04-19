"""
Contact Us form tests for AutomationExercise.

Verifies that a user can navigate to the Contact Us page,
submit the enquiry form with a file attachment, and receive
a success confirmation before returning to the home page.
"""

import allure
import pytest


@allure.epic("Customer Support")
@allure.feature("Contact Us")
class TestContactUs:
    """Covers the Contact Us form submission flow."""

    @allure.story("Submit enquiry form")
    @allure.title("Fill and submit Contact Us form and verify success message")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_contact_us(
        self,
        home_page,
        contact_us_page,
        load_contact_data,
    ):
        """
        GIVEN  the user is on the home page
        WHEN   the Contact Us form is filled and submitted with a file attachment
        THEN   a success message is displayed and the user can return to the home page
        """
        form_data = load_contact_data

        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Navigate to the Contact Us page"):
            home_page.go_to_contact_us()

        with allure.step("Verify the Get In Touch form is visible"):
            contact_us_page.expect_get_in_touch_form_visible()

        with allure.step("Fill in the Contact Us form with test data"):
            contact_us_page.fill_contact_us_form(
                form_data["name"],
                form_data["email"],
                form_data["subject"],
                form_data["message"],
                form_data["upload_file"],
            )

        with allure.step("Submit the form and accept the confirmation dialog"):
            contact_us_page.submit_and_accept_dialog()

        with allure.step("Verify success message is displayed"):
            contact_us_page.expect_success_message_visible()

        with allure.step("Click Home button and verify return to home page"):
            contact_us_page.click_home_button()
            home_page.expect_home_page_visible()
