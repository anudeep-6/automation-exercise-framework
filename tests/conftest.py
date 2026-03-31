"""
Pytest configuration and shared fixtures.

This conftest.py provides fixtures that are available to all tests in the framework.
Fixtures are organized by scope for optimal test performance.
"""

from typing import Any, Dict, List

import pytest

from src.utils.config_reader import ConfigReader
from src.utils.data_reader import DataReader


@pytest.fixture(scope="session")
def config_reader() -> ConfigReader:
    """
    Create ConfigReader instance once per test session.

    This fixture creates a ConfigReader object that loads configuration
    from config.json. The ConfigReader is reused across ALL tests.

    Returns:
        ConfigReader: ConfigReader instance with loaded configuration

    Raises:
        FileNotFoundError: If config.json is not found
        ValueError: If config.json has invalid JSON
    """
    try:
        reader = ConfigReader()
        print("\n[SESSION] Config loaded via ConfigReader")
        return reader
    except (FileNotFoundError, ValueError) as err:
        pytest.fail(f"Failed to load config: {err}")


@pytest.fixture(scope="session")
def config(config_reader: ConfigReader) -> Dict[str, Any]:
    """
    Get raw config dictionary from ConfigReader.

    This provides backward compatibility - tests can use either:
    - config_reader (the ConfigReader object with properties)
    - config (the raw dictionary)

    Args:
        config_reader: ConfigReader fixture (automatically injected)

    Returns:
        dict: Raw configuration dictionary
    """
    return config_reader._config


@pytest.fixture(scope="session")
def base_url(config_reader: ConfigReader) -> str:
    """
    Get base URL from ConfigReader - session scoped.

    Uses the ConfigReader's base_url property which handles validation.

    Args:
        config_reader: ConfigReader fixture (automatically injected)

    Returns:
        str: Base URL for the application

    Raises:
        ValueError: If base_url is not configured
    """
    url = config_reader.base_url
    print(f"[SESSION] Base URL set to {url}")
    return url


@pytest.fixture(scope="session")
def browser(config_reader: ConfigReader) -> str:
    """
    Get browser from ConfigReader - session scoped.

    Uses the ConfigReader's browser property which validates the browser.

    Args:
        config_reader: ConfigReader fixture (automatically injected)

    Returns:
        str: Browser name (chromium, firefox, or webkit)

    Raises:
        ValueError: If browser is not configured or invalid
    """
    browser_name = config_reader.browser
    print(f"[SESSION] Browser set to: {browser_name}")
    return browser_name


@pytest.fixture(scope="session")
def timeout(config_reader: ConfigReader) -> int:
    """
    Get default timeout from ConfigReader - session scoped.

    Uses the ConfigReader's timeout property with default fallback.

    Args:
        config_reader: ConfigReader fixture (automatically injected)

    Returns:
        int: Timeout value in milliseconds (default: 30000)
    """
    timeout_value = config_reader.timeout
    print(f"[SESSION] Timeout set to: {timeout_value}ms")
    return timeout_value


@pytest.fixture(scope="module")
def data_reader() -> DataReader:
    """
    Create DataReader instance - module scoped.

    Runs once per test module (test file). Provides access to your
    DataReader utility for reading CSV and JSON test data files.

    Returns:
        DataReader: DataReader instance for accessing test data
    """
    reader = DataReader()
    print("\n[MODULE] Data reader initialized for test_data directory")
    return reader


@pytest.fixture(scope="class")
def sample_user_data(data_reader: DataReader) -> List[Dict[str, str]]:
    """
    Load sample user data from users.csv - class scoped.

    Runs once per test class. Uses DataReader to load actual test data
    from your users.csv file instead of hardcoding values.

    Args:
        data_reader: DataReader fixture (automatically injected)

    Returns:
        list: List of user dictionaries from users.csv
    """
    print("\n[CLASS] Loading user data from users.csv via DataReader")
    users = data_reader.read_csv("users.csv")
    return users


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for use in fixtures.

    This makes test results available to fixtures like screenshot_on_failure.
    The call parameter is required by pytest's hook signature but not used here.

    Args:
        item: Test item being executed
        call: information about the test call (setup/call/teardown phase)
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def browser_setup():
    """Session-scoped fixture to simulate browser lifecycle."""
    print("\n[SESSION SETUP] Browser starting")
    yield
    print("\n[SESSION TEARDOWN] Browser closing")
