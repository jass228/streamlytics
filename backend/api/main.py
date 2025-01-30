from fastapi import FastAPI
from config.db import database
from routes.movies import router as movies_router
from routes.series import router as series_router

app = FastAPI()

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

app.include_router(movies_router)
app.include_router(series_router)

# API Root
@app.get('/')
def read_root():
    return {"message": "Welcome to the Streamlytics API 🎬"}
