"""
@author: Joseph A.
Description: Script for analyzing movies and TV series data, generating statistical distributions 
and ratings, and saving them in JSON format both as daily snapshots and latest versions.
"""
import os
from datetime import datetime
import pandas as pd
from utils.data_processing import count_split_data, explode_split_data
from utils.save_data import save_json_data, save_to_supabase

# pylint: disable=C0103:invalid-name

def get_distribution(df_series:pd.DataFrame, df_movies:pd.DataFrame, column_name:str):
    """Get distribution counts for a specific column across movies and TV series.

    Args:
        df_series (pd.DataFrame): DataFrame containing TV series data
        df_movies (pd.DataFrame): DataFrame containing movie data
        column_name (str): Name of the column to analyze

    Returns:
        tuple: (movie_distribution, series_distribution) where each is a pd.Series of value counts
    """
    c_m_d = count_split_data(df_movies, column_name)
    c_s_d = count_split_data(df_series, column_name)
    return c_m_d, c_s_d

def get_year(df:pd.DataFrame):
    """Extract year from release date and add it as a new column.

    Args:
        df (pd.DataFrame): DataFrame containing a 'release_date' column

    Returns:
        pd.DataFrame: DataFrame with additional 'year' column
    """
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['year'] = df['release_date'].dt.year
    return df

def year_distribution(df_series:pd.DataFrame, df_movies:pd.DataFrame, column_name:str):
    """Get yearly distribution of movies and TV series.

    Args:
        df_series (pd.DataFrame): DataFrame containing TV series data
        df_movies (pd.DataFrame): DataFrame containing movie data
        column_name (str): Name of the column containing year data

    Returns:
        tuple: (movie_year_counts, series_year_counts) 
        where each is a pd.Series of yearly counts
    """
    y_m_d = df_movies[column_name].value_counts().sort_index()
    y_s_d = df_series[column_name].value_counts().sort_index()
    return y_m_d, y_s_d

def get_ratings(df, column_name:str):
    """Calculate average ratings and counts by category.

    Args:
        df (_type_): DataFrame containing rating data
        column_name (str): Name of the column to group by

    Returns:
        pd.DataFrame: DataFrame with 'mean' and 'count' columns, filtered for count >= 3
    """
    ratings_values = df.groupby(column_name)['rating'].agg(['mean', 'count'])
    ratings_values = ratings_values[ratings_values['count'] >= 3]
    ratings_values = ratings_values.sort_values('mean', ascending=False)
    return ratings_values


def get_avg_ratings(df_series:pd.DataFrame, df_movies:pd.DataFrame, column_name:str):
    """Get average ratings for movies and TV series by category.

    Args:
        df_series (pd.DataFrame): DataFrame containing TV series data
        df_movies (pd.DataFrame): DataFrame containing movie data
        column_name (str): Name of the column to analyze

    Returns:
        tuple: (movie_ratings, series_ratings) where each is a pd.DataFrame with ratings stats
    """
    df_movie_explode = explode_split_data(df_movies, column_name)
    df_serie_explode = explode_split_data(df_series, column_name)

    m_a_r = get_ratings(df_movie_explode, column_name)
    s_a_r = get_ratings(df_serie_explode, column_name)

    return m_a_r, s_a_r

# Load latest data
base_path = os.path.join('db', 'clean', 'latest')
movie_filename = f"{base_path}/movie_latest.csv"
serie_filename = f"{base_path}/serie_latest.csv"

df_movie = pd.read_csv(movie_filename)
df_tv = pd.read_csv(serie_filename)

# Create working copies and add year data
df_movie_copy = df_movie.copy()
df_tv_copy = df_tv.copy()

df_movie_copy = get_year(df_movie_copy)
df_tv_copy = get_year(df_tv_copy)

# Generate distributions and ratings
# Distribution of media by country
country_movies_distribution, country_series_distribution = get_distribution(df_tv, df_movie,
                                                                            'country_code_3')
# Analysis of media genres
genres_movies_distribution, genres_series_distribution = get_distribution(df_tv, df_movie, 'genre')
# Media releases over time
yearly_counts_movies, yearly_counts_series = year_distribution(df_tv_copy, df_movie_copy, 'year')
# Average score by country
country_avg_ratings_movies, country_avg_ratings_series = get_avg_ratings(df_tv_copy, df_movie_copy,
                                                                        'country_name')
# Average score by genres
genres_avg_ratings_movies, genres_avg_ratings_series = get_avg_ratings(df_tv_copy, df_movie_copy,
                                                                    'genre')

# Setup paths for saving data
base_path = os.path.join("db", "api")
current_year = datetime.now().strftime("%Y")
current_month = datetime.now().strftime("%m")
current_date = datetime.now().strftime("%d_%m_%y")
dir_name = f"{current_month}_{current_year}"

db_path = os.path.join(base_path, current_year, dir_name)
latest_path = os.path.join(base_path, 'latest')

# Save daily snapshots
save_json_data(country_movies_distribution, f"country_movies_distribution_{current_date}", db_path)
save_json_data(country_series_distribution, f"country_series_distribution_{current_date}", db_path)
save_json_data(genres_movies_distribution, f"genres_movies_distribution_{current_date}", db_path)
save_json_data(genres_series_distribution, f"genres_series_distribution_{current_date}", db_path)
save_json_data(yearly_counts_movies, f"yearly_counts_movies_{current_date}", db_path)
save_json_data(yearly_counts_series, f"yearly_counts_series_{current_date}", db_path)
save_json_data(country_avg_ratings_movies, f"country_avg_ratings_movies_{current_date}",
            db_path, 'ratings')
save_json_data(country_avg_ratings_series, f"country_avg_ratings_series_{current_date}",
            db_path, 'ratings')
save_json_data(genres_avg_ratings_movies, f"genres_avg_ratings_movies_{current_date}",
            db_path, 'ratings')
save_json_data(genres_avg_ratings_series, f"genres_avg_ratings_series_{current_date}",
            db_path, 'ratings')

# Save latest versions
save_json_data(country_movies_distribution, "country_movies_distribution_latest", latest_path)
save_json_data(country_series_distribution, "country_series_distribution_latest", latest_path)
save_json_data(genres_movies_distribution, "genres_movies_distribution_latest", latest_path)
save_json_data(genres_series_distribution, "genres_series_distribution_latest", latest_path)
save_json_data(yearly_counts_movies, "yearly_counts_movies_latest", latest_path)
save_json_data(yearly_counts_series, "yearly_counts_series_latest", latest_path)
save_json_data(country_avg_ratings_movies, "country_avg_ratings_movies_latest",
            latest_path, 'ratings')
save_json_data(country_avg_ratings_series, "country_avg_ratings_series_latest",
            latest_path, 'ratings')
save_json_data(genres_avg_ratings_movies, "genres_avg_ratings_movies_latest",
            latest_path, 'ratings')
save_json_data(genres_avg_ratings_series, "genres_avg_ratings_series_latest",
            latest_path, 'ratings')

# Save to Supabase
print("Saving statistics to Supabase...")
save_to_supabase(country_movies_distribution, 'country_distribution', 'movies')
save_to_supabase(country_series_distribution, 'country_distribution', 'series')
save_to_supabase(genres_movies_distribution, 'genre_distribution', 'movies')
save_to_supabase(genres_series_distribution, 'genre_distribution', 'series')
save_to_supabase(yearly_counts_movies, 'yearly_distribution', 'movies')
save_to_supabase(yearly_counts_series, 'yearly_distribution', 'series')
save_to_supabase(country_avg_ratings_movies, 'country_avg_ratings', 'movies', 'ratings')
save_to_supabase(country_avg_ratings_series, 'country_avg_ratings', 'series', 'ratings')
save_to_supabase(genres_avg_ratings_movies, 'genre_avg_ratings', 'movies', 'ratings')
save_to_supabase(genres_avg_ratings_series, 'genre_avg_ratings', 'series', 'ratings')
print("Statistics saved to Supabase successfully!")
