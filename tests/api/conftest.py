"""
API-layer conftest.

Provides the api_client fixture used by all tests under tests/api/.
Scoped to 'session' so the same Session object (and its connection
pool) is reused across the entire test run — same reasoning as the
browser fixture in the UI layer.
"""

import pytest

from src.api.api_client import APIClient


@pytest.fixture(scope="session")
def api_client(base_api_url: str) -> APIClient:
    """
    Session-scoped APIClient pointed at the configured base API URL.

    Yields the client for the duration of the test session, then
    closes the underlying requests.Session to release connections.
    """
    client = APIClient(base_url=base_api_url)
    yield client
    client.close()
