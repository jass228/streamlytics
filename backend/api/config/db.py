"""
@author: Joseph A.
Description: This script contains the configuration of the API.
"""
import os
from dotenv import load_dotenv
import psycopg2

# Configuration
load_dotenv()

# PostgreSQL
db = psycopg2.connect(
    user=os.getenv("user"),
    password=os.getenv("password"),
    host=os.getenv("host"),
    port=os.getenv("port"),
    dbname=os.getenv("dbname")
)
