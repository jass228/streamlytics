"""
@author: Joseph A.
Description: FastAPI router for handling series-related endpoints.
"""
from fastapi import APIRouter, HTTPException
#pylint: disable = E0401:import-error
from config.db import db

router = APIRouter()

# Get all series
@router.get('/series')
async def get_series():
    """Get all series from the database

    Returns:
        list: A list of dictionaries containing series information.
    """
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM series')
        columns = [desc[0] for desc in cursor.description]
        series = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return series

# Get a serie by tmdb_id
@router.get('/series/{tmdb_id}')
async def get_serie(tmdb_id: int):
    """Get a specific series by its tmdb_id

    Args:
        tmdb_id (int): The tmdb_id of the serie to retrieve

    Returns:
        dict: Series information.
    """
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM series WHERE tmdb_id = %s', (tmdb_id,))
        columns = [desc[0] for desc in cursor.description]
        serie = cursor.fetchone()

        if not serie:
            raise HTTPException(status_code=404, detail='Serie not found.')

        return dict(zip(columns, serie))
