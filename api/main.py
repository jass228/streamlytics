"""
@author: Joseph A.
Description:  Main FastAPI application for the Streamlytics API, handling movies and TV series data.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config.db import database
from routers import movies, series, statistics

#pylint: disable = W0718:broad-exception-caught
#pylint: disable = E0401:import-error

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
        print("Database connected successfully")
    except Exception as e:
        print(f"Warning: Failed to connect to database: {e}")
        print("API will run without database - only statistics endpoints will work")

@app.on_event('shutdown')
async def shutdown():
    """Disconnect from the database when the application shuts down
    """
    try:
        if database.is_connected:
            await database.disconnect()
    except Exception as e:
        print(f"Error during database disconnect: {e}")

# Include routers
app.include_router(movies.router, prefix="/api", tags=["Movies"])
app.include_router(series.router, prefix="/api", tags=["Series"])
app.include_router(statistics.router, prefix="/api/stats", tags=["Statistics"])

# API Root
@app.get('/')
def read_root():
    """Get the API welcome message

    Returns:
        dict: A dictionary containing the welcome message
    """
    return JSONResponse(
        content={"message": "Welcome to the Streamlytics API 🎬"},
        media_type="application/json; charset=utf-8"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
