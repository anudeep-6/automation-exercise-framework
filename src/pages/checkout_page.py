"""Page object for the Checkout page."""

import allure

from src.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for checkout — address review, order summary, and place order."""

    PATH = "/checkout"

    DELIVERY_ADDRESS_BLOCK = "ul#address_delivery"
    BILLING_ADDRESS_BLOCK = "ul#address_invoice"
    DELIVERY_FULLNAME = "ul#address_delivery li.address_firstname"
    DELIVERY_STREET = "ul#address_delivery li.address_address1:nth-child(3)"
    DELIVERY_CITY_STATE_ZIP = "ul#address_delivery li.address_city"
    DELIVERY_COUNTRY = "ul#address_delivery li.address_country_name"
    DELIVERY_PHONE = "ul#address_delivery li.address_phone"
    BILLING_FULLNAME = "ul#address_invoice li.address_firstname"
    BILLING_CITY_STATE_ZIP = "ul#address_invoice li.address_city"
    BILLING_COUNTRY = "ul#address_invoice li.address_country_name"
    BILLING_PHONE = "ul#address_invoice li.address_phone"
    ORDER_TABLE = "table.table"
    PRODUCT_ROW = "tr#product-{product_id}"
    PRODUCT_NAME = "tr#product-{product_id} td.cart_description h4 a"
    PRODUCT_PRICE = "tr#product-{product_id} td.cart_price p"
    PRODUCT_QUANTITY = "tr#product-{product_id} td.cart_quantity button"
    PRODUCT_TOTAL = "tr#product-{product_id} td.cart_total p.cart_total_price"
    GRAND_TOTAL = "tr:has(td:has-text('Total Amount')) td p.cart_total_price"
    COMMENT_TEXTAREA = "textarea[name='message']"
    PLACE_ORDER_BTN = "a.check_out"

    @allure.step("Verify checkout page is loaded")
    def verify_page_loaded(self) -> None:
        """Assert both address blocks and order table are visible."""
        self.expect_visible(self.DELIVERY_ADDRESS_BLOCK)
        self.expect_visible(self.BILLING_ADDRESS_BLOCK)
        self.expect_visible(self.ORDER_TABLE)

    @allure.step("Verify delivery address for {fullname}")
    def verify_delivery_address(
        self, fullname: str, city_state_zip: str, country: str, phone: str
    ) -> None:
        """Assert all visible fields in the delivery address block.

        Args:
            fullname: Expected name text e.g. 'Mr. test demo user'.
            city_state_zip: Expected city/state/postcode e.g.
                'Bangalore Karnataka 506034'.
            country: Expected country name e.g. 'India'.
            phone: Expected phone number string.
        """
        self.expect_contains_text(self.DELIVERY_FULLNAME, fullname)
        self.expect_contains_text(self.DELIVERY_CITY_STATE_ZIP, city_state_zip)
        self.expect_contains_text(self.DELIVERY_COUNTRY, country)
        self.expect_contains_text(self.DELIVERY_PHONE, phone)

    @allure.step("Verify billing address for {fullname}")
    def verify_billing_address(
        self, fullname: str, city_state_zip: str, country: str, phone: str
    ) -> None:
        """Assert all visible fields in the billing address block.

        Args:
            fullname: Expected name text.
            city_state_zip: Expected city/state/postcode string.
            country: Expected country name.
            phone: Expected phone number string.
        """
        self.expect_contains_text(self.BILLING_FULLNAME, fullname)
        self.expect_contains_text(self.BILLING_CITY_STATE_ZIP, city_state_zip)
        self.expect_contains_text(self.BILLING_COUNTRY, country)
        self.expect_contains_text(self.BILLING_PHONE, phone)

    @allure.step("Verify order item for product {product_id}")
    def verify_order_item(
        self,
        product_id: int,
        name: str,
        price: str,
        quantity: int,
        total: str,
    ) -> None:
        """Assert all columns for a single product row in the order summary table.

        Asserts row presence first, then validates each column value. Fails with
        a clear message if the product row is missing entirely.

        Args:
            product_id: Numeric ID matching tr#product-{id} in the DOM.
            name: Expected product name e.g. 'Blue Top'.
            price: Expected price string e.g. 'Rs. 500'.
            quantity: Expected quantity count e.g. 1.
            total: Expected line total string e.g. 'Rs. 500'.
        """
        self.expect_visible(self.PRODUCT_ROW.format(product_id=product_id))
        self.expect_contains_text(self.PRODUCT_NAME.format(product_id=product_id), name)
        self.expect_contains_text(
            self.PRODUCT_PRICE.format(product_id=product_id), price
        )
        self.expect_contains_text(
            self.PRODUCT_QUANTITY.format(product_id=product_id), str(quantity)
        )
        self.expect_contains_text(
            self.PRODUCT_TOTAL.format(product_id=product_id), total
        )

    @allure.step("Verify grand total is visible")
    def verify_grand_total(self) -> None:
        """Assert the grand total cell is visible in the order summary."""
        self.expect_visible(self.GRAND_TOTAL)

    @allure.step("Enter order comment")
    def enter_comment(self, comment: str) -> None:
        """Type an optional order comment into the message textarea.

        Args:
            comment: Text to enter in the comment box.
        """
        self.fill(self.COMMENT_TEXTAREA, comment)

    @allure.step("Click Place Order")
    def place_order(self) -> None:
        """Click Place Order to proceed to the payment page."""
        self.click(self.PLACE_ORDER_BTN)
