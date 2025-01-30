"""
@author: Joseph A.
Description: This script loads the extracted data into the databases.
"""
import json
from functools import lru_cache
import requests
from pymongo import MongoClient, UpdateOne
from airflow.providers.postgres.hooks.postgres import PostgresHook

from .config import (TMDB_BASE_URL, TMDB_API_KEY, OUTPUT_DIR, LOGGER,
                    POSTGRES_DB_NAME, MONGO_DB_HOST, MONGO_DB_NAME)

@lru_cache(maxsize=None) # Cache the result of the function
def get_genres():
    """Get the genres of a media type

    Returns:
        dict: A dictionary of genres
    """
    url = f'{TMDB_BASE_URL}/genre'
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'fr'
    }

    genres_data = {}

    try:
        # Get the genres of movies
        response_movie = requests.get(f'{url}/movie/list', params=params, timeout=10)
        genres_data['movie'] = {genre['id']: genre['name']
                    for genre in response_movie.json().get('genres', [])}

        # Get the genres of tv shows
        response_tv = requests.get(f'{url}/tv/list', params=params, timeout=10)
        genres_data['tv'] = {genre['id']: genre['name']
                            for genre in response_tv.json().get('genres', [])}
    except Exception as e:
        LOGGER.error(f"❌ Error during API request: {str(e)}")
        raise e

    return genres_data

def load_to_postgres():
    """Load the data into the Postgres database
    """
    LOGGER.info("🚚 Launch of the loading of the extracted data into the Postgres database")

    genres_data = get_genres() # Get the genres of movies and tv shows

    pg_hook = PostgresHook(postgres_conn_id=POSTGRES_DB_NAME)
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    try:
        # Load movies
        with open(f'{OUTPUT_DIR}/netflix_movies.json', 'r', encoding='utf-8') as f:
            movies = json.load(f)

        movies_data = [(
            movie["title"],
            movie["release_date"],
            movie["vote_average"],
            ", ".join([genres_data['movie'].get(g, "") for g in movie["genre_ids"]]),
            movie["id"],
            movie["original_language"],
            movie["poster_path"]
            ) for movie in movies]

        cursor.executemany(
            """
            INSERT INTO movies (
                title, release_date, rating, genre, tmdb_id,
                original_language, poster_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (tmdb_id) DO NOTHING
            """,
            movies_data
        )
        LOGGER.info(f'✅ {len(movies)} movies loaded into the database')

        # Load series
        with open(f'{OUTPUT_DIR}/netflix_series.json', 'r', encoding='utf-8') as f:
            series = json.load(f)

        series_data = [(
            serie["name"],
            serie["first_air_date"],
            serie["vote_average"],
            ", ".join([genres_data['tv'].get(g, "") for g in serie["genre_ids"]]),
            serie["id"],
            serie["original_language"],
            serie["poster_path"]
            ) for serie in series]

        cursor.executemany(
            """
            INSERT INTO series (
                title, first_air_date, rating, genre, tmdb_id,
                original_language, poster_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (tmdb_id) DO NOTHING
            """,
            series_data
        )
        LOGGER.info(f'✅ {len(series)} series loaded into the database')

        conn.commit()
    except Exception as e:
        LOGGER.error(f"❌ Error during loading: {str(e)}")
        raise e
    finally:
        cursor.close()
        conn.close()

    LOGGER.info('✅ Loading complete')

def load_to_mongo():
    """Load the data into the MongoDB database
    """
    LOGGER.info("🚚 Launch of the loading of the extracted data into the MongoDB database")

    try:
        client = MongoClient(MONGO_DB_HOST)
        db = client[MONGO_DB_NAME]
        collection_movies = db['movies']
        collection_series = db['series']

        # Load movies
        with open(f'{OUTPUT_DIR}/netflix_movies.json', 'r', encoding='utf-8') as f:
            movies = json.load(f)
        with open(f'{OUTPUT_DIR}/netflix_series.json', 'r', encoding='utf-8') as f:
            series = json.load(f)

        if movies:
            try:
                # Add the tmdb_id field
                movies_data = [{**movie, "tmdb_id": movie["id"]}
                            for movie in movies if "id" in movie]

                bulk_operations = [
                    UpdateOne(
                        {"tmdb_id": movie["tmdb_id"]},
                        {"$set": movie},
                        upsert=True
                    ) for movie in movies_data
                ]

                if bulk_operations:
                    collection_movies.bulk_write(bulk_operations, ordered=False)
                    LOGGER.info(f'✅ {len(movies)} movies loaded into the database')
            except Exception as e:
                LOGGER.error(f"❌ Error during loading: {str(e)}")
                raise e

        if series:
            try:
                series_data = [{**serie, "tmdb_id": serie["id"]}
                            for serie in series if "id" in serie]

                bulk_operations = [
                    UpdateOne(
                        {"tmdb_id": serie["tmdb_id"]},
                        {"$set": serie},
                        upsert=True
                    ) for serie in series_data
                ]

                if bulk_operations:
                    collection_series.bulk_write(bulk_operations, ordered=False)
                    LOGGER.info(f'✅ {len(series)} series loaded into the database')
            except Exception as e:
                LOGGER.error(f"❌ Error during loading: {str(e)}")
                raise e
    except Exception as e:
        LOGGER.error(f"❌ Error during loading: {str(e)}")
        raise e
    finally:
        client.close()
