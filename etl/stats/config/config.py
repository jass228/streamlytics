"""
@author: Joseph A.
Description: This script contains the configuration.
"""
import os
from dotenv import load_dotenv
# Database
from sqlalchemy import create_engine

# Configs
load_dotenv()

# PostgreSQL
POSTGRES_URL = os.getenv('POSTGRES_URL')
engine = create_engine(POSTGRES_URL)

# TMDB API
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
