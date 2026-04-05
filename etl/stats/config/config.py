"""
@author: Joseph A.
Description: This script contains the configuration.
"""
import os
from dotenv import load_dotenv
# Database
from sqlalchemy import create_engine

# Configs - load .env from etl directory
ETL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(ETL_DIR, '.env'))

# PostgreSQL - Use DATABASE_URL (Neon) if available, fallback to POSTGRES_URL
POSTGRES_URL = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
engine = create_engine(POSTGRES_URL)

# TMDB API
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
