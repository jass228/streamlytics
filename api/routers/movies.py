"""
@author: Joseph A.
Description: FastAPI router for handling movies-related endpoints.
"""
from fastapi import APIRouter,HTTPException
#pylint: disable = E0401:import-error
from config.db import database

router = APIRouter()

# Get all movies
@router.get('/movies')
async def get_movies():
    """Get all movies from the database

    Returns:
        list: A list of dictionaries containing movies information.
    """
    query = 'SELECT * FROM movies;'
    return await database.fetch_all(query)

# Get a movie by tmdb_id
@router.get('/movies/{tmdb_id}')
async def get_movie(tmdb_id: int):
    """Get a specific movies by its tmdb_id

    Args:
        tmdb_id (int): The tmdb_id of the movie to retrieve

    Returns:
        dict: Movie information
    """
    query = 'SELECT * FROM movies WHERE tmdb_id = :tmdb_id;'
    movie = await database.fetch_one(query=query, values={'tmdb_id': tmdb_id})
    if not movie:
        raise HTTPException(status_code=404, detail='Movie not found.')
    return movie
