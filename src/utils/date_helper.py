"""Date formatting and arithmetic utilities for test data preparation."""

from datetime import datetime, timedelta

import allure

from src.utils.logger import get_logger

logger = get_logger(__name__)


class DateHelper:
    """Provides date helpers needed by registration forms and date-based assertions.

    All methods are static — no instance state required.
    """

    @staticmethod
    def get_today(fmt: str = "%Y-%m-%d") -> str:
        """Return today's date as a formatted string.

        Args:
            fmt: strftime format string. Defaults to ISO 8601 ('%Y-%m-%d').
        """
        result = datetime.today().strftime(fmt)
        logger.debug("get_today(fmt=%s) -> %s", fmt, result)
        return result

    @staticmethod
    def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
        """Format an arbitrary datetime object to a string.

        Args:
            dt:  The datetime to format.
            fmt: strftime format string. Defaults to '%Y-%m-%d'.
        """
        result = dt.strftime(fmt)
        logger.debug("format_date(fmt=%s) -> %s", fmt, result)
        return result

    @staticmethod
    def days_from_now(n: int, fmt: str = "%Y-%m-%d") -> str:
        """Return the date n days from today as a formatted string.

        Negative values produce past dates, positive values future dates.

        Args:
            n:   Number of days offset from today.
            fmt: strftime format string. Defaults to '%Y-%m-%d'.
        """
        target = datetime.today() + timedelta(days=n)
        result = target.strftime(fmt)
        logger.debug("days_from_now(n=%d, fmt=%s) -> %s", n, fmt, result)
        return result

    @staticmethod
    def birth_date_parts(years_ago: int = 25) -> dict[str, str]:
        """Return day, month, and year strings for a DOB dropdown.

        automationexercise.com registration uses separate day/month/year
        selects. Returns values pre-formatted to match the option text.

        Args:
            years_ago: Age in years. Defaults to 25.

        Returns:
            Dict with keys 'day' (e.g. '15'), 'month' (e.g. 'June'),
            'year' (e.g. '1999').
        """
        with allure.step(f"Generate DOB parts ({years_ago} years ago)"):
            dob = datetime.today() - timedelta(days=years_ago * 365)
            parts = {
                "day": str(dob.day),
                "month": dob.strftime("%B"),
                "year": str(dob.year),
            }
            logger.debug(
                "birth_date_parts -> day=%s, month=%s, year=%s",
                parts["day"],
                parts["month"],
                parts["year"],
            )
            return parts
