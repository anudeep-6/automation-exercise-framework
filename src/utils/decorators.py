"""This file contains custom decorators for the automation framework"""

import logging
import time

logger = logging.getLogger(__name__)


def retry(max_attempts=3, delay=1):
    """Decorator that retries a function if it raises an exception.
    Args
        max_attempts(int): Maximun number of attempts. Defaults to 3.
        delay(int): Seconds to wait between attempts. Defaults to 1
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if attempt == max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts"
                        )
                        raise
                    logger.warning(
                        f"Attempt {attempt} failed for {func.__name__}: {err}."
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)

        return wrapper

    return decorator
