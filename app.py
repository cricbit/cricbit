from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException

from services.db.manager import DatabaseService
from services.file.manager import FileService
import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_service.initialize()
    yield

app = FastAPI(lifespan=lifespan)

db_service = DatabaseService(
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    dbname=config.DB_NAME,
    port=config.DB_PORT
)
file_service = FileService(db_service)

@app.get("/")
async def root():
    total_matches = await db_service.get_total_matches()
    return {
        "status": "ok",
        "total_matches": total_matches
    }

@app.post("/matches/insert")
async def add_matches(request: Request):
    try:
        body = await request.json()
        url = body.get('url')
        if not url:
            raise HTTPException(status_code=400, detail="No URL provided")

        match_ids = await file_service.process_matches_url(url)
        if not match_ids:
            raise HTTPException(status_code=400, detail="No matches found or error processing matches")

        return {
            "status": "ok",
            "total_matches_processed": len(match_ids)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/matches/count")
async def get_total_matches():
    matches_count = await db_service.get_total_matches()
    return {
        "status": "ok",
        "data": {
            "total_matches": matches_count
        }
    }

@app.get("/matches/{match_id}")
async def get_match_by_id(match_id: int):
    match = await db_service.get_match_by_id(match_id)
    return {
        "status": "ok",
        "data": {
            "match": match
        }
    }

@app.post("/matches/{match_id}")
async def insert_match(match_id: int, request: Request):
   try:
       body = await request.json()
       match_data = body.get('match_data')
       if not match_data:
           raise HTTPException(status_code=400, detail="No match data provided")

       await db_service.insert_match(match_id, match_data)
       return {
           "status": "ok",
           "data": {
               "match_id": match_id
           }
       }
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

@app.post("/players")
async def update_players(request: Request):
    body = await request.json()
    url = body.get('url')
    if not url:
        raise HTTPException(status_code=400, detail="No URL provided")

    await file_service.process_players_url(url)
    return {
        "status": "ok",
        "data": {
            "players_count": await db_service.get_players_count()
        }
    }

@app.post("/db/initialize")
async def initialize_db():
    await db_service.initialize()
    return {
        "status": "ok"
    }
