"""Dynamic test data generation using the Faker library."""

import allure
from faker import Faker

from src.utils.logger import get_logger

_fake = Faker()
logger = get_logger(__name__)


class FakeData:
    """Generates randomised, unique test data for use across UI and API tests.

    Each method call produces a new value — safe for parallel test runs.
    """

    @staticmethod
    def generate_email() -> str:
        """Return a unique email address."""
        with allure.step("Generate unique email"):
            email = _fake.unique.email()
            logger.debug("Generated email: %s", email)
            return email

    @staticmethod
    def generate_first_name() -> str:
        """Return a random first name."""
        name = _fake.first_name()
        logger.debug("Generated first name: %s", name)
        return name

    @staticmethod
    def generate_last_name() -> str:
        """Return a random last name."""
        name = _fake.last_name()
        logger.debug("Generated last name: %s", name)
        return name

    @staticmethod
    def generate_full_name() -> tuple[str, str]:
        """Return a (first_name, last_name) tuple."""
        with allure.step("Generate full name"):
            first, last = _fake.first_name(), _fake.last_name()
            logger.debug("Generated full name: %s %s", first, last)
            return first, last

    @staticmethod
    def generate_password(length: int = 12) -> str:
        """Return a password that meets automationexercise.com complexity rules.

        Args:
            length: Desired password length (minimum 8). Defaults to 12.
        """
        with allure.step("Generate password"):
            pwd = _fake.password(
                length=length, special_chars=True, digits=True, upper_case=True
            )
            logger.debug("Generated password of length %d", len(pwd))
            return pwd

    @staticmethod
    def generate_phone() -> str:
        """Return a numeric mobile number string."""
        phone = _fake.numerify("##########")
        logger.debug("Generated phone: %s", phone)
        return phone

    @staticmethod
    def generate_address() -> dict[str, str]:
        """Return a dictionary with street-level address components.

        Keys: address1, address2, city, state, zipcode, country.
        """
        with allure.step("Generate address"):
            address = {
                "address1": _fake.street_address(),
                "address2": _fake.secondary_address(),
                "city": _fake.city(),
                "state": _fake.state(),
                "zipcode": _fake.zipcode(),
                "country": "United States",
            }
            logger.debug(
                "Generated address: city=%s, state=%s",
                address["city"],
                address["state"],
            )
            return address
