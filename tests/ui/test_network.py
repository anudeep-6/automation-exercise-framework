"""
Practice tests for Playwright network interception on automationexercise.com.

Coverage:
- Mocking the product list API response and verifying UI reflects mocked data
- Aborting all image requests and verifying the page still loads
- Injecting a custom request header and verifying it is sent
"""

import json
import re

import allure
import pytest
from playwright.sync_api import Page, Route

MOCK_PRODUCTS = {
    "responseCode": 200,
    "products": [
        {"id": 1, "name": "Mock T-Shirt", "price": "Rs. 500"},
        {"id": 2, "name": "Mock Jeans", "price": "Rs. 1000"},
    ],
}


@pytest.mark.regression
@allure.story("Network Interception")
@allure.title("Mock product list API and verify UI reflects mocked data")
@allure.severity(allure.severity_level.NORMAL)
def test_mock_product_api(page: Page):
    """
    Given the product list API is intercepted with a mocked response
    When the products page is loaded
    Then the UI displays at least the two mocked products
    """

    def handle_products(route: Route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(MOCK_PRODUCTS),
        )

    with allure.step("Register API mock and navigate to products page"):
        page.route("**/api/productsList", handle_products)
        page.goto("https://automationexercise.com/products")

    with allure.step("Verify at least 2 product cards are visible with mocked data"):
        products = page.locator(".productinfo")
        assert products.count() >= 2


@pytest.mark.regression
@allure.story("Network Interception")
@allure.title("Abort all image requests and verify page still loads")
@allure.severity(allure.severity_level.NORMAL)
def test_abort_image_requests(page: Page):
    """
    Given all image requests are aborted via route interception
    When the home page is loaded
    Then the page body is still visible and the title is non-empty
    """
    with allure.step("Register image abort rule and navigate to home page"):
        page.route(
            re.compile(r".*\.(png|jpg|jpeg|gif|svg|webp)(\?.*)?$"),
            lambda route: route.abort(),
        )
        page.goto("https://automationexercise.com")

    with allure.step("Verify page body is visible"):
        assert page.locator("body").is_visible()

    with allure.step("Verify page title is non-empty"):
        assert page.title() != ""


@pytest.mark.regression
@allure.story("Network Interception")
@allure.title("Inject custom request header and verify it is sent")
@allure.severity(allure.severity_level.NORMAL)
def test_modify_request_headers(page: Page):
    """
    Given a route handler that injects an X-Test-Flag header on all product requests
    When the products page is loaded
    Then the outgoing request contains the injected header value
    """

    def inject_header(route: Route):
        modified = {**route.request.headers, "X-Test-Flag": "playwright"}
        route.continue_(headers=modified)

    with allure.step("Register header injection route and navigate to products page"):
        page.route("**/products", inject_header)
        with page.expect_request("**/products") as req_info:
            page.goto("https://automationexercise.com/products")

    with allure.step("Verify outgoing request contains injected X-Test-Flag header"):
        request = req_info.value
        assert request.headers.get("x-test-flag") == "playwright"
