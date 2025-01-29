""" etl_tmdb.py
@author: Joseph A.
Description: This script extracts data from the TMDB API about Netflix movies and series.
"""

# Libraries
import os
import json
from datetime import datetime, timedelta
import requests
# Others
import psycopg2
from dotenv import load_dotenv
from pymongo import MongoClient
# Airflow Libraries
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Bypass proxy for TMDB API
os.environ['NO_PROXY'] = '*'

# Configuration
load_dotenv()
LOGGER = LoggingMixin().log

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
OUTPUT_DIR = 'tmdb_data'
PROVIDER_ID = 8
WATCH_REGION = 'FR'

# Create the output directory if does not exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Functions
def extract_netflix_data():
    """Extract Netflix data from TMDB API"""
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

        # Movies
        url = f'{TMDB_BASE_URL}/discover/movie'
        LOGGER.info(f"🔄 Request for movies - Page {page}")

        try:
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

def load_to_postgres():
    """Load the data into the Postgres database"""
    LOGGER.info("🚚 Launch of the loading of the extracted data into the Postgres database")
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    # Load movies
    with open(f'{OUTPUT_DIR}/netflix_movies.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)

    for movie in movies:
        cursor.execute(
            """
            INSERT INTO movies (title, release_date, rating, genre, tmdb_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
                (movie['title'], movie['release_date'],movie['vote_average'], ", ".join([g["name"] for g in movie["genres"]]), movie['id'])
            )
        LOGGER.info(f'✅ {len(movies)} movies loaded into the database')
    
    conn.commit()
    cursor.close()
    conn.close()
    LOGGER.info('✅ Loading complete')

def load_to_mongo():
    """Load the data into the MongoDB database"""
    LOGGER.info("🚚 Launch of the loading of the extracted data into the MongoDB database")
    client = MongoClient('mongodb://localhost:27017/')
    db = client['streamlytics']
    collection_movies = db['movies']
    collection_series = db['series']
    
    # Load movies
    with open(f'{OUTPUT_DIR}/netflix_movies.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)
    with open(f'{OUTPUT_DIR}/netflix_series.json', 'r', encoding='utf-8') as f:
        series = json.load(f)
    
    if movies:
        collection_movies.insert_many(movies)
        LOGGER.info(f'✅ {len(movies)} movies loaded into the database')
    if series:  
        collection_series.insert_many(series)
        LOGGER.info(f'✅ {len(series)} series loaded into the database')

# DAG Arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    #'max_active_runs': 1
}

# DAG Definition
dag = DAG(
    'etl_tmdb_netflix',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    #max_active_runs=1 # Only one DAG run at a time
)

# Tasks
extract_task = PythonOperator(
    task_id='extract_netflix_data',
    python_callable=extract_netflix_data,
    dag=dag
)

load_postgres_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    dag=dag
)

load_mongo_task = PythonOperator(
    task_id='load_to_mongo',
    python_callable=load_to_mongo,
    dag=dag
)

# Task dependencies
extract_task >> [load_postgres_task, load_mongo_task]
