"""Manages per-test log file setup and teardown."""

import logging
from datetime import datetime
from pathlib import Path


def get_test_output_dir(test_name: str) -> Path:
    """Creates and returns a timestamped output directory for a test."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    folder_name = f"{test_name}_{timestamp}"
    output_dir = Path("artifacts") / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def attach_file_handler(output_dir: Path) -> logging.FileHandler:
    """Attaches a file handler to the root logger for per-test log capture."""
    log_path = output_dir / "test.log"
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logging.getLogger()
    logging.getLogger().addHandler(handler)
    return handler


def detach_file_handler(handler: logging.FileHandler) -> None:
    """Removes the file handler from the root logger."""
    logging.getLogger().removeHandler(handler)
    handler.close()
