"""Manages per-test log file setup, teardown, and Allure attachment."""

import logging
from datetime import datetime
from pathlib import Path

import allure


def get_test_output_dir(test_name: str) -> Path:
    """Creates and returns a timestamped output directory for a test.

    Args:
        test_name (str): Name of the test, used as the folder prefix.

    Returns:
        Path: Created output directory path.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    folder_name = f"{test_name}_{timestamp}"
    output_dir = Path("artifacts") / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def attach_file_handler(output_dir: Path) -> logging.FileHandler:
    """Attaches a file handler to the root logger for per-test log capture.

    Also ensures the root logger level is set to DEBUG so all messages
    reach the handler regardless of the default logger configuration.

    Args:
        output_dir (Path): Directory where test.log will be written.

    Returns:
        logging.FileHandler: The attached handler — pass to detach_file_handler
            at teardown.
    """
    log_path = output_dir / "test.log"
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)
    return handler


def detach_file_handler(handler: logging.FileHandler) -> None:
    """Removes the file handler from the root logger and closes the log file.

    Args:
        handler (logging.FileHandler): The handler returned by attach_file_handler.
    """
    logging.getLogger().removeHandler(handler)
    handler.close()


def attach_log_to_allure(output_dir: Path) -> None:
    """Attaches the test.log file to the Allure report for the current test.

    Call this after detach_file_handler to ensure the file is fully written
    before attachment.

    Args:
        output_dir (Path): Directory containing the test.log file.
    """
    log_path = output_dir / "test.log"
    if log_path.exists():
        allure.attach.file(
            str(log_path),
            name="test.log",
            attachment_type=allure.attachment_type.TEXT,
        )
