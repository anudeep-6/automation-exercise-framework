"""
API authentication tests for automationexercise.com.

Covers four assertion layers on each endpoint:
  1. Transport layer   — HTTP status code
  2. Contract layer    — response shape via JSON Schema
  3. Application layer — responseCode in the JSON envelope
  4. Business logic    — field values confirm the expected outcome

Coverage:
- POST /api/verifyLogin — valid credentials, wrong password, empty email,
  invalid format
- GET /api/getUserDetailByEmail — valid email returns user fields,
  nonexistent email returns error
"""

import allure
import pytest

from src.api.api_client import APIClient
from src.utils.data_reader import DataReader
from src.utils.schema_validator import validate
from tests.api.schemas.account_schema import (
    ACCOUNT_DETAIL_SCHEMA,
    SIMPLE_RESPONSE_SCHEMA,
)

VERIFY_ENDPOINT = "/verifyLogin"
GET_USER_ENDPOINT = "/getUserDetailByEmail"


def load_login_cases(expected_result: str) -> list[tuple]:
    """Load and shape user rows from users_test_data.csv for login parametrization.

    Args:
        expected_result: Filter value for the 'expected_result' column.
            'success' for valid credentials, 'failure' for invalid.

    Returns:
        List of (email, password, validation_type, expected_response_code) tuples.
    """
    reader = DataReader()
    rows = reader.load_csv_rows(
        "users_test_data.csv", filter_by={"expected_result": expected_result}
    )
    return [
        (
            row["username"],
            row["password"],
            row.get("validation_type", ""),
            int(row.get("expected_response_code", 404)),
        )
        for row in rows
    ]


def load_valid_user() -> tuple:
    """Load the single valid user from users_test_data.csv.

    Returns:
        Tuple of (email, password, name) for the success-row user.
    """
    reader = DataReader()
    rows = reader.load_csv_rows(
        "users_test_data.csv", filter_by={"expected_result": "success"}
    )
    row = rows[0]
    return row["username"], row["password"], row["name"]


@allure.epic("API")
@allure.feature("Authentication")
class TestAuthApi:
    """Tests covering POST /api/verifyLogin and GET /api/getUserDetailByEmail."""

    @allure.story("Verify Login — valid credentials")
    @allure.title("POST /api/verifyLogin — valid credentials returns 200")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_valid_login_returns_200(self, api_client: APIClient) -> None:
        """Verify that correct credentials return responseCode 200.

        Given a registered user with valid email and password
        When POST /api/verifyLogin is called with those credentials
        Then the body conforms to SIMPLE_RESPONSE_SCHEMA, responseCode is 200,
        and the message confirms the user exists.
        """
        email, password, _ = load_valid_user()

        with allure.step(f"POST /api/verifyLogin with valid credentials — {email}"):
            response = api_client.post(
                VERIFY_ENDPOINT,
                data={"email": email, "password": password},
            )

        with allure.step("Assert HTTP status code is 200"):
            assert (
                response.status_code == 200
            ), f"Expected HTTP 200, got {response.status_code}"

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against SIMPLE_RESPONSE_SCHEMA"):
            validate(body, SIMPLE_RESPONSE_SCHEMA)

        with allure.step("Assert responseCode 200 and message confirms user exists"):
            assert (
                body["responseCode"] == 200
            ), f"Expected responseCode 200, got {body['responseCode']}"
            assert (
                "User exists" in body["message"]
            ), f"Unexpected message: {body['message']}"

    @allure.story("Verify Login — invalid credentials")
    @allure.title("POST /api/verifyLogin — {validation_type}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "email, password, validation_type, expected_response_code",
        load_login_cases("failure"),
    )
    def test_invalid_login_returns_error(
        self,
        email: str,
        password: str,
        validation_type: str,
        expected_response_code: int,
        api_client: APIClient,
    ) -> None:
        """Verify that invalid credentials return the appropriate error responseCode.

        Given a user submitting invalid, empty, or malformed credentials
        When POST /api/verifyLogin is called
        Then the body conforms to SIMPLE_RESPONSE_SCHEMA and responseCode matches
        the expected error code for that scenario (404 for wrong credentials,
        400 for missing/empty fields).

        Args:
            email: Email value from CSV (may be empty or malformed).
            password: Password value from CSV.
            validation_type: Describes the failure scenario for traceability.
            expected_response_code: Per-row expected responseCode from CSV.
            api_client: Session-scoped API client fixture.
        """
        with allure.step(f"POST /api/verifyLogin — scenario: '{validation_type}'"):
            response = api_client.post(
                VERIFY_ENDPOINT,
                data={"email": email, "password": password},
            )

        with allure.step("Assert HTTP status code is 200"):
            assert (
                response.status_code == 200
            ), f"Expected HTTP 200, got {response.status_code}"

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against SIMPLE_RESPONSE_SCHEMA"):
            validate(body, SIMPLE_RESPONSE_SCHEMA)

        with allure.step(
            f"Assert responseCode {expected_response_code} for "
            f"scenario '{validation_type}'"
        ):
            assert body["responseCode"] == expected_response_code, (
                f"Scenario '{validation_type}': "
                f"expected responseCode {expected_response_code}, "
                f"got {body['responseCode']}"
            )

    @allure.story("Get User Detail — valid email")
    @allure.title("GET /api/getUserDetailByEmail — valid email returns user fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_user_detail_valid_email(self, api_client: APIClient) -> None:
        """Verify that a valid email returns a user object.

        Given a registered user's email address
        When GET /api/getUserDetailByEmail is called with that email
        Then the body conforms to ACCOUNT_DETAIL_SCHEMA,
        responseCode is 200, and the user object contains the expected
        email value.
        """
        email, _, _ = load_valid_user()

        with allure.step(f"GET /api/getUserDetailByEmail?email={email}"):
            response = api_client.get(
                GET_USER_ENDPOINT,
                params={"email": email},
            )

        with allure.step("Assert HTTP status code is 200"):
            assert (
                response.status_code == 200
            ), f"Expected HTTP 200, got {response.status_code}"

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against ACCOUNT_DETAIL_SCHEMA"):
            validate(body, ACCOUNT_DETAIL_SCHEMA)

        with allure.step("Assert responseCode is 200"):
            assert (
                body["responseCode"] == 200
            ), f"Expected responseCode 200, got {body['responseCode']}"

        with allure.step("Assert user object contains correct email"):
            user = body["user"]
            assert (
                user["email"] == email
            ), f"Expected email '{email}', got '{user['email']}'"

    @allure.story("Get User Detail — nonexistent email")
    @allure.title("GET /api/getUserDetailByEmail — nonexistent email returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user_detail_nonexistent_email(self, api_client: APIClient) -> None:
        """Verify that a nonexistent email returns responseCode 404.

        Given an email address that does not belong to any registered account
        When GET /api/getUserDetailByEmail is called with that email
        Then the body conforms to SIMPLE_RESPONSE_SCHEMA and responseCode is 404.

        Note: SIMPLE_RESPONSE_SCHEMA is used here, not ACCOUNT_DETAIL_SCHEMA,
        because a 404 response returns no user object — only responseCode and message.
        """
        reader = DataReader()
        auth_data = reader.read_json("auth_test_data.json")
        nonexistent_email = auth_data["nonexistent_email"]

        with allure.step(f"GET /api/getUserDetailByEmail?email={nonexistent_email}"):
            response = api_client.get(
                GET_USER_ENDPOINT,
                params={"email": nonexistent_email},
            )

        with allure.step("Assert HTTP status code is 200"):
            assert (
                response.status_code == 200
            ), f"Expected HTTP 200, got {response.status_code}"

        with allure.step("Parse response body as JSON"):
            body = response.json()

        with allure.step("Validate response body shape against SIMPLE_RESPONSE_SCHEMA"):
            validate(body, SIMPLE_RESPONSE_SCHEMA)

        with allure.step("Assert responseCode 404 for unknown email"):
            assert (
                body["responseCode"] == 404
            ), f"Expected responseCode 404, got {body['responseCode']}"
