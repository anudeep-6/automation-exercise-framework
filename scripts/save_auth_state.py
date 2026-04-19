"""
One-time script to perform login and persist browser authentication state
to auth/state.json. Run this before the test suite when the session expires.
"""

import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

from playwright.sync_api import sync_playwright  # noqa: E402

from src.utils.config_reader import ConfigReader  # noqa: E402
from src.utils.data_reader import DataReader  # noqa: E402

AUTH_STATE_PATH = os.path.join(os.path.dirname(__file__), "..", "auth", "state.json")


def get_valid_credentials() -> tuple[str, str]:
    """Read the first valid credentials row from users.csv.

    Returns:
        tuple[str, str]: (username, password)

    Raises:
        SystemExit: If no valid credentials row is found in users.csv.
    """
    reader = DataReader()
    rows = reader.load_csv_rows("users.csv", filter_by={"expected_result": "success"})

    if not rows:
        print("ERROR: No 'success' rows found in users.csv.")
        print("Add at least one registered account row before running this script.")
        sys.exit(1)

    first_valid = rows[0]
    return first_valid["username"], first_valid["password"]


def save_auth_state() -> None:
    """
    Launch a browser, log in with credentials from users.csv, and save
    the resulting storage state (cookies + localStorage) to auth/state.json.
    """
    config = ConfigReader()
    base_url: str = config.base_url
    email, password = get_valid_credentials()

    os.makedirs(os.path.dirname(AUTH_STATE_PATH), exist_ok=True)

    with sync_playwright() as p:
        launcher = getattr(p, config.browser)
        browser = launcher.launch(headless=config.headless, slow_mo=config.slow_mo)
        context = browser.new_context(viewport=config.viewport)
        page = context.new_page()

        print(f"[AUTH] Navigating to: {base_url}/login")
        page.goto(f"{base_url}/login")

        page.locator("input[data-qa='login-email']").fill(email)
        page.locator("input[data-qa='login-password']").fill(password)
        page.locator("button[data-qa='login-button']").click()

        page.wait_for_selector("a[href='/logout']", timeout=10_000)
        print(f"[AUTH] Login successful for: {email}")

        context.storage_state(path=AUTH_STATE_PATH)
        print(f"[AUTH] Auth state saved to: {AUTH_STATE_PATH}")

        browser.close()


if __name__ == "__main__":
    save_auth_state()
