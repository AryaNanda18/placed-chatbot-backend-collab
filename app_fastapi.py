from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from itertools import cycle
import httpx
import uvicorn
from chat import *

app = FastAPI()

# 1. Combined all your origins into one clean list
origins = [
    "https://www.placededu.com", 
    "https://placededu.com",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

apis = cycle([
    "https://edubuddy-api-0wsz.onrender.com",
    "https://edubuddy-chatbot.onrender.com"
])

# 2. Only ONE middleware block
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def round_robin_proxy(request: Request, path: str):
    # Select the next server in the cycle
    next_server = next(apis)
    target_url = f"{next_server}/{path}"
    
    # Read the incoming request body
    body = await request.body()
    
    # Forward the request using httpx
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=dict(request.headers),
            content=body
        )
        return response.content

@app.get("/")
async def main():
    return {"message": "CORS is configured!"}

class PredictRequest(BaseModel):
    message: str = ""
    
@app.get("/cron-job")
async def cron_job():
    return {"message": "Cron job executed successfully!"}

# 3. CRITICAL FIX: Changed from /predict to /chat to match your Next.js frontend
@app.post("/chat")
async def predict(data: PredictRequest):
    text = data.message
    response = chat(text)
    return {"answer": response}

if __name__ == "__main__":
    uvicorn.run("app_fastapi:app", host='0.0.0.0', port=5000, workers=4)