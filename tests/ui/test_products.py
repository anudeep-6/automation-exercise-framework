"""
Product browsing and search flow tests for automationexercise.com.

Coverage:
- Product detail page visibility after navigating from the product listing
- Product search results display for a given search term
"""

import allure
import pytest


@allure.epic("Product Catalog")
@allure.feature("Products")
class TestProducts:
    """Tests covering product detail viewing and product search result flows."""

    @allure.story("Product details")
    @allure.title("View product details page for a listed product")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_product_details(
        self,
        home_page,
        products_page,
    ):
        """Verify clicking 'View Product' navigates to product details page.

        Given a user on the home page
        When they navigate to the products listing and click 'View Product' on
             the first item
        Then the product details page is displayed with all expected details
             visible
        """
        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to products page and verify all products are visible"):
            home_page.go_to_products()
            products_page.expect_all_products_is_visible()

        with allure.step("Click 'View Product' and verify product details are visible"):
            products_page.click_on_view_product(1)
            products_page.expect_product_details_are_visible()

    @allure.story("Product search")
    @allure.title("Search for products by keyword returns relevant results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_search_products(
        self,
        home_page,
        products_page,
    ):
        """Verify search displays searched products heading and results.

        Given a user on the home page
        When they navigate to the products page and search for 'shirts'
        Then the searched products heading is displayed and the results are
             shown
        """
        with allure.step("Navigate to home page and verify it is visible"):
            home_page.navigate()
            home_page.expect_home_page_visible()

        with allure.step("Go to products page and verify all products are visible"):
            home_page.go_to_products()
            products_page.expect_all_products_is_visible()

        with allure.step("Search for 'shirts' and verify searched products heading"):
            products_page.search_product("shirts")
            products_page.expect_searched_products_heading()

        with allure.step("Verify search results are displayed"):
            products_page.verify_product_search_results("shirts")
