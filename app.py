import asyncio
import uvicorn
from fastapi import FastAPI, Request
from qstash import QStash
import os

import db_service
import file_service
from redis_resource import get_redis

app = FastAPI()

# Initialize Qstash client
qstash_client = QStash(os.getenv("QSTASH_TOKEN"))

@app.get("/")
async def root():
    return {
        "status": 200,
        "total_matches": get_redis('total_matches'),
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

        return {
            "status": "ok",
            "extracted_files": len(match_ids),
            "queued_tasks": len(match_ids)
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

if __name__ == "__main__":
    uvicorn.run(app)