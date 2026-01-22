"""
@author: Joseph A.
Description: Router for handling statistical data related to movies and TV series
"""
from fastapi import APIRouter, HTTPException
from services.statistics_service import StatisticsService

#pylint: disable = E0401:import-error

router = APIRouter()
stats_service = StatisticsService()

@router.get("/distribution/movies/countries")
async def get_movies_countries_distribution():
    """Get the distribution of movies by country.

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Distribution data containing:
            - data: Dictionary of country counts
            - total: Total number of movies
            - count: Number of unique countries
    """
    try:
        return await stats_service.get_json_data("country_movies_distribution_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/distribution/series/countries")
async def get_tv_countries_distribution():
    """Get the distribution of TV series by country.

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Distribution data containing:
            - data: Dictionary of country counts
            - total: Total number of series
            - count: Number of unique countries
    """
    try:
        return await stats_service.get_json_data("country_series_distribution_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/distribution/movies/genres")
async def get_movies_genres_distribution():
    """Get the distribution of movies by genre.

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Distribution data containing:
            - data: Dictionary of genre counts
            - total: Total number of movies
            - count: Number of unique genres
    """
    try:
        return await stats_service.get_json_data("genres_movies_distribution_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/distribution/series/genres")
async def get_tv_genres_distribution():
    """Get the distribution of TV series by genre.

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Distribution data containing:
            - data: Dictionary of genre counts
            - total: Total number of series
            - count: Number of unique genres
    """
    try:
        return await stats_service.get_json_data("genres_series_distribution_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/distribution/movies/yearly")
async def get_movies_yearly_distribution():
    """

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Ratings data containing:
            - data: Dictionary of country ratings with mean and count
            - total_ratings: Total number of ratings
            - average_rating: Overall average rating
    """
    try:
        return await stats_service.get_json_data("yearly_counts_movies_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/distribution/series/yearly")
async def get_series_yearly_distribution():
    """

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Ratings data containing:
            - data: Dictionary of country ratings with mean and count
            - total_ratings: Total number of ratings
            - average_rating: Overall average rating
    """
    try:
        return await stats_service.get_json_data("yearly_counts_series_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/ratings/movies/countries")
async def get_movies_countries_ratings():
    """Get the average ratings of movies by country.

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Ratings data containing:
            - data: Dictionary of country ratings with mean and count
            - total_ratings: Total number of ratings
            - average_rating: Overall average rating
    """
    try:
        return await stats_service.get_json_data("country_avg_ratings_movies_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/ratings/series/countries")
async def get_series_countries_ratings():
    """Get the average ratings of TV series by country.

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Ratings data containing:
            - data: Dictionary of country ratings with mean and count
            - total_ratings: Total number of ratings
            - average_rating: Overall average rating
    """
    try:
        return await stats_service.get_json_data("country_avg_ratings_series_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/ratings/movies/genres")
async def get_movies_genres_ratings():
    """Get the average ratings of movies by genre.

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Ratings data containing:
            - data: Dictionary of genre ratings with mean and count
            - total_ratings: Total number of ratings
            - average_rating: Overall average rating
    """
    try:
        return await stats_service.get_json_data("genres_avg_ratings_movies_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/ratings/series/genres")
async def get_series_genres_ratings():
    """Get the average ratings of TV series by genre.

    Raises:
        HTTPException: If there is an error accessing or parsing the data file

    Returns:
        dict: Ratings data containing:
            - data: Dictionary of genre ratings with mean and count
            - total_ratings: Total number of ratings
            - average_rating: Overall average rating
    """
    try:
        return await stats_service.get_json_data("genres_avg_ratings_series_latest")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
