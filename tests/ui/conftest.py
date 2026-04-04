"""
UI-specific fixtures for the tests/ui/ directory.

Provides page object fixtures that inject the Playwright page
and base_url from the root conftest into each page class.
All fixtures are function-scoped — a fresh page object per test.
"""

import json
import logging
import time
from pathlib import Path

import allure
import pytest

from src.pages.account_created_page import AccountCreatedPage
from src.pages.account_deleted_page import AccountDeletedPage
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.pages.registration_page import RegistrationPage
from src.utils.log_manager import (
    attach_file_handler,
    detach_file_handler,
    get_test_output_dir,
)

root_logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def login_page(page, base_url) -> LoginPage:
    """Returns a LoginPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        LoginPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] LoginPage initialised")
    return LoginPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def home_page(page, base_url) -> HomePage:
    """Returns a HomePage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        HomePage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] HomePage initialised")
    return HomePage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def registration_page(page, base_url) -> RegistrationPage:
    """Returns a RegistrationPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        RegistrationPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] RegistrationPage initialised")
    return RegistrationPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def account_created_page(page, base_url) -> AccountCreatedPage:
    """Returns an AccountCreatedPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        AccountCreatedPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] AccountCreatedPage initialised")
    return AccountCreatedPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def account_deleted_page(page, base_url) -> AccountDeletedPage:
    """Returns an AccountDeletedPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        AccountDeletedPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] AccountDeletedPage initialised")
    return AccountDeletedPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def register_user_data() -> dict:
    """Loads registration test data from register_user.json and patches
    the email with a timestamp to ensure uniqueness per test run.

    Returns:
        dict: Registration data with a unique email address.
    """
    path = Path("test_data/register_user.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data["email"] = f"testuser_{int(time.time())}@example.com"
    root_logger.info("[FIXTURE] register_user_data loaded, email: %s", data["email"])
    return data


@pytest.fixture(autouse=True)
def per_test_artifacts(request, page, context, config_reader):
    """Creates a per-test output folder with logs, screenshot, and trace on failure."""
    test_name = request.node.name.replace("[", "_").replace("]", "")
    output_dir = get_test_output_dir(test_name)
    handler = attach_file_handler(output_dir)

    yield

    failed = request.node.rep_call.failed
    trace_mode = config_reader.trace

    if trace_mode in ("on", "retain-on-failure"):
        if trace_mode == "on" or (trace_mode == "retain-on-failure" and failed):
            trace_path = output_dir / "trace.zip"
            context.tracing.stop(path=trace_path)
            allure.attach.file(
                str(trace_path),
                name="trace",
                attachment_type=allure.attachment_type.ZIP,
            )
            root_logger.info(f"[FIXTURE] Trace saved: {trace_path}")
        else:
            context.tracing.stop()  # discard — test passed
            root_logger.info("[FIXTURE] Trace discarded — test passed")

    if failed:
        screenshot_path = output_dir / "screenshot.png"
        page.screenshot(path=screenshot_path)
        allure.attach.file(
            str(screenshot_path),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        root_logger.info(f"[FIXTURE] Screenshot saved: {screenshot_path}")

    detach_file_handler(handler)
