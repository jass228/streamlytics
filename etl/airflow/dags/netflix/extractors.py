"""
@author: Joseph A.
Description: This script extracts data from the TMDB API about Netflix movies and series.
"""
import json
import requests
from .config import TMDB_API_KEY, PROVIDER_ID, WATCH_REGION, TMDB_BASE_URL, OUTPUT_DIR, LOGGER

def extract_netflix_data():
    """Extract data from the TMDB API about Netflix movies and series.
    """
    LOGGER.info("🎬 Launch of extraction of Netflix films and series data from TMDB API")
    netflix_movies = []
    netflix_series = []

    for page in range(1, 6): # We will get the first 5 pages (20 movies per page)
        params = {
            'api_key': TMDB_API_KEY,
            'with_watch_providers': PROVIDER_ID,
            'watch_region': WATCH_REGION,
            'page': page
        }

        try:
            # Movies
            url = f'{TMDB_BASE_URL}/discover/movie'
            LOGGER.info(f"🔄 Request for movies - Page {page}")

            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                error_msg = f"❌ Error while getting movies - Page {page}: {response.status_code}"
                LOGGER.error(error_msg)
                raise ValueError(error_msg)

            data = response.json()
            netflix_movies.extend(data['results'])
            LOGGER.info(f"✅ Recovered movies -  Page {page}: {len(data['results'])} movies")

            # Tv Shows
            url_series = f'{TMDB_BASE_URL}/discover/tv'
            LOGGER.info(f"🔄 Request for tv show - Page {page}")

            response_tv = requests.get(url_series, params=params, timeout=10)
            if response_tv.status_code != 200:
                error_msg = f"❌ Error while getting series - Page {page}: {response_tv.status_code}"
                LOGGER.error(error_msg)
                raise ValueError(error_msg)

            data_series = response_tv.json()
            netflix_series.extend(data_series['results'])
            LOGGER.info(f"✅ Recovered tv show -  Page {page}: {len(data_series['results'])} series")
        except Exception as e:
            LOGGER.error(f"❌ Error during API request: {str(e)}")
            raise

    # Save the data
    if netflix_movies:
        with open(f'{OUTPUT_DIR}/netflix_movies.json', 'w', encoding='utf-8') as f:
            json.dump(netflix_movies, f)
        LOGGER.info(f'✅ {len(netflix_movies)} movies save in netflix_movies.json')
    else:
        LOGGER.warning('❌ No movies found')

    if netflix_series:
        with open(f'{OUTPUT_DIR}/netflix_series.json', 'w', encoding='utf-8') as f:
            json.dump(netflix_series, f)
        LOGGER.info(f'✅ {len(netflix_series)} series save in netflix_series.json')
    else:
        LOGGER.warning('❌ No series found')

    LOGGER.info(f'✅ Extraction complete : {len(netflix_movies)} movies, {len(netflix_series)} tv')
