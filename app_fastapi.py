from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
    "https://edubuddy-chatbot.onrender.com"
]

# 2. Only ONE middleware block
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    uvicorn.run(app, host='0.0.0.0', port=5000)