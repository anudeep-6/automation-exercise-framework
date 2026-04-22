"""
API tests for account CRUD lifecycle.

Covers four assertion layers on each endpoint:
  1. Transport layer   — HTTP status code
  2. Contract layer    — response shape via JSON Schema
  3. Application layer — responseCode in the JSON envelope
  4. Business logic    — message confirms the expected operation

Test order: create → verify → update → delete (chained test proves
the full lifecycle with a single dynamically-generated account).
"""

import uuid

import allure
import pytest

from src.api.api_client import APIClient
from src.utils.schema_validator import validate
from tests.api.schemas.account_schema import (
    ACCOUNT_DETAIL_SCHEMA,
    SIMPLE_RESPONSE_SCHEMA,
)

CREATE_ENDPOINT = "/createAccount"
VERIFY_ENDPOINT = "/verifyLogin"
UPDATE_ENDPOINT = "/updateAccount"
DELETE_ENDPOINT = "/deleteAccount"


def _unique_email() -> str:
    """
    Generate a collision-safe email for each test run.

    Using uuid4 guarantees uniqueness across parallel workers and
    re-runs without needing a shared counter or database.
    """
    return f"testuser_{uuid.uuid4().hex[:8]}@qatest.com"


def _base_payload(email: str, password: str) -> dict:
    """
    Minimal valid payload accepted by createAccount / updateAccount.

    All fields are required by the API.  Title, country, and DOB values
    are fixed strings — the goal is lifecycle correctness, not data variety.
    """
    return {
        "name": "QA Test User",
        "email": email,
        "password": password,
        "title": "Mr",
        "birth_date": "15",
        "birth_month": "6",
        "birth_year": "1990",
        "firstname": "QA",
        "lastname": "Tester",
        "company": "TestCorp",
        "address1": "123 Test Street",
        "address2": "Suite 4",
        "country": "United States",
        "zipcode": "10001",
        "state": "New York",
        "city": "New York",
        "mobile_number": "5550001234",
    }


@allure.epic("API")
@allure.feature("Account API")
class TestAccountAPI:
    """
    Tests for the account CRUD endpoints.

    Each test in this class is self-contained: it creates (and cleans up)
    its own account so tests can run in any order without shared state.
    The chained test at the bottom exercises the full lifecycle explicitly.
    """

    @allure.title("POST /api/createAccount returns HTTP 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_account_http_status(self, api_client: APIClient) -> None:
        """
        Assert the transport-level HTTP status code is 200.

        This is the first gate — if the server returns 4xx/5xx,
        no downstream assertions are meaningful.
        """
        email = _unique_email()
        password = "Test@1234"
        payload = _base_payload(email, password)

        with allure.step("POST to /api/createAccount"):
            response = api_client.post(CREATE_ENDPOINT, data=payload)

        with allure.step("Assert HTTP status code is 200"):
            assert (
                response.status_code == 200
            ), f"Expected HTTP 200, got {response.status_code}"

        with allure.step("Cleanup: delete the created account"):
            api_client.delete(
                DELETE_ENDPOINT, data={"email": email, "password": password}
            )

    @allure.title("POST /api/createAccount returns responseCode 201 in body")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_account_response_code_in_body(self, api_client: APIClient) -> None:
        """
        Assert the application-level responseCode in the JSON envelope is 201.

        The site always returns HTTP 200 at the transport layer.
        The real outcome — 201 Created vs 400 Bad Request — lives in
        body["responseCode"].  Both layers must be checked independently.
        """
        email = _unique_email()
        password = "Test@1234"
        payload = _base_payload(email, password)

        with allure.step("POST to /api/createAccount"):
            response = api_client.post(CREATE_ENDPOINT, data=payload)

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against SIMPLE_RESPONSE_SCHEMA"):
            validate(body, SIMPLE_RESPONSE_SCHEMA)

        with allure.step("Assert responseCode in body is 201"):
            assert (
                body["responseCode"] == 201
            ), f"Expected responseCode 201, got {body['responseCode']}"

        with allure.step("Cleanup: delete the created account"):
            api_client.delete(
                DELETE_ENDPOINT, data={"email": email, "password": password}
            )

    @allure.title("POST /api/createAccount message confirms user created")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_account_message(self, api_client: APIClient) -> None:
        """
        Assert the response message confirms account creation.

        Checking the human-readable message alongside the responseCode
        catches cases where the code is correct but the operation
        silently diverged (e.g., partial write, wrong record created).
        """
        email = _unique_email()
        password = "Test@1234"
        payload = _base_payload(email, password)

        with allure.step("POST to /api/createAccount"):
            response = api_client.post(CREATE_ENDPOINT, data=payload)

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against SIMPLE_RESPONSE_SCHEMA"):
            validate(body, SIMPLE_RESPONSE_SCHEMA)

        with allure.step("Assert message contains 'User created'"):
            assert (
                "User created" in body["message"]
            ), f"Unexpected message: {body['message']}"

        with allure.step("Cleanup: delete the created account"):
            api_client.delete(
                DELETE_ENDPOINT, data={"email": email, "password": password}
            )

    @allure.title("POST /api/verifyLogin confirms credentials of created account")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_verify_login_after_create(self, api_client: APIClient) -> None:
        """
        Create an account, then verify its credentials via /api/verifyLogin.

        This is the 'create was real' check.  A 201 from createAccount
        tells us the API accepted our request — verifyLogin tells us
        the account actually exists in the system and is usable.
        """
        email = _unique_email()
        password = "Test@1234"
        payload = _base_payload(email, password)

        with allure.step("Create the account"):
            api_client.post(CREATE_ENDPOINT, data=payload)

        with allure.step("POST to /api/verifyLogin with new credentials"):
            response = api_client.post(
                VERIFY_ENDPOINT,
                data={"email": email, "password": password},
            )

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against SIMPLE_RESPONSE_SCHEMA"):
            validate(body, SIMPLE_RESPONSE_SCHEMA)

        with allure.step("Assert responseCode is 200 and message confirms valid user"):
            assert (
                body["responseCode"] == 200
            ), f"Expected responseCode 200, got {body['responseCode']}"
            assert (
                "User exists" in body["message"]
            ), f"Unexpected message: {body['message']}"

        with allure.step("Cleanup: delete the created account"):
            api_client.delete(
                DELETE_ENDPOINT, data={"email": email, "password": password}
            )

    @allure.title("PUT /api/updateAccount returns responseCode 200 and confirms update")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_account(self, api_client: APIClient) -> None:
        """
        Create an account, update it, and assert the update was acknowledged.

        PUT sends the full payload (same shape as createAccount).
        We change 'name' and 'city' to values distinct from creation
        so the update is not a no-op.
        """
        email = _unique_email()
        password = "Test@1234"
        payload = _base_payload(email, password)

        with allure.step("Create the account"):
            api_client.post(CREATE_ENDPOINT, data=payload)

        with allure.step("Build updated payload with changed name and city"):
            updated_payload = {
                **payload,
                "name": "QA Updated User",
                "city": "Los Angeles",
            }

        with allure.step("PUT to /api/updateAccount"):
            response = api_client.put(UPDATE_ENDPOINT, data=updated_payload)

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against SIMPLE_RESPONSE_SCHEMA"):
            validate(body, SIMPLE_RESPONSE_SCHEMA)

        with allure.step("Assert responseCode is 200 and message confirms update"):
            assert (
                body["responseCode"] == 200
            ), f"Expected responseCode 200, got {body['responseCode']}"
            assert (
                "User updated" in body["message"]
            ), f"Unexpected message: {body['message']}"

        with allure.step("Cleanup: delete the updated account"):
            api_client.delete(
                DELETE_ENDPOINT, data={"email": email, "password": password}
            )

    @allure.title(
        "DELETE /api/deleteAccount returns responseCode 200 and confirms deletion"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_account(self, api_client: APIClient) -> None:
        """
        Create an account then delete it; assert both responseCode and message.

        Asserting the deletion response makes teardown an actual test,
        not just a best-effort cleanup.
        """
        email = _unique_email()
        password = "Test@1234"
        payload = _base_payload(email, password)

        with allure.step("Create the account to be deleted"):
            api_client.post(CREATE_ENDPOINT, data=payload)

        with allure.step("DELETE /api/deleteAccount"):
            response = api_client.delete(
                DELETE_ENDPOINT,
                data={"email": email, "password": password},
            )

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against SIMPLE_RESPONSE_SCHEMA"):
            validate(body, SIMPLE_RESPONSE_SCHEMA)

        with allure.step("Assert responseCode is 200 and message confirms deletion"):
            assert (
                body["responseCode"] == 200
            ), f"Expected responseCode 200, got {body['responseCode']}"
            assert (
                "Account deleted" in body["message"]
            ), f"Unexpected message: {body['message']}"

    @allure.title("GET /api/getUserDetailByEmail returns full user object")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user_detail_by_email(self, api_client: APIClient) -> None:
        """
        Create an account, fetch its detail by email, validate the full
        user object shape against ACCOUNT_DETAIL_SCHEMA, then assert key
        field values round-trip correctly.

        This is the only test that exercises ACCOUNT_DETAIL_SCHEMA because
        it is the only endpoint that returns a nested user object.
        All other endpoints return the simpler responseCode + message shape.
        """
        email = _unique_email()
        password = "Test@1234"
        payload = _base_payload(email, password)

        with allure.step("Create the account"):
            api_client.post(CREATE_ENDPOINT, data=payload)

        with allure.step("GET /api/getUserDetailByEmail"):
            response = api_client.get("/getUserDetailByEmail", params={"email": email})

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against ACCOUNT_DETAIL_SCHEMA"):
            validate(body, ACCOUNT_DETAIL_SCHEMA)

        with allure.step("Assert responseCode is 200"):
            assert (
                body["responseCode"] == 200
            ), f"Expected responseCode 200, got {body['responseCode']}"

        with allure.step("Assert key user fields round-trip correctly"):
            user = body["user"]
            assert (
                user["email"] == email
            ), f"Expected email '{email}', got '{user['email']}'"
            assert (
                user["name"] == payload["name"]
            ), f"Expected name '{payload['name']}', got '{user['name']}'"

        with allure.step("Cleanup: delete the created account"):
            api_client.delete(
                DELETE_ENDPOINT, data={"email": email, "password": password}
            )

    @allure.title("Account lifecycle: create → verify → update → delete")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_account_full_lifecycle(self, api_client: APIClient) -> None:
        """
        Exercise the full account CRUD lifecycle in a single test.

        Schema validation is applied at every step so a contract regression
        anywhere in the lifecycle is caught immediately with a named field
        in the failure message rather than a KeyError mid-assertion.

        Marked smoke because this single test answers the most important
        question quickly: is the account API up and functional end-to-end?
        Individual tests above cover each endpoint in isolation for
        regression depth.
        """
        email = _unique_email()
        password = "Test@1234"
        payload = _base_payload(email, password)

        with allure.step(f"Step 1: Create account [{email}]"):
            create_resp = api_client.post(CREATE_ENDPOINT, data=payload)
            create_body = create_resp.json()
            validate(create_body, SIMPLE_RESPONSE_SCHEMA)
            assert create_body["responseCode"] == 201, f"Create failed: {create_body}"
            assert (
                "User created" in create_body["message"]
            ), f"Unexpected create message: {create_body['message']}"

        with allure.step("Step 2: Verify login with new credentials"):
            verify_resp = api_client.post(
                VERIFY_ENDPOINT,
                data={"email": email, "password": password},
            )
            verify_body = verify_resp.json()
            validate(verify_body, SIMPLE_RESPONSE_SCHEMA)
            assert verify_body["responseCode"] == 200, f"Verify failed: {verify_body}"
            assert (
                "User exists" in verify_body["message"]
            ), f"Unexpected verify message: {verify_body['message']}"

        with allure.step("Step 3: Update account name and city"):
            updated_payload = {
                **payload,
                "name": "QA Updated User",
                "city": "Los Angeles",
            }
            update_resp = api_client.put(UPDATE_ENDPOINT, data=updated_payload)
            update_body = update_resp.json()
            validate(update_body, SIMPLE_RESPONSE_SCHEMA)
            assert update_body["responseCode"] == 200, f"Update failed: {update_body}"
            assert (
                "User updated" in update_body["message"]
            ), f"Unexpected update message: {update_body['message']}"

        with allure.step("Step 4: Delete the account"):
            delete_resp = api_client.delete(
                DELETE_ENDPOINT,
                data={"email": email, "password": password},
            )
            delete_body = delete_resp.json()
            validate(delete_body, SIMPLE_RESPONSE_SCHEMA)
            assert delete_body["responseCode"] == 200, f"Delete failed: {delete_body}"
            assert (
                "Account deleted" in delete_body["message"]
            ), f"Unexpected delete message: {delete_body['message']}"
