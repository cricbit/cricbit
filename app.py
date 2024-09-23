import uvicorn
from fastapi import FastAPI, Request
from ingestion import main

app = FastAPI()

@app.get("/")
async def root():
    return {"Status": "OK"}

@app.post("/add-data")
async def add_data(request: Request):
    data = await request.json()
    url = data.get('url')
    if url:
        response = main(url)
        return {"message": response}
    else:
        return {"message": "No URL provided"}

if __name__ == "__main__":
    uvicorn.run(app)