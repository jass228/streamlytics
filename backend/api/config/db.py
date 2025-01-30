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

# PostgreSQL
POSTGRES_URL = os.getenv('POSTGRES_URL')
database = Database(POSTGRES_URL)
engine = create_engine(POSTGRES_URL)
metadata = MetaData()
