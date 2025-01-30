"""
@author: Joseph A.
Description: This script checks if the JSON files have the required keys.
"""
import os
import json

def check_json_structure(file_path, required_keys):
    """Check if the JSON file has the required keys"""
    if not os.path.exists(file_path):
        print(f"❌ The file {file_path} does not exist")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print(f"❌ The file {file_path} is not a JSON object")
            return False

        for item in data[:5]:
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                print(f"❌ The file {file_path} does not have the keys: {missing_keys}")
                return False

        print(f"✅ The file {file_path} has the required keys")
        return True
    except (OSError, json.JSONDecodeError) as e:
        print(f"❌ Error while reading the file {file_path}: {str(e)}")
        return False

required_keys_movies = ['id', 'title', 'release_date', 'vote_average', 'genre_ids']
required_keys_series = ['id', 'name', 'first_air_date', 'vote_average', 'genre_ids']

check_json_structure('./tmdb_data/netflix_movies.json', required_keys_movies)
check_json_structure('./tmdb_data/netflix_series.json', required_keys_series)
