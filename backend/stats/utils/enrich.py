"""
@author: Joseph A.
Description: Utilities for enriching media data with country information from TMDB API
"""
import pandas as pd
import requests
import pycountry
from tqdm import tqdm
# My Libraries
from config.config import TMDB_API_KEY, TMDB_BASE_URL

def convert_country_code_to_name(country_code:str):
    """Convert a two-letter country code to its full country name.

    Args:
        country_code (str): Two-letter ISO 3166-1 alpha-2 country code

    Returns:
        str: Full name of the country, or:
            - Special case name for certain countries
            - Original code if country cannot be found
    """
    special_cases = {
        "KR": "South Korea",
        "RU": "Russia",
        "VN": "Vietnam",
        "IR": "Iran",
        "TW": "Taiwan",
    }
    try:
        if country_code in special_cases:
            return special_cases[country_code]
        country = pycountry.countries.get(alpha_2=country_code)
        return country.name if country else None
    except KeyError:
        return country_code

def get_media_origin_country(tmdb_id: int, media: str):
    """Fetch origin country information for a media item from TMDB API.

    Args:
        tmdb_id (int): TMDB ID of the media item
        media (str): Type of media ('movie' or 'tv')

    Returns:
        tuple: A pair of (country_codes, country_names) where:
            - country_codes (str): Comma-separated list of country codes
            - country_names (str): Comma-separated list of country names
            - Returns (None, None) if no country information is found
    """
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'fr-FR'
    }
    url = f'{TMDB_BASE_URL}/{media}/{tmdb_id}'

    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        print(f"Error while getting {media}: {response.status_code}")
        return []

    data = response.json()
    origin_countries = data.get("origin_country", [])

    if origin_countries:
        country_codes = origin_countries
        country_names = [convert_country_code_to_name(code) for code in origin_countries]

        country_codes_str = ", ".join(country_codes)
        country_names_str = ", ".join(country_names)

        return country_codes_str, country_names_str
    return None, None

def enrich_dataframe(df:pd.DataFrame, media:str):
    """Enrich a DataFrame with country information for each media item.

    Args:
        df (pd.DataFrame): DataFrame containing media information with tmdb_id column
        media (str): Type of media ('movie' or 'tv')

    Returns:
        pd.DataFrame: Enriched DataFrame with additional columns:
            - country_code: Comma-separated list of country codes
            - country_name: Comma-separated list of country names
    """
    df['country_code'] = None
    df['country_name'] = None

    for idx, row in tqdm(df.iterrows(), total=df.shape[0], desc=f"Processing {media}"):
        country_code, country_name = get_media_origin_country(row['tmdb_id'], media)
        df.at[idx, 'country_code'] = country_code
        df.at[idx, 'country_name'] = country_name

    return df
