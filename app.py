import asyncio
import uvicorn
from fastapi import FastAPI, Request
from qstash import QStash
import os

import db_service
import file_service

app = FastAPI()

# Initialize Qstash client
qstash_client = QStash(os.getenv("QSTASH_TOKEN"))

BASE_URL = os.getenv("BASE_URL") or "localhost:8000"

@app.get("/")
async def root():
    return {
        "status": 200,
        "total_matches": 0
    }

@app.post("/extract-files")
async def extract_files(request: Request):
    try:
        data = await request.json()
        url = data.get('url')
    except Exception as e:
        return {"error": str(e)}
    if url:
        match_ids = await file_service.extract_files(url)

        try:
            qstash_client.message.enqueue_json(
                queue='processing_queue',
                url=f'{BASE_URL}/insert-matches',
                body={
                    'match_ids': match_ids
                }
            )
        except Exception as e:
            return {"error": str(e)}

        return {
            "status": "ok",
            "total_matches": len(match_ids)
        }
    else:
        return {"error": "No URL provided"}

@app.post("/insert-match")
async def insert_match(request: Request):
    try:
        data = await request.json()
        match_id = data.get('match_id')
    except Exception as e:
        return {"error": str(e)}
    if match_id:
        await db_service.insert_match(match_id)
        return {"status": "ok"}
    else:
        return {"error": "No match_id provided"}

@app.post("/insert-matches")
async def insert_matches(request: Request):
    data = await request.json()
    match_ids = data.get('match_ids')
    if match_ids and len(match_ids) > 0:
        await asyncio.gather(*(db_service.insert_match(match_id) for match_id in match_ids))
        return {"status": "ok"}
    else:
        return {"error": "No match_ids provided"}

if __name__ == "__main__":
    uvicorn.run(app)