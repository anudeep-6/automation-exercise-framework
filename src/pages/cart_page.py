"""This file contains the CartPage class"""

import allure

from src.pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for the Cart Page (/view_cart).

    Provides interactions for viewing cart contents, validating products,
    deleting items, and proceeding to checkout.
    """

    PATH = "/view_cart"

    CART_MENU = ".cart_menu"
    DESCRIPTION = ".cart_description"
    PRICE = ".cart_price p"
    QUANTITY = ".cart_quantity button"
    TOTAL_PRICE = ".cart_total_price"
    DELETE_BUTTON = ".cart_quantity_delete"
    PRODUCT_ROWS = "tbody tr"
    PRODUCT_ID = "[data-product-id='{product_id}']"
    EMPTY_CART = "b:has-text('Cart is empty!')"
    CHECKOUT_BUTTON = "a.btn.btn-default.check_out"

    @allure.step("Validate cart products are visible")
    def validate_cart_products(self) -> None:
        """Assert cart contains products and all product columns are visible."""
        product_rows = self.page.locator(self.PRODUCT_ROWS)
        products_count = product_rows.count()

        assert products_count > 0, "Cart is empty"

        for i in range(products_count):
            row = product_rows.nth(i)
            self.expect_locator_visible(row.locator(self.DESCRIPTION))
            self.expect_locator_visible(row.locator(self.PRICE))
            self.expect_locator_visible(row.locator(self.QUANTITY))
            self.expect_locator_visible(row.locator(self.TOTAL_PRICE))

    @allure.step("Validate product quantity is {expected_quantity}")
    def validate_product_quantity(self, expected_quantity: int) -> None:
        """Assert the quantity button displays the expected quantity value.

        Args:
            expected_quantity (int): Expected quantity value.
        """
        quantity = self.get_text(self.QUANTITY)
        assert (
            int(quantity) == expected_quantity
        ), f"Quantity mismatch, expected {expected_quantity} got {quantity}"

    @allure.step("Delete products from cart")
    def delete_products_and_validate(self, product_id: int | None = None) -> None:
        """Delete product(s) from the cart and validate removal.

        Args:
            product_id (int | None): Product ID to delete a specific product.
                                     If None, deletes all products from cart.
        """
        if product_id:
            product = self.PRODUCT_ID.format(product_id=product_id)
            self.click(product)
            self.page.locator(product).wait_for(state="detached")
        else:
            delete_buttons = self.page.locator(self.DELETE_BUTTON)

            while delete_buttons.count() > 0:
                prev_count = delete_buttons.count()
                delete_buttons.first.click()

                self.page.wait_for_function(
                    "(args) => document.querySelectorAll(args.selector).length "
                    "< args.prevCount",
                    arg={"selector": self.DELETE_BUTTON, "prevCount": prev_count},
                )

            self.expect_visible(self.EMPTY_CART)

    @allure.step("Click Proceed to Checkout button")
    def click_proceed_to_checkout_button(self) -> None:
        """Clicks the Proceed to Checkout button."""
        self.click(self.CHECKOUT_BUTTON)
