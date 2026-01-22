"""
@author: Joseph A.
Description: Service class for handling statistical data operations from Supabase
"""
import json
import dataclasses
from config.db import database

# Mapping from old filename to (stat_type, media_type)
STAT_MAPPING = {
    "country_movies_distribution_latest": ("country_distribution", "movies"),
    "country_series_distribution_latest": ("country_distribution", "series"),
    "genres_movies_distribution_latest": ("genre_distribution", "movies"),
    "genres_series_distribution_latest": ("genre_distribution", "series"),
    "yearly_counts_movies_latest": ("yearly_distribution", "movies"),
    "yearly_counts_series_latest": ("yearly_distribution", "series"),
    "country_avg_ratings_movies_latest": ("country_avg_ratings", "movies"),
    "country_avg_ratings_series_latest": ("country_avg_ratings", "series"),
    "genres_avg_ratings_movies_latest": ("genre_avg_ratings", "movies"),
    "genres_avg_ratings_series_latest": ("genre_avg_ratings", "series"),
}


@dataclasses.dataclass
class StatisticsService:
    """Service class that provides methods to read statistical data from Supabase.
    """

    async def get_json_data(self, filename: str):
        """Read and return statistical data from Supabase.

        Args:
            filename (str): Legacy filename pattern (for backward compatibility)

        Returns:
            Dict[str, Any]: JSON data containing statistics

        Raises:
            ValueError: If the filename is not recognized
            Exception: If there's an error fetching from database
        """
        if filename not in STAT_MAPPING:
            raise ValueError(f"Unknown stat type: {filename}")

        stat_type, media_type = STAT_MAPPING[filename]

        query = """
            SELECT data FROM stats
            WHERE stat_type = :stat_type AND media_type = :media_type
        """
        result = await database.fetch_one(
            query=query,
            values={"stat_type": stat_type, "media_type": media_type}
        )

        if result is None:
            raise ValueError(f"No data found for {stat_type}/{media_type}")

        data = result["data"]
        # Parse JSON if data is a string (JSONB might be returned as string)
        if isinstance(data, str):
            return json.loads(data)
        return data
