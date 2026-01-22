"""
@author: Joseph A.
Description: This script contains the configuration of the project.
"""
import os
from dotenv import load_dotenv
from airflow.utils.log.logging_mixin import LoggingMixin

# Bypass proxy for TMDB API
os.environ['NO_PROXY'] = '*'

# Configuration - load .env from etl directory
ETL_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv(os.path.join(ETL_DIR, '.env'))
LOGGER = LoggingMixin().log

# TMDB API
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
PROVIDER_ID = 8
WATCH_REGION = 'FR'

# Output directory (absolute path)
OUTPUT_DIR = os.path.join(ETL_DIR, 'tmdb_data')

# Databases
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
MONGO_DB_HOST = os.getenv('MONGO_DB_HOST')
POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME')
DATABASE_URL = os.getenv('DATABASE_URL')

# Create the output directory if does not exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
