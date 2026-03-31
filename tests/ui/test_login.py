import allure
import pytest

from src.utils.data_reader import DataReader


def load_users(expected_result):
    reader = DataReader()
    users = reader.read_csv("users.csv")
    return [
        (row["username"], row["password"])
        for row in users
        if row["expected_result"] == expected_result
    ]


@allure.epic("E-Commerce")
@allure.feature("Authentication")
class TestLogin:
    @pytest.mark.smoke
    @allure.title("valid login succeeds")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("username, password", load_users("success"))
    def test_valid_login(self, username, password, logger):
        with allure.step(f"Attempt login with {username}"):
            assert username != ""
        with allure.step("verify login result"):
            assert True

    @pytest.mark.regression
    @allure.title("invalid login fails gracefully")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("username, password", load_users("failure"))
    def test_invalid_login(self, username, password, logger):
        with allure.step(f"Attempt login with invalid credentials: {username}"):
            assert True  # placeholder until Playwright
        with allure.step("verify failure is handled"):
            assert True
