"""
@author: Joseph A.
Description: Service class for handling statistical data operations and file access
"""
import os
import json
import dataclasses

@dataclasses.dataclass
class StatisticsService:
    """Service class that provides methods to read and parse statistical data from JSON files.
    """
    def __init__(self):
        self.base_path = os.path.join("..", "stats", "db", "api", "latest")

    async def get_json_data(self, filename: str):
        """Read and return data from a JSON file.

        Args:
            filename (str): Name of the JSON file without extension

        Returns:
            Dict[str, Any]: JSON data that can be either:
                - Distribution data containing:
                    - data: Dictionary of item counts
                    - total: Total number of items
                    - count: Number of unique items
                OR
                - Ratings data containing:
                    - data: Dictionary of ratings with mean and count per item
                    - total_ratings: Total number of ratings
                    - average_rating: Overall average rating

        Raises:
            FileNotFoundError: If the specified JSON file doesn't exist
            ValueError: If the JSON file is invalid or cannot be parsed
        """
        filepath = os.path.join(self.base_path, f"{filename}.json")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"File not found: {filepath}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON decoding error: {filepath}") from exc
