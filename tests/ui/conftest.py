import pytest


@pytest.fixture(scope="function")
def logger():
    print("\n[SETUP] Test starting")
    yield
    print("\n[TEARDOWN] Test finished")
