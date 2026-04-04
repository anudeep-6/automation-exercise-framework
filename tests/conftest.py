"""
Pytest configuration and shared fixtures.

This conftest.py provides session, module, and class scoped fixtures
available to all tests in the framework.
"""

import logging

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.utils.config_reader import ConfigReader
from src.utils.data_reader import DataReader
from src.utils.exceptions import ConfigurationException, TestDataException

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config_reader() -> ConfigReader:
    """Creates ConfigReader once per session.

    Returns:
        ConfigReader: Loaded and validated config instance.

    Raises:
        ConfigurationException: If config file is missing or invalid.
    """
    try:
        reader = ConfigReader()
        logger.info("[SESSION] Config loaded via ConfigReader")
        return reader
    except ConfigurationException as err:
        pytest.fail(f"Failed to load config: {err}")


@pytest.fixture(scope="session")
def base_url(config_reader: ConfigReader) -> str:
    """Returns validated base UI URL from config.

    Args:
        config_reader: Injected ConfigReader fixture.

    Returns:
        str: Base URL for the application.
    """
    url = config_reader.base_url
    logger.info(f"[SESSION] Base URL: {url}")
    return url


@pytest.fixture(scope="session")
def browser_name(config_reader: ConfigReader) -> str:
    """Returns validated browser name from config.

    Args:
        config_reader: Injected ConfigReader fixture.

    Returns:
        str: Browser name — chromium, firefox, or webkit.
    """
    name = config_reader.browser
    logger.info(f"[SESSION] Browser: {name}")
    return name


@pytest.fixture(scope="session")
def timeout(config_reader: ConfigReader) -> int:
    """Returns default timeout in milliseconds from config.

    Args:
        config_reader: Injected ConfigReader fixture.

    Returns:
        int: Timeout in milliseconds.
    """
    value = config_reader.timeout
    logger.info(f"[SESSION] Timeout: {value}ms")
    return value


@pytest.fixture(scope="session")
def playwright_instance():
    """Starts and stops the Playwright engine once per session."""
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser_instance(
    playwright_instance, browser_name: str, config_reader: ConfigReader
) -> Browser:
    """Launches the browser once per session.

    Args:
        playwright_instance: Running Playwright engine.
        browser_name: Browser to launch from config.
        config_reader: Config for headless and slow_mo settings.

    Returns:
        Browser: Launched Playwright Browser instance.
    """
    launcher = getattr(playwright_instance, browser_name)
    browser = launcher.launch(
        headless=config_reader.headless,
        slow_mo=config_reader.slow_mo,
    )
    logger.info(f"[SESSION] Browser launched: {browser_name}")
    yield browser
    browser.close()
    logger.info("[SESSION] Browser closed")


@pytest.fixture(scope="function")
def context(browser_instance: Browser, config_reader: ConfigReader) -> BrowserContext:
    """Creates a fresh browser context per test function.

    Args:
        browser_instance: Session-scoped browser.
        config_reader: Config for viewport, timeout, and trace settings.

    Returns:
        BrowserContext: Isolated browser context with tracing started.
    """
    ctx = browser_instance.new_context(
        viewport=config_reader.viewport,
    )
    ctx.set_default_timeout(config_reader.timeout)

    trace_mode = config_reader.trace
    if trace_mode in ("on", "retain-on-failure"):
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
        logger.info(f"[FIXTURE] Tracing started — mode: {trace_mode}")

    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Creates a fresh page per test function.

    Args:
        context: Function-scoped browser context.

    Returns:
        Page: Playwright Page object ready for interaction.
    """
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="module")
def data_reader() -> DataReader:
    """Creates DataReader once per test module.

    Returns:
        DataReader: Instance pointing at test_data directory.
    """
    reader = DataReader()
    logger.info("[MODULE] DataReader initialised")
    return reader


@pytest.fixture(scope="class")
def sample_user_data(data_reader: DataReader) -> list[dict]:
    """Loads users.csv once per test class.

    Args:
        data_reader: Injected DataReader fixture.

    Returns:
        list[dict]: Rows from users.csv as dictionaries.
    """
    try:
        users = data_reader.read_csv("users.csv")
        logger.info("[CLASS] Loaded user data from users.csv")
        return users
    except TestDataException as err:
        pytest.fail(f"Failed to load user data: {err}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures test result per phase for use in fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
