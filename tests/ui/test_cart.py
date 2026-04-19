"""
Cart management tests for AutomationExercise.

Verifies adding products to cart, product quantity management,
and removal of products from the cart.
"""

import allure
import pytest


@allure.epic("Shopping Cart")
@allure.feature("Cart Management")
class TestCart:
    """Covers add, quantity update, and remove flows for the cart."""

    @allure.story("Add products to cart")
    @allure.title("Add two products via hover overlay and verify cart contents")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_add_products_to_cart(
        self,
        home_page,
        products_page,
        cart_page,
    ) -> None:
        """
        GIVEN  the user is on the home page
        WHEN   two products are added to the cart via the hover overlay
        THEN   the cart page displays both products correctly
        """
        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to the Products page"):
            home_page.go_to_products()

        with allure.step("Add product 1 to cart and continue shopping"):
            products_page.hover_and_add_to_cart(1)
            products_page.click_continue_shopping()

        with allure.step("Add product 2 to cart and navigate to cart"):
            products_page.hover_and_add_to_cart(2)
            products_page.click_view_cart()

        with allure.step("Verify both products are present in the cart"):
            cart_page.validate_cart_products()

    @allure.story("Product quantity in cart")
    @allure.title("Set product quantity to 5 on detail page and verify in cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_verify_product_quantity_in_cart(
        self,
        home_page,
        products_page,
        cart_page,
    ) -> None:
        """
        GIVEN  the user is on the product detail page for product 1
        WHEN   the quantity is incremented by 4 steps (from default 1 → final 5)
        AND    the product is added to cart
        THEN   the cart shows quantity of 5 for that product
        """
        expected_quantity = 5

        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to the Products page and verify product list is visible"):
            home_page.go_to_products()
            products_page.expect_all_products_is_visible()

        with allure.step("Open detail page for product 1"):
            products_page.click_on_view_product(1)
            products_page.expect_product_details_are_visible()

        with allure.step(f"Set quantity to {expected_quantity} and add to cart"):
            products_page.set_quantity(quantity=expected_quantity)
            products_page.click_add_to_cart_button()
            products_page.click_view_cart()

        with allure.step(f"Verify cart shows quantity of {expected_quantity}"):
            cart_page.validate_cart_products()
            cart_page.validate_product_quantity(expected_quantity)

    @allure.story("Remove products from cart")
    @allure.title("Add three products then delete each and verify cart is empty")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_remove_products_from_cart(
        self,
        home_page,
        products_page,
        cart_page,
    ) -> None:
        """
        GIVEN  three products have been added to the cart
        WHEN   each product is deleted from the cart
        THEN   the cart is empty after all deletions
        """
        products_to_add = [1, 2, 3]

        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to the Products page"):
            home_page.go_to_products()

        with allure.step(f"Add products {products_to_add} to cart"):
            for i, product in enumerate(products_to_add):
                products_page.hover_and_add_to_cart(product)
                is_last = i == len(products_to_add) - 1
                if is_last:
                    products_page.click_view_cart()
                else:
                    products_page.click_continue_shopping()

        with allure.step("Verify all products are present in cart"):
            cart_page.validate_cart_products()

        with allure.step("Delete all products and verify cart is empty"):
            cart_page.delete_products_and_validate()
