"""This file contains DataReader class for reading test data files."""

import csv
import json
import os

from src.utils.exceptions import TestDataException


class DataReader:
    """Reads test data from CSV and JSON files.

    Args:
        data_dir (str): Path to the test data directory. Defaults to 'test_data'.
    """

    def __init__(self, data_dir: str = "test_data"):
        self.data_dir = data_dir

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
            raise TestDataException(file_path, "file not found")
        return file_path

    def read_csv(self, file_name: str) -> list[dict]:
        """Reads a CSV file and returns a list of dictionaries.

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
                return list(reader)
        except csv.Error as err:
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
                return json.load(file)
        except json.JSONDecodeError as err:
            raise TestDataException(file_name, str(err))
