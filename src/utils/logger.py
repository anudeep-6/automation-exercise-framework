"""Provides named loggers for framework modules."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Returns a named logger for the given module.

    Loggers propagate to the root logger, which log_manager configures
    per test with a file handler and appropriate level.

    Args:
        name (str): Logger name — pass __name__ from the calling module.

    Returns:
        logging.Logger: Named logger instance.
    """
    return logging.getLogger(name)
