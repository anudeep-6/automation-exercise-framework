"""
API tests for GET /api/productsList.

Covers four assertion layers:
  1. Transport layer   — HTTP status code
  2. Contract layer    — response shape via JSON Schema
  3. Application layer — responseCode in the JSON envelope
  4. Business logic    — products list is non-empty and items are well-shaped

"""

import allure
import pytest

from src.api.api_client import APIClient
from src.utils.schema_validator import validate
from tests.api.schemas.product_schema import PRODUCT_LIST_SCHEMA

PRODUCTS_ENDPOINT = "/productsList"


@allure.epic("API")
@allure.feature("Products API")
class TestProductsAPI:
    """Tests for the /api/productsList GET endpoint."""

    @allure.title("GET /api/productsList returns HTTP 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_products_http_status(self, api_client: APIClient) -> None:
        """
        Assert that the transport-level HTTP status code is 200.

        This is the first gate: if the server returns 4xx or 5xx,
        all downstream assertions are meaningless.
        """
        with allure.step("Send GET request to /api/productsList"):
            response = api_client.get(PRODUCTS_ENDPOINT)

        with allure.step("Assert HTTP status code is 200"):
            assert (
                response.status_code == 200
            ), f"Expected HTTP 200, got {response.status_code}"

    @allure.title("GET /api/productsList returns responseCode 200 in body")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_products_response_code_in_body(self, api_client: APIClient) -> None:
        """
        Assert the application-level responseCode in the JSON envelope is 200.

        The site wraps all API responses in {"responseCode": ..., ...}.
        This is distinct from the HTTP status code — an endpoint could
        return HTTP 200 with responseCode 500 in the body (misconfigured
        APIs do this). Both must be checked.
        """
        with allure.step("Send GET request to /api/productsList"):
            response = api_client.get(PRODUCTS_ENDPOINT)

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against PRODUCT_LIST_SCHEMA"):
            validate(body, PRODUCT_LIST_SCHEMA)

        with allure.step("Assert responseCode in body is 200"):
            assert (
                body["responseCode"] == 200
            ), f"Expected responseCode 200 in body, got {body['responseCode']}"

    @allure.title("GET /api/productsList returns a non-empty products list")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_products_list_not_empty(self, api_client: APIClient) -> None:
        """
        Assert that the products list in the response body is non-empty.

        An empty list is a business logic failure even if all status
        codes look healthy. This test would catch a silent data outage
        or a misconfigured filter on the server side.

        Schema validation runs before the length check — if the 'products'
        key is missing entirely, the schema failure names the missing field
        clearly instead of raising a KeyError on body["products"].
        """
        with allure.step("Send GET request to /api/productsList"):
            response = api_client.get(PRODUCTS_ENDPOINT)

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against PRODUCT_LIST_SCHEMA"):
            validate(body, PRODUCT_LIST_SCHEMA)

        with allure.step("Assert products list is non-empty"):
            assert (
                len(body["products"]) > 0
            ), "Products list is empty — expected at least one product"
