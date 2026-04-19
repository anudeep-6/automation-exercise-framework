"""This file contains the ProductsPage class"""

import allure

from src.pages.base_page import BasePage


@allure.feature("Products")
class ProductsPage(BasePage):
    """Page object for the Products Page (/products).

    Provides interactions for browsing products, viewing product details,
    searching, adding items to cart, and managing quantities.
    """

    PATH = "/products"

    ALL_PRODUCTS_HEADING = "h2:has-text('All Products')"
    VIEW_PRODUCT = "a[href='/product_details/{product_id}']"
    PRODUCT_NAME = ".product-information h2"
    PRODUCT_PRICE = ".product-information span span"
    PRODUCT_CATEGORY = ".product-information p:has-text('Category')"
    PRODUCT_AVAILABILITY = ".product-information p:has-text('Availability')"
    PRODUCT_CONDITION = ".product-information p:has-text('Condition')"
    PRODUCT_BRAND = ".product-information p:has-text('Brand')"
    PRODUCT_NAMES = ".productinfo p"
    PRODUCT_IMAGE = ".product-image-wrapper"
    SEARCH_BAR = "input[name='search']"
    SEARCH_BUTTON = "div.container button#submit_search"
    SEARCHED_PRODUCTS_HEADING = "h2.title.text-center:has-text('Searched Products')"
    ADD_TO_CART = ".add-to-cart:visible"
    CONTINUE_SHOPPING_BTN = "button:has-text('Continue Shopping')"
    VIEW_CART_BTN = "a:has-text('View Cart')"
    QUANTITY = "#quantity"
    ADD_TO_CART_BUTTON = "button:has-text('Add to cart')"

    @allure.step("Expect All Products heading is visible")
    def expect_all_products_is_visible(self):
        """Asserts the 'All Products' heading is visible on the page."""
        self.expect_visible(self.ALL_PRODUCTS_HEADING)

    @allure.step("Click View Product for product ID {product_id}")
    def click_on_view_product(self, product_id: int):
        """Clicks the view product link for a specific product.

        Args:
            product_id (int): Product ID to view details for.
        """
        self.click(self.VIEW_PRODUCT.format(product_id=product_id))

    @allure.step("Expect product name is visible")
    def expect_product_name_visible(self):
        """Asserts the product name is visible in the product details."""
        self.expect_visible(self.PRODUCT_NAME)

    @allure.step("Expect product category is visible")
    def expect_product_category_visible(self):
        """Asserts the product category is visible in the product details."""
        self.expect_visible(self.PRODUCT_CATEGORY)

    @allure.step("Expect product price is visible")
    def expect_product_price_visible(self):
        """Asserts the product price is visible in the product details."""
        self.expect_visible(self.PRODUCT_PRICE)

    @allure.step("Expect product availability is visible")
    def expect_product_availability_visible(self):
        """Asserts the product availability is visible in the product details."""
        self.expect_visible(self.PRODUCT_AVAILABILITY)

    @allure.step("Expect product condition is visible")
    def expect_product_condition_visible(self):
        """Asserts the product condition is visible in the product details."""
        self.expect_visible(self.PRODUCT_CONDITION)

    @allure.step("Expect product brand is visible")
    def expect_product_brand_visible(self):
        """Asserts the product brand is visible in the product details."""
        self.expect_visible(self.PRODUCT_BRAND)

    @allure.step("Expect all product details are visible")
    def expect_product_details_are_visible(self):
        """Asserts all product detail fields are visible.

        Checks: name, category, price, availability, condition, and brand.
        """
        self.expect_product_name_visible()
        self.expect_product_category_visible()
        self.expect_product_price_visible()
        self.expect_product_availability_visible()
        self.expect_product_condition_visible()
        self.expect_product_brand_visible()

    @allure.step("Search product with keyword: {keyword}")
    def search_product(self, keyword: str) -> None:
        """Types a keyword into the search input and submits the search.

        Args:
            keyword (str): Product search keyword.
        """
        self.fill(self.SEARCH_BAR, keyword)
        self.click(self.SEARCH_BUTTON)

    @allure.step("Get searched product names")
    def get_searched_product_names(self) -> list[str]:
        """Returns all visible product names on the search results page.

        Returns:
            list[str]: List of product name strings.
        """
        return self.get_all_text_contents(self.PRODUCT_NAMES)

    @allure.step("Expect searched products heading is visible")
    def expect_searched_products_heading(self) -> None:
        """Asserts the 'Searched Products' heading is visible."""
        self.expect_visible(self.SEARCHED_PRODUCTS_HEADING)

    @allure.step("Verify product search results for keyword: {keyword}")
    def verify_product_search_results(self, keyword: str) -> None:
        """Verifies that search results are visible and non-empty.

        Args:
            keyword (str): The search keyword used (also interpolated into
                the Allure step label above).

        Raises:
            AssertionError: If no products are found for the keyword.
        """
        product_names = self.get_searched_product_names()
        assert (
            len(product_names) > 0
        ), f"No products returned for search keyword: '{keyword}'"

    @allure.step("Hover and add to cart product ID {product_id}")
    def hover_and_add_to_cart(self, product_id: int):
        """Hovers over a product card and clicks its 'Add to cart' overlay.

        Args:
            product_id (int): 1-based product index to add to cart.
        """
        with allure.step(f"Hover over product {product_id}"):
            product = self.page.locator(self.PRODUCT_IMAGE).nth(product_id - 1)
            product.hover()
        with allure.step(f"Click 'Add to cart' for product {product_id}"):
            product.locator(self.ADD_TO_CART).first.click()

    @allure.step("Click Continue Shopping button")
    def click_continue_shopping(self):
        """Clicks the 'Continue Shopping' button to stay on products page."""
        self.click(self.CONTINUE_SHOPPING_BTN)

    @allure.step("Click View Cart button")
    def click_view_cart(self):
        """Clicks the 'View Cart' button to navigate to the cart page."""
        self.click(self.VIEW_CART_BTN)

    @allure.step("Set product quantity to {quantity}")
    def set_quantity(self, quantity: int) -> None:
        """Sets the product quantity field to an explicit value.

        Args:
            quantity (int): The exact quantity to set. Must be >= 1.

        Raises:
            ValueError: If the quantity is less than 1.
        """
        if quantity < 1:
            raise ValueError(f"Quantity must be >= 1, got {quantity}")
        self.page.locator(self.QUANTITY).fill(str(quantity))

    @allure.step("Click Add to Cart button")
    def click_add_to_cart_button(self):
        """Clicks the 'Add to cart' button on the product details page."""
        self.click(self.ADD_TO_CART_BUTTON)
