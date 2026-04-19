"""Reusable decorators for retry logic and other cross-cutting framework concerns."""

import functools
import logging
import time

logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retries a function on exception up to a maximum number of attempts.

    Useful for interactions that are inherently flaky — file upload dialogs,
    third-party widgets, or API endpoints with transient failures.

    Args:
        max_attempts (int): Maximum number of attempts before re-raising.
            Defaults to 3.
        delay (float): Seconds to wait between attempts. Accepts floats
            for sub-second intervals (e.g. 0.5). Defaults to 1.0.

    Raises:
        Exception: Re-raises the last exception if all attempts are exhausted.

    Example:
        @retry(max_attempts=3, delay=2.0)
        def submit_payment(self):
            ...
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if attempt == max_attempts:
                        logger.error(
                            "%s failed after %d attempts",
                            func.__name__,
                            max_attempts,
                        )
                        raise
                    logger.warning(
                        "Attempt %d/%d failed for %s: %s — retrying in %.1fs",
                        attempt,
                        max_attempts,
                        func.__name__,
                        err,
                        delay,
                    )
                    time.sleep(delay)

        return wrapper

    return decorator
