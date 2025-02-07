"""
@author: Joseph A.
Description: FastAPI router for handling movies-related endpoints.
"""
from fastapi import APIRouter,HTTPException
#pylint: disable = E0401:import-error
from config.db import db

router = APIRouter()

# Get all movies
@router.get('/movies')
async def get_movies():
    """Get all movies from the database

    Returns:
        list: A list of dictionnaries containing movies information.
    """
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM movies')
        columns = [desc[0] for desc in cursor.description]
        movies = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return movies

# Get a movie by tmdb_id
@router.get('/movies/{tmdb_id}')
async def get_movie(tmdb_id: int):
    """Get a specific movies by its tmdb_id

    Args:
        tmdb_id (int): The tmdb_id of the movie to retrieve

    Returns:
        dict: Movie information
    """
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM movies WHERE tmdb_id = %s', (tmdb_id,))
        columns = [desc[0] for desc in cursor.description]
        movie = cursor.fetchone()

        if not movie:
            raise HTTPException(status_code=404, detail='Movie not found.')
    return dict(zip(columns, movie))
