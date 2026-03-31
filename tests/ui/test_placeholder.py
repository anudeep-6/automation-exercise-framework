import os

import pytest


def test_first(logger):
    print("Running test_first")
    assert True


def test_second(logger):
    print("Running test_second")
    assert True


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature(logger):
    assert False


@pytest.mark.xfail(reason="Known bug - login return 500 intermittently")
def test_known_bug(logger):
    assert False


@pytest.mark.skipif(
    os.getenv("RUN_ENV") != "staging", reason="only runs in staging environment"
)
def test_staging_only(logger):
    assert True
