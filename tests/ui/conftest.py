"""
UI-specific fixtures for the tests/ui/ directory.

Provides page object fixtures that inject the Playwright page
and base_url from the root conftest into each page class.
All fixtures are function-scoped — a fresh page object per test.
"""

import logging
import os
import time

import allure
import pytest
from playwright.sync_api import BrowserContext, Page

from src.pages.account_created_page import AccountCreatedPage
from src.pages.account_deleted_page import AccountDeletedPage
from src.pages.cart_page import CartPage
from src.pages.checkout_page import CheckoutPage
from src.pages.contact_us_page import ContactUsPage
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.pages.order_confirmation_page import OrderConfirmationPage
from src.pages.payment_page import PaymentPage
from src.pages.product_page import ProductsPage
from src.pages.registration_page import RegistrationPage
from src.utils.data_reader import DataReader
from src.utils.log_manager import (
    attach_file_handler,
    attach_log_to_allure,
    detach_file_handler,
    get_test_output_dir,
)

AUTH_STATE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "auth", "state.json"
)

root_logger = logging.getLogger()


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
def contact_us_page(page, base_url) -> ContactUsPage:
    """Returns an ContactUsPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        ContactUsPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] ContactUsPage initialised")
    return ContactUsPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def products_page(page, base_url) -> ProductsPage:
    """Returns an ProductsPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        ProductsPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] ProductsPage initialised")
    return ProductsPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def cart_page(page, base_url) -> CartPage:
    """Returns an CartPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        CartPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] CartPage initialised")
    return CartPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def checkout_page(page, base_url) -> CheckoutPage:
    """Returns an CheckoutPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        CheckoutPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] CheckoutPage initialised")
    return CheckoutPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def order_confirmation_page(page, base_url) -> OrderConfirmationPage:
    """Returns an OrderConfirmationPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        OrderConfirmationPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] OrderConfirmationPage initialised")
    return OrderConfirmationPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def payment_page(page, base_url) -> PaymentPage:
    """Returns an PaymentPage instance for the current test.

    Args:
        page: Playwright Page object from root conftest.
        base_url: Base URL string from root conftest.

    Returns:
        PaymentPage: Ready-to-use page object, not yet navigated.
    """
    root_logger.info("[FIXTURE] PaymentPage initialised")
    return PaymentPage(page=page, base_url=base_url)


@pytest.fixture(scope="function")
def load_contact_data() -> dict:
    """Load contact form test data from contact_us_test_data.json.

    Returns:
        dict: Contact form fields — name, email, subject, message.
    """
    reader = DataReader()
    return reader.read_json("contact_us_test_data.json")


@pytest.fixture(scope="function")
def register_user_data(data_reader: DataReader) -> dict:
    """Loads registration test data from register_user_test_data.json and patches
    the email with a timestamp to ensure uniqueness per test run.

    Args:
        data_reader: Session-scoped DataReader instance from root conftest.

    Returns:
        dict: Registration data with a unique email address.
    """
    data = data_reader.read_json("register_user_test_data.json")
    data["email"] = f"testuser_{int(time.time())}@example.com"
    root_logger.info("[FIXTURE] register_user_data loaded, email: %s", data["email"])
    return data


@pytest.fixture(autouse=True)
def per_test_artifacts(request, page, context, config_reader):
    """Creates a per-test output folder with logs, screenshot, and trace on failure.

    Attaches trace, screenshot, and test.log to the Allure report based on
    the outcome of the test and the configured trace/screenshot modes.
    """
    test_name = request.node.name.replace("[", "_").replace("]", "")
    output_dir = get_test_output_dir(test_name)
    handler = attach_file_handler(output_dir)

    yield

    # rep_call is absent if the test failed during setup — fall back to False
    rep_call = getattr(request.node, "rep_call", None)
    failed = rep_call.failed if rep_call is not None else False

    trace_mode = config_reader.trace

    if trace_mode in ("on", "retain-on-failure"):
        save_trace = failed or trace_mode == "on"
        if save_trace:
            trace_path = output_dir / "trace.zip"
            context.tracing.stop(path=trace_path)
            root_logger.info("[FIXTURE] Trace saved: %s", trace_path)
            if failed:
                allure.attach.file(
                    str(trace_path),
                    name="trace",
                    attachment_type=allure.attachment_type.ZIP,
                )
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
        root_logger.info("[FIXTURE] Screenshot saved: %s", screenshot_path)

    detach_file_handler(handler)
    attach_log_to_allure(output_dir)


def load_existing_users() -> list[dict]:
    """Load already-registered users from users_test_data.csv.

    Returns:
        list[dict]: Row dicts where expected_result == 'success'.
    """
    data_reader = DataReader()
    return data_reader.load_csv_rows(
        "users_test_data.csv", filter_by={"expected_result": "success"}
    )


@pytest.fixture()
def load_product_test_data(data_reader: DataReader):
    """Loads product test data from product_test_data.json.

    Returns:
        dict: Product fields (id, name, price, quantity, total, comment).
    """
    return data_reader.read_json("product_test_data.json")


@pytest.fixture()
def load_payment_test_data(data_reader: DataReader):
    """Loads payment test data from payment_test_data.json.

    Returns:
        dict: Payment fields (card number, expiry, CVV, name on card).
    """
    return data_reader.read_json("payment_test_data.json")


@pytest.fixture(scope="function")
def auth_context(browser_instance, config_reader) -> BrowserContext:
    """Browser context pre-loaded with saved authentication state.

    Requires auth/state.json to exist. Run scripts/save_auth_state.py
    first if the file is missing or the session has expired.

    Tests using this fixture start already logged in — the login page
    is never visited.

    Args:
        browser_instance: Session-scoped browser from root conftest.
        config_reader: Config for viewport, timeout, and trace settings.

    Returns:
        BrowserContext: Context with injected cookies and localStorage.
    """
    if not os.path.exists(AUTH_STATE_PATH):
        pytest.fail(
            "auth/state.json not found. "
            "Run `python scripts/save_auth_state.py` to generate it."
        )

    ctx: BrowserContext = browser_instance.new_context(
        storage_state=AUTH_STATE_PATH,
        viewport=config_reader.viewport,
    )
    ctx.set_default_timeout(config_reader.timeout)

    trace_mode = config_reader.trace
    if trace_mode in ("on", "retain-on-failure"):
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
        root_logger.info(f"[FIXTURE] auth_context tracing started — mode: {trace_mode}")

    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def auth_page(auth_context: BrowserContext) -> Page:
    """Playwright Page derived from the authenticated browser context.

    Use this fixture in any test that requires a logged-in user.
    The session is already active — no login step required.

    Args:
        auth_context: Function-scoped authenticated context.

    Returns:
        Page: Playwright Page ready for authenticated interactions.
    """
    p = auth_context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="function")
def auth_home_page(auth_page: Page, base_url: str) -> HomePage:
    """Returns a HomePage initialised on the authenticated page object.

    Use this when a test needs to start on the home page as a logged-in user
    without going through the login flow.

    Args:
        auth_page: Authenticated Playwright Page from auth_page fixture.
        base_url: Base URL from root conftest.

    Returns:
        HomePage: Ready-to-use page object backed by an authenticated session.
    """
    root_logger.info("[FIXTURE] auth_home_page initialised")
    return HomePage(page=auth_page, base_url=base_url)
