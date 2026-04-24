"""
Hybrid tests — API setup/teardown with UI verification.

Test 1 — Account lifecycle:
    POST /createAccount  →  login via UI  →  assert navbar  →  DELETE /api/deleteAccount

Test 2 — Product discovery:
    GET /productsList  →  pick first product  →  search in UI  →  assert result visible
"""

import allure
import pytest
from playwright.sync_api import Page

from src.api.api_client import APIClient
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.pages.product_page import ProductsPage
from src.utils.date_helper import DateHelper
from src.utils.fake_data import FakeData

ACCOUNT_ENDPOINT = "/createAccount"
DELETE_ENDPOINT = "/deleteAccount"
PRODUCTS_ENDPOINT = "/productsList"


@allure.epic("Hybrid")
@allure.feature("UI + API Combined")
class TestHybrid:
    """Hybrid tests that combine API and UI layers in a single test flow.

    Each test uses the API layer for setup and/or teardown and the UI layer
    for verification — exercising the contract between both surfaces on the
    same domain.
    """

    @allure.story("Account lifecycle")
    @allure.title("Create account via API, verify login in UI, delete via API")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.hybrid
    def test_account_lifecycle(
        self, page: Page, api_client: APIClient, base_url: str
    ) -> None:
        """Create a user via API, verify the logged-in navbar state in UI,
        then delete via API.

        API handles setup and teardown; the UI verifies only what the UI can
        confirm — that the authenticated session is reflected correctly in the
        navbar. Cleanup runs in a finally block so no accounts are orphaned on
        assertion failure.
        """
        fake = FakeData()
        first, last = fake.generate_full_name()
        address = fake.generate_address()
        dob = DateHelper.birth_date_parts(years_ago=25)

        user = {
            "name": f"{first} {last}",
            "email": fake.generate_email(),
            "password": fake.generate_password(),
            "title": "Mr",
            "birth_date": dob["day"],
            "birth_month": dob["month"],
            "birth_year": dob["year"],
            "firstname": first,
            "lastname": last,
            "company": "Test Corp",
            "address1": address["address1"],
            "address2": address["address2"],
            "country": "United States",
            "state": address["state"],
            "city": address["city"],
            "zipcode": address["zipcode"],
            "mobile_number": fake.generate_phone(),
        }

        with allure.step("[API] Create account via POST /createAccount"):
            response = api_client.post(ACCOUNT_ENDPOINT, data=user)
            assert (
                response.status_code == 200
            ), f"Expected 200, got {response.status_code}. Body: {response.text[:300]}"
            body = response.json()
            assert body.get("responseCode") == 201, (
                f"Expected responseCode 201, got {body.get('responseCode')}. "
                f"Message: {body.get('message')}"
            )

        try:
            with allure.step("[UI] Navigate to login page"):
                home_page = HomePage(page, base_url)
                home_page.navigate()
                home_page.go_to_signup_login()

            with allure.step("[UI] Login as newly created user"):
                login_page = LoginPage(page, base_url)
                login_page.login(user["email"], user["password"])

            with allure.step("[UI] Verify navbar shows correct username"):
                home_page.expect_logged_in(user["name"])

        finally:
            with allure.step("[API] Delete account via DELETE /deleteAccount"):
                cleanup = api_client.delete(
                    DELETE_ENDPOINT,
                    data={
                        "email": user["email"],
                        "password": user["password"],
                    },
                )
                assert cleanup.status_code == 200, (
                    f"Cleanup failed — account may be orphaned. "
                    f"Status: {cleanup.status_code}. Body: {cleanup.text[:300]}"
                )

    @allure.story("Product discovery")
    @allure.title("Fetch first product via API, verify it appears in UI search results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.hybrid
    def test_product_discovery(
        self, page: Page, api_client: APIClient, base_url: str
    ) -> None:
        """Fetch live product catalog via API and verify first product
        appears in UI search.

        Confirms the API and UI are in sync on product data — if the API lists
        a product, searching for it in the UI must surface at least one result.
        No teardown needed; the test is read-only on both layers.
        """
        with allure.step("[API] Fetch product catalog via GET /productsList"):
            response = api_client.get(PRODUCTS_ENDPOINT)
            assert (
                response.status_code == 200
            ), f"Expected 200, got {response.status_code}"
            body = response.json()
            assert (
                body.get("responseCode") == 200
            ), f"Expected responseCode 200, got {body.get('responseCode')}"
            products = body.get("products", [])
            assert (
                products
            ), "Product list is empty — cannot proceed with UI verification"

        with allure.step("[API] Extract first product name"):
            first_product_name = products[0]["name"]

        with allure.step(
            f"[UI] Search for '{first_product_name}' on the products page"
        ):
            home_page = HomePage(page, base_url)
            home_page.navigate()
            home_page.go_to_products()
            products_page = ProductsPage(page, base_url)
            products_page.search_product(first_product_name)

        with allure.step("[UI] Verify at least one search result is visible"):
            products_page.expect_searched_products_heading()
            products_page.verify_product_search_results(first_product_name)
