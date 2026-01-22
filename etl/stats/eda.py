"""
@author: Joseph A.
Script for extracting media data from database, enriching it with country information, 
and saving both daily and latest snapshots.
"""
import os
from datetime import datetime
import pandas as pd
from utils.enrich import enrich_dataframe
from config.config import engine

# pylint: disable=C0103:invalid-name

# Database extraction queries
QUERY_MOVIE = 'SELECT * FROM movies;'
QUERY_SERIE = 'SELECT * FROM series;'

data_movie = pd.read_sql_query(QUERY_MOVIE, engine)
data_serie = pd.read_sql_query(QUERY_SERIE, engine)

# Standardize column names
data_serie = data_serie.rename(columns={'first_air_date': 'release_date'})

# Create copies for processing
df_series = data_serie.copy()
df_movies = data_movie.copy()

# Enrich data with country information
df_series = enrich_dataframe(df_series, 'tv')
print("") # Visual separator
df_movies = enrich_dataframe(df_movies, 'movie')

# Setup paths and filenames for saving data
current_year = datetime.now().strftime("%Y")
current_month = datetime.now().strftime("%m")
current_date = datetime.now().strftime("%d_%m_%y")
dir_name = f"{current_month}_{current_year}"

# Define storage paths
db_path = os.path.join('db', 'clean', current_year, dir_name)
latest_path = os.path.join('db', 'clean', 'latest')

# Create storage directories
os.makedirs(db_path, exist_ok=True)
os.makedirs(latest_path, exist_ok=True)

# Save daily snapshots and latest versions
df_movies.to_csv(f"{db_path}/movie_{current_date}.csv", index=False)
df_series.to_csv(f"{db_path}/serie_{current_date}.csv", index=False)
df_movies.to_csv(f"{latest_path}/movie_latest.csv", index=False)
df_series.to_csv(f"{latest_path}/serie_latest.csv", index=False)
