"""
@author: Joseph A.
Description: Utility functions for saving statistical data to JSON files and Supabase
"""
import os
import json
import psycopg2
from psycopg2.extras import Json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
ETL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(ETL_DIR, '.env'))
DATABASE_URL = os.getenv('DATABASE_URL')

def save_json_data(data, filename: str, base_path: str, data_type: str = 'distribution'):
    """Save pandas data (Series or DataFrame) to a JSON file.

    Args:
        data (Union[pd.Series, pd.DataFrame]): Data to save:
            - Series for distribution data
            - DataFrame for ratings data (must have 'mean' and 'count' columns)
        filename (str): Name of the output file (without extension)
        base_path (str): Directory path where to save the JSON file
        data_type (str, optional):Type of data to save ('distribution' or 'ratings'). 
            Defaults to 'distribution'.

    Raises:
        ValueError: If data_type is 'ratings' but DataFrame doesn't have required columns
    """
    os.makedirs(base_path, exist_ok=True)

    if data_type == 'distribution':
        json_data = {
            'data': data.to_dict(),
            'total': int(data.sum()),
            'count': len(data)
        }
    else:  # ratings
        if not all(col in data.columns for col in ['mean', 'count']):
            raise ValueError("Ratings DataFrame must have 'mean' and 'count' columns")

        json_data = {
            'data': data.round(2).to_dict(orient='index'),
            'total_ratings': int(data['count'].sum()),
            'average_rating': float(data['mean'].mean().round(2))
        }

    with open(os.path.join(base_path, f'{filename}.json'), 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)


def save_to_supabase(data, stat_type: str, media_type: str, data_type: str = 'distribution'):
    """Save statistical data to Supabase stats table.

    Args:
        data (Union[pd.Series, pd.DataFrame]): Data to save
        stat_type (str): Type of statistic (e.g., 'genre_distribution', 'country_avg_ratings')
        media_type (str): 'movies' or 'series'
        data_type (str, optional): Type of data ('distribution' or 'ratings'). Defaults to 'distribution'.
    """
    if data_type == 'distribution':
        json_data = {
            'data': data.to_dict(),
            'total': int(data.sum()),
            'count': len(data)
        }
    else:  # ratings
        json_data = {
            'data': data.round(2).to_dict(orient='index'),
            'total_ratings': int(data['count'].sum()),
            'average_rating': float(data['mean'].mean().round(2))
        }

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO stats (stat_type, media_type, data, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (stat_type, media_type)
            DO UPDATE SET data = EXCLUDED.data, created_at = EXCLUDED.created_at
        """, (stat_type, media_type, Json(json_data), datetime.now()))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
