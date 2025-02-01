"""
@author: Joseph A.
Description: FastAPI router for handling series-related endpoints.
"""
from fastapi import APIRouter, HTTPException
#pylint: disable = E0401:import-error
from config.db import database

router = APIRouter()

# Get all series
@router.get('/series')
async def get_series():
    """Get all series from the database

    Returns:
        list: A list of dictionaries containing series information.
    """
    query = 'SELECT * FROM series;'
    return await database.fetch_all(query)

# Get a serie by tmdb_id
@router.get('/series/{tmdb_id}')
async def get_serie(tmdb_id: int):
    """Get a specific series by its tmdb_id

    Args:
        tmdb_id (int): The tmdb_id of the serie to retrieve

    Returns:
        dict: Series information.
    """
    query = 'SELECT * FROM series WHERE tmdb_id = :tmdb_id;'
    serie = await database.fetch_one(query=query, values={'tmdb_id': tmdb_id})
    if not serie:
        raise HTTPException(status_code=404, detail='Serie not found.')
    return serie
