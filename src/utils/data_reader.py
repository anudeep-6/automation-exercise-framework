"""Reads test data from CSV and JSON files in the test_data directory."""

import csv
import json
import logging
import os
from typing import Optional

from src.utils.exceptions import TestDataException

logger = logging.getLogger(__name__)


class DataReader:
    """Reads test data from CSV and JSON files."""

    def __init__(self, data_dir: str = "test_data") -> None:
        """Initialises DataReader with the test data directory.

        Args:
            data_dir (str): Path to the test data directory.
                Defaults to 'test_data'.
        """
        self.data_dir = data_dir
        logger.info("[DATA] DataReader initialised — data_dir: %s", data_dir)

    def _get_file_path(self, file_name: str) -> str:
        """Builds and validates the full file path.

        Args:
            file_name (str): Name of the file to read.

        Returns:
            str: Full path to the file.

        Raises:
            TestDataException: If the file does not exist at the resolved path.
        """
        file_path = os.path.join(self.data_dir, file_name)
        if not os.path.exists(file_path):
            logger.error("[DATA] File not found: %s", file_path)
            raise TestDataException(file_path, "file not found")
        return file_path

    def read_csv(self, file_name: str) -> list[dict]:
        """Reads a CSV file and returns a list of row dictionaries.

        Each row becomes a dictionary where keys are column headers.

        Args:
            file_name (str): Name of the CSV file.

        Returns:
            list[dict]: List of dictionaries, one per row.

        Raises:
            TestDataException: If the file is malformed or unreadable.
        """
        file_path = self._get_file_path(file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                rows = list(reader)
            if not rows:
                logger.warning("[DATA] CSV file is empty (no data rows): %s", file_name)
            else:
                logger.info("[DATA] CSV loaded — %s: %d rows", file_name, len(rows))
            return rows
        except csv.Error as err:
            logger.error("[DATA] Failed to parse CSV %s: %s", file_name, err)
            raise TestDataException(file_name, str(err))

    def read_json(self, file_name: str) -> dict | list:
        """Reads a JSON file and returns parsed data.

        Args:
            file_name (str): Name of the JSON file.

        Returns:
            dict | list: Parsed JSON data.

        Raises:
            TestDataException: If the file contains invalid JSON.
        """
        file_path = self._get_file_path(file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            logger.info("[DATA] JSON loaded — %s", file_name)
            return data
        except json.JSONDecodeError as err:
            logger.error("[DATA] Failed to parse JSON %s: %s", file_name, err)
            raise TestDataException(file_name, str(err))

    def load_csv_rows(
        self, file_name: str, filter_by: Optional[dict] = None
    ) -> list[dict]:
        """Loads CSV rows with optional column-based filtering.

        A convenience wrapper over read_csv() that filters rows by one or more
        column values without requiring manual list comprehension in test files.

        Args:
            file_name (str): Name of the CSV file to read.
            filter_by (dict, optional): Column-value pairs to filter rows by.
                Only rows matching ALL specified key-value pairs are returned.
                Defaults to None, which returns all rows unfiltered.

        Returns:
            list[dict]: Filtered list of row dictionaries.

        Raises:
            TestDataException: If the file does not exist or is malformed.
        """
        rows = self.read_csv(file_name)
        if filter_by:
            rows = [
                row
                for row in rows
                if all(row.get(k) == v for k, v in filter_by.items())
            ]
            logger.info(
                "[DATA] load_csv_rows — %s: %d rows after filter %s",
                file_name,
                len(rows),
                filter_by,
            )
        return rows
