"""This file contains DataReader class for reading test data files"""

import csv
import json
import os


class DataReader:
    """Reads test data from CSV and JSON files.
    Args:
        data_dir (str): Path to the test data directory. Defaults to 'test_data'
    """

    def __init__(self, data_dir="test_data"):
        self.data_dir = data_dir

    def _get_file_path(self, filename):
        """Builds and validates the full file path.
        Args:
            filename (str): Name of the file to read
        Returns:
            str: Full path to the file
        """
        file_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Test data file not found at: {file_path}")
        return file_path

    def read_csv(self, file_name):
        """Reads a CSV file and returns list of dictionaries.
        Each row becomes a dictionary where keys are column headers.
        Args:
            file_name (str): Name of the CSV file
        Returns:
            list: List of dictionaries, one per row
        """
        file_path = self._get_file_path(file_name)
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except csv.Error as err:
            raise ValueError(f"Error reading CSV file {file_name}: {err}")

    def read_json(self, file_name):
        """Reads a JSON file and returns parsed data.
        Args:
            file_name (str): Name of the JSON file
        Returns:
            dict or list: Parsed JSON data
        """
        file_path = self._get_file_path(file_name)
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as err:
            raise ValueError(f"Error reading JSON file {file_name}: {err}")
