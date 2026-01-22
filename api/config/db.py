"""
@author: Joseph A.
Description: This script contains the configuration of the API.
"""
import os
from dotenv import load_dotenv
from databases import Database
from sqlalchemy import create_engine, MetaData

# Configuration
load_dotenv()

# PostgreSQL - Use DATABASE_URL (Supabase) if available, fallback to POSTGRES_URL
POSTGRES_URL = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')

# Disable prepared statement cache for PgBouncer compatibility (Supabase)
database = Database(
    POSTGRES_URL,
    min_size=1,
    max_size=5,
    statement_cache_size=0
)
engine = create_engine(POSTGRES_URL)
metadata = MetaData()
