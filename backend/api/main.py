"""
@author: Joseph A.
Description:  Main FastAPI application for the Streamlytics API, handling movies and TV series data.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import database
from routes.movies import router as movies_router
from routes.series import router as series_router

app = FastAPI(
    title="Streamlytics API",
    description="API for accessing movies and TV series data from netflix",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def startup():
    """Connect to the database when the application starts
    """
    try:
        await database.connect()
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        raise e

@app.on_event('shutdown')
async def shutdown():
    """Disconnect from the database when the application shuts down
    """
    try:
        await database.disconnect()
    except Exception as e:
        print(f"Error during database disconnect: {e}")
        raise e

# Include routers
app.include_router(movies_router)
app.include_router(series_router)

# API Root
@app.get('/')
def read_root():
    """Get the API welcome message

    Returns:
        dict: A dictionary containing the welcome message
    """
    return {"message": "Welcome to the Streamlytics API 🎬"}
