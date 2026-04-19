"""Tests for the end-to-end checkout flow including invoice download and validation."""

import allure
import pytest

from tests.ui.conftest import load_existing_users


@allure.epic("E-Commerce")
@allure.feature("Checkout")
class TestCheckout:
    """End-to-end tests covering the full purchase flow on AutomationExercise."""

    @allure.story("Full purchase flow")
    @allure.title("Checkout, place order, and download invoice")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("user_credentials", load_existing_users())
    def test_checkout_and_download_invoice_after_purchase(
        self,
        login_page,
        home_page,
        products_page,
        cart_page,
        checkout_page,
        payment_page,
        order_confirmation_page,
        user_credentials,
        load_product_test_data,
        load_payment_test_data,
    ):
        """Verifies the full checkout journey: login → add to cart → checkout →
        payment → order confirmation → invoice download and content validation.

        Args:
            login_page: Page object for the Login page.
            home_page: Page object for the Home page.
            products_page: Page object for the Products page.
            cart_page: Page object for the Shopping Cart page.
            checkout_page: Page object for the Checkout page.
            payment_page: Page object for the Payment page.
            order_confirmation_page: Page object for the Order Confirmation page.
            user_credentials: Parametrized row from users.csv containing
                              username, password, name, fullname,
                              city_state_zip, country, and phone.
            load_product_test_data: Dict loaded from product_test_data.json.
            load_payment_test_data: Dict loaded from payment_test_data.json.
        """
        user = user_credentials
        product_test_data = load_product_test_data
        payment_data = load_payment_test_data

        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to Sign In / Login page"):
            home_page.go_to_signup_login()

        with allure.step(f"Log in as {user['username']}"):
            login_page.expect_login_form_visible()
            login_page.login(user["username"], user["password"])

        with allure.step(f"Verify user '{user['name']}' is logged in"):
            home_page.expect_logged_in(user["name"])

        with allure.step("Navigate to Products page and add product to cart"):
            home_page.go_to_products()
            products_page.hover_and_add_to_cart(product_test_data["product_id"])
            products_page.click_view_cart()

        with allure.step("Verify cart contents and proceed to checkout"):
            cart_page.validate_cart_products()
            cart_page.click_proceed_to_checkout_button()

        with allure.step(
            "Verify checkout page, delivery/billing address, and order item"
        ):
            checkout_page.verify_page_loaded()
            checkout_page.verify_delivery_address(
                user["fullname"],
                user["city_state_zip"],
                user["country"],
                user["phone"],
            )
            checkout_page.verify_billing_address(
                user["fullname"],
                user["city_state_zip"],
                user["country"],
                user["phone"],
            )
            checkout_page.verify_order_item(
                product_test_data["product_id"],
                product_test_data["product_name"],
                product_test_data["product_price"],
                product_test_data["product_quantity"],
                product_test_data["product_total"],
            )
            checkout_page.verify_grand_total()

        with allure.step("Enter order comment and place order"):
            checkout_page.enter_comment(product_test_data["order_comment"])
            checkout_page.place_order()

        with allure.step("Fill in payment details and confirm"):
            payment_page.verify_page_loaded()
            payment_page.fill_and_confirm(
                payment_data["name_on_card"],
                payment_data["card_number"],
                payment_data["cvv"],
                payment_data["expiry_month"],
                payment_data["expiry_year"],
            )

        with allure.step("Verify order confirmation is displayed"):
            order_confirmation_page.expect_order_placed_visible()
            order_confirmation_page.expect_order_placed_text()
            order_confirmation_page.expect_confirmation_message()

        with allure.step("Download invoice and validate its content"):
            invoice_path = order_confirmation_page.download_invoice("downloads/")
            order_confirmation_page.verify_invoice_content(
                invoice_path,
                user["name"],
                product_test_data["product_total"],
            )

        with allure.step("Continue and verify return to home page"):
            order_confirmation_page.click_continue()
            home_page.expect_home_page_visible()
