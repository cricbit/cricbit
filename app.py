import uvicorn
from fastapi import FastAPI, Request

import file_service
app = FastAPI()

@app.get("/")
async def root():
    return {"Status": "OK"}

@app.post("/extract-files")
async def extract_files(request: Request):
    try:
        data = await request.json()
        url = data.get('url')
    except Exception as e:
        return {"error": str(e)}
    if url:
        file_urls = await file_service.extract_files(url)
        return file_urls
    else:
        return {"error": "No URL provided"}

if __name__ == "__main__":
    uvicorn.run(app)