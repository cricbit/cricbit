import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
from ingestion import main

app = FastAPI()

@app.get("/")
async def root():
    return {"Status": "OK"}

@app.post("/add-data")
async def add_data(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        url = data.get('url')
        if url:
            background_tasks.add_task(main, url)
            return {"message": "Data ingestion started in the background"}
        else:
            return {"message": "No URL provided"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app)